# Stage87F: Global spatial Bombus data-quality stress test

2026-11-18 JST, original-source GitHub Actions #44292016726 SUCCESS.
Derived artifact **14420869553**, ZIP SHA256 b743bf81776f95115d71d219dc316b438d76eb676be7fa3f4ca526ba5dbc3b48. Inputs immutable Stage87C Global native NHM 367 WCVP regions + 5 WorldClim climates ZIP SHA256 4c0ab25596078be4b2aa35a254e42695fd260e1720864e173970aac8aa7db83a; Stage87D original 3,958,417 GBIF Bombus records in 165 observed-positive regions ZIP SHA256 2fe7510fe8c08189d63151fe255a00baafb96c7acc87d3d0fedc970966ca1a43.

## Cohorts and construction

Actual Stage87E prior positive-only, source-complete, no repaired GIS regions: 139 TDWG3 regions with ≥50 documented one-hue botanical species, ≥5 unique observed GBIF 1° cells, ≥1 bee species supported by ≥3 occurrences in ≥2 distinct 1° cells, five climatological variables. The entire 367-region global matrix retains 202 original regions without reported archived Bombus occurrences as UNKNOWN, not zeros.

Vary one independent source quality definition at a time:
- Original GBIF source ≥10 distinct reported 1° cells: **109** regions.
- GBIF ≥20 distinct reported 1° cells: **76** regions.
- Original NHM ≥100 explicit single hue species before the bee outcome: **135** regions.
- Original stricter species-qualified richness using GBIF coordinate-uncertainty ≤10 km records across ≥2 1° cells: **139** original positive regions.

Each scenario refits all 11 original NHM lexical hue categories, both botanical-species pooled and genus-balanced composition; model conditions on climate, latitude, longitude, documented hue coverage, hue flora number, recorded grid-cell coverage and observed Bombus richness as well as wind×richness. Standardize covariates WITHIN each cohort; do not compare magnitudes as the same geographical exposure range. BH correction over 11 predefined hues is exploratory; repeated analyses and source bias remain uncorrected by the nominal q values.

## Real source stress-test findings (genus-balanced, original hue fraction points per within-cohort 1 SD log Bombus richness)

| Source sample quality | N regions | Yellow hue beta (exploratory 11-hue BH q) | Purple hue beta (exploratory BH q) |
|---|---:|---:|---:|
| Archived primary GBIF, ≥5 cells | 139 | **+0.0225** (q <0.001) | **−0.0135** (q <0.001) |
| Source positive ≥10 cells | 109 | **+0.0184** (q <0.001) | **−0.0082** (q=0.042) |
| Source positive ≥20 cells | 76 | **+0.0168** (q=0.015) | −0.0074 (q=0.165) |
| NHM documented ≥100 one-hue plants | 135 | **+0.0193** (q <0.001) | **−0.0116** (q <0.001) |
| Alternate ≤10 km uncertainty richness | 139 | **+0.0255** (q <0.001) | **−0.0121** (q=0.002) |

Yellow genus-balanced positive is consistent in all 5 archived-source definitions. Purple genus-balanced remains negative in all 5 but loses nominal 11-hue significance at high recording effort ≥20 cells. **This is not an insect preference for yellow and against purple flowers.** Source floristic distributions and GBIF observed richness are derived independently, but recorded species richness is strongly associated with sampling coverage (in source accepted 139-region cohort, Spearman rho=+0.767 with number of GBIF 1° cells), and sampling intensity by non-Bombus insects is unknown. A proxy of occupied recorded Bombus grid cells is not target-group background or verified species richness.

## Wind × bee: not source-robust

A positive wind×recorded-Bombus interaction for white lexical hue emerged only in genus-balanced 139-region exploration (partial coefficient +0.0081, BH q=0.048). Under stronger GBIF ≥10 recorded cells q~0.818, ≥20 cells q~0.292, and ≥100 botanical hue taxa q~0.177. Source species-pooled white hue never shows a corrected association (all 5 source q≥0.17). The nominal alternative ≤10km estimate has q~0.057. There is therefore **NO reproducible multi-definition cross-scale information-order effect**. Never interpret white coefficient as wind-induced bee sensory learning, foraging choice, fragrance plume or seed fitness.

In the GBIF-positive region subset, green and brown hue mean wind main effects are not stable: green has positive coefficient in 4/5 quality scenarios and negative in one, with zero source 11-hue BH-significant cases; brown positive in 2/5 and negative in 3/5, again zero significant. In contrast, Stage87E's global source-274 native-plant-region green/brown wind associations occur independently of GBIF positive sample restrictions and can reflect plant community climate niche differences, anemophily and uneven source representation.

## Other crucial identification limits

Original NHM floral-text source contains 59,369 plant taxa but only **ONE** nonblank field for pollination mode. It is currently impossible to filter all true insect-pollinated flora or exclude anemophily using this source. Green, brown and wind relations are not proof of the flowers' sensory signals having been shaped by pollinators. Stage87C WorldClim uses 1970–2000 regional mean wind at ~2m, not wind or turbulent odor dispersion during GBIF collection (1950–2025). Some vegetation/plant species are native in multiple TDWG3 regions; spatially blocked bootstrap in Stage87E does not account for phylogeny or native lineage origin. No source-measured bee learning, first-cue acquisition, approach, landing, effective pollen delivery or plant reproductive fitness is included.

**Current scientific claim ceiling:** The global spatial floristic correspondences are empirical and directionally interesting. The strong candidate is a positive conditional geography of reported yellow hue and *recorded* Bombus richness under climate and sampling covariates, with purple a negative but more effort-sensitive contrast. Wind main effects on green/brown are global botanical geographical gradients, not demonstrated visual attraction mechanisms. The crucial conditional wind×Bombus effect is not robust. Stage88 would need original species-level pollination-mode labels and non-bee insect recording-effort/background data, preferably independent site-level native flora and true phenology, before mechanism tests.

Implementation: research/floral_macro_stage87/sensitivity_global_hue_Bombus_effort_wind.py, source tests and .github/workflows/floral-stage87F-Bombus-effort-hue-sensitivity.yml. All source original ZIP hashes fixed, original full GBIF and raster archives not redistributed.
