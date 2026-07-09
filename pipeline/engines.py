import json
import math
import random
import statistics
import threading
import time
from collections import deque

from .config import Config
from .schemas import Cls, ParseError, parse_cls

E1_SYSTEM = """These are product titles from a noisy Indian B2B grocery/food-service catalog
(multilingual, abbreviations, internal codes, all kinds of sellers).

Goal: deduce whether the product is BRANDED or UNBRANDED, along with its brand
name and the reasoning involved. Include as many facts as you can.

Output only this JSON, nothing else:
{"Branding": "Branded" | "Unbranded",
 "Brandname": "NA" | "<brand name, e.g. Coca-Cola>",
 "Reasoning": "<why you arrived at the decision — as many facts as possible>"}"""

E2_SYSTEM = """You are an adversarial auditor of another model's product classification. You will
see a product TITLE, a claimed LABEL (Branded/Unbranded), a BRANDNAME, and the
REASONING given.

Your job: decide whether the label is actually COMPELLED by the reasoning and the
title — not whether the reasoning is well-written. Fluent, confident, plausible
prose is NOT evidence. You must actively hunt for the weakest link:

- Does any factual claim look invented or unverifiable? (fabricated brand histories
  for unknown tokens are the #1 failure)
- Is the argument "this word looks coined/unique, therefore brand"? Morphology alone
  is NEVER sufficient — Disagree unless corroborated by recalled knowledge or
  structural evidence (seller slot, known owner).
- Does the reasoning ignore an alternative reading (vernacular word, internal code,
  generic descriptor in the seller slot)?
- Does the reasoning contradict the title itself?
- Did the classifier admit "morphology-based inference" or "unrecognized token"?
  If that admission is load-bearing for the label, Disagree.

If the reasoning contains recalled, specific, checkable facts (real owner, real
product line, real vernacular meaning) that dispositively support the label: Agree.
If the label is merely plausible: Disagree. Plausible is not enough.

Answer with exactly one letter:
A = Agree (label compelled by dispositive evidence)
D = Disagree (evidence insufficient, invented, or contradicted)"""

E2_USER = """TITLE: {title}
LABEL: {label}
BRANDNAME: {name}
REASONING: {reasoning}

One letter, A or D:"""

WEB_SYSTEM = """You research whether a name from an Indian B2B grocery/food-service catalog is a
real brand, company, or seller. Use web search. Report concretely what you
find: the owning company, product lines, store/marketplace listings,
trademark/registration, city/region — with source names. Report every company
you find carrying the name; do NOT judge whether it matches this particular
product — that is a downstream job, and sellers in this catalog often tag
items far outside their known product focus. Never conclude "no evidence"
when you did find a company with the name: report the company. Only say the
search found nothing when there is genuinely no such company at all.
3-6 sentences, facts only."""

WEB_USER = """Product title: {title}
Candidate brand/seller name: {name}
{context}
What does the web say about this name as a brand/company/seller? Sellers in
this catalog are often small Indian outlets, cloud kitchens, bakeries, or D2C
labels whose name tags MANY unrelated items (their whole catalog, including
packaging). So if you find a real company with this name in India, that
corroborates it even if its main products differ from this one item. If the
candidate looks wrong, also check the other distinctive tokens in the title —
especially a trailing "- Name" segment, which is usually the seller's name."""

E2_WEB_SYSTEM = """You make the FINAL call on a product classification, weighing ALL the evidence
given: the product TITLE, a prior classifier's LABEL/BRANDNAME/REASONING,
CATALOG CONTEXT (how the candidate name recurs across this catalog), and WEB
RESEARCH (findings from a live internet search we ran on the candidate name
just now — independent external evidence, more current than your training
data).

Weigh evidence by class:
- Strong: web findings naming a real company — owner, trademark, website,
  store/marketplace listings — whose name matches a distinctive token in the
  title; the same name recurring across many UNRELATED items in this catalog
  (outlets, cloud kitchens, and D2C sellers tag their whole menu and even
  packaging with their name).
- Weak: the prior classifier's unsupported assertions; your own inability to
  recall the name (obscure real sellers are common here); a web-found company
  whose known products differ from this one item — that does NOT disqualify
  it when the catalog shows the name recurring as a seller tag.
- Against: web search finding no such company at all; a fitting generic or
  vernacular reading of the token; findings that contradict the claimed brand.

Decide whether the LABEL is correct. Answer with exactly one letter:
A = the label is correct on this evidence
D = the label is wrong, or the evidence cannot support it"""

E2_USER_WEB = """TITLE: {title}
LABEL: {label}
BRANDNAME: {name}
REASONING: {reasoning}
{context}
WEB RESEARCH (live search results): {findings}

One letter, A or D:"""

