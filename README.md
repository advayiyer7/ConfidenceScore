# ConfidenceScore

Branded/Unbranded classification for noisy Indian B2B catalog titles, with
**measured confidence** from token logprobs — never self-reported. Governing
policy: low-confidence-wrong routes to review; **high-confidence-wrong must
not ship**.

Full method write-up: **[summary.md](summary.md)**. Every prior approach and
the standing negative results: **[past.md](past.md)**.

## Architecture

```
title ─► claude-sonnet-4-6      minimal goal-phrased prompt
              {Branding, Brandname, Reasoning}
      ─► gpt-4o DIGIT SCORER    0-9 rubric, digit forced as FIRST token;
              confidence = probability-weighted expected digit / 9
      ─► route by confidence:
              >= 0.85      auto-accept
              0.70 - 0.85  phase 2: web search on the candidate name
                           (+ catalog sibling context) → logprob re-verdict
              <  0.70      human review
```

Key design rules (each backed by a measured negative result — see past.md):
one-token-first verdicts only (reasoning-before-verdict measures
self-persuasion); no deference instructions; "plausible" is not an acceptance
criterion; binary A/D output saturates — the 0-9 scale is what gives the
middle band.

## Run

```bash
pip install openai anthropic python-dotenv pytest
# .env: ANTHROPIC_API_KEY=...  OPENAI_API_KEY=...

python -m pipeline.run_phase1     # Sonnet classify + binary verifier (legacy verifier)
python -m pipeline.run_scorer     # 0-9 digit scorer -> finalconfident.csv
python -m pipeline.run_phase2     # web-search grounding for the middle band
python -m pytest tests/           # offline acceptance tests (mocked engines)
```

All runners flush per row and support `--resume`; terminal API errors
(quota/auth) abort loudly — a failed row is never defaulted to a label.

## Results (1,000-row catalog, independent Opus labels as the check)

| band | rows | outcome |
|---|---|---|
| auto-accept (>= 0.85) | 717 | 8 Opus-disagrees, all borderline 0.85-0.90 |
| phase-2 web search (0.70-0.85) | 268 | 211 accepted / 57 review |
| human review (< 0.70) | 15 | genuinely dubious |
| **total** | **928 accepted / 72 review** | 10 known-wrong accepts; 0 at the 0.90 line |

## Files

| file | purpose |
|---|---|
| `distinct_products_po_1000.csv` | input catalog |
| `opus_phase1_results.csv` | Sonnet outputs + binary verifier conf + Opus labels |
| `finalconfident.csv` | **deliverable** — digit-scorer confidence + band per title |
| `phase2_results_070_085.csv` | phase-2 outcomes for the middle band |
| `pipeline/` | engines (prompts, logprob extraction, throttle, mocks) + runners |
| `summary.md` / `past.md` | current method / project history |
| `advaynextclaude.md` | deep-dive on the June entity-first architecture |
