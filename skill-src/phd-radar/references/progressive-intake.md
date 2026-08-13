# Progressive intake

Use this reference on first use and when a returning profile is incomplete, contradictory, or stale for a new application cycle. The goal is recall: collect enough search vocabulary and application-route flexibility before research begins.

## First use

Run 3–5 short adaptive rounds instead of one large form. Preserve every answer in a draft profile with `intake_complete: false` until the user confirms the final summary.

1. **Field and search taxonomy:** collect primary field, 3–8 subfields, methods, populations/systems, application domains, and adjacent topics the user would accept. Generate a visible synonym map and let the user remove false friends.
2. **Advising model:** confirm `discipline_mode` as `lab_based`, `faculty_based`, or `hybrid`. For lab/hybrid work, ask PI/lab preferences and recruitment signals. For faculty/hybrid work, ask advisor eligibility, committee breadth, intellectual/method fit, languages/archives, and training priorities.
3. **Geography and scale:** collect regions, exclusions, seed institutions/labs, desired formal-result target, and advisors per program. Defaults are 20 formal results, up to 80 unique discovery candidates, and up to 4 advisors per program.
4. **Funding and application routes:** distinguish guaranteed funding from competitive funding routes. Collect tuition-waiver needs, stipend/salary floor when any, international eligibility, target cycle/intakes, deadlines, tests/languages, and whether `needs_confirmation` candidates should be shown. Default: show them separately.
5. **Ranking and delivery:** confirm hard gates versus preferences, QS behavior, outcome priorities, output language, and Dashboard auto-open.

Summarize the final profile in 6–10 bullets. The user's confirmation makes `intake_complete: true` and saves the permanent default profile. Do not begin research while required intake values are missing or contradictory.

## Returning use

Show a compact summary and ask only what changed. Reconfirm only when the application cycle, geography, funding policy, discipline mode, or hard gates changed; otherwise reuse the saved profile immediately. Preserve unchanged values and stable IDs.

## Search vocabulary

Create these internal buckets from the confirmed intake:

- `primary_topics`: exact core research directions;
- `adjacent_topics`: acceptable neighboring directions;
- `methods`: methodological signals;
- `application_domains`: systems or industries;
- `role_terms`: degree/position variants and local-language equivalents;
- `program_terms`: department, program, center, lab, scholarship, fellowship, studentship;
- `advisor_terms`: PI, supervisor, faculty, committee, lab/group leader.

Use the buckets for query expansion without treating every word as a hard AND condition. Match by multiple routes: primary topic, method + domain, or advisor/lab continuity. Record which route discovered each candidate.

Completion: the profile exposes discipline mode, cycle, funding policy, candidate visibility policy, result scale, and a user-approved search taxonomy broad enough to find adjacent valid routes.
