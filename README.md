# ConfidenceScore

Two-stage branded/unbranded classifier for noisy Indian B2B catalog titles, with
**measured confidence** from token logprobs — never self-reported. Governing
policy: low-confidence-wrong routes to review; **high-confidence-wrong must not
ship**. When in doubt, rows move INTO the grey zone, never out of it.

(The previous entity-first/CEC pipeline lives in git history at `a115801`;
`advaynextclaude.md` documents it and the lessons this design inherits.)

## Architecture

```
Phase 1:
  title ──► ENGINE 1  claude-sonnet-4-6
            rich classification {Branding, Brandname, Reasoning} (fact-dense,
            must self-declare "morphology-based inference" / "unrecognized token")
        ──► ENGINE 2  gpt-4o, logprobs=True
            adversarial auditor, forced single token A/D
            confidence = renormalized P(A) over {A, D} token mass
        ──► accept iff verdict A AND p_agree >= 0.85, else grey

Phase 2 (grey only):
  grey  ──► ENGINE 3  gpt-5 (no logprobs — it 403s; classifier only)
            fresh derivation, sees phase-1 output + auditor concern
        ──► ENGINE 2 re-verifies the new output
        ──► accept iff A AND >= 0.85, else review_queue.csv
```

Guard rails:
- A verifier Disagree never flips a label — it only routes to Phase 2 / review.
- A Branded label whose deciding reasoning admits "morphology-based inference"
  can never be accepted (deterministic guard + verifier instruction).
- The verifier completion is ONE token — no reasoning before the verdict
  (reasoning-then-verdict logprobs measure self-persuasion; documented negative
  result from the previous pipeline).
- Terminal API errors (quota/auth) abort the run loudly; rows are flushed per
  row, so `--resume` continues where it died. No silent label defaults, ever.

## Run

```bash
pip install openai anthropic python-dotenv pytest
# .env: ANTHROPIC_API_KEY=...  OPENAI_API_KEY=...

python -m pipeline.run_phase1                # distinct_products_po_1000.csv -> phase1_results.csv
python -m pipeline.run_phase2                # -> final_predictions.csv + review_queue.csv

# useful flags (both scripts): --mock  --resume  --limit N  --k N (median-of-N
# verifier)  --grey 0.85  --tpm 30000  --workers 6  --e1/e2/e3-model ...
```

Offline check: `python -m pytest tests/` (20 tests: logprob extraction variants,
strict JSON parsing, resume, and a 12-title mock smoke set covering every trap
class — famous-brand-as-generic-words, vernacular words, seller-slot food names,
inline brands, internal codes).

## Output schema (`final_predictions.csv`)

```
title, label, brandname, confidence, verdict, phase, status, reasoning_s1,
reasoning_s2, p_agree_s1, p_agree_s2, flags
```

`status ∈ {accepted, review}`, `phase ∈ {1, 2}`, flags include `likely_wrong`
(high-confidence Disagree, priority review), `verifier_anomaly`,
`stage1_error`/`stage2_error`, `morphology_guard`.

## Files

| file | purpose |
|---|---|
| `pipeline/config.py` | models, thresholds (GREY=0.85), rate limits — all CLI-overridable |
| `pipeline/engines.py` | three engine clients, logprob extraction, TPM throttle, mocks |
| `pipeline/schemas.py` | strict JSON contract for Engine 1/3 output |
| `pipeline/run_phase1.py` | classify + verify → `phase1_results.csv` |
| `pipeline/run_phase2.py` | grey-zone escalation → `final_predictions.csv`, `review_queue.csv` |
| `tests/` | acceptance tests incl. mock end-to-end smoke |
| `phase1_results.csv` | current phase-1 run: Sonnet labels + gpt-4o logprob confidence |
| `opus_phase1_results.csv` | same + independent Opus label column (`OPUS(BRAND/NO BRAND)`) |
| `*_raw.jsonl` | every raw API response, for audit (not committed) |
