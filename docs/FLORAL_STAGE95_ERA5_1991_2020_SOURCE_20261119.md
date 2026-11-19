# Stage95 | Original daily ERA5-model 1991–2020 gust climatology pilot, mainland only

2026-11-19 JST. Status: an original source-access/test pilot; not a new floral wind association. The Stage94 mainland frame and common holdout are inherited exactly from source SHA verified artifact 14529576121. No cue/bee outcome is used to pick the pilot.

## Why this next

Stage94 established 125 source TDWG3 regions whose Natural Earth land geometry is mainland-only and flagged 120 island / 122 mixed source areas as excluded. Its shared preoutcome geographical partition is 88 exploration regions (18 blocks) and 37 heldout regions (5 blocks), although physical spatial buffering remains unverified. Stage94B revealed that only 4 heldout mainland regions have >=10 authentically labelled AusTraits flower diameter species, making a strong universal size claim unjustified without new data.

The intended primary *wind* predictor is a **1991–2020 climate fraction of days where daily maximum 10m wind gust strictly exceeds 15 m/s, in climatologically warm months with 30-year monthly 2m mean temperature strictly above 5 °C**. This must not be confused with Stage77 WorldClim 1970–2000 average wind or Stage78's observed-study June 2018 ERA5 gust pilot.

## Frozen source-first pilot

From Stage94 original geographic region IDs, pick the first region in each of five distinct source-geographic EXPLORATION blocks using original source block ID and TDWG code only. Obtain each original TDWG3 polygon representative point (not a species occurrence, climate- or bee-selected location). For these FIVE source points only, query the publicly validated historical archive with explicit models=era5, timezone=GMT, wind_speed_unit=ms, elevation=nan, daily=wind_gusts_10m_max,temperature_2m_mean. Fetch three disjoint decades 1991–2000, 2001–2010, 2011–2020.

For each returned point require exact complete GMT source day sequence including leap days (10,958 days across 30 years), original daily units m/s and °C, nonmissing finite day values, plausible gust bounds and source API SHA256. First compute January–December 30-year climatological temperature means, select months with strict T2m >5 °C. Then compute the fraction of eligible days with strict daily maximum gust >15 m/s; 10 and 20 m/s are prespecified exploratory sensitivity and >=15 is a diagnostic to document threshold equality. No eligibility months is NA, never a false zero. Same month subset is used for all 30 years. Site-specific annual weather is NOT a long-term plant-flora composition predictor by itself.

The 5-point pilot is **not region-wide ERA5 wind climatology**: not mainland land-area averaged, not flowering-hour weather and not validated against independently obtained original CDS hourly ERA5 10fg. Open-Meteo is a historical reanalysis-model delivery and aggregating service, not the original ECMWF CDS raw hourly source. This pilot tests whether the exact long-term daily gust metric can be acquired and checked before scaling to all mainland source polygons.

## Holdout and future work

Never use holdout signal outcomes to tune exposure or model. Full Stage94 heldout geography still requires measured separation buffer. A full valid regional strong-wind predictor must sample/aggregate native mainland land area of each qualifying TDWG3 polygon, account for extreme terrain/forest boundary masking and verify source timestamp/units. Possible downstream covariates: long-term T/P, elevation, canopy openness and coast distance. Independently source-verify pollination guild and clade, and retain reporting/ascertainment controls.

The stage does not recover original source floral scent, verified nectar guides, actual bee learning or wind landing, nor fit coefficients. Numeric source pilot results are UNKNOWN until original GitHub Actions completes with source SHA checks.

## Files

- research/floral_macro_stage95/original_ERA5_1991_2020_gust_five_mainland_pilot.py
- research/floral_macro_stage95/test_original_ERA5_1991_2020_gust_five_mainland_pilot.py
- .github/workflows/floral-stage95A-ERA5-1991-2020-mainland-pilot.yml

If remote ERA5-model source cannot deliver consistent complete dates or units across decades, fail rather than filling missing days or switching silently to mean wind.


## Original 30-year source execution actually SUCCESS

Source GitHub Actions [#44525653919](https://github.com/zuizui0223/adaptive-gain/actions/runs/44525653919), derived ZIP artifact ID **14532170043**, ZIP SHA256 **ead1dd4a717bdc7de31455f5d02e953c2ce8406547dcc03e158391b4bc1b9b06**. All ten source-free tests and original Stage94 source geographic ZIP SHA passed. The original three source API response JSON SHA256 checks were:
- 1991–2000: c5a907fe4c3a5c4ec79aace410423b97b99487fb794cecf3d6952510c5978233
- 2001–2010: a0b87bfb02dce76ad36b1448f2b81c788cc611f19a38d0ed3b5c0b079d39b5e1
- 2011–2020: 1919218c1b3b5c0c6c554f5d553a0b04a9a12eee147e64731e1d0eab78de0bc1

All five original geographical source-selected exploration block sites have complete original derived daily ERA5-model arrays for **10,958** UTC days, including 1991–2020 leap days. The original 30-year mean monthly 2m temperatures exceeded 5C for **all 12 months at these five pilot sites**, so this pilot validates full-period source retrieval and strong-gust exceedance logic, not the real ecological operation of omitting cold flowering months.

| TDWG3 source site code | Strict fraction of 30-year daily max 10m gust days >15 m/s |
| --- | ---: |
| CLC | 0.022449352071545903 |
| NSW | 0.08076291294031758 |
| AGW | 0.01706515787552473 |
| GHA | 0.0 |
| BEN | 0.0 |

The two zero site values are actual **reanalysis-model grid-cell 30-year candidate threshold exceedance zeros**, not an absence of wind or storms throughout the flora's TDWG region. Source model: Open-Meteo historical archive explicit models=era5. **No original CDS hourly ERA5 10fg cross-check, no TDWG land-area spatial average, and no wind-visual/odor ecological coefficient** has yet been obtained. The fixed >15 threshold differs from older Stage78 >=15. This is a physical measurement source feasibility result only.

The immediate next source-validation target is a **cold high-latitude/high-altitude mainland test** to demonstrate >5C month restriction on real daily data. Regional mainland landmask integration remains a separate exposure prerequisite.
