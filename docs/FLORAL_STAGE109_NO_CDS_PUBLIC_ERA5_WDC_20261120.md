# Stage109 — NO CDS token required: genuine 1991–2020 public ERA5-model mainland gridded gust climate

2026-11-20 JST. Scientific source-acquisition pilot, no flower/bee/odor/visual signal results and no causal effect. Draft stacked on Stage108 #187.

## Why the CDS access is optional for this source-climate engineering test

Stage108 GitHub Actions #44728278046 verified scientific code and source original geodesic WDC grid-cell areas but showed BLOCKED_NO_EXISTING_CDS_PERSONAL_ACCESS_TOKEN. We can still obtain the historical ERA5 MODEL daily climate from the unauthenticated public Open-Meteo historical weather API, specifying models=era5, at 0.25-degree native ERA5 grid, archive since 1940. Provider references: https://open-meteo.com/en/docs/historical-weather-api and https://github.com/open-meteo/open-data . Respect provider fair-use terms; not a bypass of a CDS account.

The API is an independent *delivery and derivation service* for ERA5 reanalysis model output, NOT a byte-verified official ECMWF CDS raw hourly 10fg archive. Its daily 10m wind gust maximum cannot be asserted identical to CDS daily statistics without matched grid/time independent verification. It is entirely different from WorldClim 1970–2000 long-term mean wind speed used as source documentation sensitivity in Stage107.

## Preselected original source mainland geometry

Stage106 original source land polygon intersection is SHA-verified: derived original GitHub Actions artifact 14602954663 ZIP SHA256 09c65542c221daecd1867baf250b694e9229f7c85fc09d401849765aa234b6b8. The first geography-selected smallest eligible mainland region WDC (Washington DC TDWG3) spans two ERA5 0.25-degree land-intersecting cells: 38.75 N / 77 W with 41.6868537 km2 of geodesic land and 39 N / 77 W with 142.95504263 km2. Original mainland region area ~184.6 km2, effective independently weighted model cells Neff ~1.54. No source flower or wind outcome is used in selecting this geography.

For both predeclared grid-cell centres request historical 1991-2020 weather in 3 strict decades 1991–2000, 2001–2010 and 2011–2020, specifying daily wind_gusts_10m_max and temperature_2m_mean, models=era5, timezone=GMT, wind_speed_unit=ms, cell_selection=nearest and elevation=nan to avoid service surface-elevation downscaling.

Every returned model-grid coordinate must match the source original requested 0.25-degree centre (0.051-degree tolerance); distinct model cells must remain unchanged across decades. Source raw JSON SHA256 is separately recorded per decade. Require 10,958 complete daily UTC dates per original source cell including leap years, full gust m/s and 2m temperature °C units, plausible physical ranges, no missing source days, no borrowed model grid or silent missing-data imputation.

## 30-year gridded exposure calculated WITHOUT a CDS token

At each original land-intersecting ERA5-model cell, compute long-term 30-year mean 2m temperature for each of twelve calendar months. Prespecify eligible months with STRICT long-term monthly 2m temperature >5 C. Among all days of those months over 1991–2020 count daily maximum 10m gust STRICT >15 m/s / number of eligible days. Also retain original 10 and 20 m/s sensitivity. The WDC region proxy is the sum of the original two CELL-specific exceedance frequencies weighted by the exact original geodesic mainland km2 in each cell; it is not an equal-cell mean or the single-polygon representative point.

No full-125-mainland-area ERA5 CDS wind climate has been generated, and WDC has no independent field plant flowers/traits/bees observed. The result is a model-grid spatial sampling proof, not wind-mediated odor plume, bee learning, landing behavior, UV pattern ecology, or evolutionary selection. Do not fit any floral effect here. WDC only one small mainland region means no global biological gradient conclusion.

## Next scaling step if verified

Scale the same source-only cell-integrity and land-area weighting to DEL and CAB, whose original 0.25-degree land-grid weights are already verified in Stage106 (16 and 18 cells). Then expand to 72 source-contact-free mainland exploration regions, keeping the original 37 holdout signal values unopened and identifying source documentation and phylogenetic repetition as major confounders. A later original CDS authenticated source still provides important independent reanalysis daily gust reproducibility, but no CDS token is needed for this explicitly labelled OPEN-METEO historical ERA5-model route.

Code: research/floral_macro_stage109/original_geogrid_public_ERA5_1991_2020_WDC_area_gust.py and tests, GitHub Actions floral-stage109-no-CDS-public-ERA5-30y-WDC-grid.yml. Source WDC numeric result is UNKNOWN until actual authenticated original-source geometry and public model API GitHub Actions gates pass.
