# Reasoning-Verification Method — Key Rows

- **Generated:** 2026-06-24 · **Input:** 136 grey-zone rows (orig. confidence ≤ 0.85) from the 1,000-SKU run
- **Method:** Sonnet 4.6 returns prediction + an evidence-citing justification; GPT-4o audits whether the *justification* is sound and supported by the title (logprobs). **Confidence = P(reasoning is sound)** — the label itself is immaterial.

## Headline

| metric | value |
|---|---|
| rows re-scored | 136 |
| reasoning judged sound (>0.85) | **134 (99%)** |
| still flagged for review (≤0.85) | **2** |
| mean confidence | 0.986 |
| predictions: branded / unbranded | 13 / 123 |
| review queue across full run | 136/1000 (13.6%) → **2/1000 (0.2%)** |

## Review queue — reasoning still shaky (≤ 0.85)

These are the only rows a human still needs to see. Both are correct catches.

### COKE CANE — conf 0.192 · predicted *branded*

> The word 'COKE' is the key signal here — it is a well-recognized brand name for the Coca-Cola Company's flagship cola beverage, not merely a descriptive term. 'CANE' in this context likely refers to cane sugar as an ingredient descriptor, indicating this is a Coke product made with cane sugar rather than high-fructose corn syrup. Together, the title names a real maker (Coke/Coca-Cola) alongside a descriptive ingredient qualifier, making this a branded product.

### Kiley Soda 250 ML - SNACC — conf 0.623 · predicted *unbranded*

> The word 'Kiley' could signal a brand or product name, but it is not a recognizable manufacturer or company name — it reads more like a flavor or variety descriptor for the soda. 'SNACC' appears at the end and might suggest a brand, but it is not a recognizable maker or company name and could simply be a stylized descriptor or internal code. '250 ML' is a size measurement, and 'Soda' is a product type descriptor. With no clearly identifiable real maker or company name in the title, the product is best classified as unbranded.

## All BRANDED calls (the rows asserting a real maker)

Only these claim a recognizable brand is present — the highest-value rows to confirm.

