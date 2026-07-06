"""arbiter.py — reasoning arbiter. ******* NEGATIVE RESULT — DO NOT USE *******

Hypothesis: a reasoning-then-verdict call (chain of thought, then a forced
'VERDICT: Yes/No' token whose logprob is read) is a stronger evidence class
than single-token probes and can safely resolve grey-zone conflicts.

REFUTED by the smoke test (2026-07-05). On exactly the contested cases the
arbiter was decisively wrong in BOTH directions:
  - murukku -> 'No' @ p=1.0: given room to reason, the model's prior
    ('murukku is a snack') OVERRIDES the dispositive cross-category evidence
    (it labels a stirrer). Promotion = confidently-wrong unbranded.
  - Kit Kat -> 'No' @ p=1.0: reasons itself into 'a product name, not a
    maker' under the strict maker framing.
  - kanga (Marathi: sweet potato) -> 'Yes' @ p=1.0: confidently-wrong branded.

Lesson recorded for the project: reasoning makes the model more persuasive to
itself, not more reliable, on ambiguity. The residual grey zone is genuinely
hard; HUMAN REVIEW is its correct disposition (see review_queue.py /
apply_reviews.py). Kept for the negative-result documentation only.

Safety rules so the zero-confident-error guarantee survives:
  1. Recognition-CAPPED entities are untouchable — thin-evidence unrecognized
     names (CHULLA) can never be promoted past grey by anything.
  2. An entity may only be promoted past grey when it has strong corpus
     evidence: suffix seller-slot OR >=2 cross-categories.
  3. A grey TITLE may only be promoted to confident-branded when the arbiter
     both reasons to a decisive verdict AND names the brand, and that name
     independently passes the recognition probe.
  4. Promotions are ceilinged at 0.98; indecisive verdicts leave rows grey.

Usage:
    python arbiter.py [--grey 0.85] [--decisive 0.90] [--workers 6]
Reads  final_entity_decisions.csv + final_predictions.csv
Writes resolved_entity_decisions.csv + resolved_predictions.csv
"""
from __future__ import annotations

import argparse
import csv
import logging
import math
import os
import re
import sys

from dotenv import load_dotenv
from openai import OpenAI

from cross_examine import run_pool
from dual_stage_confidence import EPSILON, call_with_retry
from entity_extract import resolve_entities
from entity_first import diverse_examples
from recognition_gate import probe_recognition

log = logging.getLogger("arbiter")
MODEL = "gpt-4o"
PROMOTE_CEIL = 0.98

ENTITY_ARB_SYSTEM = (
    "You resolve whether a TOKEN from grocery product titles is the name of a "
    "real MAKER (brand/manufacturer/seller) or a GENERIC term (product type, "
    "ingredient, material, size, packaging word, code, day, place, or other "
    "common word in English or any Indian language). Reason it out first: "
    "what could the token mean, and does that meaning explain its use in "
    "EVERY title shown? A token that labels structurally unrelated items can "
    "only be the seller. Write 2-4 sentences of reasoning, then a final line "
    "of exactly: VERDICT: Yes   (it is a maker)  or  VERDICT: No")

ENTITY_ARB_USER = (
    "Token: {token!r}\n"
    "Titles containing it:\n{examples}\n"
    "Is {token!r} a maker/brand/seller name?")

TITLE_ARB_SYSTEM = (
    "You decide whether one grocery/catalog product title names a real MAKER "
    "(a brand, manufacturer, or seller company — well-known or obscure, any "
    "language, any casing). Product types, ingredients, materials, sizes, "
    "colors, codes and measurements are not makers. Reason in 2-3 sentences, "
    "then output exactly two final lines:\n"
    "BRAND: <the maker name, or none>\n"
    "VERDICT: Yes   (a maker is named)  or  VERDICT: No")

TITLE_ARB_USER = "Product title: {title!r}\nDoes it name a maker?"


