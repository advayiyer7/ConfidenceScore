"""dual_stage_confidence.py — two-stage branded/unbranded confidence.

Stage 1 (answer):    Claude Sonnet 4.6 classifies the product title as
                     branded/unbranded AND returns a short reasoning.
Stage 2 (confidence): GPT-4o verifies Stage 1's answer with logprobs on a
                     forced single Yes/No token. The verifier is
                     *reasoning-augmented*: it is shown Stage 1's reasoning
                     as context (per the agreed design).

Final confidence = P(Yes) renormalized over the {Yes, No} tokens — the
verifier's probability that Stage 1's class is correct. This is a real token
logprob (OpenAI cookbook recipe), not a self-reported number. GPT-5/reasoning
models block logprobs, which is why GPT-4o is the confidence stage.

Output is schema-compatible with brand_analysis.py (title, brand, pred_brand,
confidence, p_branded) so the existing analysis harness can score it.

Usage:
    python dual_stage_confidence.py --input distinct_products_po_1000.csv \
        --output dual_stage_scored.csv [--limit 10] [--workers 3]
"""

import argparse
import concurrent.futures
import csv
import json
import logging
import math
import os
import random
import sys
import threading
import time

import anthropic
import openai
from anthropic import Anthropic
from dotenv import load_dotenv
from openai import (
    APIConnectionError, APIStatusError, APITimeoutError, OpenAI, RateLimitError,
)

log = logging.getLogger("dual_stage")
EPSILON = 1e-6

STAGE1_MODEL = "claude-sonnet-4-6"
STAGE2_MODEL = "gpt-4o"

SYSTEM = (
    "You classify grocery/catalog products as BRANDED or UNBRANDED using ONLY "
    "the product title.\n\n"
    "A product is BRANDED only when the title names a real maker — a "
    "manufacturer or company name that identifies WHO makes or sells the item.\n\n"
    "A product is UNBRANDED when the title only describes WHAT the item is — its "
    "type, ingredient, material, size, flavor, shape, or function — without "
    "naming a maker.\n\n"
    "Judge the words by what they mean, not by whether they are capitalized. A "
    "word in caps, an abbreviation, a measurement, or an internal code is not a "
    "brand unless you actually recognize it as a company. Do not turn the "
    "product's own descriptive name into a brand. If no part of the title "
    "clearly identifies a real maker, classify it UNBRANDED; when genuinely "
    "uncertain, choose UNBRANDED.")

STAGE1_INSTRUCT = (
    'Classify this product title. Respond ONLY with a JSON object: '
    '{{"classification": "branded" or "unbranded", "reasoning": '
    '"one short sentence"}}.\n\nProduct title: {title!r}')

VERIFY_SYSTEM = (
    "You verify whether a product's BRANDED/UNBRANDED classification is correct, "
    "judging ONLY from the title. A product is BRANDED only when the title names "
    "a real maker (manufacturer or company). A word in caps, an abbreviation, a "
    "measurement, an internal code, or the product's own descriptive name does "
    "not count as a brand unless it is genuinely a recognizable company. If no "
    "real maker is named, the correct label is UNBRANDED. Reply with exactly one "
    "word: Yes or No.")

VERIFY_USER = (
    "Product title: {title!r}\n"
    "A classifier labeled this product as: {cls}\n"
    "Classifier's reasoning: {reasoning}\n\n"
    "Is this classification correct given the product title? "
    "Reply strictly with either 'Yes' or 'No'.")


def call_with_retry(fn, max_retries=5):
    last = None
    for attempt in range(max_retries):
        try:
            return fn()
        except (RateLimitError, APIConnectionError, APITimeoutError,
                anthropic.RateLimitError, anthropic.APIConnectionError,
                anthropic.APITimeoutError) as exc:
            last = exc
        except (APIStatusError, anthropic.APIStatusError) as exc:
            if getattr(exc, "status_code", 500) < 500:
                raise
            last = exc
        time.sleep(min(30.0, (2 ** attempt) + random.uniform(0, 1)))
    raise last


def stage1_classify(aclient, title):
    """Sonnet 4.6: branded/unbranded + short reasoning."""
    resp = call_with_retry(lambda: aclient.messages.create(
        model=STAGE1_MODEL, max_tokens=200, system=SYSTEM,
        messages=[{"role": "user",
                   "content": STAGE1_INSTRUCT.format(title=title)}]))
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    cls, reasoning = parse_stage1(text)
    return cls, reasoning


def parse_stage1(text):
    raw = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
    try:
        obj = json.loads(raw)
        cls = str(obj.get("classification", "")).strip().lower()
        reasoning = str(obj.get("reasoning", "")).strip()
        if cls in ("branded", "unbranded"):
            return cls, reasoning
    except (json.JSONDecodeError, AttributeError):
        pass
    low = text.lower()
    cls = "unbranded" if "unbranded" in low else ("branded" if "branded" in low
                                                  else "")
    return cls, text[:200]


