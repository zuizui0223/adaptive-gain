# Stage93 — Real floral-fragrance botanical prose from World Flora Online eFloras

**2026-11-19 JST. New source-discovery and source-only empirical audit, not a wind association or a causal scent effect.** Stacked onto Stage92 PR #171; no main edit.

## Original-source breakthrough

World Flora Online has public **Darwin Core Archive original botanical descriptions** for:
- Flora of China, WFO source resource 33516, original publisher eFloras, source URL https://files.worldfloraonline.org/files/eFloras/Flora_Of_China/Flora_Of_China.zip
- Flora of North America, resource 33517, original publisher eFloras, source URL https://files.worldfloraonline.org/files/eFloras/FNA/FNA.zip

Both publicly documented resources explicitly enable IMPORT_DESCRIPTIONS in the WFO harvest. The source bulk archives, not NHM's 59,369-row compact extracted trait field table, can be screened for explicit *floral* fragrance statements. WFO harvested these sources on 2026-08-03 (source page metadata); a first successful retrieval must record archive SHA256 and description-field schema and freeze them before a later model.

Examples of source prose supported by the original eFloras website include "Flowers fragrant" and "Flowers fragrant, opening widely, ... in diam." These are discovery evidence only and are not supplied as counts to the actual program. The 2020 305-species Farré-Armengol original emitted-VOC set remains a separate possible proxy validation dataset.

## Fixed source extraction and missingness rules

1. Retrieve the two original resource ZIPs. Read DwC-A meta.xml for row types, file names, field indexes and delimiters; do not assume arbitrary CSV positions.
2. Join original Taxon core ID to original Description extension ID, normalize only exact WCVP/NHM accepted species binomials (not infraspecific names or uncertain synonym merges). Confirm 55,775 source native plants in 367 TDWG3 regional lists, *including islands for source coverage only*.
3. Decode full descriptions as botanical prose with explicit flower/tepal/petal/corolla subject proximity for reported scent. Differentiate source-positive floral fragrance, explicitly negative (scentless/odorless/not fragrant), contradictory reports, and not mentioned/uncertain; garden-only and nonfloral scent should not be silently promoted to positive floral species states.
4. Independently record WFO source identity, description length (for source-ascertainment correction), within-species original text duplicates (SHA, not independent species), and source animal/wind/unknown GIFT pollination mode; source-level missingness is not biological absence.
5. Derive only regional source-coverage counts and authentic raw-source SHA manifests. Do not upload all full descriptions, or use any initial original prose cues to select a wind coefficient. The first new WFO archive fingerprint is source discovery; later cross-region comparison must pin it.
6. Require real independently audited mainland-only polygons, long-term ERA5 1991–2020 daily max 10m gust >15m/s across climatological >5C eligible months, climate/canopy and taxonomy controls before any wind regression.

## Important limitation

Floristic descriptions can be highly uneven in detail. Even an exact phrase like "Flowers fragrant" is a **reported human description**, not measured emission flux, ecological pollinator plume, nocturnal pollination mode, or chemical communication effect. Explicit negative citations may be extremely rare. The source collection is regionally uneven (China/North America) and lacks unbiased recording/quality standards; compare source-conditional rates before claiming true species fragrance proportions.

Any nontrivial stage-93 regional count can justify broadening textual-source coverage, but absence of explicitly negative documentation blocks the biological negative-vs-positive prevalence estimand. No forcing all three sensory endpoints onto a single complete-case species subset.

## Code and execution

- research/floral_macro_stage93/original_wfo_eFloras_scent_full_prose.py
- research/floral_macro_stage93/test_original_wfo_eFloras_scent_full_prose.py
- .github/workflows/floral-stage93-WFO-eFloras-original-scent.yml

**Actual original-source counts: pending first verified Actions run.** If original archive is unreachable or does not contain expected DwC-A meta and description linking, fail and record source limitation. Do not claim original records were actually read until verified success.
