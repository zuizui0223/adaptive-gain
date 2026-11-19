# Stage90 | Global floral wind–hue correspondence: species range recurrence, genus common support and wind-family leaveout

2026-11-19 JST. Source-proofed Stage90A, Stage90B and Stage90C all **SUCCESS**, independent original-source full-retrieval provenance in GitHub Actions. This document reports an ecological spatial *description/identification boundary*, not a model of adaptive floral cue-order acquisition or wind-selected bee attraction.

## Main discovery

The preceding Stage87–89 program finally matched large original source botanical floras (NHM 59,369 prose entries, WCVP 55,775 strict native species × 367 TDWG regions), actual WorldClim source wind/temperature/precipitation/solar/vapour climate and 3,958,417 archived GBIF Bombus positive records to independently literature-qualified GIFT 3.2 pollen-mode species (2,560 biotic, 612 wind). Stage89B reported a wind-mode green-vs-brown hue spatial gradient across **155 common-animal/wind-hue native floristic regions**, with **113 independently GBIF-positive** regions.

**The pseudo-replication problem:** The 612 wind-labelled species include only **57 original NHM explicitly one-hue species in 38 genera**. Those species recur across a median of **56 native TDWG3 regions per source species**, compared with the **598** source one-hue animal-mediated plant species in 373 genera repeating across a median of 24 regions. Native-region incidence is not an independently evolved floral hue origin. The 155 region models therefore have much smaller independent source colour/lineage support than the apparent region sample size implies.

**The common-ancestry comparison problem:** Among **3,172** mode-qualified native species globally, source GIFT includes **13 genera** with both animal- and wind-pollination labels; but only **two genera, *Artemisia* and *Plantago*, have an explicit NHM one-hue floral description from BOTH modes**. Only 54 of 367 original region keys even contain both colour-documented pollen modes within a botanical genus, often recurring taxa across regions. Genus overlap is NOT a known count of independent evolutionary mode transitions, nor a dated clade phylogeny. No credible across-phylogeny effect estimate is identified by 155 region-level regressions.

## Stage90A: real source taxon repetition audit

