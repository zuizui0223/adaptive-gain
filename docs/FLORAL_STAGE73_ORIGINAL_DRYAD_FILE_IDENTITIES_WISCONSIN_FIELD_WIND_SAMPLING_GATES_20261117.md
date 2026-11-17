# Stage73 | Original multi-region floral signals and receiver environments: source provenance, admission and identifiability

**2026-11-17 JST. Draft PR, stacks on Stage72 PR #151; main unchanged.** This stage executes two independent original-author-source access procedures. One discovers official Xie/Albor Dryad file identities but confirms an unauthorized file access barrier. A second successfully ingests Wisconsin field wind×floral trait×visitor source records with an original Git blob SHA and identifies that local wind cannot be separated from site-date strata in this source.

## 1. Correct original Dryad source identity: China and California

After Stage72 only recorded the Dryad titles/DOIs, Stage73 uses the **documented official Dryad API v2** `/datasets/{doi}/versions`, `/versions/{version-id}/files` and `/files/{file-id}/download` rather than constructing guessed file URLs. Source metadata response JSON bytes are independently SHA256 logged.

| Original study | Dataset DOI | Original version ID(s) | Original versioned file metadata | Actual original file bytes |
|---|---|---|---|---|
| Xie et al. (2025), China | 10.5061/dryad.612jm64gq | **406487** | **4 original filenames + immutable source SHA256** | **No, HTTP 401** |
| Albor et al. (2022), California | 10.5061/dryad.2ngf1vhrb | **187121, 188497** | **2 original filenames + immutable source SHA256**, same actual file IDs across two version records | **No, HTTP 401** |

### China: exact original archived file identities

- `bee_visitation_frequency_to_each_floral_color_within_each_island.xlsx`: file **4450812**, **11,677 bytes**, original Dryad SHA256 `df10807d357feae189a6041567748f21cee17109c6e3f4988f82c0ee247a2bf5`.
- `flower_color_reflectance_spectra.xlsx`: file **4450811**, **554,537 bytes**, original Dryad SHA256 `a00d5560daefb47d04c354955cefce55b128da0a76013a6b875979860ef2073d`.
- `plant_bee_interactions_on_islands.zip`: file **4450810**, **286,903 bytes**, original Dryad SHA256 `6acbd86793ff7f6f3e53ff8894604f39342f27c12cecc2f767f277244838a393`.
- `README.md`: file **4450817**, **3,733 bytes**, original Dryad SHA256 `6e2c8fdf105ebb9c9b73dc3d239ccee4911ecf8a09b016fa6d62dbb5911c051a`.

The source metadata describes a spectrometer 300–700 nm flower reflectance matrix for 98 plant codes and 42 Excel files of original island/mainland plant×bee interactions across the 41 islands and mainland sampling scheme. These are **author-documented schema facts only** until source bytes are retrieved. Do not claim 98 real reflectance spectra ingested or 42 underlying matrices parsed. Published flower-color bins B/BG/G/UB/UG should not be treated as true binary spatial nectar-guide states.

### California: exact original archived file identities

- `Data_Albor_etal_2022.xlsx`: file **1644670**, **300,928 bytes**, official source SHA256 `f334eeb7bfdc3e728f3f5f229592c9ab1c6eb21d5db84b72fa5215ba5acae52a`.
- `README_Albor_etal.2020_FuncEcol.txt`: file **1644653**, **4,453 bytes**, source SHA256 `728d1476574c340fa62545e11d70ab1140e00af9e75586ce71095490ff56aa7b`.

