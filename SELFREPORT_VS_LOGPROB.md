# Logprob Confidence vs. Self-Reported Confidence

- **Generated:** 2026-06-15
- **Logprob file:** `newtest_scored.csv`
- **Self-report file:** `newtest_selfreport.csv`

Both runs score the same rows with the same deterministic fast path. The difference is the confidence signal on model-estimated rows: one is derived from token **logprobs** (the candidate-selection mass), the other is **self-reported** — the model is simply asked "how confident are you, 0-1?". This contrasts them, split by brand. Comparison is over the **38 model-estimated rows** only.

## Mean confidence by method

| group | n | logprob | self-reported | Δ (self − logprob) |
|---|---|---|---|---|
| all | 38 | 0.9021 | 0.5842 | -0.3179 |
| branded | 7 | 0.7468 | 0.6429 | -0.1040 |
| unbranded | 31 | 0.9372 | 0.5710 | -0.3662 |

Δ is self-reported minus logprob mean. The sign is not the headline (self-report can run high or low); the point is the two signals disagree by a large margin, and the spread table below shows which one is actually discriminating.

## Spread: does the score actually discriminate?

A useful confidence varies with uncertainty. Self-reported numbers tend to collapse onto a few round values (low distinct count, high share on the 0.05 grid, low std dev).

| method | distinct values | std dev | share on 0.05 grid | min | max |
|---|---|---|---|---|---|
| logprob | 38 / 38 | 0.1354 | 0.03 | 0.5101 | 1.0000 |
| self-reported | 5 / 38 | 0.1328 | 1.00 | 0.5000 | 0.9000 |

## Takeaway

Across 38 estimated rows, self-reported confidence used only **5 distinct values** (100% of them on the 0.05 grid) versus **38** for the logprob score. Self-report defaults to a flat 0.5 on commodity produce (Spring Onion, Tomato, Curry Leaves) — items the logprob method rates ~0.99 because their typical retail size is well known. It is keying off "the title has no number", not real uncertainty. The logprob signal is continuous and orders rows by genuine sizing difficulty; the self-reported one cannot.

## Per-row, side by side

| title | brand | logprob | self-reported | self − logprob |
|---|---|---|---|---|
| Chilli Cheese mixer-Snacc | branded | 0.5101 | 0.5000 | -0.0101 |
| Broccoli | unbranded | 0.5702 | 0.5000 | -0.0702 |
| Green Zucchini | unbranded | 0.5793 | 0.5000 | -0.0793 |
| Ajinomoto (Golden Crown) | branded | 0.6664 | 0.5000 | -0.1664 |
| #_# Salted Caramel Brownie - Sassy Teaspoon | branded | 0.7416 | 0.6000 | -0.1416 |
| Pizza Box 12*12 (TS) | branded | 0.7481 | 0.7000 | -0.0481 |
| Lettuce Green Curly/Leafy | unbranded | 0.7565 | 0.5000 | -0.2565 |
| ONION LARGE | unbranded | 0.7735 | 0.5000 | -0.2735 |
| Samosa (half Done)-Snacc | branded | 0.7969 | 0.9000 | +0.1031 |
| Paneer Tikka filling-Snacc | branded | 0.8559 | 0.5000 | -0.3559 |
| EGGS TRAY | unbranded | 0.8623 | 0.8000 | -0.0623 |
| #_# Strawberry Raspberry Ice Pop - Getaway | branded | 0.9089 | 0.8000 | -0.1089 |
| Paneer | unbranded | 0.9199 | 0.5000 | -0.4199 |
| Rajma (Kidney beans) Pkt | unbranded | 0.9464 | 0.6000 | -0.3464 |
| Coriander Leaves (Dhaniya) | unbranded | 0.9485 | 0.6000 | -0.3485 |
| EGGS TRAY | unbranded | 0.9632 | 0.8000 | -0.1632 |
| Carrot | unbranded | 0.9690 | 0.5000 | -0.4690 |
| TOMATO | unbranded | 0.9767 | 0.5000 | -0.4767 |
| American Corn | unbranded | 0.9782 | 0.8000 | -0.1782 |
| CARROT | unbranded | 0.9792 | 0.5000 | -0.4792 |
| Eggplant (Brinjal) | unbranded | 0.9810 | 0.5000 | -0.4810 |
| MILK FULL CREAM | unbranded | 0.9836 | 0.5000 | -0.4836 |
| Onion Big | unbranded | 0.9840 | 0.5000 | -0.4840 |
| MILK TONNED | unbranded | 0.9842 | 0.5000 | -0.4842 |
| Mint Leaves | unbranded | 0.9864 | 0.6000 | -0.3864 |
| Green Chilli | unbranded | 0.9867 | 0.5000 | -0.4867 |
| RAJMA | unbranded | 0.9868 | 0.5000 | -0.4868 |
| Button Mushroom | unbranded | 0.9873 | 0.5000 | -0.4873 |
| Bada Pyaz ( Big Onion) | unbranded | 0.9879 | 0.5000 | -0.4879 |
| Potato Bun | unbranded | 0.9887 | 0.8000 | -0.1887 |
| Cucumbar | unbranded | 0.9943 | 0.5000 | -0.4943 |
| Cauliflower | unbranded | 0.9944 | 0.8000 | -0.1944 |
| Mutton Boneless | unbranded | 0.9955 | 0.5000 | -0.4955 |
| Spring Onion | unbranded | 0.9964 | 0.5000 | -0.4964 |
| ONION LARGE | unbranded | 0.9976 | 0.5000 | -0.4976 |
| Spring Onion | unbranded | 0.9978 | 0.5000 | -0.4978 |
| Curry Leaves | unbranded | 0.9982 | 0.5000 | -0.4982 |
| Bok Choy incremental 0.5 10333 | unbranded | 1.0000 | 0.9000 | -0.1000 |

