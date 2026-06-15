# Confidence Benchmark Results

- **Generated:** 2026-06-10
- **Scored file:** `sample_output.csv`
- **Gold file:** `gold.csv`

Measures how well the logprob-derived `confidence` column predicts whether `computed_std_qty` is actually correct. A row counts as correct when the prediction is within its gold tolerance (tight for explicit measurements, loose for world-knowledge estimates).

## Coverage

| | count |
|---|---|
| Gold rows scored and evaluated | 7 |
| Gold rows where model abstained (missed coverage) | 0 |
| Non-estimable gold rows (correct behavior = abstain) | 1 (abstained on 1) |
| Scored rows without a gold label (skipped) | 0 |
| Gold rows not present in scored file | 18 |

## Headline metrics

| metric | value | reading |
|---|---|---|
| Accuracy | 1.0000 | fraction of predictions within tolerance |
| Mean confidence | 0.9674 | should track accuracy if calibrated |
| Calibration gap | -0.0326 | >0 means overconfident |
| Brier score | 0.0059 | 0 = perfect, 0.25 = uninformative |
| ECE | 0.0326 | expected calibration error, lower is better |
| AUROC | n/a | 1.0 = confidence perfectly ranks right above wrong; n/a if all rows are one class |
| Mean conf (correct rows) | 0.9674 | |
| Mean conf (incorrect rows) | n/a | |

## Per-source breakdown

| source | n | accuracy | mean confidence |
|---|---|---|---|
| deterministic | 3 | 1.0000 | 1.0000 |
| logprob | 4 | 1.0000 | 0.9430 |

## Reliability table

Within each confidence bin, mean confidence should match observed accuracy.

| confidence bin | n | mean confidence | accuracy | gap |
|---|---|---|---|---|
| [0.00, 0.50) | 0 | — | — | — |
| [0.50, 0.70) | 0 | — | — | — |
| [0.70, 0.80) | 1 | 0.7969 | 1.0000 | -0.2031 |
| [0.80, 0.90) | 0 | — | — | — |
| [0.90, 1.00] | 6 | 0.9959 | 1.0000 | -0.0041 |

## Threshold sweep

If rows below the cutoff are routed to human review: coverage is the share auto-accepted, selective accuracy is the accuracy of what was auto-accepted.

| threshold | coverage | selective accuracy |
|---|---|---|
| 0.50 | 100% (7/7) | 1.0000 |
| 0.60 | 100% (7/7) | 1.0000 |
| 0.70 | 100% (7/7) | 1.0000 |
| 0.80 | 86% (6/7) | 1.0000 |
| 0.90 | 86% (6/7) | 1.0000 |
| 0.95 | 86% (6/7) | 1.0000 |

## Overconfident errors (confidence ≥ 0.90 but wrong)

None.

## Per-row detail

| title | source | confidence | predicted | gold | tol % | correct |
|---|---|---|---|---|---|---|
| Samosa (half Done)-Snacc | logprob | 0.7969 | 0.05 | 0.05 | 50 | yes |
| Banana Robusta | logprob | 0.9814 | 0.9 | 0.9 | 50 | yes |
| Idli Batter | logprob | 0.9951 | 1.0 | 1.0 | 50 | yes |
| Curry Leaves | logprob | 0.9987 | 0.025 | 0.025 | 60 | yes |
| Sunflower Oil 5L | deterministic | 1.0000 | 5.0 | 5.0 | 1 | yes |
| Dettol Hand Wash 60 ml Refill | deterministic | 1.0000 | 0.06 | 0.06 | 1 | yes |
| Maggi Masala Noodles 30 G x 30 sachet | deterministic | 1.0000 | 0.9 | 0.9 | 1 | yes |

## Gold rows not yet scored

Run `python uom_confidence.py --input gold.csv --output gold_scored.csv` (needs OPENAI_API_KEY), then re-run this benchmark with `--scored gold_scored.csv`.

- Tata Salt 1kg
- Amul Taaza Toned Milk 500ml Pouch
- Coca-Cola 1.25 L
- Aashirvaad Atta 5kg
- Paneer Fresh 200g
- Onion 1 Kg
- Lays Classic Salted 52g
- Red Bull Energy Drink 250ml Can
- Surf Excel Matic 2 Kg
- Ginger 250 g
- Eggs - Pack of 12
- Coriander Bunch
- Watermelon Big
- Bread - Whole Wheat Loaf
- Green Chilli
- Toor Dal Loose
- Tender Coconut
- Lemon

## Caveats

- Only **7 evaluable rows** — treat every number above as directional, not statistically meaningful. The gold set should grow to a few hundred labeled rows before calibration (isotonic/Platt in `calibrate()`) is fitted.
- Gold values for estimate rows are typical retail quantities with wide tolerances; they reward order-of-magnitude correctness, not exactness.

