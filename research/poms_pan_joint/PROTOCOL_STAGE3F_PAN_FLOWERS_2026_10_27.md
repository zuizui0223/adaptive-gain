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
