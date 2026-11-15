# Stage31 — Multiscale multimodal floral decision hierarchy

2026-11-15. This is an evidence- and source-gated analytical implementation, NOT a completed stagewise meta-analysis or a new floral fitness finding. Draft is stacked on Stage30 PR #109. Earlier Stage22–30 studies and main are unchanged.

## Main question

At what step in the full pollinator route does an original floral signal change a choice: patch discovery, plant approach, individual flower choice, landing, within-flower movement, reward assessment, pollen transfer, or real plant fitness? How does the answer vary with the sensory modality, visual background, wind, target scale, reward status, pollinator memory, and guild?

Signal and decision stage MUST be separate axes. Floral display size can affect both initial attraction and within-inflorescence staying. Odor can cue patch discovery, flower recognition or spatially structured navigation; ultraviolet and human-visible markings can affect flower detection or later landing. Nectar guides are not assumed to act only close up. Temporal colour and scent changes can inform reward/flower age or pollination status.

**Novelty boundary:** Hierarchical cue use has already been discussed in ecological theory (2024 DOI 10.1111/1365-2435.14606). Odor can reduce visual uncertainty (2011 DOI 10.1242/jeb.047407); aligned scent/visual patterns improve learning (Lawson et al. 2018 DOI 10.1098/rspb.2018.0661); visual cues back up scent under wind and chemical noise (2017 PMID 29291092). The proposal is NOT that floral signals contain information for the first time, but that their causal and observational effects can be compared by STAGE, MULTIMODAL INTERACTION, and reproductive consequence.

## Eight modeled stages

1. patch_detection: original search opportunity, detectable distance, discovery events and known search effort
2. plant_approach: approaches given known detected patches/displays
3. flower_choice: which flower is selected among an explicitly defined available set
4. landing: initial contact, landing geometry and aborted contacts
5. within_flower_search: movement toward nectar or sexual organs, proboscis entry and handling time
6. reward_assessment: observed nectar/pollen intake and decision to continue or abandon
7. pollen_transfer: actual pollen export, stigma contact and outcross pollen deposition, with male and female processes distinguished
8. plant_fitness: fruit, viable seed and actual siring endpoints

The eight stages form a candidate partial sequential path. They are NOT automatically a directly observed nested cohort in existing studies.

## Two distinct inferential products

### A. Original experimental meta-analysis

The eligibility target is genuine manipulation of visual display area/number, visible/UV contrast, scent presence/blend/congruence, scent spatial orientation, post-pollination signal state, or a factorial visual-by-scent cue. Study × treatment contrast × original plant population × pollinator guild/taxon × decision stage × endpoint is the effect grain. Repeated trajectories from a bee, visits on a plant, and multiple reported endpoints are correlated. An article is not itself one independent data point.

Endpoint metrics must be separate: log odds ratios for binary transitions when denominators are known; signed log time ratios for legitimate approach/search/handling intervals with variance estimated from independent samples or paired covariance; risk-scale factorial interactions of scent×visual congruence or wind×vision; original plant fitness and selection gradients in their own likelihood family. A 2×2 interaction means the incremental benefit of cue 1 depends on cue 2, NOT simply a positive main effect of both signals. Do not average mixed-scale estimates into one universal "information" effect.

For a true nested sequence with the same cohort and explicit original denominator, total stage-success probability equals the PRODUCT of conditional stage probabilities. The log relative success for treatment versus control equals the SUM of stage-specific conditional log ratios when each is positive. This is the chain rule, not evidence of an evolutionary mechanism. Never sum stage SEs as independent, and never multiply transitions measured from unrelated species/cohorts as if they represented one observed path.

Planned models: separate sampling likelihoods for binary, positive continuous and plant reproductive endpoints. Random effects or robust variances for study, experiment, original pollinator/plant, and phylogenetic structure where supported; moderators for actual detection distance, wind, light background, display area and density, signal spatial congruence, experience, reward and guild. Registered search, dual screening, unique original source IDs, sampling covariance policy and reporting-bias analysis are required before any new pooled result.

