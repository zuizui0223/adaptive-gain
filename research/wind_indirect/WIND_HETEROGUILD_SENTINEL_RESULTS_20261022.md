# Independent other-trap guild indicators under wind: UK PoMS original-data results

**22 October 2026.** An exploratory, source-verified 92-site reanalysis. Pre-outcome protocol on this branch: `WIND_HETEROGUILD_SENTINEL_PROTOCOL_20261022.md`. **The cross-species predictive-value and wind-moderation promotion gates FAILED.** Do not promote to an actual trophic/cognitive interaction, causal wind effect or new `C_A<C_F` field measurement. No edits to `main` or V5/V6.

## Question, observable data, analysis units

Does counting a *different* insect group at neighboring trap stations help predict hoverfly/bee catches beyond observing wind, local flower-record labels, habitat and weather AND counts of the *same focal insect group* at neighboring trap stations? Is the additional signal stronger/different in windy conditions?

UK Pollinator Monitoring Scheme original 2017–2023 **pan trap** event tables, EIDC DOI `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5`. The original station and flower tables' SHA256 values were verified: `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`; `53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba`.

Original inclusion: undisturbed 4–8h exposure, recorded start/end ordinal Beaufort in 0–5, all selected guild counts valid integers including zero; discard whole ambiguous duplicate site-date; >=3 stations and >=0.5 observed wind-class contrast per site-date. Analysable cohort: **5,507 stations, 1,139 site-dates, 92 independent site labels**. Total catches: 9,719 hoverflies and 9,264 bees. Parasitoid-wasp leave-one-station-out catch rate >0 in 5,005+ samples; spider leave-one-station-out >0 in ~1,209. Plant species richness refers to recorded near-station herbaceous plants only, with a separate missing-inventory indicator; an unrecorded plant is NOT assumed absent.

**One-record original QC correction:** The previous source reader subtracted decimal clock-hour values and dropped an exact 09:25–17:25 **8-hour** sample (`sample_id=23673911`) because the computed duration was `8.000000000000002`. The newly isolated local reproduction computes elapsed time from the difference of timestamps, making the inclusive 4–8h criterion robust. Earlier PoMS branch results were on 5,506 stations; we do not silently overwrite them. Full 120-model comparison was recomputed with 5,507 stations. Regression test now covers the 8-hour edge.

## Frozen nested response models, validation and effect size

Five whole-site held-out cross-validation folds (all observations of one original site in only one partition). Response is the original **trap count** with log actual trap hours as an exposure offset via a weighted Poisson-rate model; 99th percentile of neighbor-rate features, categorical coding and all normalizations are estimated ONLY on training sites. Predictors: wind grade, within-day-centered wind, temperature, sun, vegetation, habitat/country, year/month, station number, recorded flower-name richness and explicit no-list flag.

- **M0**: measured weather and local environmental context.
- **M1**: M0 + *same-guild* counts per hour at OTHER pan traps in the **same site/date**, excluding the target trap entirely.
- **M2**: M1 + *other-trap* parasitoid wasps and spider catches (different taxonomic guilds, NOT species-specific host/prey records).
- **M3**: M2 + within-day wind × each other-guild feature.

Primary outcome: hoverfly catches; secondary bee catches. Alpha `0.1` (Poisson ridge weighted-rate scale); frozen sensitivities `0.01`, `1.0` (not chosen by response). All **120 Poisson fits converged** under numerically audited Newton–Cholesky solver. Compare held-out Poisson negative log-likelihood, averaged *within sites then equally across sites*. Percentages are relative **prediction-loss reductions**; they are NOT changes in species abundance, catch rate, animal fitness or R².

| Target, model comparison | alpha 0.01 | alpha 0.1 | alpha 1.0 |
| --- | ---: | ---: | ---: |
| Hoverflies, **M0→M1** (same-guild independent neighbors) | **+30.96%** | **+32.48%** | **+21.89%** |
| Bees, **M0→M1** | **+15.32%** | **+16.23%** | **+9.20%** |
| Hoverflies, **M1→M2** (different guilds added) | −0.03% | +0.23% | +0.50% |
| Bees, **M1→M2** | +0.11% | +0.10% | +0.23% |
| Hoverflies, **M2→M3** (wind moderation) | −0.20% | −0.14% | −0.02% |
| Bees, **M2→M3** | −0.10% | −0.07% | −0.02% |

