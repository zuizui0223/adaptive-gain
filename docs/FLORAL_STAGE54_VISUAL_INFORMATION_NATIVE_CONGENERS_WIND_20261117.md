# Stage54 | Floral visual information across lineages, pollinator guilds and wind

Status: 17 November 2026. Source-backed atlas and candidate contrasts, not evidence of general adaptation or plant fitness. This research line is independent of earlier wind-landing Stages 37–44.

## Central falsifiable question

Which floral visual channels (long-distance colour display, UV/visible landing guides, flower-age and reward-state change) are evolutionarily associated with receiver guild availability, and when does wind/flower movement change the behavioural value and accessibility of those signals?

**No single “visual signal present” binary can represent all these channels.** Every phenotype must retain source, receptor, modality, outcome stage, direct-measurement quality, geographic origin and missingness. A uniform UV flower can still have a visible guide or age-dependent colour change. A review containing only changers gives no unchanged species denominator.

## Actually verified botanical data and limits

1. Original Koski & Ashman 2016 + Tunes et al. 2021: 230 independently GBIF-accepted species with UV spatial contrast measured at source, **101 patterned and 129 uniform**, after original accepted-key deduplication. Another 32 accepted species only have historical UV-absorbing area trajectories, not categorical visual guides. Total 262 accepted botanical species in source atlas. The source 2016 method's discrete 0 represents patterned, 1 uniform.
2. Original Ohashi, Makino & Arikawa 2015 age-resolved reflectance archive (doi:10.5061/dryad.8fh42): **219 source taxon/variety directories**, strict GBIF name crosswalk **212 original source rows to 207 accepted species**. Only 3 accepted species overlap the original UV262, so the union has **466 accepted species**. The original ZIP central directory was verified via bytes/range against source file size; full 285.9MB archive checksum not independently downloaded. No per-species colour-change status can be inferred from a directory. The source article reports bee-perceptible age changes for 48/219 taxa, butterfly 97/219, fly 28/219, and changes perceivable to any tested pollinator class for 101 species, but this manuscript-level total is not yet the per-species response table.
3. Original 2025 review (doi:10.3390/plants14142185): reports 151 literature-documented colour-changing species in 55 families. Its actual original Table S1 supplemental PDF SHA256 0c2ba82cd6eb554942fc3ac93014f7ecc9834686f695cf628f2873a2be213039. First extraction: **136 source taxon-column groups, 128 provisional binomial candidates**; remaining source rows/aliases not yet verified as 151. This is SECONDARY/POSITIVE-ONLY evidence, not a population of measured negatives and not confirmed reward cues.
4. Published 51-clade flower/fruit-colour study (Sinnott-Armstrong et al., 2026; doi:10.5061/dryad.r4xgxd2sc) contains human-view eight-colour categories for **2,960 taxa** plus 51 clade phylogenies. Official Dryad original file manifest and SHA256 for final_dataset.csv and trees.zip checked; actual per-species content source audit separate, not relabelled UV.
5. Published Taiwan elevational flower-colour dataset (doi:10.5061/dryad.63xsj3v08) includes a **727-species original list** and phylogeny. Source CSV access/specific trait columns still being verified. Country, altitude and colour are not nectar guide.
6. Existing original FCP 4,475 flower-photo species and NHM 59,369 source trait taxa, with 3,412 exact name intersections and 58 source textual marking leads among FCP plants, remain additional review opportunities, NOT source-measured guides.

**Species evidence is overlapping and must not be summed.** The count of 466 is accepted botanical species with at least one of UV phenotypes / named age-resolved reflectance source. It is NOT 466 visually signaling species.

## Close-relative controls actually constructed

Original 2016 directly measured patterned versus uniformly absorbing UV species within the same named genus with Kew WCVP confirmed native botanical WGSRPD Level-3 area overlap:

| Selection | Nonrepeating congeneric UV-opposite pairs |
|---|---:|
| Same original genus and at least one shared native Kew plant area | 61 |
| Above, plus published latitude within 10 degrees, UV-B within 1200, annual temperature within 6 C | 53 |
| Above, latitude within 5 degrees, UV-B within 700, temperature within 4 C | **45** |

Strict 45 pairs span two author genera and have a mean source latitude gap 1.303 degrees. Actual source CI 43900591747 succeeded, with source-validated 159 GBIF accepted species and 153 having >=1 Kew native area. These are **measured opposite UV states**, not sister species, local sympatric populations, “no visual signal” flowers or experimental causal controls. Pair sets under three alternative thresholds are not independent biological replicates.

