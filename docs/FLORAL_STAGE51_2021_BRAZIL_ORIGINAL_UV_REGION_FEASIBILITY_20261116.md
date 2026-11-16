# Stage51 — original 2021 UV flora, regional GBIF occurrences, source study HEX

**2026-11-16 JST.** Original study domain verification, not a new ecological effect or validated pollinator cue-use mechanism.

## Problem resolved

The Stage50 global first-page GBIF pilot wrongly reported no Brazilian records for 30 original 2021 UV-study plant species. Audit of the original Stage50 60-species receipt revealed **26/30** originally Brazilian taxa already had high-quality model-eligible records with the literal **country name "Brazil"**. The code had compared this name with ISO "BR"; the result 0 was a **data-field interpretation bug**, not a species occurrence result. The GBIF API's two-letter country identifier is **countryCode**. The original source data, UV categories, modelled bee values and 2016 measured climate values were not changed by this diagnosis. Stage50 science interpretation must disregard its old false "zero Brazilian" claim.

Stage51 first source-region CI repeated the same ISO vs name comparison and rejected 3,052/3,052 retrieved records. We independently inspected the derived artifact and verified all exclusions were the country comparison. The code was changed to prioritize countryCode=BR, accepting a verified full Brazil name only when code is missing, and a new original source workflow was run successfully.

## Authentic original 2021 geographical test

Plant phenotype: Tunes et al. (2021), Frontiers in Plant Science, doi:10.3389/fpls.2021.618028. Source original Table S2 measured 80 taxa; strict GBIF accepted taxonomy retains **71 species** (48 UV-uniform, 23 UV-spatially patterned).

Original field sites (Stage47 source-verified): Botucatu, Santa Bárbara Ecological Station, Serra da Canastra National Park, Brazil. Original source study does NOT identify exactly which measured plant taxon came from which of the three source locations. The original paper's optical category is not an observation of UV pattern at an arbitrary GBIF occurrence coordinate.

Source region bounded BEFORE result: Brazilian country=BR, WGS84 longitudes **−50.0 to −45.5**, latitudes **−23.5 to −19.5**, years **2010–2026**. This rectangular window encompasses the three original sites but includes other Cerrado habitats and is NOT the exact plant sampling locality. GBIF occurrence/search queried one bounded first index page up to 150 records per species; this is opportunistic presence search, NOT a representative complete native range.

Spatial match: original Laborieux et al. (2026) 10,242 original projected HEX polygons recovered from source authenticated repository as in Stages46–47, with point-in-polygon original Sphere_Robinson transformation. The source original published study-site model eligible HEX cells and author-filtered model species-name richness, preserved from Stage47:

| Source HEX | Modelled Bombus source species names | Modelled all-bee species names |
| --- | ---: | ---: |
| HEX8285 | 4 | 132 |
| HEX8318 | 3 | 137 |
| HEX8252 | 4 | 124 |

These are not current independently observed individual Bombus, native-only abundance, realized visits or proven local pollen transport.

## New genuine regional-data results

Source-provenance original Actions run [43871068388](https://github.com/zuizui0223/adaptive-gain/actions/runs/43871068388) **SUCCESS**, derived original-source artifact **14227722807**, digest **sha256:cf8b47d4d23274a69e90dfd61e0747d719c49b2461b7607026d3ac84a9d5e186**.

| Region/domain coverage | Count |
| --- | ---: |
| Original 2021 UV-measured taxon names with verified accepted species key | **71** |
| Taxa with a positive GBIF index count under the Brazilian source-region query | **70/71** |
| Original regional GBIF records retrieved in bounded first pages | **3,052** |
| Records with source species-key, Brazil ISO country code or validated full name, coordinate uncertainty within 10km, and one source HEX polygon | **682** |
| Source taxa with ≥1 high-quality record in the regional original bee model geometry | **46/71** |
| Source taxa with ≥1 high-quality occurrence located in a polygon containing an original published study site | **39/71** |
| Different original published study HEX occupied by at least one eligible record | **3/3** |

UV-patterned original accepted species n=23: 23 have a positive regional GBIF index count; 17 have at least one quality-qualified region record; **11** reach an original study-site candidate HEX. UV-uniform n=48: regional positive index n=47; high-quality regional support n=29; original site candidate HEX support **28**.

These are **detection and geography coverage counts**, not UV pattern prevalence across a native plant community. In particular, the 71 species are preselected by the original optical study, GBIF record density is observation-dependent, and 39 taxa with a GBIF occurrence in a study HEX were **not proven to have been UV-measured at that location**.

## Inference and next ecological target

The source region overlap correction creates a valid **source-qualified spatial opportunity frame**; the earlier zero Brazil finding must never be reused as evidence. It still does not generate a test of UV visual information's evolutionary link with Bombus: only 3 source-site HEX model cells show Bombus richness 3–4, the original per-species collection locality is unresolved and no independent morphological/nectar-use or seed fitness observations exist.

The stronger next primary hypothesis test should use the 2016 *Potentilleae* paper: 177 original UV-source taxon measurements (86 patterned/91 uniform), 159 taxonomically accepted species, with **original study latitude, UV-B irradiance, mean annual temperature and precipitation**. Link original geographic source regions to bee model cells without replacing original source phenotyping sites with arbitrary global GBIF records. Separately evaluate other bee taxa guilds, study-block climate/lineage, explicit native/introduced occurrence and source selection. A true source-measured optical contrast in the flower is **not** direct demonstration of receiver use or plant adaptation.

Code: research/floral_visual_macro_stage51/verify_2021_Brazil_source_region_gbif.py, with source-free unit tests and dedicated Actions pipeline. Original raw GBIF rows are ephemeral, only derived per-taxon source-HEX counts and receipt JSON are kept. Keep Draft/unmerged; main unchanged.
