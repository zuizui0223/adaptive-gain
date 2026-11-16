# Stage46 — source-authenticated global Bombus modeled geographic exposure

**2026-11-16 JST.** Source-based reproduction of the published global bee species × HEX matrix and original author species eligibility, prepared for a subsequent floral-visual-signal macro analysis. No UV × Bombus biological correlation has been estimated yet.

## A. Original modeled bee distributions

Laborieux et al. 2026, Global bee bioregions mirror those of other taxa despite a uniquely bimodal latitudinal diversity gradient; data DOI 10.5281/zenodo.20525239, deposit record 20525240. Original data.zip: 126,014,850 bytes, declared MD5 4bfd250a66d21c791d0a55db08b5ada6. Original zipped member data/bee_presence_only_matrix_15deg.csv is 1,301,962 compressed bytes, 12,617,604 raw bytes; ZIP CRC32 1022223877; source SHA256 641c0bb832781d3c41402a6e8158d971d0d0f663557c3f53a3b81a69dbbacd15. Compressed member was extracted via verified HTTP 206 ranges without downloading the 126MB container or 21GB SDM archive.

The intermediate source contains **396,703 (siteid,species) positive modeled bee pairs**, **11,594 bee taxon strings** and **7,035 populated HEX cells**. Original Bombus intermediate: **171 source taxon strings**, **1,981 modeled Bombus-positive cells**, and **5,054 modeled-bee-positive cells with no Bombus**.

Geographical source Hexgon_shapefile.zip MD5 999c8c9eb6688628588d0d794ac390e1 holds **10,242** source hexagon records with genuine ID, CENTRELAT and CENTRELON. Projection is Sphere_Robinson, **not proven equal-area**, and there are 3,207 grid cells absent from intermediate modeled source data (unknown, not absence). Source georeference CI [43849439077](https://github.com/zuizui0223/adaptive-gain/actions/runs/43849439077) SUCCESS. Derived geographic source CSV artifact 14216892826, sha256 359d0c8c3c7b1d12329f5f219b24add1393d758d3b7b47d015d1f7393aeb9d11.

## B. Exact author phylogenetic and grid eligibility: the published 3,370-species frame

Original author analysis source file 4_Bee_bioregion_analysis_data_export.r MD5 **9dd9d647685c8ce684b429dd650fcb8c** and original phylogeny BEE_mat7_fulltree_tplo35_sf20lp.nwk SHA256 **7bd21fe796209e9108baf989ff3bc9f05d127aa64e67bbf8255ade93b0c74525**. Original R processes tree-tip labels to genus + species, intersects source model names with tree tips and enforces **pa_cutoff=5 distinct taxa per cell**.

| Source eligibility audit | Count |
| --- | ---: |
| Original intermediate bee taxon strings | 11,594 |
| Matching original phylogenetic source tips | 3,379 |
| After original R cell cutoff | **3,370** |
| Filtered Bombus source name strings | **133** |
| Hexagons with at least one tree-matched species before cell cutoff | 3,772 |
| Source-author eligible hexagons (>=5 species) | **2,695** |
| Eligible hexagons containing at least one Bombus source name | **1,512** |
| Eligible hexagons with 0 modeled Bombus source names | **1,183** |
| Other original global hexagons not eligible, NOT zeros | **7,547** |

This reproduces the paper's 3,370 taxon **selection number** exactly, but is **not** a full replay of all R model/simulations or a verified accepted-taxonomic list. 133 is filtered source Bombus names, not 133 independently taxonomically accepted/natively present species. Eligible cells with zero mean zero within this source model, **not documented biological absence**.

Source-focused CI [43850263676](https://github.com/zuizui0223/adaptive-gain/actions/runs/43850263676) SUCCESS. Authenticated geo HEX source artifact ID 14216053945, sha256 b772fa7f481f4e7d15d5adffcc2527e94745f1b91c752b8571a2ef7eaa954ebd; source species-filter receipt artifact 14217935078, sha256 0f720516888582c5091a1c4646fdea67a4185ce8fa9e50af0639f5eb2f114d38. Exact source scripts in research/floral_visual_macro_stage46, including ZIP-range-catalog, extract_bee_pa_matrix, derive_bombus_hex_prediction, georeference_bombus_prediction and author_tree_filtered_bombus.

## C. Floral visual signal × geographic pollinator prediction

Research hypothesis: geographically distributed flower UV guides and other visual signal structures are associated with the **native environmentally available visually capable pollinator guild**, conditioned on lineage, geography, vegetation, climate and observation effort. This is **not** the simplistic relationship between conspicuous flower colors and GBIF Bombus record counts, and Bombus-only guilds are not representative of tropical/other contexts.

Stage45 original UV seed: 80 Brazilian Cerrado source taxa, 26 real UV patterned; 71 matched exact GBIF taxa. NHM global 59,369 taxa had 32,183 recorded visible colour entries and 353 unverified marking text candidates, which are NOT independently measured UV guides. Those plant records have NOT been joined to the original bee HEX polygons. **No published positive UV × Bombus association or coefficient, plant fitness, behavioral cognition or evolutionary adaptation is inferred from this source-preparation stage.**

Required next: independently verify plant source occurrence coordinates and taxon keys, true **point-in-polygon** source bee hex-grid assignment, classify botanical guide measurement evidence, native/introduced source review, and match temporal/spatial sampling effort before a climate/phylogeny-controlled spatially blocked comparison. Source region and guild context must be modeled; missing plant/bee record cells must not silently become zeros.

## D. Workflow provenance

Direct download of the 126MB published data.zip failed HTTP 406; limited HTTP byte Range 206 calls succeeded and the original ZIP member and 13MB geography sources passed ZIP CRC/MD5 checks. The legacy full-file-fetch workflow is now preserved manual-only; the actual new source-preserving range workflow has source CI success.

The experimental UV/flower-pollinator geographic joint hypothesis is prospective, not verified. Keep this branch Draft/unmerged and preserve main and Stages37-44 wind work.