def verdict_prob(resp) -> tuple[float, str]:
    """Locate the token after the final 'VERDICT:' and renormalize P(Yes)
    over the {Yes, No} mass at that position. Returns (p_yes, full_text)."""
    content = resp.choices[0].logprobs.content
    text = resp.choices[0].message.content or ""
    if not content:
        raise ValueError("no logprobs in arbiter response")
    idx = None
    for i in range(len(content) - 1, -1, -1):
        tok = content[i].token.strip().lower()
        if tok in ("yes", "no") or tok.rstrip(".!").lower() in ("yes", "no"):
            idx = i
            break
    if idx is None:
        raise ValueError(f"no verdict token found in: {text[-80:]!r}")
    chosen = content[idx]
    raw = math.exp(chosen.logprob)
    p_yes = p_no = 0.0
    for e in chosen.top_logprobs:
        t = e.token.strip().rstrip(".!").lower()
        if t == "yes":
            p_yes += math.exp(e.logprob)
        elif t == "no":
            p_no += math.exp(e.logprob)
    if p_yes == 0.0 and chosen.token.strip().lower().startswith("y"):
        p_yes = raw
    if p_no == 0.0 and chosen.token.strip().lower().startswith("n"):
        p_no = raw
    return (p_yes + EPSILON) / (p_yes + p_no + 2 * EPSILON), text


def arb_entity(oclient: OpenAI, ent) -> tuple[float, str]:
    examples = "\n".join(f"  - {t}" for t in diverse_examples(ent, 6))
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": ENTITY_ARB_SYSTEM},
                  {"role": "user", "content": ENTITY_ARB_USER.format(
                      token=ent.key, examples=examples)}],
        temperature=0, max_tokens=220, logprobs=True, top_logprobs=5))
    return verdict_prob(resp)


def arb_title(oclient: OpenAI, title: str) -> tuple[float, str, str]:
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": TITLE_ARB_SYSTEM},
                  {"role": "user", "content": TITLE_ARB_USER.format(
                      title=title)}],
        temperature=0, max_tokens=220, logprobs=True, top_logprobs=5))
    p_yes, text = verdict_prob(resp)
    m = re.search(r"BRAND:\s*(.+)", text)
    brand = (m.group(1).strip().strip("'\"") if m else "")
    if brand.lower() in ("none", "n/a", ""):
        brand = ""
    return p_yes, brand, text


