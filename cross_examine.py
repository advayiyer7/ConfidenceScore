"""cross_examine.py — Cross-Examined Confidence (CEC).

Goal: eliminate HIGH-CONFIDENCE-WRONG predictions. Low-confidence-wrong is
acceptable (it routes to human review); confident errors are not.

Why the old confidence could be confidently wrong:
  1. A single maker-probe pattern-matches ("coined word => maker") at p~0.99 on
     obscure words (CHULLA = a stove) even though the model KNOWS the word —
     the one framing never elicits that knowledge.
  2. The '- X' suffix rule presumes X is a seller (fails on '- PAPAD').
  3. Titles where extraction found NO candidate defaulted to unbranded with a
     fabricated ~1.0 confidence no model ever measured (RED LABEL TEA).

The fix — confidence = cross-examined agreement, all real token logprobs:
  Probe A (cached from entity_first): "is X a maker?"          -> p_A
  Probe B (adversarial, same evidence): "is X used in these
     titles as a generic word for the product itself?"         -> p_B
  Combine in log-odds: logit(p) = (logit(p_A) + logit(1-p_B))/2.
     Agreement stays extreme; conflict collapses toward 0.5 => grey zone.
  Title safety net: every NO-entity title gets one direct logprob probe
     ("does this title name a maker?") so its confidence is measured, not
     assumed.

Usage:
    python cross_examine.py [--input dual_stage_scored.csv]
        [--decisions entity_decisions.csv] [--workers 6] [--grey 0.85]
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import logging
import math
import os
import sys
import threading

from dotenv import load_dotenv
from openai import OpenAI

from dual_stage_confidence import EPSILON, call_with_retry
from entity_first import (
    _is_terminal, diverse_examples, load_cache, slot_note,
)
from entity_extract import Entity, resolve_entities

log = logging.getLogger("cross_examine")
MODEL = "gpt-4o"

# ---------------------------------------------------------------- probe B ---
GENERIC_SYSTEM = (
    "You check how a TOKEN is used inside grocery product titles. Decide "
    "whether, IN THESE TITLES, the token is used as a GENERIC word for the "
    "product itself or its properties (a type of item, food, dish, material, "
    "cooking term, or descriptor in English or any Indian language) rather "
    "than as the name of the maker/brand/seller. If the token is the thing "
    "being sold or describes it, answer Yes. If it identifies who makes or "
    "sells the items — especially when the items themselves are named by OTHER "
    "words — answer No. Reply one word: Yes (generic product word here) or No "
    "(maker/seller name here).")

GENERIC_USER = (
    "Token: {token!r}  surfaces={surfaces}\n"
    "Seen in {n_titles} title(s) across {n_cats} unrelated categories; "
    "slot(s): {slots}{slot_note}\n"
    "Titles:\n{examples}\n"
    "In these titles, is {token!r} a generic product word (not a maker's "
    "name)? Reply 'Yes' or 'No'.")

# Probe B2 — alternative-meaning framing. Catches tokens that are NEITHER the
# product NOR a maker (a day abbreviation, a river, a Hindi household word):
# the binary maker/product-word framings rubber-stamp those with false
# confidence because their true reading isn't an offered option.
MEANING_SYSTEM = (
    "You check whether a TOKEN from grocery product titles has a plain "
    "NON-COMPANY meaning that explains its presence. Consider meanings in "
    "English and Indian languages: a food, dish, household object, cooking "
    "term, material, color, day, month, place, river, person's name used "
    "descriptively, or any common word. Answer Yes ONLY if such a meaning "
    "fits how the token is actually used in EVERY example title shown. If the "
    "only reading that explains all the titles is a maker/brand/seller name, "
    "answer No. Reply one word: Yes (a fitting non-company meaning exists) or "
    "No (only a maker name fits).")

MEANING_USER = (
    "Token: {token!r}  surfaces={surfaces}\n"
    "Titles:\n{examples}\n"
    "Does {token!r} have a plain non-company meaning that fits its use in "
    "ALL these titles? Reply 'Yes' or 'No'.")

# ------------------------------------------------------- title safety net ---
TITLE_SYSTEM = (
    "You read one grocery/catalog product title and decide whether it names a "
    "real MAKER — a manufacturer, brand, or seller company (well-known or "
    "obscure, in any language or casing). Product types, ingredients, "
    "materials, sizes, colors, measurements, and internal codes are not "
    "makers. Reply one word: Yes (a maker is named) or No (purely generic).")

TITLE_USER = (
    "Product title: {title!r}\n"
    "Does this title contain a maker/brand/seller name? Reply 'Yes' or 'No'.")


def yes_prob(resp) -> float:
    """Renormalized P(Yes) over the {Yes, No} mass at the answer position."""
    content = resp.choices[0].logprobs.content
    if not content:
        raise ValueError("no logprobs at answer position")
    chosen = content[0]
    raw = math.exp(chosen.logprob)
    p_yes = p_no = 0.0
    for e in chosen.top_logprobs:
        tok = e.token.strip().lower()
        if tok.startswith("y"):
            p_yes += math.exp(e.logprob)
        elif tok.startswith("n"):
            p_no += math.exp(e.logprob)
    if p_yes == 0.0 and chosen.token.strip().lower().startswith("y"):
        p_yes = raw
    if p_no == 0.0 and chosen.token.strip().lower().startswith("n"):
        p_no = raw
    return (p_yes + EPSILON) / (p_yes + p_no + 2 * EPSILON)


def logit(p: float) -> float:
    p = min(1.0 - EPSILON, max(EPSILON, p))
    return math.log(p / (1.0 - p))


def combine(votes: list[float]) -> tuple[float, bool]:
    """Agreement-gated aggregation of independent votes for 'maker'.

    Confident output requires UNANIMOUS cross-examination:
      - all votes > 0.5 (maker):     p = weakest supporting vote (min)
      - all votes < 0.5 (not maker): p = weakest opposing vote (max)
      - any disagreement:            p = 0.5 -> deep grey, forced review
    A log-odds mean is NOT used: one framing at logit +5 would outvote another
    at -3 and keep a conflicted entity above the grey threshold.
    Returns (p_maker, conflicted)."""
    if all(v > 0.5 for v in votes):
        return min(votes), False
    if all(v < 0.5 for v in votes):
        return max(votes), False
    return 0.5, True


def probe_generic(oclient: OpenAI, ent: Entity) -> float:
    examples = "\n".join(f"  - {t}" for t in diverse_examples(ent))
    user = GENERIC_USER.format(
        token=ent.key, surfaces=sorted(ent.surfaces)[:5],
        n_titles=ent.n_titles, n_cats=ent.n_categories,
        slots=", ".join(sorted(ent.slots)) or "n/a",
        slot_note=slot_note(ent), examples=examples)
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": GENERIC_SYSTEM},
                  {"role": "user", "content": user}],
        temperature=0, max_tokens=1, logprobs=True, top_logprobs=5))
    return yes_prob(resp)


def probe_meaning(oclient: OpenAI, ent: Entity) -> float:
    examples = "\n".join(f"  - {t}" for t in diverse_examples(ent))
    user = MEANING_USER.format(
        token=ent.key, surfaces=sorted(ent.surfaces)[:5], examples=examples)
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": MEANING_SYSTEM},
                  {"role": "user", "content": user}],
        temperature=0, max_tokens=1, logprobs=True, top_logprobs=5))
    return yes_prob(resp)


def probe_title(oclient: OpenAI, title: str) -> float:
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": TITLE_SYSTEM},
                  {"role": "user", "content": TITLE_USER.format(title=title)}],
        temperature=0, max_tokens=1, logprobs=True, top_logprobs=5))
    return yes_prob(resp)


def run_pool(items, fn, workers: int, what: str):
    """Map fn over items concurrently; abort hard on terminal errors so a
    quota outage can never silently poison results."""
    results: dict = {}
    lock, done, abort = threading.Lock(), [0], threading.Event()

    def worker(item):
        if abort.is_set():
            return item, None
        try:
            res = fn(item)
        except Exception as exc:                      # noqa: BLE001
            if _is_terminal(exc):
                abort.set()
                log.error("TERMINAL error on %r: %s", item, exc)
            else:
                log.error("%s %r failed (skipped): %s", what, item, exc)
            return item, None
        with lock:
            done[0] += 1
            if done[0] % 100 == 0:
                log.info("%s: %d/%d", what, done[0], len(items))
        return item, res

    with concurrent.futures.ThreadPoolExecutor(workers) as pool:
        for item, res in pool.map(worker, list(items)):
            if res is not None:
                results[item] = res
    return results, abort.is_set()


def main() -> None:
    ap = argparse.ArgumentParser(description="Cross-Examined Confidence.")
    ap.add_argument("--input", default="dual_stage_scored.csv")
    ap.add_argument("--title-col", default="title")
    ap.add_argument("--decisions", default="entity_decisions.csv",
                    help="cached probe-A results from entity_first.py")
    ap.add_argument("--entities-out", default="cec_entity_decisions.csv")
    ap.add_argument("--predictions-out", default="cec_predictions.csv")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--grey", type=float, default=0.85)
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("missing env var: OPENAI_API_KEY")

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        titles = [r[args.title_col].strip() for r in csv.DictReader(fh)
                  if r.get(args.title_col, "").strip()]
    ents, title_keys = resolve_entities(titles)
    probe_a = load_cache(args.decisions)
    missing_a = [k for k in ents if k not in probe_a]
    if missing_a:
        sys.exit(f"{len(missing_a)} entities missing from {args.decisions} "
                 f"(e.g. {missing_a[:5]}); rerun entity_first.py first")
    log.info("%d entities (probe A cached), %d titles", len(ents), len(titles))

    oclient = OpenAI()

    # ---- Probes B1 + B2: two adversarial framings, every entity ------------
    probe_b1, aborted = run_pool(
        list(ents), lambda k: probe_generic(oclient, ents[k]),
        args.workers, "probe-B1")
    if aborted:
        sys.exit("aborted on terminal API error; nothing written")
    probe_b2, aborted = run_pool(
        list(ents), lambda k: probe_meaning(oclient, ents[k]),
        args.workers, "probe-B2")
    if aborted:
        sys.exit("aborted on terminal API error; nothing written")

    # entity -> (label, p_cec, conflicted, p_a, p_b1, p_b2)
    cec: dict[str, tuple[str, float, bool, float, float, float]] = {}
    for k in ents:
        p_a = probe_a[k][1]
        votes = [p_a]
        b1, b2 = probe_b1.get(k), probe_b2.get(k)
        if b1 is not None:
            votes.append(1.0 - b1)           # B1's vote FOR maker
        if b2 is not None:
            votes.append(1.0 - b2)           # B2's vote FOR maker
        if len(votes) == 1:                  # both probes failed transiently:
            p, conflicted = 0.5, True        # uncorroborated => forced review
        else:
            p, conflicted = combine(votes)
        label = ("branded" if p > 0.5 else "unbranded") if not conflicted \
            else probe_a[k][0]               # conflict keeps probe-A label
        cec[k] = (label, p, conflicted,
                  p_a,
                  float("nan") if b1 is None else b1,
                  float("nan") if b2 is None else b2)

    # ---- Title safety net: measure the no-entity titles --------------------
    no_ent = [t for t in titles if not title_keys.get(t)]
    log.info("title safety net: probing %d no-entity titles", len(no_ent))
    p_title, aborted = run_pool(
        no_ent, lambda t: probe_title(oclient, t), args.workers, "title-probe")
    if aborted:
        sys.exit("aborted on terminal API error; nothing written")

    with open(args.entities_out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["entity", "label", "p_cec", "conflict", "p_maker",
                    "p_generic_use", "p_alt_meaning", "n_titles",
                    "n_categories", "slots", "example_title"])
        for k, (lab, p, conf_, p_a, b1, b2) in sorted(
                cec.items(), key=lambda kv: -kv[1][1]):
            e = ents[k]
            w.writerow([k, lab, round(p, 4), conf_, round(p_a, 4),
                        "" if math.isnan(b1) else round(b1, 4),
                        "" if math.isnan(b2) else round(b2, 4),
                        e.n_titles, e.n_categories,
                        "|".join(sorted(e.slots)),
                        e.titles[0] if e.titles else ""])
    log.info("wrote %s", args.entities_out)

    rows = []
    for title in titles:
        keys = title_keys.get(title, [])
        branded = [(k, cec[k][1]) for k in keys if cec[k][0] == "branded"]
        if branded:
            k, p = max(branded, key=lambda x: x[1])
            rows.append((title, "branded", round(p, 4), k))
        elif keys:
            p = max(cec[k][1] for k in keys)
            rows.append((title, "unbranded", round(1 - p, 4), ""))
        else:
            pt = p_title.get(title)
            if pt is None:                   # probe failed: force review
                rows.append((title, "unbranded", 0.5, "(unprobed)"))
            elif pt > 0.5:
                rows.append((title, "branded", round(pt, 4), "(title-probe)"))
            else:
                rows.append((title, "unbranded", round(1 - pt, 4),
                             "(title-probe)"))

    with open(args.predictions_out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["title", "prediction", "confidence", "deciding_entity"])
        for r in sorted(rows, key=lambda x: x[2]):
            w.writerow(r)
    log.info("wrote %s", args.predictions_out)

    n_b = sum(1 for _, l, _, _ in rows if l == "branded")
    grey = sum(1 for _, _, c, _ in rows if c <= args.grey)
    n_conf = sum(1 for v in cec.values() if v[2])
    log.info("=" * 60)
    log.info("titles: %d  branded: %d  unbranded: %d", len(rows), n_b,
             len(rows) - n_b)
    log.info("cross-examination conflicts: %d entities -> forced review",
             n_conf)
    log.info("grey zone (conf <= %.2f): %d (%.1f%%) -> human review",
             args.grey, grey, 100 * grey / len(rows))


if __name__ == "__main__":
    main()
