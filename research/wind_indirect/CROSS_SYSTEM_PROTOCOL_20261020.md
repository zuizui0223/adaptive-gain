# Cross-system original-data wind × indirect-species tests (2026-10-20)

**Design fixed before reading original event rows.** Extends the prior UK PoMS + EuPollTrait original-data analyses without altering their recorded no-go thresholds. Main, V5 and V6 remain untouched.

## Goal and ecological novelty question

Can wind *moderate a measured biotic effect on flower visitors* instead of simply filtering taxonomic guilds? The independent field sources here include actual predator-risk manipulation or observed plant–pollinator–predator/prey encounters. **Do not pool them into PoMS species-trait RR; those estimands, spatial scales, and wind instruments differ.**

## Source A: Rieken & Oester 2026, Dryad DOI 10.5061/dryad.1c59zw4bt

Original `dataset_field_experiment.csv` (Dryad stream 4965081) and `README.md` (stream 4965085), unmodified bytes, record SHA256. The published design has 22 one-hour observational blocks in 15 days, nine Nuphar flowers/block, allocated to randomized *artificial dragonfly*, *neutral object* and *control* treatments (3 flowers each). Wind is a **binary observational** indicator (roughly >=2 m/s), natural odonate abundance is contemporaneous, outcome visit duration is measured **only among actual visits**. Analysis shall check that Treatment, Wind, Obs_Block, Flower_ID, Visit_Duration and Pollinator_Group columns exist, and report missingness and treatment×wind×group counts before fitting.

- **Primary behavioral candidate**, only if both wind strata contain randomized treatments within multiple independent observation blocks: treatment effect for artificial predator versus neutral object on log1p visit duration, and a *treatment×wind* difference in that effect. Neutral object is crucial: distinguishes predator appearance from the presence of any object.
- Model a block-adjusted contrast and block-cluster interval, retaining Diptera/Hymenoptera as separate strata only when observed n>=30 per comparison arm and >=8 independent blocks per wind condition. Do not treat 100 visits in one flower as 100 independently randomized units; use flower×block as assignment cluster, and inspect within-block wind variation and class balance first.
- **Selection warning:** conditioning on being a visit is post-treatment selection. Differences in duration among visitors do not identify an unconditional randomized effect on average activity/fitness. If zero-visit flowers cannot be reconstructed, do NOT claim a causal visitation-frequency effect or a per-flower rate.
- Covariate Odonate_Abundance can be measured concurrently with visitor duration; never claim a wind→odonate→duration mediated effect without temporal/structural identification. Descriptive risk/abundance dose-response is separately tagged.
- Wind is NOT randomized; wind×treatment only tests heterogeneity of a randomized treatment effect conditional on observed wind *if allocation and overlap truly support it*. Do not translate binary wind to Beaufort class/m/s and pool PoMS.

## Source B: Hulting et al. 2024, Dryad DOI 10.5061/dryad.zpc866tg0

Original `CLE_pollinator.csv` (~2678 pollinator interaction events), `CLE_crabspider.csv` (individual spider, prey=yes/no), `CLE_floral.csv` (species abundance), and `CLE_summarized.csv`. Streams from source landing page: 2887401, 2887402, 2887403, 2887396; precise filenames and checksum established from downloaded bytes, never guess file identity. The design has 12 sites×four transects and three sampling rounds, experimental *seed mix richness/provenance* (not randomized wind).

- Reconstruct site×transect×round matched resource/visitor/spider counts, **without imputing a spider/non-visitor absence where survey denominators are undocumented**. Check date and event/grain before joining; avoid many-to-many join expansion. Do not link a wind value to spiders if wind only recorded as a covariate of **positive pollinator interaction rows** with unobserved no-visitor sampling periods.
- Describe exact plant–spider and plant–pollinator overlap; test whether plant species used by crab spiders carry different pollinator group visit rates *conditional on independently counted floral abundance*, controlling site and sampling round and treating transects within site as dependent units. Because the original paper already described florals and spider predation, any redone result is a **small mechanistic bridge**, not a new global macro law.
- Hulting may have incomplete within-round denominators. If wind, spider, and pollinator cannot all be joined without positive-event leakage, make wind×spider pathway **NO-GO**, but retain observed interaction edges as independent proof that some multi-trophic edges are actually measurable.

## Cross-dataset output

Preserve source SHA256s, file schemas, row counts and zero semantics, analysis-eligibility and no-go decisions, site/block independence, predeclared contrasts and exact unsupported claims. Positive next result only if it survives all declared basic sensitivity comparisons and is not simply the known source paper's main result. Require independent prediction or experimental contrast before promoting a new ecological proposition.

## Distinct previous claims

PoMS 86-site adult hoverfly larval feeding class×wind RR 1.62 was primarily *genus/lineage-confounded*; adding 2-m observed flower label richness reached only 622 traps against a frozen 1000 threshold and did not improve held-out five-fold predictions. The external predator-risk and spider-plant data should not be used to retroactively validate larval feeding causation.