RETRY_JSON = "\n\nReturn ONLY the JSON object."
TERMINAL_PAT = ("insufficient_quota", "exceeded your current quota",
                "invalid_api_key", "authentication_error", "access denied")


class Terminal(RuntimeError):
    """Quota/auth failure — abort the run, never default a label."""


def is_terminal(exc: Exception) -> bool:
    s = str(exc).lower()
    if any(p in s for p in TERMINAL_PAT):
        return True
    return getattr(exc, "status_code", None) in (401, 403)


def call_with_retry(fn, retries: int = 5):
    last = None
    for i in range(retries):
        try:
            return fn()
        except Exception as exc:                          # noqa: BLE001
            if is_terminal(exc):
                raise Terminal(str(exc)) from exc
            code = getattr(exc, "status_code", None)
            if code is not None and 400 <= code < 500 and code != 429:
                raise
            last = exc
            time.sleep(min(30.0, 2 ** i + random.uniform(0, 1)))
    raise last


class Tpm:
    """Sliding-window tokens-per-minute throttle shared across worker threads."""

    def __init__(self, budget: int):
        self.budget = budget
        self.lock = threading.Lock()
        self.win: deque = deque()

    def take(self, n: int) -> None:
        while True:
            with self.lock:
                now = time.time()
                while self.win and now - self.win[0][0] > 60:
                    self.win.popleft()
                if sum(t for _, t in self.win) + n <= self.budget:
                    self.win.append((now, n))
                    return
                wait = 60 - (now - self.win[0][0]) + 0.05 if self.win else 1.0
            time.sleep(min(max(wait, 0.05), 5.0))


def est(*texts: str, out: int = 0) -> int:
    return sum(len(t or "") for t in texts) // 4 + out


class RawLog:
    def __init__(self, path: str):
        self.fh = open(path, "a", encoding="utf-8")
        self.lock = threading.Lock()

    def write(self, engine: str, title: str, payload) -> None:
        rec = {"ts": time.time(), "engine": engine, "title": title,
               "payload": payload}
        with self.lock:
            self.fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
            self.fh.flush()


def dump(resp):
    try:
        return resp.model_dump()
    except Exception:                                     # noqa: BLE001
        return str(resp)


def extract_p_agree(resp) -> tuple[float, bool]:
    """(p_agree, anomaly). Mass on A/D token variants at position 0, renormalized."""
    content = getattr(resp.choices[0].logprobs, "content", None)
    if not content:
        return 0.5, True
    p_a = p_d = 0.0
    for e in content[0].top_logprobs:
        t = e.token.strip().strip(".,:;!?'\"").upper()
        if t == "A":
            p_a += math.exp(e.logprob)
        elif t == "D":
            p_d += math.exp(e.logprob)
    if p_a == 0.0 and p_d == 0.0:
        return 0.5, True
    return (p_a + 1e-6) / (p_a + p_d + 2e-6), False


# ---------------------------------------------------------------- mock mode --
# Deterministic offline stubs. Verifier keys on evidence markers the classifier
# stubs plant: FACT: (dispositive) / CODE: (weak) / WEAK: (plausible only) /
# the two admission phrases from the E1 prompt.
MOCK_TABLE = {
    "maggi": (
        ("Branded", "Maggi (Nestle India)",
         "FACT: Maggi is an instant-noodle brand owned by Nestle India; the token leads the title."),
        None),
    "kinley": (
        ("Branded", "Kinley (Coca-Cola)",
         "FACT: Kinley is Coca-Cola's packaged water/soda brand; the token appears inline in the title."),
        None),
    "sassy teaspoon": (
        ("Branded", "Sassy Teaspoon",
         "FACT: 'Sassy Teaspoon' occupies the trailing 'product - X' seller slot; The Sassy Teaspoon is a Mumbai bakery."),
        None),
    "curry leaves": (
        ("Unbranded", "NA",
         "FACT: 'curry leaves' names a fresh-produce commodity; no maker token is present."),
        None),
    "onion": (
        ("Unbranded", "NA",
         "FACT: 'onion large' is a commodity description with a size word; no maker token."),
        None),
    "eggs tray": (
        ("Unbranded", "NA",
         "FACT: 'eggs tray' is a commodity plus packaging word; no maker token."),
        None),
    "red label": (
        ("Unbranded", "NA",
         "WEAK: 'red' and 'label' read as ordinary packaging words; no maker token identified."),
        ("Branded", "Red Label (Brooke Bond / Hindustan Unilever)",
         "FACT: 'Red Label' is a Brooke Bond tea brand line owned by Hindustan Unilever; the bigram is a brand even though each word alone is generic.")),
    "chulla": (
        ("Branded", "Chulla",
         "The token looks coined and brand-like; morphology-based inference, not recalled knowledge."),
        ("Unbranded", "NA",
         "FACT: 'chulla'/'chulha' is Hindi for a cooking stove; the title is the vernacular product word itself, not a maker.")),
    "murukku": (
        ("Unbranded", "NA",
         "WEAK: the trailing token names murukku, a South Indian snack; assumed the suffix is the product word."),
        ("Branded", "Murukku (seller)",
         "FACT: the token occupies the trailing 'product - X' seller slot on a non-food item (a stirrer); a seller can be named after a snack.")),
    "gluten nb": (
        ("Unbranded", "NA",
         "CODE: 'GLUTEN NB 0121' matches an internal stock-code pattern (word + alpha prefix + numeric run); no maker token."),
        ("Unbranded", "NA",
         "CODE: alpha-numeric internal code; unrecognized token 'NB 0121'; no maker evidence either way.")),
    "3cp plate": (
        ("Unbranded", "NA",
         "CODE: '3CP' is an unrecognized token that matches packaging-SKU code patterns; 'plate' is generic."),
        ("Unbranded", "NA",
         "CODE: packaging SKU; unrecognized token '3CP'; no maker evidence either way.")),
    "chonker": (
        ("Branded", "Chonkers",
         "'OG Choc Chip Chonker' reads like a D2C cookie brand; morphology-based inference, not recalled knowledge."),
        ("Branded", "Chonkers",
         "The coined word 'Chonker' resembles a playful D2C brand; morphology-based inference, not recalled knowledge.")),
}


