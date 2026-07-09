# ConfidenceScore — Complete Project Handoff & Algorithm Documentation

**Purpose of this document:** a self-contained description of everything built in this
project — the problem, every iteration of the algorithm, the exact mechanics of the
current pipeline, all empirical results, negative results, and known weaknesses — so
that a fresh model (no repo access) can propose a structured plan for improving the
system. The ask is at the end.

---

## 1. The problem

Classify grocery/food-service catalog product **titles** (real Indian B2B catalog data,
noisy, multilingual, full of internal codes) as **branded** vs **unbranded**, with a
per-prediction **confidence** that is trustworthy enough to auto-accept most rows and
route the rest to human review.

Examples of the data's character:

- `#_# Mango Biscoff Tub - Sassy Teaspoon` → branded (seller "Sassy Teaspoon" in trailing slot)
- `Curry Leaves`, `ONION LARGE`, `EGGS TRAY` → unbranded
- `CHULLA` → a Hindi word for stove — unbranded, but *looks* like a coined brand
- `#_# Stirrer - Murukku` → "Murukku" is a famous snack word, but here it's a **seller name** (it also labels asafoetida and modak in the same catalog)
- `RED LABEL TEA (1 KG)` → a famous brand written as two individually-generic words
- `GLUTEN NB 0121`, `3CP PLATE`, `95 Die lid` → internal codes / packaging SKUs, genuinely ill-posed

**The governing policy (set by the user, drives the whole architecture):**
> Low-confidence-wrong is acceptable (it routes to review). **High-confidence-wrong is
> unacceptable** — a confident error ships silently.

**Hard constraint on confidence:** all confidence values must be **real token
logprobs** (probability mass on a forced answer token), never a self-reported
"I'm 90% sure" number — verbalized confidence was empirically shown to collapse to
~5 round values while logprob confidence is continuous and discriminating.

**Tooling constraint:** GPT-5 / reasoning models **block the `logprobs` parameter**
(403), so GPT-4o is the confidence engine throughout. GPT-4o at `temperature=0` is
**not deterministic** — boundary cases jitter across runs (measured: CHULLA jittered
0.75→0.95 between identical runs). This nondeterminism shaped several design choices.

---

## 2. Project history — every phase, what worked, what failed

### Phase 0 — origins
Started as a logprob-based unit-of-measure (UoM) confidence scorer; compared
**self-reported (verbalized) confidence vs token logprobs** and found self-report
uninformative (collapses to round numbers). Refocused the project on
branded/unbranded classification with logprob confidence.

### Phase 1 — single forced-token classifier (`brand_confidence.py`)
- One GPT-4o call per title: system prompt defining BRANDED/UNBRANDED, user asks
  "Answer with a single letter: B or U", `temperature=0, max_tokens=1, logprobs=True,
  top_logprobs=5`.
- **Confidence = `exp(logprob)` of the chosen token** (OpenAI cookbook classification
  recipe — a true softmax probability over the vocabulary). A renormalized
  `P(branded)` over the {B, U} token mass kept alongside.
- Results: **98.0%** on 50 hand-labeled SKUs; **97.3%** on 110 including deliberately
  ambiguous rows.
- Statistical rigor pass (`brand_analysis.py`): confusion matrix, confidence bands,
  right-vs-wrong confidence separation, **bootstrap 95% CIs + label-permutation
  significance test** — this caught and rejected a spurious "significant"
  branded/unbranded confidence gap (p went 0.001 → 0.12 once the method was fixed).

### Phase 2 — 1,000-SKU production run
- Scored 997/1000 real catalog titles under a 30k tokens-per-minute rate limit
  (ThreadPoolExecutor + exponential backoff).
- Confidence distribution strongly bimodal: 87.6% of rows at 0.95–1.00, min 0.51.
  Defined the **grey zone at confidence ≤ 0.85** → 7.9% review queue.
- **Key data finding:** only ~55% agreement with the catalog's own `brand` column —
  driven by the *catalog* mislabeling obvious brands (HARPIC, Rooh Afza, Sakthi) as
  "Unbranded" and by brands recorded in data but absent from the title. The classifier
  surfaced source-data quality problems; there is **no clean ground truth** for this
  catalog.
- GPT-5 second-opinion experiment on the 79 grey rows: GPT-5 flipped 46% of borderline
  calls, symmetric directions, no measurable accuracy gain vs (noisy) labels, and
  cannot produce logprobs — useful as a tiebreaker only.

