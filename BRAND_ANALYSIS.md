# Branded vs. Unbranded — Logprob Confidence

- **Generated:** 2026-06-16
- **Scored file:** `brand_eval_scored.csv`

Each product is classified branded/unbranded by the model in a single forced token (B/U) with logprobs on. The **confidence is the token probability mass on the chosen letter** — a real logprob, not a self-reported number. No quantity is involved.

## Headline

- **Accuracy** (vs. gold labels): **98.9%** (89/90)
- **Mean confidence:** 0.9992
- **Mean confidence when correct:** 0.9993
- **Mean confidence when wrong:** 0.9986
- **Separation (right − wrong):** +0.0007 — positive means the logprob confidence actually tracks correctness.

## Confidence by true class

| true class | n | mean confidence | accuracy |
|---|---|---|---|
| branded | 41 | 0.9988 | 97.6% |
| unbranded | 49 | 0.9996 | 100.0% |

## Confidence bands

High ≥ 0.85 · Medium 0.70–0.85 · Low < 0.70.

| band | n | accuracy in band |
|---|---|---|
| high | 90 | 0.989 |
| medium | 0 | — |
| low | 0 | — |

## Misclassifications

| title | true | predicted | confidence |
|---|---|---|---|
| Pizza Box 12*12 (TS) | branded | unbranded | 0.9986 |

## Per-row detail

