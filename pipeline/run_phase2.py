import argparse
import concurrent.futures
import csv
import logging
import os
import re
import sys
import threading
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

from pipeline import config
from pipeline.config import LIKELY_WRONG
from pipeline.engines import Engines, RawLog, Terminal, hist
from pipeline.schemas import Cls

log = logging.getLogger("phase2")
COLS = ["title", "label", "brandname", "conf_phase1", "conf_phase2", "verdict",
        "status", "flags", "opus_label", "web_findings"]
OPUS = "OPUS(BRAND/NO BRAND)"
OPUS_LABEL = {"BRAND": "Branded", "NO BRAND": "Unbranded"}


def flat(text: str, limit: int = 900) -> str:
    t = re.sub(r"\s+", " ", text or "").strip()
    return t[:limit]


def catalog_context(name: str, title: str, titles: list[str]) -> str:
    """Structural corpus evidence: other titles carrying the same name."""
    if not name or name.upper() == "NA" or len(name) < 3:
        return ""
    sibs = [t for t in titles if t != title and name.lower() in t.lower()]
    if not sibs:
        return f"CATALOG CONTEXT: {name!r} appears on no other item in this catalog."
    ex = "; ".join(s[:60] for s in sibs[:5])
    return (f"CATALOG CONTEXT: {name!r} appears on {len(sibs) + 1} items in "
            f"this catalog, e.g.: {ex}")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(
        description="Phase 2: web-research the grey zone, re-verify with "
                    "logprobs on the search findings.")
    ap.add_argument("--input", default="phase1_results.csv")
    ap.add_argument("--opus", default="opus_phase1_results.csv",
                    help="optional file with an OPUS label column to carry "
                         "through for checking")
    ap.add_argument("--out", default="phase2_results.csv")
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

    with open(a.input, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    grey = [r for r in rows if r["status"] == "grey"]
    all_titles = [r["title"] for r in rows]

    opus = {}
    if a.opus and os.path.exists(a.opus):
        for r in csv.DictReader(open(a.opus, encoding="utf-8-sig")):
            if r.get(OPUS):
                opus[r["title"]] = OPUS_LABEL.get(r[OPUS].strip(), "")

    exists = os.path.exists(a.out) and os.path.getsize(a.out) > 0
    if exists and not a.resume:
        sys.exit(f"{a.out} exists — pass --resume to continue it, or delete it")
    done = set()
    if exists:
        with open(a.out, newline="", encoding="utf-8-sig") as fh:
            done = {r["title"] for r in csv.DictReader(fh)}
    todo = [r for r in grey if r["title"] not in done]
    log.info("%d grey rows (%d done, %d to research)", len(grey), len(done),
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
            if n[0] % 10 == 0:
                log.info("%d/%d", n[0], len(todo))

    def work(r: dict) -> None:
        if abort.is_set():
            return
        title = r["title"]
        name = r["brandname"].strip()
        if not name or name.upper() == "NA":
            name = title
        ctx = catalog_context(r["brandname"].strip(), title, all_titles)
        cls = Cls(r["label"], r["brandname"] or "NA", r["reasoning"])
        row = {"title": title, "label": r["label"], "brandname": r["brandname"],
               "conf_phase1": r["confidence"], "conf_phase2": "",
               "verdict": "", "status": "review", "flags": "",
               "opus_label": opus.get(title, ""), "web_findings": ""}
        try:
            findings = eng.research(title, name, ctx)
        except Terminal as exc:
            abort.set()
            log.error("TERMINAL on %r: %s", title, exc)
            return
        except Exception as exc:                          # noqa: BLE001
            log.error("research %r failed: %s", title, exc)
            row.update(flags="research_error",
                       web_findings=flat(f"(research failed: {exc})"))
            emit(row)
            return
        row["web_findings"] = flat(findings)
        try:
            p, v, anom = eng.verify_web(title, cls, findings, ctx)
        except Terminal as exc:
            abort.set()
            log.error("TERMINAL on %r: %s", title, exc)
            return
        except Exception as exc:                          # noqa: BLE001
            log.error("verify %r failed: %s", title, exc)
            row.update(flags="verify_error")
            emit(row)
            return
        flags = []
        if anom:
            flags.append("verifier_anomaly")
            p = 0.5
        if v == "D" and p <= LIKELY_WRONG:
            flags.append("likely_wrong")
        row.update(conf_phase2=round(p, 4), verdict=v,
                   status="accepted" if (v == "A" and p >= cfg.grey)
                   else "review",
                   flags=";".join(flags))
        emit(row)

    with concurrent.futures.ThreadPoolExecutor(cfg.workers) as pool:
        list(pool.map(work, todo))
    fh.close()

    if abort.is_set():
        log.error("RUN ABORTED on a terminal error (quota/auth). Completed "
                  "rows are saved; rerun with --resume.")
        sys.exit(2)

    with open(a.out, newline="", encoding="utf-8-sig") as fh:
        out_rows = list(csv.DictReader(fh))
    out_rows.sort(key=lambda r: float(r["conf_phase2"])
                  if r["conf_phase2"] else -1.0)
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        w.writerows(out_rows)

    acc = [r for r in out_rows if r["status"] == "accepted"]
    rev = [r for r in out_rows if r["status"] == "review"]
    ps = [float(r["conf_phase2"]) for r in out_rows if r["conf_phase2"]]
    print("=" * 60)
    print(f"phase 2: {len(out_rows)} grey rows -> accepted {len(acc)}  "
          f"review {len(rev)}")
    if opus:
        bad = [r for r in acc if r["opus_label"]
               and r["opus_label"] != r["label"]]
        print(f"accepted rows where OPUS disagrees: {len(bad)}")
        for r in bad:
            print(f"  {r['title'][:60]} label={r['label']} "
                  f"opus={r['opus_label']} conf={r['conf_phase2']}")
    print("phase-2 confidence histogram:")
    print(hist(ps))


if __name__ == "__main__":
    main()
