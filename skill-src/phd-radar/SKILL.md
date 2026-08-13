---
name: phd-radar
description: Search, verify, score, rank, summarize, and display funded or salaried doctoral opportunities from natural-language requirements. Use when the user wants to find or refresh PhD vacancies by region or topic, compare verified opportunities, inspect search coverage and statistics, generate or open a card-based results dashboard, change a reusable search profile, or add a public vacancy website. Combine configured sources with region-specific open Web discovery, return to official project or institution pages for verification, and rank verified results on a 0.0–10.0 scale. Route advisor-only research, application writing, outreach drafting, and application submission elsewhere.
---

# PhD Radar

Turn the user's conversation into a bounded doctoral-opportunity search. Treat configured sources and open Web discovery as complementary discovery channels. Admit a Web lead to the ranked result set only after verifying it on an official project, university, department, institute, employer, or officially designated application page.

## Choose the execution surface

Use available public Web search and browser tools directly for one-off discovery and verification. If the active workspace exposes a PhD Radar engine, inspect its help, schemas, and current state before using it; call only interfaces proven by that environment. Never invent a CLI command, database table, API, saved profile, or source registry.

When no persistent state backend exists, complete one-off searches from the conversation. For a requested persistent profile or source change, show the exact proposed record and state clearly that it is not saved until a real writable state location is selected or available.

Completion: every claimed search, saved setting, and registered source corresponds to an actual tool result or readable state artifact.

## Onboard and reuse the user profile

Before resolving a search, check for an existing profile with `python scripts/profile_store.py show`. If it returns `PROFILE_NOT_FOUND`, read [references/onboarding-and-profile.md](references/onboarding-and-profile.md) and run the first-use conversation. Its form states that the completed reply confirms persistence; save that reply merged with executable defaults and read it back. The first configuration becomes the user's persistent `default` profile.

For later searches, start from that profile and apply current-turn overrides. Preview and confirm persistent patches; apply explicit temporary overrides without changing saved state. Read the saved profile back after every write. Never repeat the full onboarding form when a usable profile already exists.

Treat a legacy profile with no `dashboard` object as `dashboard.generate: true` and `dashboard.auto_open: true`. This backward-compatible default does not require a profile rewrite before the next search.

Completion: every search uses a readable saved default or an explicitly disclosed temporary configuration, and the user can change it conversationally.

### FIRST_RUN_AUTO_DASHBOARD

Treat the user's completed first-use form as authorization for the full local read-only workflow. Continue in the same task without waiting for another “开始搜索” or “打开 Dashboard” message. The mandatory first-run sequence is **save → search → render → serve → open**:

1. save and read back the `default` profile;
2. run the search and produce a valid `DashboardPacket`;
3. render the self-contained Dashboard;
4. start or reuse a local static server;
5. call `codex_app__open_in_codex` with the mounted browser URL when that tool is available.

Build and open the Dashboard including zero verified results; in that case show the empty result state plus coverage, source failures, pending leads, and exclusion statistics. If the user explicitly disables `dashboard.auto_open`, still generate the page and return its path without opening it. Do not claim that the Dashboard loaded unless the mounted URL responded successfully and the open action succeeded or was queued.

Completion: the first configuration reply ends with a mounted Dashboard opened in Codex, or with a precise tool/server failure and a usable generated-file path.

## Route the request

- For a first use without a profile, run **Onboard**, then automatically run **Search** and **Build the dashboard** in the same task.
- For a new or one-off search with a profile, run **Search**.
- For “refresh”, reuse the saved profile and apply only explicit current-turn overrides.
- For “以后/默认/保存”, preview the persistent profile delta and apply it only after confirmation.
- For a request to add a site, run **Add a source**.
- After every completed search, run **Build the dashboard** by default. Also run it for explicit “dashboard/网页/卡片展示/打开结果” requests using the latest packet.
- For explanation or comparison, use the existing verified result evidence; search again only when freshness or missing evidence requires it.
- Use another skill for advisor-only discovery, deep advisor background research, application documents, outreach, interviews, or submitting an application.

Read [references/conversation-contract.md](references/conversation-contract.md) when parsing or changing configuration. Read [references/contracts.md](references/contracts.md) before recording or exchanging structured search data.

## Search

### 1. Resolve the effective request

Extract regions, topics, methods, application domains, opportunity types, funding requirements, applicant constraints, language, deadline rules, exclusions, institution/subject ranking thresholds, lab-audit scope, output preferences, and one-off versus persistent intent.

