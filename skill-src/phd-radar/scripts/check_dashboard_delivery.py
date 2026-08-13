#!/usr/bin/env python3
"""Regression checks for safe links and low-score dashboard disclosure."""

import json
import re
import tempfile
from pathlib import Path

from check_run_packet import check
from render_dashboard import render_dashboard


ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "examples" / "dashboard-sample.json"


def main():
    failures = []
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "dashboard.html"
        render_dashboard(SAMPLE, output)
        html = output.read_text(encoding="utf-8")

    if re.search(r'href="https?://(?:[^"/]+\.)?example\.(?:com|org|net)', html, re.I):
        failures.append("reserved example domain is clickable")
    if 'id="low-score-section"' not in html or '<details class="low-score-section"' not in html:
        failures.append("projects below 8.0 are not in a default-collapsed section")
    if "const DEFAULT_COLLAPSE_BELOW_SCORE = 8" not in html:
        failures.append("the 8.0 collapse threshold is not explicit")

    sample = json.loads(SAMPLE.read_text(encoding="utf-8-sig"))
    low_count = sum(
        float(item.get("overall_match_raw", item.get("overall_match", 0)) or 0) < 8
        for item in sample.get("results", []) + sample.get("needs_confirmation", [])
    )
    if low_count and "low-score-cards" not in html:
        failures.append("low-score projects are omitted instead of retained")

    reserved_packet = {
        "formal_results": [{
            "opportunity_id": "reserved-link-repro",
            "overall_match_raw": 8.5,
            "official_detail_url": "https://example.org/project",
            "official_application_url": "https://example.com/apply",
            "field_evidence": [],
        }],
        "needs_confirmation": [],
        "research_signals": [],
        "excluded": [],
    }
    report = check(reserved_packet)
    if not any(error.get("code") == "reserved_example_url" for error in report["errors"]):
        failures.append("quality gate accepts reserved example domains")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: links are safe and projects below 8.0 remain available in a collapsed section")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
