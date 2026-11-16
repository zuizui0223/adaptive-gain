# Stage49 — original literature-confirmed species for floral visual information × predicted pollinator geography

**2026-11-16 JST. Completed original source-specific taxon acquisition and GBIF-name bridge. Not a new UV signal × Bombus hypothesis result.**

## Reason for the new route

The practical research direction is to start from **botanical species with published directly measured UV/petal visual traits**, not to require remeasurement of hundreds of original photographs before any ecological macroecology can be attempted. The Stage48 original FCP 4,475-species photographic review queue remains a subsequent independent image-phenotyping extension. Wind Stages37–44 are not part of this pipeline.

The literature evidence unit is **original publication × published taxon × directly measured trait**. UV-reflectance spatial guidance, uniform UV reflectance, visible-color markings and the temporal proportion of UV-absorbing area are distinct physical variables. Pollinator behaviour or actual nectar guide usage is not inferred from optical images or plant distribution.

## Original source 1: measured flower UV guide-pattern categories

Tunes et al. (2021), Frontiers in Plant Science, DOI **10.3389/fpls.2021.618028**. Source Table S2 original PDF SHA256 **d11b41a36d85d1b70c8d3d47c04f3e03e7d8f5f58ebaaa331a737e56ed4c2820**, authenticated by the Stage45 source workflow.

- **80 published taxon rows** from the Brazilian Cerrado.
- A uniform UV absorbing: 47; R uniform UV reflecting: 7; BE bullseye: 7; CM contrasting corolla markings: 4; CR reproductive-structure contrast: 15.
- **26 directly source-classified spatial UV patterns**, **54 source-classified uniform**. These are original UV phenotypes, not a proof that a bee uses them to find nectar.
- Seven names are genus/uncertain, not complete candidate binomials; article prose's R6/CM5 differs from original Table S2 R7/CM4. Original source codes were preserved; no individual taxon was reassigned.

## Original source 2: UV pigmentation measured across three continents

Koski, MacQueen & Ashman (2020), Current Biology DOI **10.1016/j.cub.2020.08.077**. Original open access PDF with embedded Supplemental Table S1, SHA256 **180c0cfbfb74219edfeae8c3596b7a815968aa30fb10d82cd022debe426646e6**. Full source 15-page PDF was verified, not redistributed.

Exact parser recovers **45 continent × published taxon records** and their **1,238 independently counted herbarium specimens** (in source records, not 1,238 independent species):
- Australia **14** continent-taxon records;
- Eurasia **19**;
- North America **12**.
- Four literal taxon names are repeated across continents: *Caltha palustris*, *Cerastium arvense*, *Potentilla anserina*, *Utricularia vulgaris*.
- Therefore the source Table S1 has **41 distinct literal genus-species strings**, while the paper says **42 species**. This is an **unresolved original source denominator/name conflict**, not proof of author mistake and not grounds to invent a 42nd name.
- For each record preserve family, original genus/species spelling, anther exposure code (E/C), life-history, habitat, sample n, original first/last year and standardized annual UVP/ozone/temperature slopes.
- This source measured the **fraction of petal area absorbing UV over time**. Table S1 DOES NOT classify the 41 distinct names as "UV nectar guide present" or "guide absent"; these labels remain explicitly **NOT CLASSIFIED**.

