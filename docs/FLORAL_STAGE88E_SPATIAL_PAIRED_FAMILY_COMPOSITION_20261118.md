# Stage88E | Fixed-geography, paired spatial block test of anemophily-enriched families

2026-11-18 JST. Complete independent local numerical re-run on original SHA-verified source-derived ZIPs; GitHub Actions source re-run is in progress. **This tests a phylogenetic/taxonomic composition confound, NOT individual-source animal versus wind pollination mode.**

## Exact tested estimand and denominators

The initial Stage87 spatial comparison had 274 worldwide TDWG Level3 native-flora regions with 50+ explicitly single-lexical-hue NHM source species, complete long-term WorldClim five-variable coverage, no source TDWG polygon repaired geometry; independently positive GBIF Bombus records in 139 of these regions. Excluding three source graminoid families, Poaceae, Cyperaceae and Juncaceae, leaves 50,754/55,775 distinct source WCVP plants globally; excluding those plus nine further source families with many wind-pollinated taxa leaves 49,161 native species. Family lists are frozen by code; a family label is **not** evidence that all its member plants are wind-pollinated.

To avoid spurious coefficient differences caused by the selection of different regions after taxon removal, the Stage88E *primary* model retains only the **identical 268** original regions with ≥50 source-hue taxa under all 3 original family scopes, and the **identical 138** of those with observed 5+ distinct GBIF occupied 1-degree cells and positive Bombus richness. Covariates (wind, temperature, precipitation, solar radiation, vapor pressure, geographic latitude/longitude terms, source description fraction, log source hue flora count; plus Bombus observed richness and recorded grid effort, and wind×observed richness in the 138 positive subset) are standardized and **frozen at the initial all-native-flora definition**. Only the source native botanical colour **response composition** changes, making source family removal a paired contrast. A second sensitivity updates description fraction/count controls under each family exclusion.

Global real observational response: 11 NHM lexical visible flower hues, mean of original genus-specific documented one-hue fractions and alternative original species-pooled composition. Input phylogenetic repetitions and region source-description bias are NOT removed by genus balancing.

## Recomputed actual source coefficients (original genus-balanced hue fractions)

Source effect numbers represent absolute proportions per 1 standardized source predictor; for example 0.005 = 0.5 percentage points. The terms are **descriptive partial slopes**, not floral physiological sensory-receptor effects.

| Source geography / term | All native original plants | Exclude 3 graminoid families | Exclude 12 mostly wind-associated families |
| --- | ---: | ---: | ---: |
| Global 268 regions, wind → reported brown hue | **+0.003997** | **−0.000901** | **−0.000905** |
| Global 268 regions, wind → reported green hue | **+0.005829** | **+0.005530** | **+0.005136** |
| GBIF-positive 138 regions, log recorded Bombus richness → reported yellow hue | **+0.022350** | **+0.022669** | **+0.021548** |
| GBIF-positive 138 regions, log recorded Bombus richness → reported purple hue | **−0.012215** | **−0.013100** | **−0.013597** |

All changes are evaluated in the **same original geographic sample**. A genus-mean is not an independent reconstructed phylogenetic comparative method. The botanical prose lacks strong coverage for morphological style, pollination mode, UV nectar guides, fragrance or bee perceptual contrast.

## Direct paired spatial uncertainty — bootstrap actual regions by geographic blocks

In the same-source global 268 regions, 20° latitude×45° longitude yields **36** spatial resampling blocks, 30°×60° yields **25**. For the actual 138 recorded-bee positive regions these have **23** and **16** blocks, respectively. The independent source code re-estimates *both* all-native and family-exclusion coefficients under the **same 999 resampled spatial blocks**, so the difference interval is paired rather than inferred from overlap of two separate intervals.