### Phase 3 — dual-stage & reasoning-verification (`dual_stage_confidence.py`, `reasoning_verify.py`)
- **Dual-stage:** Claude Sonnet 4.6 classifies + gives one-sentence reasoning; GPT-4o
  verifies the (title, label, reasoning) with a forced Yes/No logprob token.
  Confidence = renormalized P(Yes).
- **Reasoning-verification variant:** Sonnet gives an evidence-citing justification;
  GPT-4o judges *whether the justification is sound*. On the 136 grey rows this judged
  99% of reasoning "sound" and collapsed the review queue from 13.6% → 0.2%.
- This *looked* great but was later revealed to be **overconfident agreement** — the
  verifier rubber-stamps plausible reasoning. Which led to…

### Phase 4 — the Opus review: three failure modes (the turning point)
An independent Claude Opus review of the full 1000-row reasoning output flagged three
systematic failure classes, all rooted in **recognizability bias** ("I've heard of it
⇒ brand; I haven't ⇒ generic") plus **per-row independence** (each title judged in
isolation):

- **Type-1 — self-contradictions:** the same maker name labeled both ways across rows
  (MDH branded 8×, unbranded 1×). ~17–20 split-label entities measured by
  `consistency_audit.py` (groups titles by shared candidate maker token, zero ground
  truth needed).
- **Type-2 — unfamiliar suffix sellers:** unknown seller names in the trailing
  `product - X` slot (Ether, Murukku-the-seller) called unbranded because the model
  doesn't recognize them.
- **Type-3 — inline brands missed:** brands mid-title (…Knorr, Soda Kinley) missed
  because attention anchors on the product noun.

### Phase 5 — entity-first rearchitecture (`entity_extract.py`, `entity_first.py`)
**The core insight: change the unit of classification from the title to the maker
ENTITY.** Decide once per distinct candidate maker name, propagate to every title
containing it. Type-1 contradictions become impossible *by construction*.

Run on 1000 titles: 1,121 entities classified once each → 384 branded / 616 unbranded
titles, **0 split-label entities**, grey zone 5.6%. Against Opus's flagged lists:
**Type-1 fixed 8/8, Type-2 7/7, Type-3 10/10.**

### Phase 6 — Cross-Examined Confidence (CEC) (`cross_examine.py`, `recognition_gate.py`)
Entity-first still allowed **confident-wrong** on three paths (see §3.4). CEC adds
adversarial probes + an agreement gate + a recognition gate. A 30-case known-answer
eval (`evaluate_cec.py`): the pre-CEC output **FAILED** (3 confident errors); the
post-CEC `final_predictions.csv` **PASSES 30/30** with 0 split labels.
Cost: grey zone 5.6% → **26.6%** (145 deep-uncertain at ~0.5 + 121 near-boundary at
0.6–0.85).

### Phase 7 — arbiter (NEGATIVE RESULT) + human review loop (`arbiter.py`, `review_queue.py`, `apply_reviews.py`)
- **Arbiter hypothesis:** a chain-of-thought-then-verdict call (reason 2–4 sentences,
  then a forced `VERDICT: Yes/No` token whose logprob is read) is a stronger evidence
  class and can resolve grey-zone conflicts. **REFUTED** — on exactly the contested
  cases it was decisively wrong in both directions:
  - `murukku` → No @ p=1.0 (its snack prior overrides dispositive cross-category evidence)
  - `Kit Kat` → No @ p=1.0 (reasons itself into "product name, not a maker")
  - `kanga` (Marathi: sweet potato) → Yes @ p=1.0
  Lesson recorded: **reasoning makes the model more persuasive to itself, not more
  reliable, on ambiguity.** `arbiter.py` kept as documentation only; never used for
  promotion.
- **Review loop shipped instead:** grey zone is title-shaped (266 rows) but decisions
  are entity-shaped — reviewing `murukku` once clears all 9 titles carrying it.
  `review_queue.py` → 240 impact-ordered one-glance decisions (entity rows carry all
  probe values + why-grey reason); `apply_reviews.py` fans verdicts out at confidence
  1.0, marked `(human)`.

---

## 3. The current algorithm, in full detail

Pipeline: `entity_extract → entity_first (probe A) → cross_examine (probes B1+B2 +
agreement gate + title net) → recognition_gate → final_predictions.csv`, with
`review_queue/apply_reviews` as the human loop and `evaluate_cec` as the gate.

### 3.1 Deterministic extraction & entity resolution (`entity_extract.py`, no API)

**Candidate extraction per title** — slots in precedence order
`suffix (3) > allcaps (2) > prefix (1) > inline (0)`:

