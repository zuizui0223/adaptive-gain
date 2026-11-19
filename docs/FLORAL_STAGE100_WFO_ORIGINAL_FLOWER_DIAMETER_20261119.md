# Stage100 — Source-original WFO eFloras whole-flower diameter descriptions

**2026-11-19 JST. This is source evidence discovery, NOT a wind effect or a pollinator-visible floral size measurement.** Draft stacked on Stage99 #178, main unchanged.

## Scientific bottleneck

The SHA-verified original AusTraits 7.0.0 source provides only **104** exact WCVP accepted native species with source-labelled flower_diameter; the untouched 37 mainland holdout regions have **54** such species, of which only **19** are novel versus the geographically contact-free 72-region training flora (Stage99). This is not enough to assert broad floral size evolution or independently replicated wind selection. The next valid source is full botanical prose from original Flora of China and Flora of North America, independent of AusTraits.

## Original-source retrieval

- Restore original verified NHM 59,369 source species labels and Kew WCVP 55,775 accepted native species × 367 TDWG3 regions, including islands in the raw source inventory.
- Independently load original GIFT 3.2 pollen-vector source labels, preserving unknown (never infer mode from flower colour or genus).
- Restore full WFO eFloras original botanical treatment DwC-A ZIPs using their previously confirmed byte-level SHA256: China **4c0b89280efdcfd0ef8dc753cca5d63566ddf8c34542b0bb4a78cdce799b63a9**, North America **0757eb55f2e844383d34650ea3aa577d15c2210f3893561b6694559dd9aa02e1**.
- Use official WFO 2026-06 ID-to-accepted-species classification archive, Zenodo record 20782718, MD5 **0e4486945cd9f7af548ca87eb9a870ed**. No fuzzy taxonomy; no assumed WFO name lookup from raw ID alone.
- For code stability, the latest source-validated WFO 2026-06 original taxon-ID and botanical description reader is included as a frozen, explicit snapshot in research/floral_macro_stage100/wfo202606_source_reader_frozen.py. It is not a fresh inferred identity map.

## Source-only flower diameter lexical parser

Identify English explicit phrases indicating **flower/flowers diameter, flowers ... mm across/diam., or corolla diameter/width**. Preserve flower and corolla categories as **distinct types**, and reject intervening leaves, peduncles, capitula, inflorescences, spikes, fruit, stems, bracts and other non-flower organs.

Admit single physically plausible original mm/cm numeric values and convert to mm. Skip numeric ranges for the initial high-precision candidate set; values are not automatically taken as means or interval endpoints. If multiple source statements for the same species disagree by more than 1.5-fold, classify as a source-conflicting candidate rather than return an arbitrary size.

Even the admitted true *whole-flower diameter prose candidate* is **unreviewed lexical evidence**, not a direct experimental measurement of flower viewing angle, display contrast, detection distance, open stage, or visual signaling. Source descriptions may represent sampled population ranges or geographic species generalizations; all missing size descriptions are UNKNOWN, never zero-size flowers.

Outputs: distinct authentic WCVP native accepted species candidates, source collection and GIFT pollen mode coverage, genus counts and regional-native record repetitions. The original 367 regions include islands until Stage94 geographic eligibility is joined in a separate stage. No botanical/prose copyright bulk redistribution; publish derived-only source counts.

## No inferential overreach

Do not fit a wind × flower-size coefficient from this newly discovered raw-text trait without independently reviewing positive extraction accuracy, excluding inflorescence/corolla-only items, considering source study/reporting effects, taxonomic source bias, and original geographic source recurrence. Strong gust metric remains under development: Stage97 acquired 50 points, but no 125-region land-area-weighted CDS hourly 10fg baseline. No insect recognition, olfactory plume, learned cue order, natural selection, or fitness is identified from this source task.

Code:
- research/floral_macro_stage100/original_WFO_flora_flower_diameter_prose_candidates.py
- research/floral_macro_stage100/test_original_WFO_flora_flower_diameter_prose_candidates.py
- research/floral_macro_stage100/wfo202606_source_reader_frozen.py
- .github/workflows/floral-stage100-original-WFO-flower-diameter-prose.yml

**Real species counts pending original-source CI.** Do not insert a fabricated positive number if the strict lexical parser finds no authentic complete flower-diameter records.