Source extraction code: `extract_current_biology_table_s1.py` and its mock-only tests. Source original-data workflow [43858144218](https://github.com/zuizui0223/adaptive-gain/actions/runs/43858144218) passed. The combined published-source study ledger workflow [43858644202](https://github.com/zuizui0223/adaptive-gain/actions/runs/43858644202) passed with 121 study-taxon records and zero exact cross-paper binomial overlaps.

## Joint original-study evidence registry and GBIF taxonomy

- **121 original study × taxon rows = 80 + 41**.
- **114 distinct literal full binomial candidates**, because seven source-2021 records lack confident species-level binomials and no full-binomial names overlap between the two source studies.
- Strict original-name GBIF taxonomic match requires `Plantae` kingdom, `SPECIES` rank, `EXACT` match type, canonical full binomial equality, and `confidence >=95`. GBIF synonym names retain their accepted species usage key.
- **111/121** published study-taxon records resolved to **111 unique GBIF accepted usage keys**, **10 unresolved** (3 not exact/confident species, 7 lacking complete source names).
- By article: 2021 UV-pattern study **71/80** strict high-confidence matches; 2020 historical-UV-pigment study **40/41**.
- All source records (including unmatched) remain in output. No unmatched species is treated as absent, no multi-continental taxon is counted as independent species, no optical UV pattern is imputed to the 2020 historical study.

Source taxonomy workflow [43859048339](https://github.com/zuizui0223/adaptive-gain/actions/runs/43859048339) passed and produced `original_121_source_visual_taxa_GBIF_species_keys.csv` and source coverage receipt.

## Large source not yet acquired per species (honest inclusion queue)

The 2016 Koski & Ashman New Phytologist Potentilleae study measured UV pattern for **177 taxa**, and the 2020 Frontiers macroevolution paper revisited approximately the same Potentilleae original 177-taxon cohort while adding visible floral pattern. **DO NOT report these as 354 independent taxa.** The Dryad deposit `10.5061/dryad.k98sf7m3z` (original XLSX `Supplementary_Data_File.xlsx`, 31,980 bytes, SHA256 `988e185526623394e3ae6c05cb842dd5c066d1be9ed550c167cf48fb515e8e3d`) is confirmed by the official Dryad public REST API, but normal file_stream returned **403** and official `/api/v2/files/543161/download` returned **401**. It was **not acquired**. 2016 source Table S2 is identified by the 2016 New Phytologist publication; do not create 177 per-species UV states from the aggregate paper result alone.

Likewise the Dryad 2020 Current Biology original XLSX `Koski_et_al._Current_Biology_Data.xlsx`, DOI `10.5061/dryad.ttdz08kw1`, is metadata authenticated (204,378 bytes, SHA256 `cfcbf56ab0a9753b20cfa31d94c89aff58691b8f38036306d453a8678ee4d71e`) but was inaccessible by 401/403. **The open-access article's embedded Table S1**, not an invented workbook export, supplied the 45 original data rows. All failed source attempts and authentication receipts are recorded.

## Next defensible spatial test

With the now-taxon-matched 111 study taxa, attach independently audited plant locations **only for the original phenotype's geographic applicability**. Project genuine plant occurrence points into the original published global bee GRID from Stage46: 10,242 source hexes, 3,370 author-filtered bee model names including 133 original model Bombus names, with only 2,695 author-eligible hexes. The source bee model's prediction support, native/introduced status, model type, and accessible domain must be explicit. Taxon–region inference has to account for source literature sampling and regional phylogenetic/climate covariance.

The botanical response `UV_spatial_pattern` is legitimate **only in the 2021 study 80 source rows** (26 original patterned/54 uniform), not in the 41 2020 UVP temporal-study names or 353 lexical marking candidates from NHM. Since 2021 source locations are narrowly Brazilian and plant-by-site measurement is not established, no globally valid binary UV × Bombus model is yet identifiable. The 41 2020 taxa are an independent **geographic UVP temporal-history exposure** cohort, not additional true UV guide outcomes.

Longer term, recruit the accessible Potentilleae 177 original individual UV-phenotype table and other independent UV-labelled botanical studies, preserving study/cohort ID and within-species geography. Include visually capable non-Bombus bee guilds, butterflies/flies/birds as ecological comparators, with source-blocked/region-held-out validation, effort/climate/UV-B/phylogenetic controls and negative controls.

**Bottom line:** Actual directly documented literature **species roster and taxonomic matching exist**, not just a protocol. There is **no new UV visual information × Bombus estimated effect, measured bee signal use, natural pollen transfer, seed set or adaptive fitness**. Stage49 remains Draft and unmerged.
