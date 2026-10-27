# Stage 3f result — joint Pan-flower / FIT environmental context (2026-10-27)

**Status:** original-data analysis completed successfully; scientifically defensible result is an **observational wind–guild association robust to one measured contextual floral-richness covariate**. No positive evidence that wind × site-day Pan flowering richness modifies the association. **Not** a behavioral routing, competition or selection experiment.

Original-data [GitHub Actions run 40490455205](https://github.com/zuizui0223/adaptive-gain/actions/runs/40490455205) passed all **15 focused tests** with `POMS_PAN_JOIN_AUDIT_COMPLETE` and `POMS_PAN_CONTEXTUAL_MODEL_COMPLETE`. An earlier fully verified exact join run is [40488952159](https://github.com/zuizui0223/adaptive-gain/actions/runs/40488952159), passing 11 tests.

## Published data provenance and grain

Both datasets originate from the *same* UK Pollinator Monitoring Scheme, published as two separate EIDC original datasets under the Open Government Licence:
- **Pan-trap surveys 2017–2023:** DOI https://doi.org/10.5285/5841bfae-471b-498c-af89-c30e5140d6c5. Pan original station table 7,050 records, exact CSV SHA256 `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`; original flower occurrence table 12,858 records, exact SHA256 `53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba`.
- **FIT Counts 2017–2023:** DOI https://doi.org/10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618. Original structured 1km FIT CSV 3,053 records, exact SHA256 `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`.

Original Pan flowering occurrences have an explicit **Pan** sample_id foreign key to the Pan station table; that key is never equated to an FIT sample_id. Eleven original Pan flower records (nine orphan Pan sample IDs, all from 2017) have no matching original Pan station and cannot be assigned a valid site/date. Their original count/years are preserved in QA and only **spatially linkable occurrences** enter Pan context construction. There are **509 distinct plant-label identities** among linked Pan records (mostly native taxon version keys); that is not a verified nationally exhaustive or taxonomically harmonised floristic inventory.

Pan sites: 1,422 unique declared square–day contexts; 1,394 have exactly five station rows and 34 lack any linked flower taxon label. Five pan traps record forbs flowering within a 2m radius of stations across a 1km square; FIT observes insects on a single preselected floral target for 10 minutes in a 50×50cm quadrat. The linked Pan observation is a **square-day floral environment proxy**, not a simultaneous alternative set observed by the individual FIT insects.

## Exact administrative join

Require exact source `location_code × x1km_square × date`; no grid-only match replacement. Pan station and flower occurrences are first collapsed to **one source context per site-day**. A one-to-many join that inflates FIT survey counts is rejected by code/tests.

| Audit count | FIT surveys |
| --- | ---: |
| Original FIT records | **3,053** |
| Exact same Pan site, grid, day | **2,987 (97.8%)** |
| Exact matched with >=1 Pan flower taxon label | **2,929** |
| Exact with five Pan station rows | **2,931** |
| Exact with all five Pan stations AND flower taxon data | **2,877** |
| Native Stage 3d full-covariate eligible FIT surveys | **3,037** |
| Stage 3d covariate eligible, exact five-station Pan+floral context | **2,862** |
| Above FIT contexts with >=1 bumblebee-or-other-fly visit | **2,210** |
| Sites in paired main model | **95** |

At exact-join grain there are 1,224 unique site-days over seven years. A **7-day** same-square/year nearest-date *descriptive* alternative matches 3,022 surveys, but is **not adopted** for the main analysis. Site identity + grid was preserved in both samples; one additional grid/day-only match was explicitly rejected for namespace mismatch.

## Measured contextual richness in modelling population

Primary model uses exactly five *separate* Pan station samples per site-day, at least one documented Pan flower taxon, and native FIT source treatment of zeros and measured covariates. The relative guild count endpoint conditions on `bumblebees+other_flies>0` as in Stage 3b–d; original zero-total insect censuses remain in the overall FIT quality/Stage 3 visit-rate analysis, not fabricated as ratios.

- Pair-positive matched FIT census count: **2,210**; matched census records without pair observations: **652**.
- Wind recorded in paired subset: calm/occasional = 964, gentle = 1,030, strong = 216.
- Pan flower taxon richness across five Pan stations: **1–23 labels**, quartiles **4, 6, 9**.
- **84/95** sites contain repeated Pan richness variation; model admission thresholds (100 pair surveys, 10 sites, 4 richness levels and within-site richness support) passed.
- Exactly the **same 2,210 FIT observations** are used in the original Stage 3d matched-sample baseline and the Pan-enriched model, not two different denominators.

## Primary contextual-adjustment result

Grouped binomial `[bumblebees, other_flies]` on pair-positive FIT visits. Previous Stage 3d controls are retained: wind category, focal flower identity, log1p recorded FIT focal-flower units, floral-unit type, calendar-year, 4-df day-of-year spline, sunshine, five measured start-clock bins, observer classification, flower-cover category, **site fixed effects** and **site-clustered sandwich covariance**.

| Preselected contrast | OR or per-unit ratio | 95% cluster CI |
| --- | ---: | ---: |
| Strong vs calm wind, Stage 3d baseline *on matched subset* | **1.948** | 1.310–2.898 |
| Strong vs calm wind, with log1p(Pan flower richness) | **1.910** | 1.260–2.896 |
| Pan richness coefficient per 1 unit log1p(richness) | 0.863 | 0.628–1.185 |

Both models converge with full-rank design (139/139 vs 140/140) and no fitted-model warnings. Pearson overdispersion per df is 2.789 baseline and 2.759 with floral context.

**Allowed biological statement:** the *observed relative visits* association under reported strong leaf movement is not eliminated by controlling measured same-square/same-day Pan flowering taxon richness, alongside the previous environmental/plant/time/site variables. The richness main coefficient is **not** clearly different from zero, conditional on this model.

Do not report the small change in log OR as a causal percentage of wind effect explained by Pan richness. Neither the habitat context nor weather is randomized; the two monitoring surveys are not co-located quadrat observations.

## Prespecified secondary wind × Pan richness association: no clear effect modification

Two predeclared extra terms `gentle_wind × centered_log1p_richness` and `strong_wind × centered_log1p_richness` were fitted on the **same 2,210 pair-positive matched observations**. The centered richness uses log1p(6) at the sample median.

- Joint **2-df Wald chi-square = 2.6579, p = 0.26475**.
- Strong-wind effect-modification OR per 1 unit log1p Pan richness = **0.592 [0.313, 1.120]**, imprecise and including 1.
- Conditional strong-wind OR evaluated at four recorded flowering taxa (25th percentile): **2.142 [1.410, 3.256]**.
- Conditional strong-wind OR at nine recorded taxa (75th percentile): **1.489 [0.841, 2.636]**.

This difference of point estimates is **not** evidence for an identified biological interaction: the global interaction test does not reject and the ratios have large uncertainties. The fitted model has full design rank (142/142), converges, and all the **predeclared wind/richness contrast intervals and contrast covariance entries are finite**. Eight unrelated nuisance fixed-effect CI cells are nonfinite; therefore these fixed-effect *nuisance coefficients* are **not** interpretable, and source code explicitly logs them instead of misdescribing the full parameter vector as stable. No data filtering, model selection or significance-chasing was performed after seeing the interaction test.

## Main remaining limitations

1. FIT survey is a ten-minute observation on one chosen plant. Pan-forbs within 2m of five different trap locations are **site-day proxies**, not measured alternative plants accessible to the focal insect. A local habitat distance, simultaneous option or fitness claim remains absent.
2. `total_floral_units` cannot be summed across different plant-specific floral-unit definitions as homogeneous flower abundance; the model uses the number of **recorded Pan taxon labels** only.
3. The Pan survey has many station records without linked flower occurrences; zero recorded flowers may be ecology, observation/processing gaps or survey differences, not necessarily true absence. The main model includes only site-days with at least one labelled Pan flower taxon and five original Pan stations.
4. No wind direction, quantitative velocity, insect individual tracking, pollen transfer, interspecific competition, reward costs, adaptive information-sequence or fitness measure exists in the joint observational data. `C_A,C_F` cannot be estimated from this evidence.
5. Public and structured FIT are parts of one monitoring scheme, and Pan is another measurement within that scheme. None of these analyses is a separate randomized replication. This entire research line is exploratory/post-hoc after the earlier wind finding.

## Publication/next-step boundary

Retain this as **source-backed observational evidence for a wind–guild-composition association robust to a site-date flowering-community proxy**. The Stage 3f richness interaction was not supported. The general routeability mechanism and floral trait causal adaptation remain unverified. Next direct evidence requires simultaneous alternative-flower availability at the FIT quadrat and timed individual-insect observations under calibrated wind manipulations; do not promote to a causal abstract or frozen V5/V6 without those data.

Required acknowledgements and data citations follow the UK PoMS official EIDC source records (DOIs above). Do not re-host original microdata or publish unverified raw sample identifiers.