- **Brown and wind**: after exclusion of three graminoid families, difference in adjusted partial coefficient is **−0.004898**, with 20×45° paired block 95% interval **[−0.00775, −0.00203]**; at coarser 30×60°, **[−0.00890, −0.00187]**. Thus the taxonomic family mixture materially contributes to the original positive source climate–colour correspondence. The excluded cohort's *own* brown wind coefficient has a 20×45° interval **[−0.00237, +0.00103]** and is not separately distinguishable from zero.
- Excluding all twelve families yields brown-wind coefficient −0.000905 with paired all-minus-filter difference **−0.004902**; 20×45° **[−0.00793, −0.00194]**, 30×60° **[−0.00897, −0.00169]**.
- **Green and wind**: after three family exclusions, +0.005530 with 20×45° 95% interval **[+0.00269, +0.00906]**. The *change* from all-native is only −0.000299 with paired 20×45° interval **[−0.00135, +0.00071]**. Even after twelve excluded families, +0.005136 and paired difference interval crosses zero. The green positive geographic association remains and is not specifically explained by the selected families.
- **Yellow and recorded Bombus species richness**: after three-family exclusions, +0.022669 with 20×45° interval **[+0.00946,+0.03182]**; after twelve +0.021548 with 20×45° **[+0.00829,+0.03097]**. Neither *paired coefficient change* differs consistently from zero. This association survives *these* taxonomic composition checks; it is not identified as plant–bee mutualistic choice or hue selection, especially because original archived Bombus richness correlates with recorded coverage.
- **Purple and recorded Bombus richness** remains negative in all three, with 20×45° intervals under zero. This does not establish bees' dislike of purple: these are source native species assemblages, not observed flower-level visit preference.

The local numerical run validated original SHA256 for all three ZIP inputs, 264 source comparison rows, all **999/999 valid resamples** per geographic block resolution and scope. Source-matched code is committed to GitHub and GitHub Actions is configured to independently rerun and check the sign of the paired brown effect. Source DOI-level and phylogenetic evolutionary independence are NOT yet established.

## Why this narrows the scientific claim

The main Stage87 all-species wind → brown hue signal is **confounded by native flora composition**: a minimal phylogenetic-family exclusion kills its apparent positive direction and a paired geographic bootstrap confirms the effect change. In contrast, green wind and yellow/purple recorded-bumblebee geography cannot be dismissed on that particular group of twelve families alone. They remain *spatial co-occurrence hypotheses* subject to non-independent species native ranges, genus and functional trait content, background climate, habitat, latitude, floristic reporting, GBIF receiver ascertainment.

The independent 2025 Wang et al source dataset (Dryad DOI 10.5061/dryad.73n5tb35w; published 179,263 animal/wind labels) has original title, version and file SHA verified. However actual anonymous Dryad data download returned **HTTP 401**, and the separately identified official Wiley supporting Rdata URL returned **HTTP 403**. No source species-mode rows have been recovered from that archive, so Stage88C must remain unexecuted rather than invent 179,263 mode assignments. An independent AusTraits v7 explicit insect/wind syndrome dataset has been source-verified previously in a separate repository; its global WCVP overlap and geographic coverage are being independently audited as a narrower positive-only backup, not an automatic replacement of the original 179,263 database.

**No source currently joins actual wind-at-flower, turbulent scent plume, the order of cue acquisition, bee learning, landing probability or plant fitness.** The exact theorem about deterministic adaptive access does not prove a noisy bee chooses a particular flower cue. A robust global taxonomic association cannot by itself prove any of these mechanisms.

## Reproduction

- Input source original family exlusions: Stage88D GitHub Artifact 14426246428, ZIP SHA256 4451986d53f653cb96966d0595765d2c7806fb81057177be65ccfb3d2519e7d2.
- Stage87C global original region climate: Artifact 14420920043, ZIP SHA256 4c0ab25596078be4b2aa35a254e42695fd260e1720864e173970aac8aa7db83a.
- Stage87D GBIF 3,958,417 original observations: Artifact 14419407872, ZIP SHA256 2fe7510fe8c08189d63151fe255a00baafb96c7acc87d3d0fedc970966ca1a43.
- Code: research/floral_macro_stage88/source_paired_global_family_spatial_ablation.py; CI: .github/workflows/floral-stage88E-global-family-geoblock-paired.yml.
- No original restricted bulk author sources redistributed.
