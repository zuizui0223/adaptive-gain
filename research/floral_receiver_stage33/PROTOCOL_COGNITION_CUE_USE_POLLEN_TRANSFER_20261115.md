# Stage33 — Receiver-specific use of floral information versus true pollination effectiveness

2026-11-15 | A SOURCE-BACKED COMPARATIVE DESIGN plus exact source-free counterexamples, not an empirical cognition-efficiency meta-analysis. Branch stacked on Stage32. No past observational raw data or manuscripts modified.

## Main scientific decision

The critical contrast is **NOT "intelligent bumblebee vs random fly"**. It is between several independently measured behavioral and functional traits:

1. Whether the pollinator *perceives* the scent, display, color, nectar guide, UV or tactile marking in a given environment.
2. How reliably it discriminates reward classes and learns/remembers a cue's mapping, with within-animal source trials.
3. Whether it actually *uses* the cue to choose a plant, land at the right entrance, orient, or persist, rather than relying on innate preference, exploration, chance or other cues.
4. Its energetic/time cost of cognitive processing, flight or handling, measured independently rather than imputed from species identity or brain size.
5. Its physical/mechanical per-visit pollen removal, stigma contact, deposition and eventual plant siring/seed set. These can differ in sign and magnitude from nectar foraging reward.

The guild identity and sociality are candidate moderators, NEVER substitutes for measured sensory/cognitive learning speed or pollen-transfer rate. In particular, a nonselective-looking trajectory can be optimal exploratory sampling when current flowers are unreliable; a slow learner can have strong innate sensory bias or high mechanical pollen transfer. Not visiting a guide does not prove no sensory recognition.

### Direct empirical prior art

Kandori et al. 2021 (Ecological Research; DOI 10.1111/1440-1703.12249) experimentally compared color-reward learning in eight species: eusocial *Bombus ignitus*; solitary *Osmia orientalis*; two hoverflies *Eristalis cerealis* and *E. tenax*; and the butterflies *Idea leuconoe*, *Argyreus hyperbius*, *Pieris rapae* and *Lycaena phlaeas*. All eight learned. In their task B. ignitus was the fastest learner, followed by the larger butterflies, then smaller butterflies, with hoverflies and Osmia in a slower group. The design reuses four butterfly studies: eight taxa are **not eight independent article replicates**. No original eight-species learning coefficient, standard error, behavior×pollen transfer pair or independently replicated colony-plant pairing has been extracted in Stage33.

Dukas and Real (1991, DOI 10.1016/S0003-3472(05)80558-5) found social bumblebees faster learners than a carpenter bee in three tasks, but overnight memory retention similar: learning speed and retention are distinct traits.

Haverkamp et al. (2016, DOI 10.1038/ncomms11644) found naïve hawkmoths use innate olfactory cues matching flower/proboscis morphology; this is a counterexample to labeling non-bees as random or cognitively unresponsive. Cepero et al. (2015, DOI 10.1007/s10905-015-9519-z) found monarch butterflies learn flower color more readily than shape, yet also can learn shape.

Page et al. (2021, DOI 10.1002/ajb2.1764) synthesized single-visit pollination effectiveness from 168 studies, 1,564 measures and 240 plants. Honeybee effectiveness varied and was often below the most effective non-honeybee pollinator. That SVE dataset does not estimate the same individuals' Kandori learning rates, and a taxon name join between these independent meta sources does not identify a cognitive effect on pollination. Plant morphology and visitor anatomy, task context, visitation frequency, floral constancy and sampling effort all matter.

Recent flower constancy research (2025, DOI 10.1111/1365-2435.70008) and earlier cognitive ecology syntheses already examine learning and memory costs. Those concepts are PRIOR ART, not a novel theory invented in Stage33.

## Stage × modality × receiver design

Experimental signal contrasts must be original independent manipulations whenever possible:
- distant: display area/flower count × odor plume delivery × visual background and wind, with patch detection opportunity denominator;
- approach/landing: color, UV, guide or scent spatial arrangement × experience, with true landings, trajectory, and legitimate-vs-robbing route;
- within-flower: guide, floral geometry, odor gradient, tactile/temperature pattern × probing time, opening discovery, pollen-contact;
- reward/choice: fresh/depleted and old/young flower state × learning trials to criterion, memory retention and flower constancy;
- plant consequences: pollen removal/deposition and seed production after verified visits, separately for each original plant and pollinator.

For EACH receiver species/individual, annotate actual stimulus contrast, innate preference baseline, after-training discrimination or cue-use frequency, sensory noise/light/wind, number of learning exposures, associative memory, distance/motor cost, handling speed, body–flower compatibility and original independent plant/pollinator IDs. Avoid labeling "guild random" for missing behavioral data: mark UNKNOWN and distinguish experimentally randomized policy, untrained novelty-seeking, and measured low cue-discrimination.

### Statistical analysis planned (not fit)

A. **Perceptual/learning meta-analysis**: within-study original tasks with learning-curve coefficients and sampling uncertainty, or trial-level response models with random insect identity. Compare species/order/sociality only after matching color, contrast, stimulus reward and number of exposures. A published qualitative ordering is not an individual numeric effect.

