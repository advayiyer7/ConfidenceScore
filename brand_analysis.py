"""brand_analysis.py — analyze the branded/unbranded logprob confidence.

Reads the output of brand_confidence.py and reports how good the logprob
confidence is at the branded-vs-unbranded call: overall accuracy, confidence
per true class, and the key check — is confidence higher when the model is
right than when it is wrong (i.e. does the logprob actually mean something)?

Usage:
    python brand_analysis.py --scored brand_eval_scored.csv [--output BRAND_ANALYSIS.md]
"""

import argparse
import csv
import datetime
import math

HIGH, LOW = 0.85, 0.70
GREY = 0.85   # confidence <= GREY -> "grey zone", route to human review


def to_float(v):
    try:
        f = float(str(v).strip())
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def fmt(v, d=4):
    return "n/a" if v is None else f"{v:.{d}f}"


def render(rows, scored_path):
    recs = []
    for r in rows:
        conf = to_float(r.get("confidence"))
        if conf is None:
            continue
        true = (r.get("brand") or "").strip().lower() or None
        pred = (r.get("pred_brand") or "").strip().lower()
        recs.append({
            "title": r.get("title", ""), "true": true, "pred": pred,
            "conf": conf, "p_branded": to_float(r.get("p_branded")),
            "correct": (true == pred) if true else None,
        })


    lines, out = [], None
    buf = []
    out = buf.append
    out("# Branded vs. Unbranded — Logprob Confidence")
    out("")
    out(f"- **Generated:** {datetime.date.today().isoformat()}")
    out(f"- **Scored file:** `{scored_path}`")
    out("")
    out("Each product is classified branded/unbranded by the model in a single "
        "forced token (B/U) with logprobs on. The **confidence is the token "
        "probability mass on the chosen letter** — a real logprob, not a "
        "self-reported number. No quantity is involved.")
    out("")

    graded = [r for r in recs if r["correct"] is not None]
    if graded:
        acc = sum(r["correct"] for r in graded) / len(graded)
        out("## Headline")
        out("")
        out(f"- **Accuracy** (vs. gold labels): **{acc:.1%}** "
            f"({sum(r['correct'] for r in graded)}/{len(graded)})")
        out(f"- **Mean confidence:** {fmt(mean([r['conf'] for r in graded]))}")
        cright = [r["conf"] for r in graded if r["correct"]]
        cwrong = [r["conf"] for r in graded if not r["correct"]]
        out(f"- **Mean confidence when correct:** {fmt(mean(cright))}")
        out(f"- **Mean confidence when wrong:** {fmt(mean(cwrong))}")
        if cright and cwrong:
            out(f"- **Separation (right − wrong):** "
                f"{mean(cright) - mean(cwrong):+.4f} — positive means the "
                f"logprob confidence actually tracks correctness.")
        elif not cwrong:
            out("- No misclassifications, so right/wrong separation can't be "
                "measured on this set.")
        out("")

    out("## Confidence by true class")
    out("")
    out("| true class | n | mean confidence | accuracy |")
    out("|---|---|---|---|")
    for cls in ("branded", "unbranded"):
        grp = [r for r in graded if r["true"] == cls]
        if grp:
            out(f"| {cls} | {len(grp)} | {fmt(mean([r['conf'] for r in grp]))} "
                f"| {sum(r['correct'] for r in grp) / len(grp):.1%} |")
        else:
            out(f"| {cls} | 0 | — | — |")
    out("")

    out("## Confidence bands")
    out("")
    out(f"High ≥ {HIGH:.2f} · Medium {LOW:.2f}–{HIGH:.2f} · Low < {LOW:.2f}.")
    out("")
    out("| band | n | accuracy in band |")
    out("|---|---|---|")
    for label, lo, hi in (("high", HIGH, 1.01), ("medium", LOW, HIGH),
                          ("low", 0.0, LOW)):
        grp = [r for r in graded if lo <= r["conf"] < hi]
        acc = (sum(r["correct"] for r in grp) / len(grp)) if grp else None
        out(f"| {label} | {len(grp)} | {fmt(acc, 3) if acc is not None else '—'} |")
    out("")

    grey = [r for r in recs if r["conf"] <= GREY]
    out(f"**Grey zone (confidence ≤ {GREY:.2f} → route to review): "
        f"{len(grey)} / {len(recs)} rows ({len(grey)/len(recs):.0%}).** "
        f"Everything above is auto-accept.")
    out("")

    wrong = [r for r in graded if not r["correct"]]
    out("## Misclassifications")
    out("")
    if wrong:
        out("| title | true | predicted | confidence |")
        out("|---|---|---|---|")
        for r in sorted(wrong, key=lambda r: -r["conf"]):
            out(f"| {r['title']} | {r['true']} | {r['pred']} | {r['conf']:.4f} |")
    else:
        out("None — every row classified correctly.")
    out("")

    out("## Per-row detail")
    out("")
    out("| title | true | pred | P(branded) | confidence |")
    out("|---|---|---|---|---|")
    for r in sorted(recs, key=lambda r: (r["true"] or "", -(r["p_branded"] or 0))):
        mark = "" if r["correct"] in (True, None) else " ⚠"
        out(f"| {r['title']}{mark} | {r['true'] or '—'} | {r['pred']} "
            f"| {fmt(r['p_branded'])} | {r['conf']:.4f} |")
    out("")
    return "\n".join(buf) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scored", required=True)
    ap.add_argument("--output", default="BRAND_ANALYSIS.md")
    args = ap.parse_args()
    report = render(read_csv(args.scored), args.scored)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