Actual [GitHub source CI #44447111097](https://github.com/zuizui0223/adaptive-gain/actions/runs/44447111097) SUCCESS, derived artifact **14493253828**, ZIP SHA256 **523c0369483af34f702157021066174ed503c77c322fb1fa3ca88dcc2dbbe2fa**.

Original author verified assets: GIFT 3.2 original full public API acquisition in island H5c run 34803493307 (source artifact SHA256 074a52323ba835201043a3a5980cc2b2d0ff79878e83bc9be19511ae83a1c0e8), NHM botanical source CSV SHA256 b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a, Kew original WCVP ZIP SHA256 d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa, and prior Stage89 original 367×3 region data artifact SHA256 26ffa12c78a583743735d89575b6b8d4c4066a01da5b2a7e54aea531915bb7a8. The actual **367×3 prior unweighted original source regional colour fractions were numerically recomputed and checked** against the prior Stage89 source, not trusted without a regression check.

| Stage90A source metric | Biotic animal-mode | Wind-mode |
| --- | ---: | ---: |
| Qualified source-native species with mode label | 2,560 | 612 |
| Source species with actual explicit one-hue original botanical text | **598** | **57** |
| Unique genera with an explicit one-hue species | 373 | 38 |
| Median native TDWG3 range breadth of one-hue species | 24 regions | **56 regions** |
| One-hue species native in >=10 TDWG3 regions | 452 | 53 |
| Total original regional source one-hue species×region appearances | 16,382 | 3,688 |

Mode contrast genus support (with no strict genomic phylogeny): **13 genera have both literature-reported modes in the 3,172 source species**, only *Artemisia* and *Plantago* have a source one-hue species on both sides. Exact region-genus same-mode overlap is a necessary but not sufficient condition for an independently replicated evolutionary mode transition. The absence of source hue in another genus means UNKNOWN, never a measured absence.

In the original **155** common-region mode-hue cohort, source wind-mode flora contains a median **15** explicit one-hue species/region, median **11 genera**, and after inverse native-range weighting a median equivalent **10.62 effective native-source species**/region (not the effective number of independent ancestral transitions). The most frequent original top family by wind hue plant numbers is Cyperaceae in **120/155** regions, Poaceae in **31/155**, Juncaceae in 2 and Amaranthaceae in 2. This is an enormous source family concentration that cannot be fixed by spatially blocked p-values.

## Stage90B: paired range-breadth weighting / geographical bootstrap

Actual [source-locked GitHub Actions #44448207801](https://github.com/zuizui0223/adaptive-gain/actions/runs/44448207801) SUCCESS; derived artifact **14494940518**, ZIP SHA256 **a6ef1ae7f3a68f6719b7201961af08ab66a4bff73fa185fc8c488f13b6a45fc3**. A previous source-locked #44447447497 successful run produced the same continuous coefficients but had an ambiguity in how positivity was summarized for signed within-region contrasts. The new artifact corrects that receipt classification without changing any estimates.

Every species' contribution to a region's original source one-hue flora is reweighted by **1 / (number of WCVP native TDWG3 regions for that exact accepted species)**. The new hue fraction is a weighted sum among documented source hue species, again with a separately genus-equal version. No source wind vs animal labels are imputed. The model uses the same original 155 (global) / 113 (GBIF-positive) regions, identical WorldClim/plant textual source coverages/latitude/longitude/GBIF recorded-cell covariates, and the **same 999 geographically blocked resamples** for each source *unweighted–reweighted* pair at both 20×45 and 30×60 degree spatial block scales. There are 264 fully enumerated original response–predictor contrasts, of which 40 from wind-mode hues without original positive lexical documentation are marked not estimable (rather than estimated as zero effects).

| Same-region source comparison, genus-balanced hue fractions | Original slope | Inverse species native-range slope | Range-weighted 30×60 block 95% |
| --- | ---: | ---: | --- |
| 155 regions: wind speed vs WIND-mode original GREEN-hue share | −0.024131 | **−0.026453** | [−0.03979,−0.00522] |
| 155 regions: wind speed vs WIND-mode original BROWN-hue share | +0.023701 | **+0.027148** | [+0.00127,+0.03841] |
| 113 GBIF-positive regions: recorded Bombus richness vs animal-mode YELLOW-hue share | +0.023521 | +0.023576 | [−0.03057,+0.04791] |

Original wind hue green/brown signs persist after inverse source native-range reweighting, and the **paired change** intervals for wind-mode green and brown include zero at coarse spatial block scale. This only shows the associations are not *solely* an artifact of WCVP range breadth frequencies. It does not yield independent source genus/classic PGLS/phylogenetic mode transitions. In the 113 GBIF-positive region subset there is still no stable source animal-yellow response to *recorded* Bombus richness under coarse geography resampling. The climate used was 1970–2000 regional mean wind; the Bombus presence data 1950–2025 are source opportunistic archive occurrences, not unbiased native receiver availability.

## Stage90C: direct original wind-hue taxonomic source-support falsification

Actual [GitHub original-source Stage90C Actions #44448207898](https://github.com/zuizui0223/adaptive-gain/actions/runs/44448207898) SUCCESS; derived artifact **14493782612**, ZIP SHA256 **9c4f809aeca477287c1f6e1b89a1dfbf88bd39df32c154e7a855789f573d646b**.

We independently retained only source-verified GIFT wind-labelled native botanical species with source documented exactly one hue, and used original Kew source accepted families to predeclare removal of **Poaceae, Cyperaceae, Juncaceae** as source-lineage quality sensitivity. An excluded family is **not** an intervention setting every one of its species to wind-mode; the pollination-mode label is sourced independently from GIFT.

### True 57 source wind-mode one-hue species by Kew family

- **Cyperaceae 18** (13 brown-hue reported), **Poaceae 14** (2 brown), **Juncaceae 8** (4 brown): three graminoid families contribute **40/57 original wind one-hue species (70.2%)**.
- Wind brown-hue source species: 20; **19/20 (95%)** from those three families (the other is one Typhaceae source species). Thus the source word "brown" is nearly entirely a graminoid syndrome marker in the qualifying wind-mode subset.
- Remaining 17 source wind one-hue species span 10 other families / 14 genera. Some are animal-pollinated within their family or uncertain locally; source GIFT mode assignments are literature classifications not observed flower-local pollen vectors.

### How many regions retain enough independent source plants?

| Removed family/lineage | Source wind one-hue species still present globally | Of 155 original global comparison regions, how many retain at least 10 wind source one-hue taxa |
| --- | ---: | ---: |
| None | 57 | **155** |
| Cyperaceae only | 39 | **64** |
| Poaceae only | 43 | **121** |
| Juncaceae only | 49 | **121** |
| All 3 graminoid families | **17** | **0** |
| These 3 + 9 additional wind-enriched families | **12** | **0** |

More strongly, after excluding the three families there is **zero of the entire 367 source native TDWG3 regions** with >=10 original documented one-hue wind plants. The maximum remaining regional colour-documentation count is only eight. This is a source-data **NO-GO** for generalizing the previously positive wind-mode brown/green regional slopes to other plant phylogenetic families. It is not a biological null effect of wind on non-graminoid wind-pollinated flowers.

## Scientific conclusion and next source bottleneck

The original global flower-text/hue×wind correspondence from Stage87 was strongly confounded by wind mode and floristic lineage. Stage88E independently showed all-flora wind–brown beta +0.003997 drops to −0.000901 after graminoid families are removed (within original 268 regions, fine paired geographic 95% difference −0.00775,−0.00203). Stage89B source-independent GIFT mode confirmed brown/green wind-mode floristic geographic gradients in 155 regions; Stage90B shows its direction survives correcting for repeated range breadth. But Stage90C proves **the actual independent source wind floral-colour support is 57 species in 38 genera, concentrated in three graminoid families, and collapses completely outside those lineages at fixed 10-one-hue regional eligibility**. There is no defensible full-angiosperm *evolutionary* generalization about flower cue function from this source.

The GIFT and AusTraits two-mode label panel agrees in 223/225 overlapping original strict species, but they can share source publications. The Stage90A data have only **two genuine genera with different source modes and flower colour documentation**, not sufficient repeated within-clade mode contrasts. Thus the *phylogenetic effect of pollination mode per se* is not identifiable from this data.

**Empirically supported:** global geographic association with reported botanical flower colours, global wind climate and GIFT source pollen-vector categories. 
**Not supported:** far vs near stage cue ordering, flower-level ecological reward, flower-specific gust/plume, documented bee learning, actual landing choice, plant fecundity, independently repeated evolution, or yellow flower preference by Bombus. The conditional wind×bee sensory-order effect remains NO-GO.

Next valid comparative input: a large independently versioned angiosperm pollen-vector mode source (e.g., Wang et al. 2025 author Dryad 179,263 species but its anonymous original download currently returns HTTP 401, publisher Dataset S2 HTTP 403) PLUS independently source-confirmed flower-colour traits *outside* Cyperaceae/Poaceae/Juncaceae; or directly acquired local plant taxa and pollinator survey effort across independently sampled native sites. Until true phylogeny/source-transitions and independent non-Bombus target-group GBIF sampling effort are obtained, no causal floral signaling manuscript conclusion can be promoted.

## Code, scientific provenance, no bulk source redistribution

- Stage90A source: research/floral_macro_stage90/authentic_GIFT_native_range_breadth_and_genus_support.py
- Stage90B source: research/floral_macro_stage90/source_reweighted_GIFT_hue_wind_Bombus_spatial_pairs.py
- Stage90C source: research/floral_macro_stage90/original_wind_mode_floral_family_lineage_leaveout.py
- All three contain separate source-free guards and original GitHub Actions pipelines in .github/workflows.
- Author raw NHM text, Kew WCVP bulk accepted taxonomy, GIFT original API long table, original GBIF 3.96M archive and WorldClim GeoTIFF originals are NOT redistributed in these derived-only source receipts.
- All PR changes are Draft on the stacked Stage89 source branch; default main unchanged.
