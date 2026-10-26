# Stage 3e real-data result — wind × annotated floral structure (2026-10-26)

**Status:** Completed original-data *exploratory post-hoc* analysis, with the proposed 2-df wind × morphology interaction **not detected** for the preselected bumblebee-to-other-fly relative-count outcome. Dedicated source workflow [40321382576](https://github.com/zuizui0223/adaptive-gain/actions/runs/40321382576) passed 11 local numerical/source-shape tests; original data hashes matched; `POMS_STRUCTURE_PROFILE_COMPLETE` and `POMS_STRUCTURE_INTERACTION_COMPLETE` both printed. No previously frozen V5/V6 theory manuscript was modified.

## Reproducibility and provenance

UK Pollinator Monitoring Scheme PoMS FIT Count 2017–2023; EIDC DOI https://doi.org/10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618, Open Government Licence.

Two original uncompressed CSVs each have independently pinned SHA-256:
- 1km structured: `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`;
- public: `bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c`.

The observation is **one 10-minute FIT Count at one investigator-chosen target flower**, not an insect's simultaneous choice among plants.

## Support gate (primary excludes taxonomically mixed 'Other')

Native provider morphology values are `open`, `closed`, and occasional source NA. Among initially valid data with a **named target flower**, the same previously chosen bumblebee-versus-other-fly *pair-positive* composition endpoint is retained.

| Count or gate | Structured open | Structured closed | Public open | Public closed |
| --- | ---: | ---: | ---: | ---: |
| Pair-positive survey samples | 1,352 | 251 | 3,824 | 2,032 |
| Pair-positive samples under calm | 593 | 98 | 1,875 | 1,033 |
| Pair-positive samples under strong wind | 138 | **31** | 374 | 170 |
| Sites with both calm and strong pair-positive samples in this structure | 53 | **11** | 91 | 49 |
| Distinct corrected named flower labels | 9 | 5 | 11 | 6 |

The frozen minimum gates were >=100 pair-positive records for each structure, >=30 calm *and* strong within each structure, and >=10 sites with within-structure strong/calm observations. Both modes pass, but the structured **closed** strong-wind sample and site count barely exceed the no-go rules. This imposes a severe precision ceiling.

The UK PoMS `flower_structure` classification is a coarse species/flower-type annotation. Among *named* targets, it is deterministic for target identity in the structured data (source labels are not within-flower treatments). A separate morphology main effect is therefore aliased with plant identity and omitted, whereas **wind × morphology interactions** remain identifiable when the same annotated flower class is observed at different winds.

## Declared model

Same clock/recorder/flower-cover controls as Stage 3d, plus target identity, site, year, season spline, source wind class, sunlight, and log reported floral quantity. The primary model omits floral-unit-type main effects since among named taxa these are spanned by target identity. Response is aggregate paired binomial counts `[bumblebees, other_flies]` among pair-positive FIT surveys. Structured analysis clusters robust standard errors by 1km survey site; public by 1km grid square. Wind-interaction terms are exactly `gentle_wind × closed` and `strong_wind × closed`. Primary test is the **joint 2-df Wald** restriction that both are zero. Every model result is reported regardless of sign.

## Primary result: no detectable wind × open/closed interaction

| Parameter | 1km structured, named targets | Public, named targets |
| --- | ---: | ---: |
| Interaction joint 2-df Wald p | **0.69995** | **0.97017** |
| Strong-wind effect modification: OR ratio (closed vs open) | **1.420** | **1.015** |
| 95% site/square cluster CI for effect-modification ratio | 0.338–5.960 | 0.641–1.608 |
| Strong-wind vs calm OR for open flowers | 2.123 [1.347,3.348] | 1.680 [1.313,2.151] |
| Strong-wind vs calm OR for closed flowers | 3.014 [0.819,11.088] | 1.706 [1.154,2.521] |
| Valid fitted columns / rank | 134 / 134 | 51 / 51 |
| Pearson binomial dispersion/df | 2.453 | 2.262 |

**Interpretation:** Neither original survey mode demonstrates an effect of coarse binary source-annotated flower structure on the association between strong wind and bumblebee-versus-other-fly visit composition. The point estimate for structured closed flowers is extremely uncertain. Failing to reject the interaction is not evidence of an ecologically negligible interaction, *especially* where closed-strong observations are sparse.

The within-open and within-closed odds contrasts are conditional binomial visit-composition associations; they are not independent effects or evidence that absolute bumblebee activity increases in wind.

## Heterogeneous 'Other' flower target sensitivity (also exploratory)

| Interaction quantity | Structured including 'Other' | Public including 'Other' |
| --- | ---: | ---: |
| Pair-positive open/closed surveys | 1,874 / 460 | 5,913 / 3,972 |
| Joint 2-df interaction Wald p | 0.82100 | 0.08423 |
| Strong-wind interaction OR ratio (closed vs open) | 0.781 [0.261,2.342] | 1.404 [0.9998,1.972] |

The shape contrast itself changes after including a non-specific `Other` flower category whose recorded target species/traits are heterogeneous; this is not a clean morphology replication. Therefore the scientifically preferred result remains the named-flower primary and the large cross-structure uncertainty.

## Implications and priority next tests

- The **conditional wind–insect-guild association** documented in Stage 3b–d survives several statistical controls, but **coarse open-versus-closed floral structure does not provide supported effect modification in Stage 3e**.
- Explicitly reject overstatements: this is not evidence that wind effects are morphology-independent, nor evidence that flower shape mediates competition, flight direction or a sensory routing hierarchy.
- Broader morphology hypotheses involving capitulum orientation (upright/nodding), spines, corolla access and insect body-size/handling require independent individual-flower traits; PoMS broad open/closed labels cannot test them.
- A new independent sample with flower-specific open/closed replication across wind conditions and simultaneous flower availability is the direct next morphological mechanism gate. An in-sample target-specific heterogeneity audit would be exploratory and cannot repair missing causal identification.

## Attribution

UK Pollinator Monitoring Scheme (UK PoMS), UK Centre for Ecology & Hydrology, Joint Nature Conservation Committee, Defra, Scottish and Welsh Governments, DAERA, NERC, volunteers and partner organisations. Original source DOI above; credit the publisher for these data and do not re-host source microdata in this repository.
