"""brand_analysis.py — break the confidence score down by branded vs unbranded.

Reads a scored CSV (output of uom_confidence.py) that carries a `brand`
column ("branded" / "unbranded") and reports, per group, how the confidence
score behaves: coverage (scored vs. abstained), the deterministic/LLM split,
and the confidence distribution. No gold labels needed — this measures the
confidence column itself, not its calibration.

The hypothesis under test: branded items carry explicit pack sizes (e.g.
"750Ml", "300gm") and have a single clear reading, so they should score HIGH
(often deterministic at 1.0); unbranded loose produce ("Spring Onion",
"Broccoli") has no stated quantity and must be estimated, so it should score
LOWER and lean on the LLM path.

Usage:
    python brand_analysis.py --scored newtest_scored.csv [--output BRAND_ANALYSIS.md]
"""

import argparse
import csv
import datetime
import math

THRESHOLD = 0.70  # review cutoff used elsewhere in the project


def to_float(value):
    try:
        f = float(str(value).strip())
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def median(values):
    if not values:
        return None
    s = sorted(values)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2.0


def summarize(rows):
    """Per-group stats over a list of scored rows."""
    confs = [to_float(r.get("confidence")) for r in rows]
    scored = [c for c in confs if c is not None]
    sources = [r.get("confidence_source", "") for r in rows]
    return {
        "n": len(rows),
        "scored": len(scored),
        "abstained": len(rows) - len(scored),
        "deterministic": sources.count("deterministic"),
        "logprob": sources.count("logprob"),
        "none": sources.count("none"),
        "mean": (sum(scored) / len(scored)) if scored else None,
        "median": median(scored),
        "min": min(scored) if scored else None,
        "below": sum(1 for c in scored if c < THRESHOLD),
        "confs": scored,
    }


def fmt(value, digits=4):
    return "n/a" if value is None else f"{value:.{digits}f}"


def render(rows, scored_path):
    groups = {
        "branded": [r for r in rows if (r.get("brand") or "").strip().lower() == "branded"],
        "unbranded": [r for r in rows if (r.get("brand") or "").strip().lower() == "unbranded"],
    }
    stats = {name: summarize(grp) for name, grp in groups.items()}

    lines = []
    out = lines.append
    out("# Confidence by Branded vs. Unbranded")
    out("")
    out(f"- **Generated:** {datetime.date.today().isoformat()}")
    out(f"- **Scored file:** `{scored_path}`")
    out("")
    out("Breaks the logprob-derived `confidence` score down by whether the "
        "product carries a brand. No gold labels here — this measures the "
        "confidence distribution and coverage, not calibration. The split "
        "separates two effects: explicit pack sizes in the title (parsed "
        "deterministically at 1.0) versus how confidently the model can "
        "*size* an item that states no quantity (the LLM path). Read the "
        "estimate-only table for the fair comparison of the latter.")
    out("")

    # Headline confidence score per group. The logprob score is the number
    # this method exists to produce, so it leads; the all-rows mean (which
    # includes deterministic 1.0s) is shown alongside for context.
    llm_stats = {
        name: summarize([r for r in grp
                         if (r.get("confidence_source") or "") == "logprob"])
        for name, grp in groups.items()
    }
    out("## Confidence score")
    out("")
    out("| group | logprob confidence | all-rows confidence |")
    out("|---|---|---|")
    for name in ("branded", "unbranded"):
        out(f"| {name} | {fmt(llm_stats[name]['mean'])} "
            f"| {fmt(stats[name]['mean'])} |")
    out("")

    out("## Coverage and source split")
    out("")
    out("| group | rows | scored | abstained | deterministic | LLM (logprob) |")
    out("|---|---|---|---|---|---|")
    for name in ("branded", "unbranded"):
        s = stats[name]
        out(f"| {name} | {s['n']} | {s['scored']} | {s['abstained']} "
            f"| {s['deterministic']} | {s['logprob']} |")
    out("")

    out("## Confidence distribution (scored rows only)")
    out("")
    out("| group | n | mean | median | min | share below 0.70 |")
    out("|---|---|---|---|---|---|")
    for name in ("branded", "unbranded"):
        s = stats[name]
        share = f"{s['below'] / s['scored']:.0%}" if s["scored"] else "n/a"
        out(f"| {name} | {s['scored']} | {fmt(s['mean'])} | {fmt(s['median'])} "
            f"| {fmt(s['min'])} | {share} |")
    out("")

    def describe_gap(b, u, label):
        if b is None or u is None:
            missing = "branded" if b is None else "unbranded"
            return (f"_No scored {missing} {label} rows — set OPENAI_API_KEY "
                    f"and re-run the scorer._")
        gap = b - u
        if gap > 0.01:
            reading = "branded items score HIGHER"
        elif gap < -0.01:
            reading = "branded items score LOWER"
        else:
            reading = "the two groups are effectively tied"
        return (f"**Separation (branded − unbranded mean confidence): "
                f"{gap:+.4f}** — {reading}.")

    out(describe_gap(stats["branded"]["mean"], stats["unbranded"]["mean"],
                     "scored"))
    out("")

    # Apples-to-apples: deterministic rows are pinned to 1.0 by explicit text,
    # so the fair comparison of the *estimation* is over LLM-path rows only
    # (llm_stats computed above for the headline).
    out("## Estimate-only (LLM path), excluding deterministic 1.0s")
    out("")
    out("The deterministic rows score 1.0 purely because the title states an "
        "explicit measurement, which would swamp the comparison. Restricting "
        "to LLM-estimated rows isolates how confidently the model *sizes* an "
        "item with no stated quantity.")
    out("")
    out("| group | n | mean | median | min | share below 0.70 |")
    out("|---|---|---|---|---|---|")
    for name in ("branded", "unbranded"):
        s = llm_stats[name]
        share = f"{s['below'] / s['scored']:.0%}" if s["scored"] else "n/a"
        out(f"| {name} | {s['scored']} | {fmt(s['mean'])} | {fmt(s['median'])} "
            f"| {fmt(s['min'])} | {share} |")
    out("")
    out(describe_gap(llm_stats["branded"]["mean"],
                     llm_stats["unbranded"]["mean"], "LLM"))
    out("")

    out("## Per-row detail")
    out("")
    out("| title | brand | source | confidence |")
    out("|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (
            r.get("brand", ""), -(to_float(r.get("confidence")) or -1))):
        conf = to_float(r.get("confidence"))
        out(f"| {r.get('title','')} | {r.get('brand','')} "
            f"| {r.get('confidence_source','')} "
            f"| {fmt(conf) if conf is not None else '— (abstained)'} |")
    out("")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Break confidence down by branded vs unbranded.")
    parser.add_argument("--scored", required=True,
                        help="CSV from uom_confidence.py with a `brand` column")
    parser.add_argument("--output", default="BRAND_ANALYSIS.md")
    args = parser.parse_args()

    rows = read_csv(args.scored)
    report = render(rows, args.scored)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"wrote {args.output}: {len(rows)} rows")


if __name__ == "__main__":
    main()
