# PoMS external zero/effort source gate (2026-10-19)

**Purpose:** Independently test whether seasonal variation in observed flower visits survives **standardized flower-target observation exposure**. This is a distinct analysis from Schwarz 30-source daily-event macro analysis (PR #70). Use the official UK PoMS FIT Count 2017–2023 original data, not an interpretation of published aggregate effects.

## Source and rights
- EIDC DOI: 10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618, published 2026-06-03, Open Government Licence.
- Official source URL (dataset): https://data-package.ceh.ac.uk/data/d706088c-9d48-4be5-b156-6ed6ad5e0618
- Supporting docs: https://data-package.ceh.ac.uk/sd/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip
- EIDC requires attribution and the UK PoMS partnership acknowledgement in any published analysis. Access may require user licence acceptance and/or a personal access token. Do not evade access restrictions or invent raw data.
- FIT Count samples are 10-min observations of broad insect groups visiting **one chosen plant target** within a 50×50-cm quadrat, not observation of all simultaneously offered plants. Public counts are subject to self-chosen target/date/site; 1-km-square surveys are closer to standardized site sampling but may have small panel n.

## Stage 0: data access and exact schema (executed first)
Download original ZIP **only if accessible without authorization**, retain original SHA256 and archive manifest, report exact filenames/headers/row counts and sample-level zero and missingness without reproducing individual positions. Never treat non-zip HTTP/HTML or an authenticated download failure as analyzable CSV. Keep raw ZIP in transient CI and archive **only non-sensitive schema/QC JSON**. Source metadata alone is insufficient for empirical conclusions.

## Stage 1: observational response and denominators (feasibility-gated)
Once headers and codebook confirm relationships:
1. Reconstruct unique completed 10-min survey IDs; retain zero-guild counts for performed FIT surveys and distinguish missing from recorded zero. If counts are not explicitly present for all insect guilds, stop; do not synthesize absence.
2. Separate volunteer public FIT counts versus selected 1-km-square surveys and years 2017 pilot versus 2018–2023. Require valid date, target plant, insect group, survey ID, floral abundance and exposure/effort fields. Document failed joins and QA flags.
3. Analyze individual 10-min visits to the **surveyed target flower**, with observed zero visits and preferably flower number as offset/covariate, weather, survey method, site/time terms. Cross-date comparisons must hold location/site and surveyed flower identity fixed, or explicitly standardize sample composition; changing flower-target survey mix can create spurious partner partitioning.
4. Only estimate time-varying insect-group *relative visitation across target plants* if multiple target-plant identities are adequately replicated in each comparable site×time stratum. Restrict to common support across time/flower; require positive survey exposure for every compared flower (a flower not surveyed is not a recorded zero). Report support coverage, n independent sites, and block validation. No data-rich stratum -> mark NO-GO and report proper flower-specific rate results instead.

## Hypotheses and analysis contract

**H0-availability/effort:** Conditional on counted flower numbers, fixed ten-minute observation exposure, survey method, place and temporal eligibility, pollinator-group target-plant visitation composition is explainable by surveyed-plant exposure and detection covariates.

**H1-residual specialization:** After fixing flower-target survey exposure, matching repeated site/period/flower support, and accounting for flower number and covariates, there is detectable within-season pollinator-group×flower identity×time variation beyond a no-interaction conditional null.

Study-only null/diagnostics must preserve visit count/exposure and flower-by-time survey availability, not shuffle positive insects among dates while ignoring which flowers were surveyed. Use blocked site/season holdouts, avoid pseudo-replication by multiple survey rows from the same site, report multiplicity. Compute effect sizes and uncertainty, not significance-only. Species identity is available only for target plants (if reported); insect groups are broad, so do not compare directly to Schwarz species-level pollinator species results as identical populations.

## Hard interpretation boundaries
- Even if H1 holds, changed guild-group visitation is **not** an individual insect's cue-by-cue conditional routing or adaptation, and its 10-minute **observer** duration is not an insect information-acquisition deadline.
- Surveyed target flower preference and wider simultaneous flower choice sets are not established; causal cue accessibility requires independent flowers in bloom, reward trait targets, sensory discriminability and randomized cue acquisition order.
- If downloaded PoMS data do not have comparable multiple-flower within-site repeated seasons or zero and effort denominators, report that identifiable scope precisely, not an invented result.
- Pre-2026 older PoMS releases overlap 2017–2023; do not count overlapping rows as independent validation.
