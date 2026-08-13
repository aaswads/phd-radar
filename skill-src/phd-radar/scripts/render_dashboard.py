#!/usr/bin/env python3
"""Render a self-contained, read-only PhD Radar dashboard from JSON."""

import argparse
import json
from pathlib import Path

from rank_results import rank_results


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = ROOT / "assets" / "dashboard-template.html"


def render_dashboard(input_path, output_path, template_path=DEFAULT_TEMPLATE):
    payload = json.loads(Path(input_path).read_text(encoding="utf-8-sig"))
    if isinstance(payload, list):
        payload = {"results": payload}
    if not isinstance(payload, dict) or not isinstance(payload.get("results", []), list):
        raise ValueError("Input must be a JSON object with a results array or a results array")

    payload["results"] = rank_results(payload.get("results", []))
    payload.setdefault("needs_confirmation", [])
    payload["needs_confirmation"] = sorted(
        payload["needs_confirmation"],
        key=lambda item: (
            -float(item.get("overall_match_raw", item.get("overall_match", 0)) or 0),
            str(item.get("opportunity_id", item.get("candidate_id", ""))),
        ),
    )
    payload.setdefault("summary", {})
    payload.setdefault("meta", {})
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    encoded = encoded.replace("</", "<\\/")
    template = Path(template_path).read_text(encoding="utf-8")
    marker = "__PHD_RADAR_DATA__"
    if template.count(marker) != 1:
        raise ValueError("Dashboard template must contain exactly one data marker")
    output = template.replace(marker, encoded)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(output, encoding="utf-8")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    args = parser.parse_args()
    payload = render_dashboard(args.input, args.output, args.template)
    print(f"Rendered {len(payload['results'])} opportunities to {args.output}")


if __name__ == "__main__":
    main()