For main alpha=.1:
- Hoverfly **M0→M1** site-equal NLL improvement 0.93786 [fixed-fold site bootstrap .60164, 1.39667] (**92.4%** of sites improved).
- Bees **M0→M1** improvement 0.35236 [.28129,.43128].
- Hoverfly **M1→M2** improvement 0.00440 [−.00021,.00910]; bees 0.00186 [−.00322,.00662]. Both intervals include zero.
- Hoverfly **M2→M3** deteriorates −0.00263 [−.00545,−.00049]. Bees −0.00136 [−.00293,−.00001]. The prediction loss increased, not decreased. All three fixed alphas show mean degradation of wind×other-guild interactions.
- At alpha=1 only, heteroguild M1→M2 hoverfly mean improvement 0.01180 with interval [.00616,.01773], but alpha=.01 turns negative, thus it **fails** the pre-declared all-alpha generality rule. Do not report the alpha=1 alone as the primary discovery.

A separate **descriptive** country breakdown of alpha=.1 hoverfly M1→M2 site-equal losses shows England −0.00239, Northern Ireland +0.02252, Scotland +0.00389, Wales +0.00354. Bees show Wales −0.00567 versus Scotland +0.00584. They are not independent causal geographic treatment contrasts; regional sampling and habitat mix differ.

## Verification, source and software QA

- **9 focused unit/regression tests passed**, including the exact eight-hour duration boundary (RED→GREEN), unknown sites guarded, site-disjoint folds, train-only feature transformation, independent neighbors excluding the focal sample, response zeros and synthetic comparison of Newton vs L-BFGS.
- Original source population independently reconstituted from both unmodified byte-verified tables (5,507 stations/1,139 site-dates/92 sites), avoiding dependence on the production grouping helper.
- **22,028** held-out-station guild rate calculations independently checked by explicit sibling-trap exclusion, max absolute disagreement `1.776e−15`.
- **All 24** alpha×outcome×model contrasts independently reaggregated from saved hashed-site OOF rows, maximum mean / relative / fixed-site-bootstrap discrepancy `1.110e−16`. Independent reaggregation is NOT independent refitting of every Poisson model. A separate first-fold solver equivalence check had max predicted-rate difference about 1e−6.
- Original sources, all runnable Python scripts, source metadata/rights, protocol, original 5,507-station QC, 2,208 hashed-site score lines, 24 exact comparisons, country diagnostics, unit tests and independent checks in the conversation's `wind_multiguild_indicator_20261022.zip` reproduction package (SHA256 `3516d28c904cc38965c9c4a33a3acd2987dcb27ed6dcf7ae8c08ac6e93c94f7f`).
- No original collector identity is included in derived scores. This is a research-branch result, not a clean general repository CI run.

## Ecological inference and stop rule

**Observed macro pattern:** contemporaneous *same-guild* captures across nearby traps carry strong, transferable information about local guild activity beyond local weather, flower records and site habitats. This can arise from shared emergence phenology, regional abundance, resource patch structure or detection rather than social information use. Different unrelated coarse bycatch guilds contribute little robust **additional** held-out information, and adding wind×heteroguild terms does not improve prediction.

**Not identified:** specific parasitoid/prey/host relations, true species-level ecological interactions, adaptation or animal cue acquisition. Since other traps are read at the SAME observation time, this is neither a forward prediction nor a behavioral sensor query without those measurements. The 5-fold split protects against using one site's records in both fit and test, but spatial dependence across site labels and overdispersion are not fully corrected; the exploratory 95% intervals bootstrap fixed OOF site-level scores without refitting.

**Stop:** Do not select extra bycatch guilds or adjust regularization by looking at the test performance to produce a favorable ecological indirect-interaction claim. Next mechanistic question is whether *measured* species-resolved predator/host activity and floral choice sets produce prospectively identifiable wind-mediated partner changes. Retain the higher-level question from adaptive-gain: whether wind changes the **accessible** order/quality of cues, not merely pooled species count.

## Source acknowledgement

UK PoMS/UKCEH EIDC Open Government Licence v3, pan trap dataset DOI above. Include PoMS partnership, JNCC, environmental funders and volunteer acknowledgements as required by original source. Underlying unmodified source documentation/metadata and full credits are included in portable package.
