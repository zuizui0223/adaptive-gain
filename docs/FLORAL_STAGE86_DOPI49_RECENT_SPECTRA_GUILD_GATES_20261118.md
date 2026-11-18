# Stage86 — 49 authentic age-resolved floral optical species and original DoPI comparison opportunities

**Date:** 2026-11-18 JST. This is a source-authenticated **study/site sampling feasibility** analysis, not a causal inference of nectar-guide recognition, multimodal learning, wind odor plume or landing.

## Scientifically relevant starting point

Ohashi et al. (2015) spectrometer archive source verified original ZIP SHA256 860ad9ef71d99efdda441fae00090ddb1dad0145f5c54a04b581b09490e718b7 and an original DoPI v2 source check (676,900 rows, 384,896,230 bytes, MD5 d1c76fc0fd4df6a6828550c5866e4af1). Previously Stage83 had 28 source taxon Apis visual receptor metrics and only 23 species informative for corrected EuPP observed Bombus/other bees; flower-age optical species repeated across 194 observed European networks and a 28-species shuffle gave no generalizable association.

Stage85 independently measured 50 source spectrometer species and 2,263 actual 300–700nm spectra. **49 taxa** have at least one author flower part with ten independent early and ten late original measurements (82 flower-part groups). *Houttuynia cordata* is the sole missing age-paired taxon. *Firmiana simplex* has early/late specimens from one outer floral part although its central part is absent; do not omit it. Stage85 successful pavo honeybee D65 + green foliage model in original Actions run 44277843552, artifact **14414838373**, ZIP SHA256 **fd49543ccbc27631e37ccff25d7fc7ab17def7f2b8f9365658d272d24d25097d**: **11/49** species have at least one 0.09-hexagon above-threshold stage-change part with BH adjustment across 82 source parts, 19/49 have descriptive far-green maintained / near-chroma reduced signed median cues. All prior 28 source continuous receptor indicators replicate to numerical precision (max difference 4.996e-16). This is an Apis *model* under fixed illumination/background, not actual Bombus psychology or recognition distance; published Ohashi 48/219 classifications are not automatically the same.

## New independently executable Stage86 question

Does source-original DoPI v2 provide a sufficient number of distinct DOI/site/month and studied plant lineages to compare these 49 genuine flower-age optical traits to actual independently identified bee guild observations, after restricting analysis to source-original methodological data?

Scripts and source-free tests in research/floral_macro_stage86/verify_real_dopi49_receptor_community_power.py; CI in .github/workflows/floral-stage86-dopi49-receptor-cooccurrence.yml. Fixed source cohort before seeing observed guild outcomes is **49 taxon names** from Stage85; 28 were previously modeled and 21 are newly age-eligible. The source DOI/site/month key is the exact tuple: author original DOI, country, year, month, latitude, longitude and habitat, with no imputed coordinates or replacement of missing observation periods.

Four increasing source-effort filters are audited separately:
1. ALL_METADATA: any original DoPI record with the exact source citation/time/geography and matched Apis source taxon.
2. AUTHOR_DO_DIRECT: original source methodology code DO only, while leaving code semantics author-native instead of equating with verified pollen transfer.
3. DO_PLANT_AND_INSECT_ALL: source DO and both original plant_survey and pollinator_survey equal All.
4. DO_ALL_AND_POLLEN_GRADE_1_2: the above plus original source pollination code 1 or 2, distinguished from unconfirmed but positive flower visitor code 3.

In each stratum, compare a metadata block with ≥2 original measured source plant species before bee outcomes, and a separate *informative positive guild* opportunity requiring ≥2 different originally identified plant genera with positive identified bee observations and both source species-ranked Bombus and other bee entries across the two plants. The same definition is recomputed on *old 28 only* vs *full 49* vs *at least one newly eligible 21 taxon*; report actual original normalized DOI support, information concentration across DOIs and within-block optical trait contrasts. These are still not confirmed botanical abundance/flower survey effort comparable field networks: a matching DOI/year/month may pool observations from different days or observers, even with the original source All labels.

Source DoPI rows are positive interaction reports only: no unrecorded visitor is counted as zero, no plant occurrence is considered absent, no observed record count is equated to a species independent colour-change origin, and the original Stage84 148 repeated record labels are never assumed unique observations. The original "interactions" column is not treated as standardized visits per flower, and no conditional bee preference beta is fitted. Distinct study DOI strings do not guarantee independently sampled field studies, and global plant phylogeny and native source field population need a separate support audit.

## Preregistered stop / advance rule

