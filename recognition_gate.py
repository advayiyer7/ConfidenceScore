"""recognition_gate.py — final defense against confident-wrong BRANDED calls.

The failure it closes: on a thin-evidence token (one title, no seller-slot, no
cross-category recurrence) all question framings can be unanimously confident
for the same wrong reason — the word merely LOOKS like a brand (CHULLA is a
Hindi stove, not a maker). Unanimity cannot detect unanimous ignorance.

The gate: a confident BRANDED entity with thin corpus evidence must ALSO pass a
recognition probe ("have you actually heard of this as a company?"). Knowledge
or corpus evidence can justify confidence; morphology alone cannot. Entities
that fail are kept branded but CAPPED into the grey zone => human review.

Runs as a cheap post-pass over cross_examine.py output (probes only the
qualifying entities, typically <150 calls).

Usage:
    python recognition_gate.py [--cec cec_entity_decisions.csv]
        [--workers 6] [--grey 0.85] [--cap 0.80]
"""
from __future__ import annotations

import argparse
import csv
import logging
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from cross_examine import run_pool, yes_prob
from dual_stage_confidence import call_with_retry
from entity_extract import resolve_entities

log = logging.getLogger("recognition_gate")
MODEL = "gpt-4o"

RECOG_SYSTEM = (
    "You are asked whether you have actual knowledge of a name as a real "
    "company. Answer Yes ONLY if you have genuinely encountered this name as "
    "a brand, manufacturer, or seller (any country, any size) in your "
    "training data. Answer No if you have not heard of it as a company — "
    "even if it LOOKS like a plausible brand name. Do not guess from how the "
    "word looks. Reply one word: Yes or No.")

RECOG_USER = (
    "Name: {token!r} (surface forms: {surfaces})\n"
    "Example title: {example}\n"
    "Have you actually heard of {token!r} as a real brand/company? "
    "Reply 'Yes' or 'No'.")


def probe_recognition(oclient: OpenAI, token: str, surfaces: str,
                      example: str) -> float:
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": RECOG_SYSTEM},
                  {"role": "user", "content": RECOG_USER.format(
                      token=token, surfaces=surfaces, example=example)}],
        temperature=0, max_tokens=1, logprobs=True, top_logprobs=5))
    return yes_prob(resp)


def main() -> None:
    ap = argparse.ArgumentParser(description="Recognition gate post-pass.")
    ap.add_argument("--input", default="dual_stage_scored.csv")
    ap.add_argument("--title-col", default="title")
    ap.add_argument("--cec", default="cec_entity_decisions.csv")
    ap.add_argument("--cec-predictions", default="cec_predictions.csv")
    ap.add_argument("--entities-out", default="final_entity_decisions.csv")
    ap.add_argument("--predictions-out", default="final_predictions.csv")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--grey", type=float, default=0.85)
    ap.add_argument("--cap", type=float, default=0.80,
                    help="confidence ceiling for unrecognized thin-evidence "
                         "branded entities (must be <= grey)")
    args = ap.parse_args()
    if args.cap > args.grey:
        sys.exit("--cap must be <= --grey or the gate is meaningless")

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("missing env var: OPENAI_API_KEY")

    ents_meta = list(csv.DictReader(open(args.cec, encoding="utf-8-sig")))
    by_key = {e["entity"]: e for e in ents_meta}

    # Gate applies to entities that would AUTO-ACCEPT as branded on evidence
    # that is neither corpus-corroborated nor (yet shown to be) recognized.
    def thin(e) -> bool:
        return ("suffix" not in e["slots"]
                and int(e["n_categories"]) <= 1
                and int(e["n_titles"]) <= 2)

    candidates = [e for e in ents_meta
                  if e["label"] == "branded"
                  and float(e["p_cec"]) > args.grey
                  and thin(e)]
    log.info("recognition-gating %d confident-branded thin-evidence entities "
             "of %d total", len(candidates), len(ents_meta))

    oclient = OpenAI()
    recog, aborted = run_pool(
        [e["entity"] for e in candidates],
        lambda k: probe_recognition(
            oclient, k, k, by_key[k].get("example_title", "")),
        args.workers, "recognition")
    if aborted:
        sys.exit("aborted on terminal API error; nothing written")

    capped: dict[str, float] = {}
    for e in candidates:
        k = e["entity"]
        p_rec = recog.get(k)
        if p_rec is None or p_rec < 0.5:      # unknown => cannot be confident
            capped[k] = args.cap
    log.info("capped %d/%d (unrecognized, thin evidence) to %.2f",
             len(capped), len(candidates), args.cap)

    # ---- rewrite entity table -------------------------------------------
    with open(args.entities_out, "w", newline="", encoding="utf-8") as fh:
        cols = list(ents_meta[0].keys()) + ["p_recognized", "gated"]
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for e in ents_meta:
            k = e["entity"]
            row = dict(e)
            row["p_recognized"] = round(recog[k], 4) if k in recog else ""
            row["gated"] = k in capped
            if k in capped:
                row["p_cec"] = capped[k]
            w.writerow(row)
    log.info("wrote %s", args.entities_out)

    # ---- re-propagate to titles: only capped entities change -------------
    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        titles = [r[args.title_col].strip() for r in csv.DictReader(fh)
                  if r.get(args.title_col, "").strip()]
    _, title_keys = resolve_entities(titles)
    prior = {r["title"]: r for r in csv.DictReader(
        open(args.cec_predictions, encoding="utf-8-sig"))}

    p_of = {e["entity"]: float(e["p_cec"]) for e in ents_meta}
    p_of.update(capped)
    lab_of = {e["entity"]: e["label"] for e in ents_meta}

    rows = []
    for title in titles:
        pr = prior[title]
        keys = [k for k in title_keys.get(title, []) if k in p_of]
        de = pr["deciding_entity"]
        if de and not de.startswith("("):     # entity-decided title: recompute
            branded = [(k, p_of[k]) for k in keys if lab_of[k] == "branded"]
            if branded:
                k, p = max(branded, key=lambda x: x[1])
                rows.append((title, "branded", round(p, 4), k))
            else:
                p = max((p_of[k] for k in keys), default=0.0)
                rows.append((title, "unbranded", round(1 - p, 4), ""))
        else:                                  # title-probe / no-entity rows
            rows.append((title, pr["prediction"], float(pr["confidence"]), de))

    with open(args.predictions_out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["title", "prediction", "confidence", "deciding_entity"])
        for r in sorted(rows, key=lambda x: x[2]):
            w.writerow(r)
    log.info("wrote %s", args.predictions_out)

    n_b = sum(1 for _, l, _, _ in rows if l == "branded")
    grey = sum(1 for _, _, c, _ in rows if c <= args.grey)
    log.info("=" * 60)
    log.info("titles: %d  branded: %d  unbranded: %d", len(rows), n_b,
             len(rows) - n_b)
    log.info("grey zone (conf <= %.2f): %d (%.1f%%) -> human review",
             args.grey, grey, 100 * grey / len(rows))


if __name__ == "__main__":
    main()
