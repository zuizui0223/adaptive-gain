# Stage106 — Original source mainland ERA5 0.25° land-cell weights + official CDS daily 10fg contract

**2026-11-20 JST. Geographic and physical source preflight only: NOT a retrieved 1991–2020 CDS daily climate dataset and NOT an ecological wind effect.** Stacked onto Stage105 #184, main unchanged.

## Correct official Copernicus ERA5 data product

The Copernicus Climate Data Store provides **ERA5 post-processed daily statistics on single levels from 1940 to present**, dataset name derived-era5-single-levels-daily-statistics, publication documentation updated November 2026 and DOI 10.24381/cds.4991cf48. The CDS performs daily statistics on-demand from the hourly ERA5 source (1_hourly, 3_hourly or 6_hourly sampling), with original 0.25°×0.25° atmospheric horizontal resolution. The source 10m gust variable is ECMWF 10fg, **10m_wind_gust_since_previous_post_processing**, a modelled maximum 3-second wind, not the average horizontal speed or observed station gust. The separate original source 2m temperature is 2m_temperature in K.

The exact climate predictor should be built by **two separate CDS daily-statistic requests**:
1. 10m_wind_gust_since_previous_post_processing with daily_statistic=daily_max from frequency=1_hourly; result gust in m/s.
2. 2m_temperature with daily_statistic=daily_mean from frequency=1_hourly; result K, converted to Celsius before the 5°C flowering-potential monthly condition.

Fix product_type=reanalysis and time_zone=utc+00:00 for both, from 1991-01-01 through 2020-12-31. Do not substitute Open-Meteo daily 10m gust derived model values without independent cell-source comparability audits; Stage95/97 50 representative points are a diagnostic, not the final region exposure.

**No single CDS request can correctly ask for gust daily_max AND 2m temperature daily_mean under one shared daily_statistic; the two must be requested separately and then joined by original source grid/time.**

## Frozen genuine mainland geography

Original 367 TDWG3 floristic regions include 120 exclusively island and 122 mainland+island mixed regions in the independently audited original source geo stage; **125 strictly mainland** were retained. Stage98B removes only 16 source geometry-contact exploration regions, leaving 72 exploration, 37 unchanged holdouts for future ecological effect analysis. Stage106 geographic preflight is NOT allowed to read floral pattern, scent or flower-size outcomes.

To obtain the actual **cell area weights** rather than a fake coastal grid-centre mask:
- SHA-verify the original Stage94 source geographic registry (ZIP SHA256 3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833).
- Retrieve and Git-blob-SHA-verify original TDWG WGSRPD level3 geographic polygons (91104e5159e31f88154833a51d3b0d1c9271083f).
- Retrieve independent Natural Earth physical 1:10m land polygons including true islands, ZIP SHA256 e547d749445eaa0964aba76738090ec88f5e63c4585122170f98c67a7ea922dc. Identify *connected source continental landmasses* (separate Greenland, Madagascar, Britain, Bali), not a large-island area cutoff.
- Compute actual original mainland intersection with each area region polygon, then actual geodesic area in km² of intersection with every ERA5 0.25° grid **cell footprint**; a coastal cell gets its physically intersected land fraction rather than an all-land or all-sea label.
- Compare sum of grid-cell intersected areas to exact original regional mainland geodesic polygon area, and refuse >1.5% discrepancy. Freeze source area weights independent of any wind and flower values.
- For the first reproducible source-scale test choose the **three smallest originally eligible mainland regions by source original land area**. This is selection by original geography only and not a representative sample of all mainland ecoregions.

## Main regional wind metric from original full 30-year gridded daily source

For each grid cell (i), among all original 1991–2020 days, calculate its long-term mean 2m temperature for each of 12 calendar months. Its eligible months are strictly those where that mean is greater than 5°C. Among days in eligible months calculate the fraction whose source daily maximum ERA5 10fg strictly exceeds 15m/s (not >=15); threshold 10/20m/s are prespecified future sensitivity checks. If no warm month exists, exposure at that cell is NA, NOT a zero gust exposure.

The region's primary exposure is the area-weighted mean of those **cell-level flowering-eligible exceedance proportions**, weighted by ORIGINAL mainland source cell land-intersection area in km²; it is not an unweighted average of surrounding point values, a pooled day count with unacknowledged varying flowering seasons, or an across-region average of wind speed. Require complete actual 1991–2020 days (10,958 including leap days), proper source original m/s & K units, valid meteorology for >=95% of original mainland land area, and declare missing cells explicitly. A cell with no biological bloom month is not an observed flower or gust response. The original 0.25° model signal can still miss local canopy orography and is not exact flower-level turbulence.

## CI scope and blockers

Stage106 GitHub Actions uses real original geometry inputs and computes actual source **0.25° land-cell fractional km² weights** for three geography-selected continental regions. It writes official CDS one-month source request JSON for gust daily_max and temperature daily_mean (six possible source requests), but **DOES NOT send those requests to CDS** because a CDS user-authorized account/API licence and credentials are not verified as available in this repository. This is intentional; no fake authentication, no unused giant 30-year data request, and no false source climate totals.

Unit tests with synthetic complete 30-year daily arrays verify the strict gust/temperature thresholds, Celsius conversion from original Kelvin, calendar leap days, source-correct units, missing-weather failures, and fractional source mainland land-cell weighting. Tests do not establish empirical gust effects. A future authenticated CDS small-area month probe should validate actual NetCDF variable/time/dimension conventions before the source area-weighted 125-mainland-period extraction is expanded and any signal regression is fitted.

The observed Stage105 33-region one-point source screening found source floral mark lexical report rho +0.679 before source reporting corrections but +0.082 after ranked documentation, latitude and temperature controls; WFO full description coverage and NHM flower-colour coverage each correlates with point gust at around rho +0.77. These are *source reporting artefact risk diagnostics*, not biological mechanism claims. Their true regional ERA5 CDS land-area exposure remains the main physical data obstacle.

## Files

- research/floral_macro_stage106/original_CDS_ERA5_025deg_mainland_area_weights.py
- research/floral_macro_stage106/test_original_CDS_ERA5_025deg_mainland_area_weights.py
- .github/workflows/floral-stage106-source-mainland-CDS-ERA5-gridarea.yml

No real full CDS 1991–2020 climate has been downloaded by this preflight. Any source-specific area-weighted gust region numbers in a later stage must have original CDS response file hashes, source grids, missingness and masks attached.