def _mock_lookup(title: str):
    t = title.lower()
    for key, val in MOCK_TABLE.items():
        if key in t:
            return val
    return None


def mock_classify(title: str, stage: int) -> Cls:
    hit = _mock_lookup(title)
    if hit:
        s1, s2 = hit
        b, n, r = s2 if (stage == 2 and s2) else s1
        return Cls(b, n, r)
    t = title.strip()
    if " - " in t:
        seller = t.rsplit(" - ", 1)[1].strip()
        return Cls("Branded", seller,
                   f"FACT: '{seller}' occupies the trailing 'product - X' seller slot.")
    if any(c.isdigit() for c in t) and t.upper() == t:
        return Cls("Unbranded", "NA",
                   "CODE: all-caps title with a numeric run matches internal code patterns.")
    return Cls("Unbranded", "NA",
               "FACT: descriptive commodity words only; no maker token present.")


MOCK_WEB = {
    "chonker": "Found: Chonkers is an Indian D2C cookie brand (site and "
               "Instagram store listings, Mumbai).",
    "murukku": "Found: Murukku is a Chennai-based snacks seller listed on "
               "Swiggy and marketplaces.",
    "red label": "Found: Red Label is a Brooke Bond tea brand owned by "
                 "Hindustan Unilever.",
}


def mock_research(title: str, name: str) -> str:
    t = f"{title} {name}".lower()
    for k, v in MOCK_WEB.items():
        if k in t:
            return v
    return f"Search found no evidence of {name!r} as a brand or company."


def mock_verify_web(cls: Cls, findings: str) -> tuple[float, str, bool]:
    if findings.startswith("Found:"):
        p = 0.95 if cls.branding == "Branded" else 0.05
    else:
        p = 0.55                     # unverifiable stays mid, never zero
    return p, ("A" if p > 0.5 else "D"), False


def mock_verify(title: str, cls: Cls) -> tuple[float, str, bool]:
    r = cls.reasoning
    if "morphology-based inference" in r:
        p = 0.10
    elif r.startswith("WEAK:"):
        p = 0.60
    elif r.startswith("CODE:"):
        p = 0.78
    elif "unrecognized token" in r:
        p = 0.45
    elif "FACT:" in r:
        p = 0.96
    else:
        p = 0.70
    p += (hash(title + cls.branding) % 7) * 0.003          # stable, non-degenerate
    p = min(max(p, 0.01), 0.995)
    return p, ("A" if p > 0.5 else "D"), False


