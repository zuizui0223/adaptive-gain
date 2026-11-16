# Stage50 — original UV species × actual plant GBIF records × source bee-model HEX

2026-11-16 JST. Completed source-authenticated geographic feasibility study, not a plant–pollinator fitness experiment or an identified evolutionary UV effect. Wind work remains separate.

## A. Verified original sources

- Botanical original published trait frame: Stage49, 262 GBIF accepted species across three studies, including 230 species with measured spatial UV categories (101 patterned, 129 UV-uniform). The 2020-only 32 historical UV-pigment-change species are NOT included as a binary pattern response.
- Pilot was fixed before reading GBIF occurrences: 15 patterned and 15 uniform species from each of two main source studies, Koski & Ashman (2016, doi:10.1111/nph.13921) and Tunes et al. (2021, doi:10.3389/fpls.2021.618028), 60 taxon keys total, deterministic source-key hash.
- Source bee geography: Laborieux et al. 2026 original model archive (doi:10.5281/zenodo.20525239), original source phylogeny and pa_cutoff 5 reproduced 3,370 bee taxon names (133 Bombus source names), 2,695 author-eligible bee HEX cells within 10,242 original projected shapefile polygons. The other 7,547 cells are UNKNOWN, not modelled bee absence.
- Original GBIF occurrence first-page sample: 2000–2026 with coordinates, hasGeospatialIssue false, present status, exact speciesKey, explicit introduced/managed records excluded, recorded coordinate uncertainty <=10 km, and precise point-in-polygon in original source projected CRS. Missing coordinate uncertainty is not treated as a native range or confirmed absence.

## B. First real-source geographic feasibility

Authenticated original-source Actions run 43867539658 SUCCESS. Original 60-source derived CSV and numerical receipt artifact 14225738477, digest sha256:53f625d0ec08f84e590e7d9fb609d2f921fe762aea1dcfd1603b9313e425712b.

- 7,146 real GBIF indexed occurrence records retrieved in 60 first bounded pages (maximum 150 records per selected taxon).
- 2,452 actual plant records retained after model-domain and quality filters.
- 54/60 source plants have at least one retained model-eligible bee HEX record.
- 37/60 species meet the preliminary minimum of 15 eligible records and 3 different original bee-model HEX cells.
- One original GBIF taxon query indexed zero records under these filters; zero API source errors in successful run. These findings do NOT establish species absence or full native ranges.

The first implementation attempted two separated GBIF index windows per species, but it stopped after the source index total count changed between pages. This is a source snapshot problem. The corrected source-gated pilot uses one bounded first page per species and explicitly does NOT claim a representative random or complete sample. A journal-grade distribution estimate will need source-controlled full downloads.

## C. Exploratory UV source response vs modeled bee community

Equal weight for plant taxa, and equal weight for the original author bee HEX visited within each taxon's first GBIF page. Only plants meeting the preliminary quality minimum:

| Original study | Source UV state | Species | Mean source-model Bombus names | Mean all-bee model names |
| --- | --- | ---: | ---: | ---: |
| 2016 | uniform | 9 | 6.2614 | 198.6041 |
| 2016 | patterned | 11 | 4.1094 | 119.8151 |
| 2021 | uniform | 8 | 2.7953 | 99.8963 |
| 2021 | patterned | 9 | 2.5703 | 97.4090 |

In this bounded convenience sample the raw differences are negative (patterned plant records occur in model cells with fewer predicted bee source taxon names). This is NOT a reliable biological association, hypothesis success, causal effect, or inferred selection. The source of the plant phenotype, species geographic history, model eligibility, sampling effort, climate, plant phylogeny and nativity have not been jointly controlled. Modelled Bee source taxon name count is NOT abundance or effective pollen transport.

## D. Important second-stage original source check

Original 2016 PDF Table S2 latitude, UV-B exposure and mean annual temperature were independently joined to 30 pilot 2016 plants by their verified GBIF accepted species keys. Original-source audit Actions run 43868594919 SUCCESS; artifact 14226777830, digest sha256:c6348299553a2a94bcad0794add6569e64e805f3f396c444c605b68d7ff2be29.

- 30/30 selected 2016 pilot taxa have original published source-mean latitude and UV-B values; 22/30 published mean latitudes fall within the min-max latitudes of the first-page GBIF records. This weak interval overlap is NOT evidence that an occurrence was where its UV phenotype was measured.
- For 2016 viability subset: original mean absolute latitude 45.76 degrees for uniform (n=9) versus 46.57 degrees patterned (n=11); original mean annual temperature 4.91 versus 2.55 Celsius; original mean UV-B 2464.74 vs 2663.43 J/m2/day. Different climates remain a major common-cause explanation.
- Only TWO disjoint source-same-genus and original-mean-latitude-within-5-degrees pattern/uniform pairs can be formed (pilot mean model Bombus patterned-minus-uniform −1.0247). Two pairs are far too few for statistical inference, functional convergence or exclusion of phylogenetic/climatic effects.
- Most critically, among the 30 original Tunes 2021 Brazilian source UV taxa in this pilot, NONE has Brazil among its high-quality author-bee-model-eligible country codes in the first global GBIF index page. This is first-page sample regional bias, NOT actual absence from the Brazilian Cerrado. The 2021 raw Bombus contrast is therefore geographically unrepresentative of the study's original source phenotype.

## E. What is scientifically established, and next test

The data-processing claim is confirmed: existing directly published UV phenotypes can be linked by accepted species keys to true original bee source model HEX polygons with explicit observation-quality and missing-data gates.

The biological claim is NOT confirmed: no valid statement that UV guide patterns are less common where Bombus is richer, that bees select UV signalling, or that plants gain or lose fitness.

Follow-up: query GBIF specifically within original Brazilian study geography for all 71 accepted Tunes source taxa; verify near-site occurrence support using independently authenticated three original study localities (Botucatu, Santa Bárbara, Serra da Canastra), without reassigning individual original 2021 UV measurements to arbitrary GBIF points. A full-source native-range restricted, spatially blocked and phylogeny/UV-B/climate-adjusted comparison is still required.

Code: research/floral_visual_macro_stage50/pilot_original_uv_species_gbif_bee_hex.py and research/floral_visual_macro_stage50_confounds/audit_original_UV_source_latitude_vs_GBIF_bee_exposure.py. Original derived CSVs and JSON receipts in the named GitHub Actions artifacts; raw GBIF occurrence rows and original bee archive not republished. Draft/unmerged. Main unchanged.
