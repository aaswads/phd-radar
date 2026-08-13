# PhD Radar

**English** | [简体中文](README.zh-CN.md)

PhD Radar is a Codex skill for discovering, verifying, screening, scoring, ranking, and presenting funded or salaried doctoral opportunities. It turns a natural-language request into a bounded search, verifies promising leads on official pages, and produces an auditable shortlist instead of treating search snippets as vacancies.

## What it does

- Saves and reuses a search profile for regions, topics, methods, funding rules, eligibility, and exclusions.
- Searches for both advertised PhD positions and verified funded-program application routes.
- Combines structured source categories with region-specific open-Web discovery.
- Returns to official university, institute, employer, project, or application pages for verification.
- Applies optional QS institution/subject gates and research-group evidence checks.
- Scores verified results on a 0.0-10.0 scale and ranks them deterministically.
- Reports search coverage and exclusions, then optionally creates a self-contained HTML dashboard.

## Install

Clone the repository and copy the skill into your Codex skills directory:

```powershell
git clone https://github.com/aaswads/phd-radar.git
Copy-Item -Recurse .\phd-radar\skill-src\phd-radar "$HOME\.codex\skills\phd-radar"
```

Restart Codex or start a new task so the skill is discovered.

## How to use it

Ask in natural language. Naming the skill is the most explicit option:

> Use PhD Radar to find salaried Human-AI Interaction PhD positions in the Netherlands, Germany, and the Nordic countries.

Useful follow-up requests include:

- `Refresh my PhD Radar results.`
- `Only search Switzerland this time; do not change my saved profile.`
- `Change my default QS overall threshold to 200.`
- `Explain why result 3 ranks above result 4.`
- `Build and open the card dashboard.`
- `Add this public vacancy website as a source: <URL>.`

PhD Radar distinguishes persistent wording such as “from now on”, “default”, or “save this” from one-search wording such as “this time” or “temporarily”. Persistent changes are previewed before they are saved; temporary overrides leave the profile unchanged.

## First-time setup

On the first run, PhD Radar checks for a saved `default` profile. If none exists, it asks for one copyable configuration reply. Two fields are required:

- **Target regions**, such as the Netherlands, Germany, the Nordic countries, or the UK.
- **Research topics**, such as solid-state batteries, electrochemical energy storage, or computational materials science.

It also accepts:

- official QS subject names;
- education and discipline;
- methods and skills;
- application domains;
- language and eligibility constraints;
- earliest start date;
- explicit exclusions;
- a CV, while still requiring target regions and topics.

Example first-time reply:

```text
Target regions: Germany, Netherlands, Belgium, Sweden
Research topics: solid-state batteries, electrochemical energy storage
QS subjects: Materials Sciences; Engineering - Chemical
Background: MSc in Chemical Engineering, graduating June 2027
Methods and skills: electrochemical impedance spectroscopy, materials characterization, Python
Application domains: electric vehicles and grid-scale energy storage
Language constraints: English-speaking positions only
Earliest start: September 2027
Exclude: self-funded positions
```

The completed reply confirms the first save. The skill merges it with executable defaults, writes the profile, reads it back, and shows a compact saved summary. The default state file is:

```text
~/.codex/phd-radar/profile.json
```

You can override the state location with `PHD_RADAR_STATE_DIR`. Personal profiles and generated search results are excluded from this repository.

### Executable defaults

Unless the user changes them, first-time setup uses:

- opportunity types: PhD, doctoral researcher, and doctoral candidate;
- funding: salaried or fully funded only;
- deadline: expired opportunities excluded; unknown deadlines excluded from formal recommendations;
- application routes: advertised positions and verified funded-program routes;
- discovery: source categories plus regional open-Web discovery, followed by official-page verification;
- QS overall gate: rank 300 or better, inclusive;
- QS subject gate: rank 100 or better, inclusive; top 50 preferred; any configured subject may pass;
- unranked institutions: manual review rather than automatic acceptance;
- lab review: the most recent five years, including research continuity, ERC/MSCA evidence, doctoral outputs and destinations, and external collaborations;
- formal result target: 20;
- broad discovery roster: about three candidates per desired result, capped at 60;
- output language: Chinese.

These are starting defaults, not claims about the user. They can be changed conversationally.

## Search sources and verification

The open-source skill does **not** ship with a hidden fixed database or claim exhaustive Internet coverage. It builds a bounded plan for each requested region from the following source categories:

1. **Vacancy sources:** public university and institute job portals, EURAXESS or regional equivalents, and targeted vacancy searches.
2. **Official institution and program pages:** graduate schools, doctoral programs, departments, research centers, and funding pages.
3. **Advisor and lab pages:** official faculty and lab rosters used to identify research and recruiting signals.
4. **Project and funder sources:** official ERC, MSCA, CORDIS, national funder, consortium, and project pages.
5. **Discovery-only sources:** search engines, aggregators, Scholar, dblp, OpenReview, ORCID, DOI/publisher records, and field directories.

The fifth category can surface a lead, but it cannot prove that a funded opening exists. Every promising lead must return to the most specific official vacancy, project, institution, employer, or designated application page. The skill verifies the opening, institution, location, type, status, deadline, funding or salary, eligibility, language, PI/contact, and application link field by field.

Each source or query ends with a visible status such as `success`, `zero_results`, `blocked`, `failed`, `skipped`, or `budget_limited`. A failed or empty source is reported as a coverage limitation, not silently treated as a complete search.

## Screening, scoring, and ranking

Only deduplicated opportunities with an official evidence chain enter formal scoring.

### Scores

Each candidate receives four raw scores from 0.0 to 10.0:

- **Research fit:** topic, research question, methods, application domain, and long-term-direction fit.
- **Eligibility:** degree, discipline, required skills, applicant eligibility, and language fit.
- **Funding confidence:** strength and completeness of salary, contract, stipend, tuition, and funding evidence.
- **Overall match:** the configured weighted recommendation score.

The skill does not impose one universal hidden weighting formula. The overall weighting belongs to the effective configuration and should be disclosed with the result when it matters. Displayed scores use conventional half-up rounding to one decimal; raw values are retained for sorting.

### Hard gates

Scores do not override hard conflicts. An expired deadline, failed funding requirement, explicit ineligibility, unmet required language, or failed configured QS threshold prevents formal recommendation. Unknown facts remain unknown rather than receiving optimistic points.

### Deterministic order

Results are sorted by:

1. unrounded overall match, descending;
2. unrounded research fit, descending;
3. unrounded eligibility, descending;
4. unrounded funding confidence, descending;
5. known valid deadline, earliest first; unknown last;
6. stable opportunity ID, ascending.

This order is reproducible with `scripts/rank_results.py` and remains consistent across the conversation, JSON packet, spreadsheet, and dashboard.

## Results and dashboard

PhD Radar first reports the effective request and coverage: selected and failed sources, Web queries, raw leads, official returns, duplicates, exclusions, verified results, funding confirmations, deadlines, QS outcomes, and incomplete checks. It then presents the ranked shortlist with official and application links. The main findings remain in the conversation, so the dashboard is optional.

When requested, the skill generates a self-contained, read-only HTML dashboard:

```powershell
python .\skill-src\phd-radar\scripts\render_dashboard.py results.json `
  --output .\output\phd-radar-dashboard.html
```

The dashboard provides:

- summary and coverage metrics;
- text, region, minimum-score, QS-outcome, and lab-audit filters;
- ranked cards with title, institution, location, deadline, funding, PI/contact, recommendation reason, warnings, and official links;
- expandable field-level evidence;
- explicit missing-link, unknown-evidence, empty, and partial-coverage states;
- desktop and mobile layouts with no external runtime dependency.

The Web dashboard intentionally displays one overall score, such as `9.1 / 10`. Component scores remain available to the screening and explanation pipeline but are omitted from the card interface to keep decisions readable.

## Scope and safety

PhD Radar searches public information, verifies evidence, and creates local reports. It does not bypass login, CAPTCHA, paywalls, or access controls, and it never submits an application. Vacancy details change; always treat the linked official application page as authoritative before applying.

## Repository layout

```text
skill-src/phd-radar/
|-- SKILL.md
|-- agents/openai.yaml
|-- assets/
|-- examples/
|-- references/
`-- scripts/
```

## Validate

Run the bundled deterministic ranking self-test:

```powershell
python .\skill-src\phd-radar\scripts\rank_results.py --self-test
```

Codex installations include an optional `quick_validate.py` utility under the preinstalled `skill-creator` system skill. It checks Skill packaging rules such as YAML frontmatter, required fields, and folder naming. It is a development-time structure check, not a PhD Radar runtime dependency. Contributors who have that utility installed can run:

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\skill-src\phd-radar
```

## License

[MIT](LICENSE)