Use the current turn first, then a saved profile, then disclosed defaults. Ask only for a missing value that would materially change the search. Echo a compact effective request before searching.

Read [references/institution-and-lab-screen.md](references/institution-and-lab-screen.md) whenever an institution, subject-ranking, publication-window, grant, doctoral-output, alumni-destination, or external-partner screen is enabled.

Completion: every effective field traces to the user's words, a saved profile, or an explicitly disclosed default; ranking subjects use official labels; no one-off value is persisted.

### 2. Build a two-channel plan for every region

For each target region:

1. Select enabled sources whose region and opportunity capabilities match.
2. Generate bounded open Web queries using English and useful local-language role terms, topic synonyms, funding terms, and official-domain hints.
3. Record why each configured source is selected, skipped, or unavailable.
4. State the query budget and coverage limits. Never claim exhaustive Internet coverage.

Read [references/source-policy.md](references/source-policy.md) for source selection. Read [references/web-discovery-policy.md](references/web-discovery-policy.md) and [references/discovery-funnel.md](references/discovery-funnel.md) before generating Web queries or following discovery leads.

Completion: every region has both a configured-source plan and an open-Web query set; every planned source and query has a bounded scope.

### 3. Discover leads

Run the breadth-first funnel: vacancy sources, institution/program pages, advisor/lab rosters, project/funder sources, then publication/directory expansion. For broad searches, target roughly three unique discovery candidates per requested formal result, capped at 60. Record channel, source/query, URL, title, snippet, discovered time, and terminal status. Treat search snippets, aggregators, news, lab pages, social posts, scholarly directories, and funding pages as leads rather than vacancy proof.

Deep-verify candidates in batches. When a candidate is excluded by QS, funding, deadline, eligibility, or official-return failure, continue from the discovery roster until the requested formal-result target or a documented saturation/budget stop condition is reached. Support both specific advertised positions and verified funded-program application routes when the profile permits them.

Completion: every planned source and query ends as `success`, `zero_results`, `blocked`, `failed`, `skipped`, or `budget_limited`; leads remain separate from verified opportunities; a small final set has a reconciled discovery-to-exclusion funnel.

### 4. Return to official pages

Follow each promising lead to the most specific official vacancy or project page. Verify opportunity existence, institution, region, type, open status, deadline, funding or salary, applicant eligibility, working language, PI/contact, and official application link field by field.

Use `confirmed`, `unknown`, or `conflicting`; preserve discovery and official URLs separately. Prefer the official page when a snippet or aggregator conflicts. Keep unverified vacancy leads out of the ranked result set. Put PI/project/funding signals without a vacancy in a separate research queue.

Read [references/evidence-policy.md](references/evidence-policy.md) for admission and conflict rules.

Completion: every ranked opportunity has a traceable discovery-to-official evidence chain; every other lead is classified as pending, no-official-source, research-signal, duplicate, expired, excluded, or irrelevant.

### 5. Apply institution and lab screens

When enabled, apply the configured three-stage screen in strict order:

1. verify the official QS overall table and edition; apply the inclusive maximum-rank gate;
2. verify each configured official QS subject table and edition; apply the maximum and preferred thresholds;
3. only for pass/manual-review candidates, inspect the PI/lab's recent 3–5 year research continuity, ERC/MSCA evidence, doctoral production and destinations, and named external collaborations.

Keep `pass`, `preferred`, `manual_review`, and `excluded` populations explicit. A failed institution/subject gate is not rescued by a strong PI. Ranking data and lab evidence require source URLs and checked dates. Do not infer absent alumni outcomes, grants, or collaborations from silence.

Completion: each admitted opportunity has a verified gate outcome and a source-backed lab audit or explicit incomplete status; exclusions state the failed threshold and evidence.

### 6. Normalize, deduplicate, and score

Normalize verified opportunities to [references/contracts.md](references/contracts.md). Merge duplicates while retaining all discovery sources and field evidence. Keep objective facts separate from semantic judgments.

Score `research_fit`, `eligibility_score`, `funding_confidence`, and `overall_match` from 0.0 to 10.0. Apply hard gates after scoring. Read [references/scoring-and-grades.md](references/scoring-and-grades.md) before scoring or explaining a grade.

