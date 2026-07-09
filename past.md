# Past Approaches (chronological) — what was tried and why it was superseded

All code and outputs referenced here live in git history (commit hashes noted).
Deep-dive on the June-era architecture: `advaynextclaude.md`.

## 1. Origins: logprobs vs verbalized confidence (June)
Started as a unit-of-measure confidence scorer. Established the project's
foundational finding: **self-reported ("I'm 90% sure") confidence collapses to
~5 round values and is uninformative; `exp(logprob)` of a forced answer token
is continuous and discriminating.** Every later design keeps this rule.

## 2. Single forced-token classifier (`brand_confidence.py`, git `4ddf7c0`)
One gpt-4o call per title: answer "B"/"U", confidence = exp(logprob) (OpenAI
cookbook recipe). 98.0% on 50 hand-labeled rows, 97.3% on 110. Statistical
rigor pass (bootstrap CIs, permutation test) caught a spurious significance.
**Why superseded:** confidence saturated at ~1.0 and was confidently wrong on
obscure tokens; no second opinion.

## 3. 1,000-SKU production run (June 21)
Bimodal confidence, 7.9% grey at 0.85. **Key data finding:** only ~55%
agreement with the catalog's own brand field — because the catalog itself
mislabels obvious brands (HARPIC tagged "Unbranded"). There is no clean gold
truth; the classifier doubles as a data-quality detector. Also discovered
**GPT-5-class reasoning models block the `logprobs` param (403)** — they can
classify but never provide confidence.

## 4. Dual-stage + reasoning-verification (git `d271be8` era)
Sonnet classifies + explains; gpt-4o verifies with a Yes/No logprob token.
A variant judged whether the *justification* was sound: 99% judged sound,
review queue 0.2%. **Why superseded:** that was overconfident agreement — the
verifier rubber-stamped fluent reasoning. First sighting of the central
failure mode: *plausible prose is not evidence.*

## 5. The Opus review: three failure modes
Independent review flagged: **Type-1** self-contradictions (MDH branded 8x,
unbranded 1x), **Type-2** unfamiliar suffix sellers called unbranded
(Ether, Murukku), **Type-3** inline brands missed (Knorr). Root cause:
recognizability bias + judging every title in isolation.

## 6. Entity-first + Cross-Examined Confidence (git `e7fd189`, `a115801`)
The June architecture: extract candidate maker tokens deterministically,
fuzzy-merge into entities, classify each entity ONCE (making Type-1
impossible by construction), then cross-examine with adversarial probes
(is it generic-in-context? does a non-company meaning fit?) combined by an
**agreement gate** (unanimous → weakest vote; any conflict → 0.5), plus a
**recognition gate** capping thin-evidence brand calls the model hasn't
actually heard of. Result: 0 split labels, 30/30 on the policy eval, grey
26.6%. **Negative result recorded:** a reasoning-then-verdict arbiter to
resolve grey rows was decisively wrong in both directions (murukku→No@1.0,
Kit Kat→No@1.0, kanga→Yes@1.0) — *reasoning makes the model more persuasive
to itself, not more reliable.* **Why superseded:** the user pivoted (July 6)
to a simpler per-title two-stage design; the entity layer's key insight
(cross-category recurrence proves a seller) survives as the catalog-sibling
context in phase 2. Full detail: `advaynextclaude.md`.

## 7. Two-stage pipeline, binary verifier era (July 6-8, git `fff5fb6`..`ee4d078`)
Sonnet 4.6 rich classification → gpt-4o(-mini) adversarial auditor, forced
single A/D token, confidence = renormalized P(A).
- **Rich vs minimal classifier prompt:** minimal won (896 vs 841 accepted,
  all trap cases equal) — trap inventories weren't load-bearing.
- **gpt-4o-mini vs gpt-4o verifier:** same net accept (~90%); 14/81 of mini's
  hard-rejects were knowledge-floor false alarms rescued by 4o; 52
  obscure-but-real brands rejected by BOTH → model size can't verify what
  the training data lacks.
- **The 12-conflict finding:** Sonnet and Opus disagreed on 12/1000 rows —
  ALL inside the accepted set at conf ≥ 0.85 (7 Murukku seller rows + 5
  others), and the verifier flagged 0 of them. Grey zone had ZERO
  cross-model disagreements. Verifier logprobs and cross-model disagreement
  are orthogonal error signals.
- **GPT-5 escalation phase 2:** worked (41/159 rescued) but slow (~2.5
  min/call) and 24 parse failures; replaced by web-search phase 2.
- **Why superseded:** binary output saturates — the verifier was either too
  harsh or too lenient, with no middle (see 8).

## 8. Verifier-prompt experiments (July 9, TestingDiffPromptPhase series)
On the 200 lowest-confidence rows:
- **v1 deferential, reasoning-first** ("higher model may know more; plausible
  ⇒ agree"): constant ~1.0. Zero signal. Deference + a plausibility bar +
  reasoning-before-verdict each independently destroy discrimination.
- **v2 paranoid, verdict-first**: constant ~0.0. Over-corrected.
- **v3 merged (adversarial criteria + four-input structure + verdict-token
  first)**: real spread; 17/17 accepts Opus-correct; caught all 4 conflicts
  in the sample — but too strict (17/200 accepted).
- **Conclusion that produced the current method:** the binary A/D format is
  the root cause — no wording can express 0.6 with two tokens. → the 0-9
  digit scorer (see `summary.md`).

## Standing negative results (do not revisit without new evidence)
1. Verbalized/self-reported confidence — uninformative.
2. Reasoning-then-verdict logprobs — measure self-persuasion (arbiter, v1).
3. Deference instructions in a verifier — collapse to constant Agree.
4. "Plausible reasoning ⇒ agree" — always true, hence no signal.
5. Bigger verifier model as a fix for unverifiable brands — both sizes fail
   the same 52 rows; evidence (catalog recurrence, web search, gazetteer)
   is the only fix.
6. Web search cannot fix wrong-*Unbranded* labels when no candidate name is
   extracted (the Murukku leak) — needs the suffix-token sibling lookup.