1. **Suffix seller-slot:** split title on ` - ` / ` – `; the last segment is a seller
   candidate unless it matches a code regex (`^\d…`, `^[a-z]{1,3}\d…`) or is composed
   entirely of ~180 hand-listed GENERIC words (units, packaging, foods, colors…).
2. **Prefix:** single leading Title-case token of the first segment (multi-word prefix
   runs are almost always generic descriptions, so only one token).
3. **Corpus-confirmed acronyms (`allcaps`):** an ALL-CAPS token counts as an
   acronym-brand only if it appears uppercase inside an otherwise *mixed-case* title
   somewhere in the corpus (a token seen only in fully-shouted titles is just a loud
   product word).
4. **Inline:** every non-leading Title-case word ≥3 chars not in GENERIC —
   high-recall, low precision; the per-entity model supplies precision.
5. **Shouty fallback:** for fully-UPPERCASE titles, take the single distinctive
   leading caps token (ANANDA) as prefix + each non-generic caps token inline.

**Entity resolution:** normalize (lowercase, strip non-alphanumerics), fuzzy-merge
surface variants with `SequenceMatcher ratio ≥ 0.86` (Twinning≈Twinings, SNACC≈Snacc).
Each entity accumulates: surfaces, titles, slot profile, and **categories** = crude
product head (first non-generic content word after removing that entity's own
surfaces).

**The key corpus signal — cross-category recurrence:** a token labeling structurally
UNRELATED items (a stirrer AND a spice AND a sweet) can only be the seller. But note
the design lesson: recurrence ALONE doesn't separate sellers from generics (`butter`
recurs across 10 categories too) — recurrence **plus the seller-slot** does.

### 3.2 Probe A — per-entity maker classification (`entity_first.py`)

One GPT-4o call per unique entity (`temperature=0, max_tokens=1, logprobs=True,
top_logprobs=5`). System prompt (short, since it multiplies into the 30k TPM budget):

> Decide if a TOKEN from grocery product titles names a real MAKER … or is GENERIC …
> Judge the token, not its fame; a coined/proper-noun word you don't recognize can
> still be a maker. Evidence: (1) a token in the trailing 'product - X' slot is the
> seller X; (2) if the SAME token labels structurally UNRELATED items … it is a
> seller, even if the word also names a food … (3) coined or company-like morphology
> ⇒ maker, plain food/material words ⇒ generic. Reply one word: Yes or No.

User message carries the structural evidence: surfaces, #titles, #categories, slot
profile with a human-readable note, and **diverse example titles** — one per distinct
category first (critical: `murukku` flipped wrong when its 3 samples were all spices;
the model must *see* the cross-category spread).

Score: `p_A = (p_yes + ε) / (p_yes + p_no + 2ε)` over the Yes/No token mass at the
answer position (ε = 1e-6). Label branded iff p_A > 0.5.

**Title propagation:** a title is branded iff any contained entity is branded;
confidence = deciding entity's p when branded, else `1 − max p` over its entities;
titles with no entity default unbranded (this fabricated-confidence hole is what the
title safety net later fixes).

**Ops hardening:** terminal errors (quota/auth) abort the whole run rather than
silently defaulting brands to unbranded; decisions cache to CSV; resume with
`--cache entity_decisions.csv` re-classifies only new entities.

### 3.3 Probes B1/B2 + agreement gate (`cross_examine.py`)

Why: a single framing pattern-matches ("coined-looking word ⇒ brand" at p≈0.99 on
CHULLA) even when the model *knows* the word — that one framing never elicits the
knowledge. The framings are chosen to **fail differently**:

| probe | forced question (Yes/No logprob) | catches |
|---|---|---|
| A | is X a maker? | the base decision |
| B1 | is X used *in these titles* as a generic word for the product itself? | descriptors sitting in the seller slot (`- PAPAD`) |
| B2 | does X have a fitting plain non-company meaning (food, day, river, Hindi word…) that explains **every** example title? | tokens that are *neither* product nor maker (TUES, GANGA, CHULLA) |

B1 and B2 vote FOR maker as `1 − p_B1`, `1 − p_B2`.

