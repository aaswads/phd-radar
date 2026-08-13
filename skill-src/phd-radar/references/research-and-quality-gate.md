# Research and quality gate

Use this reference after intake for every search run.

## Parallel research slices

When independent execution is available, research these bounded slices in parallel; otherwise execute the same slices sequentially and preserve their separate statuses:

1. program/vacancy discovery by region;
2. current program facts, admissions, deadlines, and funding;
3. eligible PIs/advisors and recent research fit;
4. lab/program outcomes, doctoral production, and external partnerships when requested;
5. independent critical-claim retrieval and reconciliation.

Assign stable IDs based on normalized institutional and route identity. Preserve blocked, failed, stale, and partial slices instead of dropping their candidates.

## Two result tiers

Classify every deduplicated candidate:

- `formal`: a current official vacancy or program application route exists; required funding policy and eligibility pass; material claims are confirmed or explicitly acceptable under the profile. Formal results receive the public rank and 10-point overall score.
- `needs_confirmation`: an official program, scholarship, vacancy, or recruiting/advisor route exists and research fit is plausible, but exactly identified critical facts remain unresolved, such as individual funding award, current PI recruiting, international tuition waiver, or next-cycle deadline. Show separately when enabled. It may receive a provisional overall score labeled as provisional; never mix it into formal ranks and never discard it due to score alone.
- `research_signal`: fitting PI/lab/project exists but no current application route has been located. Keep in the research queue, not the recommendation cards.
- `excluded`: a verified hard gate fails, the route is expired, or the candidate is irrelevant/duplicate.

`not_found`, blocked access, or skipped research is not a negative fact. Use `needs_confirmation` or `research_signal` according to what is positively established.

## Claim-level checks

For every decision-critical field, store the source URL, source kind, effective cycle, retrieval status, checked time, observed value, and supported field path. Reconcile independent evidence as `confirmed`, `corrected`, `conflict`, or `unresolved`. A reachable URL alone is not verification.

Critical fields are route existence, open/intake status, deadline, funding and tuition scope, international eligibility, official application route, PI/advisor eligibility or recruiting when required, and institution/subject gate evidence when enabled. Reserved documentation domains (`example.com`, `example.org`, `example.net`, including subdomains) support no claim and fail the quality gate.

## Run artifact and checker

Write one run packet with `profile_snapshot`, `source_runs`, `discovery_leads`, `formal_results`, `needs_confirmation`, `research_signals`, `excluded`, `quality`, and `summary`. Run `scripts/check_run_packet.py` before Dashboard rendering.

The checker verifies stable/unique IDs, tier separation, URL shape, score ranges, critical field evidence, counts, and exclusion reasons. Errors block “verified” delivery. Warnings remain visible in the Dashboard and run summary.

Completion: every candidate is retained in one terminal tier, formal and provisional results cannot be confused, critical claims have field-level sources, and the run packet passes its structural quality gate.
