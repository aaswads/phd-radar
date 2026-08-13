# Configured source policy

Use this reference when selecting, probing, adding, enabling, or reporting a vacancy source.

## Capability record

Store source ID, display name, canonical entry URL, domains, regions, opportunity types, disciplinary scope, available fields, access method, access limitations, status, health timestamp, fixture, and contract-test result.

Access methods are `api`, `feed`, `static`, `browser_assisted`, or `discovery_only`. Statuses are `testing`, `enabled`, `disabled`, `blocked`, and `retired`.

## Selection

Select an enabled source when its region and opportunity-type capabilities match the effective request. Record a reason for selected, skipped, and unavailable sources. A successful HTTP response with zero parsed detail pages does not prove coverage.

## Adding a source

Normalize and deduplicate before probing. Inspect only public pages. Determine listing/detail separation, pagination, identifiers, date behavior, and field availability. Run a small non-persistent extraction and preview the proposed record.

Persist only after confirmation. Register as `testing`; enable only when a saved representative fixture and contract test demonstrate stable extraction. A single vacancy page is an example, not a reusable source, unless a stable listing endpoint is found.

Never enable a source that requires bypassing access controls, cannot map critical fields reliably, duplicates an existing source, or conflicts with site restrictions. Use `discovery_only` when it can surface leads but cannot support objective claims.

Completion: every enabled source has a capability record, access policy, recent fixture, passing contract test, and explicit health state.

