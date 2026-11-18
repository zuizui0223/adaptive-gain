# Stage84 | Original DoPI v2 versus Ohashi spectral taxa: source-bounded macro admission

2026-11-18 JST. Status: verified original Zenodo file identity and schema, original full taxon/publication audit executable; numerical coverage must be read from the successful source CI receipt, not assumed from the published database totals.

## Scientific question

Can independently archived, source-labelled 2026 DoPI v2 European pollinator-plant records add **new lineages and independent original studies** to the current Stage83 Ohashi-based floral far/near colour-contrast × Bombus community source study, or do they mostly reproduce existing taxa and already sampled authors? Greater interaction count alone cannot solve source phenotype, phylogeny or sampling unit nonindependence.

## Verified original source identities

1. DoPI v2 2026 original record: DOI 10.5281/zenodo.22876365, Zenodo source file DoPI_dataset_2.0.csv, 384,896,230 original bytes, author-provided MD5 d1c76fc0fd4df6a6828550c5866e4af1, original CC BY 4.0. Verified first physical UTF8-BOM CSV bytes and schema in source-success Action 44268902340. The original source has 31 actual columns, including plant_species, plant_family, pollinator_species, pollinator_family/order, interaction record counts, publication, DOI, methodology, plant_survey/pollinator_survey scope, country, date/location, and pollination evidence. No invented positive/negative source controls.
2. Original Ohashi et al 2015 285,933,377-byte full author spectrometer ZIP, MD5 d98ddd3b93fb79fdbaaa5eec5818c187, SHA256 860ad9ef71d99efdda441fae00090ddb1dad0145f5c54a04b581b09490e718b7. Original ZIP contains **219** spectrometer taxon folders, of which **180** are strict simple two-word binomials, 33 infraspecific folders held separate, six not resolved to strict binomials. Neither of the latter is treated as a biological absence.
3. Exact Stage81D Apis D65 far-green and near-hexagon receptor traits for only **28** species, source derived artifact ID 14409142056, SHA256 9139935f10fbd94a8fb888d807af872c9e5289422249d138fb8a61ac799a0b2a. The 28 are those originally matched to EuPP, and are not a random sample of all 219 flowering taxa.
4. Corrected EuPPollNet original 18,798 accepted plant×study-network-year rows, source SHA256 475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617 and 52 original contributing published studies represented as 54 Study IDs. DOI matching must use the source author's DOI column, not 54 labels.

## Pre-specified database joins (before response outcomes)

- Match DoPI source plant_species against original Ohashi source exact **strict binomials** only; no genus-only match, undocumented synonym match, family substitution or assumed species-negative.
- Separately count all 180 source names with original Ohashi spectra, the current 28 species with verified Apis receiver model, and source taxa in the 180 not represented in the current 28. The latter are **spectrometer available only**, not assigned species-specific green/hexagon values until author original true sheets have been processed.
- Count at DOI level (validated 10.x DOI), not record row level. Compare original DoPI DOI strings with the actual EuPP source author publication DOI set; report the intersection and nonintersection, but **DOI nonintersection does not prove source study independence** if citations/versions/supplements are different.
- Only classify a source identified Bombus versus another source-identified bee if pollinator_order and pollinator_family agree on a bee, and species-rank pollinator name is exact. Treat all other visitors separately; an unlisted Bombus record is never a true ecological absence.
- Record source original methodology, source plant_survey/pollinator_survey sampling coverage, and 'pollination' quality. Do not equate total interactions with independent observed pollination or reproductive fitness.
- As a conservative potential network opportunity diagnostic only: require same author DOI, country, year, month, original exact latitude, longitude and habitat AND at least two original matched 28 plants and both recorded bee channels. These metadata blocks are NOT automatically confirmed same survey effort, sympatric flowers, native distribution, or independent field study replicates.
- No wind-at-flower, odor plume transport, learning or landing observations are added by DoPI source data; no SEM/mediation/trait evolution inference is valid from this join alone.

## Executable and source control

Code: research/floral_macro_stage84/probe_original_dopi_v2_archive.py, audit_real_dopi_v2_ohashi_eupp_power.py, and corresponding source-free semantics tests. GitHub Actions source SHA and checksum-locks full official 385 MB DoPI 2026 and 286 MB Ohashi original archives; only a compact derived numerical source receipt is uploaded, never publisher bulk source originals.

Scientific STOP: even if the 180 original spectrometer taxa gain many historical DoPI visits, **field source plant abundance, species-specific flower colour at the time of visit, independent site sampled panels and plant phylogeny remain missing**. A prior 2022 DoPI paper and the 2026 database release already performed the aggregation; species matching alone is data integration, not a novel ecological inference. Source-aware candidate power counts are the only deliverable until true independent source data support actual signal × receiver conditional models.
