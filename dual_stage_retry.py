"""dual_stage_retry.py — re-score only the grey-zone rows with improved prompts.

Reads a prior dual-stage scored file, selects every row whose confidence was at
or below the grey-zone threshold (default 0.85 → human-review queue), and
re-runs the same two-stage pipeline (Sonnet predict → GPT-4o logprob verify)
using the *improved* prompts now in dual_stage_confidence.py.

The goal is to shrink the human-review queue: most grey rows were Stage-1 brand
hallucinations (treating "SS", "Danish", "Boba", internal codes as brands). The
sharper prompt should make Stage 1 correct, so the verifier agrees confidently
and the row leaves the grey zone.

Output (dual_stage_grey_retry.csv) is a before/after comparison so the
improvement is auditable per row.

Usage:
    python dual_stage_retry.py [--input dual_stage_scored.csv]
        [--output dual_stage_grey_retry.csv] [--grey 0.85] [--workers 3]
"""

import argparse
import concurrent.futures
import csv
import logging
import os
import sys
import threading

from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI

from dual_stage_confidence import process_row

log = logging.getLogger("dual_stage_retry")


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser(description="Re-score grey-zone rows with improved prompts.")
    ap.add_argument("--input", default="dual_stage_scored.csv")
    ap.add_argument("--output", default="dual_stage_grey_retry.csv")
    ap.add_argument("--grey", type=float, default=0.85,
                    help="rows with confidence <= this were the review queue")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

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
            if (c := to_float(r.get("confidence"))) is not None and c <= args.grey
            and (r.get("title") or "").strip()]
    log.info("re-scoring %d grey rows (confidence <= %.2f) of %d total",
             len(grey), args.grey, len(all_rows))

    aclient, oclient = Anthropic(), OpenAI()
    results = [None] * len(grey)
    lock, done = threading.Lock(), [0]

    def worker(i):
        title = grey[i]["title"].strip()
        try:
            res = process_row(aclient, oclient, title)
            err = ""
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

    cols = ["title", "brand", "old_pred", "old_conf", "new_pred", "new_conf",
            "conf_delta", "pred_changed", "escaped_grey", "verifier_token",
            "new_reasoning", "error"]
    out_rows = []
    for r, (res, err) in zip(grey, results):
        old_conf = to_float(r.get("confidence"))
        row = {
            "title": r["title"].strip(),
            "brand": (r.get("brand") or "").strip(),
            "old_pred": r.get("pred_brand", ""),
            "old_conf": round(old_conf, 4) if old_conf is not None else "",
            "new_pred": "", "new_conf": "", "conf_delta": "",
            "pred_changed": "", "escaped_grey": "",
            "verifier_token": "", "new_reasoning": "", "error": err,
        }
        if res:
            new_conf = res["confidence"]
            row.update({
                "new_pred": res["pred_brand"],
                "new_conf": new_conf,
                "conf_delta": round(new_conf - (old_conf or 0), 4),
                "pred_changed": res["pred_brand"] != r.get("pred_brand", ""),
                "escaped_grey": new_conf > args.grey,
                "verifier_token": res["verifier_token"],
                "new_reasoning": res["stage1_reasoning"],
            })
        out_rows.append(row)

    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out_rows)
    log.info("wrote %s", args.output)

    scored = [r for r in out_rows if r["new_conf"] != ""]
    escaped = sum(1 for r in scored if r["escaped_grey"])
    changed = sum(1 for r in scored if r["pred_changed"])
    still_grey = len(scored) - escaped
    log.info("=" * 60)
    log.info("grey rows re-scored:        %d", len(scored))
    log.info("left the grey zone (>%.2f):  %d (%.0f%%)",
             args.grey, escaped, 100 * escaped / len(scored) if scored else 0)
    log.info("still grey (<=%.2f):         %d", args.grey, still_grey)
    log.info("prediction flipped:         %d", changed)
    new_queue = len(all_rows) - (len([r for r in all_rows if to_float(r.get("confidence")) is not None]) ) + still_grey
    prior_total = len([r for r in all_rows if to_float(r.get("confidence")) is not None])
    log.info("review queue: %d -> %d of %d scored (%.1f%% -> %.1f%%)",
             len(scored), still_grey, prior_total,
             100 * len(scored) / prior_total, 100 * still_grey / prior_total)


if __name__ == "__main__":
    main()
