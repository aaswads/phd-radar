#!/usr/bin/env python3
"""Compile a profile into a deterministic, inspectable SearchPlan."""
import argparse, hashlib, json
from datetime import date
from pathlib import Path

QUERY_PACK_VERSION = "1"
FAMILY_ORDER = ["exact_topic", "synonym", "method_domain", "doctoral_terms", "funding", "project_funder", "official_pages", "regional_platform", "source_discovery"]
FUNDING_TERMS = ["funded", "salaried", "studentship", "scholarship", "salary"]
ROLE_TERMS = ["PhD position", "doctoral researcher", "doctoral candidate", "funded PhD"]

def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def digest(value):
    return hashlib.sha256(canon(value).encode()).hexdigest()

def terms(profile):
    topics = [str(x).strip() for x in profile.get("topics", []) if str(x).strip()]
    methods = [str(x).strip() for x in profile.get("methods", []) if str(x).strip()]
    domains = [str(x).strip() for x in profile.get("application_domains", []) if str(x).strip()]
    return topics, methods, domains

def make_queries(profile):
    queries = []
    topics, methods, domains = terms(profile)
    for region in sorted(str(x).strip() for x in profile.get("regions", []) if str(x).strip()):
        local = profile.get("local_role_terms", {}).get(region, [])
        groups = {
            "exact_topic": [f'"{t}" (PhD OR doctoral) {region}' for t in topics],
            "synonym": [f'{t} doctorate {region}' for t in topics],
            "method_domain": [f'{m} {d} PhD {region}' for m in methods for d in domains] or [f'{m} PhD {region}' for m in methods],
            "doctoral_terms": [f'{role} {t} {region}' for role in ROLE_TERMS for t in topics],
            "funding": [f'{t} {f} PhD {region}' for t in topics for f in FUNDING_TERMS],
            "project_funder": [f'{t} project doctoral funding {region}' for t in topics],
            "official_pages": [f'site:.edu {t} doctoral position {region}' for t in topics],
            "regional_platform": [f'{t} PhD vacancy {region}' for t in topics],
            "source_discovery": [f'{region} official doctoral vacancy portal {t}' for t in topics],
        }
        if local:
            groups["doctoral_terms"] += [f'{role} {t}' for role in local for t in topics]
        for family in FAMILY_ORDER:
            for text in sorted(set(groups[family])):
                qid = digest({"region": region, "family": family, "text": text})[:16]
                queries.append({"query_id": qid, "region": region, "family": family, "text": text, "language": "local" if text in local else "en", "official_domain_hint": None, "max_pages": 3, "max_results": 10, "status": "planned"})
    return queries

def compile_plan(profile, registry=None, mode="stable_refresh", planning_date=None):
    planning_date = planning_date or date.today().isoformat()
    snapshot = json.loads(json.dumps(profile, ensure_ascii=False, sort_keys=True))
    sources = []
    for item in sorted(registry or [], key=lambda x: (x.get("id", ""), x.get("entry_url", ""))):
        regions = set(item.get("regions", []))
        selected = not regions or bool(regions.intersection(snapshot.get("regions", [])))
        sources.append({"id": item.get("id"), "entry_url": item.get("entry_url"), "selected": selected, "status": item.get("status", "unknown"), "reason": "region_and_capability_match" if selected else "region_not_requested"})
    body = {"schema_version": 1, "query_pack_version": QUERY_PACK_VERSION, "created_at": planning_date, "profile_hash": digest(snapshot), "profile_snapshot": snapshot, "mode": mode, "regions": sorted(snapshot.get("regions", [])), "query_families": FAMILY_ORDER, "queries": make_queries(snapshot), "sources": sources, "budgets": {"result_target": snapshot.get("result_target", 20), "candidate_target": max(80, len(snapshot.get("regions", [])) * 40), "max_queries_per_region": len(FAMILY_ORDER) * 20}, "stop_conditions": {"required_families": FAMILY_ORDER, "require_source_terminal_state": True, "expansion_batches": 3, "min_new_official_domains": 1}}
    body["plan_hash"] = digest(body)
    return body

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("profile", type=Path)
    ap.add_argument("--registry", type=Path)
    ap.add_argument("--mode", choices=("replay", "stable_refresh", "clean_discovery"), default="stable_refresh")
    ap.add_argument("--date", default=None)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    profile = json.loads(args.profile.read_text(encoding="utf-8-sig"))
    registry = json.loads(args.registry.read_text(encoding="utf-8-sig")) if args.registry else []
    result = compile_plan(profile, registry, args.mode, args.date)
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); print(result["plan_hash"])
if __name__ == "__main__": main()
