# ConfidenceScore

Logprob-based confidence for classifying grocery/food product titles as
**branded** vs. **unbranded**, using the OpenAI API.

The confidence is derived from the model's **token logprobs** — not a
self-reported "I'm 90% sure" number, which LLMs are known to inflate.

## How it works

For each product title the model answers a single forced token — `B` (branded)
or `U` (unbranded) — with `logprobs=True`. The probability mass on the chosen
letter, renormalized over `{B, U}`, is the confidence:

```
P(branded)  = exp(lp_B) / (exp(lp_B) + exp(lp_U))
prediction  = branded if P(branded) >= 0.5 else unbranded
confidence  = max(P(branded), 1 - P(branded))
```

A *branded* product is sold under a specific company/brand name (Amul, Maggi,
Haldiram); an *unbranded* one is generic, loose, or a commodity (Onion, Curry
Leaves, Tomato). No quantity or unit estimation is involved.

## Usage

```bash
pip install openai
export OPENAI_API_KEY=sk-...   # PowerShell: $env:OPENAI_API_KEY = "sk-..."

python brand_confidence.py --input brand_eval.csv --output brand_eval_scored.csv \
    [--model gpt-4o] [--workers 3]
```

Input needs a `title` column (and optionally a `brand` gold label, carried
through for scoring). Output appends `pred_brand`, `confidence`, and
`p_branded`.

## Analysis

`brand_analysis.py` reads the scored file and reports how good the logprob
confidence is: overall accuracy vs. gold, mean confidence per true class,
confidence bands, **confidence-when-right vs. confidence-when-wrong** (does the
logprob actually track correctness?), and a list of misclassifications.

```bash
python brand_analysis.py --scored brand_eval_scored.csv --output BRAND_ANALYSIS.md
```

See `BRAND_ANALYSIS.md` for the latest run.

## Files

| file | purpose |
|---|---|
| `brand_confidence.py` | the logprob B/U classifier |
| `brand_analysis.py` | accuracy + confidence analysis |
| `brand_eval.csv` | 90 labeled titles (`title`, `brand`) |
| `brand_eval_scored.csv` | scored output |
| `BRAND_ANALYSIS.md` | generated report |

## Current finding

On the 90-row eval set the classifier is **98.9% accurate**, but the logprob
confidence **saturates near 0.999 for both correct and wrong calls** — the
branded/unbranded distinction is too easy here, so the confidence barely
discriminates (it was 0.9986 even on the single misclassification). The
confidence only becomes informative once **genuinely ambiguous items** (private
labels, ambiguous abbreviations, brand-like common words) are added to the set.

> The old quantity/UoM CSVs from a previous project direction have been removed.
