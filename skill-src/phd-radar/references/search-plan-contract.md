# SearchPlan and candidate ledger contract

`SearchPlan` is the reproducibility boundary. The same profile snapshot, query-pack version, source registry, and planning date must produce the same canonical plan and `plan_hash`. Search execution may return different pages, but it must preserve the plan's order, IDs, budgets, and terminal statuses.

## SearchPlan required fields

- `schema_version`, `query_pack_version`, `plan_hash`
- `created_at`, `profile_hash`, `profile_snapshot`
- `regions`, `query_families`, `queries`
- `sources`, including `selected`, `status`, and `reason`
- `budgets` and `stop_conditions`
- `mode`: `replay`, `stable_refresh`, or `clean_discovery`

Each query has a stable `query_id`, `region`, `family`, `text`, `language`, `official_domain_hint`, `max_pages`, `max_results`, and terminal `status`. Query order is lexical by region, family order, language, and query ID; never use search-engine rank as the plan order.

## Run modes

- `replay` reads one saved snapshot and performs no new discovery.
- `stable_refresh` reuses eligible ledger candidates, executes the current plan, and re-verifies due or changed official pages.
- `clean_discovery` ignores ledger candidates for discovery, but may still merge verified discoveries into the ledger.

## Candidate lifecycle

`new → verified → carried_forward → updated/reopened → expired/stale/manual_review`.

An absent search hit is not closure evidence. Automatic `expired` requires an official closed, withdrawn, or past-deadline signal. Every merge records `merge_reason`, `discovery_channels`, `first_seen_at`, `last_seen_at`, `last_verified_at`, and a content hash.

## Stability metrics

Runs should report plan hash, source/query completion, new/updated/carried-forward/expired counts, historical rediscovery rate, candidate-set Jaccard similarity, and Top-20 overlap. Explain changes as `official_change`, `source_failure`, `budget_limited`, `new_discovery`, or `score_revision`.
