import argparse
import concurrent.futures
import csv
import logging
import os
import sys
import threading
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

from pipeline import config
from pipeline.config import LIKELY_WRONG, MORPH
from pipeline.engines import Engines, RawLog, Terminal, hist

log = logging.getLogger("phase1")
COLS = ["title", "label", "confidence", "brandname", "verdict", "status",
        "flags", "reasoning"]


def read_titles(path: str, col: str) -> list[str]:
    seen, out = set(), []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            t = (r.get(col) or "").strip()
            if t and t not in seen:
                seen.add(t)
                out.append(t)
    return out


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Phase 1: classify + logprob-verify.")
    ap.add_argument("--input", default="distinct_products_po_1000.csv")
    ap.add_argument("--title-col", default="product_title")
    ap.add_argument("--out", default="phase1_results.csv")
    ap.add_argument("--raw-log", default="phase1_raw.jsonl")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    config.add_args(ap)
    a = ap.parse_args(argv)
    cfg = config.from_args(a)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    if not cfg.mock:
        missing = [k for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")
                   if not os.environ.get(k)]
        if missing:
            sys.exit(f"missing env var(s): {', '.join(missing)}")

    titles = read_titles(a.input, a.title_col)
    if a.limit:
        titles = titles[:a.limit]

    exists = os.path.exists(a.out) and os.path.getsize(a.out) > 0
    if exists and not a.resume:
        sys.exit(f"{a.out} exists — pass --resume to continue it, or delete it")
    done = set()
    if exists:
        with open(a.out, newline="", encoding="utf-8-sig") as fh:
            done = {r["title"] for r in csv.DictReader(fh)}
    todo = [t for t in titles if t not in done]
    log.info("%d titles (%d already done, %d to run)", len(titles), len(done),
             len(todo))

    eng = Engines(cfg, RawLog(a.raw_log))
    fh = open(a.out, "a", newline="", encoding="utf-8")
    w = csv.DictWriter(fh, fieldnames=COLS)
    if not exists:
        w.writeheader()
        fh.flush()
    wlock = threading.Lock()
    abort = threading.Event()
    n = [0]

    def emit(row: dict) -> None:
        with wlock:
            w.writerow(row)
            fh.flush()
            n[0] += 1
            if n[0] % 25 == 0:
                log.info("%d/%d", n[0], len(todo))

    def work(title: str) -> None:
        if abort.is_set():
            return
        row = {"title": title, "label": "", "confidence": "", "brandname": "",
               "verdict": "", "status": "grey", "flags": "", "reasoning": ""}
        try:
            cls = eng.classify1(title)
        except Terminal as exc:
            abort.set()
            log.error("TERMINAL on %r: %s", title, exc)
            return
        except Exception as exc:                          # noqa: BLE001
            log.error("stage1 %r failed: %s", title, exc)
            row["flags"] = "stage1_error"
            emit(row)
            return
        if cls is None:
            row["flags"] = "stage1_error"
            emit(row)
            return
        row.update(label=cls.branding, brandname=cls.brandname,
                   reasoning=cls.reasoning)
        try:
            p, v, anom = eng.verify(title, cls)
        except Terminal as exc:
            abort.set()
            log.error("TERMINAL on %r: %s", title, exc)
            return
        except Exception as exc:                          # noqa: BLE001
            log.error("verify %r failed: %s", title, exc)
            row["flags"] = "verify_error"
            emit(row)
            return
        flags = []
        if anom:
            flags.append("verifier_anomaly")
            p = 0.5
        if v == "D" and p <= LIKELY_WRONG:
            flags.append("likely_wrong")
        guard = cls.branding == "Branded" and MORPH in cls.reasoning
        if guard:
            flags.append("morphology_guard")
        row.update(verdict=v, confidence=round(p, 4),
                   status="accepted" if (v == "A" and p >= cfg.grey and not guard)
                   else "grey",
                   flags=";".join(flags))
        emit(row)

    with concurrent.futures.ThreadPoolExecutor(cfg.workers) as pool:
        list(pool.map(work, todo))
    fh.close()

    if abort.is_set():
        log.error("RUN ABORTED on a terminal error (quota/auth). Completed rows "
                  "are saved; fix billing/keys then rerun with --resume.")
        sys.exit(2)

    with open(a.out, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    # final file is sorted lowest-confidence first (missing confidence on top)
    rows.sort(key=lambda r: float(r["confidence"]) if r["confidence"] else -1.0)
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    acc = [r for r in rows if r["status"] == "accepted"]
    grey = [r for r in rows if r["status"] == "grey"]
    ps = [float(r["confidence"]) for r in rows if r["confidence"]]
    hard_d = sum(1 for r in rows if r["verdict"] == "D"
                 and r["confidence"] and float(r["confidence"]) <= LIKELY_WRONG)
    print("=" * 60)
    print(f"phase 1: {len(rows)} rows  accepted {len(acc)}  grey {len(grey)}")
    print(f"high-confidence Disagrees (p_agree <= {LIKELY_WRONG}): {hard_d}")
    print("p_agree histogram:")
    print(hist(ps))


if __name__ == "__main__":
    main()
