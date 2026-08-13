# Conversation contract

Use this reference when translating user conversation into a search request or persistent profile change.

## SearchRequest

Capture:

```yaml
regions: []
institutions: []
topics: []
methods: []
application_domains: []
opportunity_types: []
funding_requirement: salaried_or_fully_funded
applicant_constraints: []
working_languages: []
deadline:
  minimum_days_remaining: null
  include_unknown: false
exclusions: []
source_overrides: []
web_discovery: true
result_target: 20
discovery_candidate_cap: 60
application_routes: [advertised_position, funded_program_route]
institution_screen:
  enabled: true
  provider: QS
  overall_maximum_rank: 300
  subjects: []
  subject_maximum_rank: 100
  subject_preferred_rank: 50
  subject_policy: any_subject_passes
  ranking_year: latest_available
  unranked_policy: manual_review
lab_screen:
  enabled: true
  publication_window_years: 5
  topics: []
  funding_programs: [ERC, MSCA]
  inspect_doctoral_outputs: true
  inspect_alumni_destinations: true
  external_partner_keywords: []
output_language: zh-CN
persistence: saved_default
```

Omit no field silently: use an empty collection, explicit null, saved value, or disclosed default.

## Precedence

1. Current-turn explicit statement.
2. Unambiguous prior-turn statement in the active request.
3. Saved profile.
4. Disclosed default.

On first use, create a proposed `saved_default` profile from the user's answers plus disclosed defaults. Treat “这次/只查/临时/本轮” as `one_off`. Treat “以后/默认/保存/加入我的配置” as a proposed persistent change. Preview first saves and persistent changes and apply only after confirmation.

## Minimum questions

When no saved profile exists, run the onboarding in `onboarding-and-profile.md`; regions and research topics are required. With a saved profile, continue without asking when defaults do not materially alter the search. Ask one focused question when two interpretations would produce substantially different searches.

## Effective-request echo

Before searching, show a compact summary containing regions, topics, opportunity types, funding requirement, language/eligibility constraints, deadline rule, exclusions, configured sources, Web discovery state, institution/subject thresholds, lab-audit scope, and whether the request is one-off.

Completion: every effective value is attributable and the echo matches the actual search plan.
