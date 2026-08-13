# Data contracts

Use these logical contracts regardless of the storage or tool implementation. Preserve unknown values rather than inventing them.

## Opportunity

Required fields:

- `opportunity_id`: stable identifier.
- `title`, `institution`, `department`, `country`, `city`.
- `opportunity_type`, `pi_or_contact`.
- `pi_profile_url` and `pi_summary` when officially available.
- `official_detail_url`, `official_application_url`.
- `discovery_urls[]`, each with channel and discovered time.
- `deadline`, `open_status`, `working_languages`.
- `salary_text`, `funding_text`, `employment_or_studentship_type`.
- `international_eligibility` and `requirements_text`.
- `field_evidence[]`.
- `content_hash`, `first_seen`, `last_seen`.
- `research_fit_raw`, `eligibility_score_raw`, `funding_confidence_raw`, `overall_match_raw`.
- displayed one-decimal scores, `grade`, gate outcomes, reasons, concerns, rank.
- `institution_screen` with provider, edition, overall and subject evidence, gate outcome, and exclusion reason.
- `lab_screen` with configured review window, dimension statuses, source-backed findings, coverage limits, and overall audit status.

## FieldEvidence

```yaml
field: deadline
status: confirmed | unknown | conflicting
value: null
source_url: https://official.example/position
source_kind: official_vacancy | official_institution | official_project | official_funder
excerpt: short supporting text
checked_at: ISO-8601
```

## DiscoveryLead

Keep `lead_id`, region, query/source, result URL, title, snippet, discovered time, inferred type, official-return status, and linked opportunity ID. A lead is not an opportunity.

## SourceRun

Use terminal status `success`, `zero_results`, `blocked`, `failed`, `skipped`, or `budget_limited`. Record raw hits, parsed records, contributed unique opportunities, error summary, and coverage notes.

## RunSummary

Keep effective request, start/end time, selected sources, Web queries by region, all source/query terminal states, lead and official-return counts, deduplication counts, verified result counts, score/grade bands, changes, pending evidence, and coverage gaps.

## DashboardPacket

Use a JSON object with `meta`, `summary`, `results`, and `needs_confirmation`. `meta` may carry title, subtitle, generated time, coverage label, footer, and `collapse_below_score`. `summary` carries already reconciled counts. `results` carries ranked verified `Opportunity` records only. `needs_confirmation` carries promising official routes with named unresolved critical fields and provisional scores; it never shares formal ranks. Both arrays retain worthwhile candidates below the configured collapse threshold for the Dashboard's collapsed section. See `dashboard-contract.md` for card behavior.

## RunPacket

Store `profile_snapshot`, `source_runs`, `discovery_leads`, `formal_results`, `needs_confirmation`, `research_signals`, `excluded`, `quality`, and `summary`. Each candidate appears in exactly one terminal tier. Run `scripts/check_run_packet.py` before building the Dashboard.

## Invariants

- One verified opportunity has one stable ID and may retain many discovery sources.
- Objective evidence and semantic scores remain separate.
- Discovery leads without official verification never receive a formal rank.
- `needs_confirmation` candidates remain visible but never enter the formal ranked sequence.
- Opportunities that fail a configured institution or subject gate never receive a formal rank; `manual_review` items remain separate.
- Counts reconcile from raw leads through deduplicated verified opportunities.
- All outputs preserve the same ranked opportunity-ID sequence.
