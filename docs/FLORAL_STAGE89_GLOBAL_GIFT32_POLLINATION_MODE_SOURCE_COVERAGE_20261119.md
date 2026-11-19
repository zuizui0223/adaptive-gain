# Stage89 | Genuine independent pollination-mode labels: global geographic floral hue/receiver contrasts

Date: 2026-11-19 JST. Authors' original source classifications and artifact hashes verified. This is a new macroecological correspondence screen, NOT demonstrated adaptive visual or multimodal sensory cue-order change.

## Scientific reason for Stage89

The initial Stage87 worldwide source flora results showed regional winds correlate with floral description hue green/brown and observed Bombus species richness with yellow/purple, after regional temperature, rainfall, solar radiation, vapor, geography and source recording coverage. Stage88 then showed the original wind-brown correlation vanished after removing three graminoid families, with the source SAME 268 global TDWG regions and paired geography block 95% delta -0.00775 to -0.00203. But a family proxy is not a direct source pollination-mode classification.

Stage88F read original AusTraits v7, 1,798,215 raw source trait records, exact source pollination_syndrome for 4,619 one-label source species. Only 631 source species matched the 55,775 strict accepted NHM/WCVP globally native plant taxa: 476 insect, 155 wind, and ZERO regions with >=10 wind taxa having source one-hue flower documentation. Therefore no whole-world insect-vs-wind spatial test was valid from that source alone.

## Original external GIFT data: 5,770 genuine species, 3,172 matched globally

- Independent genuine GIFT stable version 3.2: original API download and semantic source checks in zuizui0223/island GitHub Actions run 34803493307, source artifact 10332810251, GitHub ZIP SHA256 074a52323ba835201043a3a5980cc2b2d0ff79878e83bc9be19511ae83a1c0e8, original 2026-09-14T03:43Z.
- Actual public source intake 14,122 raw API trait rows from 23 independently enumerated public/non-bias reference-trait source pairs. GIFT catalog includes 372,098 original species taxonomy metadata rows. Author taxonomy checks exclude derived traits, restricted references, rank mismatches and source mixed/contradictory pollination labels.
- Existing GIFT qualification declared 5,771 assignments: 4,538 biotic and 1,233 wind. An additional strict two-word source-rank recheck identified source literal "Taraxacum sect." among biotic assignments, which is a section, NOT a biological species. The valid species-rank analysis starts with **5,770 strict binomials = 4,537 biotic + 1,233 wind**.
- Original native flora exactly reconstituted from SHA-pinned NHM 59,369 botanical taxon text and original Kew WCVP 2026 55,775 strict accepted native plant names in **367 TDWG3 regions**. Strict name equality finds **3,172 real species (2,560 animal-mediated, 612 wind-mediated)**. Other **52,603 native source species** lack qualified GIFT mode and are UNKNOWN; not assigned to wind. Of 5,770 GIFT binomials, 2,598 do not map to the strict native NHM/WCVP cohort.
- After requiring actual >=10 source one-hue plants in each original mode per region, global WCVP climatology complete and no repaired TDWG geometry, the **same 155 source TDWG regions** have BOTH animal and wind mode measured flora, with 28 blocks at 20x45 degrees and 21 at 30x60. Archived original GBIF Bombus 3,958,417 occurrence-source positive, >=5 observed one-degree grid cells reduces this to **113 source regions**, with 18 fine and 14 coarse blocks. No GBIF no-record regions are imputed as absence.
- Original regional mode coverage before region climatology eligibility: animal source regions with >=10 single-hue species = **290** and >=25 = **178**; wind source regions >=10 **166**, >=25 **28**, >=50 **0**. Thus even GIFT is temperate-biased in joint mode support (median 155-region source latitude ~40.9 degrees), and most wind sites have modest source representation. 25/25 strict both-mode support would leave only ~26 mostly European source regions.

