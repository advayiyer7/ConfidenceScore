"""
uom_confidence.py — logprob-based confidence scoring for UoM standardization.

Adds a standardized-quantity estimate (`computed_std_qty`) plus a numeric
confidence in [0,1] to each product row of a 3-tier UoM pipeline output CSV.
The confidence is derived from the model's TOKEN LOGPROBS, never from a
self-reported number.

Two-stage logprob mechanic
--------------------------
Stage 1 (estimate, normal completion):
    The row context (title, inferred_raw_unit, inferred_raw_qty, uom_std_unit)
    is sent to the model, which returns a JSON list of 2-4 candidate
    interpretations {std_unit, std_qty, reasoning}, ordered best-first.
    For "piece" items (with PIECE_TO_KG=True) the candidates are plausible
    per-piece weights in kg, e.g. one samosa ~ 0.05 kg.

Stage 2 (select, ~1-token completion WITH logprobs):
    The Stage-1 candidates are presented labelled A, B, C, ... and the model
    is instructed to output ONLY the single letter of the best candidate.
    The call uses logprobs=True, top_logprobs=min(5, max(K, #candidates)).
    Each logprob at the answer position is converted to a probability with
    math.exp; only candidate-letter tokens are kept (absent letters get a
    small epsilon) and the distribution is renormalized to sum to 1.

    confidence   = normalized probability of the top letter
    alternatives = the top-K candidates with their normalized probabilities,
                   populated only when confidence < THRESHOLD

Stage 2 costs a single output token, keeping total cost within ~2x of a
single-call design.

Rows whose title/inferred fields contain an explicit, fully-determining
measurement (e.g. "5L", "60 ml", "30 G x 30 sachet" -> 0.9 kg) are computed
deterministically with no API call: confidence=1.0, source="deterministic".

NOTE: confidence is currently RAW, uncalibrated logprob mass. See calibrate().

Usage:
    python uom_confidence.py --input pipeline_out.csv --output scored.csv \
        [--model gpt-4o] [--threshold 0.70] [--k 2] [--workers 4] \
        [--no-piece-to-kg]
"""

import argparse
import concurrent.futures
import csv
import json
import logging
import math
import os
import random
import re
import string
import sys
import threading
import time

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    OpenAI,
    RateLimitError,
)

# --------------------------------------------------------------------------
# Config (overridable via CLI)
# --------------------------------------------------------------------------
THRESHOLD = 0.70      # below this, emit top-K alternatives
K = 2                 # number of alternatives to emit when below threshold
MODEL = "gpt-4o"
PIECE_TO_KG = True    # piece items: estimate per-piece weight in kg
                      # (False keeps "piece" and estimates count instead)
WORKERS = 4
MAX_RETRIES = 5
EPSILON = 1e-6        # prob floor for candidate letters absent from top_logprobs
LETTERS = string.ascii_uppercase[:5]  # top_logprobs cap is 5 -> at most A..E

NEW_COLUMNS = [
    "computed_std_qty",
    "confidence",
    "confidence_source",
    "alternatives",
    "model_reasoning",
]

log = logging.getLogger("uom_confidence")


# --------------------------------------------------------------------------
# Calibration stub
# --------------------------------------------------------------------------
def calibrate(raw_confidence):
    """Map raw logprob-derived confidence to calibrated probability.

    No-op for now. Once a labeled gold set exists, fit isotonic regression
    or Platt scaling on (raw_confidence, correct) pairs and apply it here.
    """
    return raw_confidence


