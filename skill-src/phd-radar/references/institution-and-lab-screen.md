# Institution, subject, and lab screen

Use this reference when the search profile includes university-ranking thresholds or lab-level due diligence. Treat rankings as configurable gates and context, not as a substitute for research fit.

## Configurable profile

```yaml
institution_screen:
  enabled: true
  provider: QS
  overall:
    maximum_rank: 300
  subjects:
    - name: Computer Science and Information Systems
      maximum_rank: 100
      preferred_rank: 50
    - name: Psychology
      maximum_rank: 100
      preferred_rank: 50
  ranking_year: latest_available
  unranked_policy: manual_review
lab_screen:
  enabled: true
  publication_window_years: 5
  topics: [Human-AI, agent evaluation, agent harness, human factors]
  funding_programs: [ERC, MSCA]
  inspect_doctoral_outputs: true
  inspect_alumni_destinations: true
  external_partner_keywords: [aviation, IMEC]
```

The user may change any field through conversation. Preview and confirm persistent changes; apply explicit one-off changes only to the current run. `maximum_rank` is inclusive: 300 passes and 301 fails. Never silently map a user topic to a QS subject; record the selected official QS subject label.

## Three-stage decision

1. **QS overall coarse gate.** Verify the institution in the configured edition of the official QS World University Rankings. Exclude ranks worse than `overall.maximum_rank`.
2. **QS subject gate.** For every configured target subject, verify the official QS subject table and edition. The default policy is `any_subject_passes`: at least one configured subject must rank at or above its `maximum_rank`. Label ranks at or above `preferred_rank` as preferred. Support `all_subjects_pass` only when the user explicitly selects it.
3. **Lab audit.** Only after the ranking gates pass, investigate the PI/lab at group level. Do not spend the deep-research budget on excluded institutions.

If QS provides a band such as `101–150`, use the conservative upper bound for a maximum-rank gate. If no exact or banded rank can be verified, use `manual_review` or the configured unranked policy; do not invent a midpoint. Every record must include provider, edition/year, table or subject, rank/band, official URL, and checked time.

## Lab audit dimensions

- **Recent research continuity:** inspect the most recent 3–5 years (configured window) of papers from official publication, DOI/publisher, institutional repository, ORCID, or PI/lab pages. Record topic matches and counterevidence; a keyword in one paper is not continuity.
- **ERC/MSCA funding:** verify project title, scheme, role, dates, and grant/project identifier on official ERC, European Commission/CORDIS, funder, or institution pages. A proposal, affiliation, or collaborator mention is not proof that the PI holds the grant.
- **Doctoral production and destinations:** record named doctoral completions, dates, and observable next destinations from lab/institution thesis repositories, alumni pages, or named public profiles. Report coverage as a numerator/denominator or `unknown`; absence of a public alumni list is not a negative outcome.
- **External collaboration:** verify named, dated projects or outputs with relevant partners such as aviation bodies, research institutes, or IMEC. Distinguish funded project partner, co-publication, advisory relationship, and unsupported name mention.

Store each dimension as `strong`, `adequate`, `weak`, `unknown`, or `conflicting`, with concise evidence and checked dates. Generate `lab_screen_status` as `strong`, `adequate`, `weak`, or `incomplete`; keep the underlying facts visible. The lab audit may inform research fit and the configured overall score, but it never changes a failed QS gate into a pass.

## Admission and reporting

- `pass`: overall and subject gates pass; proceed to lab audit and formal ranking.
- `preferred`: pass, with at least one target subject at or above the preferred rank.
- `manual_review`: missing, band-ambiguous, institution-name ambiguous, or configured exception; show separately and do not silently mix into the formal ranking.
- `excluded`: a verified threshold failure; report the exact gate and evidence.

Completion: every formally ranked result has verified ranking evidence, a pass/preferred screen outcome, a lab audit or explicit incomplete status, and no deep-audit claim without a traceable source.