def stage2_verify(oclient, title, cls, reasoning):
    """GPT-4o verifier with logprobs; returns P(class is correct)."""
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=STAGE2_MODEL,
        messages=[{"role": "system", "content": VERIFY_SYSTEM},
                  {"role": "user", "content": VERIFY_USER.format(
                      title=title, cls=cls, reasoning=reasoning or "n/a")}],
        temperature=0, max_tokens=1, logprobs=True, top_logprobs=5))
    content = resp.choices[0].logprobs.content
    if not content:
        raise ValueError("no logprobs at answer position")
    chosen = content[0]
    raw_conf = math.exp(chosen.logprob)

    p_yes = p_no = 0.0
    for entry in chosen.top_logprobs:
        t = entry.token.strip().lower()
        if t.startswith("y"):
            p_yes += math.exp(entry.logprob)
        elif t.startswith("n"):
            p_no += math.exp(entry.logprob)
    # If only the chosen token had mass, seed it so renormalization is defined.
    if p_yes == 0.0 and chosen.token.strip().lower().startswith("y"):
        p_yes = raw_conf
    if p_no == 0.0 and chosen.token.strip().lower().startswith("n"):
        p_no = raw_conf
    p_correct = (p_yes + EPSILON) / (p_yes + p_no + 2 * EPSILON)
    return chosen.token.strip(), p_correct, raw_conf, chosen.logprob


def process_row(aclient, oclient, title):
    cls, reasoning = stage1_classify(aclient, title)
    if not cls:
        raise ValueError("stage 1 produced no class")
    token, p_correct, raw_conf, logprob = stage2_verify(
        oclient, title, cls, reasoning)
    return {
        "pred_brand": cls,
        "stage1_reasoning": reasoning,
        "verifier_token": token,
        "confidence": round(p_correct, 4),
        "raw_conf": round(raw_conf, 4),
        "logprob": round(logprob, 6),
        "p_branded": "",
    }


def main():
    ap = argparse.ArgumentParser(description="Two-stage Sonnet->GPT-4o confidence.")
    ap.add_argument("--input", default="distinct_products_po_1000.csv")
    ap.add_argument("--output", default="dual_stage_scored.csv")
    ap.add_argument("--title-col", default="product_title")
    ap.add_argument("--brand-col", default="brand")
    ap.add_argument("--limit", type=int, default=0,
                    help="score only the first N rows (0 = all)")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    missing = [k for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")
               if not os.environ.get(k)]
    if missing:
        sys.exit(f"missing env var(s): {', '.join(missing)}")

    aclient, oclient = Anthropic(), OpenAI()

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if args.limit:
        rows = rows[:args.limit]
    log.info("scoring %d rows (stage1=%s, stage2=%s)",
             len(rows), STAGE1_MODEL, STAGE2_MODEL)

    results = [None] * len(rows)
    lock, done = threading.Lock(), [0]

    def worker(i):
        title = (rows[i].get(args.title_col) or "").strip()
        try:
            res = process_row(aclient, oclient, title) if title else None
            err = "" if title else "empty title"
        except Exception as exc:
            log.error("row %r failed: %s", title, exc)
            res, err = None, f"{type(exc).__name__}: {exc}"
        with lock:
            done[0] += 1
            if done[0] % 25 == 0:
                log.info("processed %d/%d", done[0], len(rows))
        return i, res, err

    with concurrent.futures.ThreadPoolExecutor(args.workers) as pool:
        for i, res, err in pool.map(worker, range(len(rows))):
            results[i] = (res, err)

    cols = ["title", "brand", "pred_brand", "confidence", "p_branded",
            "raw_conf", "logprob", "verifier_token", "stage1_reasoning", "error"]
    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row, (res, err) in zip(rows, results):
            out = {"title": (row.get(args.title_col) or "").strip(),
                   "brand": (row.get(args.brand_col) or "").strip(),
                   "error": err}
            if res:
                out.update(res)
            w.writerow(out)
    log.info("wrote %s", args.output)

    scored = [(r, res) for r, (res, _) in zip(rows, results) if res]

    def gold_cls(r):
        b = (r.get(args.brand_col) or "").strip().lower()
        return "unbranded" if b.startswith("unbrand") or b == "" else "branded"

    if scored:
        correct = sum(1 for r, res in scored if res["pred_brand"] == gold_cls(r))
        log.info("stage1 accuracy vs noisy catalog gold: %d/%d = %.1f%%",
                 correct, len(scored), 100 * correct / len(scored))


if __name__ == "__main__":
    main()