# --------------------------------------------------------------------------
# Deterministic fast path
# --------------------------------------------------------------------------
# unit token -> (standard unit, factor to standard unit)
_UNIT_MAP = {
    "g": ("kg", 0.001), "gm": ("kg", 0.001), "gms": ("kg", 0.001),
    "gram": ("kg", 0.001), "grams": ("kg", 0.001), "gr": ("kg", 0.001),
    "kg": ("kg", 1.0), "kgs": ("kg", 1.0), "kilo": ("kg", 1.0),
    "kilogram": ("kg", 1.0), "kilograms": ("kg", 1.0),
    "mg": ("kg", 0.000001),
    "ml": ("litre", 0.001), "mls": ("litre", 0.001),
    "l": ("litre", 1.0), "lt": ("litre", 1.0), "ltr": ("litre", 1.0),
    "ltrs": ("litre", 1.0), "litre": ("litre", 1.0), "litres": ("litre", 1.0),
    "liter": ("litre", 1.0), "liters": ("litre", 1.0),
    "pc": ("piece", 1.0), "pcs": ("piece", 1.0), "piece": ("piece", 1.0),
    "pieces": ("piece", 1.0), "pkt": ("piece", 1.0), "nos": ("piece", 1.0),
    "no": ("piece", 1.0), "unit": ("piece", 1.0), "units": ("piece", 1.0),
    "sachet": ("piece", 1.0), "sachets": ("piece", 1.0),
}

_UNIT_ALTS = "|".join(sorted(_UNIT_MAP, key=len, reverse=True))
_NUM = r"(\d+(?:\.\d+)?)"

# "30 G x 30 sachet", "30g x 30", "100ml x 6"
_RE_QTY_UNIT_X_N = re.compile(
    rf"{_NUM}\s*({_UNIT_ALTS})\b\.?\s*[x×*]\s*{_NUM}", re.IGNORECASE)
# "30 x 100 g", "6 x 1L"
_RE_N_X_QTY_UNIT = re.compile(
    rf"{_NUM}\s*[x×*]\s*{_NUM}\s*({_UNIT_ALTS})\b", re.IGNORECASE)
# "5L", "60 ml", "1.5 kg"
_RE_QTY_UNIT = re.compile(rf"{_NUM}\s*({_UNIT_ALTS})\b", re.IGNORECASE)
# "pack of 12"
_RE_PACK_OF = re.compile(rf"pack\s+of\s+{_NUM}", re.IGNORECASE)


def _to_float(value):
    try:
        f = float(str(value).strip())
        return f if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def _norm_unit(unit):
    return _UNIT_MAP.get(str(unit or "").strip().lower().rstrip("."))


def deterministic_qty(title, raw_unit, raw_qty, target_unit):
    """Return explicit quantity in target_unit parsed from the row, or None.

    Tried in priority order: multiplicative title patterns ("30 G x 30"),
    simple title measurements ("5L"), then the inferred unit/qty fields.
    Only a match whose standard unit equals target_unit counts as
    fully-determining.
    """
    title = title or ""

    m = _RE_QTY_UNIT_X_N.search(title)
    if m:
        hit = _norm_unit(m.group(2))
        if hit and hit[0] == target_unit:
            return float(m.group(1)) * hit[1] * float(m.group(3))

    m = _RE_N_X_QTY_UNIT.search(title)
    if m:
        hit = _norm_unit(m.group(3))
        if hit and hit[0] == target_unit:
            return float(m.group(1)) * float(m.group(2)) * hit[1]

    for m in _RE_QTY_UNIT.finditer(title):
        hit = _norm_unit(m.group(2))
        if hit and hit[0] == target_unit:
            return float(m.group(1)) * hit[1]

    if target_unit == "piece":
        m = _RE_PACK_OF.search(title)
        if m:
            return float(m.group(1))

    qty = _to_float(raw_qty)
    hit = _norm_unit(raw_unit)
    if qty is not None and hit and hit[0] == target_unit:
        return qty * hit[1]

    return None


def piece_count(raw_unit, raw_qty):
    """Count of pieces from the inferred fields, defaulting to 1."""
    qty = _to_float(raw_qty)
    if qty is None or qty <= 0:
        return 1.0
    hit = _norm_unit(raw_unit)
    if hit is None or hit[0] == "piece":  # blank/unknown unit: treat as count
        return qty
    return 1.0


