import argparse
import concurrent.futures
import csv
import logging
import math
import os
import sys
import threading
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from openai import OpenAI

from pipeline.engines import E1_SYSTEM, Terminal, Tpm, call_with_retry, est, hist

log = logging.getLogger("scorer")
COLS = ["title", "label", "brandname", "confidence", "status",
        "opus_label", "verifier_reasoning"]
OPUS = "OPUS(BRAND/NO BRAND)"
OPUS_LABEL = {"BRAND": "Branded", "NO BRAND": "Unbranded"}

SCORER_SYSTEM = """You are an output confidence checker who audits another model's classification.
You will receive:
Input 1 - the raw input given to the other model
Input 2 - the prompt the other model was given
Input 3 - the output the other model generated
Input 4 - the reasoning the other model gave for that output

Rate how well the OUTPUT is supported by the reasoning, the raw input, and
your own knowledge, on a 0-9 scale:
9   = certainly correct — specific, independently checkable anchors (a real
      owner or company, a real word/vernacular meaning, a concrete structural
      pattern in the raw input) that survive the obvious alternative readings
7-8 = strong support with minor gaps
4-6 = cannot verify either way — e.g. an unfamiliar name that may well be a
      real small seller: neither corroborated nor refuted
2-3 = weak — the reasoning leans on appearance/pattern-matching alone, or
      ignores a plausible alternative reading (vernacular word, internal
      code, generic descriptor)
0-1 = clearly wrong — invented facts, contradicts the raw input, or a better
      reading clearly exists

The other model may know facts you don't; an unfamiliar claim is not
automatically false — that is exactly what the middle of the scale is for.
But rank is not evidence: judge the anchors, not the author.

Output format — exactly this:
Line 1: one digit, 0-9
Then: your justification for that score, succinct, max 100 words."""

SCORER_USER = """Input 1 (raw input given to the other model): {title}
Input 2 (prompt given to the other model): {prompt}
Input 3 (output the other model generated): Branding={label}, Brandname={name}
Input 4 (reasoning given by the other model): {reasoning}"""


def expected_confidence(resp) -> tuple[float | str, str]:
    """Digit is the first token; confidence = expected digit / 9 over the
    top_logprobs digit mass at position 0."""
    content = resp.choices[0].logprobs.content
    text = (resp.choices[0].message.content or "").strip()
    if not content:
        return "", text
    mass: dict[int, float] = {}
    for e in content[0].top_logprobs:
        t = e.token.strip()
        if t.isdigit() and len(t) == 1:
            mass[int(t)] = mass.get(int(t), 0.0) + math.exp(e.logprob)
    total = sum(mass.values())
    if total == 0.0:
        return "", text
    exp_score = sum(d * p for d, p in mass.items()) / total
    reasoning = text.split("\n", 1)[1].strip() if "\n" in text else ""
    return round(exp_score / 9, 4), reasoning.replace("\n", " ").strip()


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(
        description="0-9 digit-scorer verifier over classified rows.")
    ap.add_argument("--input", default="opus_phase1_results.csv",
                    help="needs title,label,brandname,reasoning; an "
                         f"'{OPUS}' column is carried through if present")
    ap.add_argument("--out", default="finalconfident.csv")
    ap.add_argument("--model", default="gpt-4o")
    ap.add_argument("--grey", type=float, default=0.85)
    ap.add_argument("--tpm", type=int, default=30000)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--resume", action="store_true")
    a = ap.parse_args(argv)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("missing env var: OPENAI_API_KEY")

    with open(a.input, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))

    exists = os.path.exists(a.out) and os.path.getsize(a.out) > 0
    if exists and not a.resume:
        sys.exit(f"{a.out} exists — pass --resume to continue it, or delete it")
    done = set()
    if exists:
        with open(a.out, newline="", encoding="utf-8-sig") as fh:
            done = {r["title"] for r in csv.DictReader(fh)}
    todo = [r for r in rows if r["title"] not in done]
    log.info("%d rows (%d done, %d to score)", len(rows), len(done), len(todo))

    oc = OpenAI()
    tpm = Tpm(a.tpm)
    fh = open(a.out, "a", newline="", encoding="utf-8")
    w = csv.DictWriter(fh, fieldnames=COLS)
    if not exists:
        w.writeheader()
        fh.flush()
    lock, abort, n = threading.Lock(), threading.Event(), [0]

    def work(r):
        if abort.is_set():
            return
        user = SCORER_USER.format(title=r["title"], prompt=E1_SYSTEM,
                                  label=r["label"], name=r["brandname"],
                                  reasoning=r["reasoning"])
        try:
            tpm.take(est(SCORER_SYSTEM, user, out=200))
            resp = call_with_retry(lambda: oc.chat.completions.create(
                model=a.model,
                messages=[{"role": "system", "content": SCORER_SYSTEM},
                          {"role": "user", "content": user}],
                temperature=0, max_tokens=200, logprobs=True, top_logprobs=10))
            conf, reasoning = expected_confidence(resp)
        except Terminal as exc:
            abort.set()
            log.error("TERMINAL on %r: %s", r["title"], exc)
            return
        except Exception as exc:                          # noqa: BLE001
            log.error("skip %r: %s", r["title"][:40], exc)
            conf, reasoning = "", f"(error: {exc})"
        status = "accepted" if conf != "" and float(conf) >= a.grey else "grey"
        with lock:
            w.writerow({"title": r["title"], "label": r["label"],
                        "brandname": r["brandname"], "confidence": conf,
                        "status": status,
                        "opus_label": OPUS_LABEL.get(
                            (r.get(OPUS) or "").strip(), ""),
                        "verifier_reasoning": reasoning})
            fh.flush()
            n[0] += 1
            if n[0] % 50 == 0:
                log.info("%d/%d", n[0], len(todo))

    with concurrent.futures.ThreadPoolExecutor(a.workers) as pool:
        list(pool.map(work, todo))
    fh.close()
    if abort.is_set():
        log.error("RUN ABORTED on a terminal error; rerun with --resume.")
        sys.exit(2)

    with open(a.out, newline="", encoding="utf-8-sig") as fh:
        final = list(csv.DictReader(fh))
    final.sort(key=lambda r: float(r["confidence"]) if r["confidence"] else -1)
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(final)

    scored = [r for r in final if r["confidence"]]
    acc = sum(1 for r in scored if r["status"] == "accepted")
    ps = [float(r["confidence"]) for r in scored]
    print("=" * 60)
    print(f"scorer: {len(scored)} rows  accepted {acc}  "
          f"grey {len(scored) - acc}  (threshold {a.grey})")
    print(hist(ps))


if __name__ == "__main__":
    main()
