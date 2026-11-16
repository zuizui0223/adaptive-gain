# Stage49 CURRENT — 262 source-authenticated, GBIF-accepted literature visual-trait species

**16 November 2026 JST. Updated evidence supersedes the early source-acquisition status in RESULTS_ORIGINAL_LITERATURE_VISUAL_SPECIES_TO_GBIF_20261116.md.** Research aim: species-level measured UV spatial flower structures × geographically modeled pollinator guilds. No new geographical UV×Bombus association was fitted.

## Actual completed original botanical species registry

| Original study | Original evidence unit | Taxonomic source result | Directly UV spatially patterned? |
|---|---|---:|---|
| Koski & Ashman 2016, *New Phytologist*, doi:10.1111/nph.13921 | 177 original Potentilleae source taxon/variety rows, with UVP, author pattern code, human-visible colour, average latitude/altitude, annual temperature/precipitation and UV-B | **164 mapped source rows → 159 unique GBIF accepted species** | **Yes**, 86 source taxon rows patterned; 91 UV-uniform |
| Tunes et al. 2021, *Frontiers in Plant Science*, doi:10.3389/fpls.2021.618028 | 80 real Brazilian-savanna source taxon rows, five original optical UV categories | **71 mapped source rows → 71 GBIF accepted species** | **Yes**, 26 of the 80 original taxon rows in patterned categories (BE7, CM4, CR15); 54 uniform |
| Koski, MacQueen & Ashman 2020, *Current Biology*, doi:10.1016/j.cub.2020.08.077 | 45 continent × taxon Table S1 records, 1,238 original historical specimens; 41 literal binomial names vs 42 in article wording | **40 mapped accepted species** | **No binary pattern outcome in Table S1.** This is UV-absorbing pigment-area temporal slope and anatomy/continent data |
| **Accepted-key union of three papers** | **275 mapped original study×taxon records** (164+71+40) | **262 distinct accepted GBIF species** | **230 species directly source-classified spatial UV pattern; 32 have UVP-time-series only** |

The accepted-key deduplicated, true source-measured spatial-pattern output is:
- **101** distinct accepted species with UV spatial pattern
- **129** distinct accepted species classified UV-uniform
- **32** accepted species with only historical UVP temporal trend, kept **unknown** for binary UV pattern
- **0** conflicts between source-measured spatial-pattern labels after accepted-key deduplication

These 230 direct source classifications do **NOT** all measure a strictly homologous nectar-guide trait. The 2016 study measures petal UV absorption/bullseye state; Tunes 2021 classifies UV bullseye, corolla marks, *and contrasting reproductive structures*. The broad derived binary is **UV spatial contrast vs uniform**, with subtype and study held separately. Neither directly establishes receiver learning, information use, pollen placement or fitness. The 2020 UVP temporal slope must NEVER be converted to guide positive/negative.

## Important newly recovered 2016 primary data

Original 2016 supporting PDF Table S2 was downloaded through the official Europe PMC OA supplementary API for PMCID PMC6681094, after Wiley direct supplement download returned HTTP 403. Official embedded file `NPH-211-708-s001.pdf` SHA256 **8936dc9dabc8e96d37ba98ef6c940c98d545b62f3260634bce8dfd0a4f74bd94**. The API ZIP container digest changes upon repackaging, so **the immutable embedded PDF SHA** is the accepted source identity gate.

The 2016 original Table S2 has exactly **177 taxon rows**, with source code **0 = UV PATTERN PRESENT** and **1 = UV UNIFORM**. The original Figure 2 counts **86 pattern / 91 uniform** are reproduced; *Potentilla crebridens* is coded pattern present despite printed two-decimal UVP=0.95, so the original discrete category is retained and the rounding discrepancy separately reported. Two long *Ivesia lycopodioides* infraspecific codes wrap across lines in the PDF and were faithfully reassembled without changing the phenotype.

Table S1 in the **same PDF** supplies author full genus/epithet matches to **168/177 original S2 source codes** (164 unique source binomials after four infraspecific multiple-record labels). Nine source codes remain unmatched to Table S1 and are not given invented names. Strict GBIF (Plantae, SPECIES, EXACT full name, confidence >=95) matches **164/177 original rows**, providing **159 unique accepted species keys**. Four of the 168 full-name candidates do not meet strict GBIF confidence. There are **no conflicting directly source-measured UV states among multiple source rows mapping to one accepted key**. This is accepted taxonomy matching, not native-range reconstruction.

