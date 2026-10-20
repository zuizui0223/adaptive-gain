# PoMS site-heldout results — 2026-10-20

**Status: completed exploratory analysis; no universal or causal routeability claim.**

## Main finding

Plant-category × month interactions add a small amount of out-of-site predictive information for public FIT counts of bumblebees, hoverflies and beetles. Their positive site-average score increments persist under both flower-exposure definitions and all three predeclared penalties. The more standardized 1-km monitoring sample does not yield a corresponding stable, clearly resolved cross-guild effect. This is not proof that the two survey populations differ biologically: their sample size, flower composition, seasonal window and site selection differ.

The strongest wording supported here is **small, group-specific, dataset-dependent transportable predictive information**, not a general behavioral resource-switching mechanism.

## Execution and data integrity

- Calculation commit: `f4dd0076904ae3856d74b837786e6b455f0f9e82`.
- Completed source-locked workflow: https://github.com/zuizui0223/adaptive-gain/actions/runs/39369579229
- Artifact ID: `12240069386`; SHA256: `5ed37eb05e24ee1ed823f1ce639e8757aca53fecd53875848b19678ebe6cec7e`. The downloaded archive was independently checked against this digest.
- Eight focused regression tests passed locally and in CI. All 120 model-comparison summaries were independently re-aggregated from the archived per-site CSVs, reproducing site means, survey-weighted means and fold means. Row-level fitting was performed in CI, not repeated locally.
- Three penalties × two survey designs × two exposure models × ten insect groups × five folds × two compared models = **1,200 fitted models**. Maximum observed iterations = 159; convergence warnings would fail execution. Unknown plant-month combinations in test folds = 0.
- Runtime: Python 3.11.17, NumPy 2.2.6, pandas 2.2.3, SciPy 1.15.3, scikit-learn 1.8.0.
- Original EIDC data: UK Pollinator Monitoring Scheme (2026), *Flower-Insect Timed Count data from the UK Pollinator Monitoring Scheme, 2017–2023*, DOI `10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618`.
- Source attribution/rights: Open Government Licence; UK PoMS/UKCEH/JNCC and contributing volunteers. A publication must include the full mandatory partnership/funder acknowledgement specified by the EIDC record. This is a research-stage analysis, not a submission-ready publication.

## What was compared

Public FIT: **7,325 observations, 1,967 one-km grid cells, 11 named flower categories, 34 supported flower-month combinations**, April–September. Monitoring FIT: **1,798 observations, 93 identified monitoring sites, 10 flower categories, 27 combinations**, May–August. Both analyses use 2017–2023 and retain recorded zero visits. Unnamed “Other” flowers are excluded. Some named flower categories pool several species or genera.

The baseline includes plant, month, year, country, observer experience, habitat, flower context/cover/unit and weather. The extension adds a plant-month interaction block projected off the entire baseline span using **training observations only**. Whole sites, never randomly split rows within a site, are held out in five grouped folds. These tests concern new sites within each dataset, not external training on one survey design and testing on the other.

Primary penalty alpha=0.25 on the count-objective scale; sensitivities 0.025 and 2.5 were fixed before the results. All are reported, not tuned against test scores. Flower amount is either a fitted log1p count covariate or a proportional count offset. Weighted-rate offset fits use alpha divided by mean training exposure. A regression test demonstrated and repaired the previous exposure-unit-dependent penalty; an independent direct-offset optimization agreed with the corrected weighted-rate fit to about 1.4e-8 in coefficients on a synthetic test.

The score is site-equal average Poisson negative log likelihood; positive delta means the interaction predicts better. Relative improvement below is delta divided by the corresponding site-equal baseline score. **These percentages are not changes in flower visitation, fitness, accuracy or variance explained.**

## Primary results: all ten groups

| Insect group | Public: fitted flower effect | Public: fixed flower offset | Monitoring: fitted flower effect | Monitoring: fixed flower offset |
|---|---:|---:|---:|---:|
| bumblebees | +0.845% | +0.435% | -0.084% | -0.092% |
| honeybees | -0.089% | -0.160% | +0.061% | +0.149% |
| solitary_bees | -0.002% | +0.002% | -0.091% | -0.141% |
| wasps | +0.026% | +0.015% | +0.156% | +0.112% |
| hoverflies | +0.240% | +0.267% | -0.036% | -0.324% |
| other_flies | +0.031% | +0.053% | -0.364% | -0.734% |
| butterflies_moths | +0.014% | +0.012% | +0.111% | +0.064% |
| beetles | +0.287% | +0.251% | +0.256% | +0.435% |
| insects_small | +0.545% | +0.447% | -0.025% | -0.309% |
| insects_other | -0.045% | +0.020% | -0.134% | -0.198% |

For public bumblebees, hoverflies and beetles, the primary 95% conditional site-bootstrap intervals are above zero under both exposure definitions. They also remain positive in mean under all three penalties. Their primary relative improvements are, respectively, **0.845%/0.435%, 0.240%/0.267%, and 0.287%/0.251%** (fitted effect/fixed offset).

For those three groups the fitted-flower model improves in 5/5 held-out folds in the public data; the fixed offset improves in 4/5 bumblebee folds and 5/5 hoverfly and beetle folds. Only about **53–55%** of individual public grid-cell scores improve. Average performance is not the same as large improvements in most places.

In monitoring FIT, none of the ten primary group-wise 95% intervals is clearly above zero under both exposure definitions. Beetles have positive primary point estimates but reverse sign at the weaker penalty. Wasps retain a small positive mean across both designs and all declared variants, but their primary intervals include zero; this weak direction-consistent pattern is retained rather than promoted. Public small-insect effects do not survive every exposure/penalty variant.

## Post-result influence and sample-size checks

All three shortlisted public groups remain positive after deleting their single most favorable grid cell. However, removing the top 1% most favorable cells can change the sign in some exposure models. This is an adversarial, outcome-selected influence check, **not** an alternative unbiased estimate or proof that favorable observations are artifacts.

Repeatedly drawing 93 public grid-cell scores without replacement gives intervals of the subsample mean that span zero for all three groups and both exposure models. These are fixed out-of-fold scores, not refitted 93-site models. The exercise shows why the 93-versus-1,967 site difference cannot simply be interpreted as an ecological contrast between survey methods.

## Claim limits and stop rule

The 95% intervals resample already-computed site scores: they do not refit overlapping training folds, correct spatial dependence or adjust for testing ten groups. Do not describe them as confirmatory causal confidence intervals. Sites remain observational and individual insects are unidentified. No available-choice set, floral nectar reward, cognitive acquisition sequence, latent rewiring or fitness was measured. Predictor adjustment is not complete detection/availability correction.

The earlier Schwarz 30-source result concerns temporal partitioning of observed partner composition; this analysis asks a different question about additional transferable plant-month structure at observed flowers. Do not interpret a small held-out increment as an estimate of how much of the earlier partitioning is caused by phenology or sampling. Conversely, no reproducible increment here does not prove the absence of temporal partitioning.

**Stop promotion:** do not promote the macro branch to a universal plant-pollinator routing mechanism, a causal selection effect or a general natural-network rewiring law. Do not tune more variants merely to produce a favorable monitoring result. Comparisons intended to distinguish survey populations would first need common flower/month support and a genuine between-design transfer test.

## Durable outputs

The workflow artifact contains 120 hashed-site score CSVs, three full summaries and three calculation logs. The accompanying local package also contains the code, focused tests, primary/sensitivity summary CSV, independent aggregation validation, numeric reference check, and post-result influence/size diagnostics. Source data remain the official checksum-locked EIDC originals; no fictitious field observations were generated.
