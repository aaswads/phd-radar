# PhD Radar

**English** | [简体中文](README.zh-CN.md)

PhD Radar is a Codex skill for finding, verifying, screening, scoring, and presenting funded or salaried doctoral opportunities. It combines targeted vacancy sources with open-web discovery, then returns to official university, institute, employer, project, or application pages before admitting a result to the ranked set.

## What it does

- Reuses a persistent search profile for regions, topics, methods, funding rules, and exclusions.
- Discovers advertised PhD positions and funded-program routes.
- Verifies opportunities against official sources.
- Screens institutions and research groups using configurable criteria.
- Scores and ranks verified results on a 0-10 scale.
- Generates a self-contained card-based HTML dashboard.

## Install

Clone the repository, then copy `skill-src/phd-radar` into your Codex skills directory:

```powershell
git clone https://github.com/aaswads/phd-radar.git
Copy-Item -Recurse .\phd-radar\skill-src\phd-radar "$HOME\.codex\skills\phd-radar"
```

Restart Codex or start a new task so the skill is discovered. You can then ask, for example:

> Use PhD Radar to find funded machine-learning PhD positions in Europe.

On first use, the skill guides you through creating a reusable search profile.

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

The bundled Python scripts use the standard library and support profile storage, deterministic ranking, and dashboard rendering.

## Validate

From the repository root:

```powershell
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\skill-src\phd-radar
python .\skill-src\phd-radar\scripts\rank_results.py --self-test
```

## Data and verification

PhD Radar stores a local profile under the user's Codex directory by default. Personal profiles, generated dashboards, and search outputs are not part of this repository. Vacancy details can change; always treat the linked official application page as authoritative before applying.

## License

[MIT](LICENSE)