Authentic source success:
- Direct original 2016 Table S2 and UVP source categories: [Actions 43861208761](https://github.com/zuizui0223/adaptive-gain/actions/runs/43861208761)
- Original Table S1→S2 full names: [Actions 43861717952](https://github.com/zuizui0223/adaptive-gain/actions/runs/43861717952)
- Strict GBIF accepted keys: [Actions 43862161335](https://github.com/zuizui0223/adaptive-gain/actions/runs/43862161335), source artifact **14224660534**, digest `sha256:c041b41fb89b067ca8ceff741f37b863e5344c126e1d4bcfff0646912634d65a`.

Older source evidence:
- 2021 80 taxa PDF source SHA256 `d11b41a36d85d1b70c8d3d47c04f3e03e7d8f5f58ebaaa331a737e56ed4c2820`; note Table S2 R7/CM4 vs paper prose R6/CM5; preserve Table S2.
- 2020 Table S1 original source PDF SHA256 `180c0cfbfb74219edfeae8c3596b7a815968aa30fb10d82cd022debe426646e6`; 45 continent-taxon records with 41 literal binomials, *not* 42 after string dedup. Original per-specimen Dryad .xlsx remains inaccessible (401/403), but PDF Table S1 was separately source-verified.
- 121 original 2020/21 taxa strict GBIF crosswalk: [Actions 43859048339](https://github.com/zuizui0223/adaptive-gain/actions/runs/43859048339), artifact **14223205344**, SHA256 `065c0aacdb7e0c079ccca54e581bc7066c8ba63b9aaf7357010e964931176f59`.
- **Current combined accepted-key union**: [Actions 43863056927](https://github.com/zuizui0223/adaptive-gain/actions/runs/43863056927), artifact **14223762235**, ZIP digest `sha256:ef017df8069183dc16f508a85afdd75e0b34f6f56645e499d738c51b7c97731d`. Source-original 2016/2021 input artifacts are independently authenticated and ingested with Actions/download-artifact; output file `literature_directly_measured_UV_species_GBIF_unique_accepted_registry.csv` contains **262 distinct accepted keys**, source DOI lists, original subtype/provenance, and optional binary pattern or missing for 2020-only.

## Critical inference and actual next ecological test

The global original bee source was separately source authenticated in Stage46: 10,242 original HEX cells, published phylogenetic/PA species filter to 3,370 bee species strings, 133 original Bombus species name strings, **2,695 eligible bee-model HEX**, and **7,547 out-of-eligibility HEX as UNKNOWN rather than Bombus absence**. These are historical species range/polygon modeled overlaps and cannot be interpreted as independent observed bee abundance, realized effective pollination, or native populations.

**The 230 true UV-spatial-pattern-labelled plants now enable a serious geography-based hypothesis** only once the **species' actual validated distribution/collection locations are aligned to the SAME bee-model HEX**. The 2016 paper's average latitude/UV-B climate values are valuable published covariates but **cannot alone identify which original bee HEX each taxon occupies**, because a mean location is not a presence record nor its accessible native range.

Predefine:
1. Accepted GBIF species key, native/source geographic range, true source occurrence points and source-documented spatial uncertainty, then exact point-in-polygon link to source bee HEX — no nearest centroid, no per-source absence imputation.
2. Exposures: predicted Bombus **species richness/modelled ranges** and other visually capable bee guild species in corresponding model-eligible HEX, plus climate, solar UV-B, sampling and plant lineage/phylogeny.
3. Outcome: paper-verified spatial UV-pattern vs uniform only (n=230 currently). Keep 2016 petal UV pattern vs 2021 reproductive/whole-corolla contrast subtype, isolate the regional Brazil study with study/bioregion blocks. Long-term model should test a prespecified guild-specific interaction, not a single global correlation driven by source/latitude.
4. Model and evidence gates: spatial block + source study holdout, phylogenetic clustering, species range-size/presence sampling, native/introduction flag, observation missingness and a guild model source uncertainty guard. Verify a sufficiently large common native geographic domain before fitting any coefficient.
5. No claim today of measured visual decision-routing behaviour, guide-dependent pollination, plant fitness or adaptive selection from these taxon correlations.

**Result status:** an actual reusable source-grounded **262 accepted species, including 230 verified spatial UV-phenotype statuses**, rather than an unverified proposal. **No UV×Bombus spatial association fitted yet**. Keep this development PR Draft/unmerged and main unchanged.