For developmental colour change the matched-negative source must be Ohashi’s 219 species with their original early/mid/late spectra and species-level pollinator receptor outcome table. Do not use the 2025 review's unlisted taxa as negatives. A direct functional comparison exists between colour-changing Weigela coraeensis and comparatively nonchanging W. hortensis (Suzuki and Ohashi, doi:10.1111/1365-2435.12209), with observed visitation, pollen receipt and seed production, but it differs in more than colour and is not proof that colour alone causes fitness.

## Original source specificity and native geography

Kew WCVP WGSRPD native **Level-3 area** is not a plant occurrence polygon, political country, measured original flower sample site or proof of sympatic bee presence. The previous Stage52 2016 UV pattern / source Bombus-richness association was source-window dependent: pooled Bombus/all-bee model name ratio +0.0480 for sampled original north-latitude groups, but +0.0112 in 12 posthoc genus/latitude/UVB/temperature matched pairs and leave-one-pair-out sign reversal. Do not claim a verified phylogeny/climate-independent adaptation. Use source-site botanical vouchers and independently modeled pollinator native-accessible species before inferential comparisons.

## Wind is a MODERATOR of information access, not a global flower trait axis

Mechanistic independent evidence (different species, manipulations, denominators):
- Baird, Boeddeker & Srinivasan 2021, doi:10.1098/rspb.2020.3051: **honeybee visual optic-flow wall texture and head/tail wind** were manipulated at 1–2 m/s. True visual-input × airflow design, but not flower petal UV or reward signaling.
- Chang et al. 2016, doi:10.1242/jeb.137976: original Bombus impatiens flower landing in 3.5m/s headwind; previous independent source analysis shows approach/landing speed sign robust. Not pollen or plant fitness.
- de Vries et al. 2025, doi:10.1242/jeb.249380, Dryad 10.5061/dryad.qbzkh18tj: **728 successful Bombus terrestris landings** from 2 hives on moving mimics at 0/0.03/0.24/0.53/0.65 Hz. Wind-induced flower *motion*, not direct wind-flower colour manipulation; original trial success denominator must be verified separately.
- Wang et al. 2026, doi:10.1098/rsif.2025.1198, Dryad 10.5061/dryad.37pvmcvzz: 48 Bombus terrestris individual recordings, model of visual optic-flow + angular-inertial control while landing on oscillating targets. Not measured nectar-guide evolution.

**Testable conditional route:** visible display affects detection; petal UV/visible target cues and optic expansion affect approach/landing; flower-age colour may inform learned reward choice. Wind or floral movement alters the cost/reliability of near-target cues. To test the mechanism, use a within-species, receptor-controlled visual-guide × airflow/flower-motion factorial and separately record detection, approach, touchdown, contact, pollen deposit and seed-set with stage-specific denominators. Multiplying results across Chang, Ohashi, Baird, de Vries or different species cannot give a net floral fitness effect.

## Analysis execution and stopping rules

A. Retain independent measured botanical modalities with source DOI, accepted species key, original population/voucher and receiver's spectral test, and explicit unknown instead of false negatives.
B. Resolve sister-pair relationships using independent original phylogenies, native/local accessible overlap, climate/light and phenology, then compare traits against species-specific original bee guild model (3,370 modelled bee names including 133 Bombus; 2,695 eligible bee HEX). Do not call modelled species richness actual bee abundance or visitor effectiveness.
C. Test only prespecified spatially blocked, source-study held-out, climate/phylogenetic/observer-effort-controlled associations. Require independent populations/bioregions and comparable direct signal states. The original 2016/2021 phenotyped plants cannot be assumed to express the same UV traits at every contemporary opportunistic GBIF occurrence.
D. Functional reward colour / optical motion interactions are separately testable from the macro survey. Stage37–44 wind evidence is background/mechanistic calibration until a joint wind × floral vision × real pollination dataset is obtained.
E. Falsification: if related plants with comparable native source pools and environment differ little in receiver guild or signal effect, or if the positive association disappears under source/phylogenetic/climatic conditions, do not declare general visually mediated selection.

**Current verified result:** 61 / 53 / 45 measured opposite-UV congeneric controls, original age-resolved spectral taxa expanding the distinct accepted-key source frame to 466, original review 136 candidate taxon columns, and documented direct experimental literature to connect visual-motor access and wind. No new causal pollination or robust macro UV×Bombus coefficient is claimed. Development PR remains Draft/unmerged; main untouched.
