# Stage 3d empirical result — clock time, recorder experience and flower cover (2026-10-26)

**Status: COMPLETED, exploratory post-hoc sensitivity of Stage 3b/3c, not confirmation or causal identification.** The exact original data source is UK PoMS FIT Count 2017–2023 (DOI 10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618). All 28 focused tests and complete original-data workflow passed: https://github.com/zuizui0223/adaptive-gain/actions/runs/40283986429

## Fixed question

Does the previously identified conditional **bumblebee-to-other-fly visit-count odds** contrast, comparing strong reported leaf movement with calm/occasional movement, persist when **start-time-of-day, self-reported recorder identification experience, and floral target cover** are added to the original spatial/plant/season/weather controls?

Survey grain is one original 10-minute selected-target-flower FIT Count; no simultaneous alternative-flower choice, animal identities or cue sequences were observed. This is *not* a wind treatment.

The Stage 3d protocol and endpoint were recorded on PR #72 before its Stage 3d results were inspected. Stage 3d was planned *after* the earlier exploratory positive findings, so this is **post-hoc relative to the wider hypothesis family** and not independent preregistered replication.

## Native time format and source integrity

- Structured 1km original CSV SHA-256: `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`.
- Public FIT original CSV SHA-256: `bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c`.
- Structured FIT: **3037/3037** valid original observation start times parsed, all as native `HH:MM[:SS]` 24-hour clock. No missing/invalid times.
- Public FIT: **13256/13257** parsed (99.9925%), same native 24-hour clock; **one** source-missing time excluded, not imputed.
- Time categories were: before 10, 10–12, 12–14, 14–16, at/after 16 hours. Recorder missingness is explicitly an additional category; original flower-cover "Not recorded" is retained as its own value.
- Parser/testing rejects malformed times and does not treat missing values as morning. Both survey modes clear the predeclared >=95% clock-parse gate.

## Model and reproducibility

Response: aggregated binomial pair `[bumblebees, other_flies]` among surveys recording **>=1 visit from either group**. The initial *all-survey total count* models remain separate and retain zero-visit surveys. No visits are expanded into fictitious independently sampled insect rows.

The original covariate design had wind category, log1p floral units, target flower, floral-unit type, year, sunshine and 4-df day-of-year spline; structured FIT uses site fixed effects with site-cluster robust SE, whereas the public survey mode adjusts country/habitat and clusters by the available 1km square. Stage 3d adds the three covariate families specified above, without dropping original controls. Original and clock-subset baseline estimates were reproduced before comparing changes.

## Result

| Quantity | Structured 1km FIT | Public FIT |
| --- | ---: | ---: |
| Prepared target-flower surveys | 3037 | 13257 |
| Surveys with valid source start time | 3037 | 13256 |
| Pair-positive surveys analyzed | **2335** | **9894** |
| Clusters | 95 sites | 2579 squares |
| Prior adjusted strong-wind OR | 1.97335 | 1.51303 |
| Additional-controls adjusted strong-wind OR | **1.95597** | **1.54033** |
| 95% site/square-cluster CI | **1.36071–2.81164** | **1.22183–1.94186** |
| Strong-wind coefficient p (exploratory) | 0.000291 | 0.000257 |
| Joint two-df wind Wald p | 0.001409 | 0.000458 |
| Design matrix columns / rank | 139 / 139 | 54 / 54 |
| Dispersion: Pearson / residual df | 2.739 | 2.615 |

All reported Stage 3d models converged, their wind confidence intervals are finite and the design matrices have full column rank. One missing public-FIT time excludes precisely one survey; the matched-clock-baseline strong-wind OR is 1.51300, indistinguishable at reporting precision from the original 1.51303. In the structured mode no surveys were removed for clock validity.

**Allowed finding:** the relative composition signal between broad insect groups at the *selected target flowers* remains in the same direction and of similar magnitude after the three added measured controls; it is not driven solely by recorded survey start-time, reported identification experience or target flower cover.

## Claim boundaries

- These are **conditional relative odds**, not a demonstration that strong wind increases absolute bumblebee visits. In the Stage 3 total-visit models, strong wind is associated with lower overall counts.
- Public and structured FIT data are different survey modes of **one** PoMS programme, not independent experimental replications.
- The relationship can still reflect unmeasured flowering alternatives, plant/flower selection, wind-dependent detectability, insect movement or observer response; adjusting an observer's self-reported experience does not identify measurement error.
- Weather is categorical observer-reported *leaf movement* rather than instrument wind speed or directional wind; no wind direction, flight vector, predator, competition, causal trophic cascade or within-animal cue policy is measured.
- Stage 3b pair selection followed inspection of earlier results, Stage 3c and Stage 3d were subsequent stress tests; neither the nominal p values nor the matched datasets establish selection or sensory routing.

**Next legitimate ecological analysis:** examine *heterogeneity of the selected wind–guild contrast among target-flower types* while recording sample support and preserving the previously frozen pair/strong-vs-calm endpoint, or obtain simultaneous floral availability and wind measurements for causal mechanism tests. No frozen V5/V6 theorem manuscript claim is promoted from this FIT observation.