Falsifiable tests: phase by signal interaction; matched vs mismatched sensory patterns; wind-related sensory backup; reward or flower-age conditioned effects; approach/visitation sign differing from actual pollen or fruit-set impact; guild-specific and network-scale contingencies.

### B. Independently sourced macroecological trait/event database

Original observational grains remain separate: flower part × individual × date for calibrated 300–700 nm spectra; flower or plant × time × GC-MS method for VOC absolute emissions and compounds; plant or raceme × patch × photo event for number/area/density of open flowers; same flower over age/pollination time for genuine changes; independent visitor event × known observed effort for actual visits, legitimate interactions and times; plant-level fruit/seed/siring record for reproductive outcomes.

Candidate source cohorts:
- FReD original spectral database (DOI 10.1371/journal.pone.0014287). Source-pinned CRAN example flowerID 157 is a ONE-SPECTRUM pilot. It does not measure corolla/guide regional UV contrast.
- Koski and Ashman original UV intervention workbook at Dryad 10.5061/dryad.bm558 (FEKoskiSF2.xlsx). Prioritize true independent array count and treatment contrasts before any effect or SE.
- Caruso et al. nonduplicated original selection records at Dryad 10.5061/dryad.2v8c5g0 are a comparison baseline, not direct nectar-guide experiments.
- Farré-Armengol et al. (2020, DOI 10.3389/fpls.2020.01154), a literature compilation of 305 species/851 VOC compounds/66 families from 58 studies, is NOT newly acquired original VOC sample data.
- Hanusch et al. (2025 DOI 10.1111/nph.70600), original 39 alpine species floral VOC, morphology, and visitor study with available supplementary source files. The reported existing visitor-richness IRR 2.49 and bacterial-richness IRR .37 are NOT intervention effects on floral discovery or plant fitness.
- Murakoshi et al. (2024 DOI 10.1038/s41598-024-51327-w), field evidence that within-patch display size, patch size, raceme density and between-patch distance interact.

Integrate plants broadly first, not just islands. Keep island/oceanic-vs-continental, wind, artificial light and pollinator community as stratified moderators for later source-supported comparisons. Resolve original taxonomic names with versioned synonym tracking; preserve repeated parts and original observation IDs. Do NOT require all traits present: species missing UV, VOC or flower age remain included with explicit unmeasured flags. RGB images cannot reveal UV, relative VOC mixture cannot imply absolute plume strength, and a photo of flower colour polymorphism does not prove ontogenetic colour change. Source-based effort and selection models are needed for GBIF/YAMAP/photo observations.

## Concrete code and evidence completed

- VERIFIED_SOURCE_GRANULARITY_LEDGER.csv: 23 source references coded as experiments, computational models, existing syntheses or candidate primary databases. Multiple rows may reference the same literature; these are NOT 23 independent effect sizes.
- multimodal_stage_effects.py: event-scale logOR, continuous handling time, 2×2 risk-scale sensory interaction, exact nested-stage probability decomposition, evidence registry validation and explicit UV/VOC/age unknown flags. All function tests use synthetic numbers and require appropriate independent-unit assumptions.
- fred_spectral_pilot.py: source-blob verified example of 401 wavelength records for FReD ID157 via the pinned public CRAN copy, 300–700 nm. A raw reflectance summary does NOT identify a nectar guide, insect cone-catch, or plant/pollinator response.
- GitHub Actions independently checks provenance and full repository Python matrix.

**Current scientific STOP:** quantitative experimental meta effect rows extracted with their original variance = ZERO. A joined global display+VOC+UV+fitness database does NOT yet exist. This branch is a verified infrastructure and scoping artifact, not a published meta/macro ecological conclusion. Next substantive gate is direct per-study source data and effect size extraction from the Dryad UV workbook and separate scent × visitor original data.
