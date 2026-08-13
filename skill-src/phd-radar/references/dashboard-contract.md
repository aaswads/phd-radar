# Dashboard contract

Use this reference after every completed search and when the user asks to generate, mount, open, or change the results dashboard.

## Purpose

Present verified opportunities as a read-only decision surface. Optimize for answering: which opportunity should I inspect first, why is it recommended, who is the relevant PI, and where are the official project and application pages?

## Required card fields

- consecutive rank and `overall_match` on the 10-point scale;
- project title, institution, department, country/city, opportunity type, deadline, and funding text;
- recommended PI/contact and concise PI relevance summary;
- recommendation reason and material warning chips;
- official vacancy/project page;
- official application page;
- official PI profile page when available;
- expandable field-level evidence.
- QS overall and configured subject ranks with edition/year and gate outcome;
- lab-audit status plus recent-research, ERC/MSCA, doctoral-output/destination, and external-collaboration signals.

Use `unknown` or a disabled action when a URL or fact is absent. Never invent a PI profile or application URL.

## Page hierarchy

1. Run identity and effective search scope.
2. Search/verification summary metrics.
3. Filters for text, region, minimum score, QS gate outcome, and lab-audit status.
4. Cards in the exact deterministic rank order.
5. A visually separate `needs_confirmation` section with provisional scores and named evidence gaps for items at or above the collapse threshold.
6. A default-collapsed “其他值得查看的项目” section containing every worthwhile formal or provisional item below the configured threshold, default `8.0`.
7. Coverage and freshness disclaimer.

Keep charts optional. Prefer directly actionable counts and cards over decorative analytics.

Project content owns the page. Do not display S/A/B/C grades or component research/eligibility/funding scores. These remain available to the screening and ranking pipeline but the Web surface shows only one overall score such as `9.1 / 10`.

## Behavior

- Default to numeric recommendation order; filtering never changes relative order.
- Open external links in a new tab with `noopener noreferrer`.
- Keep the dashboard read-only. Application-state writes belong to a separately confirmed control surface.
- Render loading, empty, missing-link, unknown-evidence, and partial-coverage states explicitly.
- Preserve the same opportunity-ID order as conversation, JSON, and Excel outputs.
- Never merge provisional candidates into the formal ranked sequence; label their score `暂定匹配分` and show unresolved critical fields.
- Treat score as presentation priority, not a deletion rule. Preserve every worthwhile official-route candidate; place scores below `dashboard.collapse_below_score` in the collapsed section and maintain deterministic descending order there.
- Accept only real `http` or `https` official URLs. Disable absent actions and reject `example.com`, `example.org`, `example.net`, or their subdomains. Never use the sample fixture as a user result packet.

## Visual system

Use a neutral cool background, white/dark adaptive surfaces, one restrained teal accent, 16px card radius, subtle tinted shadows, high contrast, and compact typography. Use a desktop filter rail with a two-column workspace and collapse to a single column on mobile. Respect reduced motion and keyboard focus.

## Generation and mounting

Generate a self-contained page with:

```powershell
python scripts/render_dashboard.py results.json --output output/phd-radar-dashboard.html
```

Mount the containing directory with an available local static server, for example:

```powershell
python -m http.server 8765 --directory output
```

Reuse an already-running server when possible. The server is read-only by convention: the generated page contains no write API.

Probe the mounted URL, then open it in the current Codex task with `codex_app__open_in_codex` when available. Generate and open an empty-state Dashboard when there are no verified formal results so coverage and exclusion outcomes remain visible. Respect an explicit saved `dashboard.auto_open: false` by generating without opening.

Completion: the page loads without external dependencies, every card has valid or explicitly unavailable actions, reserved example domains are not clickable, every worthwhile item remains reachable, sub-8.0 items start collapsed, filters work, the visible order matches the ranked input packet, and the mounted page opens automatically unless disabled.