# --------------------------------------------------------------------------
# OpenAI plumbing
# --------------------------------------------------------------------------
def call_with_retry(fn):
    """Run fn() with exponential backoff on 429 / 5xx / transient errors."""
    for attempt in range(MAX_RETRIES):
        try:
            return fn()
        except (RateLimitError, APIConnectionError, APITimeoutError) as exc:
            last = exc
        except APIStatusError as exc:
            if exc.status_code < 500:
                raise
            last = exc
        delay = min(60.0, (2 ** attempt) + random.uniform(0, 1))
        log.warning("retryable API error (%s); sleeping %.1fs", last, delay)
        time.sleep(delay)
    return fn()  # final attempt: let any error propagate


def extract_json_list(text):
    """Parse a JSON list out of a completion, tolerating code fences/prose."""
    text = (text or "").strip()
    text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("["), text.rfind("]")
        if start == -1 or end <= start:
            raise ValueError(f"no JSON list found in: {text[:200]!r}")
        parsed = json.loads(text[start:end + 1])
    if isinstance(parsed, dict):  # e.g. {"candidates": [...]}
        for value in parsed.values():
            if isinstance(value, list):
                parsed = value
                break
    if not isinstance(parsed, list):
        raise ValueError(f"expected JSON list, got: {type(parsed).__name__}")
    return parsed


def validate_candidates(raw_list):
    out = []
    for item in raw_list:
        if not isinstance(item, dict):
            continue
        qty = _to_float(item.get("std_qty"))
        unit = str(item.get("std_unit") or "").strip().lower()
        if qty is None or qty <= 0 or not unit:
            continue
        out.append({
            "std_unit": unit,
            "std_qty": qty,
            "reasoning": str(item.get("reasoning") or "").strip(),
        })
    return out[:len(LETTERS)]  # at most 5 (top_logprobs cap)


def stage1_candidates(client, model, row, target_unit, piece_to_kg):
    """Ask for 2-4 candidate interpretations as JSON. One retry on bad JSON."""
    title = row.get("title", "")
    if row.get("uom_std_unit") == "piece" and piece_to_kg:
        goal = ("This item is counted in pieces. Estimate the typical weight "
                "in kg of ONE piece using world knowledge (e.g. one samosa "
                "is about 0.05 kg). Every candidate must use std_unit \"kg\" "
                "and std_qty = weight of a single piece in kg.")
    elif target_unit == "piece":
        goal = ("Estimate how many pieces this product contains. Every "
                "candidate must use std_unit \"piece\".")
    else:
        goal = (f"Estimate the total quantity of this product in "
                f"{target_unit}. Every candidate must use std_unit "
                f"\"{target_unit}\".")

    prompt = (
        "Product row from a grocery catalog:\n"
        f"  title: {title!r}\n"
        f"  inferred_raw_unit: {row.get('inferred_raw_unit') or 'null'}\n"
        f"  inferred_raw_qty: {row.get('inferred_raw_qty') or 'null'}\n"
        f"  uom_std_unit: {row.get('uom_std_unit') or 'null'}\n\n"
        f"{goal}\n\n"
        "Return ONLY a JSON array of 2 to 4 candidate interpretations, "
        "ordered most-likely first. Each element must be exactly:\n"
        '{"std_unit": "<unit>", "std_qty": <number>, '
        '"reasoning": "<one short line>"}\n'
        "Use world knowledge of typical retail quantities; a rough typical "
        "value is acceptable and expected (e.g. a bunch of curry leaves is "
        "roughly 0.025 kg). Return [] ONLY if not even an order-of-magnitude "
        "estimate is possible.")

    messages = [
        {"role": "system",
         "content": "You are an expert at grocery and food product "
                    "measurements. You respond with strict JSON only."},
        {"role": "user", "content": prompt},
    ]

    for attempt in range(2):  # retry once on parse failure
        resp = call_with_retry(lambda: client.chat.completions.create(
            model=model, messages=messages, temperature=0.2, max_tokens=400))
        text = resp.choices[0].message.content
        try:
            candidates = validate_candidates(extract_json_list(text))
            return candidates
        except (ValueError, json.JSONDecodeError) as exc:
            if attempt == 1:
                raise ValueError(f"stage-1 JSON parse failed twice: {exc}")
            messages.append({"role": "assistant", "content": text})
            messages.append({"role": "user",
                             "content": "That was not valid JSON. Return "
                                        "ONLY the JSON array, nothing else."})


