# Stage60 — authentic floral VOC × flower photograph bridge: a frozen source-backed visible-guide review queue

2026-11-17 JST. **Status: original source crosswalk and source image opportunity audit completed. Actual within-flower pattern/guide annotation NOT performed.**

## Provenance and actual data result

Upstream source 1: Farré-Armengol et al. (2020) floral scent (DOI https://doi.org/10.3389/fpls.2020.01154), original 305 species-labelled VOC PRESENCE rows, independently matched to 288 GBIF accepted taxa and 817 visual-source taxa in Stage59 PR #138, source-actions [44011328406](https://github.com/zuizui0223/adaptive-gain/actions/runs/44011328406) SUCCESS. The source `wind` column means **wind pollination**, not airspeed.

Upstream source 2: original FCP `zuizui0223/fcp` 4,475 plant species with **447,500 genuinely acquired/measured photos** and **227,107 coarse 4-colour classifiable photo records**. Stage48 source reconstructed complete original 4,475 taxa and FCP source-photo counts, independently joined with NHM botanical visible marking *text leads*; source [Actions 43854189546](https://github.com/zuizui0223/adaptive-gain/actions/runs/43854189546) SUCCESS. The original FCP photographs are not rehosted in this PR.

Stage60 original source workflow **SUCCESS** [Actions 44011763557](https://github.com/zuizui0223/adaptive-gain/actions/runs/44011763557), **five source-free QA tests PASS**, artifact **14297375491** ZIP sha256 `9a73899069e1dd521627c3163e7f8989fc4b349deba779fceabb76a24ec03e9c`.

| Original-source coverage metric | Verified |
|---|---:|
| Distinct FCP source candidate flower species | 4,475 |
| Original source VOC species | 305 |
| Exact original-binomial VOC × FCP photo species name matches | **80** |
| Strict accepted VOC species among these 80 | **80** |
| Distinct source FCP taxa with ≥40 broad-colour-classifiable photos | **55** |
| Original attempted photographs attached to those 80 source FCP taxa | **8,000** |
| Original broad-colour-classifiable photographs for 80 taxa | **3,822** |
| Independent NHM visible-marking text *candidates*, not measured signals | **3** |
| NHM marking text candidates and ≥40 photos | **2** |
| Original VOC `wind`-pollination marker on the 80 matched taxa | **4**, not wind speed |

Two independent review tiers: **2** NHM text marking candidates with ≥40 source photos, **53** others with ≥40 source photos, and **25** low-photo-classifiability candidates. Original source visible-UV state remains **unknown** for all 80 until real photo/UV measurements. A fixed pre-observation name hash splits the 80 candidate taxa into **53 internal discovery annotations / 27 internal blind-check taxa**. This is an annotation quality plan using ONE photo source, **not independent external replication of an ecological result**.

An independent crosscheck of actual original 305 accepted VOC names with the existing Stage57 817 original source names found **15** accepted source spectroscopic or age-reward evidence overlaps overall, **one** original direct UV spatial positive/uniform matched species, **two** mean UV-reflectance, **seven** age spectra. Those smaller cross-study optical overlaps are distinct from the **80 source-photo opportunities**, because RGB photos can visualize within-flower spatial patterns only after manual/image QA and cannot measure UV. Seven of the 80 source photo candidates also appear in the old 817 source evidence frame, but that does not mean the same exact specimen.

## Why this is not yet a multimodal floral-evolution result

1. Original flower photograph / FCP coarse colour four-state classification is **not** a measured visible nectar-guide label. Image colour can be broad and age-dependent, crop may include nonflowers, and classification can be uncertain. UV reflectance and UV spatial contrast cannot be read from RGB photographs.
2. VOC profiles are sourced from older, independently measured populations across 58 studies. An image with the same species name is not a voucher-matched flower with the same VOC emission, same air flow, photo, phenology or current receiver.
3. The photographed morphological signal and VOC trait are both missing local sites and evolutionary tree for a causally identified analysis. Exact names do not support direct E->guild->V, VOC×wind effects, actual plume cue usefulness or plant fitness.
4. `wind` mode is pollination syndrome, never meteorological wind speed or turbulent plume advection; no source m/s is supplied.
5. The original *Farré-Armengol* paper already examined VOC richness/composition against climate, pollination guild and phylogeny. Regressing scent richness on bee guild would only replicate known prior art.

## Immediate sample-annotation protocol (separate from finished source crosswalk)

Target **the 55 high-photo-coverage species**, with blinded audit on 27 source taxa (internal, same provider). For each original licensed FCP source observation/photo:

- Restore the original FCP photo ID and licence/owner link; no unlicensed rehosting. Log observer ID, observation ID, species accepted taxonomy, locality and time, cultivar/wild status, whether open flower is actually pictured. A flower absent from an image is *image ineligible*, never species guide-absent.
- If a single flower is in frame, annotate corolla, anther, landing platform and optional within-corolla localized visible mark. Preserve distinct geometric classes (vein line, bullseye, spot, contrasting reproductive organs, none **visibly verified**). At least two independent raters on a balanced subset; a proposed automated class requires original pixel-level validation.
- Record distinct `visible_mark_present` with *measured photo-specific negative*, `visible_guide_function` **unknown until behavior**, `UV_guide` unknown until UV photography, and `VOC_bouquet` from original source taxon only—not photograph.
- Only after original morphology classifications have credible negative comparison samples and ecology/phylogeny controls: fit phenotype `visible_pattern ~ habitat/light + plant ancestry + guild`, and compare with independent VOC composition `~ climate + ancestry + guild`. Analysis using few cross-studies must not call differing observational associations coevolution.
- To test conditional information topology vs static backup, independently manipulate early cue branch identity/availability, late odor/visual cue, wind/plume/sway, and actual pollen delivery within the same cohort; existing 2017 efficacy backup and 2026 spatiotemporal cue-weighting demonstrations should be explicit baselines.

## Essential prior-art originality firewall

Lawson, Whitney & Rands (2017) `10.1098/rsos.170996` and authentic Dryad `10.5061/dryad.3g591` already demonstrated visual backup under airflow/chemical odor noise. This used four allocated arms per wind/noise experiment (18 bees each): calm odor only, wind odor only, wind odor+visual, wind visual only. It did **not** include the full `wind vs calm × odor yes/no × visual yes/no` eight-cell factorial or an experimentally isolated early-information-router vs identical simultaneous cues.

Graver et al. (2026), `10.1242/jeb.251126`, already demonstrated learned bumblebee color/odor weighting shifting with the spatiotemporal scale of cue presentation. Thus **generic hierarchical multisensory strategy is not novel**. The novel falsifiable claim would have to show under matched channel intensities and decision budget that a first cue with zero direct target reward information changes which *later* cue is action-relevant and predicts contact/pollen beyond a static integration/backup model, with a measured wind-varying context.

Existing Stage58 mathematical `C_A=r+max(v,o), C_F=r+v+o` four-world exact demonstration uses abstract unit costs: source wind measured in Crall et al. and Chang et al. are not these values. No empirical trait selection/fitness result is claimed.

The source-verified Stage60 output `80_original_VOC_flower_photo_species_visible_guide_source_review_queue.csv` is a frozen **review opportunity list** with provenance, photo counts, missingness and internal split; do not infer 80 nectar guides or 80 wind-sensitive multimodal floral systems. PR draft; `main` unchanged.
