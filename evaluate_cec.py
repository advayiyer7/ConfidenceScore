"""evaluate_cec.py — grade a predictions file against the confident-error
policy: LOW-confidence-wrong is acceptable; HIGH-confidence-wrong is not.

Uses the hand-established eval set from the Opus review + this project's
verified cases. Reports, for any predictions CSV:
  1. confident-wrong count on known cases (must be 0)
  2. known real brands that must remain confidently branded
  3. grey-zone size (review load)
  4. split-label consistency (must be 0)
"""
import csv
import sys
from collections import defaultdict

PATH = sys.argv[1] if len(sys.argv) > 1 else "cec_predictions.csv"
GREY = 0.85

# substring -> required outcome.
# "not_confident_unbranded": branded OR grey is fine; confident-unbranded fails.
# "not_confident_branded":   unbranded OR grey is fine; confident-branded fails.
# "confident_branded":       must stay branded above the grey line.
KNOWN = {
    # real brands that must remain confidently branded (famous + verified)
    "HARPIC": "confident_branded",
    "Nestle Milk Powder": "confident_branded",
    "Chicken Broth Powder Knorr": "confident_branded",
    "AASHIRVAAD": "confident_branded",
    "Perrier": "confident_branded",
    "Tropicana": "confident_branded",
    "MDH Chana Masala": "confident_branded",
    "Sakthi - Kulambu": "confident_branded",
    "Fortune Aata": "confident_branded",
    "Taski Suma Ultra": "confident_branded",
    # Opus's own MEDIUM-confidence calls: grey is acceptable, confident-
    # unbranded is not (single-title coined/ambiguous names)
    "3 EASTMADE": "not_confident_unbranded",
    "ANANDA PANEER": "not_confident_unbranded",
    "SUMA TAB": "not_confident_unbranded",
    "Hungritos": "not_confident_unbranded",
    "Newtrition": "not_confident_unbranded",
    "#_# Mango Biscoff Tub - Sassy Teaspoon": "confident_branded",
    "#_# SIERRA 72": "confident_branded",          # Ether (seller suffix)
    "#_# Frozen OG Chocolate": "confident_branded",  # Chonkers
    # generic/ambiguous items where a CONFIDENT branded call is an error
    "CHULLA": "not_confident_branded",
    "AANCH COVER": "not_confident_branded",
    "PAPER COVER BROWN - PAPAD": "not_confident_branded",
    "CHAT PLATE": "not_confident_branded",
    "COLOUR CODE DOTT TUES": "not_confident_branded",
    "ATTA GANGA": "not_confident_branded",
    "UH GREEN CAPSICUMWHOLE": "not_confident_branded",
    "JALI MAT": "not_confident_branded",
    # known brands that must not be CONFIDENTLY unbranded (grey or branded ok)
    "RED LABEL TEA": "not_confident_unbranded",
    "Twinning Lemon": "not_confident_unbranded",
    "Kiley Soda": "not_confident_unbranded",
    "#_# Stirrer - Murukku": "not_confident_unbranded",
}


def main():
    rows = list(csv.DictReader(open(PATH, newline="", encoding="utf-8-sig")))
    by_title = {r["title"]: r for r in rows}

    def find(sub):
        return next((by_title[t] for t in by_title if sub.lower() in t.lower()),
                    None)

    failures, passes = [], 0
    for sub, want in KNOWN.items():
        r = find(sub)
        if r is None:
            failures.append((sub, want, "TITLE NOT FOUND"))
            continue
        pred, conf = r["prediction"], float(r["confidence"])
        confident = conf > GREY
        ok = {
            "confident_branded": pred == "branded" and confident,
            "not_confident_branded": not (pred == "branded" and confident),
            "not_confident_unbranded": not (pred == "unbranded" and confident),
        }[want]
        if ok:
            passes += 1
        else:
            failures.append((sub, want, f"{pred}@{conf:.3f}"))

    grey = sum(1 for r in rows if float(r["confidence"]) <= GREY)
    by_ent = defaultdict(set)
    for r in rows:
        de = r["deciding_entity"]
        if de and not de.startswith("("):
            by_ent[de].add(r["prediction"])
    splits = sum(1 for s in by_ent.values() if len(s) > 1)

    print(f"file: {PATH}")
    print(f"known-case checks:   {passes}/{len(KNOWN)} pass")
    for sub, want, got in failures:
        print(f"  FAIL [{want}] {sub!r} -> {got}")
    print(f"grey zone (<= {GREY}): {grey}/{len(rows)} ({100*grey/len(rows):.1f}%)")
    print(f"split-label entities: {splits}")
    print("VERDICT:", "PASS" if not failures and splits == 0 else "FAIL")


if __name__ == "__main__":
    main()