def stage2_select(client, model, row, candidates, k):
    """1-token selection with logprobs.

    Returns (norm_probs, raw_probs, chosen_idx) where both prob dicts map
    candidate letter -> probability; norm_probs is renormalized over the
    candidate letters, raw_probs is the unnormalized exp(logprob) mass.
    """
    letters = LETTERS[:len(candidates)]
    lines = [
        f"{letter}. {c['std_qty']} {c['std_unit']} — {c['reasoning']}"
        for letter, c in zip(letters, candidates)
    ]
    prompt = (
        f"Product title: {row.get('title', '')!r}\n"
        "Candidate standardized quantities:\n" + "\n".join(lines) +
        "\n\nWhich candidate is the best interpretation? "
        "Answer with ONLY the single capital letter.")

    resp = call_with_retry(lambda: client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1,
        logprobs=True,
        top_logprobs=min(5, max(k, len(candidates)))))

    content = resp.choices[0].logprobs.content
    if not content:
        raise ValueError("no logprobs returned at answer position")
    top = content[0].top_logprobs

    # exp() each logprob; keep candidate-letter tokens (merging variants
    # like "A" / " A" / "a"); floor missing letters at EPSILON; renormalize.
    raw_probs = {letter: 0.0 for letter in letters}
    for entry in top:
        token = entry.token.strip().upper()
        if token in raw_probs:
            raw_probs[token] += math.exp(entry.logprob)
    for letter in letters:
        if raw_probs[letter] <= 0.0:
            raw_probs[letter] = EPSILON
    total = sum(raw_probs.values())
    norm_probs = {letter: p / total for letter, p in raw_probs.items()}

    chosen_letter = max(norm_probs, key=norm_probs.get)
    return norm_probs, raw_probs, letters.index(chosen_letter)


# --------------------------------------------------------------------------
# Per-row processing
# --------------------------------------------------------------------------
def blank_result(source="none"):
    return {
        "computed_std_qty": "",
        "confidence": "",
        "confidence_source": source,
        "alternatives": "[]",
        "model_reasoning": "",
    }


