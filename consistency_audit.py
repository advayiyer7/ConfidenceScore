"""consistency_audit.py — measure Type-1 self-contradictions in the current
1,000-row reasoning output, with ZERO ground truth.

Idea: extract candidate maker tokens from each title (suffix seller slot,
prefix/inline proper nouns, all-caps tokens), normalize + fuzzy-cluster them,
then for each entity look at the set of labels its titles received. An entity
whose titles got BOTH 'branded' and 'unbranded' is a self-contradiction the
model cannot defend — same name, two answers.
"""
import csv
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher

PATH = sys.argv[1] if len(sys.argv) > 1 else "reasoning_predictions.csv"

# Generic descriptor / unit / packaging words that are NOT makers even when
# they sit in a brand-like slot or are capitalized.
GENERIC = {
    "ml", "ltr", "l", "kg", "gm", "gms", "g", "gsm", "kgs", "mm", "cm", "oz",
    "pc", "pcs", "pkt", "pack", "box", "bag", "jar", "can", "tin", "tub",
    "cup", "lid", "tray", "pouch", "sticker", "stickers", "cover", "outer",
    "frozen", "fresh", "premium", "plain", "round", "big", "small", "large",
    "veg", "non", "hamper", "container", "bottle", "paper", "plastic", "roll",
    "sheet", "card", "powder", "sauce", "oil", "milk", "water", "tea", "coffee",
    "rice", "flour", "atta", "sugar", "salt", "chilli", "chili", "masala",
    "cake", "chocolate", "choc", "ice", "cream", "icecream", "bar", "cookie",
    "dough", "premix", "mix", "paste", "syrup", "juice", "crush", "seeds",
    "seed", "whole", "dal", "dry", "green", "red", "white", "black", "blue",
    "yellow", "sf", "nas", "gst", "the", "of", "with", "and", "for", "incremental",
}
# Suffix slot junk that is a code/descriptor, never a seller name.
CODE_RE = re.compile(r"^[a-z]?[-_\s]*\d{2,}|^[a-z]{1,3}\d|^\d", re.I)


def clean(s):
    return re.sub(r"[^\w\s]", " ", s).strip()


def norm(tok):
    return re.sub(r"[^a-z0-9]", "", tok.lower())


def build_acronyms(titles):
    """Corpus signal: an all-caps token is a real acronym-brand only if it ever
    appears uppercase inside an otherwise MIXED-CASE title. A token that is only
    ever seen in fully-shouted titles (CHICKEN LEG RAW) is just a loud product
    word, not a brand."""
    acro = set()
    for t in titles:
        t = re.sub(r"^#_#\s*", "", t.strip())
        has_lower = any(c.islower() for c in t)
        if not has_lower:
            continue
        for m in re.findall(r"\b[A-Z]{2,}\b", t):
            if m.lower() not in GENERIC and not m.isdigit():
                acro.add(m)
    return acro


def candidates(title, acronyms):
    """Return {candidate_string: source_slot} extracted from the title.

    source_slot in {'suffix','allcaps','prefix'} — 'suffix' and 'allcaps' are
    high-precision maker slots; 'prefix' (leading Title-case word) is noisy
    because it also catches generic product head-nouns.
    """
    t = title.strip()
    t = re.sub(r"^#_#\s*", "", t)            # drop the #_# label marker
    out = {}

    def put(s, slot):
        s = s.strip()
        if len(norm(s)) >= 3 and out.get(s) != "suffix":
            # don't let a weaker slot overwrite a strong 'suffix' tag
            if s not in out or _rank(slot) > _rank(out[s]):
                out[s] = slot

    # 1) suffix seller slot: segment after the last ' - '
    parts = [p.strip() for p in re.split(r"\s-\s|\s–\s", t) if p.strip()]
    if len(parts) >= 2:
        suf = parts[-1]
        sw = clean(suf)
        if sw and not CODE_RE.match(suf) and not _all_generic(sw):
            put(sw, "suffix")
        pre = parts[0]                       # prefix slot
        m = re.match(r"([A-Z][A-Za-z&']+(?:\s+[A-Z][A-Za-z&']+){0,2})", pre)
        if m and not _all_generic(clean(m.group(1))):
            put(clean(m.group(1)), "prefix")
    # 2) all-caps acronym tokens (MDH, VKL, SNACC) — only corpus-confirmed ones
    for m in re.findall(r"\b[A-Z]{2,}\b", t):
        if m in acronyms:
            put(m, "allcaps")
    # 3) leading Title-case token of the whole title (inline/prefix brand)
    m = re.match(r"([A-Z][a-z]{2,})", t)
    if m and m.group(1).lower() not in GENERIC:
        put(m.group(1), "prefix")
    return out


def _rank(slot):
    return {"prefix": 0, "allcaps": 1, "suffix": 2}.get(slot, 0)


def _all_generic(phrase):
    toks = [w for w in phrase.lower().split() if w]
    return bool(toks) and all(w in GENERIC or w.isdigit() for w in toks)


def fuzzy_key(n, keys, thresh=0.86):
    for k in keys:
        if SequenceMatcher(None, n, k).ratio() >= thresh:
            return k
    return None


def main():
    rows = []
    with open(PATH, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            rows.append((r["title"], r["prediction"].strip().lower(),
                         float(r["confidence"])))

    acronyms = build_acronyms([t for t, _, _ in rows])
    # entity -> list of (title, label, conf, surface, slot)
    ent = defaultdict(list)
    canon = {}          # normalized token -> canonical key (fuzzy-merged)
    for title, label, conf in rows:
        seen_keys = set()
        for c, slot in candidates(title, acronyms).items():
            n = norm(c)
            if not n:
                continue
            key = canon.get(n) or fuzzy_key(n, canon.values())
            if key is None:
                key = n
            canon[n] = key
            if key not in seen_keys:
                ent[key].append((title, label, conf, c, slot))
                seen_keys.add(key)

    strong, weak = [], []
    for key, items in ent.items():
        if len(items) < 2:
            continue
        if len({lab for _, lab, *_ in items}) > 1:
            disp = max((c for _, _, _, c, _ in items), key=len)
            slots = {s for *_, s in items}
            (strong if slots & {"suffix", "allcaps"} else weak).append((disp, items))

    strong.sort(key=lambda x: -len(x[1]))
    weak.sort(key=lambda x: -len(x[1]))

    def show(title_, groups):
        print(f"\n{'#' * 70}\n## {title_}: {len(groups)} clusters, "
              f"{sum(len(it) for _, it in groups)} titles\n{'#' * 70}")
        for disp, items in groups:
            b = sum(1 for _, l, *_ in items if l == "branded")
            print(f"\n[{disp}]  branded={b} unbranded={len(items) - b}")
            for title, lab, conf, surf, slot in sorted(items, key=lambda x: x[1]):
                print(f"   {lab:9s} c={conf:.3f} ({slot:6s}) {title[:64]}")

    print(f"rows audited:                 {len(rows)}")
    print(f"distinct candidate entities:  {len(ent)}")
    print(f"STRONG-slot contradictions:   {len(strong)} clusters "
          f"({sum(len(it) for _, it in strong)} titles)  <-- defensible Type-1")
    print(f"prefix-only (noisy) clusters: {len(weak)} clusters "
          f"({sum(len(it) for _, it in weak)} titles)  <-- mostly head-noun artifacts")
    show("STRONG-SLOT SELF-CONTRADICTIONS (suffix seller-slot / all-caps)", strong)
    show("PREFIX-ONLY (manual triage: real brands like Taski/Twinings mixed "
         "with head-noun noise)", weak)


if __name__ == "__main__":
    main()
