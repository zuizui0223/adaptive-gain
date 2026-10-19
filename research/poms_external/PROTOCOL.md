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

## Post-schema exploratory test contract (recorded before numerical matched results)

The original FIT archive contains **13,457 public** and **3,053 1km** performed 10-min counts, each with nonmissing ten-guild zero/positive counts. Each survey records `target_flower_corrected`, `floral_unit_count`, `floral_unit`, date and site. The same published choices group many unrelated flowers as `Other - please describe below`. Main comparison **excludes Other altogether** rather than treating 6,000+ surveys of different unidentified plants as one coherent target resource. Missing flower-unit counts are never interpreted as zero exposure. See `audit_fit.py` and archived source SHA256 for QC.

**Strict matched exposure design:** Within site × year, require **two different named target-flower categories**, each sampled in **both the same two calendar months**, with positive observed 10-min survey exposure and positive measured flower-unit counts in all four cells. Do not interpolate missing plant×month cells. Require one consistent `floral_unit` definition per plant category across those two months. Where multiple such 2×2 crosses exist, select the one with greatest minimum cell sample count then total sample count, based on survey exposure **without looking at insect counts**.

Use **1km survey** as the primary design (up to 95 identified monitoring sites) and separately assess nonrandom public self-selected sites with 1km grid-cell ID as a coarser comparison. To avoid reusing a site as independent replication across years, retain one exposure-selected site-year per site for the exploratory independent-site summary; separately report eligible site-years. Main sensitivity: both plants' survey median dates within the **same month** must differ by <=7 days. Compare (i) 10-min survey count exposure and (ii) flower-unit count exposure; the latter requires the unverified assumption that encounter rates scale linearly with floral units.

For each insect guild and 2×2 case, assume a *conditional null* of independent multiplicative plant and month visit intensities proportional to measured exposure. Given guild count totals by plant and by month, the off-diagonal contrast follows Fisher's **noncentral hypergeometric** distribution with offset odds `E11*E22/(E12*E21)`; calculate exact two-sided probability. A site-year with no informative table margins is not a test of absence. Combine independent-site exploratory exact tail probabilities via Fisher's method, and apply BH correction across the ten guild summaries. Fisher combination still assumes the selected spatial site units are independent; coarse public grid cells and residual spatial/weather dependence can violate it. Results are **exploratory** and do not license a general species/preference/fitness claim.

A significant result would show **observed flower-target × calendar-month interaction in guild-specific encounter counts conditional on monitored exposure under this model**, not selection among all simultaneously flowering species, ecological rewiring, sensory cue routing, or causal preference. An inconclusive result could reflect weak crossed target support, poor power, coarse guild identification, or model assumptions, not proof of no temporal structure.
