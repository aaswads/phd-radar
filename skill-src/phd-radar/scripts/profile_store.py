#!/usr/bin/env python3
"""Create, inspect, and patch the local PhD Radar user profile."""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_PROFILE = {
    "profile_name": "default",
    "regions": [],
    "topics": [],
    "methods": [],
    "application_domains": [],
    "opportunity_types": ["PhD", "doctoral researcher", "doctoral candidate"],
    "funding_requirement": "salaried_or_fully_funded",
    "applicant_constraints": [],
    "working_languages": [],
    "deadline": {"minimum_days_remaining": 0, "include_unknown": False},
    "exclusions": [],
    "source_overrides": [],
    "web_discovery": True,
    "result_target": 20,
    "discovery_candidate_cap": 60,
    "application_routes": ["advertised_position", "funded_program_route"],
    "institution_screen": {
        "enabled": True,
        "provider": "QS",
        "overall_maximum_rank": 300,
        "subjects": [],
        "subject_maximum_rank": 100,
        "subject_preferred_rank": 50,
        "subject_policy": "any_subject_passes",
        "ranking_year": "latest_available",
        "unranked_policy": "manual_review",
    },
    "lab_screen": {
        "enabled": True,
        "publication_window_years": 5,
        "topics": [],
        "funding_programs": ["ERC", "MSCA"],
        "inspect_doctoral_outputs": True,
        "inspect_alumni_destinations": True,
        "external_partner_keywords": [],
    },
    "output_language": "zh-CN",
}


def state_file(explicit_dir=None):
    if explicit_dir:
        base = Path(explicit_dir)
    elif os.environ.get("PHD_RADAR_STATE_DIR"):
        base = Path(os.environ["PHD_RADAR_STATE_DIR"])
    else:
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        base = codex_home / "phd-radar"
    return base / "profile.json"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def deep_merge(current, patch):
    result = dict(current)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def validate_profile(profile):
    for field in ("regions", "topics"):
        value = profile.get(field)
        if not isinstance(value, list) or not any(str(item).strip() for item in value):
            raise ValueError(f"{field} must contain at least one value")


def save_profile(path, profile, preserve_created=None):
    now = datetime.now(timezone.utc).isoformat()
    payload = dict(profile)
    payload["schema_version"] = 1
    payload["profile_name"] = payload.get("profile_name", "default")
    payload["created_at"] = preserve_created or payload.get("created_at") or now
    payload["updated_at"] = now
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("path", "defaults", "show", "set", "patch"))
    parser.add_argument("json_file", nargs="?", type=Path)
    parser.add_argument("--state-dir", type=Path)
    args = parser.parse_args()
    target = state_file(args.state_dir)

    if args.action == "path":
        print(target)
        return 0
    if args.action == "defaults":
        print(json.dumps(DEFAULT_PROFILE, ensure_ascii=False, indent=2))
        return 0
    if args.action == "show":
        if not target.exists():
            print("PROFILE_NOT_FOUND")
            return 2
        print(target.read_text(encoding="utf-8"), end="")
        return 0
    if args.json_file is None:
        parser.error("json_file is required for set and patch")

    incoming = read_json(args.json_file)
    if not isinstance(incoming, dict):
        raise ValueError("Profile input must be a JSON object")
    if args.action == "set":
        merged = deep_merge(DEFAULT_PROFILE, incoming)
        validate_profile(merged)
        saved = save_profile(target, merged)
    else:
        if not target.exists():
            raise FileNotFoundError("Cannot patch before the first profile is saved")
        current = read_json(target)
        merged = deep_merge(current, incoming)
        validate_profile(merged)
        saved = save_profile(target, merged, current.get("created_at"))
    print(json.dumps(saved, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
