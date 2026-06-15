"""selfreport_confidence.py — the baseline the logprob method is meant to beat.

Instead of deriving confidence from token logprobs, this asks the model to
*tell us* how confident it is: a single call returns the standardized quantity
AND a self-reported (a.k.a. verbalized) confidence in [0,1]. This is the
naive approach LLMs are known to mis-calibrate — they tend to report round,
inflated numbers (0.9, 0.95) regardless of true uncertainty.

It mirrors uom_confidence.py exactly except for the confidence mechanism:
- identical deterministic fast path (explicit measurements -> 1.0, no API call)
- identical piece->kg handling
so a side-by-side comparison isolates the difference to logprob vs. self-report.

Output columns match uom_confidence.py (computed_std_qty, confidence,
confidence_source, alternatives, model_reasoning) plus any input columns such
as `brand`, so brand_analysis.py and compare_confidence.py run on it directly.

Usage:
    python selfreport_confidence.py --input newtest_prepared.csv \
        --output newtest_selfreport.csv [--model gpt-4o] [--workers 4]
"""

import argparse
import concurrent.futures
import csv
import json
import logging
import os
import re
import sys
import threading

from openai import OpenAI

from uom_confidence import (
    NEW_COLUMNS,
    blank_result,
    call_with_retry,
    deterministic_qty,
    extract_json_list,
    piece_count,
    _to_float,
)

log = logging.getLogger("selfreport_confidence")


def selfreport_estimate(client, model, row, target_unit, piece_to_kg):
    """One call: best std_qty + a self-reported confidence in [0,1]."""
    title = row.get("title", "")
    if row.get("uom_std_unit") == "piece" and piece_to_kg:
        goal = ("This item is counted in pieces. Estimate the typical weight "
                "in kg of ONE piece using world knowledge (e.g. one samosa is "
                "about 0.05 kg). Use std_unit \"kg\" and std_qty = weight of a "
                "single piece in kg.")
    elif target_unit == "piece":
        goal = ("Estimate how many pieces this product contains. Use "
                "std_unit \"piece\".")
    else:
        goal = (f"Estimate the total quantity of this product in "
                f"{target_unit}. Use std_unit \"{target_unit}\".")

    prompt = (
        "Product row from a grocery catalog:\n"
        f"  title: {title!r}\n"
        f"  inferred_raw_unit: {row.get('inferred_raw_unit') or 'null'}\n"
        f"  inferred_raw_qty: {row.get('inferred_raw_qty') or 'null'}\n"
        f"  uom_std_unit: {row.get('uom_std_unit') or 'null'}\n\n"
        f"{goal}\n\n"
        "Then state how confident you are that your std_qty is correct, as a "
        "number from 0 to 1 (1 = certain). Return ONLY this JSON object:\n"
        '{"std_unit": "<unit>", "std_qty": <number>, '
        '"confidence": <0-1>, "reasoning": "<one short line>"}')

    messages = [
        {"role": "system",
         "content": "You are an expert at grocery and food product "
                    "measurements. You respond with strict JSON only."},
        {"role": "user", "content": prompt},
    ]
    resp = call_with_retry(lambda: client.chat.completions.create(
        model=model, messages=messages, temperature=0.2, max_tokens=200))
    text = resp.choices[0].message.content

    # The prompt asks for a single object; tolerate it arriving wrapped in a
    # list or fenced, reusing the same lenient extraction as stage 1.
    text_stripped = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", (text or "").strip())
    try:
        obj = json.loads(text_stripped)
    except json.JSONDecodeError:
        obj = extract_json_list(text)
    if isinstance(obj, list):
        obj = obj[0] if obj else {}

    qty = _to_float(obj.get("std_qty"))
    conf = _to_float(obj.get("confidence"))
    if qty is None or qty <= 0 or conf is None:
        raise ValueError(f"bad self-report payload: {text_stripped[:200]!r}")
    return qty, max(0.0, min(1.0, conf)), str(obj.get("reasoning") or "").strip()


def process_row(client, row, cfg):
    target_unit = str(row.get("uom_std_unit") or "").strip().lower()
    piece_as_kg = (target_unit == "piece") and cfg["piece_to_kg"]
    effective_unit = "kg" if piece_as_kg else target_unit

    # Identical deterministic fast path to uom_confidence.py.
    if effective_unit:
        qty = deterministic_qty(row.get("title"), row.get("inferred_raw_unit"),
                                row.get("inferred_raw_qty"), effective_unit)
        if qty is not None:
            result = blank_result("deterministic")
            result["computed_std_qty"] = round(qty, 6)
            result["confidence"] = 1.0
            result["model_reasoning"] = "explicit measurement parsed from row"
            return result, ""

    if str(row.get("api_error") or "").strip() or not target_unit:
        return blank_result("none"), ""

    try:
        qty, conf, reasoning = selfreport_estimate(
            client, cfg["model"], row, effective_unit, cfg["piece_to_kg"])
        if piece_as_kg:
            qty *= piece_count(row.get("title"), row.get("inferred_raw_unit"),
                               row.get("inferred_raw_qty"))
        result = blank_result("self_report")
        result["computed_std_qty"] = round(qty, 6)
        result["confidence"] = round(conf, 4)
        result["model_reasoning"] = reasoning
        return result, ""
    except Exception as exc:
        log.error("row %r failed: %s", row.get("title"), exc)
        return blank_result("none"), f"{type(exc).__name__}: {exc}"


def main():
    parser = argparse.ArgumentParser(
        description="Self-reported (verbalized) confidence baseline.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--piece-to-kg", action=argparse.BooleanOptionalAction,
                        default=True)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY environment variable is not set")
    client = OpenAI()

    output_path = args.output or re.sub(
        r"\.csv$", "", args.input, flags=re.IGNORECASE) + "_selfreport.csv"
    cfg = {"model": args.model, "piece_to_kg": args.piece_to_kg}

    with open(args.input, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    log.info("read %d rows from %s", len(rows), args.input)

    results = [None] * len(rows)
    lock, done = threading.Lock(), [0]

    def worker(index):
        result, err = process_row(client, rows[index], cfg)
        with lock:
            done[0] += 1
            if done[0] % 25 == 0:
                log.info("processed %d/%d rows", done[0], len(rows))
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
            if err:
                existing = str(out.get("api_error") or "").strip()
                out["api_error"] = f"{existing}; {err}" if existing else err
            writer.writerow(out)
    log.info("wrote %s", output_path)

    confs = [r["confidence"] for r, _ in results if r["confidence"] != ""]
    log.info("summary: %d rows | self_report=%d | mean self-reported conf=%s",
             len(rows),
             sum(1 for r, _ in results if r["confidence_source"] == "self_report"),
             f"{sum(confs) / len(confs):.4f}" if confs else "n/a")


if __name__ == "__main__":
    main()
