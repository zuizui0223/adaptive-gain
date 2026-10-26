# Macro Stage 2 observational result — community-day conditional null (2026-10-26)

**Exploratory / post-hoc.** This is a reanalysis of the same 30-source original dataset used in PR #70, **not** independent external validation or identification of pollinator cue-routing. The frozen manuscripts are unchanged.

## Execution and source evidence

- GitHub Actions completed original-data workflow **40262199253**: https://github.com/zuizui0223/adaptive-gain/actions/runs/40262199253
- Both `ANALYSIS_COMPLETE` and `COMMUNITY_DAY_ANALYSIS_COMPLETE` were printed. The original 14 controls and seven new conditional-null controls passed.
- Raw original dataset: `OIK-07303_database.csv`, 18,989,528 bytes, published MD5 `7a70c3e2356611b0871c163a2f9aed4a`, SHA-256 `9a9d865501d80312b0d856cc023956020fb99f744dba2b6c3192aa1540e20a3f`.
- Reference workbook checked at published MD5 `5db9f1b31fc27820e08aeff2b737ef13`.
- All **457 eligible visitor-site-season panels** were exactly reconciled with the first-stage manifest for visit counts and observed mutual information. Analyses used 199 fixed-seed permutations for each observational-unit policy. Outputs archived in GitHub Actions artifact `macro-resource-time-original-data-and-results` (artifact ID 12625430554, 90-day retention).

## Results: two distinct conditional questions

The first-stage within-visitor season-wide fixed-margin permutation gave median excess I(plant;date) **+0.458145 nats** and 440/457 panels with one-sided p<=0.05. It tests temporal dependence beyond a focal visitor's *own* season-wide plant and date totals.

Stage 2 instead permutes plant labels **within site-day across all observed visitor taxa**, preserving pooled date × plant and date × visitor recorded totals. It tests departures from random drawing from the contemporaneous observed plant composition. The two null expectations are different: do **not** interpret the difference between their excess statistics as a causal percentage explained by phenology.

| Statistic among 457 structurally testable focal panels | Recorded visits as units | One original positive row as unit |
| --- | ---: | ---: |
| Median observed minus conditional-null I, nats | **-0.015054** | **-0.086752** |
| Fraction with positive excess | 45.08% | 28.01% |
| One-sided positive p<=0.05, unadjusted | 132/457 (28.88%) | 43/457 (9.41%) |
| One-sided negative p<=0.05, unadjusted | 162/457 (35.45%) | 200/457 (43.76%) |
| Source labels with positive mean excess | 4/20 | **0/20** |

**Joint robustness:** 42/457 panels have positive-tail p<=0.05 under *both* counting policies, 90 only for expanded recorded visits, and one only under the positive-source-row policy. Some 249/457 panels have negative excess under both. The positive-row policy has across-panel mean excess **-0.12446 nats**.

A post-hoc Benjamini–Hochberg screen at q=0.05 yields 106 positive-tail rejections for visits, and **zero positive-tail rejections for positive source rows**; the latter has 162 negative-tail rejections. This is diagnostic rather than a confirmatory meta-analysis: panels share site/date/source data and Monte Carlo p-values have minimum resolution 1/200; dependency assumptions and multiplicity are unresolved.

## Source-level and shifted-date sensitivities

The visit-unit mean excess is positive only for `CaraDonna2017`, `Chacoff2018`, `Simanonok2014`, and `Thompson2018`. Each is **negative** under the source-row counting policy; the other 16 source labels are negative under both.

The original-references workbook shows that `WinfreeYYa` and `WinfreeYYb` share a DOI, and `CaraDonna2017` and `CaraDonnaYY` have identical approximate coordinates and overlapping collectors. Thus **20 source labels are not 20 demonstrated independent studies**. Exact-DOI merging leaves at most 19 unique reference groups among the eligible 20; additional same-site and same-research-team dependencies remain unresolved. Source means cannot be treated as independent meta-analytic replicates.

Excluding the two eligible source labels subject to the compilers' +182-day date shift (`Chacoff2018`, `Vazquez2003`) leaves **343 panels and 18 source labels**. The residual medians remain negative: **-0.03215 nats** for visits and **-0.08258 nats** for source rows; positive-tail p<=0.05 fractions are 22.45% and 9.04%, respectively.

## Interpretation and falsification boundary

The original positive season-wide partitioning does **not** establish visitor-specific temporal behavioral switching. Conditioning on the pooled observed site-day plant composition strongly changes the inference. Under the source-row observational unit, most source-level mean residuals are negative, a pattern **compatible** with persistent taxon-specific plant associations that constrain shifts as shared site-day plant composition changes. But the conditional null does not conserve season-wide visitor × plant preferences and thus cannot isolate behavioral change from stable specialization.

Neither policy corrects floral abundance, unrecorded flowers, genuine observation effort, observer/plant targeting, detection, overdispersion, or non-independent animal visits. It is not a test of causal cue order, sensory routeability, true latent rewiring, or selection.

## Next ecological gate

- Obtain independent, zero-inclusive focal-flower survey data with target-plant identity, observation exposure, flowering quantity, date, site and visitor class.
- Compare temporal plant association conditional on floral abundance, efforts and repeated observer/site units.
- Verify source-origin independence through the full bibliographic lineage before any meta-analytic p-value.
- UK PoMS 2017–2023 FIT Count data (DOI 10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618) are a possible independent *targeted-flower observation* source, but the survey's 10-minute focal-quadrat design does not observe simultaneous alternative flower choices. Verify actual field definitions and zero records before use.
- A separate randomized sequence-of-cues experiment remains necessary for adaptive routeability.

**No claim promotion into the frozen theory manuscripts.**
