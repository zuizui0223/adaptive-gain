# Stage47 — original UV-study site × source-filtered bee-HEX applicability test

**2026-11-16 JST. Original geographic evidence and source-derived predicted bee ranges, no new UV-pattern × Bombus association or fitness effect.**

## Goal and data identity

The 2021 original UV-photo+spectrophotometry study (Tunes, Camargo & Guimarães; doi:10.3389/fpls.2021.618028) sampled 80 plant taxa during 2019–2021 at three explicitly reported natural study localities in southeastern Brazil. Original article gives two single DMS coordinates and a latitude/longitude RANGE for Santa Bárbara; individual UV-measured taxa are NOT assigned to these three original sites in the source Table S2. The original 80 categorical UV labels are source-verified in Stage45 (26 spatially UV-patterned; 54 UV-uniform).

Global pollinator modeled source: Laborieux et al. 2026 PNAS, Zenodo data DOI 10.5281/zenodo.20525239 (record 20525240), original phylogenetic+per-cell eligibility exactly reproduced in Stage46: 3,370 retained bee taxon strings, 133 original modelled Bombus names on 2,695 study-eligible cells of the original 10,242 global HEX geometry. Original hexgrid ZIP MD5 999c8c9eb6688628588d0d794ac390e1 and projected .prj SHA256 8e813fd52a034fb7139cec28b290a856ccc81ac092658441b38925c6e7d46d5a, CRS Sphere_Robinson.

This Stage47 **uses original polygons** (SHP+SHX+DBF+PRJ) and WGS84 → original CRS transformation, exact point-in-polygon and no nearest-centroid matching or guessed grid cell. Santa Bárbara originally reports a range, NOT one representative point; evaluate all four corners and a midpoint. Modelled species-name counts are not independent pollinators, native species richness, visitation, potential fitness, or habitat probability.

## Actual authenticated study-site results

| Original study locality | Published location support | Original HEX IDs | Modeled source Bombus names | Modeled all bee names | Interpretation |
|---|---|---|---|---|---|
| Botucatu, São Paulo | -22.9125, -48.503611 (original DMS) | HEX8285 | 4 | 132 | One HEX assignment |
| Santa Bárbara Ecological Station, São Paulo | latitude -22.766667 to -22.683333; longitude -49.266667 to -49.166667 (published extent) | HEX8285 **or** HEX8318 | 4 **or** 3 | 132 **or** 137 | The source geographic interval **crosses the two model cells**; do not choose one arbitrary midpoint |
| Serra da Canastra National Park, Minas Gerais | -20.233611, -46.444444 (original DMS) | HEX8252 | 4 | 124 | One HEX assignment |

The three study localities intersect **three distinct original author-eligible model HEX cells** (HEX8285, HEX8318, HEX8252). All three have a positive modelled Bombus source name count (3–4); **zero** sampled HEX is an eligible Bombus-zero cell and **zero** is outside the original study eligibility. All-bee model counts are 124–137 (modelled phylogeny-filtered taxon strings). The Santa Bárbara ambiguity means there is not a uniquely assigned local Bombus predictor, and Botucatu/part of Santa Bárbara share HEX8285.

**Critical feasibility conclusion:** There is *some* geographical variation in author-modelled Bombus range overlap in the source UV-study region, but there are at most **three source HEX cells** and no verified UV taxon×study-site membership. Therefore a species-level UV-guide × Bombus coefficient (with phylogeny, climate and regional background controls) **is not identifiable from these original 80 study taxa and site coordinates alone**. Do not generate a spurious correlation by assigning an original UV species to an unrelated GBIF occurrence coordinate or treating all taxa in the study as if independently sampled at all three sites. In this source set, the comparator across other bees has slightly more model-variation (124/132/137) but still only three cells and no species/site labels.

## Direct next data acquisition priority

1. Expand **source-measured** UV guide categories, including wild plant populations at several biogeographic regions. Existing candidates for independent source audit: Koski & Ashman macroevolutionary Rosaceae UV-pattern taxon dataset (177 species); Koski–MacQueen–Ashman 2020 geographically repeated 42 species on three continents (Dryad 10.5061/dryad.ttdz08kw1); other original UV-sector photographic/spectral surveys. Data must have actual source taxon/UV patch fraction and sampled locality, not pigment chemistry or generic UV spectral reflectance alone.
2. Pair modeled bee community with the **same** independent plant guide-study coordinates and source period, or collect species/collection region provenance from source museum records. Record native species, model type (SDM vs convex-hull extrapolation), climate, solar radiation and other visually capable bee guilds.
3. Keep incomplete source HEX as **unknown**. At most use this Stage47 map as an *applicability gate* for the original 2021 dataset, not a hypothesis test.

## Reproducibility and STOP

- Script: `research/floral_visual_macro_stage47/align_uv_study_sites_to_bee_hex.py`; existing Stage46 source-authenticated matrix, tree, R pa_cutoff, original Polygon archive retrieved at runtime. No original shapefiles or source bee rows copied into Git.
- Five offline synthetic shape/CRS no-go unit tests; source original Actions run [43852375431](https://github.com/zuizui0223/adaptive-gain/actions/runs/43852375431) **SUCCESS** (initial code head).
- Only derived three-site/candidate source-HEX JSON and receipts saved as GitHub Actions artifacts. Check final-head source CI and whole repo Python 3.10–3.12 separately before software acceptance.
- No independent wild *Bombus* individuals/visitation, no flower-guide user behaviour, actual flower pollen deposition, seed set or adaptive evolution were measured in Stage47. Draft/unmerged; main and wind branches left unchanged.
