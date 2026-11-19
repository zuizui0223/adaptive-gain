# Stage91 | Mainland floral three-cue source preflight

**2026-11-19 JST. Status: source-availability audit, not a wind-effect result.** This Draft branch stacks onto Stage90 PR #169. It does not change main.

## Scientific target

Does continental native flora composition of different-range floral signals covary with long-term strong gusts, after geography, canopy openness, climate, taxonomy and detection/documentation bias controls?

Measure the THREE endpoints independently, with the same pre-outcome region split and wind exposure but distinct valid species and region denominators.

1. Near-range visual: objectively documented patterned flowers, separately positive, explicitly plain, ambiguous, or unmentioned. Original NHM flower colour lexical hits are *discovery candidates*, not verified visible nectar guides or true pattern prevalence.
2. Far-range visual: authentic open-flower display diameter (mm). The existing NHM source petal maximum width is NOT open flower diameter and will never be used as the primary size outcome.
3. Far-range chemical: explicitly FLORAL fragrance documented in original botanical prose, separating documented positive, explicit negative and unmentioned; report description length and botanical-source ascertainment. The compact NHM ADEPT structured source does NOT provide verified fragrance. Farré-Armengol et al. 2020 original 305-plant chemical data are reserved for separate proxy validation; do not impose complete-case intersection on all cues.

Absence of a descriptor never equals a trait's verified absence. Flora that is selected by recorded bee visits is not an unconditional regional flora sample.

## Predeclared wind primary variable (NOT yet sourced)

ERA5 1991-2020 hourly 10m gust maximum since previous post-processing (10fg): obtain daily maximum, then fraction of days **strictly greater than 15 m/s**, among months whose climatological 1991-2020 monthly mean 2m temperature is strictly above 5 C. Require complete source months/days and declare no eligible flowering-potential months as NA. Spatially aggregate with documented area and land masking to avoid ocean contamination. Day is UTC unless another boundary is registered before retrieval. Unobserved daily wind is missing, not zero.

Compare predeclared sensitivity gust thresholds 10,20 m/s and WorldClim 2.1 mean wind (physically and temporally different: 1970-2000). Stage78 PR #157 uses June 2018 source-month pilots and does NOT supply this full 1991-2020 primary exposure. Do not conflate gust with mean wind or daily gust and actual flowering-hour plume/landing conditions.

## Mainland eligibility and common holdout

Stage87-90 original source coverage: 55,775 accepted native plants, 367 TDWG3 regions (INCLUDING islands), 3,172 independently qualified GIFT mode plants (2,560 animal, 612 wind). A TDWG3 code is not an automatically mainland-only sampling unit.

An independent complete register must assign all 367 source regions an audited geographic scope [mainland, island, mixed], authoritative original polygon source and SHA256, and spatial-block ID. Exclude island and mixed regions. The freeze_mainland_region_frame script rejects incomplete/audited-in-name-only cases. A salted geographic-block split is fixed before inspecting signal outcomes and reused unchanged for all 3 separately eligible endpoint sets. Hashed IDs do not by themselves prove adequate physical buffering; inspect block distances prior to ecological claims.

Potential confounders: 1991-2020 T and P, elevation, coast distance, tree/forest cover (MODIS VCF is a temporally mismatched proxy), broad geography, documentation intensity, host plant clade and separately measured pollination guild. Unknown GIFT modes and missing GBIF Bombus records are not wind pollination or true bee absence; moth/night pollination needs directly verified labels rather than white petal assumptions alone.

## Source gate

The first task is to count real origin-backed, distinct source species/genera/families and per-region documentation opportunity for each endpoint, not fit wind slopes. Stage90 exposed wind floral hue lineage bias: 40 of 57 wind-mode single-hue source plants belonged to Poaceae/Cyperaceae/Juncaceae; removing these families left zero region with 10 non-graminoid wind-mode single-hue plants. This is source-coverage limitation, not established wind selection.

Source restoration and byte checks are inherited from SHA-pinned Stage87 NHM, Stage89 GIFT v3.2 and Kew WCVP loaders. The Stage91A workflow checks those sources and archives *derived* support counts only. Current Stage91 source CSV includes islands and cannot be passed into regression. The Stage91 mainland split cannot be generated until a complete separately checked geography register is supplied. Source-free unit tests passing is not evidence that external sources were recovered. Until real original-source execution and three valid endpoint sources are obtained, no estimates or signs are claimed.

## Claims not admissible from these data

The spatial association cannot establish how bees change sensory cue order, whether wind improves/impairs odour plume use, learning cost, within-flower landing success, flower fitness, evolutionary adaptation or phylogenetic recurrence. Fragrance wind direction remains an explicitly two-sided hypothesis. Early results are exploratory; multiple-testing and independent holdout thresholds must be fixed before true outcome inspection.

Existing Stage77 #156 is a distinct conditional European visited-flora analysis and has no existing globally usable mainland floristic holdout. Stage91 creates a new shared split **only after** verifying geography and before ecological trait modelling.
