# Stage 3: UK PoMS zero-inclusive FIT Count analysis — empirical result (2026-10-26)

**Status:** completed exploratory observational reanalysis of an independent public survey programme. **Positive association, not causal wind effect; NOT ecological routeability, within-individual partner switching or evolutionary selection.** Confirmed CI: https://github.com/zuizui0223/adaptive-gain/actions/runs/40266024816 (15 synthetic/source-integrity tests green; both schema and regression completion markers recorded).

## Source, provenance and scope

UK Pollinator Monitoring Scheme (2026), *Flower-Insect Timed Count data from the UK Pollinator Monitoring Scheme, 2017-2023*, NERC EDS EIDC, DOI https://doi.org/10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618, Open Government Licence.

**Official original uncompressed data bytes are pinned individually** because regenerated EIDC ZIP wrappers vary via readme.html:
- public FIT CSV 6,712,935 bytes, SHA-256 `bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c`;
- structured 1km FIT CSV 1,690,496 bytes, SHA-256 `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`.

Original observations: 13,457 public surveys (774 zero total-insect counts, 5.75%); 3,053 1km surveys (271 zeros, 8.88%). The original source has **no duplicated sample_id**, no negative insect totals, no mismatches between sum of 10 insect-group count columns and all_insects_total (16,510/16,510 checked). Publisher cleaning documentation confirms blank insect count fields are replaced by zero *within collected FIT surveys*. No unobserved survey dates were synthesized as zero. Source data include target flower identity, 10-minute survey, floral_unit_count, sunshine, categorical wind_speed and broad insect groups. One fractional floral count (600.5) occurs in public FIT and is reported without silently rounding.

1km FIT has 95 structured sites, 486 site-years, of which 236 contain >=3 sampling dates and 439 contain >=2 target flower labels. These are **focal-flower censuses**: they do not measure the simultaneously available alternative flower set or the animal's decision sequence.

## Frozen primary model

The primary estimand is a **conditional mean visit-rate association**, not a treatment effect. On the 1km survey, model all_insects_total using a Poisson GLM with:
- wind_speed category (reference: *Leaves still/moving occasionally*);
- log1p(floral_unit_count), floral-unit type, corrected target-flower category;
- year, sunshine, 4-df spline of day-of-year, site fixed effects;
- site-clustered sandwich SE.

Census duration is ten minutes in all records, so no floral-unit offset is imposed across incomparable flower-unit types. The same data/analysis gates are fixed in PROTOCOL_ASSOCIATIONS_2026_10_26.md. Public FIT is a different mode of the **same programme**, modelled with country/habitat covariates and clustered by 1km-square ID rather than including one fixed effect per opportunistic public location.

### Total-insect visits

| Metric | 1km structured FIT | Public FIT |
| --- | ---: | ---: |
| Included surveys | 3,037 | 13,257 |
| Included zero-visit surveys | 268 | 756 |
| Calm observed mean insect visits/10 min | 11.941 | 11.379 |
| Strong-wind observed mean insect visits/10 min | 7.860 | 9.739 |
| Poisson adjusted gentle-wind IRR [95% cluster CI] | 0.854 [0.769, 0.949] | 0.941 [0.881, 1.004] |
| Poisson adjusted strong-wind IRR [95% cluster CI] | **0.764 [0.624, 0.935]** | **0.837 [0.750, 0.933]** |
| Wind joint cluster-robust Wald p (2df) | 0.00482 | 0.00289 |
| Season spline joint Wald p (4df) | 3.56e-13 | 5.02e-58 |
| Pearson overdispersion / df | **9.22** | **16.49** |

Site support: 89/95 structured 1km sites, comprising 3,016 included surveys, have at least two recorded wind categories; 976/2,943 public 1km squares, comprising 10,210 included surveys, have at least two categories. This is not randomized exposure to weather.

**Allowed positive result:** across both survey modes, observed 10-minute insect visitation at the chosen flowers is conditionally lower during the strongest recorded leaf-movement wind category after declared covariate adjustment. Season remains associated with counts after the same controls. The Poisson family is substantially overdispersed, making model-checking essential.

## Exploratory, post-first-run robustness to overdispersion

