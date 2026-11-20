# Stage111 — Full original 72 mainland exploration regions: ERA5 0.25° grid budget and 3 new block source masks

**2026-11-21 JST.** The scientific priority is still to test whether wind physically reallocates the utility of near-field visual markings, far-field display size, and olfactory floral signals across plant species/regions, conditional on pollinator information/learning costs. This stage ONLY audits the physical geography and publicly accessible ERA5-model retrieval burden; it does not estimate cue effects.

## Genuine state at the beginning

Stage109 succeeded with Open-Meteo-delivered ERA5 MODEL daily 1991–2020 two true area-weighted WDC cells, showing 10m daily max gust>15m/s on 7.2313% of climatologically warm-month days. Stage110 succeeded twice with original 16 Delaware / 18 Cabinda actual land-grid centres and all 10,958 daily model dates per cell; original area-weighted gust>15m/s was Delaware 11.2297%, Cabinda 0.0000%. These are **model-derived public daily ERA5 values**, NOT original byte-verified ECMWF-CDS hourly 10fg. The original 72 contact-free mainland exploration regions cover **17 geographic blocks**; the completed source 3 regions belong to only **2** blocks.

The directly full-grid source route to ALL 72 original regions must be scoped before making thousands of provider historical archive requests. Original Stage94 exact accepted mainland 367→125 regional classification and Stage98B strict 72 exploration/37 unchanged holdout frame were selected by source geography, not reported floral/pollinator/wind traits. All 37 holdout floral outcomes remain unopened.

## Source geometry, coverage and explicit retrieval bounds

Use original source ZIPs:
- Stage94 original 367 TDWG3 topology + 125 strict mainland source registry: SHA256 **3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833**, original artifact 14529576121.
- Stage98B original geography-only 72 contact-free mainland exploration and unchanged 37 holdout region identifiers: SHA256 **8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7**, artifact 14537927849.
- Source-original TDWG WGSRPD level3 polygon GeoJSON Git blob SHA1 **91104e5159e31f88154833a51d3b0d1c9271083f**.
- Independent Natural Earth physical land ZIP SHA256 **e547d749445eaa0964aba76738090ec88f5e63c4585122170f98c67a7ea922dc**; continent-connected landmasses picked by original anchor point rule (exclude named large islands).
- Original Stage106 0.25° WGS84 geodesic cell-footprint intersection algorithm, not an ad hoc approximate equal-weight regional mask.

Each frozen source mainland training region has its original source land area and original TDWG polygon hash checked. We estimate a **strict geometrical lower bound** on the number of intersected 0.25° cells by dividing the real source land area by 800 km² (a conservative upper bound on one 0.25° latitude/longitude WGS84 cell area, maximal at the equator). This bound is NOT the exact cell count: many cells partly intersect coastline, mountain/lake/complex regional land geometry, and many small polygons occupy more edge cells. A loose bounding-box grid-count upper envelope is separately kept; antimeridian unsupported source bounds are explicitly flagged rather than silently accepted.

An independent source region requires at least 3 decade source responses per 5 original site grid centres over original 1991–2000, 2001–2010, and 2011–2020 calendar periods. Summing the per-region geometric cell lower bounds and the per-region 3×ceil(lower_cells/5) source query lower counts describes the scale of an **independent region-by-region** Open-Meteo model acquisition. It deliberately does not optimise reuse of identical ERA5 model cells appearing in adjacent floristic regions, which could lower global API load. This conservative scale audit is not permission to exceed Open-Meteo public fair-use quotas.

## New geography-only source pilots, independent of biological outcomes

Preselect three new representative source geographic blocks that have **not** been represented by the completed source WDC/DEL/CAB regions. Algorithm:
1. Fix the original contact-free 72 mainland region codes and original 17 block assignments.
2. Exclude WDC/DEL and CAB represented source geographic blocks from new acquisition.
3. Among remaining original source regions, require original mainland area ≤40,000 km² and original polygon not repaired; sort by original mainland land area then TDWG source code.
4. Take one smallest original source mainland region in each unrepresented geographic block until three distinct new blocks are identified.

With the original immutable 72-region source map, this yields geographically preselected **GAM, KRY, BGM** source codes (do not use trait outcome or wind value to change selection). For these three alone, load original TDWG source polygons, clip to original actual continent-connected Natural Earth land and compute the **exact geodesic mainland km² intersection with every 0.25° ERA5 model grid cell**; require sums of source cell land intersection areas to agree with source polygons within 1.5%. Give their exact land-cell centres, source regional total land area, effective area-weighted grid-cell count and number of 5-site×three-decade model requests. The names are original TDWG3 source codes, not global ecological gradient strata. This is a source selection to demonstrate broader climatological retrieval, not a statistically representative sample of all 17 blocks.

No 1991–2020 daily Open-Meteo request is submitted in this **geometry** stage. It creates an auditable low-cost acquisition plan, not a grand claim that 72 complete source AREA-weighted winds already exist. This is deliberately separate from original Stage105 (33-region point-based 1991–2020 gust vs reporting bias) and Stage107 (72-region **WorldClim 1970–2000 mean wind**, NOT gust).

## Scientific constraints before any floral-effect test

Even with fully populated ERA5-model climate cells, original source floral marks are a lexical subset of NHM botanical descriptions rather than proven UV nectar guides, WFO positive scent phrases are positive *source reports* rather than actual VOC flux, and exact flower diameter data are only 104 original AusTraits measured-source species + 212 unreviewed WFO original size report species with intervals/upper bounds/singletons, exact union 312. The original source documentation covariates are themselves geographically correlated with gust. Structural paths from wind to source reporting intensity, pollinator distributions, latitude, temperature, clade composition and mainland land exposure remain major confounders. Do NOT claim that sensory-cue order, bee learning cost, or reproductive selection is measured in these data.

The outcome-blind geographic 72 exploration and unchanged 37 holdout remain the only allowed original source splits, while Stage99 showed substantial exact species reuse between them. No accepted evolutionary result from Stage111 source geometry alone.

## Source implementation

- research/floral_macro_stage111/original_mainland72_era5_geogrid_budget.py
- research/floral_macro_stage111/test_original_mainland72_era5_geogrid_budget.py
- .github/workflows/floral-stage111-mainland72-ERA5-grid-demand.yml

Empirical exact new-region grid counts and overall 72-region source bound counts are to be copied only from a genuinely succeeded original SHA-verified Stage111 GitHub Actions run.
