"""reasoning_verify.py — verify the REASONING, not the label.

Architecture (per the new design):
  Stage 1 (Sonnet 4.6): classify branded/unbranded AND give a longer,
      *verifiable* justification that cites the specific words in the title.
  Stage 2 (GPT-4o, logprobs): audit whether that justification is logically
      sound and fully supported by the title. It does NOT judge whether the
      label is the one it would pick — only whether the reasoning holds (no
      invented brand, no descriptive word/abbreviation/code mistaken for a
      maker). The label itself is immaterial.

Confidence = P(reasoning is sound) = renormalized prob mass on the verifier's
"Yes" token (real logprob, OpenAI cookbook recipe). Low confidence => the
justification is shaky => route to human review.

Usage:
    python reasoning_verify.py [--input dual_stage_scored.csv]
        [--output dual_stage_reasoning_retry.csv] [--grey 0.85] [--workers 4]
"""

import argparse
import concurrent.futures
import csv
import json
import logging
import math
import os
import sys
import threading

from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI

from dual_stage_confidence import call_with_retry, EPSILON, SYSTEM

log = logging.getLogger("reasoning_verify")

STAGE1_MODEL = "claude-sonnet-4-6"
STAGE2_MODEL = "gpt-4o"

# Stage 1: prediction + a longer, evidence-citing justification.
STAGE1_INSTRUCT = (
    "Classify this product title as branded or unbranded, then justify it.\n\n"
    "In your justification (2-4 sentences) identify the specific word(s) in the "
    "title that could signal a brand, and for EACH one state whether it is a "
    "real maker/company name or just a descriptive term (product type, "
    "ingredient, material, size, flavor, style, or internal code). Base every "
    "claim only on the title — do not assume facts that are not present.\n\n"
    'Respond ONLY as JSON: {{"classification": "branded" or "unbranded", '
    '"justification": "..."}}\n\n'
    "Product title: {title!r}")

# Stage 2: audit the reasoning, not the label.
VERIFY_SYSTEM = (
    "You audit the REASONING behind a product classification. You receive a "
    "product title, a proposed label, and a justification for that label. Judge "
    "ONLY whether the justification is logically sound and fully supported by "
    "the title: are its claims about the words true, and does its conclusion "
    "follow from them? Do NOT judge whether you personally would choose the same "
    "label — the label is immaterial. A justification is UNSOUND if it invents a "
    "maker not present in the title, or treats a descriptive word, abbreviation, "
    "measurement, or internal code as a brand. Reply with exactly one word: "
    "Yes (reasoning is sound) or No (reasoning is flawed).")

VERIFY_USER = (
    "Product title: {title!r}\n"
    "Proposed label: {cls}\n"
    "Justification: {justification}\n\n"
    "Is the justification sound and fully supported by the title? "
    "Reply strictly with either 'Yes' or 'No'.")


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def stage1_classify(aclient, title):
    resp = call_with_retry(lambda: aclient.messages.create(
        model=STAGE1_MODEL, max_tokens=300, system=SYSTEM,
        messages=[{"role": "user",
                   "content": STAGE1_INSTRUCT.format(title=title)}]))
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    raw = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        obj = json.loads(raw)
        cls = str(obj.get("classification", "")).strip().lower()
        justification = str(obj.get("justification", "")).strip()
        if cls in ("branded", "unbranded"):
            return cls, justification
    except (json.JSONDecodeError, AttributeError):
        pass
    low = text.lower()
    cls = "unbranded" if "unbranded" in low else ("branded" if "branded" in low else "")
    return cls, text[:300]


def verify_reasoning(oclient, title, cls, justification):
    """GPT-4o audits the justification; returns P(reasoning is sound)."""
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=STAGE2_MODEL,
        messages=[{"role": "system", "content": VERIFY_SYSTEM},
                  {"role": "user", "content": VERIFY_USER.format(
                      title=title, cls=cls, justification=justification or "n/a")}],
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
    if p_yes == 0.0 and chosen.token.strip().lower().startswith("y"):
        p_yes = raw_conf
    if p_no == 0.0 and chosen.token.strip().lower().startswith("n"):
        p_no = raw_conf
    p_sound = (p_yes + EPSILON) / (p_yes + p_no + 2 * EPSILON)
    return chosen.token.strip(), p_sound, raw_conf


