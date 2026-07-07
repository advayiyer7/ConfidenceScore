import argparse
import concurrent.futures
import csv
import json
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

log = logging.getLogger("phase2")
COLS = ["title", "label", "brandname", "confidence", "verdict", "phase",
        "status", "reasoning_s1", "reasoning_s2", "p_agree_s1", "p_agree_s2",
        "flags"]


def prev_json(r: dict) -> str:
    return json.dumps({"Branding": r["label"] or "unknown",
                       "Brandname": r["brandname"] or "NA",
                       "Reasoning": r["reasoning"] or "(stage 1 errored)"},
                      ensure_ascii=False)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="Phase 2: grey-zone escalation.")
    ap.add_argument("--phase1", default="phase1_results.csv")
    ap.add_argument("--out", default="final_predictions.csv")
    ap.add_argument("--review", default="review_queue.csv")
    ap.add_argument("--raw-log", default="phase2_raw.jsonl")
    ap.add_argument("--resume", action="store_true")
    config.add_args(ap)
    a = ap.parse_args(argv)
    cfg = config.from_args(a)

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    load_dotenv()
    if not cfg.mock and not os.environ.get("OPENAI_API_KEY"):
        sys.exit("missing env var: OPENAI_API_KEY")

    with open(a.phase1, newline="", encoding="utf-8-sig") as fh:
        p1 = list(csv.DictReader(fh))

    exists = os.path.exists(a.out) and os.path.getsize(a.out) > 0
    if exists and not a.resume:
        sys.exit(f"{a.out} exists — pass --resume to continue it, or delete it")
    done = set()
    if exists:
        with open(a.out, newline="", encoding="utf-8-sig") as fh:
            done = {r["title"] for r in csv.DictReader(fh)}

    fh = open(a.out, "a", newline="", encoding="utf-8")
    w = csv.DictWriter(fh, fieldnames=COLS)
    if not exists:
        w.writeheader()
        fh.flush()
    wlock = threading.Lock()
    abort = threading.Event()

    def emit(row: dict) -> None:
        with wlock:
            w.writerow(row)
            fh.flush()

    # phase-1 accepts pass straight through, no API
    for r in p1:
        if r["status"] == "accepted" and r["title"] not in done:
            emit({"title": r["title"], "label": r["label"],
                  "brandname": r["brandname"], "confidence": r["confidence"],
                  "verdict": r["verdict"], "phase": 1, "status": "accepted",
                  "reasoning_s1": r["reasoning"], "reasoning_s2": "",
                  "p_agree_s1": r["confidence"], "p_agree_s2": "",
                  "flags": r["flags"]})

    grey = [r for r in p1 if r["status"] == "grey" and r["title"] not in done]
    log.info("%d grey rows to escalate", len(grey))
    eng = Engines(cfg, RawLog(a.raw_log))
    n = [0]

    def work(r: dict) -> None:
        if abort.is_set():
            return
        title = r["title"]
        concern = ("auditor disagreed" if r["verdict"] == "D"
                   else "low agreement confidence")
        flags = [f for f in (r["flags"] or "").split(";") if f]
        row = {"title": title, "label": r["label"], "brandname": r["brandname"],
               "confidence": 0.5, "verdict": "", "phase": 2, "status": "review",
               "reasoning_s1": r["reasoning"], "reasoning_s2": "",
               "p_agree_s1": r["confidence"], "p_agree_s2": ""}
        try:
            cls = eng.classify3(title, prev_json(r), concern)
        except Terminal as exc:
            abort.set()
            log.error("TERMINAL on %r: %s", title, exc)
            return
        except Exception as exc:                          # noqa: BLE001
            log.error("stage2 %r failed: %s", title, exc)
            cls = None
        if cls is None:
            flags.append("stage2_error")
            row["flags"] = ";".join(flags)
            emit(row)
            return
        row.update(label=cls.branding, brandname=cls.brandname,
                   reasoning_s2=cls.reasoning)
        try:
            p, v, anom = eng.verify(title, cls)
        except Terminal as exc:
            abort.set()
            log.error("TERMINAL on %r: %s", title, exc)
            return
        except Exception as exc:                          # noqa: BLE001
            log.error("verify2 %r failed: %s", title, exc)
            flags.append("verify_error")
            row["flags"] = ";".join(flags)
            emit(row)
            return
        if anom:
            flags.append("verifier_anomaly")
            p = 0.5
        if v == "D" and p <= LIKELY_WRONG:
            flags.append("likely_wrong_s2")
        guard = cls.branding == "Branded" and MORPH in cls.reasoning
        if guard:
            flags.append("morphology_guard")
        row.update(confidence=round(p, 4), verdict=v, p_agree_s2=round(p, 4),
                   status="accepted" if (v == "A" and p >= cfg.grey and not guard)
                   else "review",
                   flags=";".join(dict.fromkeys(flags)))
        emit(row)
        with wlock:
            n[0] += 1
            if n[0] % 25 == 0:
                log.info("%d/%d", n[0], len(grey))

    with concurrent.futures.ThreadPoolExecutor(cfg.workers) as pool:
        list(pool.map(work, grey))
    fh.close()

    if abort.is_set():
        log.error("RUN ABORTED on a terminal error (quota/auth). Completed rows "
                  "are saved; fix billing/keys then rerun with --resume.")
        sys.exit(2)

    with open(a.out, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    review = [r for r in rows if r["status"] == "review"]
    with open(a.review, "w", newline="", encoding="utf-8") as rfh:
        rw = csv.DictWriter(rfh, fieldnames=COLS)
        rw.writeheader()
        rw.writerows(review)

    acc1 = sum(1 for r in rows if r["status"] == "accepted" and r["phase"] == "1")
    acc2 = sum(1 for r in rows if r["status"] == "accepted" and r["phase"] == "2")
    ps = [float(r["confidence"]) for r in rows if r["confidence"]]
    hard_d = sum(1 for r in rows if r["verdict"] == "D"
                 and r["p_agree_s2"] and float(r["p_agree_s2"]) <= LIKELY_WRONG)
    print("=" * 60)
    print(f"final: {len(rows)} rows  accepted {acc1 + acc2} "
          f"(phase1 {acc1}, phase2 {acc2})  review {len(review)}")
    print(f"phase-2 high-confidence Disagrees (p_agree <= {LIKELY_WRONG}): {hard_d}")
    print(f"wrote {a.out} and {a.review}")
    print("final confidence histogram:")
    print(hist(ps))


if __name__ == "__main__":
    main()
