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
    p2 = tmp_path / "p2.csv"
    run_phase1.main(["--mock", "--input", str(tin), "--title-col", "title",
                     "--out", str(p1), "--raw-log", str(tmp_path / "r1.jsonl")])
    run_phase2.main(["--mock", "--input", str(p1), "--opus", "",
                     "--out", str(p2),
                     "--raw-log", str(tmp_path / "r2.jsonl")])
    with open(p1, newline="", encoding="utf-8-sig") as fh:
        phase1 = list(csv.DictReader(fh))
    with open(p2, newline="", encoding="utf-8-sig") as fh:
        phase2 = list(csv.DictReader(fh))
    return phase1, phase2


def test_smoke_end_to_end(tmp_path):
    phase1, phase2 = run_pipeline(tmp_path)
    assert len(phase1) == len(SMOKE)
    by1 = {r["title"]: r for r in phase1}

    for r in phase1:
        assert r["status"] in ("accepted", "grey")
        if r["confidence"]:
            assert 0.0 <= float(r["confidence"]) <= 1.0

    # phase 1: never accept Branded on morphology-only reasoning
    for r in phase1:
        if r["status"] == "accepted" and r["label"] == "Branded":
            assert MORPH not in r["reasoning"], r["title"]

    assert by1["Maggi Noodles 70g"]["status"] == "accepted"
    assert by1["Curry Leaves"]["label"] == "Unbranded"
    assert by1["CHULLA"]["status"] == "grey"

    # phase 2 covers exactly the grey rows
    grey_titles = {r["title"] for r in phase1 if r["status"] == "grey"}
    assert {r["title"] for r in phase2} == grey_titles
    by2 = {r["title"]: r for r in phase2}
    for r in phase2:
        assert r["status"] in ("accepted", "review")
        assert r["web_findings"]

    # web evidence corroborates the Branded call -> accepted with high conf
    chonk = by2["Frozen OG Choc Chip Chonker"]
    assert (chonk["label"], chonk["status"]) == ("Branded", "accepted")
    assert float(chonk["conf_phase2"]) >= 0.85
    # web evidence CONTRADICTS the Unbranded call -> hard disagree, review
    muru = by2["#_# Stirrer - Murukku"]
    assert muru["status"] == "review"
    assert float(muru["conf_phase2"]) <= 0.15
    assert "likely_wrong" in muru["flags"]
    # nothing found -> mid confidence, not zero
    gluten = by2["GLUTEN NB 0121"]
    assert gluten["status"] == "review"
    assert 0.4 <= float(gluten["conf_phase2"]) <= 0.7


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