def process_row(aclient, oclient, title):
    cls, justification = stage1_classify(aclient, title)
    if not cls:
        raise ValueError("stage 1 produced no class")
    token, p_sound, raw_conf = verify_reasoning(oclient, title, cls, justification)
    return {"pred": cls, "justification": justification,
            "verifier_token": token, "confidence": round(p_sound, 4),
            "raw_conf": round(raw_conf, 4)}


def main():
    ap = argparse.ArgumentParser(description="Reasoning-verification confidence.")
    ap.add_argument("--input", default="dual_stage_scored.csv")
    ap.add_argument("--output", default="dual_stage_reasoning_retry.csv")
    ap.add_argument("--grey", type=float, default=0.85,
                    help="review threshold: confidence <= this => human review")
    ap.add_argument("--select", type=float, default=None,
                    help="score rows whose ORIGINAL confidence <= this "
                         "(default = --grey; set >=1.0 to score all rows)")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    select = args.select if args.select is not None else args.grey

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    missing = [k for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")
               if not os.environ.get(k)]
    if missing:
        sys.exit(f"missing env var(s): {', '.join(missing)}")

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        all_rows = list(csv.DictReader(fh))
    grey = [r for r in all_rows
            if (c := to_float(r.get("confidence"))) is not None and c <= select
            and (r.get("title") or "").strip()]
    log.info("re-scoring %d rows (orig conf <= %.2f; reasoning-verification) of %d total",
             len(grey), select, len(all_rows))

    aclient, oclient = Anthropic(), OpenAI()
    results = [None] * len(grey)
    lock, done = threading.Lock(), [0]

    def worker(i):
        title = grey[i]["title"].strip()
        try:
            res, err = process_row(aclient, oclient, title), ""
        except Exception as exc:
            log.error("row %r failed: %s", title, exc)
            res, err = None, f"{type(exc).__name__}: {exc}"
        with lock:
            done[0] += 1
            if done[0] % 20 == 0:
                log.info("processed %d/%d", done[0], len(grey))
        return i, res, err

    with concurrent.futures.ThreadPoolExecutor(args.workers) as pool:
        for i, res, err in pool.map(worker, range(len(grey))):
            results[i] = (res, err)

    cols = ["title", "brand", "old_pred", "old_conf", "new_pred",
            "reasoning_conf", "conf_delta", "escaped_grey", "verifier_token",
            "justification", "error"]
    out_rows = []
    for r, (res, err) in zip(grey, results):
        old_conf = to_float(r.get("confidence"))
        row = {"title": r["title"].strip(),
               "brand": (r.get("brand") or "").strip(),
               "old_pred": r.get("pred_brand", ""),
               "old_conf": round(old_conf, 4) if old_conf is not None else "",
               "new_pred": "", "reasoning_conf": "", "conf_delta": "",
               "escaped_grey": "", "verifier_token": "", "justification": "",
               "error": err}
        if res:
            rc = res["confidence"]
            row.update({"new_pred": res["pred"], "reasoning_conf": rc,
                        "conf_delta": round(rc - (old_conf or 0), 4),
                        "escaped_grey": rc > args.grey,
                        "verifier_token": res["verifier_token"],
                        "justification": res["justification"]})
        out_rows.append(row)

    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)
    log.info("wrote %s", args.output)

    scored = [r for r in out_rows if r["reasoning_conf"] != ""]
    escaped = sum(1 for r in scored if r["escaped_grey"])
    still = len(scored) - escaped
    prior_total = sum(1 for r in all_rows if to_float(r.get("confidence")) is not None)
    log.info("=" * 60)
    log.info("grey rows re-scored:            %d", len(scored))
    log.info("reasoning judged SOUND (>%.2f):  %d (%.0f%%)",
             args.grey, escaped, 100 * escaped / len(scored) if scored else 0)
    log.info("reasoning still shaky (<=%.2f):  %d", args.grey, still)
    log.info("review queue: %d -> %d of %d scored (%.1f%% -> %.1f%%)",
             len(scored), still, prior_total,
             100 * len(scored) / prior_total, 100 * still / prior_total)


if __name__ == "__main__":
    main()