# ------------------------------------------------------------------ engines --
class Engines:
    def __init__(self, cfg: Config, raw: RawLog):
        self.cfg = cfg
        self.raw = raw
        self.tpm = Tpm(cfg.tpm)
        if not cfg.mock:
            from anthropic import Anthropic
            from openai import OpenAI
            self.ac = Anthropic()
            self.oc = OpenAI()

    def classify1(self, title: str) -> Cls | None:
        if self.cfg.mock:
            cls = mock_classify(title, 1)
            self.raw.write("e1-mock", title, cls.to_json())
            return cls
        for extra in ("", RETRY_JSON):
            user = title + extra
            self.tpm.take(est(E1_SYSTEM, user, out=500))
            resp = call_with_retry(lambda u=user: self.ac.messages.create(
                model=self.cfg.e1_model, max_tokens=500, temperature=0,
                system=E1_SYSTEM, messages=[{"role": "user", "content": u}]))
            self.raw.write("e1", title, dump(resp))
            text = "".join(b.text for b in resp.content if b.type == "text")
            try:
                return parse_cls(text)
            except ParseError:
                continue
        return None

    def research(self, title: str, name: str, context: str = "") -> str:
        """Live web search on the candidate name; returns findings text."""
        if self.cfg.mock:
            text = mock_research(title, name)
            self.raw.write("websearch-mock", title, text)
            return text
        q = WEB_USER.format(title=title, name=name, context=context)
        prompt = WEB_SYSTEM + "\n\n" + q
        # OpenAI has shipped web search under several API shapes; try newest first
        attempts = [
            lambda: self.oc.responses.create(
                model=self.cfg.search_model, tools=[{"type": "web_search"}],
                input=prompt).output_text,
            lambda: self.oc.responses.create(
                model=self.cfg.search_model,
                tools=[{"type": "web_search_preview"}],
                input=prompt).output_text,
            lambda: self.oc.chat.completions.create(
                model="gpt-4o-search-preview", web_search_options={},
                messages=[{"role": "system", "content": WEB_SYSTEM},
                          {"role": "user", "content": q}],
            ).choices[0].message.content,
        ]
        last: Exception | None = None
        for fn in attempts:
            try:
                self.tpm.take(est(prompt, out=400))
                text = call_with_retry(fn)
                if text and text.strip():
                    self.raw.write("websearch", title, text)
                    return text.strip()
            except Terminal:
                raise
            except Exception as exc:                      # noqa: BLE001
                last = exc
        raise RuntimeError(f"web research failed on all API shapes: {last}")

    def verify_web(self, title: str, cls: Cls, findings: str,
                   context: str = "") -> tuple[float, str, bool]:
        """Same forced-token logprob verdict, with web findings as evidence."""
        if self.cfg.mock:
            p, v, anom = mock_verify_web(cls, findings)
            self.raw.write("e2web-mock", title, {"p_agree": p, "verdict": v})
            return p, v, anom
        system = E2_WEB_SYSTEM
        user = E2_USER_WEB.format(title=title, label=cls.branding,
                                  name=cls.brandname, reasoning=cls.reasoning,
                                  findings=findings, context=context)
        ps, anomaly = [], False
        for _ in range(max(1, self.cfg.k)):
            self.tpm.take(est(system, user, out=1))
            resp = call_with_retry(lambda: self.oc.chat.completions.create(
                model=self.cfg.e2_model,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                temperature=0, max_tokens=1, logprobs=True, top_logprobs=10))
            self.raw.write("e2web", title, dump(resp))
            p, anom = extract_p_agree(resp)
            ps.append(p)
            anomaly = anomaly or anom
        p = statistics.median(ps)
        return p, ("A" if p > 0.5 else "D"), anomaly

    def verify(self, title: str, cls: Cls) -> tuple[float, str, bool]:
        if self.cfg.mock:
            p, v, anom = mock_verify(title, cls)
            self.raw.write("e2-mock", title, {"p_agree": p, "verdict": v})
            return p, v, anom
        user = E2_USER.format(title=title, label=cls.branding,
                              name=cls.brandname, reasoning=cls.reasoning)
        ps, anomaly = [], False
        for _ in range(max(1, self.cfg.k)):
            self.tpm.take(est(E2_SYSTEM, user, out=1))
            resp = call_with_retry(lambda: self.oc.chat.completions.create(
                model=self.cfg.e2_model,
                messages=[{"role": "system", "content": E2_SYSTEM},
                          {"role": "user", "content": user}],
                temperature=0, max_tokens=1, logprobs=True, top_logprobs=10))
            self.raw.write("e2", title, dump(resp))
            p, anom = extract_p_agree(resp)
            ps.append(p)
            anomaly = anomaly or anom
        p = statistics.median(ps)
        return p, ("A" if p > 0.5 else "D"), anomaly


def hist(ps: list[float], bins: int = 10) -> str:
    if not ps:
        return "  (no confidences)"
    counts = [0] * bins
    for p in ps:
        counts[min(int(p * bins), bins - 1)] += 1
    peak = max(counts) or 1
    lines = []
    for i, c in enumerate(counts):
        bar = "#" * max(1, round(30 * c / peak)) if c else ""
        lines.append(f"  {i / bins:.1f}-{(i + 1) / bins:.1f}  {c:5d}  {bar}")
    return "\n".join(lines)
