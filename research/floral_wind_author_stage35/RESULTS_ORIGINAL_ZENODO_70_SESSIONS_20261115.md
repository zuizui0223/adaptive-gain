# Stage35 — Original Zenodo source-grain audit of Crall et al. (2020)

2026-11-15. The ORIGINAL publicly archived Zenodo ZIP was acquired and authenticated on a GitHub Actions runner; this stage has not refitted any ecological wind effect.

Primary paper: Crall et al., Biology Letters 2020, DOI 10.1098/rsbl.2020.0103. The article's Data Accessibility cites Zenodo record **3743898**. The separately indexed record **3675327** has the same ZIP filename, CrallEtAl_OrchidBeeWindEcology.zip. Both original manifests are separately hashed and source-recorded, not silently equated.

## Original measured source grains

| Source file within ZIP | Records | Key originally observed fields |
|---|---:|---|
| Zenodo/beedata.csv | **450** | number, date, site, time, scent, genus, species |
| Zenodo/collectionMetadata.csv | **70** | site, date, start.time, scent, count, wind.mean, rel.wind.KE |
| Zenodo/integratedSpatialWindData.csv | **70** | coll.id, site, date, keep, count, wind.mean, wind.KE, turbInt, cover200m |
| Zenodo/siteMetadata.csv | **9** | site-level forest cover and wind/abundance summaries |
| Zenodo/speciesTable.csv | **23** | cin, meth, total, perc |
| Original author analysis code | present | R script for published statistical comparisons |

The ZIP also contains macOS __MACOSX sidecar metadata and an unparseable siteCoordinates.csv, both reported rather than invented as additional ecological data. Blank first CSV field is a legitimate original R row index when the rest of the columns are populated.

The critical independent observation unit for the original wind and attraction relationship is **a scent-bait collection session (70 rows, 9 sites)**, not all 450 captured-bee records as independent independent wind replicates. The source's 450 bee rows do not automatically equal the 409 male orchid bee individuals reported in the paper: count semantics, repeated sightings and published exclusions must be checked against the original author script.

## Published result and its biological ceiling

The original paper reports a positive within-site temporal association between wind speed / turbulence and orchid-bee arrival at **male fragrance-collection stations**. It does NOT report an identical positive between-site association. Wind-dispersed floral fragrance is a plausible interpretation but NOT a randomized odor ON/OFF by wind experiment. The records do not contain plant flower landing failure, legitimate pollen movement, plant seed set or a wind-by-natural-floral-scent 2x2.

Stage35 only confirms source-file integrity and the original study grain. It does not claim a newly fit GLMM coefficient or experimental meta effect. The next separate step must reanalyze the 70 sessions, reconciling the original inclusion count and distinguishing within- from between-site wind relationships; the raw author ZIP is never committed or redistributed.
