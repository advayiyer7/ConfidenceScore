# ConfidenceScore

Logprob-based confidence scoring for unit-of-measure (UoM) standardization of
grocery/food product rows, using the OpenAI API.

Given the output CSV of a 3-tier UoM pipeline (target unit already chosen in
`uom_std_unit`), the script fills in the standardized quantity and attaches a
confidence in [0,1] derived from **token logprobs** — not a self-reported
number — plus top-K alternative interpretations when confidence is low.

## How it works

1. **Deterministic fast path** (no API call): explicit measurements in the
   title/inferred fields (`5L`, `60 ml`, `30 G x 30 sachet` → 0.9 kg) are
   parsed directly → confidence 1.0.
2. **Two-stage logprob estimation** for everything else:
   - **Stage 1 (estimate):** the model returns 2–4 candidate interpretations
     `{std_unit, std_qty, reasoning}` as JSON. For "piece" items it estimates
     the typical weight of one piece in kg (e.g. one samosa ≈ 0.05 kg).
   - **Stage 2 (select, 1 token):** candidates are labelled A/B/C/… and the
     model answers with a single letter, called with `logprobs=True`. The
     top-logprob mass on the candidate letters is exponentiated, renormalized,
     and the chosen letter's probability becomes the confidence. Below the
     threshold, the top-K candidates ship as `alternatives`.

Confidence is currently **raw, uncalibrated** logprob mass — see the
`calibrate()` stub for where isotonic/Platt scaling will plug in.

## Usage

```bash
pip install openai
export OPENAI_API_KEY=sk-...   # PowerShell: $env:OPENAI_API_KEY = "sk-..."

python uom_confidence.py --input pipeline_out.csv --output scored.csv \
    [--model gpt-4o] [--threshold 0.70] [--k 2] [--workers 4] [--no-piece-to-kg]
```

Output keeps all original columns and appends `computed_std_qty`,
`confidence`, `confidence_source` (`deterministic` | `logprob` | `none`),
`alternatives` (JSON), and `model_reasoning`.

`sample_input.csv` / `sample_output.csv` show an example run.
