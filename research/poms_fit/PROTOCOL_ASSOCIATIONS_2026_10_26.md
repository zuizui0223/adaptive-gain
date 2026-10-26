# Independent FIT zero-inclusive ecological association analysis — protocol v1 (2026-10-26)

## Relation to earlier results
Stage 1 (#70) and Stage 2 (#71) used original positive-only plant–pollinator network compilations. UK PoMS FIT 2017–2023 (DOI 10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618) is an **independent** observation programme that measures **one focal flower type per 10-minute quadrat** with true recorded zero-count surveys. This is a test of time-/weather-dependent realised visitation **at targeted flowers**, not of simultaneous partner choice, perceived cue order, or routeability.

## Source integrity / grain
Exact official package ZIP SHA-256: 9e30b02e640279f0c777526f1d4e0cf057ae9ab7991da5e9a5936659f1d5dcfb (699,352 bytes). Use both original CSV files, preserve every recorded sample_id once, and verify all ten guild sums equal all_insects_total. No manual imputation of unsurveyed dates. Provider documentation notes null insect-count fields were set to zero during their cleaning; these are publisher-defined count zeros and must not be represented as confirmed individual absences.

The programme offers 13,457 public FIT surveys (774 zeros; 5.75%) and 3,053 1-km-square FIT surveys (271 zeros; 8.88%). Raw insect-group sums and all_insects_total agree in every row. The 1km dataset has 95 location_codes and 486 site-years, including 236 with at least three sampled dates. The public survey design is opportunistic, unlike the structured 1km site visits.

## Primary scientific question and estimand
For the **1km-square** primary dataset only: is observed **total flower-visit count per 10-minute focal-flower census** conditionally associated with wind category, after accounting for recorded floral quantity, taxonomic target category, season, year, site and sunshine? Test an observational conditional mean contrast: strong leaf movement versus the calm/occasional movement category, not a causal wind intervention. Keep the mid-wind contrast as secondary. Treat wind categories as unordered rather than assuming a linear wind-speed scale.

Primary model: Poisson GLM for raw all_insects_total with site fixed effects C(location_code), target flower category C(target_flower_corrected), floral-unit type C(floral_unit), log1p(floral_unit_count), C(year), C(sunshine), a four-degree spline for day-of-year, and C(wind_speed). Cluster-robust sandwich SE at location_code. Fixed census duration is ten minutes, so do **not** offset by arbitrary floral-unit counts (units differ among plant types). Record Pearson overdispersion/df, exclusion counts, site wind overlap, IRRs with robust 95% CI, and a joint wind Wald p-value. Interpretation is observational, not mechanistic.

Primary missing-value policy: drop rows with missing/nonpositive floral_unit_count, missing target, missing or unrecorded wind/sunshine, invalid date or source-defined response. Keep y=0 visits; do not treat missing covariates as zero. Record number excluded by each rule. A single noninteger floral_unit_count=600.5 occurs in the public FIT original data and must not be rounded implicitly; the primary 1km has none.

## Sensitivities (preselected)
1. Repeat the same response model in **public FIT** with C(country), C(habitat_type) instead of C(location_code); cluster by x1km_square. This is a **different survey mode from the same programme** and is not independent organismal behavior replication.
2. Repeat within 1km after excluding the heterogeneous “Other - please describe below” target category.
3. For 1km only, fit the same covariate design for four preselected guilds — bumblebees, hoverflies, other_flies, butterflies_moths — and compare wind association directions descriptively. These are not 4 independent randomized experiments; no claims of differential causal susceptibility based on overlapping/nonoverlapping CI.
4. Report joint seasonal spline Wald test and overdispersion. No selection of polynomial degree or reported guild according to significance.
5. If a model cannot be fitted/identified or its robust covariance is singular, report failure with counts rather than simplifying until a positive result appears.

## Limitations and promotion rule
Visitors were recorded at a **single selected flower** in each survey; flower availability outside the quadrat, all simultaneous alternatives, animal identity, per-cue sensory histories, fitness and unobserved sample effort are unavailable. Weather choice of survey day is not random; sunshine, season and taxon detectability may confound wind associations. Spatial same-site clustering and uneven plant selection limit generalization. Positive effects only qualify as associations of observed visits with environmental state. They do **not** demonstrate adaptive sensing costs C_A or C_F, within-individual partner switching, or a species-interaction cascade.

No V5/V6 scientific manuscript claims are promoted from this Stage 3 observational analysis without independent behavior/fitness validation.

## Attribution
UK Pollinator Monitoring Scheme (2026). *Flower-Insect Timed Count data from the UK Pollinator Monitoring Scheme, 2017-2023*. NERC EDS Environmental Information Data Centre. https://doi.org/10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618. OGL. Required acknowledgement: The UK Pollinator Monitoring Scheme (UK PoMS) is a partnership funded jointly by UKCEH and JNCC, through Defra, Scottish Government, Welsh Government and DAERA for Northern Ireland; UKCEH contribution is part-funded by NERC (NE/R016429/1 and NE/Y006208/1). Volunteers who collect the field data are gratefully acknowledged.