B. **Behavioral signal-route meta-analysis**: stage-specific randomized contrasts in detection, approach, flower choice, landing, legitimate probing and handling time. Fit signal modality × stage × measured cue-use/experience × signal reliability × wind/visual background × floral geometry, with correlated effects by study, original animal, flower, array and date. Binary and time effects stay separate.

C. **Pollen transfer meta-analysis**: per-visit pollen deposition, reproductive fruit/seed or siring conditional on original plant and visitor. Mechanistic moderators include actual route use and body fit; high learning capacity alone does not imply efficient deposition. Use the prior Page et al. SVE meta as background/comparator, not as independent new replication.

D. **Cross-study synthesis/macro**: combine independent species-level learning records and species×plant pollen transfer only for descriptive/transportability sensitivity with explicit measurement error, observed species IDs and matched ecological covariates. A cross-study taxon match does NOT establish individual behavioral mediation; source-independent mating, deposition, learning and pollen outcomes are needed for mediation. Include "unmeasured" taxa rather than labeling all flies, beetles or moths cognitively low.

The long-term large trait table should have primary grain (population × date × plant flower part for UV, scent; actual original bee/hoverfly/butterfly/moth/beetle individual × repeated trial for learning and route). Pollinator guild represents taxonomic grouping only; learning/no-learning hypotheses are additional measured dimensions. Join by original trial when available, and by harmonized taxa only for descriptive macro associations. Correct for source-dependent detection biases and missing trait/experimental coverage. Do not force an islands-only or Bombus-only species set.

## Exact source-free contrast: cognition use is not pollen-transfer efficiency

The new module receiver_cognition_route_value.py uses exact rational parameters. Define:
- d: probability of encounter after long-range floral display/scent search;
- w: probability of choosing a local cue-using route, conditioned on encounter;
- b: correct route probability without cue;
- a: correct route probability when cue is actually used;
- eta_right, eta_wrong: pollen deposition probabilities conditional on route;
- c: receiver processing/time cost expressed in assumed normalized reward units.

Then, in one *constructed model*, cue-driven incremental plant pollen transfer per search opportunity is:

    DeltaPlant = d * w * (a - b) * (eta_right - eta_wrong).

The receiving animal's incremental net utility under a **fixed cue-use policy** is:

    DeltaReceiver = d * w * ( (a - b)*reward_unit - c ).

These do not represent observed insects, and a perfectly rational animal able to ignore the cue could choose w=0 to avoid a negative net gain. They demonstrate that plant and receiver utility can have opposing signs if a receiver continues a costly policy.

Two independently invented counterexamples (NO empirical species label):
- HIGH use w=.9, a=.95, b=.55, eta_right=.25, eta_wrong=0 gives DeltaPlant=.09.
- LOWER use w=.4, a=.8, b=.5, eta_right=.9, eta_wrong=0 gives DeltaPlant=.108.

Therefore, a lower cue-use frequency can still yield greater effective pollen transfer if mechanical deposition is higher. This is a CONSTRUCTIVE identification warning, not evidence of a naturally poor Bombus or better hoverfly.

For combined distant attraction and post-landing local cue, an exact algebraic sequential decomposition is:

    DeltaPlantTotal =
       (d1 - d0) * [eta_wrong + (eta_right-eta_wrong)*b]
       + d1 * w*(a-b)*(eta_right-eta_wrong)

The first part is display/scent driven discovery; the second is conditional guide/landing. This is a mathematical chain for one fixed model, NOT a cross-study causal path; the decomposition depends on order and cannot be estimated by multiplying unrelated papers' separate effect sizes.

### Predictions that can be FALSIFIED empirically

H1. On equal original floral reward/displays, increasing experimentally measured cue-discrimination and learned-use should enhance guide effects on landing/handling, unless the task is near a baseline-performance ceiling or noise makes the cue unreliable.

H2. Higher learning ability does not imply higher *plant-level* guide benefits after adjusting for body dimensions, legitimate contact, pollen deposition, abundance and visitation. Sign/size should be measured, not assumed positive.

H3. "Low cue-use" receiver groups should exhibit weaker dependence on manipulated guide consistency, but may be strong pollinators through innate stable preferences, high visitation or floral fit. Null is not "no cognition".

H4. The influence of odor versus visual cues depends on wind/plume intermittency and background contrast. Bees may flexibly learn to ignore redundant cues when one cue already perfectly predicts reward. This is NOT a rank ordering of brain size.

H5. Display enlargement can raise total arrival yet lower per-flower pollen quality through within-plant movements; this is a plant-reward conflict independent of receiver intellectual ability.

## Scientific stop

Only the eight published comparative taxa, qualitative ordering and separately sourced SVE prior art are identified; ZERO original paired cognitive-learning-and-pollen-transfer measurements or new meta effect sizes extracted. No original pollen deposition, animal energetic processing costs, adaptive flower evolution or fitness effects estimated here. The separate Stage32 Dryad UV raw workbook still returned HTTP 401 in official API request; don't pretend it has been read. Full CI must be separately verified. Draft only; no merge.
