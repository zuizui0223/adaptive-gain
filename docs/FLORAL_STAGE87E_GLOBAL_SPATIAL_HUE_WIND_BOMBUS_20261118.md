# Stage87E: GLOBAL spatial correspondence, independently verified

2026-11-18. Observational, exploratory; no flower-specific wind, odour plume, pollinator recognition, landing or selection effect established.

## Actual source data (original records inspected, hashes fixed)

- NHM plant botanical descriptions: 59,369 unique source labels, 31,773 with any flower-colour prose, 15,062 with one explicitly recorded hue family, 925 positive reports of spotted motifs. The remaining records are UNKNOWN for a given unmentioned hue, not biologically negative; a species reported with one hue is not necessarily monochromatic. The compact botanical source has ONLY ONE nonblank pollination mode record (anemophily), so the key control animal-versus-wind-pollination is not identifiable.
- Accepted WCVP native distribution 55,775 strict species across 367 TDWG Level3 botanical regions; 466,445 species×region native distribution memberships are NOT 466,445 independently evolving native populations.
- WorldClim 2.1 1970–2000 climatological 10 arc-minute 12-month means, wind (mean, m/s), temperature, precipitation, solar radiation, vapour. 350 TDWG regions have all five variables. Stage87C used up to 48 spatially spread sample sites per region with cos(latitude) weighting: approximate spatial climatology, not exactly integrated population conditions. Original polygons had 19 invalid geometries requiring clearly labelled repair sensitivity.
- Archived GBIF DOI 10.15468/dl.jbewdc, download 0003256-260226173443078, 3,958,417 occurrence rows (1950–2025) covering Asia, Europe and North America. Positive source Bombus species records occur in 165 TDWG regions. GBIF records lack independent target-group survey effort and no archive record means UNKNOWN rather than bee absence. Species richness primary requires at least 3 records in at least 2 1-degree grid cells for a strict Bombus binomial. A 10-km uncertainty stricter species measure is independently included as a sensitivity.

Actual GitHub verified regional artifacts:
- Global native flora + WorldClim: Artifact 14420920043, ZIP SHA256 4c0ab25596078be4b2aa35a254e42695fd260e1720864e173970aac8aa7db83a.
- Archived GBIF regional bees: Artifact 14419407872, ZIP SHA256 2fe7510fe8c08189d63151fe255a00baafb96c7acc87d3d0fedc970966ca1a43.
- Stage87E actual source-locked regression and bootstrap GitHub Actions #44291024611: SUCCESS; Artifact 14422190271, derived ZIP SHA256 0d58c78fa9d1c3660f440a0e10b50881679bce2a22877796e83779b1bc1d5957.

## Fixed source data-eligibility gates

Use native source flora only, at least 50 species with explicit single recorded hue per region, all five climate variables covered with at least 12 original sample points each, and exclude the 19 native-region source polygons with required geometric repair. Actual globally complete source: **274 regions**. A separate co-occurrence analysis uses ONLY regions with positive recorded GBIF Bombus species richness and at least 5 original unique 1-degree observed cells. Actual matched: **139 regions**, no artificial non-Bombus regions.

For each of the 11 fixed lexical hues, compare (i) native species-pooled hue frequency and (ii) mean hue share within genus balanced equally across original native source genera. Source effect is a local regional HUE FRACTION, not absolute colour strength or the number of documented nectar guides. Fit independent descriptive OLS models with HC3 regional robust p, plus 1000 regional geographically blocked bootstrap replicates at 20° latitude×45° longitude and 30°×60°, and leave-out each 120° longitude sector. BH multiplicity is computed separately across the fixed 11 hue families in each study scope and original trait aggregation; it does not correct for all possible previous exploratory tests.

All source models include standardized mean wind, temperature, log(precipitation+1), solar radiation, vapour pressure, NHM source flower-colour documentation fraction, log explicitly mono-hue species count, latitude, latitude squared, sin longitude and cos longitude. Recorded-Bombus subset additionally includes log observed richness, log unique 1-degree recorded GBIF cells (still NOT unbiased effort), and the interaction of standardized wind × recorded richness.

