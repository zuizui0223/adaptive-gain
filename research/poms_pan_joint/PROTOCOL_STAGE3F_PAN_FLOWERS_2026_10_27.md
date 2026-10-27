# Stage 3f — independent-flower-inventory linkage gate (2026-10-27)

## Scientific purpose
Recover a **measured local flowering-community proxy** for the structured PoMS FIT target-flower census instead of endlessly interpreting wind × taxon regressions against unobserved plant alternatives.

The official UK PoMS 2017–2023 pan-trap dataset (EIDC DOI **10.5285/5841bfae-471b-498c-af89-c30e5140d6c5**) has flowering-plant records within **2 metres of each of five pan-trap stations** within randomly allocated 1km survey squares. The previously analyzed FIT data (EIDC DOI **10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618**) observe **one preselected flower in a 50×50cm quadrat for 10 minutes**. These are **different observation positions and methods** within the same monitoring programme; neither is an animal's simultaneous visual choice set.

The decision before any ecological model is whether their square/date/site identifiers permit justified links. **Do not infer that every flowering plant near a pan trap was available to the FIT insect.**

## Data and provenance
- Fetch complete official 2026 pan-trap data ZIP. Record original ZIP SHA256 as a receipt only; provider packaging may regenerate a dynamic readme. Record **SHA256 for every uncompressed original CSV member**.
- Download the original FIT ZIP and verify structured FIT original CSV SHA256 `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`. Do not fetch/derive invented absence surveys.
- Retain original source-level readme and metadata, but **never vendor raw microdata into Git**. Report the actual table schema and grain before join attempts.
- For pan files, identify native survey/sample/station IDs, location/grids, event times, taxon/flower status and their native column values. Flowering plant occurrences are **presence observations**, not confirmed absence lists unless explicit survey completeness semantics are documented.

## Linkage tiers — descending evidence, not interchangeable
1. **Exact matching:** only when the same native 1km grid semantics can be established for FIT/pan, and comparable original survey calendar dates exist. Count distinct matched structured FIT `sample_id`, matching square-date visits, pan station records, true flower-availability observations, duplicates and ambiguous site identifiers. A geographic square match never implies same microhabitat.
2. **Near-date contextual link:** if support exists, explicitly label a sensitivity using Pan observations no more than 7 days from FIT census in the **same verified 1km square and year**, selecting nearest day only after a deterministic tie-break. Never call this a simultaneous choice set or fill missing days with zero.
3. **Unmatched:** if same 1km square or event-date integrity is unidentifiable, retain only source inventory and classify `NO_GO_FOR_FLORAL_AVAILABILITY_JOIN`.

Require successful exact FIT CSV digest and verifiable pan source original CSV digests before making any numerical statement. Report coverage against *all eligible structured FIT census records*, then against only pair-positive bumblebee/other-fly records; preserve the latter as a **separate conditional subset**. Inspect relationship cardinality: do not allow join multiplication to convert 1 FIT survey into fictitious replicate FIT surveys.

## Scientific gate
Do not fit ecological explanatory models until original columns, matching keys and the proportion of matched FIT surveys are inspected and a join can be coded with explicit safeguards. If matched Pan local flowers are present, they are at best **square-date floral-environment proxies**, not alternative flowers actually evaluated by FIT insect individuals. Do not estimate adaptation, competition, behavioral rewiring, ecological wind cascades, wind direction, or adaptive-gain `C_A/C_F`.

This stage is independent data-source linkage but **not independent ecological programme replication**. It preserves the frozen V5/V6 and stacked PR #70–74 manuscript surfaces.


## Source-first join implementation locked 2026-10-27 (before numerical join results)
The original pan provider ZIP was obtained and original CSV columns were inspected; stable member hashes:
- Pan station/survey table `data/ukpoms_1kmpantrapdata_2017-2023_samples.csv`: SHA256 `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`.
- Pan identified insect occurrences `data/ukpoms_1kmpantrapdata_2017-2023_insects.csv`: SHA256 `2423bc370f388a0dafd05c4bd3a7af7491909311ffe6bf4d6607a3697213dcb9` (inventory only; do not blend six-hour pan insect catches with 10-min FIT visits).
- Pan flowering-plant occurrences `data/ukpoms_1kmpantrapdata_2017-2023_flowers.csv`: SHA256 `53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba`.

Pan station records have native `sample_id`, `location_code`, `x1km_square`, `date`, `year`, `pan_trap_station`; flowering occurrence rows have `sample_id`, native `taxon_source`, `source_taxon_version_key`, `floral_unit`, `total_floral_units`. FIT 1km surveys have `sample_id`, `location_code`, `x1km_square`, `date`, `year`. **Only Pan `sample_id`→flower occurrence is a source-owned foreign-key relationship**. Do not join Pan sample IDs directly to FIT sample IDs.

### Deterministic, auditable join
- Confirm original Pan sample IDs are unique, every flower occurrence sample_id refers to exactly one Pan station row and each location_code maps to a declared square/year. Record invalid keys rather than discarding.
- Create exactly one Pan environmental record per (`location_code`, `x1km_square`, `date`) by grouping stations for that site-day. Record number of stations (expected up to 5), plant taxon labels (use provider taxon version key where present; fallback to source name only as an explicitly flagged legacy taxon), and number of distinct **recorded** flowering plant labels.
- Exact same-day FIT match must equal ALL THREE (`location_code`, `x1km_square`, `date`). An alternate grid+date-only diagnostic can reveal namespace collisions but is **never silently adopted**.
- Nearest-date (<=7 days, same year, same verified location_code and x1km_square) is a distinctly labelled context sensitivity. Choose minimum day separation, earlier Pan date in ties, retain at most **one** Pan context per FIT sample_id.
- Track FIT distinct sample IDs and source visit counts before/after; never multiply FIT observations by station count or flower occurrence count; store site- and year-level coverage, number of Pan sites, full 5-station coverage, and context taxon labels.
- Do not equate varying `floral_unit` across plant taxa. Mixed-type total floral-unit sums are noncomparable and cannot be a direct common-currency abundance measure.
- Treat Pan station with no linked flowering occurrence rows as `unrecorded` rather than `no flowering plants` until source metadata establishes explicit zero-complete survey semantics.

### Inference admission
If exact-date linkage passes >=10 unique sites AND >=100 distinct FIT pair-positive surveys AND source joins verify one-to-one at FIT grain, consider a **future separate** site-date contextual sensitivity model with Pan recorded flowering richness and station-coverage control, retaining full Stage 3d temporal/spatial/plant model and the preselected bumblebee/other-fly relative-count endpoint. This is not a confirmatory causal test. **Never refit a model if join coverage is inadequate, and do not choose a broader matching window based on significance.**

### Observed source-integrity exception (diagnosed before join fit)
The first original-data run found **11 original flowering occurrence rows whose `sample_id` has no matching Pan station record**. The original source itself is retained. Since an orphan occurrence cannot inherit a verified site/date, the original row count, orphan record count, unique orphan sample IDs and source years are emitted to the provenance receipt and those 11 rows are quarantined *only for geographical join construction*. They are never assigned an invented station, site or FIT survey. A standalone numerical test checks this explicit exclusion. No positive ecological inference is permitted until join coverage is recalculated.