The predeclared primary Poisson results above prompted two separately labelled, **post-hoc** negative-binomial GLM weight sensitivities with fixed dispersion parameter alpha=1 or 2, using the same design and site-clustered SE:

| Model | Structured strong wind IRR [95% CI] | Public strong wind IRR [95% CI] |
| --- | ---: | ---: |
| Poisson | 0.764 [0.624, 0.935] | 0.837 [0.750, 0.933] |
| NB alpha=1 | **0.769 [0.659, 0.897]** | **0.812 [0.738, 0.893]** |
| NB alpha=2 | **0.764 [0.655, 0.892]** | **0.809 [0.736, 0.890]** |

These fixed-alpha NB models are **sensitivity checks, not independently selected best-fitting dispersion estimates or independent confirmation**. Their agreement improves confidence in the sign of the conditional mean association, not causality.

## Taxon-specific exploratory associations (structured FIT, n=3037)

| Group | Gentle-wind IRR [95% CI] | Strong-wind IRR [95% CI] | Joint wind p |
| --- | ---: | ---: | ---: |
| Bumblebees | 1.004 [0.844,1.194] | 1.262 [0.862,1.846] | 0.469 |
| Hoverflies | 0.825 [0.712,0.954] | 0.814 [0.617,1.076] | 0.031 |
| Other flies | 0.813 [0.694,0.952] | 0.704 [0.513,0.966] | 0.033 |
| Butterflies/moths | 0.886 [0.654,1.200] | 0.573 [0.330,0.997] | 0.141 |

The *absence of a significant bumblebee wind coefficient is not evidence of no effect*, and the four separate model p-values **do not test between-guild difference**. Counts are overdispersed and guild identities broad. Treat taxon-specific patterns only as hypotheses for new interaction/within-survey analyses, not as established wind-niche partitioning.

## Explicit sensitivity failure / identifiable correction

Predeclared exclusion of the heterogeneous `Other - please describe below` flower category leaves 2,058 structured observations. For every one of the 14 remaining named target categories, the source data associate that target with **exactly one floral-unit type**. Hence the original design including *both* full target indicators and floral-unit indicators has an exact rank deficit: its robust covariance is not identified; no p-values or confidence limits from that aliased original design should be used.

A separately labelled **post-hoc algebraic collinearity repair** drops only the redundant floral-unit indicators (which are fully spanned by the named target indicators). This produces:
- gentle-wind IRR 0.878 [0.775, 0.996];
- strong-wind IRR 0.799 [0.640, 0.997];
- **joint wind Wald p=0.0709** (not significant at 0.05).

This is a boundary on the robustness claim: point direction persists on the named-flower subset, but evidence for a joint wind difference is weaker. We keep the invalid original design recorded as a nonidentifiability result and the corrected model explicitly marked post-hoc.

## Biological interpretation and what remains unproven

**Supported:** wind category and season are associated with detected visitation even after adjusting for floral quantity, target species, date, sunshine, year and available spatial structure. Different guild estimates suggest possible heterogeneity but do **not** establish it.

**Unproven:** causal wind response, actual numerical wind speed or wind direction, wind-mediated sensory routing, simultaneous plant choice, competition, adaptive-foraging payoff, species-network rewiring, indirect other-species causal cascades or fitness/evolutionary consequences. Insect guild identities are broad and surveys focus on one plant at a time. Spatially structured FIT is not a randomized weather intervention; public FIT timing and target selection are opportunistic. Cluster robust errors protect against certain within-site correlations, not omitted-variable confounding.

**Next ecological gate:** independent replication with simultaneously documented floral availability for alternative plants; model wind × insect guild interaction within survey with appropriate dependence; ideally direct filmed within-individual cue sequences or controlled wind manipulations to connect to the adaptive-gain causal mechanism. Do not alter frozen V5/V6 main claims from this observational result.

## Required attribution

The UK Pollinator Monitoring Scheme (UK PoMS) is a partnership funded jointly by the UK Centre for Ecology & Hydrology (UKCEH) and Joint Nature Conservation Committee (JNCC) through funding from Defra, Scottish Government, Welsh Government and DAERA for Northern Ireland. UKCEH contributions are part-funded by NERC (NE/R016429/1 and NE/Y006208/1). Thanks to the volunteers and staff who collected the surveys.
