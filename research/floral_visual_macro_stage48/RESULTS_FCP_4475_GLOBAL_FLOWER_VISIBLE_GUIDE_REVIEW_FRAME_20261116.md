# Stage48 — globally sampled flower-photo opportunity × source visual pattern review registry

**2026-11-16. Original species-level source-backed discovery, no new flower-guide phenotype or Bombus joint model fit.**

## Main actionable result

Re-used the user's FCP original 4,475 species-level photo-measurement ledger, verified as Git blob SHA1 `95ec1140a622ae11c816bcfbd1d3b33150ec104a` from Git commit `c45a95420a96abfb3fdb8e9ad1a37c75288c63fb`. Exactly **447,500 attempted original photographs**, **227,107 classifiable four-state colour photographs**; these do NOT yet contain within-corolla guide annotations. Source CSV SHA256 `23d3daadc9799c2e7b5867d54ccc1ed98369ba79a81b72dc7f831e5197e63c49`.

Independently obtained source-authenticated NHM 2026 `NaturalHistoryMuseum/plant-traits` original 59,369 taxa (Git blob SHA1 `e1cfd2d5c518c2061ec91d1a9e8b64fc7ca69389`, doi:10.5519/p3dm31kc), of which 353 original colour description strings include potential visible spatial marking terms. Original 2021 Tunes et al. UV photography and spectrometry source supplement PDF pinned SHA256 `d11b41a36d85d1b70c8d3d47c04f3e03e7d8f5f58ebaaa331a737e56ed4c2820`, 80 taxa, 26 measured UV patterned categories.

The three sources were merged by **unambiguous exact candidate binomial spelling only**, not accepted taxonomic synonym resolution or photograph-level floral trait scoring.

| Review coverage/priority | Actual original-source result |
|---|---:|
| FCP original flower-photographed species in new output | **4,475** |
| FCP species exactly matching ONE NHM source taxon name | **3,412** |
| FCP species with no exact NHM name | 1,063 |
| FCP species with NHM unconfirmed visible marking TEXT candidate | **58** |
| FCP species whose names exactly match original UV measured source taxon | **8** |
| Original UV reference + photo candidate | 8 |
| NHM textual marking candidate + >=40 already-colour-classifiable photos (excluding original UV priority) | **46** |
| Remaining >=40 classifiable photo candidate species | **3,244** |
| Remaining low-classifiability photo candidate species | **1,177** |
| **Sum of four nonoverlapping review queues** | **4,475** |

**No photograph was reviewed for nectar guides or flower-sector orientation by this stage.** An NHM textual 'spot/stripe/vein/bicolour' is only a search cue, not a proven guide. 'No NHM marking keyword' is not botanical absence. No UV phenotype was inferred from FCP conventional RGB photographs. A UV label from the 2021 source study is *not transferable to another individual, geographic location or original FCP image* without validation; eight exact source name matches are merely reference cases. The >=40 photo criterion measures broad coarse-colour classifiability only; it does not validate petal region segmentation or consistent guide imaging.

## What the pipeline makes immediately possible

1. **Original-photo review seed**: 46 source-supported candidate taxa, source iNaturalist Taxon IDs, original source photo count and classification count; preserve no inference about UV.
2. **Within-species and geographic test controls**: 3,244 original-photo taxa with >=40 colour-classifiable images allow balanced review sampling across plant lineages, locations and observation effort rather than visually selecting only spotted species.
3. **Original UV reference checks**: eight taxa whose names occur in the authenticated 2021 80-taxon UV study; can guide validation design but cannot be treated as images with measured UV patterns.
4. **Data quality**: keep the 1,177 classifiability-poor taxa and 1,063 NHM-name unmatched taxa as explicit NA/unmatched strata, never negatives.

### Next phenotype measurement gate (not performed yet)

For each selected original licensed iNaturalist/FCP photo, require flower and petal/corolla segmentation, visible within-flower multi-sector contrast, radial guide orientation to entrance/reward, flower age/flower organ/exposure state, photo identity, and human verification. No artificial UV channel may be generated from RGB. UV spectra/photos from an independently measured source retain separate observability codes. Licensed-photo rehosting requires original attribution/licence review. This must precede fitting any guide trait against predicted bee species maps.

### Main statistical macro target

(G_{s,c}): verified species s floral visible-guide or UV-sector architecture measured in a documented region/time c; (B_{c,g}): source-native/suitability-filtered bee group or Bombus model predictions in same accessible/temporal cell, never GBIF photo count. Compare bee-guild availability with source-measured information traits controlling climate, light, plant lineage, species occupancy, accessible source region and photo sampling. Separate structured within-species variation from between-species traits. Do not treat 4,475 species as UV-guide-documented or 353 NHM lexical candidates as proven positive; both would inflate the response numerator.

## Reproducibility

- `probe_fcp_photo_species_frame.py` — exact original FCP 4,475 source species and schema; offline tests and source-only workflow.
- `crossmatch_fcp_nhm_uv_candidates.py` — independently checksum-pinned FCP/NHM/UV original input merge into an auditable 4,475-species reviewing queue.
- Six mock-only tests of source-grain, ambiguous taxonomy, no false absence, and classification count.
- Original source Actions run [43854189546](https://github.com/zuizui0223/adaptive-gain/actions/runs/43854189546) **SUCCESS** (initial source run); output: 4,475-row source review CSV and source provenance JSON in the Actions artifact. Re-run and independently check final PR head whole Python 3.10–3.12 matrix before calling software freeze.
- No original image pixels are committed or redistributed, no new insect occurrence, flower-guidance behaviour, pollen transfer, seeds or fitness analyzed.

**Scientific scope:** This is a user-owned macro species discovery / photographic review sampling frame, not a literature effect-size meta-analysis or verified pollen-mediated visual information adaptation. Stage47 original Cerrado study-site test remains a geography overlap feasibility result, not the macro plant-trait effect.
