import csv

from pipeline import run_phase1, run_phase2
from pipeline.config import MORPH

SMOKE = [
    "RED LABEL TEA (1 KG)",
    "CHULLA",
    "#_# Stirrer - Murukku",
    "#_# Mango Biscoff Tub - Sassy Teaspoon",
    "Curry Leaves",
    "ONION LARGE",
    "GLUTEN NB 0121",
    "3CP PLATE",
    "Maggi Noodles 70g",
    "Soda Kinley 750ml",
    "Frozen OG Choc Chip Chonker",
    "EGGS TRAY",
]


def run_pipeline(tmp_path):
    tin = tmp_path / "titles.csv"
    with open(tin, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["title"])
        w.writerows([[t] for t in SMOKE])
    p1 = tmp_path / "p1.csv"
    fin = tmp_path / "final.csv"
    rq = tmp_path / "rq.csv"
    run_phase1.main(["--mock", "--input", str(tin), "--title-col", "title",
                     "--out", str(p1), "--raw-log", str(tmp_path / "r1.jsonl")])
    run_phase2.main(["--mock", "--phase1", str(p1), "--out", str(fin),
                     "--review", str(rq),
                     "--raw-log", str(tmp_path / "r2.jsonl")])
    with open(fin, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    with open(rq, newline="", encoding="utf-8-sig") as fh:
        review = list(csv.DictReader(fh))
    return rows, review


def test_smoke_end_to_end(tmp_path):
    rows, review = run_pipeline(tmp_path)
    assert len(rows) == len(SMOKE)
    by = {r["title"]: r for r in rows}

    for r in rows:
        assert r["status"] in ("accepted", "review")
        if r["confidence"]:
            assert 0.0 <= float(r["confidence"]) <= 1.0

    # the spec's core assertion: never ship Branded on morphology-only reasoning
    for r in rows:
        if r["status"] == "accepted" and r["label"] == "Branded":
            deciding = r["reasoning_s2"] if r["phase"] == "2" else r["reasoning_s1"]
            assert MORPH not in deciding, r["title"]

    # trap-class expectations
    red = by["RED LABEL TEA (1 KG)"]
    assert (red["label"], red["status"], red["phase"]) == ("Branded", "accepted", "2")
    chulla = by["CHULLA"]
    assert (chulla["label"], chulla["status"]) == ("Unbranded", "accepted")
    muru = by["#_# Stirrer - Murukku"]
    assert (muru["label"], muru["status"], muru["phase"]) == ("Branded", "accepted", "2")
    assert by["Maggi Noodles 70g"]["phase"] == "1"
    assert by["Maggi Noodles 70g"]["status"] == "accepted"
    assert by["Curry Leaves"]["label"] == "Unbranded"
    assert by["Frozen OG Choc Chip Chonker"]["status"] == "review"
    assert by["GLUTEN NB 0121"]["status"] == "review"

    review_titles = {r["title"] for r in review}
    assert review_titles == {r["title"] for r in rows if r["status"] == "review"}


def test_phase1_resume_skips_done(tmp_path):
    tin = tmp_path / "titles.csv"
    with open(tin, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["title"])
        w.writerows([[t] for t in SMOKE])
    p1 = tmp_path / "p1.csv"
    args = ["--mock", "--input", str(tin), "--title-col", "title",
            "--out", str(p1), "--raw-log", str(tmp_path / "r1.jsonl")]
    run_phase1.main(args + ["--limit", "5"])
    run_phase1.main(args + ["--resume"])
    with open(p1, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == len(SMOKE)
    assert len({r["title"] for r in rows}) == len(SMOKE)