Completion: each result has four auditable scores, gate outcomes, a recommendation explanation, and a stable opportunity ID; duplicates appear once.

### 7. Rank deterministically

Sort verified results by:

1. unrounded `overall_match_raw` descending;
2. `research_fit_raw` descending;
3. `eligibility_score_raw` descending;
4. `funding_confidence_raw` descending;
5. known valid deadline ascending, unknown last;
6. stable opportunity ID ascending.

Display scores rounded to one decimal. Thus 9.1 precedes 9.0. Use [scripts/rank_results.py](scripts/rank_results.py) when a local JSON result packet exists or when cross-output ordering must be reproduced exactly.

Completion: ranks are consecutive and conversation, JSON, Excel, and any dashboard use the same opportunity-ID order.

### 8. Report statistics, then results

Report:

- the effective request and coverage window;
- configured-source selected/success/zero/failed/skipped counts;
- Web query, lead, official-return, no-official-source, pending, and verified-contribution counts by region;
- raw leads, parsed records, duplicates merged, verified formal opportunities, valid deadlines, and confirmed funding counts;
- S/A/B/C and score-band counts;
- new, updated, reopened, and expired counts when history exists;
- failures, unknowns, and coverage gaps.
- QS overall/subject pass, preferred, manual-review, and excluded counts; lab-audit strong/adequate/weak/incomplete counts.

Then show the ranked verified results with rank, grade, overall score, institution, title, PI, region, research/eligibility/funding scores, funding, deadline, QS overall and target-subject status, lab-audit status, discovery channel, official verification page, application link, and recommendation reason.

Distinguish `zero_results` from incomplete coverage. Do not make the user open an artifact to understand the main findings.

Completion: statistics reconcile with the displayed verified result set and explicitly explain incomplete coverage.

## Add a source

Accept a site name, home page, vacancy listing URL, or example vacancy URL.

1. Normalize the domain and URLs; classify the page as a listing, institution site, aggregator, or single vacancy.
2. Check for an existing domain, canonical URL, redirect target, or adapter.
3. Inspect public access rules, listing/detail structure, pagination, stable identifiers, fields, and login or CAPTCHA requirements.
4. Choose API/feed, static adapter, browser-assisted discovery, discovery-only, or unsupported.
5. Perform a small non-persistent sample extraction.
6. Preview the canonical entry URL, capabilities, access method, field coverage, limitations, sample outcome, and proposed status.
7. Persist only after confirmation. Enter as `testing`; enable only after its fixture and contract test pass.
8. If the user asked to continue searching, rebuild the search plan only after enablement succeeds.

Read [references/source-policy.md](references/source-policy.md) before probing or registering a source.

Completion: the source has a unique ID, canonical entry URL, capability labels, access policy, test evidence, and explicit status; a rejected source is not represented as searched.

## Build the dashboard

Read [references/dashboard-contract.md](references/dashboard-contract.md). Confirm that the input packet follows [references/contracts.md](references/contracts.md) and already contains only verified formal opportunities in `results`.

Generate a self-contained page:

```powershell
python scripts/render_dashboard.py <results.json> --output <output/phd-radar-dashboard.html>
```

The renderer reapplies deterministic ranking and embeds all data locally. Mount the output directory with an available local static server, reuse an existing server when possible, and return the local URL. Keep the server and page read-only.

Probe the mounted URL for a successful response, then use `codex_app__open_in_codex` with `{target: {type: "browser", url: mounted_url}}` when available. Opening is part of the default search delivery, not an optional follow-up. If the app-opening tool is unavailable, open the mounted URL with the available browser surface and return a clickable URL.

Inspect the rendered page at desktop and narrow-mobile widths before handoff. Verify card order, filters, empty state, Apply/project/PI links, disabled missing links, evidence expansion, long titles, and partial-coverage warnings. Preserve the main findings in the conversation even when a dashboard is provided.

Completion: the mounted page loads without external dependencies, cards match the ranked opportunity-ID order, every external action is valid or explicitly unavailable, and the user receives the local URL with the page opened automatically unless disabled.

## Authorization

Proceed without extra confirmation for public read-only search, official-page verification, local analysis, and local report creation.

Preview and obtain confirmation before persisting a profile, registering or enabling a source, bulk-changing application state, migrating data, creating an external automation, using a login session, uploading personal material, sending a message, or writing to an external system. Never bypass access controls, CAPTCHA, paywalls, or site restrictions. Never submit an application.
