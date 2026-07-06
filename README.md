# ConfidenceScore

Logprob-based confidence for classifying grocery/food product titles as
**branded** vs. **unbranded** — engineered so that **high-confidence-wrong
predictions cannot ship**. Low-confidence rows route to a human review queue;
confident rows must earn it.

All confidence values are real **token logprobs** (renormalized probability
mass on a forced answer token) — never a self-reported "I'm 90% sure" number,
which LLMs are known to inflate.

## Architecture (current)

The unit of classification is the **maker entity, not the title**. Deciding
once per brand name and propagating makes self-contradictions (the same brand
labeled both ways across the catalog) impossible by construction.

```
titles ──► entity_extract.py      deterministic: candidate maker tokens
                │                 (suffix seller-slot, corpus-confirmed
                │                  acronyms, inline/prefix, shouty fallback),
                │                  fuzzy entity resolution, corpus signals
                ▼
           entity_first.py        probe A per unique entity (GPT-4o logprob):
                │                 "is X a maker?" + structural evidence
                ▼
           cross_examine.py       probes B1+B2 (adversarial framings) and an
                │                 AGREEMENT GATE: unanimous → weakest vote;
                │                 any disagreement → 0.5 (forced review).
                │                 Title-probe safety net for titles where
                │                 extraction found nothing.
                ▼
           recognition_gate.py    confident-branded on thin evidence must ALSO
                │                 pass "have you actually heard of this
                │                 company?" — morphology alone can never
                │                 justify confidence.
                ▼
           final_predictions.csv  deliverable: title, prediction, confidence,
                                  deciding_entity
```

### Why three probes + a gate?

A single forced-token probe can be confidently wrong by *pattern-matching*
("coined-looking word ⇒ brand" fires at p≈0.99 on CHULLA — a Hindi stove).
The framings are chosen to fail differently:

| probe | question | catches |
|---|---|---|
| A | is X a maker? | the base decision |
| B1 | is X used as a generic product word *in these titles*? | descriptors in the seller slot (`- PAPAD`) |
| B2 | does X have a fitting non-company meaning (food, day, river, Hindi word)? | tokens that are *neither* product nor maker (TUES, GANGA) |
| recognition | have you actually *heard of* X as a company? | unanimous ignorance — all framings pattern-matching the same wrong way |

Votes combine by **agreement, not averaging** (a +5-logit framing must not
outvote a −3 dissenter): unanimous → confidence = weakest vote; any
disagreement → 0.5. GPT-4o at `temperature=0` still jitters across runs, which
is why the final gate (recognition) is a deterministic cap, not another vote.

### Negative result worth knowing

A reasoning arbiter (chain-of-thought, then a verdict token) was tested as a
way to resolve grey-zone conflicts — and was decisively wrong in both
directions on exactly the contested cases (`arbiter.py`, kept as
documentation). Reasoning makes the model more persuasive to itself, not more
reliable, on ambiguity. The residual grey zone is genuinely hard; human review
is its correct disposition.

## Review workflow

The grey zone is title-shaped but decisions are entity-shaped — reviewing
`murukku` once clears all 9 titles that carry it.

```bash
python review_queue.py        # grey titles -> impact-ordered decision queue
#   fill the human_label column (branded/unbranded), then:
python apply_reviews.py       # verdicts fan out to every affected title
```

## Running the pipeline

```bash
pip install openai anthropic python-dotenv
# .env: OPENAI_API_KEY=...  (ANTHROPIC_API_KEY only for legacy dual-stage)

python entity_first.py     --input dual_stage_scored.csv   # probe A (cacheable: --cache entity_decisions.csv)
python cross_examine.py                                    # probes B1+B2 + agreement gate + title net
python recognition_gate.py                                 # thin-evidence knowledge cap
python evaluate_cec.py final_predictions.csv               # grade vs the 30-case known-answer set
```

Every stage aborts on quota/auth errors rather than silently defaulting, and
resumes incrementally from its cached decisions.

## Results (1,000-SKU catalog)

| metric | per-title baseline | entity-first + CEC |
|---|---|---|
| split-label entities (self-contradictions) | ~17–20 | **0** |
| confident-wrong on 30 known-answer cases | 3 | **0** |
| Opus-review flagged errors fixed | — | Type-1 8/8 · Type-2 7/7 · Type-3 10/10 |
| review queue | 5.6% | 26.6% (266 titles → **240 one-glance decisions**) |

The larger grey zone is the price of the guarantee — and it is honest: it
contains the genuinely ambiguous items (obscure Hindi words, coined one-off
names, cryptic codes). Thresholds are tunable (`--grey`, `--cap`).

## Files

| file | purpose |
|---|---|
| `entity_extract.py` | deterministic extraction + entity resolution + corpus signals |
| `entity_first.py` | probe A: per-entity logprob classification |
| `cross_examine.py` | probes B1/B2, agreement gate, title safety net |
| `recognition_gate.py` | knowledge cap on thin-evidence branded calls |
| `evaluate_cec.py` | 30-case known-answer policy eval |
| `review_queue.py` / `apply_reviews.py` | human review loop |
| `consistency_audit.py` | Type-1 contradiction measurement |
| `arbiter.py` | negative result: reasoning arbitration (do not use) |
| `final_predictions.csv` | **deliverable** |
| `final_entity_decisions.csv` | per-entity audit trail (all probe values) |
| `brand_confidence.py` / `brand_analysis.py` | legacy per-title B/U classifier |
| `dual_stage_confidence.py` / `reasoning_verify.py` | legacy two-stage experiments |
