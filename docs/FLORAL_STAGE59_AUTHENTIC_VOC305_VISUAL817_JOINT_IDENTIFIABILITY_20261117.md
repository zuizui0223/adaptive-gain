# Stage59 — authenticated flower VOC × original visual signal source accepted-species overlap

Date: 2026-11-17 (JST). Scope: **source-native taxon identity and evidence availability**. Not a multi-modal signal-effect study, wind × scent manipulation, pollinator information-use or causal evolutionary SEM.

## Primary audited original inputs and provenance

1. Farré-Armengol et al. 2020, https://doi.org/10.3389/fpls.2020.01154, original EuropePMC `PMC7412988` supplement `DataSheet_1.xlsx` `PRESENCE`; inner authored XLSX SHA256 `918ebcf51db693eb14ae8dec5eca1cb19fd48513cc345af050070d24e88ffe45`. A genuine original workbook, **4,461 XML rows**, of which 1 header and **305 distinct source species-name records**, remaining **4,155 non-species rows**; only explicit source-labeled species are used. Original paper's **851 VOCs** are compounds, not species or sensory information bits.
2. Distinct accepted 817 visual-source atlas Stage57 run [44009319879](https://github.com/zuizui0223/adaptive-gain/actions/runs/44009319879) artifact `14295149129`. Entries from independently measured UV spatial pattern, age spectra, 2025 measured mean UV reflectance and positive-only colour-change review, with missing states retained as unknown.
3. Strict source original name `Acer negundo` → canonical binomial → GBIF exact species, Plantae, confidence ≥95; no automatic genus-only or unrelated fuzzy synonyms. Names unresolved at source stay unknown and may later be audited manually. The crosswalk uses source GBIF accepted IDs, not literal matches alone.
4. Original successful Stage59 source GitHub Actions [44011082321](https://github.com/zuizui0223/adaptive-gain/actions/runs/44011082321): 6 source-free tests passed; accepted source artifact **14296278415**, ZIP SHA256 `9522821741ad3054345235f6a3711a709144cc86cc13c0cc6e06cd278b2f6552`. Original result with subsequent explicit no-positive-VOC field revision is rechecked separately.

## Original result

| Measure | Source-verified result |
|---|---:|
| Authored unique floral VOC source species labels | 305 |
| Lexically parseable source binomial names | 298 |
| Strict unique GBIF accepted flower VOC species IDs | **288** |
| Source nonexact GBIF names | 10 |
| Source names without lexical binomial | 7 |
| Earlier visual source accepted species | 817 |
| Accepted names with both VOC evidence and any visual-source evidence | **15** |
| Both VOC + directly measured spatial UV pattern (230-source frame) | **1** |
| Both VOC + Oliveira mean UV reflectance (243-source frame) | **2** |
| Both VOC + Ohashi stage-specific spectral archive (207-source frame) | **7** |
| Both VOC + 2025 positive-only colour-change review (124-source frame) | **7** |
| Distinct accepted source identity union `817+288-15` | **1,090** |

Source intersection may overlap across individual visual modalities; subcounts are not mutually exclusive. A source-accepted **1,090-name index** is **not** 1,090 jointly phenotyped flowers, ecological replicates, or a 1,090-species VOC×visual complete-case dataset. **15 shared species names** are not even the same sampled plant population or flowering stage.

Exactly nine original 305 source species have no explicitly positive numeric VOC column in the authenticated `PRESENCE` sheet; five-character/sparse summary/blank-cell definitions and source extraction limits must be distinguished from true floral scentlessness. These nine source names are *Aetanthus andreanus*, *Berberis sp.*, *Brownea coccinea*, *Chuquiraga jussieui*, *Gasteranthus oncogastrus*, *Mutisia alata*, *Oreocallis grandiflora*, *Razisea spicata*, *Symbolanthus calygonus*. A subsequent code patch keeps a separate `source_VOC_profile_has_any_explicit_positive_cell` and labels a zero cell count **unknown source profile, not odor absence**.

Original 305: wind-pollination YES rows **9**, Hymenoptera YES rows **44**, bird YES rows **22**. Critically source workbook's `wind` column is **WIND POLLINATION category**, not measured airflow, gustiness, plume advection, wind speed in m/s or disturbance to visual landing.

## Why not fit an 817/1,090-species multinomial SEM?

Source-measured visual UV guide contrast directly overlaps VOC in only one accepted species. The other two quantitative mean-UV overlap taxa are distinct signal modality, not source-measured spatial UV nectar guides. The two datasets are from distinct studies, periods, regions and individuals. A list union creates mostly *unknown* other-modality cells, not experimental zeros. Any model of `VOC ~ UV × wind × Bombus` treating all unmeasured fields as zero is false, and a sample selected to joint complete cases would be extremely sparse and source-confounded.

Known prior art: Farré-Armengol et al. already analysed climate × pollinator guild × scent from 305 taxa. 2017 `Colour as a backup for scent in the presence of olfactory noise` (PMCID PMC5717666) experimentally demonstrates wind-induced sensory efficacy backup by flower colour; 2026 `Timing impacts responses to color and odor in a model insect` reports spatiotemporal cue weighting. **Neither backup nor hierarchical sensory weighting can be claimed novel on their own.**

## Next viable route

- Source-verified FCP original **4,475 flower-photo species** (PR #128) can be exact-name joined to original VOC taxon inventory. Independent original two-artifact initial check finds **80** binomial-name matches; **55** have ≥40 source colour-classifiable photos, 3 NHM marking-text review leads. This is an **image annotation candidate set**: unlabelled photographs do NOT prove a UV or visible nectar guide.
- Build an auditable actual petal-sector visible pattern review from licensed original photos, with source image ID, accession/locality, repeat-plant control, missingness and human QC. Do not transfer flower-level original VOC chemistry to every occurrence of the taxon as if locally measured.
- For mechanistic evidence, test **fixed / static multisensory backup vs conditional next-cue routing** (first cue may carry zero direct reward information yet change which later cue is needed), keeping matched wind, VOC concentration, visible contrast, receiver identity, opportunity and pollen endpoint within an independently randomized study. Existing Stage58 exact routing cost demonstration is not yet an observation.
- Explicit location/phylogeny/environment controls, source study and sampling effort must precede any macro association claiming evidence of evolutionary selection.

Reproducibility: `research/floral_routeability_stage59/original_VOC305_visual817_accepted_overlap.py` uses authentic OOXML primary source and independent accepted-key crosswalk; 6 mock-only tests; dedicated source workflow `.github/workflows/floral-stage59-original-VOC305-visual817-accepted.yml`. Keep branch Draft, no merge to `main` and no claims of new pollinator visual-scent-wind adaptive effect.
