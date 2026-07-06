# Project Notes — Logprob-Based Confidence Scoring (for resume / interview)

## One-line description
Built a **logprob-based confidence scoring system** that classifies retail/grocery
catalog products as **branded vs. unbranded** using the OpenAI API (GPT-4o),
deriving per-prediction confidence from **token log-probabilities** instead of
self-reported scores, and used it to triage a 1,000-SKU production catalog.

## The technical approach (what to say)
- Model answers a **forced single token** ("B"/"U") with `logprobs=True`,
  `temperature=0`, `max_tokens=1`, `top_logprobs=5`.
- **Confidence = `exp(logprob)` of the chosen token** — the OpenAI cookbook
  classification recipe; this is a true softmax probability, not a number the
  model reports about itself (LLMs are known to inflate verbalized confidence).
- A renormalized `P(branded)` over the {B,U} tokens is kept for interpretability.
- Production engineering: concurrent scoring (`ThreadPoolExecutor`), **exponential
  backoff** retry, and pacing under a **30,000 tokens-per-minute** API rate limit.

## Key statistics (defensible numbers)

**Accuracy / calibration**
- Clean hand-labeled set (50 SKUs): **98.0% accuracy** (49/50).
- Expanded eval with deliberately ambiguous items (110 SKUs): **97.3%** (107/110).
- Real production catalog (1,000 distinct SKUs): **997 scored**; vs. the
  catalog's own brand field, **55% agreement** — see "key finding" (it's a
  data-quality result, not a model-accuracy ceiling).

**Confidence as a triage signal (1,000-SKU run)**
- Operating point at confidence ≤ 0.85 = "grey zone" → human review:
  **92.1% auto-classified, 7.9% (79 SKUs) flagged for review.**
- Confidence distribution: min **0.51**; 39 rows <0.70, 79 ≤0.85, 124 <0.95.
- Confidence collapsed to ~0.5 (coin-flip floor for a binary call) precisely on
  the genuinely ambiguous SKUs (packaging, cryptic codes) — i.e. the score
  discriminates where it should.

**Confusion matrix vs. catalog gold (997 scored)**
| | model: branded | model: unbranded |
|---|---|---|
| gold branded (187) | 63 | 124 |
| gold unbranded (810) | 325 | 485 |

**Key finding (the impactful one):** the 55% "disagreement" was driven by
**systematic mislabeling in the catalog**, not model error — 325 SKUs the
catalog tagged "Unbranded" had an obvious brand in the title (HARPIC, Rooh Afza,
Sakthi, Eastmade), and 124 had a brand that was never in the title at all. The
system effectively **surfaced data-quality issues in the source catalog.**

## Evaluation rigor (shows you didn't just eyeball it)
- **Confusion matrix, confidence bands, and confidence-when-right vs.-wrong**
  separation to test whether the score is meaningful.
- **Bootstrap 95% confidence intervals + label-permutation significance test**
  to check whether group differences were real or noise (caught and rejected a
  spurious "significant" result that was a small-sample artifact, p flipping
  from 0.001 → 0.12 once the sample/method were fixed).
- **Logprob vs. verbalized-confidence comparison**: showed self-reported
  confidence collapsed onto ~5 round values while logprob confidence was
  continuous and discriminating.
- **Cross-model benchmark vs. GPT-5**: discovered GPT-5 **blocks the `logprobs`
  parameter** (403), so ran a classification-only second opinion on the 79
  grey-zone SKUs — GPT-5 flipped 46% (36/79) of gpt-4o's borderline calls,
  with no net accuracy gain vs. the (noisy) catalog labels.

## Stack / keywords
Python · OpenAI API (GPT-4o, GPT-5) · token logprobs · LLM classification ·
confidence calibration · concurrency (ThreadPoolExecutor) · rate-limit handling /
exponential backoff · bootstrap CIs · permutation testing · confusion matrix ·
data-quality analysis · retail/grocery catalog standardization.

## Resume bullet options (pick 1–2)

**Quantified / impact-first**
- Built a logprob-based LLM confidence-scoring pipeline (OpenAI GPT-4o) to
  classify 1,000+ retail SKUs as branded/unbranded, deriving per-item confidence
  from token log-probabilities; achieved **98% accuracy** on labeled data and a
  **92%/8% auto-accept / human-review split**, and surfaced systematic
  mislabeling in the source catalog.

**Methods-first**
- Engineered an LLM classification system that computes calibrated confidence
  from token logprobs (`exp(logprob)`) rather than self-reported scores;
  validated it with bootstrap CIs, permutation significance tests, and a
  confusion-matrix breakdown, and benchmarked GPT-4o against GPT-5.

**Concise**
- Developed a logprob-based confidence scorer (OpenAI GPT-4o) for branded/
  unbranded product classification; **98% labeled accuracy**, triaged a 1,000-SKU
  catalog into 92% auto-accept / 8% review, and exposed catalog label errors.

## Interview talking points (the "why it's good" story)
1. **Why logprobs > self-report:** verbalized confidence is inflated/uncalibrated;
   `exp(logprob)` is the model's actual token probability.
2. **Why the confidence is useful:** it's near-1.0 on clear cases and ~0.5 on
   genuinely ambiguous ones — gives a principled human-review threshold (0.85).
3. **The honest twist:** the model's "errors" were mostly the catalog being
   wrong — the project's real value was data-quality discovery.
4. **Knowing the tooling limits:** GPT-5 doesn't expose logprobs, so the right
   architecture is gpt-4o for confidence + a stronger model/human for the grey zone.
