"""brand_confidence.py — logprob confidence for branded vs. unbranded.

For each product title the model answers a single forced token — "B" (branded)
or "U" (unbranded) — with logprobs enabled. Confidence follows the OpenAI
cookbook classification recipe: the linear probability of the chosen token,

    confidence = exp(logprob_of_chosen_token)

which is already a true probability (softmax over the full vocabulary), so no
renormalization is needed. `p_branded` (renormalized over just B/U) is reported
alongside for reference. This is a real token logprob — the model's own
probability for the class — not a self-reported number. No quantity, no
estimation: the only question is branded vs. unbranded.

Input CSV needs a `title` column (and optionally a `brand` gold label, carried
through for scoring). Output adds: pred_brand, confidence, p_branded.

Usage:
    python brand_confidence.py --input brand_eval.csv --output brand_eval_scored.csv \
        [--model gpt-4o] [--workers 3]
"""

import argparse
import concurrent.futures
import csv
import logging
import math
import os
import random
import sys
import threading
import time

from openai import (
    APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError,
)

log = logging.getLogger("brand_confidence")
EPSILON = 1e-6

SYSTEM = (
    "You classify grocery catalog products as BRANDED or UNBRANDED. "
    "BRANDED = sold under a specific company/brand name (e.g. Amul, Maggi, "
    "Haldiram, Britannia). UNBRANDED = generic, loose, or commodity items with "
    "no brand (e.g. Onion, Curry Leaves, Tomato, Paneer).")


def call_with_retry(fn, max_retries=5):
    last = None
    for attempt in range(max_retries):
        try:
            return fn()
        except (RateLimitError, APIConnectionError, APITimeoutError) as exc:
            last = exc
        except APIStatusError as exc:
            if exc.status_code < 500:
                raise
            last = exc
        time.sleep(min(30.0, (2 ** attempt) + random.uniform(0, 1)))
    raise last


def classify(client, model, title):
    """Classify branded/unbranded with logprobs.

    Confidence follows the OpenAI cookbook classification recipe exactly: the
    linear probability of the actually-chosen output token, `exp(logprob)`.
    That value is already a true probability (softmax over the whole
    vocabulary), so no renormalization is needed. `p_branded` (renormalized
    over just B/U) is reported alongside for reference.
    """
    prompt = (f"Product title: {title!r}\n\n"
              "Is this product branded or unbranded? "
              "Answer with a single letter: B for branded, U for unbranded.")
    resp = call_with_retry(lambda: client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": prompt}],
        temperature=0, max_tokens=1, logprobs=True, top_logprobs=5))

    content = resp.choices[0].logprobs.content
    if not content:
        raise ValueError("no logprobs at answer position")
    chosen = content[0]
    token = chosen.token.strip().upper()

    # Cookbook confidence: linear probability of the chosen token.
    confidence = math.exp(chosen.logprob)

    # Prediction from the chosen token; fall back to renormalized B/U mass.
    p_b = p_u = 0.0
    for entry in chosen.top_logprobs:
        t = entry.token.strip().upper()
        if t.startswith("B"):
            p_b += math.exp(entry.logprob)
        elif t.startswith("U"):
            p_u += math.exp(entry.logprob)
    p_branded = (p_b + EPSILON) / (p_b + p_u + 2 * EPSILON)
    if token.startswith("B"):
        pred = "branded"
    elif token.startswith("U"):
        pred = "unbranded"
    else:
        pred = "branded" if p_branded >= 0.5 else "unbranded"
    return pred, confidence, p_branded, chosen.logprob


def process_row(client, row, model, title_col):
    title = (row.get(title_col) or "").strip()
    if not title:
        return {"pred_brand": "", "confidence": "", "p_branded": "",
                "logprob": ""}, ""
    try:
        pred, confidence, p_branded, logprob = classify(client, model, title)
        return {"pred_brand": pred,
                "confidence": round(confidence, 4),
                "p_branded": round(p_branded, 4),
                "logprob": round(logprob, 6)}, ""
    except Exception as exc:
        log.error("row %r failed: %s", title, exc)
        return {"pred_brand": "", "confidence": "", "p_branded": "",
                "logprob": ""}, f"{type(exc).__name__}: {exc}"


def main():
    ap = argparse.ArgumentParser(
        description="Logprob confidence for branded vs unbranded.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output")
    ap.add_argument("--model", default="gpt-4o")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--title-col", default="title",
                    help="column holding the product title")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY environment variable is not set")
    client = OpenAI()
    out_path = args.output or "brand_eval_scored.csv"

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    log.info("read %d rows from %s", len(rows), args.input)

    results = [None] * len(rows)
    lock, done = threading.Lock(), [0]

    def worker(i):
        res, err = process_row(client, rows[i], args.model, args.title_col)
        with lock:
            done[0] += 1
            if done[0] % 25 == 0:
                log.info("processed %d/%d", done[0], len(rows))
        return i, res, err

    with concurrent.futures.ThreadPoolExecutor(args.workers) as pool:
        for i, res, err in pool.map(worker, range(len(rows))):
            results[i] = (res, err)

    new_cols = ["pred_brand", "confidence", "p_branded", "logprob"]
    out_fields = fieldnames + [c for c in new_cols if c not in fieldnames]
    if "error" not in out_fields:
        out_fields.append("error")
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=out_fields)
        w.writeheader()
        for row, (res, err) in zip(rows, results):
            out = dict(row); out.update(res)
            if err:
                out["error"] = err
            w.writerow(out)
    log.info("wrote %s", out_path)

    scored = [(r, res) for r, (res, _) in zip(rows, results)
              if res["confidence"] != ""]
    if scored and all("brand" in r for r, _ in scored):
        def gold_cls(r):
            b = (r.get("brand") or "").strip().lower()
            return "unbranded" if b in ("unbranded", "") else "branded"
        correct = sum(1 for r, res in scored
                      if res["pred_brand"] == gold_cls(r))
        log.info("accuracy vs gold (brand col -> branded/unbranded): "
                 "%d/%d = %.1f%%",
                 correct, len(scored), 100 * correct / len(scored))


if __name__ == "__main__":
    main()