**Agreement gate (`combine`)** — votes combine by agreement, never averaging:
- all votes > 0.5 (maker): p = **min** of votes (weakest supporting vote)
- all votes < 0.5: p = **max** (weakest opposing vote)
- **any disagreement: p = 0.5**, conflicted flag → deep grey, forced review (label
  stays probe-A's)
- both B-probes failed transiently → uncorroborated → 0.5 forced review

A log-odds mean was explicitly rejected: one framing at logit +5 would outvote a
dissenter at −3 and keep a conflicted entity above the grey threshold.

**Title safety net:** every title where extraction found **no** entity gets one direct
logprob probe ("does this title contain a maker/brand/seller name?") so its confidence
is *measured*, not the fabricated ~1.0 of the old default (616 such titles in this
catalog; RED LABEL TEA lives here).

### 3.4 Recognition gate (`recognition_gate.py`)

The failure it closes: **unanimity cannot detect unanimous ignorance** — on a
thin-evidence token all framings can be confidently wrong *for the same reason* (the
word merely looks like a brand). Deterministic-by-design because GPT-4o probes jitter.

- Applies to entities that are **confident-branded** (p_cec > grey=0.85) with **thin
  evidence**: no suffix slot AND ≤1 category AND ≤2 titles.
- Those must ALSO pass a recognition probe: *"Have you actually heard of X as a real
  company? Do not guess from how the word looks."* (Yes/No logprob).
- p_recognized < 0.5 → confidence **capped to 0.80** (into grey; label stays branded).
  Knowledge or corpus evidence can justify confidence; **morphology alone cannot.**
- Run result: 72 capped (hungritos, milkhana, dollur…), 68 recognized survived
  (perrier, godrej, oaksmith).

### 3.5 Evaluation (`evaluate_cec.py`)

30 hand-established known-answer cases (from the Opus review + verified items), each
mapped to a *policy* requirement rather than a bare label:
- `confident_branded` — must stay branded above grey (HARPIC, Knorr, MDH, Sassy Teaspoon, …)
- `not_confident_branded` — confident-branded is a failure; grey or unbranded fine (CHULLA, PAPAD, ATTA GANGA, …)
- `not_confident_unbranded` — confident-unbranded is a failure (RED LABEL TEA, Murukku-the-seller, Kiley Soda, …)

Also checks grey-zone size and split-label count. Current deliverable
`final_predictions.csv`: **PASS 30/30, 0 split labels.** The pre-CEC output fails the
same eval with 3 confident errors.

### 3.6 Human review loop

`review_queue.py`: grey titles grouped by deciding entity; queue ordered by impact
(titles cleared per decision) then depth of uncertainty; each row carries p_maker,
p_generic_use, p_alt_meaning, p_recognized, and a `why_grey` reason (probe conflict /
recognition-capped / weak agreement / title-probe uncertain). 266 grey titles → **240
decisions**. Human fills `human_label`; `apply_reviews.py` fans out entity verdicts to
all affected titles at confidence 1.0 marked `(human)` (a branded verdict overrides
any title containing the entity; unbranded only overrides titles that entity decided).

---

## 4. Headline results (1,000-SKU catalog)

| metric | per-title baseline | entity-first + CEC |
|---|---|---|
| split-label entities (self-contradictions) | ~17–20 | **0** |
| confident-wrong on 30 known-answer cases | 3 | **0** |
| Opus-flagged errors fixed | — | Type-1 8/8 · Type-2 7/7 · Type-3 10/10 |
| review queue | 5.6% | 26.6% (266 titles → 240 decisions) |

Branded/unbranded split: 384 / 616. 1,121 entities decided. Thresholds tunable:
`--grey 0.85`, `--cap 0.80`.

---

## 5. Key design lessons (hard-won, keep these)

1. **Decide per entity, not per title** — consistency by construction beats
   consistency by prompting.
2. **Confidence = cross-examined agreement, not one probe's softmax.** Diverse
   framings that fail differently; combine by agreement (min-of-unanimous / 0.5 on
   conflict), never by averaging.
3. **Unanimity can't catch unanimous ignorance** — thin-evidence confident calls need
   an orthogonal *knowledge* check (recognition gate), applied as a deterministic cap
   because probe outputs jitter.
4. **Chain-of-thought arbitration is anti-helpful on ambiguity** (negative result §2
   Phase 7). Reasoning amplifies the prior; the logprob stops measuring uncertainty.
5. **Cross-category recurrence alone ≠ seller** (`butter` recurs too); the
   **seller-slot** is the load-bearing structural signal.
6. **Show the model diverse examples** — one per category — or it can't feel the
   cross-category force.
7. **Verbalized confidence is useless; logprobs are the signal.** GPT-5 blocks
   logprobs; GPT-4o at temp=0 is still nondeterministic.
8. **Fail loudly on terminal API errors** — silently defaulting to a class poisons
   the dataset. All stages abort + resume incrementally from caches.
9. The catalog's own labels are too noisy to train/fine-tune on without cleaning; the
   pipeline doubles as a data-quality detector.

---

## 6. Known weaknesses, open problems, and current state

1. **Grey zone is large: 26.6%** (145 deep-uncertain at ~0.5 from probe conflicts +
   121 near-boundary 0.6–0.85). This is the price of the zero-confident-error
   guarantee, and human review handles it — but shrinking it *without* breaking the
   guarantee is the main open optimization.
2. **Pending re-run (BLOCKER):** the final shouty-fix re-run (recovers ANANDA, SUMA;
   adds ~170 entities → ~1,277) died on OpenAI `insufficient_quota`. Resume after
   billing top-up: `python entity_first.py --cache entity_decisions.csv`, then re-run
   cross_examine → recognition_gate.
3. **Irreducible miss:** `RED LABEL TEA (1 KG)` — both words individually generic, the
   bigram appears nowhere else in the corpus; the title-probe puts it in grey (which
   satisfies policy) but a correct confident call would need an external **brand
   gazetteer**.
4. **Eval set is only 30 cases** and was hand-assembled from the same review that
   drove the design — risk of teaching to the test. No clean held-out gold set exists.
5. **Hand-tuned pieces:** the GENERIC stoplist (~180 words), fuzzy-merge threshold
   0.86, grey 0.85, cap 0.80, thin-evidence definition (no suffix slot ∧ ≤1 category ∧
   ≤2 titles), decisive 0.90. None are learned or validated beyond the 30-case eval.
6. **Fuzzy merge risks:** SequenceMatcher at 0.86 can merge distinct entities or fail
   to merge true variants; no systematic audit of cluster quality.
7. **Extraction recall limits:** multi-word brands not in the suffix slot, brands in
   fully-shouted titles beyond the single leading token, transliterated/vernacular
   brand names.
8. **Nondeterminism unquantified:** boundary jitter is observed (CHULLA 0.75→0.95) but
   there's no repeat-run variance measurement or seed/majority-vote mitigation on the
   probes themselves.
9. **Cost/latency:** 3 probes per entity + 1 per no-entity title + recognition probes
   ≈ ~4,000 GPT-4o calls per 1,000 titles. No batching, no cheaper-model cascade, no
   embedding prefilter.
10. **Single provider:** all probes are GPT-4o; correlated blind spots across probes
    are only partially mitigated by framing diversity. (Claude was used in the legacy
    dual-stage, not in the current pipeline; Anthropic models expose no logprobs, but
    could serve as a non-logprob disagreement signal.)
11. **Human verdicts don't feed back** into anything (no gazetteer accumulation, no
    few-shot memory, no threshold recalibration from review outcomes).

