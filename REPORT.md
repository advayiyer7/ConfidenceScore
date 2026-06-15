# Status Report: Logprob-Based Confidence Scoring for UoM Standardization

**Date:** 2026-06-10
**Author:** Advay Iyer
**Repo:** `confidencescore`

## Executive summary

We built a scorer that takes the output of our 3-tier unit-of-measure
pipeline and attaches, to every product row, a standardized quantity plus a
**numeric confidence in [0,1] derived from the model's token logprobs** —
not a self-reported "I'm 90% sure," which LLMs are known to inflate. Rows
below a confidence threshold automatically carry their top alternative
interpretations so a reviewer sees the runner-up readings, not just the pick.

On the initial labeled sample, all 7 evaluable predictions were correct,
mean confidence was 0.97, and the score never claimed high confidence on a
wrong answer. A benchmark harness is now in place to track confidence
accuracy as the gold set grows (see `RESULTS.md`).

## What was delivered

1. **`uom_confidence.py`** — the scorer.
   - **Deterministic fast path:** rows with explicit measurements in the
     title (`5L`, `60 ml`, `30 G x 30 sachet` → 0.9 kg) are parsed by regex
     with no API call: confidence 1.0, near-zero cost.
   - **Two-stage logprob estimation** for everything else: the model first
     proposes 2–4 candidate interpretations (e.g. "one samosa ≈ 0.05 kg"),
     then picks the best in a second call that emits a **single token** with
     logprobs enabled. The probability mass on that choice — renormalized
     across candidates — is the confidence. Stage 2 costs one output token,
     keeping total spend within ~2× of a single-call design.
   - Production plumbing: retry with exponential backoff, parallel workers,
     per-row error isolation (a bad row is recorded, never crashes the run),
     and an end-of-run summary.
2. **`benchmark.py` + `gold.csv`** — an evaluation harness measuring how
   well the confidence score predicts actual correctness: accuracy, Brier
   score, expected calibration error (ECE), reliability bins, and a
   threshold sweep showing the auto-accept vs. human-review tradeoff at
   each cutoff. A 26-row labeled gold set seeds it.
3. **`RESULTS.md`** — generated benchmark report (regenerated on every run).

## Current results (small sample — directional only)

From `RESULTS.md`, evaluated on the 7 scored gold rows plus 1 abstention
case:

| Metric | Value | Meaning |
|---|---|---|
| Accuracy | 100% (7/7) | predictions within gold tolerance |
| Mean confidence | 0.967 | tracks accuracy → well calibrated so far |
| Brier score | 0.006 | 0 = perfect, 0.25 = uninformative |
| ECE | 0.033 | expected calibration error |
| Overconfident errors (≥0.90 conf, wrong) | 0 | the failure mode we most care about |
| Correct abstentions | 1/1 | unidentifiable item correctly left unscored |

Notable behaviors: the scorer's *least* confident row (samosa per-piece
weight, 0.80) is exactly the kind of world-knowledge guess that deserves
scrutiny, while explicit-measurement rows score 1.0 deterministically —
the ordering is sensible even before formal calibration.

## Caveats

- **7 rows is not statistics.** The gold set includes 18 more labeled rows
  ready to score, and should grow to a few hundred before we trust the
  curves.
- Confidence is currently **raw logprob mass, uncalibrated**. A
  `calibrate()` hook is already in the code; once the gold set is larger we
  fit isotonic regression or Platt scaling there and re-run the benchmark
  to verify the calibration gap closes.
- Gold values for estimate rows (loose produce, per-piece weights) use wide
  tolerances (±50–60%) — the bar is order-of-magnitude correctness.

## Recommended next steps

1. Label ~200–500 production rows (cheap: one number per row) and run the
   scorer + benchmark over them — this gives real ECE/AUROC curves.
2. Fit calibration in `calibrate()` from that data.
3. Use the benchmark's threshold sweep to pick the auto-accept cutoff for
   production based on how much human review capacity we have.

## How to reproduce

```bash
export OPENAI_API_KEY=sk-...
python uom_confidence.py --input gold.csv --output gold_scored.csv
python benchmark.py --scored gold_scored.csv --gold gold.csv --output RESULTS.md
```
