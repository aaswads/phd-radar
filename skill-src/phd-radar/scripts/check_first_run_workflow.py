#!/usr/bin/env python3
"""Regression check for the first-run automatic dashboard workflow."""

import argparse
from pathlib import Path


REQUIRED_MARKERS = (
    "FIRST_RUN_AUTO_DASHBOARD",
    "save → search → render → serve → open",
    "codex_app__open_in_codex",
    "including zero verified results",
    "legacy profile with no `dashboard` object",
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    skill_file = args.skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    missing = [marker for marker in REQUIRED_MARKERS if marker not in text]
    if missing:
        print("FIRST_RUN_DASHBOARD_MISSING")
        for marker in missing:
            print(f"- {marker}")
        return 1
    print("FIRST_RUN_DASHBOARD_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
