# Confidence Benchmark Results

- **Generated:** 2026-06-11
- **Scored file:** `test_scored.csv`
- **Gold file:** `test.csv`

Measures how well the logprob-derived `confidence` column predicts whether `computed_std_qty` is actually correct. A row counts as correct when the prediction is within its gold tolerance (tight for explicit measurements, loose for world-knowledge estimates).

## Coverage

| | count |
|---|---|
| Gold rows scored and evaluated | 71 |
| Gold rows where model abstained (missed coverage) | 46 |
| Non-estimable gold rows (correct behavior = abstain) | 5 (abstained on 5) |
| Scored rows without a gold label (skipped) | 0 |
| Gold rows not present in scored file | 0 |

## Headline metrics

| metric | value | reading |
|---|---|---|
| Accuracy | 1.0000 | fraction of predictions within tolerance |
| Mean confidence | 1.0000 | should track accuracy if calibrated |
| Calibration gap | +0.0000 | >0 means overconfident |
| Brier score | 0.0000 | 0 = perfect, 0.25 = uninformative |
| ECE | 0.0000 | expected calibration error, lower is better |
| AUROC | n/a | 1.0 = confidence perfectly ranks right above wrong; n/a if all rows are one class |
| Mean conf (correct rows) | 1.0000 | |
| Mean conf (incorrect rows) | n/a | |

## Per-source breakdown

| source | n | accuracy | mean confidence |
|---|---|---|---|
| deterministic | 71 | 1.0000 | 1.0000 |

## Ambiguity discrimination

Rows labeled `gold_ambiguous` have more than one defensible reading (e.g. "Paneer 1p", "Coca Cola 600"); a good confidence score should be **lower** there than on clear rows, pushing them below the review threshold.

_No ambiguous rows evaluated yet (ambiguous rows need the LLM path; run without --deterministic-only)._

## Reliability table

Within each confidence bin, mean confidence should match observed accuracy.

| confidence bin | n | mean confidence | accuracy | gap |
|---|---|---|---|---|
| [0.00, 0.50) | 0 | — | — | — |
| [0.50, 0.70) | 0 | — | — | — |
| [0.70, 0.80) | 0 | — | — | — |
| [0.80, 0.90) | 0 | — | — | — |
| [0.90, 1.00] | 71 | 1.0000 | 1.0000 | +0.0000 |

## Threshold sweep

If rows below the cutoff are routed to human review: coverage is the share auto-accepted, selective accuracy is the accuracy of what was auto-accepted.

| threshold | coverage | selective accuracy |
|---|---|---|
| 0.50 | 100% (71/71) | 1.0000 |
| 0.60 | 100% (71/71) | 1.0000 |
| 0.70 | 100% (71/71) | 1.0000 |
| 0.80 | 100% (71/71) | 1.0000 |
| 0.90 | 100% (71/71) | 1.0000 |
| 0.95 | 100% (71/71) | 1.0000 |

## Overconfident errors (confidence ≥ 0.90 but wrong)

None.

## Missed coverage (gold available, model abstained)

- Farm Fresh Eggs - Pack of 6
- Banana Yelakki
- Tender Coconut Medium
- Coriander Leaves Bunch
- Mint Leaves Bunch
- Spinach Palak Bunch
- Dosa Batter Fresh Homestyle
- Chapati Dough Fresh
- Paneer Half Kg Fresh
- Sugar Quarter Kg Pack
- Punjabi Samosa Single
- Veg Puff Bakery Fresh
- Butter Croissant Large
- Watermelon Kiran Big
- Pineapple Queen Whole
- Cabbage Medium Fresh
- Multigrain Bread Loaf
- Spiced Buttermilk Pouch
- Traditional Curd Pot
- Dozen Bananas Robusta
- Ginger Fresh Loose
- Green Chilli Loose
- Sweet Corn Steamed Cup
- Rasgulla Tin Standard
- Dabur Honey 500g Jar
- Nestle Dahi 400g Cup
- Pure Desi Ghee 1kg Jar
- Paneer Fresh 1p
- Amul Butter 1 lb
- Borges Olive Oil 1 gal
- Cheddar Cheese Block 8 oz
- Tropicana Orange Juice 16 oz
- Parle-G Biscuit 10
- Lays Chips Pack 20
- Coca Cola Bottle 600
- Amul Milk Pouch 500
- Eggs Tray 30
- Sugar 5k Value Pack
- Dettol Soap 4x75
- Frooti Mango 160 Tetra Pack
- Onion Sack 2-3 kg
- Ghee 1 pav Loose
- Curd 1 ser Local Dairy
- Pepsi Mega Bottle 2.25
- Maaza Mango Drink 1.2L/600ml
- Britannia Bread 400/800g

