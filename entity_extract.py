"""entity_extract.py — deterministic candidate-maker extraction, fuzzy entity
resolution, and corpus signals. NO API calls; fully unit-testable.

This is the front half of the entity-first redesign. It answers, for a catalog
of product titles:
  - which candidate maker/seller tokens does each title contain, and in which
    structural slot (suffix seller-slot, prefix/inline, corpus-confirmed
    acronym)?
  - after fuzzy-merging surface variants (Twinning≈Twinings, SNACC≈Snacc),
    what are the distinct ENTITIES, and what corpus evidence do we have that
    each is a real maker vs. a generic descriptor?

The key corpus signal is cross-category recurrence: a token that appears across
many UNRELATED product categories (Murukku on a stirrer AND asafoetida AND
modak) cannot be a product word — it is a seller. That signal, not model
familiarity, is what fixes the recognizability bias.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher

# Generic descriptor / unit / packaging words that are NOT makers even in a
# brand-like slot or when capitalized.
GENERIC = {
    "ml", "ltr", "l", "kg", "gm", "gms", "g", "gsm", "kgs", "mm", "cm", "oz",
    "pc", "pcs", "pkt", "pack", "box", "bag", "jar", "can", "tin", "tub",
    "cup", "lid", "tray", "pouch", "sticker", "stickers", "cover", "outer",
    "frozen", "fresh", "premium", "plain", "round", "big", "small", "large",
    "veg", "nonveg", "non", "hamper", "container", "bottle", "paper", "plastic",
    "roll", "sheet", "card", "powder", "sauce", "oil", "milk", "water", "tea",
    "coffee", "rice", "flour", "atta", "sugar", "salt", "chilli", "chili",
    "masala", "cake", "chocolate", "choc", "ice", "cream", "icecream", "bar",
    "cookie", "cookies", "dough", "premix", "mix", "paste", "syrup", "juice",
    "crush", "seeds", "seed", "whole", "dal", "dry", "green", "red", "white",
    "black", "blue", "yellow", "sf", "nas", "gst", "the", "of", "with", "and",
    "for", "incremental", "chicken", "mutton", "fish", "paneer", "cheese",
    "bread", "bun", "buns", "fries", "fruit", "fruits", "vanilla", "mango",
    "coconut", "curry", "baked", "sweet", "sweets", "staff", "soda", "pizza",
    "cocoa", "hazelnut", "strawberry", "blueberry", "truffle", "cassata",
    "paprika", "liquid", "classic", "mixed", "pink", "cone", "softy", "corn",
    "cutlery", "nihari", "bagasse", "sriracha", "french", "chana", "maida",
    "spoon", "mat", "mop", "rose", "pan", "frypan", "desert", "cap", "plate",
    "rosemary", "gluten", "torch", "glass", "booklet", "ribban", "channi",
}

# A suffix segment that is a code/measurement, never a seller name.
CODE_RE = re.compile(r"^[a-z]?[-_\s]*\d{2,}|^[a-z]{1,3}\d|^\d", re.I)
# Slot precedence (higher = stronger structural evidence of a maker).
# 'inline' = any non-leading Title-case word (catches mid/end brands like
# "...Knorr", "Soda Kinley"); noisiest, so the per-entity model filters it.
SLOT_RANK = {"inline": 0, "prefix": 1, "allcaps": 2, "suffix": 3}


def clean(s: str) -> str:
    return re.sub(r"[^\w\s&']", " ", s).strip()


def norm(tok: str) -> str:
    return re.sub(r"[^a-z0-9]", "", tok.lower())


def _all_generic(phrase: str) -> bool:
    toks = [w for w in phrase.lower().split() if w]
    return bool(toks) and all(w in GENERIC or w.isdigit() for w in toks)


def split_segments(title: str) -> list[str]:
    t = re.sub(r"^#_#\s*", "", title.strip())
    return [p.strip() for p in re.split(r"\s[-–]\s", t) if p.strip()]


def build_acronyms(titles: list[str]) -> set[str]:
    """An all-caps token counts as an acronym-brand only if it appears uppercase
    inside an otherwise MIXED-CASE title. A token seen only in fully-shouted
    titles (CHICKEN LEG RAW) is just a loud product word, not a brand."""
    acro: set[str] = set()
    for t in titles:
        body = re.sub(r"^#_#\s*", "", t.strip())
        if not any(c.islower() for c in body):
            continue
        for m in re.findall(r"\b[A-Z][A-Z0-9]{1,}\b", body):
            if m.lower() not in GENERIC and not m.isdigit():
                acro.add(m)
    return acro


def extract_candidates(title: str, acronyms: set[str]) -> dict[str, str]:
    """Return {candidate_surface: slot} for one title.

    slot in {'suffix','allcaps','prefix'}. 'suffix' and 'allcaps' are
    high-precision maker slots; 'prefix' is the noisy leading-word slot.
    """
    t = re.sub(r"^#_#\s*", "", title.strip())
    out: dict[str, str] = {}

    def put(s: str, slot: str) -> None:
        s = clean(s).strip()
        if len(norm(s)) < 3:
            return
        if s not in out or SLOT_RANK[slot] > SLOT_RANK[out[s]]:
            out[s] = slot

    parts = split_segments(t)
    if len(parts) >= 2:
        suf = parts[-1]
        if not CODE_RE.match(suf) and not _all_generic(clean(suf)):
            put(suf, "suffix")
        # SINGLE leading token only — multi-word prefix runs are almost always
        # generic descriptions (PAPER COVER BROWN), not makers. Multi-word
        # sellers live in the suffix slot (Sassy Teaspoon, Cookie Cartel).
        m = re.match(r"([A-Z][A-Za-z&']+)", parts[0])
        if m and not _all_generic(clean(m.group(1))):
            put(m.group(1), "prefix")
    for m in re.findall(r"\b[A-Z][A-Z0-9]{1,}\b", t):
        if m in acronyms:
            put(m, "allcaps")
    # every Title-case word is a low-priority inline candidate (recall); the
    # leading one is upgraded to 'prefix'.
    for m in re.finditer(r"\b[A-Z][a-z]{2,}\b", t):
        if m.group().lower() not in GENERIC:
            put(m.group(), "prefix" if m.start() == 0 else "inline")
    # Shouty fallback: a fully-UPPERCASE title (RED LABEL TEA, ANANDA PANEER)
    # under-fires the mixed-case rules, so a brand written in caps gets missed.
    # Take the leading run of caps words up to the first generic product word as
    # a brand-phrase candidate, plus each non-generic caps token inline; the
    # per-entity model supplies precision.
    if not any(c.islower() for c in parts[0] if c.isalpha()):
        lead = re.findall(r"[A-Z][A-Z']+", parts[0])
        # only a SINGLE distinctive leading caps token (ANANDA) — never a
        # concatenated run (DESERT SPOON GTIDY).
        if lead and lead[0].lower() not in GENERIC:
            put(lead[0].title(), "prefix")
        for w in re.findall(r"\b[A-Z][A-Z']{2,}\b", t):
            if w.lower() not in GENERIC and not CODE_RE.match(w):
                put(w.title(), "inline")
    return out


def head_category(title: str, brand_surfaces: set[str]) -> str:
    """Crude product category = first content word of the title after removing
    the brand spans and the #_# marker. Used to measure cross-category spread."""
    t = re.sub(r"^#_#\s*", "", title.strip())
    for b in brand_surfaces:
        t = re.sub(re.escape(b), " ", t, flags=re.I)
    for w in re.findall(r"[A-Za-z]{3,}", t):
        lw = w.lower()
        if lw not in GENERIC:
            return lw
    return "?"


