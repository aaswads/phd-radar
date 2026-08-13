# Evidence policy

Use this reference to decide whether a lead may enter the formal ranked result set.

## Source hierarchy

Prefer, in order:

1. Official vacancy or doctoral-project detail page.
2. Official university, department, institute, employer, or designated application page.
3. Official project consortium page.
4. Official funder database or award notice for funding/project facts.

Search results, aggregators, caches, news, lab descriptions, social media, and third-party summaries are discovery evidence only.

## Field decisions

- `confirmed`: an official source directly supports the value.
- `unknown`: no official source supports a value.
- `conflicting`: current sources disagree; retain both and identify the preferred authoritative source.

Verify title, institution, location, opportunity type, open status, deadline, funding/salary, eligibility, language, PI/contact, and application link separately. Never infer one field from another.

## Formal admission

Admit a record to formal results only when an official page proves a real doctoral opportunity and supplies an official or officially designated application route. If open status is unknown, keep it visibly unknown and exclude it when the user requires confirmed-open opportunities. Never score a lead whose vacancy existence is unverified.

Route a PI, grant, lab, or project signal without a vacancy to the research queue. Route a promising vacancy lead without an official page to pending verification.

## Conflicts and freshness

Prefer a current official detail page over a search snippet or aggregator. Preserve the conflict and checked time. If the content hash changes, invalidate dependent semantic decisions and re-review them.

Completion: every objective value in a ranked result has field-level official evidence or an explicit unknown/conflicting state.

