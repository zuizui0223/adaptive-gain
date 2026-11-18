# Stage78 — Strong-wind extremes, not average wind, in the floral visual-signal × Bombus macro analysis

**Research scope:** No islands. Continue the source-verified Stage77 continental 54-study flower visual text × observed Bombus mainline. The environmental modifier is episodic **strong wind**, not WorldClim 1970–2000 mean wind.

## Primary registered exposure and source

**Strong-wind metric**: fraction of calendar days in the original recorded visitation months with ECMWF ERA5 reanalysis **daily maximum 10 m wind gust ≥15 m/s**. Pre-specified sensitivities are ≥10 and ≥20 m/s, p95 of daily maximum gust, and fraction of days with 10 m daily maximum sustained speed ≥8 m/s. The 15 m/s threshold is a meteorological exploratory cut point, not a verified bumblebee flight-stop threshold. The thresholds are frozen *before opening bee outcomes*. User intent distinguishes rare gust exposure from average ambient wind.

Source: documented [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), explicit ECMWF ERA5 model, 0.25° original source grid, historical field network year/month, GMT days, no elevation downscaling, metres per second, 10m daily max gust. Attribution Weather data by Open-Meteo.com / ECMWF ERA5; Open-Meteo CC BY 4.0. This original reanalysis is **not a source anemometer at a flower, a gust observed at the exact bee visitation hour, or a measured turbulent VOC scent plume**. Grouping by months with positive visitor records may itself depend on biological observation/detection; source survey effort is not identified.

## Original five independent field-study ERA5 source pilot, June 2018

After fixing a multiple-coordinate elevation-list error in the public historical API request, all five independently selected real original EuPPPollNet study coordinates returned true daily m/s gust arrays. Five studies were selected by original study/year/month/coordinate, without consulting insect/flower phenotype outcomes. Response raw JSON SHA256 c31640b6ab07f2184c3f55b4f673e28304ab28047c9e088b, with original API source URL, timezone, returned ERA5 grid coordinates and daily 30 entries recorded.

| Original source survey | Actual ERA5 June maximum 10m gust | Days max gust >=15m/s | Days >=20m/s | p95 daily max gust |
|---|---:|---:|---:|---:|
| Estonia, Karise K10 2018 | 24.7 m/s | 7/30 | 1/30 | 19.0 m/s |
| Ireland, White An 2018 | 20.0 m/s | 3/30 | 1/30 | 19.6 m/s |
| Czech Republic, Knight Hermanovice | 15.0 m/s | 1/30 | 0/30 | 14.5 m/s |
| Czech Republic, Knight Gora Gipsowa | 16.5 m/s | 1/30 | 0/30 | 14.2 m/s |
| Italy, Marini UNIPD01 A | 10.9 m/s | 0/30 | 0/30 | 8.8 m/s |

[Verified real five-study pilot run 44213424207](https://github.com/zuizui0223/adaptive-gain/actions/runs/44213424207) SUCCESS with six source-free threshold and no-zero-imputation tests. These 5-site descriptive wind counts alone **do not** support a visual-signal × Bombus effect.

## Original continental study-balanced macro sample and explanatory paths

The original source NHM 59,369 botanical text labels include 233 lexically single-hue documented visited plant taxa. Stage77 identifies 424 EuPPPollNet study×network×year communities across 43 independent original study IDs containing two different explicitly recorded hue families. 422 have unique source field coordinates, with 2 excluded. For bounded historical ERA5 retrieval, select up to **four networks per original study**, deterministic source study/year/network sort, before inspecting either strong-wind values or Bombus response. This is a bounded, **study-balanced observational subset**, not the entire original 424 frame or the true European floral species population.

For each selected source network-year, obtain ERA5 daily maximum gust only over the actual source recorded visitation calendar months. Save original API URL, response SHA256, units, dates, original field site coordinates and returned ERA5 grid coordinates. For any missing ERA5 daily variable or ambiguous source site, **exclude/fail** rather than fill it with zero. The source 1970–2000 WorldClim average wind is not used as a substitute for these measured-modelled gust extremes.

Exploratory recorded-bee composition equation with source study fixed effects:

  B = visual + gust15 + visual × gust15 + ERA5-temperature + ERA5-precipitation + study FE.

Here B is a continuity-adjusted log ratio of **actually recorded species-ranked Bombus versus other bee** events, NOT measured original site Bombus suitability/true absence. Visual is the positive lexically reported yellow-family species ratio *within visited plants*, NOT field measured UV guide geometry, calibrated reflectance or a confirmed unvisited plant community. Gust15 is the ERA5 daily maximum gust >=15m/s day fraction, reported per 10 percentage points. Cluster studies, perform study leave-one-out, and check whether within-study extreme-wind variation and original study number support a distinct model. Sensitivity uses gust10, gust20 and p95 daily gust, not selectively whichever gives a desired sign. Source 10m gust exposure is area/time coarse; do NOT interpret a regression coefficient as instantaneous sensory cue occlusion.

If gust days are all zero or identical within each source study, report **unidentified** rather than overclaiming a wind effect. If study/bee records are insufficient, report number and source admission failure. The study fixed-effects observational screen does not adjust genuine plant phylogeny and cannot establish adaptive evolution or causality. Avoid comparing model fit across source-selected samples as if preregistered random field experiments.

## Real scent and visual signal coverage limitation

Previously verified source original multispecies VOC DataSheet 1/2/3 from Farré-Armengol et al. (2020) contains 291 exact Latin binomials, of which 47 overlap 1,408 real EuPPPollNet flower species, five overlap 233 positive single-hue textual flowers, and **only one species, Knautia arvensis**, overlaps the truly source-measured 73 petal reflectance species AND original EuPPPollNet flower visitors. All three studies measured different populations/times. The original VOC source field named wind is a **wind-pollination syndrome flag** and is absolutely not meteorological wind speed. Therefore **strong gust -> scent plume -> bumblebee** causal mediation remains **not identified**. Source floral VOCs cannot simply be given synthetic zero values for the 232 unmeasured text-colour taxa.

For reference, 2025 Behavioral Ecology field work already found bee/visitor-community changes between <0.5 and >2.5 m/s ambient winds (DOI 10.1093/beheco/araf067). Those experimental treatment speeds are NOT equivalent to this reanalysis daily maximum gust >=15m/s; threshold values have different definitions and must not be interchanged.

## Reproducibility

- research/floral_macro_stage78/probe_original_era5_strong_gusts.py and six threshold/source consistency tests; workflow floral-stage78A-ERA5-strong-gust-pilot.yml, real source run 44213424207 SUCCESS.
- research/floral_macro_stage78/source_era5_strong_gust_visual_Bombus_macro.py and six source-free main macro threshold/day/source support tests; workflow floral-stage78B-continental-extreme-gust-macro.yml.
- Source original NHM/EuPP/Stage77 studies raw-derived artifacts have immutable SHA256 locks; no source flower photos or private source data are imported.
- **Full original source 43-study balanced macro wind-gust output is not claimed until its own separate GitHub Actions run succeeds.**

Scientific next step is a real independent site/effort-controlled study with measured visit-hour gusts, plant optical cues and species specific VOC, so causal strong wind modulation of communication can be distinguished from foraging impairment and temporal/spatial environmental selection. Do not substitute another single-species UV experiment for the macro evidence frame.
