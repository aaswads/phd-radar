# Broad discovery funnel

Use this reference for every search when the verified result set could be reduced by ranking gates, funding requirements, or lab-audit depth.

## Coverage target

Read `result_target` from the profile; default to 20. For a broad regional or multi-school search, build a discovery roster of roughly `result_target * 3`, capped at 60 unique candidates. For one named institution, cover the complete plausible official roster rather than padding to a quota. Targets guide effort; they are not promised result counts.

Do not stop after the first few verified matches. Continue until one of these is true:

- the verified, gate-passing result target is reached;
- every planned query/source has a terminal state and new variants yield only duplicates for two consecutive query batches;
- the configured time/query budget is exhausted;
- remaining leads are outside the user's hard constraints.

If a candidate fails QS, funding, deadline, eligibility, or official verification, continue drawing from the discovery roster. Report the shortfall and exclusion funnel instead of silently returning a small list.

## Breadth-first passes

Run low-cost discovery before deep verification:

1. **Vacancy pass:** configured vacancy sources, university job portals, EURAXESS or regional equivalents, and targeted open Web queries.
2. **Institution/program pass:** official doctoral-program, graduate-school, department, research-center, and funding pages matching the target field.
3. **Advisor/lab pass:** official faculty/lab rosters plus current personal/lab pages; record recruiting signals and representative recent work only.
4. **Project/funder pass:** official ERC, MSCA, CORDIS, national funder, consortium, and project pages that may lead back to recruiting institutions or PIs.
5. **Publication/directory expansion:** use Scholar, dblp, OpenReview, ORCID, DOI/publisher records, and field directories to discover current researchers; return to official institution/program/vacancy pages before formal admission.

Keep the breadth pass cheap: identity, institution, department, official homepage, high-level topic, recruiting signal, discovery URL, and likely application route. Defer deadlines, complete funding terms, QS gates, eligibility, full lab audit, and claim reconciliation until shortlist admission.

## Query expansion

For every region, cross a bounded selection—not a full Cartesian product—of:

- role synonyms: PhD position, doctoral researcher, doctoral candidate, doctoral student, research assistant with PhD option, studentship, graduate research position, and local-language equivalents;
- topic taxonomy: exact user phrases, parent fields, adjacent concepts, methods, and application domains;
- route terms: vacancy, jobs, apply, admissions, funded, scholarship, studentship, project, lab, group, recruitment;
- official-domain hints and known institution/funder domains.

Generate at least one exact-topic query, one synonym-expanded query, one method/application query, one local-language role query, and one project/funder query per region. Record which variants contributed new official domains.

## Shortlist and deep pass

Deduplicate candidates by normalized institution + opportunity/program identity and stable IDs. Rank the broad pool by cheap relevance only to choose verification order; do not publish that preliminary order or score.

Deep-verify enough candidates to reach the formal target or a stop condition. For each candidate, perform official return, QS screening, funding/deadline/eligibility checks, PI/program mapping, recent-research profiling, and lab audit. Preserve excluded candidates and exact reasons.

When the profile permits both routes, distinguish:

- `advertised_position`: a specific current opening with an official vacancy/application page;
- `funded_program_route`: a current doctoral program/application route with official funding and advisor/program evidence, but no single vacancy advert.

Never represent a lab page or interesting PI alone as an open funded opportunity. Keep it as a research signal until a valid application route is verified.

## Coverage report

Report the funnel: raw leads → unique candidates → official returns → QS pass/manual review/excluded → funding/eligibility pass → deep audits → formal recommendations. Include candidates not deep-checked because of budget and every failed/blocked source batch.

Completion: discovery breadth is measured against a target, excluded candidates trigger replacement discovery, and a small final set is explained by a reconciled funnel rather than early stopping.
