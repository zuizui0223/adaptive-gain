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