| title | true | pred | P(branded) | confidence |
|---|---|---|---|---|
| #_# Mango Duet (60 ml) - Go Zero | branded | branded | 1.0000 | 1.0000 |
| GK - Infinite Food - Lemon Ice Tea Powder (30 G x 30 sachet) | branded | branded | 1.0000 | 1.0000 |
| Alpha 6 -Toilet Bowl Cleaner 5L Can | branded | branded | 1.0000 | 1.0000 |
| Ajinomoto (Golden Crown) | branded | branded | 1.0000 | 1.0000 |
| #_# Raspberry Cream Cake [500 gms] - Sassy Teaspoon | branded | branded | 1.0000 | 1.0000 |
| #_# Salted Caramel Brownie - Sassy Teaspoon | branded | branded | 1.0000 | 1.0000 |
| #_# Kesar Pista Kulfi 300gm - Parsi Dairy Farm | branded | branded | 1.0000 | 1.0000 |
| #_# Frozen The Snicky Chonker (150g - Cookie) - Chonkers | branded | branded | 1.0000 | 1.0000 |
| Priya - Mustard Oil 1 L | branded | branded | 1.0000 | 1.0000 |
| Gig Great Indian Gin 750Ml | branded | branded | 1.0000 | 1.0000 |
| #_# Sugar Free Pancake Syrup [355Ml] - Noto | branded | branded | 1.0000 | 1.0000 |
| Haldiram Aloo Bhujia | branded | branded | 1.0000 | 1.0000 |
| McCain Smiles | branded | branded | 1.0000 | 1.0000 |
| Amul Cheese Slice | branded | branded | 1.0000 | 1.0000 |
| Britannia Bourbon Biscuit | branded | branded | 1.0000 | 1.0000 |
| Maggi Masala Noodles | branded | branded | 1.0000 | 1.0000 |
| Bikaji Soan Papdi | branded | branded | 1.0000 | 1.0000 |
| MTR Rava Idli Mix | branded | branded | 1.0000 | 1.0000 |
| Mother Dairy Lassi | branded | branded | 1.0000 | 1.0000 |
| Epigamia Greek Yogurt | branded | branded | 1.0000 | 1.0000 |
| Wow Momo Veg Momo | branded | branded | 1.0000 | 1.0000 |
| Theobroma Walnut Brownie | branded | branded | 1.0000 | 1.0000 |
| Keventers Cold Coffee | branded | branded | 1.0000 | 1.0000 |
| Go Cheese Cubes | branded | branded | 1.0000 | 1.0000 |
| Cornitos Nacho Crisps | branded | branded | 1.0000 | 1.0000 |
| Unibic Choco Chip Cookies | branded | branded | 1.0000 | 1.0000 |
| Nestle Munch Chocolate | branded | branded | 1.0000 | 1.0000 |
| Lay's Magic Masala | branded | branded | 1.0000 | 1.0000 |
| Haldiram Rasgulla | branded | branded | 1.0000 | 1.0000 |
| Amul Gold Milk 500ml | branded | branded | 1.0000 | 1.0000 |
| Tata Sampann Toor Dal 1kg | branded | branded | 1.0000 | 1.0000 |
| Surf Excel Liquid 1L | branded | branded | 1.0000 | 1.0000 |
| Kissan Mixed Fruit Jam 200g | branded | branded | 1.0000 | 1.0000 |
| Red Bull Energy 250ml | branded | branded | 1.0000 | 1.0000 |
| Colgate MaxFresh 100g | branded | branded | 1.0000 | 1.0000 |
| Chilli Cheese mixer-Snacc | branded | branded | 0.9999 | 0.9999 |
| Paneer Tikka filling-Snacc | branded | branded | 0.9998 | 0.9998 |
| #_# Sugar Free Red Ruby Thai Ice Cream Tub (125 ml) - Bina | branded | branded | 0.9998 | 0.9998 |
| Samosa (half Done)-Snacc | branded | branded | 0.9800 | 0.9800 |
| #_# Strawberry Raspberry Ice Pop - Getaway | branded | branded | 0.9724 | 0.9724 |
| Pizza Box 12*12 (TS) ⚠ | branded | unbranded | 0.0014 | 0.9986 |
| Potato Bun | unbranded | unbranded | 0.0177 | 0.9823 |
| Paneer tikka Cubes (200 GM) | unbranded | unbranded | 0.0004 | 0.9996 |
| Rajma (Kidney beans) Pkt | unbranded | unbranded | 0.0001 | 0.9999 |
| Olive Oil | unbranded | unbranded | 0.0001 | 0.9999 |
| Curry Leaves | unbranded | unbranded | 0.0000 | 1.0000 |
| Spring Onion | unbranded | unbranded | 0.0000 | 1.0000 |
| American Corn | unbranded | unbranded | 0.0000 | 1.0000 |
| Paneer | unbranded | unbranded | 0.0000 | 1.0000 |
| Mutton Boneless | unbranded | unbranded | 0.0000 | 1.0000 |
| Green Zucchini | unbranded | unbranded | 0.0000 | 1.0000 |
| MILK TONNED | unbranded | unbranded | 0.0000 | 1.0000 |
| MILK FULL CREAM | unbranded | unbranded | 0.0000 | 1.0000 |
| Green Chilli | unbranded | unbranded | 0.0000 | 1.0000 |
| Cucumbar | unbranded | unbranded | 0.0000 | 1.0000 |
| Coriander Leaves (Dhaniya) | unbranded | unbranded | 0.0000 | 1.0000 |
| CARROT | unbranded | unbranded | 0.0000 | 1.0000 |
| ONION LARGE | unbranded | unbranded | 0.0000 | 1.0000 |
| Bok Choy incremental 0.5 10333 | unbranded | unbranded | 0.0000 | 1.0000 |
| Button Mushroom | unbranded | unbranded | 0.0000 | 1.0000 |
| Bada Pyaz ( Big Onion) | unbranded | unbranded | 0.0000 | 1.0000 |
| Eggplant (Brinjal) | unbranded | unbranded | 0.0000 | 1.0000 |
| RAJMA | unbranded | unbranded | 0.0000 | 1.0000 |
| Spring Onion | unbranded | unbranded | 0.0000 | 1.0000 |
| Cauliflower | unbranded | unbranded | 0.0000 | 1.0000 |
| EGGS TRAY | unbranded | unbranded | 0.0000 | 1.0000 |
| TOMATO | unbranded | unbranded | 0.0000 | 1.0000 |
| EGGS TRAY | unbranded | unbranded | 0.0000 | 1.0000 |
| Lettuce Green Curly/Leafy | unbranded | unbranded | 0.0000 | 1.0000 |
| Mint Leaves | unbranded | unbranded | 0.0000 | 1.0000 |
| ONION LARGE | unbranded | unbranded | 0.0000 | 1.0000 |
| Onion Big | unbranded | unbranded | 0.0000 | 1.0000 |
| Broccoli | unbranded | unbranded | 0.0000 | 1.0000 |
| Carrot | unbranded | unbranded | 0.0000 | 1.0000 |
| Lady Finger | unbranded | unbranded | 0.0000 | 1.0000 |
| Bottle Gourd | unbranded | unbranded | 0.0000 | 1.0000 |
| Capsicum Green | unbranded | unbranded | 0.0000 | 1.0000 |
| Beetroot | unbranded | unbranded | 0.0000 | 1.0000 |
| Sweet Potato | unbranded | unbranded | 0.0000 | 1.0000 |
| Pomegranate | unbranded | unbranded | 0.0000 | 1.0000 |
| Guava | unbranded | unbranded | 0.0000 | 1.0000 |
| Drumstick | unbranded | unbranded | 0.0000 | 1.0000 |
| Raw Banana | unbranded | unbranded | 0.0000 | 1.0000 |
| Ridge Gourd | unbranded | unbranded | 0.0000 | 1.0000 |
| Methi Leaves | unbranded | unbranded | 0.0000 | 1.0000 |
| Red Cabbage | unbranded | unbranded | 0.0000 | 1.0000 |
| Spinach Fresh | unbranded | unbranded | 0.0000 | 1.0000 |
| White Radish | unbranded | unbranded | 0.0000 | 1.0000 |
| Turnip | unbranded | unbranded | 0.0000 | 1.0000 |
| Green Peas | unbranded | unbranded | 0.0000 | 1.0000 |

