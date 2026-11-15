# Stage34 — Does wind benefit scented flowers more than scent-suppressed flowers?

**2026-11-15. Precise HYPOTHESIS/EXPERIMENTAL ESTIMAND and source-free model counterexamples. Not an observed wind×scent ecological effect.** Stacked on Stage33 PR #112; main and prior stage results unchanged.

## Correct question: relative interaction, not a universal scent-positive outcome

The biologically useful prediction is:

**The wind effect on initial discovery may be greater for flowers emitting detectable, attractive VOCs than for experimentally scent-suppressed but otherwise matched flowers.** This prediction does NOT imply higher absolute net pollen transfer under wind, and is not universal across odor bouquets, wind speeds, light, floral display and pollinator species.

Not all flowers in a species share emission rate. Human-odorless does not equal no insect-detectable VOC. A volatile might repel pollinators, attract antagonists, or deliver spatial reward information only after probing. Neither VOC richness nor total emission necessarily predicts detection at the receiver antenna after advective dilution. Original emissions (ng / flower / hour or verified source units), blend composition, measured plume, distance, wind direction and intermittency are preferable to a simple "scent yes/no" species category.

## Required 2×2 randomized experiment

Randomly cross **flower odor ON versus odor suppressed with matched sham**, and **measured low versus high wind**, holding flower/display number, floral color, UV/reflectance, reward concentration, handling geometry, and plant age constant as far as the treatment design allows. Insects should be sampled independently by original individual and colony/site. Wind must be characterized at actual flower height and scent-tracking distance (speed, direction, gust/turbulence and flower sway), not replaced by general weather-station airspeed.

Keep original denominators and distinct stages:
1. Flower patch detected among surveyed available patches, true search effort and detection distance.
2. Plant/flower approach given discovery.
3. Landing success given approach, plus flower oscillation and receiver flight control.
4. Legitimate flower entry/pollen deposition per original landing, and ultimately plant seeds/siring (not inferred from visits).
5. Same individuals' actual scent preference, detection threshold, learned visual cue usage and motor-flight performance, without "Bombus = cognitively high, flies = random" imputations.

For a given original source opportunity, denote discovery D, landing conditional on discovery L, and deposited-pollen success conditional on landing T. Success probability V=D*L*T. For fixed combinations (w,s) in {calm,wind}×{odor off,odor on}, define the **discovery-scale** interaction:

    I_detection =
      [D(wind,odor on)-D(calm,odor on)]
      -
      [D(wind,odor off)-D(calm,odor off)].

The **actual-plant transfer** interaction differs:

    I_transfer =
      [V(wind,odor on)-V(calm,odor on)]
      -
      [V(wind,odor off)-V(calm,odor off)].

Pseudoreplication, repeated bee visits, weather/site/flower variation and missing recorded attempts all change the sampling variance and identification of an experimental effect. Code here is **exact math for ASSUMED probabilities**, not an estimator from actual randomized counts.

### Constructed counterexample — positive interaction, yet harmful wind for BOTH scent groups

Set all conditional deposition probabilities T=.75, and these entirely HYPOTHETICAL source-free numbers:

| Wind | Scent | D | L | V=D*L*T |
|---|---|---:|---:|---:|
| Calm | OFF | .30 | .80 | .1800 |
| Wind | OFF | .30 | .50 | .1125 |
| Calm | ON | .40 | .80 | .2400 |
| Wind | ON | .60 | .50 | .2250 |

This gives I_detection=+0.20, but net wind change with scent ON =−.015, with scent OFF =−.0675, and I_transfer=+.0525. **The scented plant is less harmed by wind, not benefited by wind in absolute terms.** Other constructed cells can make I_detection positive but I_transfer negative, particularly with scent-dependent landing penalties or florivore responses.

What looks like a positive cue×wind interaction in a distant-arrival outcome does not determine the direction of the plant's actual fitness response.

## Relevant real evidence, without false empirical factorial claims

- Crall et al. 2020 (Biology Letters, DOI 10.1098/rsbl.2020.0103) observed more visits to **artificial fragrance bait stations** by male orchid bees under temporally greater wind/turbulence within sites. This study does NOT independently randomize a no-odor station crossed with wind regimes or document direct stigma pollen deposition. The authors explicitly say evidence across pollinator species and broader wind ranges remains needed.
- Haverkamp et al. 2016 (eLife, DOI 10.7554/eLife.15039) compared flowers with an emitted benzylacetone volatile versus nonemitting flowers; hawkmoths showed comparable flower visits and approaches, yet emitting flowers received better pollination services and higher seed production. Their wind tunnel is not a fully randomized calm/windy×scent 2×2. It is a strong warning against equating attraction with transfer or scent emission with always greater flight approaches.
- Scent matters (Annals of Botany, DOI 10.1093/aob/mcy131): 11 Thalictrum species with transitions between insect and WIND POLLINATION modes had different emitted VOC and bumblebee antennal responses. Here "wind pollinated" is **pollen transport mode**, NOT a randomized windspeed exposure. Pooling the two meanings of wind would be a categorical error.
- Petunia scented versus near scentless genotypes (Current Biology, DOI 10.1016/j.cub.2011.03.059): reciprocal scent-QTL introgressions showed short-distance hawkmoth scent preference but scent and color can offset each other. Do not attribute all flower-visitation change to scent while genotype/color covary.
- The Stage33 source ledger has wind-scent bait observations and wind/landing experiments, but **they are independent source experiments** and cannot be combined algebraically as if the same 2×2 randomized population was observed.

## Distinguishing discovery effects from real plant selection

A useful hierarchical meta-analysis should have stage-specific effect families:

- Wind×scent on odor-source discovery / arrival (known search opportunities, wind and verified VOC treatment).
- Wind×scent on landing (same original encounters with tracking and failure denominator).
- Wind×scent on legitimate stigma pollen deposition and independently quantified plant fruit/seed output.
- Wind×scent×receiver discrimination or flight control, with **measured**, not taxonomically assigned, cognitive moderator.

Wind also changes volatile blend, background plant odors, flower motion, insect activity/abundance and pollen transport itself. Stronger scent can attract nectar robbers/herbivores. Site-matched scent on/off factorial experiments and measured costs are necessary before any ecological claim.

**Evidence state:** The original published sources presently provide separate pieces of the mechanism. We have NOT located, extracted or fitted one all-four-cell original wind×floral-scent field experiment. No pooled wind×scent effect or universal "fragrant flowers benefit more from wind" claim is established. Keep it as a pre-registered prediction, not a positive result.
