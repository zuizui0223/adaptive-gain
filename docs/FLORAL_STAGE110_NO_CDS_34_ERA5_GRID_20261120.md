# Stage110 — CDS-free physical ERA5-model source wind climatology: 16 Delaware + 18 Cabinda mainland grid cells

2026-11-20 JST. Actual original source geography and publicly accessible Open-Meteo historical ERA5-model daily climate, no Copernicus CDS personal token required. Scientific source-data scale-up from successful original 2-cell Stage109 WDC 1991–2020 climate (source validation Actions #44742876248, WDC original mainland land-area >15m/s strong gust frequency 7.231%).

## Why these regions

Three smallest original source strictly mainland TDWG3 regions were already frozen by Stage106 original WCVP/TDWG/Natural Earth geography before any wind or floral outcome was opened. WDC source original 0.25-degree model cells were 2; source original DEL comprises Delaware, eastern United States (NOT Delhi, India; coordinate latitude around 38–39N, longitude around 75W) and CAB comprises Cabinda, Angola (Africa). The latter are original 16 + 18 genuinely intersecting mainland land-grid cells respectively, each with fractional geodesic land-area weights verified independently in the original Stage106 GitHub Actions artifact 14602954663 ZIP SHA256 09c65542c221daecd1867baf250b694e9229f7c85fc09d401849765aa234b6b8.

No original botanical trait, bee records, source positive cue ratios, wind value, or original 37-region holdout outcome influenced selection. The original DEL mainland land area is about 4,811.2 km², CAB about 7,559.6 km²; effective original geodesically weighted source model grid cell counts approximately 12.55 and 13.48, allowing comparison of actual within-region model wind variability absent from WDC's only two source cells.

## Public source and exact physical predictor

Open-Meteo Historical Weather API (https://open-meteo.com/en/docs/historical-weather-api), explicit models=era5 global reanalysis model grid (~0.25-degree from 1940), accepts no account token for noncommercial fair-use; current documentation confirms multi-coordinate archive queries, cell_selection=nearest, elevation=nan disabling service topographic downscaling, timezone=GMT, wind_speed_unit=ms, and original daily wind_gusts_10m_max & temperature_2m_mean. This public model delivery is NOT an independent original ECMWF CDS hourly 10fg source product. Its original source JSON bytes have a separate SHA256 per source query and returned original model grid centres are checked against the original geography.

For all 34 fixed original grid-cell coordinates use 5-site-bounded grouped requests, 3 disjoint 10-year source decades 1991–2000, 2001–2010, 2011–2020, 24 authenticated-by-JSON-SHA API query receipts, 10,958 original UTC daily dates per source site. Fixed source-provider per-group spacing 68 seconds and 12 seconds between decades, quota/transport retries bounded. Each completed 5-site source group writes a separate explicitly PARTIAL source receipt; a later API failure must never be misreported as a completed 34-grid meteorological region.

For each cell compute 30-year January-to-December original 2m daily mean temperature climatology. Eligible months only where that month mean T >5°C STRICT. For all 10,958 original source days in eligible months count daily MAX 10m gust >15m/s STRICT divided by eligible days. Retain >10/>20 m/s prespecified source sensitivity. Then take geodesically weighted regional average of these source original CELL fractions using source land-area intersections. Require >=95% of the original mainland land area has complete 30-year original weather and at least one warm month; no missing-day zero imputation. Record min/max and area-weighted standard deviation of within-region source cell gust15 fractions, and effective land grid count. Uncertainty is spatial *model* heterogeneity, NOT confidence intervals for real flower-wind exposure.

## Claim ceiling

This is regional climate data source validation, not any biological selection effect. It advances the *spatial coverage* of previously verified Stage109 WDC result, but no original 125 mainland region exposure nor original CDS hourly 10fg external comparison exists. Open-Meteo derived daily model source may have model/source aggregation differences from original Copernicus CDS, so it must remain labelled public ERA5-model daily archive. Local roughness, forest canopy/landings, actual flower-point wind, odor plume dynamics, visual display and learned bee cue use are not directly measured.

No plant-native floristic WCVP or WFO lexical trait descriptions are read by the execution. Any next global flower signalling contrast must be limited to the source-frozen 72 geography-only exploration mainland regions, with 37 unchanged holdout regions and source reporting/phylogenetic controls, because Stage105 and Stage107 found large artifactual botanical-reporting dependence of apparent wind-to-floral marking/scent correlations.

## Reproducibility

- research/floral_macro_stage110/original_public_ERA5_model_34cells_DEL_CAB_landarea.py
- research/floral_macro_stage110/test_original_public_ERA5_model_34cells_DEL_CAB_landarea.py
- .github/workflows/floral-stage110-public-ERA5-DEL-CAB-34grid.yml

Until genuine source API SHA and geographic integration CI completes, no numerical DEL/CAB 30yr source strong gust fractions are claimed.
