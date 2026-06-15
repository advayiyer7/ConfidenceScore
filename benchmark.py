"""benchmark.py — measure how well `confidence` predicts correctness.

Joins a scored CSV (output of uom_confidence.py) against a gold-labeled CSV
on `title` and evaluates the confidence score as a predictor of whether
`computed_std_qty` is correct, writing a markdown report.

A prediction is CORRECT when it is within `gold_tolerance_pct` percent of
`gold_std_qty` (tight, e.g. 1%, for rows with explicit measurements; loose,
e.g. 50-60%, for world-knowledge estimates where order-of-magnitude is the
bar). Gold rows with a blank `gold_std_qty` are non-estimable: the right
behavior there is to abstain, tracked separately from calibration metrics.

Gold quantities for `piece` rows assume the scorer's default --piece-to-kg
mode (per-piece weight in kg x piece count).

Metrics:
  accuracy            fraction of scored gold rows within tolerance
  Brier score         mean (confidence - correct)^2; lower is better
  ECE                 expected calibration error over confidence bins
  AUROC               does ranking by confidence separate right from wrong
  reliability table   per-bin mean confidence vs observed accuracy
  threshold sweep     coverage and selective accuracy at each cutoff

Usage:
    python benchmark.py --scored scored.csv [--gold gold.csv]
                        [--output RESULTS.md]
"""

import argparse
import csv
import datetime
import math

BINS = [0.0, 0.5, 0.7, 0.8, 0.9, 1.000001]
THRESHOLDS = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95]


