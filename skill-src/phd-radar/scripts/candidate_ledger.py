#!/usr/bin/env python3
"""Small SQLite ledger for stable-refresh candidate continuity."""
import argparse, hashlib, json, sqlite3
from datetime import datetime, timezone

SCHEMA = """CREATE TABLE IF NOT EXISTS candidates (opportunity_id TEXT PRIMARY KEY, canonical_url TEXT, official_id TEXT, institution TEXT, title TEXT, status TEXT NOT NULL, content_hash TEXT, first_seen_at TEXT NOT NULL, last_seen_at TEXT NOT NULL, last_verified_at TEXT, rediscovered INTEGER NOT NULL DEFAULT 0, merge_reason TEXT, discovery_channels TEXT NOT NULL DEFAULT '[]', evidence TEXT NOT NULL DEFAULT '{}'); CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);"""
def now(): return datetime.now(timezone.utc).isoformat()
def stable_id(c):
    if c.get("official_id"): return "official:" + str(c["official_id"])
    if c.get("canonical_url"): return "url:" + str(c["canonical_url"])
    raw = "|".join(str(c.get(k, "")).strip().lower() for k in ("institution", "department", "title", "application_cycle"))
    return "hash:" + hashlib.sha256(raw.encode()).hexdigest()[:24]
def init(db):
    with sqlite3.connect(db) as cx: cx.executescript(SCHEMA)
def upsert(db, candidate, channel="unknown", verified=False):
    init(db); t = now(); oid = candidate.get("opportunity_id") or stable_id(candidate); content = hashlib.sha256(json.dumps(candidate, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    with sqlite3.connect(db) as cx:
        old = cx.execute("SELECT content_hash FROM candidates WHERE opportunity_id=?", (oid,)).fetchone()
        status = "verified" if verified else ("updated" if old and old[0] != content else "carried_forward" if old else "new")
        cx.execute("""INSERT INTO candidates(opportunity_id,canonical_url,official_id,institution,title,status,content_hash,first_seen_at,last_seen_at,last_verified_at,rediscovered,merge_reason,discovery_channels,evidence) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(opportunity_id) DO UPDATE SET canonical_url=excluded.canonical_url, official_id=excluded.official_id, institution=excluded.institution, title=excluded.title, status=excluded.status, content_hash=excluded.content_hash, last_seen_at=excluded.last_seen_at, last_verified_at=COALESCE(excluded.last_verified_at,candidates.last_verified_at), rediscovered=1, merge_reason=excluded.merge_reason, discovery_channels=excluded.discovery_channels, evidence=excluded.evidence""", (oid, candidate.get("canonical_url"), candidate.get("official_id"), candidate.get("institution"), candidate.get("title"), status, content, t, t, t if verified else None, 1 if old else 0, "official_update" if old and old[0] != content else "rediscovered" if old else "first_discovery", json.dumps([channel]), json.dumps(candidate, ensure_ascii=False)))
    return oid
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("db"); sub=ap.add_subparsers(dest="action", required=True); sub.add_parser("init"); u=sub.add_parser("upsert"); u.add_argument("candidate", type=argparse.FileType("r", encoding="utf-8")); u.add_argument("--channel", default="unknown"); u.add_argument("--verified", action="store_true"); args=ap.parse_args()
    if args.action == "init": init(args.db); return
    print(upsert(args.db, json.loads(args.candidate.read().lstrip("\ufeff")), args.channel, args.verified))
if __name__ == "__main__": main()
