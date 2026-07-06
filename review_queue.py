"""review_queue.py — turn the grey zone into the smallest possible set of
one-glance human decisions.

The grey zone is title-shaped (266 rows) but the DECISIONS are entity-shaped:
reviewing 'murukku' once resolves all 9 titles that carry it. This script
groups grey titles by deciding entity, orders the queue by impact (titles
cleared per decision) then by depth of uncertainty, and emits a CSV with the
full probe evidence so a reviewer can answer each row in seconds.

Fill the `human_label` column with 'branded' / 'unbranded' (leave blank to
skip) and run apply_reviews.py to propagate verdicts back to every affected
title at confidence 1.0.

Usage:
    python review_queue.py [--predictions final_predictions.csv]
        [--entities final_entity_decisions.csv] [--grey 0.85]
        [--out review_queue.csv]
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the human review queue.")
    ap.add_argument("--predictions", default="final_predictions.csv")
    ap.add_argument("--entities", default="final_entity_decisions.csv")
    ap.add_argument("--grey", type=float, default=0.85)
    ap.add_argument("--out", default="review_queue.csv")
    args = ap.parse_args()

    preds = list(csv.DictReader(open(args.predictions, encoding="utf-8-sig")))
    ents = {e["entity"]: e for e in csv.DictReader(
        open(args.entities, encoding="utf-8-sig"))}

    grey = [r for r in preds if float(r["confidence"]) <= args.grey]
    by_entity: dict[str, list[dict]] = defaultdict(list)
    singles: list[dict] = []
    for r in grey:
        de = r["deciding_entity"]
        if de and not de.startswith("("):
            by_entity[de].append(r)
        else:
            singles.append(r)

    rows = []
    for key, items in by_entity.items():
        e = ents.get(key, {})
        conf = min(float(r["confidence"]) for r in items)
        titles = "; ".join(r["title"][:60] for r in items[:6])
        rows.append({
            "decision_type": "entity",
            "decision_key": key,
            "titles_cleared": len(items),
            "current_label": items[0]["prediction"],
            "confidence": conf,
            "p_maker": e.get("p_maker", ""),
            "p_generic_use": e.get("p_generic_use", ""),
            "p_alt_meaning": e.get("p_alt_meaning", ""),
            "p_recognized": e.get("p_recognized", ""),
            "why_grey": ("probe conflict" if e.get("conflict") == "True"
                         else "recognition-capped" if e.get("gated") == "True"
                         else "weak agreement"),
            "example_titles": titles,
            "human_label": "",
        })
    for r in singles:
        rows.append({
            "decision_type": "title",
            "decision_key": r["title"],
            "titles_cleared": 1,
            "current_label": r["prediction"],
            "confidence": float(r["confidence"]),
            "p_maker": "", "p_generic_use": "", "p_alt_meaning": "",
            "p_recognized": "",
            "why_grey": "title-probe uncertain",
            "example_titles": r["title"],
            "human_label": "",
        })

    # Impact first (one decision clears many titles), then deepest uncertainty.
    rows.sort(key=lambda x: (-x["titles_cleared"], x["confidence"]))
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    cleared = sum(r["titles_cleared"] for r in rows)
    print(f"grey titles:      {len(grey)}")
    print(f"review decisions: {len(rows)} "
          f"({sum(1 for r in rows if r['decision_type'] == 'entity')} entity"
          f" + {sum(1 for r in rows if r['decision_type'] == 'title')} title)")
    print(f"titles cleared when done: {cleared}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
