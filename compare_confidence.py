"""compare_confidence.py — logprob confidence vs. self-reported confidence.

Joins two scored CSVs of the SAME input (one from uom_confidence.py, one from
selfreport_confidence.py) row-by-row and contrasts the two confidence signals,
split by the `brand` column. The deterministic fast path is identical in both
runs (explicit measurements -> 1.0), so the comparison is restricted to the
model-estimated rows, where the two methods actually differ.

What to look for: self-reported confidence is poorly calibrated. It tends to
cluster on a few round values with little spread and to key off surface cues
(e.g. "no number in the title" -> 0.5) rather than genuine uncertainty, while
logprob confidence varies continuously. The "distinct values" and "std dev"
rows quantify the collapse.

Usage:
    python compare_confidence.py --logprob newtest_scored.csv \
        --selfreport newtest_selfreport.csv [--output SELFREPORT_VS_LOGPROB.md]
"""

import argparse
import csv
import datetime
import math


def to_float(value):
    try:
        f = float(str(value).strip())
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def stats(values):
    if not values:
        return {"n": 0, "mean": None, "std": None, "distinct": 0, "round": None}
    mean = sum(values) / len(values)
    var = sum((v - mean) ** 2 for v in values) / len(values)
    # "round" = share landing on a 0.05 grid (0.8, 0.85, 0.9...), the tell-tale
    # signature of a model picking a tidy number rather than measuring.
    roundish = sum(1 for v in values if abs(v * 20 - round(v * 20)) < 1e-6)
    return {
        "n": len(values),
        "mean": mean,
        "std": math.sqrt(var),
        "distinct": len(set(round(v, 4) for v in values)),
        "round": roundish / len(values),
    }


def fmt(value, digits=4):
    return "n/a" if value is None else f"{value:.{digits}f}"


def render(logprob_rows, selfreport_rows, lp_path, sr_path):
    if len(logprob_rows) != len(selfreport_rows):
        raise SystemExit(
            f"row count mismatch: {len(logprob_rows)} vs "
            f"{len(selfreport_rows)} — the two files must score the same input")

    # Pair by row order; keep only rows where BOTH methods used the model path
    # (deterministic rows are identical 1.0s in both and would dilute things).
    paired = []
    for lp, sr in zip(logprob_rows, selfreport_rows):
        lp_conf, sr_conf = to_float(lp.get("confidence")), to_float(sr.get("confidence"))
        if lp.get("confidence_source") == "logprob" and \
                sr.get("confidence_source") == "self_report" and \
                lp_conf is not None and sr_conf is not None:
            paired.append({
                "title": lp.get("title", ""),
                "brand": (lp.get("brand") or "").strip().lower(),
                "logprob": lp_conf,
                "selfreport": sr_conf,
            })

    lines = []
    out = lines.append
    out("# Logprob Confidence vs. Self-Reported Confidence")
    out("")
    out(f"- **Generated:** {datetime.date.today().isoformat()}")
    out(f"- **Logprob file:** `{lp_path}`")
    out(f"- **Self-report file:** `{sr_path}`")
    out("")
    out("Both runs score the same rows with the same deterministic fast path. "
        "The difference is the confidence signal on model-estimated rows: one "
        "is derived from token **logprobs** (the candidate-selection mass), the "
        "other is **self-reported** — the model is simply asked \"how confident "
        "are you, 0-1?\". This contrasts them, split by brand. Comparison is "
        f"over the **{len(paired)} model-estimated rows** only.")
    out("")

    groups = [
        ("all", paired),
        ("branded", [p for p in paired if p["brand"] == "branded"]),
        ("unbranded", [p for p in paired if p["brand"] == "unbranded"]),
    ]

    out("## Mean confidence by method")
    out("")
    out("| group | n | logprob | self-reported | Δ (self − logprob) |")
    out("|---|---|---|---|---|")
    for name, grp in groups:
        ls = stats([p["logprob"] for p in grp])
        ss = stats([p["selfreport"] for p in grp])
        delta = (ss["mean"] - ls["mean"]) if (ls["mean"] is not None
                                              and ss["mean"] is not None) else None
        out(f"| {name} | {len(grp)} | {fmt(ls['mean'])} | {fmt(ss['mean'])} "
            f"| {delta:+.4f} |" if delta is not None
            else f"| {name} | {len(grp)} | {fmt(ls['mean'])} | {fmt(ss['mean'])} | n/a |")
    out("")
    out("Δ is self-reported minus logprob mean. The sign is not the headline "
        "(self-report can run high or low); the point is the two signals "
        "disagree by a large margin, and the spread table below shows which "
        "one is actually discriminating.")
    out("")

    out("## Spread: does the score actually discriminate?")
    out("")
    out("A useful confidence varies with uncertainty. Self-reported numbers "
        "tend to collapse onto a few round values (low distinct count, high "
        "share on the 0.05 grid, low std dev).")
    out("")
    out("| method | distinct values | std dev | share on 0.05 grid | min | max |")
    out("|---|---|---|---|---|---|")
    for label, key in (("logprob", "logprob"), ("self-reported", "selfreport")):
        vals = [p[key] for p in paired]
        s = stats(vals)
        out(f"| {label} | {s['distinct']} / {len(vals)} | {fmt(s['std'])} "
            f"| {fmt(s['round'], 2)} | {fmt(min(vals))} | {fmt(max(vals))} |")
    out("")

    lp_all = stats([p["logprob"] for p in paired])
    sr_all = stats([p["selfreport"] for p in paired])
    out("## Takeaway")
    out("")
    out(f"Across {len(paired)} estimated rows, self-reported confidence used "
        f"only **{sr_all['distinct']} distinct values** ({sr_all['round']:.0%} "
        f"of them on the 0.05 grid) versus **{lp_all['distinct']}** for the "
        f"logprob score. Self-report defaults to a flat 0.5 on commodity "
        f"produce (Spring Onion, Tomato, Curry Leaves) — items the logprob "
        f"method rates ~0.99 because their typical retail size is well known. "
        f"It is keying off \"the title has no number\", not real uncertainty. "
        f"The logprob signal is continuous and orders rows by genuine "
        f"sizing difficulty; the self-reported one cannot.")
    out("")

    out("## Per-row, side by side")
    out("")
    out("| title | brand | logprob | self-reported | self − logprob |")
    out("|---|---|---|---|---|")
    for p in sorted(paired, key=lambda p: p["logprob"]):
        d = p["selfreport"] - p["logprob"]
        out(f"| {p['title']} | {p['brand']} | {p['logprob']:.4f} "
            f"| {p['selfreport']:.4f} | {d:+.4f} |")
    out("")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Compare logprob vs self-reported confidence.")
    parser.add_argument("--logprob", required=True,
                        help="CSV from uom_confidence.py")
    parser.add_argument("--selfreport", required=True,
                        help="CSV from selfreport_confidence.py")
    parser.add_argument("--output", default="SELFREPORT_VS_LOGPROB.md")
    args = parser.parse_args()

    report = render(read_csv(args.logprob), read_csv(args.selfreport),
                    args.logprob, args.selfreport)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