def to_float(value):
    try:
        f = float(str(value).strip())
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def auroc(pairs):
    """AUROC of confidence as a ranker of correctness, tie-aware.

    pairs: list of (confidence, correct). None when only one class present.
    """
    pos = sum(1 for _, y in pairs if y)
    neg = len(pairs) - pos
    if pos == 0 or neg == 0:
        return None
    ranked = sorted(pairs, key=lambda t: t[0])
    rank_sum, i = 0.0, 0
    while i < len(ranked):
        j = i
        while j < len(ranked) and ranked[j][0] == ranked[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0  # average of ranks i+1 .. j
        rank_sum += avg_rank * sum(1 for c, y in ranked[i:j] if y)
        i = j
    return (rank_sum - pos * (pos + 1) / 2.0) / (pos * neg)


def evaluate(scored_rows, gold_rows):
    gold_by_title = {r["title"]: r for r in gold_rows}

    records = []          # rows with gold qty AND a prediction w/ confidence
    missed_coverage = []  # gold qty present but model abstained
    abstain_rows = []     # gold blank (non-estimable): (row, model_abstained)
    unmatched = []        # scored rows with no gold label

    for row in scored_rows:
        gold = gold_by_title.get(row.get("title", ""))
        if gold is None:
            unmatched.append(row)
            continue
        gold_qty = to_float(gold.get("gold_std_qty"))
        pred = to_float(row.get("computed_std_qty"))
        conf = to_float(row.get("confidence"))

        if gold_qty is None:
            abstain_rows.append((row, pred is None))
            continue
        if pred is None or conf is None:
            missed_coverage.append(row)
            continue

        tol = to_float(gold.get("gold_tolerance_pct")) or 1.0
        correct = abs(pred - gold_qty) <= (tol / 100.0) * gold_qty
        records.append({
            "title": row["title"],
            "source": row.get("confidence_source", ""),
            "conf": conf,
            "pred": pred,
            "gold": gold_qty,
            "tol": tol,
            "correct": correct,
            "ambiguous": (to_float(gold.get("gold_ambiguous")) or 0) >= 1,
        })

    unscored_gold = [t for t in gold_by_title
                     if t not in {r.get("title") for r in scored_rows}]
    return records, missed_coverage, abstain_rows, unmatched, unscored_gold


def reliability(records):
    """Per-bin (label, n, mean confidence, accuracy) plus ECE."""
    table, ece = [], 0.0
    for lo, hi in zip(BINS, BINS[1:]):
        in_bin = [r for r in records if lo <= r["conf"] < hi]
        label = f"[{lo:.2f}, {min(hi, 1.0):.2f}{']' if hi > 1 else ')'}"
        if not in_bin:
            table.append((label, 0, None, None))
            continue
        mean_conf = sum(r["conf"] for r in in_bin) / len(in_bin)
        acc = sum(r["correct"] for r in in_bin) / len(in_bin)
        ece += (len(in_bin) / len(records)) * abs(mean_conf - acc)
        table.append((label, len(in_bin), mean_conf, acc))
    return table, ece


def fmt(value, digits=4):
    return "n/a" if value is None else f"{value:.{digits}f}"


def render(records, missed, abstains, unmatched, unscored_gold,
           scored_path, gold_path):
    lines = []
    out = lines.append
    n = len(records)

    out("# Confidence Benchmark Results")
    out("")
    out(f"- **Generated:** {datetime.date.today().isoformat()}")
    out(f"- **Scored file:** `{scored_path}`")
    out(f"- **Gold file:** `{gold_path}`")
    out("")
    out("Measures how well the logprob-derived `confidence` column predicts "
        "whether `computed_std_qty` is actually correct. A row counts as "
        "correct when the prediction is within its gold tolerance "
        "(tight for explicit measurements, loose for world-knowledge "
        "estimates).")
    out("")

    out("## Coverage")
    out("")
    out("| | count |")
    out("|---|---|")
    out(f"| Gold rows scored and evaluated | {n} |")
    out(f"| Gold rows where model abstained (missed coverage) | {len(missed)} |")
    abstained_ok = sum(1 for _, ok in abstains if ok)
    out(f"| Non-estimable gold rows (correct behavior = abstain) "
        f"| {len(abstains)} (abstained on {abstained_ok}) |")
    out(f"| Scored rows without a gold label (skipped) | {len(unmatched)} |")
    out(f"| Gold rows not present in scored file | {len(unscored_gold)} |")
    out("")

    if not records:
        out("**No evaluable rows — nothing to report.** Run the scorer over "
            "`gold.csv` first (see README).")
        return "\n".join(lines) + "\n"

    accuracy = sum(r["correct"] for r in records) / n
    mean_conf = sum(r["conf"] for r in records) / n
    brier = sum((r["conf"] - r["correct"]) ** 2 for r in records) / n
    table, ece = reliability(records)
    roc = auroc([(r["conf"], r["correct"]) for r in records])
    conf_right = [r["conf"] for r in records if r["correct"]]
    conf_wrong = [r["conf"] for r in records if not r["correct"]]

    out("## Headline metrics")
    out("")
    out("| metric | value | reading |")
    out("|---|---|---|")
    out(f"| Accuracy | {accuracy:.4f} | fraction of predictions within "
        "tolerance |")
    out(f"| Mean confidence | {mean_conf:.4f} | should track accuracy if "
        "calibrated |")
    out(f"| Calibration gap | {mean_conf - accuracy:+.4f} | >0 means "
        "overconfident |")
    out(f"| Brier score | {brier:.4f} | 0 = perfect, 0.25 = uninformative |")
    out(f"| ECE | {ece:.4f} | expected calibration error, lower is better |")
    out(f"| AUROC | {fmt(roc)} | 1.0 = confidence perfectly ranks right "
        "above wrong; n/a if all rows are one class |")
    out(f"| Mean conf (correct rows) | {fmt(sum(conf_right) / len(conf_right) if conf_right else None)} | |")
    out(f"| Mean conf (incorrect rows) | {fmt(sum(conf_wrong) / len(conf_wrong) if conf_wrong else None)} | |")
    out("")

    out("## Per-source breakdown")
    out("")
    out("| source | n | accuracy | mean confidence |")
    out("|---|---|---|---|")
    for source in sorted({r["source"] for r in records}):
        sub = [r for r in records if r["source"] == source]
        out(f"| {source} | {len(sub)} "
            f"| {sum(r['correct'] for r in sub) / len(sub):.4f} "
            f"| {sum(r['conf'] for r in sub) / len(sub):.4f} |")
    out("")

    out("## Ambiguity discrimination")
    out("")
    out("Rows labeled `gold_ambiguous` have more than one defensible "
        "reading (e.g. \"Paneer 1p\", \"Coca Cola 600\"); a good confidence "
        "score should be **lower** there than on clear rows, pushing them "
        "below the review threshold.")
    out("")
    amb = [r for r in records if r["ambiguous"]]
    clear = [r for r in records if not r["ambiguous"]]
    if amb and clear:
        out("| group | n | mean confidence | accuracy | share below 0.70 |")
        out("|---|---|---|---|---|")
        for label, group in (("clear", clear), ("ambiguous", amb)):
            mc = sum(r["conf"] for r in group) / len(group)
            acc = sum(r["correct"] for r in group) / len(group)
            low = sum(1 for r in group if r["conf"] < 0.70) / len(group)
            out(f"| {label} | {len(group)} | {mc:.4f} | {acc:.4f} "
                f"| {low:.0%} |")
        out("")
        gap = (sum(r["conf"] for r in clear) / len(clear)
               - sum(r["conf"] for r in amb) / len(amb))
        out(f"Separation (clear − ambiguous mean confidence): "
            f"**{gap:+.4f}** — should be clearly positive.")
    else:
        missing = "ambiguous" if not amb else "clear"
        out(f"_No {missing} rows evaluated yet (ambiguous rows need the "
            "LLM path; run without --deterministic-only)._")
    out("")

    out("## Reliability table")
    out("")
    out("Within each confidence bin, mean confidence should match observed "
        "accuracy.")
    out("")
    out("| confidence bin | n | mean confidence | accuracy | gap |")
    out("|---|---|---|---|---|")
    for label, count, mc, acc in table:
        if count == 0:
            out(f"| {label} | 0 | — | — | — |")
        else:
            out(f"| {label} | {count} | {mc:.4f} | {acc:.4f} "
                f"| {mc - acc:+.4f} |")
    out("")

    out("## Threshold sweep")
    out("")
    out("If rows below the cutoff are routed to human review: coverage is "
        "the share auto-accepted, selective accuracy is the accuracy of "
        "what was auto-accepted.")
    out("")
    out("| threshold | coverage | selective accuracy |")
    out("|---|---|---|")
    for t in THRESHOLDS:
        kept = [r for r in records if r["conf"] >= t]
        cov = len(kept) / n
        sel = (sum(r["correct"] for r in kept) / len(kept)) if kept else None
        out(f"| {t:.2f} | {cov:.0%} ({len(kept)}/{n}) | {fmt(sel)} |")
    out("")

    flagged = [r for r in records if r["conf"] >= 0.9 and not r["correct"]]
    out("## Overconfident errors (confidence ≥ 0.90 but wrong)")
    out("")
    if flagged:
        out("| title | confidence | predicted | gold |")
        out("|---|---|---|---|")
        for r in flagged:
            out(f"| {r['title']} | {r['conf']:.4f} | {r['pred']} "
                f"| {r['gold']} |")
    else:
        out("None.")
    out("")

    if n <= 40:
        out("## Per-row detail")
        out("")
        out("| title | source | confidence | predicted | gold | tol % | "
            "correct |")
        out("|---|---|---|---|---|---|---|")
        for r in sorted(records, key=lambda r: r["conf"]):
            out(f"| {r['title']} | {r['source']} | {r['conf']:.4f} "
                f"| {r['pred']} | {r['gold']} | {r['tol']:.0f} "
                f"| {'yes' if r['correct'] else 'NO'} |")
        out("")

    if missed:
        out("## Missed coverage (gold available, model abstained)")
        out("")
        for row in missed:
            out(f"- {row.get('title')}")
        out("")
    if unscored_gold:
        out("## Gold rows not yet scored")
        out("")
        out("Run `python uom_confidence.py --input gold.csv --output "
            "gold_scored.csv` (needs OPENAI_API_KEY), then re-run this "
            "benchmark with `--scored gold_scored.csv`.")
        out("")
        for title in unscored_gold:
            out(f"- {title}")
        out("")

    if n < 30:
        out("## Caveats")
        out("")
        out(f"- Only **{n} evaluable rows** — treat every number above as "
            "directional, not statistically meaningful. The gold set should "
            "grow to a few hundred labeled rows before calibration "
            "(isotonic/Platt in `calibrate()`) is fitted.")
        out("- Gold values for estimate rows are typical retail quantities "
            "with wide tolerances; they reward order-of-magnitude "
            "correctness, not exactness.")
        out("")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark confidence calibration against a gold set.")
    parser.add_argument("--scored", required=True,
                        help="CSV produced by uom_confidence.py")
    parser.add_argument("--gold", default="gold.csv",
                        help="gold-labeled CSV (default: gold.csv)")
    parser.add_argument("--output", default="RESULTS.md",
                        help="markdown report path (default: RESULTS.md)")
    args = parser.parse_args()

    records, missed, abstains, unmatched, unscored_gold = evaluate(
        read_csv(args.scored), read_csv(args.gold))
    report = render(records, missed, abstains, unmatched, unscored_gold,
                    args.scored, args.gold)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"wrote {args.output}: {len(records)} evaluable rows, "
          f"{len(missed)} missed, {len(abstains)} abstain-expected, "
          f"{len(unscored_gold)} gold rows not yet scored")


if __name__ == "__main__":
    main()
