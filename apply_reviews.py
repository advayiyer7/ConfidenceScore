"""apply_reviews.py — propagate human review verdicts back to the catalog.

Reads a review_queue.csv whose `human_label` column has been (partially)
filled with 'branded' / 'unbranded', applies each verdict to every affected
title (entity decisions fan out to all titles carrying that entity), and
writes the merged predictions with reviewed rows at confidence 1.0 and
deciding_entity marked '(human)'.

Rows left blank in the queue stay grey — review can be done in batches.

Usage:
    python apply_reviews.py [--queue review_queue.csv]
        [--predictions final_predictions.csv]
        [--input dual_stage_scored.csv] [--out reviewed_predictions.csv]
"""
from __future__ import annotations

import argparse
import csv
import sys

from entity_extract import resolve_entities

VALID = {"branded", "unbranded"}


def main() -> None:
    ap = argparse.ArgumentParser(description="Apply human review verdicts.")
    ap.add_argument("--queue", default="review_queue.csv")
    ap.add_argument("--predictions", default="final_predictions.csv")
    ap.add_argument("--input", default="dual_stage_scored.csv")
    ap.add_argument("--title-col", default="title")
    ap.add_argument("--out", default="reviewed_predictions.csv")
    args = ap.parse_args()

    queue = list(csv.DictReader(open(args.queue, encoding="utf-8-sig")))
    verdicts = [q for q in queue if q.get("human_label", "").strip()]
    bad = [q for q in verdicts
           if q["human_label"].strip().lower() not in VALID]
    if bad:
        sys.exit(f"invalid human_label values (use branded/unbranded): "
                 f"{[q['decision_key'] for q in bad][:5]}")
    if not verdicts:
        sys.exit("no filled human_label rows in the queue — nothing to apply")

    ent_verdict = {q["decision_key"]: q["human_label"].strip().lower()
                   for q in verdicts if q["decision_type"] == "entity"}
    title_verdict = {q["decision_key"]: q["human_label"].strip().lower()
                     for q in verdicts if q["decision_type"] == "title"}

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        titles = [r[args.title_col].strip() for r in csv.DictReader(fh)
                  if r.get(args.title_col, "").strip()]
    _, title_keys = resolve_entities(titles)

    preds = list(csv.DictReader(open(args.predictions, encoding="utf-8-sig")))
    applied = 0
    out_rows = []
    for r in preds:
        title = r["title"]
        row = [title, r["prediction"], float(r["confidence"]),
               r["deciding_entity"]]
        if title in title_verdict:
            row = [title, title_verdict[title], 1.0, "(human)"]
            applied += 1
        else:
            hit = next((k for k in title_keys.get(title, [])
                        if k in ent_verdict), None)
            # an entity verdict overrides only rows that entity decided, or
            # branded verdicts anywhere the entity appears (a confirmed maker
            # makes the title branded regardless of other tokens)
            if hit and (r["deciding_entity"] == hit
                        or ent_verdict[hit] == "branded"):
                row = [title, ent_verdict[hit], 1.0, "(human)"]
                applied += 1
        out_rows.append(row)

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["title", "prediction", "confidence", "deciding_entity"])
        for r in sorted(out_rows, key=lambda x: x[2]):
            w.writerow(r)

    grey = sum(1 for r in out_rows if float(r[2]) <= 0.85)
    print(f"verdicts in queue: {len(verdicts)} "
          f"({len(ent_verdict)} entity + {len(title_verdict)} title)")
    print(f"titles updated:    {applied}")
    print(f"grey remaining:    {grey}/{len(out_rows)} "
          f"({100 * grey / len(out_rows):.1f}%)")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
