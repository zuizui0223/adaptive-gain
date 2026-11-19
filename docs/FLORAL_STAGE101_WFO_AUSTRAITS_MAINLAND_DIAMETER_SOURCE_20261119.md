# Stage101 — Exact WFO prose flower diameter vs original AusTraits native species overlap on mainland

**2026-11-19 JST.** Source coverage and taxonomic generalization audit only, not an estimated wind-gradient flower-size effect. Draft intended to be stacked on Stage100 #179; main unchanged.

## Main question

The existing independently verified AusTraits v7.0.0 source provides **104** true source-labelled flower_diameter species in the 55,775 WCVP-native global plant pool, with only **19 unique new holdout species** versus contact-free exploration. Stage100 independently scanned original WFO Flora of China / Flora of North America full botanical descriptions and identified **237** unreviewed source prose phrases referring to whole-flower diameter and **58 corolla width only** species, with the original WFO taxonomy/prose codebook and underlying archives independently byte-checked.

The two collections may describe exactly the same plant species. Therefore 104 + 237 is NOT the verified global whole-flower size species count. Stage101 calculates that overlap from the immutable original source-specific species identity records and reports a correctly deduplicated *source-available* union.

## Distinguish data grades

- **A (measured-source labelled)**: AusTraits 7.0.0 original dataset flower_diameter, with original source mm/cm physical units and exact accepted WCVP species mapping. Not necessarily bee-visible detection area.
- **B (botanical textual candidate)**: explicit WFO source-prose whole flower diameter in mm or cm, numeric-only, organ-aware and source-preserving. This remains **unreviewed lexical extraction**, and is never automatically treated as independent measured flower diameter.
- **C (corolla width only)**: 58 previously identified WFO prose species with width of the corolla; **excluded entirely from the A-or-B whole-flower diameter union**, but counted as a separate possible morphological axis.

Record original A, B, A-and-B exact overlap, B-only, and A-union-B source counts, and whether originally independent WFO/AusTraits dimension values agree (ratio only, no assertion of same developmental stage, population, geometry, or phenotype). The exact genus counts for source-positive species are descriptive and do not establish independent evolved transitions.

## Geography and temporal barriers

Use independently source-authenticated Stage98B contact-remedied **72 continental exploration vs unchanged 37 mainland holdout regions**, retaining all 16 source original excluded training areas outside ecological analysis. All source species are Kew WCVP accepted-native, and a single original species can occur in many TDWG3 regions, so original regional repeated presence cannot be treated as a new measured plant or phenotype. Do not alter the 72/37 split based on source size, wind or floral response.

Report 109 mainland source-region counts at cutoffs 5 and 10 candidate source species, retaining A and B grades separately. A *source-available B* species is NOT equivalent to biological validation of flower size. Any resulting increase in global coverage or heldout coverage is **a new acquisition opportunity**, not evidence of stronger far-distance visual attraction.

## Original identity and reproducibility

- Stage100 original WFO species-level source-candidate ledger will be required with an exact artifact SHA256 fixed after successful source-specific CI.
- Original AusTraits v7.0.0 ZIP SHA256 2995fb9e5eebf9271f9241b5a6c2e2cbb7b45e8eda5ce4db43c14c68f95e2f3f is re-read rather than trusting only its 367-region aggregate.
- Original accepted WCVP ZIP SHA256 d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa and original NHM source CSV SHA256 b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a define the 55,775 original native species.
- Stage98B original 72train/37holdout contact-free derived ZIP SHA256 8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7.

## Scientific claim ceiling

No 125-region land-area-weighted original CDS hourly ERA5 10fg source has been recovered; Stage97's 50 original 30-year points are not a substitute. Source size reporting can correlate with botanical research intensity, floristic family, continent and region. A new WFO prose candidate must be manually rechecked against its original botanical treatment before final biological size comparisons. No source scent VOC emission, pollinator receptor detection distance, acquired bee learning, flower choice order, or fitness is observed. Do not fit ecological wind×size effects or assert wind adaptation from this acquisition audit.

Code:
- research/floral_macro_stage101/verify_original_WFO_AusTraits_diameter_union_mainland.py
- research/floral_macro_stage101/test_verify_original_WFO_AusTraits_diameter_union_mainland.py


## Real-source Stage101 validated results (2026-11-19)

Original [Actions #44547835621](https://github.com/zuizui0223/adaptive-gain/actions/runs/44547835621) **SUCCESS** (6 independent source-free guards plus original source and derived artifact SHA). Derived-only artifact ID **14541990862** SHA256 **caca7afc84736cfd3eda0c93fd0e69b8e6434383950ec7b6ef1ff37e5e116656**.

**Exact source species identity, not inferred by region:** original AusTraits v7 measured-source flower_diameter **104 species**, WFO 2026 China/FNA botanical prose whole-flower diameter **237 *unreviewed* candidate species**; exact accepted species overlap **4** and deduplicated A-or-B evidence **337 species** (only **104** remain original measured-grade). WFO corolla-width-only 58 species were excluded from the diameter union. Four source-overlap numeric ratios had median WFO prose mm/AusTraits mm **1.1053**, and 3/4 were within 0.5 to 2; this is insufficient to establish measurement comparability or accuracy.

| Original source coverage, strictly mainland | 72 exploration | 37 unchanged holdout |
| --- | ---: | ---: |
| Regions with >=10 original AusTraits measured-grade species | **23** | **4** |
| Regions with >=10 source-original WFO prose diameter candidate species | **36** | **16** |
| Regions with >=10 A-or-B evidence, exact-species deduplicated | **47** | **20** |
| Regions with >=5 A-or-B evidence, exact-species deduplicated | **66** | **33** |

The fixed holdout contains **195** A-or-B source-available species, of which **104** are absent from the geographically contact-free 72-region exploration source set. Unlike the reported native plant global flora where multiple regions repeat identical taxa, this statistic explicitly avoids double-counting accepted species names *within each cohort*. It does not independently verify WFO morphological extraction quality or phylogenetic evolutionary transitions.

**Claim limit:** This is improved *candidate information availability* and a separate measurement-validity bottleneck, not a wind-related biological effect. The newly added 233 WFO-only species are unreviewed prose cues. Original WFO geographic source coverage remains heavily China/North America biased, pollen vector often unknown, and no regional area-weighted verified original CDS 1991–2020 hourly gust exposure is present. Next scientific gate is source-text extraction quality review stratified by source and morphology, not ecological model fitting.

