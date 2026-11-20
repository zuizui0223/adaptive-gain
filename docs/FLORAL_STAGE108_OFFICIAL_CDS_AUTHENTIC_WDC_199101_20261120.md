# Stage108 — Real official Copernicus CDS daily ERA5 10fg + 2mT authenticated pilot (WDC, January 1991)

**2026-11-20 JST. Single goal: end the unverified source-access bottleneck before continuing regional wind × three flower-cue inference.** Draft stacked on Stage107 #186; default main unchanged.

## Genuine official source contract

Original dataset: Copernicus CDS "ERA5 post-processed daily statistics on single levels from 1940 to present", DOI https://doi.org/10.24381/cds.4991cf48, official download page https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics?tab=download. Official 2026 API guidance: https://cds.climate.copernicus.eu/en/how-to-api and original ECMWF daily-aggregation format documentation https://confluence.ecmwf.int/spaces/CKB/pages/462888259/ERA5+family+post-processed+daily+statistics+documentation.

Two **separate** original API requests for the same UTC month 1991-01:
1. variable=10m_wind_gust_since_previous_post_processing, daily_statistic=daily_max, frequency=1_hourly, time_zone=utc+00:00, product_type=reanalysis. Original ERA5 postprocessed gust name 10fg represents maximum 3-second wind at height 10 m in m/s, not mean wind speed.
2. variable=2m_temperature, daily_statistic=daily_mean, frequency=1_hourly, time_zone=utc+00:00, product_type=reanalysis; source unit Kelvin.

Read the **exact source request JSON** and ORIGINAL geodesic land-cell weights from successful Stage106 Actions artifact 14602954663 (ZIP SHA256 09c65542c221daecd1867baf250b694e9229f7c85fc09d401849765aa234b6b8). WDC is selected by earlier geography-only smallest-mainland-region policy, with two actual overlapping 0.25° source cells (38.75 N / 77.0 W and 39.00 N / 77.0 W), land-intersection areas 41.6868537 and 142.95504263 km², total approximately 184.64 km². No trait, Bombus, bee-cognition, wind or holding response is consulted in selecting this pilot.

The CDS official API returns a ZIP of original NetCDF daily data (one variable per file). Verify actual downloaded ZIP SHA256, original NetCDF member/coordinate names, 31 January 1991 UTC daily dates, 0.25-degree source grid points precisely matching the original mainland source cell centres (allow longitude ±180/360 equivalent), gust and 2mT original source units, no missing real mainland cell/day, realistic values, and exact daily max gust >15 m/s, not >=15. Compute only the ONE MONTH source area-weighted exceedance diagnostic from the two true source land-intersection cell weights. **DO NOT CLAIM** the single January 1991 fraction is the original planned 1991–2020 warm-month long-term wind exposure, and do not model any plant outcome.

## Safe credential and licence behaviour

The Copernicus CDS API **requires the user's personal-access token**. The official dataset webpage also requires the account owner to explicitly accept that dataset's CC-BY terms **before** retrieving; this project does not click the terms or accept them on the user's behalf. The user can store a GitHub repository secret named CDSAPI_KEY, CDS_API_KEY or CDS_PERSONAL_ACCESS_TOKEN. The workflow uses the first nonempty secret in that order and passes it to the Python process; secret text is never printed or included in an artifact, request URL, GitHub issue, or source code. No key is fabricated or asked for in chat.

The source task always runs source-free original scientific and NetCDF-schema unit tests, restores exact SHA-verified Stage106 source geometry, and produces a derived-only receipt:
- **If no existing token is configured**: report BLOCKED_NO_EXISTING_CDS_PERSONAL_ACCESS_TOKEN. No official CDS request is sent; no claimed climate data.
- **If an existing token is configured and the dataset's terms have ALREADY been accepted**: try exactly the two small authorized 1991-01 WDC requests via the official CDS API; verify original ZIP/NetCDF, and record the original response hashes, lat/lon, days, units, original WDC monthly cell diagnostic. The sensitive original raw data ZIPs are deleted after verification rather than uploaded or committed.
- **If CDS rejects the token, licence, request schema or transfer**: fail the authorized source gate, report only a coarse diagnostic category with no raw authentication errors or tokens. Do not automatically accept a licence or silently retry under an unauthenticated third-party source.