---

## 7. The ask

Given everything above, propose a **structured improvement plan** for this system.
Respect the two non-negotiables:

1. **The zero-high-confidence-error policy** (evaluate_cec must stay PASS; ideally
   strengthen the eval itself).
2. **Confidence must remain measured** (token logprobs / real probabilities or
   deterministic caps — no verbalized confidence, no reasoning-then-verdict promotion;
   that's a documented negative result).

Dimensions worth structuring the plan around (not exhaustive — add your own):

- **Shrinking the 26.6% grey zone safely** — e.g. better probe design, more voters
  with diverse framings, retrieval/web evidence, brand gazetteers (open datasets, GS1,
  FSSAI license data?), embedding-based nearest-neighbor evidence from the catalog
  itself, human-verdict feedback loops that compound.
- **Calibration & measurement** — repeat-run variance, proper scoring rules,
  conformal-prediction-style guarantees for the auto-accept set, growing the
  known-answer eval without contaminating design.
- **Extraction quality** — learned or LLM-assisted entity extraction vs the current
  regex/slot system; multi-word and vernacular brands; cluster-quality audit.
- **Cost/scale** — cascades (cheap model first, expensive probes only near the
  boundary), batching, caching across catalogs; what changes at 100k SKUs.
- **Architecture** — is per-entity + agreement gating the right skeleton, or is there
  a better formulation (e.g. joint catalog-level inference, weak supervision /
  Snorkel-style label modeling over the probes, fine-tuning once labels are clean)?
- **Robustness** — cross-provider disagreement signals, adversarial cases beyond the
  known three failure types, drift when the catalog changes.

Rank proposals by (expected grey-zone reduction) × (implementation cost) × (risk to
the zero-confident-error guarantee), and be explicit about how each would be
validated before it ships.
