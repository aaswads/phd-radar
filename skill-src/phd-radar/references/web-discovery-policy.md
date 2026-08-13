# Regional Web discovery policy

Use this reference for every region, alongside configured-source scanning.

## Query ladder

Generate a bounded set from:

1. Region + English doctoral role + core topic.
2. Local-language doctoral role + topic synonyms.
3. Region-specific institution/research-domain terms + vacancy/jobs/doctoral.
4. Project or funding terms + doctoral candidate/recruitment.
5. Official department/program/lab roster + recruiting or admissions terms.
6. Recent publication/directory leads + institution, followed by an official-page return.

Include role variants such as PhD position, doctoral researcher, doctoral candidate, doctoral student, research fellow, and useful local equivalents. Include topic, method, and application-domain synonyms rather than repeating one keyword.

Prefer queries that surface official institutional domains, but allow aggregators and scholarly directories for discovery. Do not enumerate an unbounded query grid. Apply the roster target and saturation rules in `discovery-funnel.md`; excluded leads must not cause early completion while useful candidate budget remains.

## Official return

For each promising lead:

1. Identify project name, institution, vacancy ID, PI, or application URL.
2. Find the most specific official page.
3. Verify fields under `evidence-policy.md`.
4. Preserve the discovery URL and official URL separately.
5. Classify as verified, pending, no-official-source, research-signal, duplicate, expired, excluded, or irrelevant.

Do not treat a search snippet as proof. Do not bypass login, CAPTCHA, paywalls, robots restrictions, or safety interstitials.

## Statistics

For each region report query count, leads, official returns, no-official-source leads, pending leads, excluded leads, and unique verified contributions. Do not combine lead counts with verified opportunity counts.

Completion: every region has a bounded query set and every retained lead has a terminal official-return classification.
