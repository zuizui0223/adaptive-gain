# Stage66 — original global flower colour × modelled bee guild macro results

**2026-11-17. User-directed pivot from 8-image visual marking checks to original-source global macroecology. Draft PR #145, base Stage65 PR #144. Main untouched.**

## Input provenance / biological boundary

The FCP original immutable pixel-derived source from [FCP release](https://github.com/zuizui0223/fcp/releases/tag/fcp-all4730-original-method-actual-colour-results-20261017) contains 447,500 actual photographed flower image measurements across 4,475 taxa; 227,107 photos have the originally classified coarse human-visible four-colour state. Original gzip SHA256: 8e7f10f0427927208485b2da6fa9c46bb681d6f3611e53b8dfdc606cfc8dabe6. Four-state photograph colour is **not an UV pattern, visual guide, nectar guide or measured pollinator information**.

Laborieux et al. [original bee source](https://doi.org/10.5281/zenodo.20525239) contains 10,242 original Robinson-projected source HEX polygons. Original author phylogeny and >=5 bee taxa per cell criteria leave **2,695 eligible modelled cells**, with 1,512 modelled Bombus-positive, 1,183 modelled Bombus-zero, and **7,547 unmodelled cells that are UNKNOWN (not true zeros)**. Authenticated original author-filtered CSV SHA256 d260b18be05a2ceac87a49fddd0645734d56c6246f80321c1c577f261dd5cee4.

Original FCP WorldClim 2.1 10-arc-minute BIO5 temperature and BIO12 precipitation archive SHA256 00513224583665ec0f2f955a4ec252730c4deb2004cce9e793492a3f26df4dcf. Use only FCP source classified photo coordinates with reported positional uncertainty <=5,000 m, and original source polygon exact point assignment in the published projected CRS. Not an independent pollinator observation source or matched native range.

## Authenticated actual macro data join — passed in GitHub Actions 44025370724

- Original FCP: 227,107 classifiable photographed flower colours; **227,078** with genuine georeferenced temperature/rainfall normals.
- Matched original author-eligible bee model: **209,464** source photograph classifications and **all 4,475 original plant species**, within **1,618** different source-author eligible HEX.
- Species×HEX fractions, not photos as pseudoreplicates: **92,010 species×HEX** observed units.
- At least two eligible modelled HEXs per plant: **4,447 species and 91,978 units**. **4,001** have within-species nonconstant modelled Bombus/all-bee fraction.
- >=3 classified photos per plant species×HEX: **3,560 species, 686 HEX, 17,524 species×HEX units**; 2,845 have nonconstant modelled Bombus exposure.
- Actual source result [Actions run 44025370724](https://github.com/zuizui0223/adaptive-gain/actions/runs/44025370724): **SUCCESS**, artifact **14302687793**, CSV SHA256 **90cb8620b4c007e3a04b06121c0b75550fb3c176f17794b21b8295031d669da4**, JSON SHA256 **18e755be03e776f7f2da12cb6c904815669a3d1b603bfe632bab58211de6bf65**. No individual original photo IDs, observer identity or precise photographed locations distributed in output.

## Within-species source-based macro model

Four-state colour photo fraction, modelled as a function of modelled Bombus/all-bee name-range overlap fraction (per +10 percentage points), log(all modelled bees), signed/absolute latitude, sin/cos longitude, BIO5, log1p(BIO12). Each plant species receives one total weight across source HEX, not each original photograph. Source global stage bootstrapped original genus clusters (499) and recomputed coefficients after >=3 photos per species×HEX.

Added exploratory posthoc **two-way robust uncertainty**: cluster original plant taxon AND source-model HEX, subtracting the intersection score component to account for shared modelled guild exposure/geography. This is not a spatial out-of-block prediction or true molecular phylogeny control.

| Visible photo coarse colour | >=1 original classified photo/cell: change in colour fraction per +10pp modelled Bombus, 2-way posthoc 95% | >=3 original classified photos/cell: same |
|---|---|---|
| White | +0.835 percentage points [ +0.311, +1.360 ] | +0.672 pp [ −0.370, +1.715 ] |
| Yellow-orange | −0.079 pp [ −0.471, +0.313 ] | +0.086 pp [ −0.775, +0.948 ] |
| Red-pink | −0.323 pp [ −0.609, −0.037 ] | −0.663 pp [ −1.225, −0.100 ] |
| Blue-purple | −0.433 pp [ −0.725, −0.141 ] | −0.096 pp [ −0.752, +0.560 ] |

**Incremental descriptive within-species R² by modelled Bombus share in >=3 original photos/cell:** white **0.000147**, red-pink **0.000333**. The effects are extremely small; do not claim adaptive colour or visual information based on a confidence interval. Intervals are posthoc and unadjusted for 4 tested colour outcomes; source sampled/introduced status and photo classification error remain major selection issues.

## Geographic replication falsification

After seeing the source global coefficients, used the physically defined 23.5° tropical boundary, each plant species required at least two **within-region** source HEXs. Collinearity of signed latitude and absolute latitude inside one hemisphere requires removal of the latter within-region, so zone coefficients are **not identical-model conditional effects**. All follow-up regional intervals are posthoc and include original-species and original-HEX score clustering.

At the >=3 photos per species×HEX limit:

| Region | Species | Original HEX | Species×HEX | Red-pink change per +10pp modelled Bombus (two-way 95%) |
|---|---:|---:|---:|---|
| North extratropics | 2,870 | 469 | 14,596 | −0.45 pp [−1.22, +0.32] |
| South extratropics | 591 | 120 | 2,081 | −1.17 pp [−2.41, +0.07] |
| Tropics | 156 | 94 | 612 | +2.64 pp [−2.53, +7.81] |

At >=1 photo/cell the tropical red-pink sign is positive (+3.50 pp [ +0.65, +6.36 ], 595 spp), unlike the global slope. **The global red-pink minus is not regionally replicated under the >=3-photo gate, so cannot be described as a global universal rule**. Regional comparisons have different plant assemblage and source photo density; not a species-disjoint external replication.

## Scientific claim ceiling and next real macro step

The new **large real database intersection** is achieved. However, general flower colour adaptation to modelled Bombus availability, and the hypothesized conditional wind×VOC×visual information routeability, **remain unproven**. Native plant range is not independently confirmed, bee counts are modelled presence-range names rather than visits or density, temporal synchrony not shown, and broad RGB human colour is not a localised sensory cue.

To seek a real novel ecological mechanism, the next predeclared work must filter plant native range versus ornamental introductions and apply heldout geographic domains, then attach independent actual spatial UV trait evidence at **documented collection places**. The 230 genuinely UV-pattern-measured species from older source studies form a **separate evidence layer**; they cannot be inflated into FCP 4,475 photo species or borrowed as if measured on matched iNaturalist photos.

## Reproducibility

- Original global macro: research/floral_visual_macro_stage66/original_FCP4475_beeHEX_coarse_colour_macro.py
- Plant species + source HEX double-cluster uncertainty and zones: research/floral_visual_macro_stage66/original_2way_species_and_author_HEX_robustness.py
- Original public image/bee/climate source workflow: .github/workflows/floral-stage66-global-FCP-bee-HEX-macro.yml
- Two-way/source-regional replay workflow: .github/workflows/floral-stage66-real-two-way-spatial-cluster-QC.yml
- GitHub Actions 44025370724 saved the original authenticated 92,010 species×HEX artifact. Two-way source replay must verify both original CSV and source JSON SHA256 and exactly match the original four-colour coefficients before reporting any additional intervals.
