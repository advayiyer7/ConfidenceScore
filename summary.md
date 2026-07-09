# ConfidenceScore — Current Method (Summary)

**Goal:** classify noisy Indian B2B catalog product titles as Branded/Unbranded
with a per-row confidence trustworthy enough to auto-accept most rows.
**Policy:** low-confidence-wrong is fine (routes to review); high-confidence-
wrong must not ship. **Constraint:** confidence is always measured from token
logprobs — never a self-reported number.

## Architecture (three stages, three bands)

```
title ─► 1. CLASSIFIER   claude-sonnet-4-6, minimal goal-phrased prompt
              → {Branding, Brandname, Reasoning}  (strict JSON)
      ─► 2. SCORER       gpt-4o, 0-9 digit rubric, digit is the FIRST token
              → confidence = probability-weighted expected digit / 9
      ─► 3. ROUTE by confidence:
              >= 0.85      auto-accept
              0.70 - 0.85  PHASE 2: live web search on the candidate name
                           (+ catalog sibling context) → gpt-4o logprob
                           re-verdict; accept iff A and >= 0.85
              <  0.70      human review
```

### 1. Classifier prompt (Sonnet) — deliberately minimal

Context line + goal + output shape, nothing else. A/B tested against a long
trap-inventory prompt: the minimal prompt did strictly better (896 vs 841
verifier-accepted; every trap case still correct). Prompt scaffolding was not
load-bearing; the model's own knowledge was.

### 2. The digit scorer (the key invention)

Binary Agree/Disagree verifier prompts saturate: every wording tested was
either too lenient (deferential prompt → constant ~1.0) or too harsh
(adversarial prompt → 0.0 on all obscure-but-real brands). The fix was the
answer format, not the wording: **rate support on a 0-9 rubric** (9 = checkable
anchors survive alternative readings; 4-6 = cannot verify either way;
0-1 = refuted), with the digit forced as the **first output token** and a
<=100-word justification after it. Confidence is read from `top_logprobs` at
position 0 across all ten digit tokens: `conf = Σ(digit × p) / Σp / 9`.

Why it works:
- ten tokens give the model a *middle* to put mass on — binary has none;
- verdict-before-reasoning keeps the logprob a measurement, not
  self-persuasion (reasoning-then-verdict was twice shown to destroy the
  signal: the arbiter negative result and the deferential-prompt test);
- the justification text is still produced, for human reviewers.

Result on the full 1,000-row catalog (`finalconfident.csv`): no saturation
(range 0.40-0.96), sensible ordering — wrong-brandname extractions
(`Quarry And Tile`, `N20`) at the bottom, real obscure brands (`Eastmade`,
`Fryola`) near the top, and all 12 known Sonnet-vs-Opus conflicts pushed into
the borderline 0.85-0.90 band (the binary verifier had scored them ~1.0).

### 3. Phase 2 — web-search grounding for the middle band

For each 0.70-0.85 row: gpt-4o with the `web_search` tool researches the
candidate brand name (instructed to report every company found and NOT judge
product fit — sellers here tag items outside their known catalog), with
catalog sibling context ("'Snacc' appears on 21 items: …"). Findings + context
go to a fresh gpt-4o logprob verdict under an evidence-weighing prompt
(web findings and catalog recurrence = strong; the verifier's own
non-recognition = weak). Median of k=3 calls damps jitter.

## Results (1,000-row catalog, Opus labels as the independent check)

| band | rows | outcome | Opus-disagrees |
|---|---|---|---|
| auto-accept (>= 0.85) | 717 | accepted | 8 (all at 0.85-0.90) |
| phase-2 web search (0.70-0.85) | 268 | 211 accepted / 57 review | 2 accepted / 2 held |
| human review (< 0.70) | 15 | review | 0 |
| **total** | **1,000** | **928 accepted / 72 review** | **10 known-wrong accepted** |

- Phase 2 rescued the real-but-web-obscure sellers (Sassy Teaspoon, Getaway,
  Ether, Eastmade, Cookie Cartel…) with zero Opus disagreements among them
  in the first (binary-grey) run.
- Alternative operating point: **auto-accept at 0.90 → zero known-wrong
  accepts** at 43% auto-acceptance (all 12 conflicts fall out of auto-accept).
- The <0.70 pile is genuinely dubious: brandname extraction errors and
  unresolvable names.

## Known issues / next levers

1. **Unbranded-side blind spot (the Murukku leak).** When Sonnet says
   Unbranded, Brandname=NA, so the catalog-sibling lookup never fires and the
   web researcher happily confirms the food-word reading. 7 seller-suffix
   rows (`- Murukku`) are still confidently wrong. Fix: run the sibling
   lookup on the trailing `- X` token even when the label is Unbranded.
2. **Scale compression.** The scorer rarely emits 9, so trivially-correct
   rows can land at 0.80-0.85 and inflate the phase-2 band (~$15/run).
   Mitigations: 0.90 auto-accept line, or skip web search for Unbranded rows
   with no candidate token.
3. **No true gold labels.** All error counts use Opus as the reference;
   a stratified ~100-row hand-label would put hard numbers on each band.
4. **Gazetteer.** The 57-row review residue is names no public source
   verifies; accumulated human verdicts should become a lookup so each is
   paid for once.

## Files

| file | role |
|---|---|
| `distinct_products_po_1000.csv` | input catalog (1,000 titles) |
| `opus_phase1_results.csv` | Sonnet outputs (label/brandname/reasoning) + binary-verifier conf + independent Opus labels |
| `finalconfident.csv` | **deliverable**: digit-scorer confidence + band status per title |
| `phase2_results_070_085.csv` | phase-2 web-search outcomes for the 0.70-0.85 band |
| `pipeline/run_phase1.py` | classifier + (binary) verifier runner |
| `pipeline/run_scorer.py` | digit-scorer verifier → finalconfident.csv |
| `pipeline/run_phase2.py` | web-search phase 2 |
| `pipeline/engines.py` | prompts, logprob extraction, throttling, mocks |
| `past.md` | every prior approach and why it was superseded |
