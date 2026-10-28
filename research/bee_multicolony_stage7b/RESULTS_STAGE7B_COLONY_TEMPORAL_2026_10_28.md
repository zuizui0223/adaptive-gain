# Stage 7b — colony-level temporal organization of robotic-flower reward use

**Date: 2026-10-28. Status: SOURCE VERIFIED, ORIGINAL AUTHOR 54,362-VISIT SENSOR PROCESSING EXACTLY RECONSTRUCTED; INDEPENDENT 18-COLONY EXPERIMENT SHOWS OBSERVATIONAL WITHIN-HOUR TEMPORAL SMOOTHNESS OF *COLLECTIVE* REWARD-USE COMPOSITION.** The result is positive against the fixed within-hour permutation null, but does **not** measure individual bee identity, movement direction, social interaction, memory, cue access, wind or causal fitness.

## Source and original-grain integrity

Debeuckelaere et al. (2026), *Data and code from a self-medication experiment: pathogen exposure-dependent foraging decisions of bumblebees*. KU Leuven Research Data Repository, [10.48804/UIIVLP](https://doi.org/10.48804/UIIVLP), **CC BY-NC-SA 4.0**. Public Dataverse v1.0:
- Original `data_selfmed.csv` Dataverse file id **365590**, 7,264,880 bytes; provider MD5 and independently recomputed MD5 **`3a3578d61d7633635615d43829df3f3c`**, original SHA256 **`5b622a02708bb4c091165dc717da2dce96ebe13b9ee5024c23d4817657da0fcc`**.
- Original `00_README.md` Dataverse file id **365598**, MD5 `b05dd7324c909f8f65d95ae938c68aca`, original SHA256 `83630493bf55aedba5b1de9883fb1b9fafa8e2dfec0270d42e78565e7143cb91`.
- Original `Data_analysis_selfmed.R` Dataverse file id **365592**, MD5 `ed741040397ea0979ce421937a42ebdd`, original SHA256 `630d4bccc5b5a654cce315db487180e70146f4545e706f67be38f0bf1d7b72e7`.
- The GitHub Actions runner downloaded and verified all three original files against the publisher source; only source IDs/hashes, schema, author-processing reconciliation and aggregate results are retained. No original per-sensor event microdata committed.
- Source CSV columns exactly `experiment,name,hour,prob,Flower,date,trt,cage,group,color,colony,disease`. 18 unique commercial *Bombus terrestris* colonies over 75 source colony-days, with three pathogen conditions (Healthy, Ascosphaera, Serratia); 8 robotic flower devices nominally per tent, quercetin versus control reward, visual color counterbalanced. **No worker bee animal ID and no continuously filmed flight trajectories.**

## Independent reconstruction of publisher source cleaning — exact original result

The original R code, not our preference, defines original sensor-event preprocessing:
- Original raw robotic source: **65,211** rows, **262** complete duplicates and **2** missing-source rows removed → **64,947** original valid rows.
- Arrange by `(experiment, flowerID, timestamp)`, merge records from the **same physical device** where current start−previous *raw* row end ≤2 s. During each merged event, use earliest start and latest end: **54,761** clusters *before* duration gate.
- Original strict `0<probing<250 seconds` filter removes 399 → **54,362** processed recorded feeding events, exactly matching the authors' source R script and README.
- Source key reconciliation found **0 cross-colony** and **0 cross-nectar** merged event clusters; an original (experiment, flowerID) group never crossed colonies. The original source did **not** identify individual bees at any stage. The source treatment mapping `CONTROL→control`, `D1→quercetin` was verified in the original R code.

This perfect raw and processed reconciliation is a source-grain quality result, not a new ecological phenomenon. Dedicated [GitHub Actions 40612564612](https://github.com/zuizui0223/adaptive-gain/actions/runs/40612564612) passed prior source-original tests, and the same source gate is run before every new Stage 7b scientific endpoint.

## Prespecified independent scientific question

The scientific unit is **the experimental colony**. Does the temporal trajectory of *which nectar option the colony collectively uses* display **5-minute local continuity** beyond:
- source *60-minute hourly* reward visit totals and same-hour quercetin percentage,
- the exact distribution of event counts `n` and quercetin counts `q` in eligible 5-minute blocks, and
- the positions of ineligible five-minute bins within each original colony × day × hour?

As predeclared in `PROTOCOL_ROBOTIC_FLOWER_2026_10_28.md` **before inspecting the observed–null outcome**:
- Partition original local (Europe/Brussels) date and hour into twelve nonoverlapping 5-minute bins; a bin is eligible only with `n≥3` already-cleaned source sensor visits. A native hour requires ≥4 eligible five-minute bins; only physically adjacent eligible positions `i,i+1` count. Do not cross a missing/ineligible slot, different hour, or day.
- Smoothed quercetin-use fraction in each eligible block: `p=(q+.5)/(n+1)`. Each qualifying colony's temporal dissimilarity is `D_colony=mean_adjacent_pairs |p_i−p_{i+1}|`, where smaller values mean locally smoother relative resource use, **not** fewer actual insect visits.
- Require ≥10 observed adjacent pairs for each colony and ≥8 qualifying source colonies before fitting. All reported qualified colonies enter equally; never weight by 54,362 event count.
- Fixed **199** constrained shuffles, RNG seed **20261028**. Within each original `(colony,date,hour)`, permute the *entire original eligible bin record* `(n,q,device-count multiset)` among exactly the eligible original positions; keep ineligible positions fixed, preserving source hour totals, source bin-intensity distribution, nectar-visit counts and available device identities observed that hour. No transfer of observations between colonies, hours, dates or original experiments.
- Primary effect: `mean_colony D_null − mean_colony D_observed`. Positive means more observed 5-minute temporal smoothness than the exact same hour-level reward-usage histogram in random order. One-tailed conditional Monte Carlo p includes the sampled actual arrangement in the denominator `(1 + #null D≤actual D)/(199+1)`; minimum p=.005. This is **not** an independently heldout forecasting test, nor an intervention on bees.

## Original-data result

The original source contains **18 colonies**, **75 colony-days** and 54,362 cleaned events: 27,072 quercetin-labelled versus 27,290 control. There are 639 native `colony × day × hour` blocks with any source events. Of those, 409 contain ≥4 eligible five-minute bins, and 407 have at least one eligible consecutive pair.

- **16 / 18 colonies** pass the fixed ≥10-pair support gate. Original colonies **L6 and R6** have zero qualifying pairs and were excluded from inferential averages but preserved in the source/flow receipt. All 16 qualifying colonies show a *positive* null-minus-observed difference; original per-colony counts range **12–522 eligible adjacent pairs**, with strong effort heterogeneity visible.
- Valid analysis includes **3,469 original adjacent 5-minute-bin pairs**, source 407 qualifying hour blocks and 4,105 eligible bins in those blocks, covering 51,732 source visits in the analyzed hour-bin positions. The source count remains 54,362, not 51,732; the latter describes *eligible positions* for this endpoint only.

| Frozen colony-equal statistic | Source-backed estimate |
| --- | ---: |
| **Observed actual 5-minute neighboring quercetin-share absolute difference** | **D = 0.1412427360** |
| **Mean of 199 colony/hour-preserving shuffles** | **D = 0.1665062647** |
| Randomized distribution, empirical 5th–95th percentile | **0.1607903–0.1722779** |
| **Extra observed temporal smoothness: null mean − actual** | **+0.0252635287** |
| Eligible independent source colonies with positive per-colony excess smoothness | **16/16** |
| One-tailed constrained Monte Carlo p | **0.005** (minimum 1/200) |

Observed D is lower than the constrained permuted null's entire sampled range. Per-colony source-colony mean D values and qualifying pair counts, null-mean per-colony D values and positive/negative directions are retained individually in `colony_reward_temporal_persistence.json`, along with the data-quality and source hashing receipts. **16 agreeing colonies** are a meaningful advance beyond the previous one-colony flower-route setup, but 54,362 individual sensor visits are still repeated events, not independent tagged bees. The 199 shuffles are **not** 199 independent experiments.

## What is established and what cannot be inferred

**Supported observation:** the relative recorded use of quercetin versus control robotic flowers in each colony has positive *fine-scale 5-minute temporal continuity*, beyond what the same colony's reward-use totals, observation effort and bin-level share distribution within each hour would yield if their ordering were exchangeable. This pattern is replicated across **16 original independent colonies** under the fixed support rules, across more than one original pathogen-treatment type.

**Important alternatives, not separated:** (1) original robot nectar-refill timing after feeding, (2) the same individual bee causing consecutive robot events but lacking an animal ID, (3) diurnal activity changes within an hour not removed by an hour-level shuffle, (4) color/reward learned preference, (5) multiple individuals with correlated timing, (6) loss of some robot devices on a colony-day and reward availability imbalance, and (7) colony physiology and event-detection effort. There is **no measured direct social influence**, no individual forager identity, no continuous animal flight path, no precise visual cue arrival order, no independent source field-wind treatment and no realized fitness or (C_A,C_F). The result cannot causally identify resource-use memory or individual routeability.

**Relationship to Stage 4–6:** the earlier one-colony tagged-bee experiment (Pasquaretta et al. 2019) showed actual spatial flower-visit ordering and particularly geometrically derived approach-direction predictability; this separate 18-colony source shows **temporal organization at the group/community resource-use scale**. It is *not* an independent replication of per-bee movement, directional flight inertia or sensory memory, because event IDs here refer to **flowers and colony**, not tagged workers. The two scales must remain separate until individual-level tracking and colony-level community monitoring are measured *concurrently*.

**Next decisive gate:** actual multi-colony tracking with worker IDs **and** flower-source positioning/heading, or a synchronized direct flight-video experiment with manipulated moving flower information, will identify which individual decisions generate the observed group-level time continuity. The 2025 two-hive moving-target Dryad original source (10.5061/dryad.qbzkh18tj) remains inaccessible through public download endpoints to this GitHub runner (401/403), so no measured kinematic result has been substituted or invented.

## Reproducibility
- Original-data [Stage 7b GitHub Actions run 40613248738](https://github.com/zuizui0223/adaptive-gain/actions/runs/40613248738) **SUCCESS**, all **20 focused unit tests passed**, original native Dataverse MD5 and source SHA-256 validated, exact 65,211→54,362 author processing and 199 conditional hour-level whole-bin shuffles performed on the original data; `STAGE7B_COLONY_TEMPORAL_COMPLETE` printed.
- Implementation `source_audit.py`, `source_semantics.py`, `reproduce_original_sensor_cleaning.py`, `colony_temporal_persistence.py`, their numerical tests and dedicated `.github/workflows/bee-stage7b-18-colony-source.yml`.
- All numerical inference is descriptive/exploratory following a chain of earlier positive discoveries. Freeze results and do **not** search additional arbitrary minute scales or colony disease subsets for significance.

**Data attribution:** Debeuckelaere et al. (2026), KU Leuven RDR, DOI 10.48804/UIIVLP, CC BY-NC-SA 4.0. Neither original raw sensor data nor the publisher's full analysis script is redistributed through this repository.
