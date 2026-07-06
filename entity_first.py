"""entity_first.py — entity-first branded/unbranded classification.

Fixes the three failure modes Opus identified by changing the UNIT of work from
the title to the maker ENTITY:

  1. Extract candidate maker tokens from every title (entity_extract.py).
  2. Fuzzy-resolve them into distinct entities with corpus signals (slot
     profile + cross-category recurrence).
  3. Classify each UNIQUE entity ONCE with GPT-4o logprobs, giving the model the
     structural evidence (is it in the trailing seller-slot? does it recur
     across unrelated product categories?) instead of relying on brand fame.
  4. Propagate the entity decision to every title that contains it.

Because the label is decided per entity, every title sharing a maker name gets
the SAME label -> Type-1 self-contradictions (MDH branded 8x / unbranded 1x)
are impossible by construction. The suffix-slot + cross-category evidence fixes
Type-2 (unfamiliar seller names like Ether/Murukku); high-recall inline
extraction + morphology judgment fixes Type-3 (inline brands like Knorr).

Usage:
    python entity_first.py [--input dual_stage_scored.csv] [--title-col title]
        [--limit-entities N] [--workers 6] [--grey 0.85]
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
from entity_extract import Entity, head_category, resolve_entities

log = logging.getLogger("entity_first")
MODEL = "gpt-4o"
BRAND_THRESHOLD = 0.5          # entity is "branded" when P(brand) > this
SAMPLE_TITLES = 5

# Kept deliberately short: it is sent on every per-entity call, so length here
# multiplies straight into the 30k tokens-per-minute rate budget.
ENTITY_SYSTEM = (
    "Decide if a TOKEN from grocery product titles names a real MAKER "
    "(brand/manufacturer/seller) or is GENERIC (product type, ingredient, "
    "material, size, packaging, or code). Judge the token, not its fame; a "
    "coined/proper-noun word you don't recognize can still be a maker. "
    "Evidence: (1) a token in the trailing 'product - X' slot is the seller X; "
    "(2) if the SAME token labels structurally UNRELATED items (e.g. a stirrer "
    "AND a spice AND a sweet) it is a seller, even if the word also names a "
    "food; a token that always describes the same kind of item (e.g. 'butter') "
    "is generic; (3) coined or company-like morphology => maker, plain "
    "food/material words => generic. Reply one word: Yes (maker) or No "
    "(generic).")

ENTITY_USER = (
    "Token: {token!r}  surfaces={surfaces}\n"
    "Seen in {n_titles} title(s) across {n_cats} unrelated categories; "
    "slot(s): {slots}{slot_note}\n"
    "Examples:\n{examples}\n"
    "Is {token!r} a maker/brand/seller name? Reply 'Yes' or 'No'.")


def slot_note(ent: Entity) -> str:
    notes = []
    if "suffix" in ent.slots:
        notes.append("appears in the trailing seller-slot")
    if "allcaps" in ent.slots:
        notes.append("appears as an all-caps acronym inside mixed-case titles")
    if ent.slots <= {"inline", "prefix"}:
        notes.append("only ever appears as an ordinary capitalized word")
    return ("  (" + "; ".join(notes) + ")") if notes else ""


def diverse_examples(ent: Entity, n: int = SAMPLE_TITLES) -> list[str]:
    """Pick example titles spanning DISTINCT product categories, so the model
    sees the cross-category spread (Stirrer / Asafoetida / Modak) that proves a
    food-sounding token is actually a seller. One title per category first."""
    by_cat: dict[str, str] = {}
    for t in ent.titles:
        c = head_category(t, ent.surfaces)
        by_cat.setdefault(c, t)
    picked = list(by_cat.values())[:n]
    for t in ent.titles:               # backfill if fewer categories than n
        if t not in picked and len(picked) < n:
            picked.append(t)
    return picked


def classify_entity(oclient: OpenAI, ent: Entity) -> tuple[str, float, float]:
    examples = "\n".join(f"  - {t}" for t in diverse_examples(ent))
    user = ENTITY_USER.format(
        token=ent.key, surfaces=sorted(ent.surfaces)[:5],
        n_titles=ent.n_titles, n_cats=ent.n_categories,
        slots=", ".join(sorted(ent.slots)) or "n/a",
        slot_note=slot_note(ent), examples=examples)
    resp = call_with_retry(lambda: oclient.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": ENTITY_SYSTEM},
                  {"role": "user", "content": user}],
        temperature=0, max_tokens=1, logprobs=True, top_logprobs=5))
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
    p_brand = (p_yes + EPSILON) / (p_yes + p_no + 2 * EPSILON)
    label = "branded" if p_brand > BRAND_THRESHOLD else "unbranded"
    return label, p_brand, raw


def _is_terminal(exc: Exception) -> bool:
    """Quota exhaustion / auth failures are NOT transient — retrying or
    defaulting them would silently mislabel real brands as unbranded."""
    s = str(exc).lower()
    return ("insufficient_quota" in s or "exceeded your current quota" in s
            or "invalid_api_key" in s or "authentication" in s)


def load_cache(path: str) -> dict[str, tuple[str, float]]:
    if not path or not os.path.exists(path):
        return {}
    out: dict[str, tuple[str, float]] = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            try:
                out[r["entity"]] = (r["label"], float(r["p_brand"]))
            except (KeyError, ValueError):
                continue
    return out


def classify_all(oclient: OpenAI, ents: dict[str, Entity], workers: int,
                 cache: dict[str, tuple[str, float]] | None = None
                 ) -> tuple[dict[str, tuple[str, float]], bool]:
    """Classify entities, reusing `cache` for ones already decided. Returns
    (decisions, aborted). On a terminal error (quota/auth) it stops issuing new
    work and returns aborted=True so the caller can refuse to write a partial,
    poisoned result."""
    cache = cache or {}
    decisions: dict[str, tuple[str, float]] = {
        k: cache[k] for k in ents if k in cache}
    todo = [k for k in ents if k not in cache]
    if cache:
        log.info("cache hit: %d entities reused, %d to classify",
                 len(decisions), len(todo))
    lock, done, abort = threading.Lock(), [0], threading.Event()

    def worker(key: str):
        if abort.is_set():
            return key, None
        try:
            label, p_brand, _ = classify_entity(oclient, ents[key])
        except Exception as exc:                      # noqa: BLE001
            if _is_terminal(exc):
                abort.set()
                log.error("TERMINAL error on %r: %s", key, exc)
            else:
                log.error("entity %r failed (skipped): %s", key, exc)
            return key, None
        with lock:
            done[0] += 1
            if done[0] % 50 == 0:
                log.info("classified %d/%d entities", done[0], len(todo))
        return key, (label, round(p_brand, 4))

    with concurrent.futures.ThreadPoolExecutor(workers) as pool:
        for key, res in pool.map(worker, todo):
            if res is not None:
                decisions[key] = res
    return decisions, abort.is_set()


def label_title(keys: list[str], decisions: dict[str, tuple[str, float]]
                ) -> tuple[str, float, str]:
    """A title is branded iff any of its entities is branded. Confidence is the
    deciding entity's P(brand) when branded, else 1 - max P(brand) (how sure no
    contained token is a maker). Returns (label, confidence, deciding_entity)."""
    branded = [(k, decisions[k][1]) for k in keys
               if decisions.get(k, ("unbranded", 0.0))[0] == "branded"]
    if branded:
        k, p = max(branded, key=lambda x: x[1])
        return "branded", round(p, 4), k
    if keys:
        k, p = max(((k, decisions.get(k, ("u", 0.0))[1]) for k in keys),
                   key=lambda x: x[1])
        return "unbranded", round(1 - p, 4), ""
    return "unbranded", 1.0, ""


def main() -> None:
    ap = argparse.ArgumentParser(description="Entity-first branded classifier.")
    ap.add_argument("--input", default="dual_stage_scored.csv")
    ap.add_argument("--title-col", default="title")
    ap.add_argument("--entities-out", default="entity_decisions.csv")
    ap.add_argument("--predictions-out", default="entity_first_predictions.csv")
    ap.add_argument("--limit-entities", type=int, default=0,
                    help="classify only the first N entities (smoke test)")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--grey", type=float, default=0.85)
    ap.add_argument("--cache", default="",
                    help="reuse prior entity_decisions.csv; only classify NEW "
                         "entities (cheap resume after a quota stop)")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("missing env var: OPENAI_API_KEY")

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        titles = [r[args.title_col].strip() for r in csv.DictReader(fh)
                  if r.get(args.title_col, "").strip()]
    log.info("resolving entities from %d titles", len(titles))
    ents, title_keys = resolve_entities(titles)
    log.info("%d distinct entities (%d multi-row)", len(ents),
             sum(1 for e in ents.values() if e.n_titles >= 2))

    if args.limit_entities:
        keep = set(sorted(ents, key=lambda k: -ents[k].n_titles
                          )[:args.limit_entities])
        ents = {k: v for k, v in ents.items() if k in keep}
        log.info("smoke mode: classifying %d entities", len(ents))

    oclient = OpenAI()
    cache = load_cache(args.cache)
    decisions, aborted = classify_all(oclient, ents, args.workers, cache)
    if aborted:
        log.error("RUN ABORTED on a terminal error (quota/auth). Existing "
                  "outputs were NOT overwritten. Top up billing, then resume "
                  "cheaply with: python entity_first.py --cache %s",
                  args.entities_out)
        sys.exit(2)
    missing = [k for k in ents if k not in decisions]
    if missing:
        log.warning("%d entities skipped (non-terminal errors); defaulting them "
                    "to unbranded: %s", len(missing), missing[:10])
        for k in missing:
            decisions[k] = ("unbranded", 0.0)

    with open(args.entities_out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["entity", "label", "p_brand", "n_titles", "n_categories",
                    "slots", "surfaces", "example_title"])
        for k, e in sorted(ents.items(), key=lambda kv: -decisions[kv[0]][1]):
            lab, p = decisions[k]
            w.writerow([k, lab, p, e.n_titles, e.n_categories,
                        "|".join(sorted(e.slots)), "|".join(sorted(e.surfaces)),
                        e.titles[0] if e.titles else ""])
    log.info("wrote %s", args.entities_out)

    rows = []
    for title in titles:
        keys = [k for k in title_keys.get(title, []) if k in decisions]
        label, conf, deciding = label_title(keys, decisions)
        rows.append((title, label, conf, deciding))
    with open(args.predictions_out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["title", "prediction", "confidence", "deciding_entity"])
        for r in sorted(rows, key=lambda x: x[2]):
            w.writerow(r)
    log.info("wrote %s", args.predictions_out)

    n_branded = sum(1 for _, l, _, _ in rows if l == "branded")
    grey = sum(1 for _, _, c, _ in rows if c <= args.grey)
    log.info("=" * 60)
    log.info("titles: %d  branded: %d  unbranded: %d", len(rows), n_branded,
             len(rows) - n_branded)
    log.info("grey zone (conf <= %.2f): %d (%.1f%%) -> human review",
             args.grey, grey, 100 * grey / len(rows))
    log.info("self-contradictions: 0 by construction (label decided per entity)")


if __name__ == "__main__":
    main()