## Real source macro observations: climate, geography and genus controls

Estimates are absolute hue composition FRACTION points per 1 SD of the named source predictor conditional on the other source controls, not change in flower physical reflectance. 0.01 coefficient means 1.00 percentage point of regional plant-colour fraction.

| Real 274-region all-native flora | Genus-balanced wind beta | 20×45 geographical bootstrap 95% | 30×60 geographical bootstrap 95% | Exploratory BH over 11 hues |
| --- | ---: | --- | --- | ---: |
| Green lexical hue | **+0.00567** | [+0.00200, +0.00984] | [+0.00219, +0.00917] | 0.0125 |
| Brown lexical hue | **+0.00763** | [+0.00339, +0.01256] | [+0.00337, +0.01313] | 0.0011 |
| Yellow lexical hue | -0.00498 | [-0.0114,+0.0026] | [-0.0108,+0.0018] | 0.2594 |
| Purple lexical hue | -0.0010 | [-0.0074,+0.0052] | [-0.0079,+0.0041] | 0.9254 |

Green/brown directions persist with source species-pooled composition and genus balancing and all original 120° longitude-sector exclusions; yellow negative exists in pooled species but NOT genus-balanced robustly. Original climate-only global spatial correspondence in green/brown can also reflect wind-pollinated plants, life form, floristic community turnover and source historical prose coverage. The source cannot stratify anemophily: ONLY 1 of 59,369 source text records has an explicitly recorded pollination mode. Therefore "wind drives floral visual signals" is NOT identified.

## Real source 139 Bombus-positive-region partial relationships

Within observed positive three-continent source-archive regions and after controlling recorded GBIF grid-cell effort and climate:

| Genus-balanced hue | Partial observed log(1+Bombus recorded species) coefficient | 20×45 95% | 30×60 95% |
| --- | ---: | --- | --- |
| Yellow | **+0.02255** | [+0.01042,+0.03093] | [+0.00269,+0.02876] |
| Purple | **-0.01346** | [-0.01757,-0.00730] | [-0.02026,-0.00486] |

Both have source exploratory 11-hue BH adjusted q below 0.05 in the base dataset. Importantly this is NOT a source-independent observed bee preference for flowers, and more recorded Bombus species can occur in regions with greater archive sampling effort or distinct natural floras.

The WIND × RECORDED BOMBUS richness source interaction does not show a consistent robust macro pattern across 11 hue families and both pooling and equal-genus compositions. A white-hue equal-genus positive interaction appears in the 139-region pilot (beta +0.00807, BH q 0.0483, 20×45 interval [+0.00015,+0.01252] and 30×60 interval [+0.00061,+0.01300]), but it is NOT supported by the species-pooled original hue summary and must not be promoted as a conditional sensory hierarchy without external target-group effort and pollination mode verification. Multiple previous model comparisons further make the nominal exploratory q an insufficient confirmatory claim.

## Scientific stop/advance

This is a genuine new **macro flora-space association** across dozens of thousands of accepted botanical species and hundreds of regions. It supports a descriptive claim: wind and geographic receiver opportunity correspond with documented plant-floral hue composition after climate/geographic adjustment. It DOES NOT establish that flowers evolved to attract Bombus at a new range, that scent becomes worse under gusts, that Bombus has a particular visual learning ability, or that landing costs choose a cue order.

The next genuine bottleneck is not 49 vs 50 species but **independent pollination-mode/animal-attraction documentation and abundance/recording effort at matched regions**, before testing ecological directionality. Stage87F independently varies original GBIF effort and local floristic sample thresholds; only source verified sensitivity results count. No true target-group observation effort or wind-at-visit is currently available, so full conditional decision-route hypothesis remains unverified.

GitHub source implementation: research/floral_macro_stage87/analyze_global_hue_wind_bombus_spatial_overlap.py; workflow .github/workflows/floral-stage87E-hue-wind-Bombus-spatial-adjusted.yml. Original derived stageE artifact is the receipt of numerical proof; no publisher raw source is redistributed.
