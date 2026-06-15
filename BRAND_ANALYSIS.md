# Confidence by Branded vs. Unbranded

- **Generated:** 2026-06-15
- **Scored file:** `newtest_scored.csv`

Breaks the logprob-derived `confidence` score down by whether the product carries a brand. No gold labels here — this measures the confidence distribution and coverage, not calibration. The split separates two effects: explicit pack sizes in the title (parsed deterministically at 1.0) versus how confidently the model can *size* an item that states no quantity (the LLM path). Read the estimate-only table for the fair comparison of the latter.

## Confidence score

| group | logprob confidence | all-rows confidence |
|---|---|---|
| branded | 0.7468 | 0.8958 |
| unbranded | 0.9391 | 0.9409 |

## Coverage and source split

| group | rows | scored | abstained | deterministic | LLM (logprob) |
|---|---|---|---|---|---|
| branded | 17 | 17 | 0 | 10 | 7 |
| unbranded | 33 | 33 | 0 | 1 | 32 |

## Confidence distribution (scored rows only)

| group | n | mean | median | min | share below 0.70 |
|---|---|---|---|---|---|
| branded | 17 | 0.8958 | 1.0000 | 0.5101 | 12% |
| unbranded | 33 | 0.9409 | 0.9842 | 0.5702 | 6% |

**Separation (branded − unbranded mean confidence): -0.0452** — branded items score LOWER.

## Estimate-only (LLM path), excluding deterministic 1.0s

The deterministic rows score 1.0 purely because the title states an explicit measurement, which would swamp the comparison. Restricting to LLM-estimated rows isolates how confidently the model *sizes* an item with no stated quantity.

| group | n | mean | median | min | share below 0.70 |
|---|---|---|---|---|---|
| branded | 7 | 0.7468 | 0.7481 | 0.5101 | 29% |
| unbranded | 32 | 0.9391 | 0.9841 | 0.5702 | 6% |

**Separation (branded − unbranded mean confidence): -0.1922** — branded items score LOWER.

## Per-row detail

| title | brand | source | confidence |
|---|---|---|---|
| #_# Mango Duet (60 ml) - Go Zero | branded | deterministic | 1.0000 |
| GK - Infinite Food - Lemon Ice Tea Powder (30 G x 30 sachet) | branded | deterministic | 1.0000 |
| Alpha 6 -Toilet Bowl Cleaner 5L Can | branded | deterministic | 1.0000 |
| #_# Raspberry Cream Cake [500 gms] - Sassy Teaspoon | branded | deterministic | 1.0000 |
| #_# Kesar Pista Kulfi 300gm - Parsi Dairy Farm | branded | deterministic | 1.0000 |
| #_# Frozen The Snicky Chonker (150g - Cookie) - Chonkers | branded | deterministic | 1.0000 |
| Priya - Mustard Oil 1 L | branded | deterministic | 1.0000 |
| Gig Great Indian Gin 750Ml | branded | deterministic | 1.0000 |
| #_# Sugar Free Pancake Syrup [355Ml] - Noto | branded | deterministic | 1.0000 |
| #_# Sugar Free Red Ruby Thai Ice Cream Tub (125 ml) - Bina | branded | deterministic | 1.0000 |
| #_# Strawberry Raspberry Ice Pop - Getaway | branded | logprob | 0.9089 |
| Paneer Tikka filling-Snacc | branded | logprob | 0.8559 |
| Samosa (half Done)-Snacc | branded | logprob | 0.7969 |
| Pizza Box 12*12 (TS) | branded | logprob | 0.7481 |
| #_# Salted Caramel Brownie - Sassy Teaspoon | branded | logprob | 0.7416 |
| Ajinomoto (Golden Crown) | branded | logprob | 0.6664 |
| Chilli Cheese mixer-Snacc | branded | logprob | 0.5101 |
| Bok Choy incremental 0.5 10333 | unbranded | logprob | 1.0000 |
| Paneer tikka Cubes (200 GM) | unbranded | deterministic | 1.0000 |
| Curry Leaves | unbranded | logprob | 0.9982 |
| Spring Onion | unbranded | logprob | 0.9978 |
| ONION LARGE | unbranded | logprob | 0.9976 |
| Olive Oil | unbranded | logprob | 0.9971 |
| Spring Onion | unbranded | logprob | 0.9964 |
| Mutton Boneless | unbranded | logprob | 0.9955 |
| Cauliflower | unbranded | logprob | 0.9944 |
| Cucumbar | unbranded | logprob | 0.9943 |
| Potato Bun | unbranded | logprob | 0.9887 |
| Bada Pyaz ( Big Onion) | unbranded | logprob | 0.9879 |
| Button Mushroom | unbranded | logprob | 0.9873 |
| RAJMA | unbranded | logprob | 0.9868 |
| Green Chilli | unbranded | logprob | 0.9867 |
| Mint Leaves | unbranded | logprob | 0.9864 |
| MILK TONNED | unbranded | logprob | 0.9842 |
| Onion Big | unbranded | logprob | 0.9840 |
| MILK FULL CREAM | unbranded | logprob | 0.9836 |
| Eggplant (Brinjal) | unbranded | logprob | 0.9810 |
| CARROT | unbranded | logprob | 0.9792 |
| American Corn | unbranded | logprob | 0.9782 |
| TOMATO | unbranded | logprob | 0.9767 |
| Carrot | unbranded | logprob | 0.9690 |
| EGGS TRAY | unbranded | logprob | 0.9632 |
| Coriander Leaves (Dhaniya) | unbranded | logprob | 0.9485 |
| Rajma (Kidney beans) Pkt | unbranded | logprob | 0.9464 |
| Paneer | unbranded | logprob | 0.9199 |
| EGGS TRAY | unbranded | logprob | 0.8623 |
| ONION LARGE | unbranded | logprob | 0.7735 |
| Lettuce Green Curly/Leafy | unbranded | logprob | 0.7565 |
| Green Zucchini | unbranded | logprob | 0.5793 |
| Broccoli | unbranded | logprob | 0.5702 |