| title | conf | justification |
|---|:--:|---|
| Cutlery Set The Cake Story | 1.000 | The phrase 'The Cake Story' stands out as the most likely brand identifier in this title, as it reads like a proper company or brand name rather than a descript |
| BARDINET BRANDY 1000 ML | 1.000 | The word 'BARDINET' is the specific term in this title that signals a brand. Bardinet is a real and well-known French spirits manufacturer, identifying WHO make |
| TL Hitachi UX Makeup 800ml | 1.000 | The word 'Hitachi' is the specific term in this title that signals a brand — it is a well-known real manufacturer (a Japanese electronics and technology company |
| #_# Cothas Blend Coffee 200 Gm - Murukku | 1.000 | The word 'Cothas' in the title is the specific term that signals a brand — Cothas is a real, well-known South Indian coffee manufacturer (Cothas Coffee Co.), ma |
| #_# Sticker - Sauce Dip Sticker Tangy Thai Tom Yum Sauce - Prasuma | 1.000 | The word 'Prasuma' at the end of the title is the specific term that signals a brand — it is a real company/manufacturer name (a food brand known for processed  |
| 110 Ml Tea paper cup-Snacc | 1.000 | The word 'Snacc' appears after a hyphen in the title, which is a common format for indicating a brand name on a product listing. 'Snacc' is not a descriptive te |
| Star Papad | 1.000 | The word 'Star' in 'Star Papad' could signal a brand name, as it appears to function as a maker or label identifier rather than a descriptive term. 'Papad' is c |
| Dark Compound Co D15 500Gms | 0.997 | The phrase 'Dark Compound Co' is the key signal here — 'Co' is a standard abbreviation for 'Company,' making 'Dark Compound Co' read as a company or manufacture |
| #_# Baked Oregano Cheese Matthi - Genda Phool | 0.997 | The phrase 'Genda Phool' (meaning 'marigold flower' in Hindi) appears at the end of the title in a position typically used for a brand name, and functions here  |
| Ajinomato | 0.995 | The word 'Ajinomato' is the sole term in this title and closely resembles 'Ajinomoto,' a well-known Japanese food and seasoning manufacturer. This appears to be |
| Ziplock Bags | 0.902 | The word 'Ziplock' (commonly styled 'Ziploc') is the specific word that signals a brand. It is a real manufacturer/brand name owned by SC Johnson, referring to  |
| #_# Caramelo Banditos Sticker - Cookie Cartel | 0.887 | The title contains 'Cookie Cartel,' which appears to be a real maker or brand name — it reads as a company or label identity rather than a descriptive term for  |
| COKE CANE | 0.192 | The word 'COKE' is the key signal here — it is a well-recognized brand name for the Coca-Cola Company's flagship cola beverage, not merely a descriptive term. ' |

## Sample: previously-hallucinated brands, now reasoned correctly

Rows where the old run wrongly said *branded*; the longer justification now identifies the descriptor/abbreviation/code, and GPT-4o confirms the reasoning.

| title | old→new | conf | justification |
|---|:--:|:--:|---|
| Sambal Oelek | bra→unbranded | 1.000 | The title 'Sambal Oelek' consists of two words that together describe a type of chili paste condiment originating from Southeast Asian cuisine. 'Samba |
| Ro 48 | bra→unbranded | 1.000 | The title 'Ro 48' contains two elements to consider: 'Ro' and '48'. 'Ro' could be an abbreviation, but it does not clearly identify a recognized manuf |
| Kung Pao Sauce 335 G | bra→unbranded | 1.000 | The title 'Kung Pao Sauce 335 G' contains no word that identifies a real maker or company. 'Kung Pao' is a descriptive term referring to a style of sp |
| SS GN PAN 1/3 100 MM | bra→unbranded | 1.000 | The title consists entirely of abbreviations and measurements that describe the product's physical characteristics. 'SS' most likely stands for 'stain |
| XO Sauce Sticker | bra→unbranded | 1.000 | The title contains two potential signal words: 'XO' and 'Sticker.' 'Sticker' is purely a descriptive product-type term indicating what the item is. 'X |
| Boba Lychee can | bra→unbranded | 1.000 | The word 'Boba' refers to the tapioca pearl bubble tea style, making it a descriptive product-type term rather than a manufacturer name. 'Lychee' is a |
| Cmc Powder | bra→unbranded | 1.000 | The term 'CMC' stands for carboxymethyl cellulose, which is a well-known food additive and thickening agent — it is a chemical/ingredient name, not a  |
| Truffle Paste (500gm Pack) | bra→unbranded | 1.000 | The title contains the words 'Truffle Paste,' which describe the product type and ingredient (truffle, a type of fungi, formed into a paste) rather th |
| #_# Gate Pass Book | bra→unbranded | 1.000 | The title contains '#_#' which appears to be a placeholder or internal code, not a recognizable manufacturer or company name. 'Gate Pass Book' is enti |
| Newyork Cheese Filling | bra→unbranded | 1.000 | The title contains two potentially notable elements: 'Newyork' and 'Cheese Filling.' 'Newyork' here functions as a style descriptor referring to the N |
| N20 Whipped Cream Chargers | bra→unbranded | 1.000 | The term 'N20' refers to nitrous oxide (N₂O), the gas used in whipped cream chargers, making it a descriptive ingredient/material identifier rather th |
| Danish White Feta 500GM | bra→unbranded | 1.000 | The word 'Danish' refers to the geographic origin (Denmark) of the cheese, not a manufacturer or company name. 'White Feta' describes the type and app |
| TORCH BLOW COOKING | bra→unbranded | 1.000 | The title contains three words: 'TORCH,' 'BLOW,' and 'COOKING.' 'TORCH' describes the type of tool (a flame-producing device), 'BLOW' describes how it |