The scientific goal is a cross-study replicated information-stage effect that remains after species identity, plant clade, observer/source study, actual sampled floral opportunity, temperature/UV irradiance, gust and pollinator guild availability are accounted for. If strict metadata/survey candidates are sparse or concentrated in one publication/species, report a positive **coverage expansion** but **NO-GO** for cue-order or ecological preference mechanism. Study-level gust in ERA5 cannot establish airborne floral VOC plume intermittency, and neither DoPI nor original Japan spectra measure learned recognition, actual flower landing or successful pollen transfer at the same time. Do not fit a fictional wind -> scent -> learning -> landing -> plant fitness SEM.


## Executed actual-original-source results and publication clustering

GitHub Actions [#44283700979](https://github.com/zuizui0223/adaptive-gain/actions/runs/44283700979) **SUCCESS**. Original DoPI source download 384,896,230 bytes and original MD5 d1c76fc0fd4df6a6828550c5866e4af1 re-verified. Genuine Stage85 49 species receptor artifact SHA256 fd49543ccbc27631e37ccff25d7fc7ab17def7f2b8f9365658d272d24d25097d also re-verified. Derived-only numerical ZIP GitHub artifact **14418760539**, ZIP SHA256 **fcaf29fde7c51faecef3f5bbbcb1040b680d9c0fc4292bfbe9b8b27926d37b34**.

The original public DoPI 676,900-row table contains **42,738** positive literature interaction rows from 49 genuine source age-comparable Apis receptor species: **39,814** from previously modeled 28 species, **2,924** from 21 newly paired species. *Houttuynia cordata* is the only source 50-species match missing a complete early/late optical contrast (one source row). Across the 49, **192 normalized source DOIs** are represented: 183 among old 28 and 35 among new21, with 26 DOIs shared and **9 DOIs not found among prior 28**. Only **35/49** source plants have both species-ranked Bombus and other bee positive reports somewhere in DoPI; only **10/21** newly added plants have both.

### Frozen source comparability gates

The cohort was selected using only authentic taxon names, original author DOI × exact coordinate × source year × source month × country × habitat, original source method, and source survey-scope labels. Outcome-defined guild filters are reported separately and do not silently control the original plant cohort.

| Source evidence gate | Before guild ≥2 species | ≥2 separately bee-visited plant species, ≥2 genera, both identified bee guilds | Same filter using old 28 species | Genuinely new blocks after adding 21 species | Blocks containing at least one new 21 taxon | Normalized DOI sources, all valid blocks | New-species DOI sources |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Original DOI/site/month/habitat only | 955 | **115** | 115 | **0** | 9 | 30 | 2 |
| Author source method DO | 916 | **107** | 106 | **1** | 9 | 29 | 2 |
| DO + plant and pollinator scope both All | 200 | **43** | 42 | **1** | 7 | **12** | **1** |
| DO + both All + pollination category 1/2 | 24 | **4** | 4 | **0** | 0 | **1** | **0** |

Caution: the "new blocks" are increases in site-key count, not new independent botanical populations or confirmations that the new source species were sampled under common effort. The tight DO+both-All block subset has one source DOI contributing 25.58% of all 43 blocks; source DOI weight concentration gives **6.58 effective DOI units**, not 12 equal studies. In the strongest source pollen evidence category, all four strict blocks arise from **one DOI**, with **no new 21-taxonomy contribution**.

Optical cue contrast power also shrinks with source quality. Under DO+both-All, all 43 blocks have some distinction among the *continuous* measured species-level far-green, near-chromatic or hexagon age-change variables; only **12 blocks in seven DOIs** contain differing values of the descriptive green-maintained/near-chroma-reduced binary source flag, five of which include a newly recruited 21-taxon plant. Under pollination-grade 1/2, four blocks share one DOI and **none** contains a binary-sign-flag contrast. Neither description identifies visual sensory behavior or preference.

### Biological interpretation / progress limit

Stage85's expansion of available optical species **28 → 49** increased the taxonomic/visual measurement substrate, but it has **not enlarged the stringent same-study candidate observational comparisons meaningfully**: 42 → 43 DO+all-survey blocks and no additional grade-1/2 original pollen-support blocks. This is a real source-level empirical **coverage bottleneck**, not an absence of any wind-dependent or learning-dependent floral behavior in nature. The source contains no observed at-visit age-specific flower colour or source-coincident bee visual learning, true plume transport, actual wind, flower oscillation, landing or plant fitness.

Preregistration consequence: stop exploratory regression tuning on the same repeated DoPI taxa. Prioritize genuine new independently sampled **site/hour/flower** optical and visit data plus experimental tracking of individual sensory cue order. A study-level positivity ledger is a source recruitment target, not a new coefficient for causation.
