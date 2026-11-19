# Stage97 — Original reanalysis ERA5-model 1991–2020 mainland source expansion, regions 26–50

2026-11-19 JST. Source acquisition stage ONLY, NOT ecological floral cue association. Draft stacked on Stage96 #175; main unchanged.

## Purpose

The single frozen wind primary exposure is fraction of days in 1991–2020 when 10m daily maximum gust >15 m/s, restricted to months with 1991–2020 climatological 2m mean temperature >5 C. Stages 95A/B checked an actual 30-year daily source at 5/3 genuine mainland sites; Stage95C retrieved its first 25 source TDWG mainland representative locations. Neither is a mainland polygon area-average, and the Open-Meteo reanalysis delivery is not yet independently byte-checked against original CDS hourly ERA5 10fg.

## Frozen second25 source policy

1. Verify original Stage94 continental-only 125 region geometry ZIP SHA256 3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833 plus TDWG original geojson Git blob 91104e5159e31f88154833a51d3b0d1c9271083f.
2. Independently verify successful original Stage95C first25 source ZIP artifact 14535045199 SHA256 7c98421306466b589b1f80ec97d4ca32ba58e73ba7807f0c2330a7f082fe6b67, and assert original first25 codes match exactly the sorted original frozen TDWG list.
3. Source-select exactly original site position 25–49, with zero overlap and without using wind, bee or botanical signal outcomes, preserving fixed 88 exploration versus 37 holdout regional split.
4. Query full 1991–2020 official ERA5-model historical reanalysis derived daily 10m gust max and 2m mean temperature in three disjoint decades, 5 sites per provider batch, with quota-grounded 70-second interbatch pacing; require 15 distinct raw-source response JSON SHA receipts.
5. Require 10,958 UTC source dates, original m/s and C units, complete 30-year monthly warm season mean temperature >5 C, strict daily gust >15, 10/20 sensitivity. Never impute missing days; no warm months means NA, not zero.
6. Publish only provenance-checked regional point fractions and source quality gates, without opening heldout cue outcomes or fitting any ecological coefficients.

## Important ceiling

A source TDWG representative point is not a land-area regional wind estimate. Open-Meteo derived daily gust is not independent CDS raw hourly 10fg. Actual plant flowering hour, odor-plume turbulence, bee sensory cue ordering, animal learning, landing success and fitness remain unobserved. This step alone does not warrant regional wind-cue regression or evolutionary claims.

Code:
- research/floral_macro_stage97/next25_source_ERA5_1991_2020.py
- research/floral_macro_stage97/test_next25_source_ERA5_1991_2020.py
- .github/workflows/floral-stage97-second25-ERA5-mainland-source.yml

Original source numeric results are UNKNOWN until successful execution and all source SHA audits pass.