def main() -> None:
    ap = argparse.ArgumentParser(description="Reasoning arbiter pass.")
    ap.add_argument("--input", default="dual_stage_scored.csv")
    ap.add_argument("--title-col", default="title")
    ap.add_argument("--entities-in", default="final_entity_decisions.csv")
    ap.add_argument("--predictions-in", default="final_predictions.csv")
    ap.add_argument("--entities-out", default="resolved_entity_decisions.csv")
    ap.add_argument("--predictions-out", default="resolved_predictions.csv")
    ap.add_argument("--grey", type=float, default=0.85)
    ap.add_argument("--decisive", type=float, default=0.90,
                    help="arbiter verdict prob needed to resolve a row")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("missing env var: OPENAI_API_KEY")

    ents_meta = list(csv.DictReader(open(args.entities_in,
                                         encoding="utf-8-sig")))
    by_key = {e["entity"]: e for e in ents_meta}
    preds = list(csv.DictReader(open(args.predictions_in,
                                     encoding="utf-8-sig")))

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        titles = [r[args.title_col].strip() for r in csv.DictReader(fh)
                  if r.get(args.title_col, "").strip()]
    ents, title_keys = resolve_entities(titles)

    def strong(e) -> bool:
        return "suffix" in e["slots"] or int(e["n_categories"]) >= 2

    # ---- eligible grey ENTITIES: not recognition-capped, strong evidence ---
    ent_todo = [e["entity"] for e in ents_meta
                if float(e["p_cec"]) <= args.grey
                and 0.15 < float(e["p_cec"])           # deep-unbranded stays
                and e.get("gated") != "True"           # rule 1: cap is final
                and strong(e)                          # rule 2
                and e["entity"] in ents]
    log.info("entity arbiter: %d eligible grey entities", len(ent_todo))
    oclient = OpenAI()
    ent_res, aborted = run_pool(
        ent_todo, lambda k: arb_entity(oclient, ents[k]),
        args.workers, "entity-arb")
    if aborted:
        sys.exit("aborted on terminal API error; nothing written")

    p_of = {e["entity"]: float(e["p_cec"]) for e in ents_meta}
    lab_of = {e["entity"]: e["label"] for e in ents_meta}
    resolved_ents = 0
    for k, (p_yes, _text) in ent_res.items():
        if p_yes >= args.decisive:
            p_of[k], lab_of[k] = min(p_yes, PROMOTE_CEIL), "branded"
            resolved_ents += 1
        elif (1 - p_yes) >= args.decisive:
            p_of[k], lab_of[k] = 1 - min(1 - p_yes, PROMOTE_CEIL), "unbranded"
            resolved_ents += 1
    log.info("entity arbiter resolved %d/%d", resolved_ents, len(ent_todo))

    with open(args.entities_out, "w", newline="", encoding="utf-8") as fh:
        cols = list(ents_meta[0].keys()) + ["p_arbiter", "arbitrated"]
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for e in ents_meta:
            k = e["entity"]
            row = dict(e)
            row["p_arbiter"] = round(ent_res[k][0], 4) if k in ent_res else ""
            row["arbitrated"] = k in ent_res and p_of[k] != float(e["p_cec"])
            row["p_cec"], row["label"] = round(p_of[k], 4), lab_of[k]
            w.writerow(row)
    log.info("wrote %s", args.entities_out)

    # ---- re-propagate entity-decided titles --------------------------------
    prior = {r["title"]: r for r in preds}
    rows = []
    title_probe_grey = []
    for title in titles:
        pr = prior[title]
        de, conf = pr["deciding_entity"], float(pr["confidence"])
        if de.startswith("("):                       # title-probe rows
            if conf <= args.grey:
                title_probe_grey.append(title)
            rows.append([title, pr["prediction"], conf, de])
            continue
        keys = [k for k in title_keys.get(title, []) if k in p_of]
        branded = [(k, p_of[k]) for k in keys if lab_of[k] == "branded"]
        if branded:
            k, p = max(branded, key=lambda x: x[1])
            rows.append([title, "branded", round(p, 4), k])
        elif keys:
            p = max(p_of[k] for k in keys)
            rows.append([title, "unbranded", round(1 - p, 4), ""])
        else:
            rows.append([title, pr["prediction"], conf, de])

    # ---- title arbiter for grey title-probe rows (rule 3) ------------------
    log.info("title arbiter: %d grey title-probe rows", len(title_probe_grey))
    t_res, aborted = run_pool(
        title_probe_grey, lambda t: arb_title(oclient, t),
        args.workers, "title-arb")
    if aborted:
        sys.exit("aborted on terminal API error; nothing written")

    need_recog = [t for t, (p, b, _) in t_res.items()
                  if p >= args.decisive and b]
    recog, aborted = run_pool(
        need_recog,
        lambda t: probe_recognition(oclient, t_res[t][1], t_res[t][1], t),
        args.workers, "title-arb-recognition")
    if aborted:
        sys.exit("aborted on terminal API error; nothing written")

    by_title_idx = {r[0]: i for i, r in enumerate(rows)}
    resolved_titles = 0
    for t, (p_yes, brand, _text) in t_res.items():
        i = by_title_idx[t]
        if p_yes >= args.decisive and brand and recog.get(t, 0.0) >= 0.5:
            rows[i] = [t, "branded", round(min(p_yes, PROMOTE_CEIL), 4),
                       f"(arbiter:{brand[:24]})"]
            resolved_titles += 1
        elif (1 - p_yes) >= args.decisive:
            rows[i] = [t, "unbranded",
                       round(1 - min(1 - p_yes, PROMOTE_CEIL), 4),
                       "(arbiter)"]
            resolved_titles += 1
    log.info("title arbiter resolved %d/%d", resolved_titles,
             len(title_probe_grey))

    with open(args.predictions_out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["title", "prediction", "confidence", "deciding_entity"])
        for r in sorted(rows, key=lambda x: x[2]):
            w.writerow(r)
    log.info("wrote %s", args.predictions_out)

    n_b = sum(1 for r in rows if r[1] == "branded")
    grey = sum(1 for r in rows if float(r[2]) <= args.grey)
    log.info("=" * 60)
    log.info("titles: %d  branded: %d  unbranded: %d",
             len(rows), n_b, len(rows) - n_b)
    log.info("grey zone (conf <= %.2f): %d (%.1f%%)  [was %d]",
             args.grey, grey, 100 * grey / len(rows),
             sum(1 for r in preds if float(r["confidence"]) <= args.grey))


if __name__ == "__main__":
    main()