The user must opt into CDS account conditions outside this GitHub PR. This action is an original real source attempt only, not an implied authorization to spend money, to submit the 30-year global archive, or to change the fixed 72 exploration / 37 independent holdout region topology.

## Subsequent scale-up, only after an actual successful pilot

Inspect native NetCDF schema once in an authentic small-area original source before constructing 1991–2020 0.25-degree daily 10fg max and 2m temperature means for the 125 original mainland regional source polygons. Freeze original hourly-to-daily time semantics, mask source mainland land area, and compute each **cell's** climatological monthly mean T2m over 1991–2020; eligible months strictly >5°C. For each cell's eligible days calculate fraction with daily max gust >15m/s, and then geodesic cell-land-area-weighted mean across the same source mainland TDWG3. No 1970–2000 WorldClim MEAN wind or 1991–2020 Open-Meteo ERA5-model one-point proxy can be substituted as the primary physical exposure.

The source trait observation/ascertainment controls from Stage105 (33 representative points) and Stage107 (72 WorldClim 1970–2000 mean-wind regions) remain essential because source NHM colour documentation and WFO prose coverage correlate with reported flower-signal patterns. Even a successful 125-region ERA5 original wind exposure will only support carefully controlled spatial associations, **not** bee cue-use order, nectar-guide function, VOC emission or natural-selection causality by itself.

## Code and reproducibility

- research/floral_macro_stage108/original_CDS_ERA5_199101_wdc_authorized_pilot.py
- research/floral_macro_stage108/test_original_CDS_ERA5_199101_wdc_authorized_pilot.py
- .github/workflows/floral-stage108-CDS-ERA5-authorized-199101-10fg.yml

**No successful original CDS climate result should be reported until the authentic GitHub Actions receipt explicitly says SUCCESS_OFFICIAL_CDS_TWO_VARIABLE_ORIGINAL_199101 with two original source ZIP hashes and verified 31-day NetCDF schemas.**


## Verified first original-source authentication gate — 2026-11-20

GitHub Actions [#44728278046](https://github.com/zuizui0223/adaptive-gain/actions/runs/44728278046) completed with **12 source-free tests passing**, including 31-day 1991 January NetCDF ZIP schema/unit validation against SYNTHETIC fixture arrays, original WDC two land-intersecting 0.25-degree source cells, strict >15m/s gust comparison, original 2mT Kelvin units and no climate-data guessing. The actual Stage106 original area-weighting source ZIP checksum was verified.

**Actual source retrieval state:** BLOCKED_NO_EXISTING_CDS_PERSONAL_ACCESS_TOKEN. The source code found no existing authorized Copernicus CDS repository token under CDSAPI_KEY, CDS_API_KEY, or CDS_PERSONAL_ACCESS_TOKEN. No official Copernicus CDS climate API request was sent. No actual original January 1991 CDS data, NetCDF units, daily climate values, or 1991–2020 regional climate exposure was obtained.

The source gate receipt is preserved in artifact **14625311199**, original ZIP SHA256 **23a9412e778da9554218edf86717eafe750953b2782815f0a6fe839fa481260d**. A green CI status verifies that the fail-closed credential gate worked; it does **not** mean the original meteorological source was retrieved.

**Explicit remaining user-only access step:** the account owner must accept the Copernicus ERA5 daily-statistics dataset licence on the CDS website, and save their own CDS Personal Access Token into the repository zuizui0223/adaptive-gain as GitHub Actions repository secret **CDSAPI_KEY** (Settings → Secrets and variables → Actions). Never send the token in chat, commit it to a repository or print it in logs. The existing Stage108 workflow can then be rerun from the Actions tab on this branch. Only a new receipt stating SUCCESS_OFFICIAL_CDS_TWO_VARIABLE_ORIGINAL_199101 with actual NetCDF-source ZIP SHA256 and full original January 1991 daily-grid evidence would close the source gate.

No 125-region 1991–2020 area-weighted primary wind exposure exists yet.
