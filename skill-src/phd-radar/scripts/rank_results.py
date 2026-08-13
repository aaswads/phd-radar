#!/usr/bin/env python3
"""Deterministically rank a PhD Radar JSON result packet."""

import argparse
import json
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


SCORE_FIELDS = (
    "overall_match_raw",
    "research_fit_raw",
    "eligibility_score_raw",
    "funding_confidence_raw",
)


def _score(item, field):
    value = item.get(field)
    if value is None:
        fallback = field.removesuffix("_raw")
        value = item.get(fallback, 0)
    return Decimal(str(value))


def _deadline_key(value):
    if not value:
        return (1, date.max.isoformat())
    try:
        return (0, date.fromisoformat(value).isoformat())
    except ValueError:
        return (1, date.max.isoformat())


def _sort_key(item):
    descending = tuple(-_score(item, field) for field in SCORE_FIELDS)
    return descending + _deadline_key(item.get("deadline")) + (
        str(item["opportunity_id"]),
    )


def _display_score(value):
    return float(Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def rank_results(items):
    ranked = sorted(items, key=_sort_key)
    for index, item in enumerate(ranked, start=1):
        item["rank"] = index
        for raw_field in SCORE_FIELDS:
            display_field = raw_field.removesuffix("_raw")
            item[display_field] = _display_score(_score(item, raw_field))
    return ranked


def self_test():
    sample = [
        {"opportunity_id": "d", "overall_match_raw": 8.94},
        {"opportunity_id": "b", "overall_match_raw": 9.04},
        {"opportunity_id": "a", "overall_match_raw": 9.06},
        {"opportunity_id": "c", "overall_match_raw": 9.00},
    ]
    ranked = rank_results(sample)
    assert [item["opportunity_id"] for item in ranked] == ["a", "b", "c", "d"]
    assert [item["overall_match"] for item in ranked] == [9.1, 9.0, 9.0, 8.9]

    tied = [
        {"opportunity_id": "b", "overall_match_raw": 8, "deadline": None},
        {"opportunity_id": "a", "overall_match_raw": 8, "deadline": "2026-10-01"},
    ]
    assert [item["opportunity_id"] for item in rank_results(tied)] == ["a", "b"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("rank_results self-test passed")
        return 0
    if args.input is None:
        parser.error("input is required unless --self-test is used")

    payload = json.loads(args.input.read_text(encoding="utf-8-sig"))
    items = payload["results"] if isinstance(payload, dict) else payload
    ranked = rank_results(items)
    output = dict(payload, results=ranked) if isinstance(payload, dict) else ranked
    rendered = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
