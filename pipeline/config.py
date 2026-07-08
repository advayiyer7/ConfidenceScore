import argparse
from dataclasses import dataclass

GREY = 0.85
LIKELY_WRONG = 0.15          # verdict D with p_agree <= this = high-confidence Disagree
MORPH = "morphology-based inference"


@dataclass
class Config:
    e1_model: str = "claude-sonnet-4-6"
    e2_model: str = "gpt-4o"
    e3_model: str = "gpt-5"
    grey: float = GREY
    tpm: int = 30000
    workers: int = 6
    k: int = 1               # verifier repeats; median p_agree
    mock: bool = False


def add_args(ap: argparse.ArgumentParser) -> None:
    d = Config()
    ap.add_argument("--e1-model", default=d.e1_model)
    ap.add_argument("--e2-model", default=d.e2_model)
    ap.add_argument("--e3-model", default=d.e3_model)
    ap.add_argument("--grey", type=float, default=d.grey)
    ap.add_argument("--tpm", type=int, default=d.tpm)
    ap.add_argument("--workers", type=int, default=d.workers)
    ap.add_argument("--k", type=int, default=d.k)
    ap.add_argument("--mock", action="store_true")


def from_args(a: argparse.Namespace) -> Config:
    return Config(e1_model=a.e1_model, e2_model=a.e2_model, e3_model=a.e3_model,
                  grey=a.grey, tpm=a.tpm, workers=a.workers, k=a.k, mock=a.mock)
