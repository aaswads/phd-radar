#!/usr/bin/env python3
"""Validate tier separation and core provenance in a PhD Radar run packet."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


TIERS = ("formal_results", "needs_confirmation", "research_signals", "excluded")
CRITICAL_FIELDS = ("official_detail_url", "official_application_url")
LINK_FIELDS = CRITICAL_FIELDS + ("pi_profile_url",)
RESERVED_HOSTS = {"example.com", "example.org", "example.net"}


def valid_url(value):
    parsed = urlparse(value or "")
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc) and not reserved_example_url(value)


def reserved_example_url(value):
    host = (urlparse(value or "").hostname or "").lower().rstrip(".")
    return host in RESERVED_HOSTS or any(host.endswith(f".{name}") for name in RESERVED_HOSTS)


def check(packet):
    errors, warnings = [], []
    seen = {}
    for tier in TIERS:
        rows = packet.get(tier, [])
        if not isinstance(rows, list):
            errors.append({"code": "tier_not_array", "path": tier})
            continue
        for index, row in enumerate(rows):
            path = f"{tier}[{index}]"
            candidate_id = row.get("opportunity_id") or row.get("candidate_id")
            if not candidate_id:
                errors.append({"code": "missing_stable_id", "path": path})
            elif candidate_id in seen:
                errors.append({"code": "candidate_in_multiple_tiers", "path": path, "first": seen[candidate_id]})
            else:
                seen[candidate_id] = path
            if tier in {"formal_results", "needs_confirmation"}:
                score = row.get("overall_match_raw", row.get("overall_match"))
                if not isinstance(score, (int, float)) or not 0 <= score <= 10:
                    errors.append({"code": "invalid_overall_score", "path": path})
                for field in LINK_FIELDS:
                    if reserved_example_url(row.get(field)):
                        errors.append({"code": "reserved_example_url", "path": f"{path}.{field}"})
                for evidence_index, evidence in enumerate(row.get("field_evidence", [])):
                    if isinstance(evidence, dict) and reserved_example_url(evidence.get("source_url")):
                        errors.append({"code": "reserved_example_url", "path": f"{path}.field_evidence[{evidence_index}].source_url"})
            if tier == "formal_results":
                for field in CRITICAL_FIELDS:
                    if not valid_url(row.get(field)):
                        errors.append({"code": "missing_official_route", "path": f"{path}.{field}"})
                evidence_fields = {item.get("field") for item in row.get("field_evidence", []) if isinstance(item, dict)}
                for field in ("deadline", "funding"):
                    if field not in evidence_fields:
                        warnings.append({"code": "critical_evidence_missing", "path": path, "field": field})
            if tier == "needs_confirmation" and not row.get("unresolved_critical_fields"):
                errors.append({"code": "provisional_without_gap", "path": path})
            if tier == "needs_confirmation" and not any(valid_url(row.get(field)) for field in CRITICAL_FIELDS):
                errors.append({"code": "missing_official_route", "path": path})
            if tier == "excluded" and not row.get("exclusion_reason"):
                errors.append({"code": "excluded_without_reason", "path": path})
    return {"valid": not errors, "errors": errors, "warnings": warnings, "counts": {tier: len(packet.get(tier, [])) if isinstance(packet.get(tier, []), list) else 0 for tier in TIERS}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    packet = json.loads(args.input.read_text(encoding="utf-8-sig"))
    report = check(packet)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if not report["valid"] or (args.strict and report["warnings"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
