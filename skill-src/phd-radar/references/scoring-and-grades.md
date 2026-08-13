# Scoring, gates, and ranking

Use this reference only after official verification and deduplication.

## Scores

Assign raw numeric scores from 0.0 through 10.0:

- `research_fit_raw`: topic, research question, methods, application domain, and long-term-direction fit.
- `eligibility_score_raw`: degree, discipline, required skills, applicant eligibility, and language fit.
- `funding_confidence_raw`: strength and completeness of salary, contract, stipend, tuition, and funding evidence.
- `overall_match_raw`: configured weighted recommendation score.

Save reasons, concerns, evidence references, model, prompt version, and input content hash. Display conventional half-up rounding to one decimal; never mix percentages with 10-point scores.

## Hard gates

Apply gates after calculating component scores. An expired deadline, failed funding requirement, explicit applicant ineligibility, unmet required language, or failed configured QS overall/subject threshold prevents formal recommendation and may exclude the opportunity under the effective request. Ranking uncertainty follows the configured `unranked_policy`; unknown facts remain unknown rather than receiving optimistic points.

Keep QS ranking gates separate from semantic scores. After the institution and subject gates pass, a source-backed lab audit may inform `research_fit_raw` or the configured overall weighting, but the reason must identify which lab evidence changed the judgment. Read `institution-and-lab-screen.md` before applying these gates.

## Default grade bands

- S: overall at least 8.5, research at least 8.5, eligibility at least 8.5, funding at least 8.0, and all relevant hard gates pass.
- A: overall at least 7.5, research at least 7.5, eligibility at least 7.5, confirmed acceptable funding, and no disqualifying gate.
- B: overall from 6.0 through 7.4, or a meaningful but explainable topic/method transition.
- C: weak core fit, a hard conflict, unacceptable funding, expired status, or poor application value.

Grades are auxiliary labels. Numeric recommendation order controls presentation.

## Stable order

Sort by unrounded overall, research, eligibility, and funding scores descending; then known valid deadline ascending with unknown last; then stable opportunity ID ascending. Assign consecutive ranks after sorting.

If displayed scores are 9.1 and 9.0, 9.1 comes first. When displayed scores tie, unrounded values still decide before the other keys.

Completion: every grade and rank is reproducible from saved scores, gates, deadline, and stable ID.