Both version records enumerate the same file IDs and byte checksums. **File downloads** from `/api/v2/files/{id}/download` and complete dataset `/datasets/{doi}/download` returned **HTTP 401**. This is a genuine anonymous API access barrier in this execution, **not** evidence the public original data are biologically absent, nor justification to infer rows or regressions from titles. Full source-integrity audit source [GitHub Actions 44087634613](https://github.com/zuizui0223/adaptive-gain/actions/runs/44087634613) **SUCCESS**, artifact **14330206937**, SHA256 `899519c0d52ef1789663ddc064fb8ecb6c1774e21a0a29da033bd8eaa751197d`.

## 2. Independent public original field study with WIND: Wisconsin

The authors' **public GitHub primary repository** [Plant-herbivory-interaction-lab/CammaranoMonardaPollinator2024](https://github.com/Plant-herbivory-interaction-lab/CammaranoMonardaPollinator2024) includes the original `Data/Pollination_neighborhood_data21.xlsx` Excel for four Wisconsin field sites. This source is independent geographically of Greece, China and California. The original source file, **69,522 bytes**, Git blob SHA1 `d456ddae4b5a737fc3351a5df612bd6a4b2c6244`, **source actual SHA256 `daae53668f32f700154378460388cba83334234f16d80844ab94539a5c9635fc`**, has been fetched and authenticated as an original author-published binary with seven real workbook sheets:

| Original workbook sheet | Actual source data rows | Biological meaning |
|---|---:|---|
| `plots` | **143** | Four source study sites, date/plot, Beaufort wind, temperature, sun, duration, focal staminate/pistillate flower counts |
| `plants` | **484** | Field plot flowering species and their floral abundance/height |
| `visitors` | **356** | Original flower visitor taxon, numbers and inflorescences visited |
| `plant_spp_traits` | **25** | Species-level reference-derived visible petal colour, coarse ordinal `petal_wvl`, shape/symmetry/corolla |
| `visitor_spp_traits` | **36** | Visitor recorded classification/length from named source references |
| `density` | **100** | Additional vegetation data for only two of four sites, not a common source wind/trait sampling unit |
| `metadata` | **38** | Workbook internal variable descriptions |

**Original source wind classes are Beaufort 0/1/2**, not anemometer velocity or an intervention. **`petal_wvl` is an ordinal literature-based visible colour scale, NOT a measured optical wavelength in nanometres, bee receptor contrast or an original UV nectar-guide presence/absence measurement.** The labels cannot be added to original spectrometer-derived petal reflectance as if directly measured on the same scale.

### Critical source date discrepancy, independently verified from workbook calendar definition

- Author README explicitly says summer **2022**.
- All **12 actual original field date serials** (44383, 44386, 44387, 44389, 44394, 44395, 44396, 44397, 44403, 44405, 44406, 44408) convert to **2021-07-06 through 2021-07-31**.
- Unlike a guessed epoch, the workbook's original `xl/workbook.xml` calendar was independently read; it is **`EXCEL_1900`**.
- Thus the mismatch is a **real original workbook–README year conflict**. Its cause is **UNKNOWN**. Until correspondence with the authors or original source records clarifies the year, **DO NOT match to external 2022 or 2021 weather reanalysis and pretend date provenance is resolved**.

### Original site-date-plot join and observational wind gate

By strict `(site,date,plot)` key (instead of falsely collapsing plot 1 across dates/sites):

- Original `plots` has 143 rows but **142** distinct composite keys; **one key occurs twice**. All rows for that duplicated key are excluded until its identity is resolved, producing **141 uniquely identified field plot strata**.
- In `plants`, **477/484** rows link to an unambiguous original plot key. In `visitors`, **350/356** rows link; **6** visitor rows lie in the ambiguous/duplicate plot, and **7** plant rows do not have unambiguous plot linkage.
- Of 141 plots, 16 have no listed source visitor rows. These cannot be asserted to be verified zero biological visitation without source detection semantics. Some visitor rows record a switch to a second flower species and are not silently collapsed into first-plant visit totals.
- Original plot wind distribution: **Beaufort 0: 16 plots, 1: 44 plots, 2: 81 plots**. Source site IDs `BEN`, `MNP`, `UWM`, `UWW`.
- **12 distinct source site×survey-date groups**. Critically **0 of the 12 groups contains more than one Beaufort category among its plots**. Wind is **constant within each source site×date**, meaning a model that conditions on site×date cannot separately identify a wind effect. Simple wind×visitation pooled contrast confounds source site/date with wind and plot/flower abundance.
- 19 visited plant names literally match the 25 original literature-based plant trait labels. Original visitor taxon list includes **37** distinct names, 36 original insect trait labels, with 1 visitor label outside the available trait table. 13 otherwise matched visitor records mention a visited plant not in the exact same plot flowering species listing. These discrepancies are not imputed.
- Original visitor row `flower_visits` denotes inflorescences visited, while `visitor_no` denotes visitor individuals; neither is an automatically standardized fruit/seed production or effective pollen-transfer rate. Sum of visits across wind categories, without plot denominators and site-date conditioning, is misleading.

**Scientific consequence:** This dataset supports actual *within-field study* floral visible-colour×flower abundance×recorded insect-guild analysis and native wind/noise source documentation, but does **not** identify a causal wind×visual signaling effect. The wind association is not identifiable under full site×date blocking. Wind and VOC are not simultaneously measured together with genuine spectrometry in this source. Four sites are NOT four independent climate-zone evolutionary replications.

Original real source [Actions 44088131106](https://github.com/zuizui0223/adaptive-gain/actions/runs/44088131106) **SUCCESS** raw source seven-sheet audit. The finalized original source-epoch/unique-plot join [Actions 44089041773](https://github.com/zuizui0223/adaptive-gain/actions/runs/44089041773) **SUCCESS**, 13 source-free guard tests passed (6 schema + 7 join/date), final artifact **14331165838**, SHA256 `feaf550ebe8a1dd8a382c25ed2b2dda511062778d24856629b78d29e19380696`.

## 3. Integrated ecological claim ceiling

Validated original source data now cover **two distinct geographical study systems for complementary modalities**: Lesvos (original VOC emission × real 2018 plant–insect network; Stage72 40 exact name joins, 7,954 original source visitor count) and Wisconsin (original site/date wind Beaufort × literature categorical visible flower traits × actual source bee/other visitor records; Stage73). **They do not jointly measure actual floral UV/spatial nectar guide, emitted VOC, wind regime and visitor behavior in the same site**, so this is not evidence of ecological conditional cue-switching. Do not pool independent source sample sizes across incompatible measurement types as a pseudo-global sample.

The two additional regions with measured field optical spectra and visitor networks (China Xie and California Albor) have **official source versions, filenames and checksums identified**, but the actual data remain unavailable without authorized Dryad download. They are **prospective acquisition** targets, NOT completed independent source effects.

A well-defined future hypothesis, if the raw data can be obtained and independently matched, is whether modality-specific observed floral signals predict visitation **conditional on receiver community opportunity and sensory noise**, with genotype/phylogenetic confounding, source site/year phenology, floral abundance and sampling effort accounted for. Current source-independent evidence cannot validate wind-driven modality compensation or selective loss of UV nectar guides. Existing prior publications on multimodal floral signals and pollination network formation are recognized, so a generic visual-scent-visitation association is not a novelty claim.

**No new global UV–guild effect, within-block wind coefficient, p-value, causally identified adaptation or fitness is claimed in Stage73.**

## 4. Executable evidence

- `research/floral_original_field_stage73/resolve_original_Dryad_versions_files.py` + eight source-free guards. GitHub workflow `.github/workflows/floral-stage73-official-dryad-binary.yml`, Actions 44087634613.
- `research/floral_original_field_stage73/audit_original_wisconsin_wind_visits.py` + six source-free guards. GitHub workflow `.github/workflows/floral-stage73b-original-wisconsin-wind-visits.yml`.
- `research/floral_original_field_stage73/validate_original_wisconsin_plot_date_wind_guilds.py` + seven source-free guards, source-exact three-key visitor joins, Excel workbook epoch verification. Actions 44089041773.

Scientific next gate: verify public source-level data for a second *same-modality* truly measured optical and guild dataset, or obtain original Dryad source bytes through lawful authorized researcher/institution access. For Wisconsin, resolve author source calendar year, plot key collision and original site×date-level wind design before attempting external climate matching, causal regression, or sign claims.