def process_row(client, row, cfg):
    """Returns (result_dict, api_error_string_or_empty)."""
    target_unit = str(row.get("uom_std_unit") or "").strip().lower()
    piece_as_kg = (target_unit == "piece") and cfg["piece_to_kg"]
    effective_unit = "kg" if piece_as_kg else target_unit

    # 1. Deterministic fast path (no API call).
    if effective_unit:
        qty = deterministic_qty(row.get("title"), row.get("inferred_raw_unit"),
                                row.get("inferred_raw_qty"), effective_unit)
        if qty is not None:
            result = blank_result("deterministic")
            result["computed_std_qty"] = round(qty, 6)
            result["confidence"] = 1.0
            result["model_reasoning"] = "explicit measurement parsed from row"
            return result, ""

    # Pre-existing API errors: don't spend more calls on a known-bad row.
    if str(row.get("api_error") or "").strip():
        return blank_result("none"), ""

    if not target_unit:
        return blank_result("none"), ""

    # 2. Two-stage logprob estimation.
    try:
        candidates = stage1_candidates(
            client, cfg["model"], row, effective_unit, cfg["piece_to_kg"])
        if not candidates:  # model judged the row non-estimable
            return blank_result("none"), ""

        probs, raw_probs, idx = stage2_select(
            client, cfg["model"], row, candidates, cfg["k"])
        if len(candidates) == 1:
            # Degenerate: renormalizing one letter would always yield 1.0,
            # so use the letter's raw (unnormalized) probability instead.
            confidence = min(1.0, raw_probs["A"])
        else:
            confidence = probs[LETTERS[idx]]

        confidence = calibrate(confidence)
        chosen = candidates[idx]

        qty = chosen["std_qty"]
        if piece_as_kg:
            qty *= piece_count(row.get("inferred_raw_unit"),
                               row.get("inferred_raw_qty"))

        result = blank_result("logprob")
        result["computed_std_qty"] = round(qty, 6)
        result["confidence"] = round(confidence, 4)
        result["model_reasoning"] = chosen["reasoning"]

        if confidence < cfg["threshold"] and len(candidates) > 1:
            letters = LETTERS[:len(candidates)]
            ranked = sorted(
                zip(letters, candidates), key=lambda t: probs[t[0]],
                reverse=True)
            result["alternatives"] = json.dumps([
                {"std_unit": c["std_unit"], "std_qty": c["std_qty"],
                 "prob": round(probs[letter], 4)}
                for letter, c in ranked[:cfg["k"]]
            ])
        return result, ""

    except Exception as exc:  # never let one bad row crash the run
        log.error("row %r failed: %s", row.get("title"), exc)
        return blank_result("none"), f"{type(exc).__name__}: {exc}"


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Add logprob-based confidence to UoM standardization.")
    parser.add_argument("--input", required=True, help="input CSV path")
    parser.add_argument("--output", help="output CSV path "
                        "(default: <input>_confidence.csv)")
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--threshold", type=float, default=THRESHOLD)
    parser.add_argument("--k", type=int, default=K)
    parser.add_argument("--workers", type=int, default=WORKERS)
    parser.add_argument("--piece-to-kg", action=argparse.BooleanOptionalAction,
                        default=PIECE_TO_KG,
                        help="estimate per-piece weight in kg for piece items "
                             "(--no-piece-to-kg keeps 'piece' and estimates "
                             "count)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY environment variable is not set")
    client = OpenAI()

    output_path = args.output or re.sub(
        r"\.csv$", "", args.input, flags=re.IGNORECASE) + "_confidence.csv"

    cfg = {
        "model": args.model,
        "threshold": args.threshold,
        "k": args.k,
        "piece_to_kg": args.piece_to_kg,
    }

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    log.info("read %d rows from %s", len(rows), args.input)

    results = [None] * len(rows)
    progress_lock = threading.Lock()
    done_count = [0]

    def worker(index):
        result, err = process_row(client, rows[index], cfg)
        with progress_lock:
            done_count[0] += 1
            if done_count[0] % 25 == 0:
                log.info("processed %d/%d rows", done_count[0], len(rows))
        return index, result, err

    with concurrent.futures.ThreadPoolExecutor(args.workers) as pool:
        for index, result, err in pool.map(worker, range(len(rows))):
            results[index] = (result, err)

    out_fields = fieldnames + [c for c in NEW_COLUMNS if c not in fieldnames]
    if "api_error" not in out_fields:
        out_fields.append("api_error")

    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=out_fields)
        writer.writeheader()
        for row, (result, err) in zip(rows, results):
            out = dict(row)
            out.update(result)
            if err:  # record new failures without clobbering upstream errors
                existing = str(out.get("api_error") or "").strip()
                out["api_error"] = f"{existing}; {err}" if existing else err
            writer.writerow(out)
    log.info("wrote %s", output_path)

    # ---- end-of-run summary -------------------------------------------
    sources = [r["confidence_source"] for r, _ in results]
    confidences = [r["confidence"] for r, _ in results
                   if r["confidence"] != ""]
    below = sum(1 for r, _ in results
                if r["confidence"] != "" and r["confidence"] < args.threshold)
    log.info("summary: %d rows | deterministic=%d | llm=%d | none=%d | "
             "below-threshold(<%.2f)=%d | mean confidence=%s",
             len(rows),
             sources.count("deterministic"),
             sources.count("logprob"),
             sources.count("none"),
             args.threshold, below,
             f"{sum(confidences) / len(confidences):.4f}"
             if confidences else "n/a")


if __name__ == "__main__":
    main()
