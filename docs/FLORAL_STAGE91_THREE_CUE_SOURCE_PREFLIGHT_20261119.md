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


## Stage91A first successful original-source run: 2026-11-19

**Genuinely executed and externally SHA checked**: [GitHub Actions #44514165386](https://github.com/zuizui0223/adaptive-gain/actions/runs/44514165386); derived-only artifact ID **14524294663**, exact artifact ZIP SHA256 **d64b015a55d4661653ede0e18e7f8250531e9d9af74a5fbe0e46ebce5d64e429**. All 17 source-free tests passed, and original NHM, GIFT, Kew ZIP byte checks and joined 367-region count gates succeeded. The first run #44513633574 failed at an overstrict compact-schema expectation of optional petal width; the optional column has been removed from the *mandatory* schema and is now flagged as missing rather than fabricating measurements. The successful original NHM compact header contains only original botanical trait fields such as flower colour, petal colour and corolla colour, but **no typed petal width, fragrance or true flower diameter column**.

Original source-native unique species **55,775** (over 367 TDWG3 regions, including islands):

| Real source trait-documentation state | Exact unique species |
| --- | ---: |
| Flower-colour fields mention spotting, stripes, maculation etc. (positive lexical candidates, not true nectar guides) | **906** |
| Flower-colour documented but no marking keyword (UNKNOWN, not validated plain) | **29,065** |
| Source flower-colour fields blank (UNKNOWN) | **25,804** |
| Explicitly documented plain/unmarked by this bounded lexical parser | **0** |
| Authenticated full open flower diameter | **0** |
| Authenticated original floral fragrance | **0** |
| Authenticated typed petal maximum width (column not present) | **0** |

The 906 positive lexical candidate species are not a prevalence estimate; **no valid negative flower-marking reference set exists** in the compact data. They recur across **322/367** original TDWG3 regions, producing **7,815 species×native-region positive appearances**, not 7,815 independent plants or evolutionary origins. **209** regions have ≥10 positive lexical candidate appearances, but these regions include islands and are not independent floral evolutionary experiments. The dominant reported marking families vary by region (Orchidaceae, Lamiaceae, Saxifragaceae often the regional top family). Taxonomic and documented-description confounding remains unresolved. No wind exposure was used to make any of these counts.

The next audit added separately to this PR counts source-positive marking names by independently GIFT-qualified **animal / wind / unknown** modes; **do not infer those counts before its new original-source run succeeds**. Even if positive cases are widespread within biotic plants, a valid negative comparison and directly measured signal are still absent. Therefore: **NO-GO for the user-proposed actual species proportion patterned/unpatterned as an identified primary biological response from compact NHM data**. The source-mention rate is at most an exploratory documentation outcome until an independent negative-ascertainment protocol is established.