Original source verified GitHub Actions:
- [Stage89A real GIFT×WCVP coverage #44430408416](https://github.com/zuizui0223/adaptive-gain/actions/runs/44430408416), derived-only artifact 14485554038 ZIP SHA256 26ffa12c78a583743735d89575b6b8d4c4066a01da5b2a7e54aea531915bb7a8.
- [Stage89B actual global controlled paired-mode spatial CI #44431399635](https://github.com/zuizui0223/adaptive-gain/actions/runs/44431399635), derived-only artifact 14486832021 ZIP SHA256 b51528d374c0e6b6710a266baa59aca6c2fcf402b9d4434a3be6e16bbb6dc826.
- Source WorldClim regional WCVP original derived artifact 14420920043 SHA256 4c0ab25596078be4b2aa35a254e42695fd260e1720864e173970aac8aa7db83a; source GBIF archive positive records derived artifact 14419407872 SHA256 2fe7510fe8c08189d63151fe255a00baafb96c7acc87d3d0fedc970966ca1a43. All four ZIPs original SHA-verified before model execution.

## Original spatial estimates from independent source-mode plant groupings

Source response is the regional fraction of exact single-colour NHM botanical prose among GIFT source-identified animal or wind species. Eleven hue families, two weighting rules (species pooling and genus-equal local means), and a within-*same*-region animal-minus-wind hue difference were evaluated. Original full 55,775 species are not treated as measured-hue negatives. Controls include WorldClim 1970–2000 wind, temperature, log rainfall, solar radiation, vapor pressure, mode-specific description coverage and source hue taxon counts, latitude/latitude squared, and longitude sin/cos. The 113 GBIF positive subset also adds observed Bombus richness, original recorded GBIF 1-degree cells as incomplete recording effort proxy, and wind×recorded richness. Standardized slopes are fractions per 1 standardized predictor difference. HC3 and 11-hue BH tests are exploratory; primary uncertainty is 999 paired geography block bootstrap resamples at two spatial scales.

**Global wind and source colour composition in 155 common-mode regions:**

| Source original GIFT mode / colour | genus-balanced wind partial beta | 20x45 geography block 95% | 30x60 geography block 95% |
| --- | ---: | --- | --- |
| Wind-mediated species: green word fraction | **-0.02413** | [-0.03932, -0.00601] | [-0.03733, -0.00495] |
| Wind-mediated species: brown word fraction | **+0.02370** | [+0.00616, +0.03757] | [+0.00131, +0.03320] |
| Animal-mediated species: green word fraction | +0.00222 | [-0.00153,+0.00810] | [-0.00249,+0.00662] |
| Animal-mediated species: brown word fraction | +0.00077 | [-0.00139,+0.00332] | [-0.00222,+0.00362] |
| Animal minus wind: green word fraction | **+0.02635** | [+0.00649,+0.04431] | [+0.00596,+0.04104] |
| Animal minus wind: brown word fraction | **-0.02293** | [-0.03674,-0.00560] | [-0.03318,-0.00113] |

The wind-source flora is dominated by reported GREEN and BROWN single hue words: mean genus-balanced shares ~25.89% green and ~42.02% brown, versus ~3.86% and ~0.42% for animal-source flora. Among the same 155 native regions, green and brown fractions of wind-mode plants are strongly NEGATIVELY correlated (Pearson r≈-0.727), so these two coefficients can reflect **the same compositional tradeoff**, not two independent pollinator information signals. Wind-mode proportion in native regional flora does not prove these are locally in-flower or wind-pollinating at the date of the climatology. High wind may covary with source regional vegetation type, range coverage, habitat and plant family even after the listed climate/lat-lon controls. No evolutionary selection mechanism inferred.

**Bombus-record positive sample 113 regions, GIFT "animal"-mode plants:**

| Ecological source association | genus-balanced beta | geography block 20x45 95% | 30x60 95% |
| --- | ---: | --- | --- |
| Yellow flower word fraction vs recorded Bombus richness | +0.02352 | [-0.00948,+0.04296] | [-0.02742,+0.04733] |
| Purple flower word fraction vs recorded Bombus richness | -0.01547 | [-0.02363,+0.00208] | [-0.02375,+0.01034] |

Neither interval excludes zero, despite the base 139-region all-flora Stage87 positive yellow geographic pattern. **Thus the previous all-flora hue–Bombus spatial correspondence is not demonstrated to generalize to the independently classified animal-pollinated subset** at this source/region support. GIFT "animal" includes nonbee insects, birds and other animals; the source guild measured in GIFT is not a documented Bombus preference.

A tentative negative animal-mode PURPLE word × wind × recorded Bombus richness term arises (beta -0.00920; exploratory 11-hue q≈0.013; fine 20x45 interval -0.01687,-0.00231), but the coarse 30x60 geography interval [-0.01573,+0.00043] crosses zero, so NO general causal sensory cue-order claim is supported. The same source family in the within-mode contrast has similar coarse spatial failure. Original beetle/bee observations, true field-level source flower colour, original regional plant abundance, actual wind-at-bee-visit, fragrance plume, insect learned recognition and landing success are missing.

### Source negative support is NOT biological absence

Wind-mediated source taxa have NO explicit blue, pink, red, orange or grey NHM single-colour word records in the included source regions. They may exist in nature; the source subset has no supporting prose records. Stage89B marks **40 slope rows NOT_IDENTIFIABLE_NO_HUE_VARIATION**, and only **224** of the full 264 descriptive combinations are estimable. We do not fit zero-effect models or treat missing hue mentions as verified biological negative. No p-value corrected for previous hypothesis searches, phylogenetic repeated species, and selection of source databases.

## Advance/stop scientific decisions

1. Genuine GLOBAL presence and taxon compatibility: PASS for 3,172 accepted mode-qualified source species.
2. Same-region animal-vs-wind botanical hue geographic contrast: PASS descriptive, 155 regions with two kinds of source plant coloration and two-scale geography blocks.
3. Animal-vs-wind mode-specific effect interpreted as evolutionary selection by wind or Bombus: NO-GO; modes and floral colours are separate trait sources attached by species, not matched field visits or phylogenetic repeated transitions.
4. GIFT "animal" colour vs archived 3.96M GBIF Bombus richness: YES data support in 113 regions, but colour preference or sign-stable regression NOT established.
5. Source-confirmed sensory information acquisition order, cognitive learning cost, wind-disturbed perfume plume, flower aerodynamics, landing or plant fitness: UNIDENTIFIED.
6. Before any stronger causal evolutionary claim, require independent source region/abundance, mode-specific local surveys, verified source phylogeny and independent transitions, GBIF target-group effort and measured plant/insect behavior in the same wind/plume/flower stage.

Repro code: research/floral_macro_stage89/gift32_independent_pollen_mode_global_native_coverage.py and compare_gift_animal_wind_hue_geographic_regimes.py; tests and GitHub source workflows in .github/workflows. All original-source-derived receipts are archived, not original NHM/WCVP bulk files, raw GBIF 3.96M records or GIFT raw source responses. Stage89 remains draft stacked on Stage88. Main unchanged.


## Stage89C: genuinely source-authenticated independent database label-concordance audit

We re-downloaded original AusTraits v7.0.0 official 21,100,078-byte author ZIP, SHA256 2995fb9e5eebf9271f9241b5a6c2e2cbb7b45e8eda5ce4db43c14c68f95e2f3f (1,798,215 author trait rows, 13,440 original pollination_syndrome source rows, 4,619 valid strict insect-only/wind-only species). These original species labels were compared to the separately original-source-verified GIFT v3.2 5,770 valid species labels, using ONLY exact names without automatic synonym inference, after excluding ambiguous or mixed reports.

Source-verified GitHub Actions [#44432262460](https://github.com/zuizui0223/adaptive-gain/actions/runs/44432262460) **SUCCESS**, derived-only artifact **14487207856**, ZIP SHA256 c721a31b2b0eb01a8132febc1e544f10fe0f70f46480c9e1fce01132ba1bce0b.

**Only 225 species in 144 genera** have qualified direct pollination categories in both external databases:
- GIFT biotic & AusTraits insect: **171 species**
- GIFT wind & AusTraits wind: **52 species**
- GIFT biotic & AusTraits wind: **1 species**
- GIFT wind & AusTraits insect: **1 species**

Thus the selected overlapping labelled species agree **223/225 = 99.11%**, with descriptive Cohen kappa **0.9753** and a genus-reclustered bootstrap agreement interval **[0.97685, 1.000]**. The two actual mismatched species are *Coprosma perpusilla* (GIFT wind; AusTraits source White_2020 insect) and *Glochidion philippicum* (GIFT biotic; AusTraits source Metcalfe_2009 wind). This is a **source-database label agreement** on 225 nonrandom taxa, NOT a demonstration that GIFT and AusTraits were independently measured in different field studies, not a phylogenetically independent test, nor an external validation of all 3,172 GIFT/WCVP native species. Both databases can cite overlapping original literature and share inherited taxonomic conservatism.

The scientifically supported statement: the 225 shared source-coded species rarely contradict on these two broad pollination categories, but neither confirms the species-mode population field identity nor resolves the wind/odor/visual-learning mechanism.

Source-validated implementation: research/floral_macro_stage89/crosscheck_GIFT_AusTraits_original_pollination_modes.py and its tests; workflow .github/workflows/floral-stage89C-GIFT32-AusTraits7-source-mode-concordance.yml. Stage89A/B/C all have their own independent actual-source Actions runs and their results are documented here. Main unchanged.