@dataclass
class Entity:
    key: str
    surfaces: set[str] = field(default_factory=set)
    titles: list[str] = field(default_factory=list)
    slots: set[str] = field(default_factory=set)
    categories: set[str] = field(default_factory=set)

    @property
    def n_titles(self) -> int:
        return len(self.titles)

    @property
    def n_categories(self) -> int:
        return len({c for c in self.categories if c != "?"})

    @property
    def strong_slot(self) -> bool:
        return bool(self.slots & {"suffix", "allcaps"})


def fuzzy_key(n: str, keys, thresh: float = 0.86):
    for k in keys:
        if SequenceMatcher(None, n, k).ratio() >= thresh:
            return k
    return None


def resolve_entities(titles: list[str]) -> tuple[dict[str, Entity], dict[str, list[str]]]:
    """Cluster surface tokens into entities and attach corpus signals.

    Returns (entities_by_key, title_to_entity_keys).
    """
    acronyms = build_acronyms(titles)
    ents: dict[str, Entity] = {}
    canon: dict[str, str] = {}                 # normalized surface -> entity key
    title_cands: list[tuple[str, dict[str, str]]] = []

    for title in titles:
        cands = extract_candidates(title, acronyms)
        title_cands.append((title, cands))
        for surf in cands:
            n = norm(surf)
            if not n:
                continue
            key = canon.get(n) or fuzzy_key(n, list(canon.values())) or n
            canon[n] = key
            ents.setdefault(key, Entity(key=key))

    title_keys: dict[str, list[str]] = {}
    for title, cands in title_cands:
        key_surfaces: dict[str, set[str]] = defaultdict(set)
        for surf, slot in cands.items():
            key = canon[norm(surf)]
            e = ents[key]
            e.surfaces.add(surf)
            e.slots.add(slot)
            if title not in e.titles:
                e.titles.append(title)
            key_surfaces[key].add(surf)
        for key, surfs in key_surfaces.items():
            # category = product head with ONLY this entity's own surface removed
            ents[key].categories.add(head_category(title, surfs))
        title_keys[title] = list(key_surfaces.keys())
    return ents, title_keys


if __name__ == "__main__":
    import csv
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "dual_stage_scored.csv"
    titles = [r["title"] for r in csv.DictReader(
        open(path, encoding="utf-8-sig")) if r.get("title", "").strip()]
    ents, tk = resolve_entities(titles)
    multi = sorted((e for e in ents.values() if e.n_titles >= 2),
                   key=lambda e: (-e.n_categories, -e.n_titles))
    print(f"titles: {len(titles)}   entities: {len(ents)}   "
          f"multi-row: {sum(1 for e in ents.values() if e.n_titles >= 2)}")
    print("\nTop multi-category entities (high cross-category spread => seller):")
    print(f"{'entity':22s} {'#titles':>7} {'#cats':>5} {'slots':<16} surfaces")
    for e in multi[:35]:
        print(f"{e.key[:22]:22s} {e.n_titles:7d} {e.n_categories:5d} "
              f"{','.join(sorted(e.slots)):<16} {sorted(e.surfaces)[:3]}")
