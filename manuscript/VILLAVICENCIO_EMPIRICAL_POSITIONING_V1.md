# Villavicencio empirical positioning v1

Status: post-freeze empirical revision reserve. This file does **not** modify the frozen Evolution Letters V5 submission surface.

## Current position

The Villavicencio work has now resolved the two largest observational ambiguities that were previously left open:

1. the published phenological-overlap surface was response-conditioned for the candidate-gain task and was quarantined;
2. raw 5-min census effort was reconstructed and showed that binary link gain/loss is materially detection-sensitive.

The resulting conclusion is narrower, but much more defensible:

> **The public Villavicencio data provide a reproducible observed-link turnover and sampling-effort test bed, but they do not identify a general natural ecological rewiring mechanism. A focal-response-excluded current-opportunity signal is strong on binary link surfaces, small and fold-mixed on an effort-standardized census-incidence response, and maps more consistently to current detectability/activity (4/6 transitions) than to latent link-state transitions (1/6).**

This means the observational network analysis is now a **feasibility and failure-boundary result**, not empirical confirmation of routeability.

## 1. Raw 18-period response reconstruction

The preferred response is reconstructed from the public Figshare raw visitor records rather than requiring unavailable Dryad RData bytes.

Using the externally documented early / mid / late date boundaries gives:

- 18 non-empty subseason networks;
- 12 within-year adjacent transitions;
- 4,581 shared-dyad rows;
- 853 observed binary changes;
- 422 observed gains;
- 431 observed losses;
- changed and unchanged dyads in all 12 transitions.

The raw reconstruction is reproducible and receipt-backed.

Exact byte-for-byte identity with the unavailable published RData object is **not** established. That is an optional source-identity cross-check, not a prerequisite for reproducing the public raw-record response surface.

The more important limitation is detection.

## 2. Sampling-effort semantics are resolved

The raw metadata define `obs.time` as the start time of a 5-min focal-plant observation period.

A census is therefore identified by:

`site × study year × date × focal plant × obs.time`.

The reconstructed annual census counts are:

- 2006: **532** raw / **532** published;
- 2007: **372 / 372**;
- 2008: **530 / 530**;
- 2009: **836 / 836**;
- 2010: **463 / 460**;
- 2011: **988 / 988**.

Thus the census identity reproduces the published totals exactly in five of six years. The +3 difference in 2010 is retained explicitly rather than coerced away.

So `sampling_effort_semantics` is no longer UNRESOLVED.

The unresolved quantity is now the **latent link state under incomplete detection**.

## 3. Detection sensitivity is material

Subseason census effort varies from **38 to 424** identifiable 5-min censuses, even in the stable two-site core.

Bias-corrected incidence Chao2 implies that the observed trait-subset link surface represents only about **31.4% to 65.4%** of the estimated incidence support across subseasons.

More directly, among the 853 observed changes, the simple score

`log(1 + current focal-plant censuses) - log(1 + previous focal-plant censuses)`

discriminates observed gain from observed loss with:

- strict dated core 2008–2010: AUC **0.815**;
- two-site core 2008–2011: AUC **0.824**;
- all 2006–2011: AUC **0.834**.

Observed gains occur where focal-plant census effort tends to increase; observed losses occur where it tends to decrease.

This AUC is a **supporting diagnostic, not independent inferential evidence**. Gain and loss are themselves defined by a reversal of observed detection state between adjacent periods, so an effort-change score is mechanically aligned with the contrast whenever detectability changes. The stronger evidence for material detection sensitivity comes from three less circular diagnostics: positive held-out skill of effort-only models, state instability under matched-effort rarefaction, and low Chao2 link completeness.

This does **not** mean the changes are pure observer artefacts. Census allocation is partly endogenous to plant flowering availability, so effort itself contains biology.

But it does mean that binary zero/non-zero link states cannot identify true absence.

## 4. Effort-only held-out models already predict binary turnover

Using only previous- and current-period focal-plant census counts, without ecological opportunity or routeability variables, gives held-out discrimination in the strict dated core:

- gain AUC = **0.697**, relative log-loss reduction = **0.0430**;
- loss AUC = **0.670**, relative log-loss reduction = **0.0503**.

The effect persists broadly, although not in every fold.

Therefore sampling intensity is not merely a theoretical nuisance. It contains enough information to predict a non-trivial part of the observed binary gain/loss surface.

## 5. Matched-effort rarefaction destabilizes link-state labels

A 500-replicate stress test downsampled both adjacent periods, within focal plant × site, to the smaller number of identifiable 5-min censuses.

In the strict dated core, the mean probability of retaining the original binary state is only:

- observed gain: **0.580**;
- observed loss: **0.595**;
- stable present: **0.604**.

Across all years, gain and loss retention remain only about **0.57–0.58**.

These complements are **not** false-rewiring fractions: downsampling can create additional false non-detections even for true persistent links.

The correct conclusion is state instability under observation-intensity standardization.

## 6. Consequence for the 853 changes

The 853 binary changes are reproducible **observed-link turnover events**.

They are **not 853 identified ecological rewiring events**.

Allowed language:

- observed link gain;
- observed link loss;
- observed-link turnover;
- detection-sensitive Stage-1 response;
- response feasibility.

Not allowed as observed facts:

- true interaction gain;
- true interaction extinction;
- ecological rewiring event;
- sampling-effort-corrected rewiring.

A simple latent-detection model has now been fitted as a sensitivity analysis, but its posterior states remain model-based quantities rather than observed truth.

## 7. Historical published-phenology result remains quarantined

The original published `phenological_overlap` reanalysis produced:

- gain AUC ≈ **0.865**;
- loss AUC ≈ **0.650**;
- strong phenology block-ablation arithmetic.

But the source-surface audit showed that every non-zero published-overlap dyad belonged to the ever-realized interaction support, while none of 5,194 never-linked candidate dyads had positive published overlap.

The gain-side ecological interpretation is therefore response-support leakage.

Those numbers remain reproducible historical arithmetic, not evidence that phenology independently predicts candidate link formation.

## 8. Focal-response-excluded binary opportunity repair

Raw dated records were used to construct current ecological opportunity without allowing the focal link itself to define its predictor.

This successfully removed the support leakage.

On the annual binary surface, the repaired current-state model showed substantial held-out discrimination:

- gain AUC ≈ **0.743**;
- loss AUC ≈ **0.668**.

Same-site × same-week opportunity also retained strong binary discrimination.

These results remain useful **detection-sensitive associations**.

They are no longer sufficient for an ecological rewiring claim because the binary response itself is effort-sensitive.

## 8b. Annual binary gain is not exhausted by focal-plant effort

The annual repaired opportunity signal was also compared directly against raw focal-plant census counts.

In the strict 2008–2011 annual core:

**Gain**
- effort-only log loss = **0.30345**, AUC = **0.6442**;
- opportunity-only log loss = **0.27804**, AUC = **0.7400**;
- opportunity + effort log loss = **0.27357**, AUC = **0.7552**;
- opportunity increment beyond effort = **+0.02988**, positive in **3/3** folds.

The same gain direction is positive in **4/4** near-core folds, but **4/5** when the 2006 expanded site pool is included.

**Loss**
- opportunity increment beyond effort = only **+0.00292**;
- positive in **2/3** strict-core folds.

Thus focal-plant census effort is **not a complete explanation of the annual gain association**.

This does not rescue a true-rewiring claim. The response is still binary observed-link presence/absence, so pollinator-side detection and zero-state misclassification remain unresolved.

The annual effort-control result and the subseason census-rate result answer different questions:

- annual binary gain: opportunity contains information beyond focal-plant census counts;
- effort-standardized subseason incidence: that incremental opportunity signal is small and only **4/6** folds positive.

Together they argue against both extreme interpretations: neither “the entire signal is just focal-plant effort” nor “the signal is a reproducible effort-independent rewiring mechanism” is supported.

## 9. Effort-standardized census-incidence response

To move observation effort into the response denominator, a second analysis models the number of positive focal-interaction detections out of the number of identifiable 5-min focal-plant censuses.

The primary strict dated scope uses six within-year transitions from 2008–2010.

Candidate dyads are defined independently of the focal response:

- the focal plant has identifiable censuses in both periods;
- the pollinator is independently observed on another plant in both periods.

This yields:

- **3,117** dyad-transition rows;
- **24,684** current dyad-census trials;
- **617** positive focal-interaction censuses.

The baseline model uses previous-period interaction incidence.

Adding current focal-response-excluded same-site × same-week opportunity gives:

- history-only per-census log loss: **0.111207**;
- history + opportunity: **0.109937**;
- pooled improvement: **0.001270**;
- positive fold direction: **4/6**.

Two 2009 transitions become worse when opportunity is added.

Under the frozen rule, the result is therefore:

**not reproducible across primary transitions**.

This is the most important update to the ecological interpretation.

## 10. What survives after effort standardization?

A weak residual survives:

> current focal-response-excluded opportunity has a small positive pooled association with per-census interaction incidence after accounting for recent interaction history.

What does **not** survive:

> a reproducibly positive opportunity increment across all primary subseason transitions.

Therefore the strong binary-network result cannot be promoted as an effort-independent ecological mechanism.

The evidence is consistent with a mixture of:

- biological opportunity;
- variation in floral availability;
- observation allocation;
- imperfect interaction detection;
- genuinely changing interactions.

The present data do not identify those components uniquely.

## 11. Repeated-detection model: binary gain/loss is not latent state identity

The repeated 5-min censuses make a simple two-season dynamic occupancy/detection sensitivity possible.

For each adjacent subseason transition, the model estimates:

- previous latent link occupancy `psi`;
- latent colonization `gamma`;
- latent extinction `epsilon`;
- previous and current per-census detection probabilities.

The identifiability rule was frozen before fitting. A transition must have:

- optimizer convergence from all deterministic starts;
- multi-start NLL range <= 1e-6;
- positive-definite Hessian;
- finite logit-scale standard errors;
- interior detection probabilities.

Five of six strict dated-core transitions pass. The only weak transition is **2009 early -> mid**, where the multi-start NLL range is 2.565e-6 rather than <= 1e-6.

Conditional per-census detection probabilities are low:

- previous-period `p`: about **0.051-0.147**;
- current-period `p`: about **0.055-0.180**.

This is enough to explain why zeros are dangerous.

On the focal-response-excluded candidate surface:

- observed binary gains = **196**;
- summed posterior expected latent gains = **279.6**;
- observed binary losses = **253**;
- summed posterior expected latent losses = **212.1**.

These are not corrected event counts. They are model-based posterior sums.

More revealingly, among observed binary changes:

- weighted mean posterior probability that an observed gain is a true latent gain = **0.575**;
- weighted mean posterior probability that an observed loss is a true latent loss = **0.464**.

The mapping varies sharply among transitions. For example, in 2009 early->mid, the mean posterior true-loss probability among observed losses is only **0.134**.

So even when a simple detection model is identifiable enough to use as a sensitivity layer, the observed gain/loss labels are not reliable latent-state identities.

## 12. Current opportunity decomposes mainly onto detection, not latent rewiring

Because current opportunity is constructed from pollinator activity on other plants, it could affect either:

1. the latent link-state transition itself; or
2. the probability of detecting the focal pollinator in the current period.

These were separated in four predeclared models per transition:

- base;
- detection-only;
- state-only;
- state + detection.

A state-side transition was counted as supported only when:

- state + detection beat detection-only by at least 2 AIC;
- `beta_gain > 0`;
- `beta_loss < 0`.

A general state result required this in **at least 5/6** transitions.

Result:

- latent state-side support: **1/6**;
- detection-side support: **4/6**;
- general state promotion: **FAIL**.

The only transition passing the state rule is **2008 early->mid**.

Detection-only is materially favored in:

- 2008 early->mid;
- 2008 mid->late;
- 2010 early->mid;
- 2010 mid->late.

The two 2009 transitions support neither a robust detection-side nor a state-side opportunity component under the frozen rule.

This changes the ecological interpretation substantially.

The strong binary opportunity signal is not best read as:

> opportunity drives network rewiring.

It is better read as:

> **current ecological opportunity strongly marks when active pollinators are encounterable/detectable, while evidence that it generally changes latent link states is weak and non-replicated across subseasons.**

Encounter and detectability are still ecological. They reflect activity, co-occurrence and observation opportunity. But they are not the same thing as latent interaction assembly or extinction.

## 12b. Richer detection heterogeneity makes latent transition inference model-dependent

The simple repeated-detection model is not the end of the detection problem.

A frozen robustness analysis replaced simple binomial detection with a beta-binomial observation model that allows extra-binomial heterogeneity among repeated focal-interaction detections.

Result:

- beta-binomial detection is preferred in **6/6** primary transitions;
- its AIC is at least **13.8** lower than the simple binomial model in every transition;
- under the richer observation model, at least one latent transition parameter reaches the frozen state boundary in **6/6** transitions.

So the simple-binomial latent gain/loss estimates are not stable enough to be promoted as a detection-corrected ecological response.

This closes an important loophole. The correct lesson is not:

> fit a more sophisticated occupancy model and recover the true rewiring surface.

It is:

> **the repeated censuses are sufficient to diagnose strong detection dependence, but the latent transition surface itself remains observation-model dependent.**

Accordingly, neither the raw binary changes nor the model-based latent transitions identify a stable natural rewiring mechanism in this dataset.

Source:
- `validation/villavicencio_detection_overdispersion_result_v1.json`

## 13. External 12-site result


The independent Domínguez-Garcia et al. dataset remains useful as a cross-system predictive test, but it also uses observational network states and should not be treated as a latent-detection validation of Villavicencio.

The pre-frozen external axis test was mixed:

- Villavicencio gain-side pollinator dominance did **not** replicate;
- the plant-side loss direction replicated under the clean focal-excluded external definition.

Measurement-mapping sensitivities showed that exact plant-versus-pollinator axis dominance changes with variable definition.

The cross-system lesson is therefore not a universal assembly/disassembly mechanism.

## 14. Relation to routeability

None of these observational analyses validates routeability.

The observational chain reaches only:

`sampling process + ecological opportunity -> observed interaction incidence / observed link states`.

Routeability requires an independent layer:

`cue / decision architecture -> additional effect beyond ordinary opportunity`.

The network response cannot be used to manufacture that decision structure.

## 15. Stop rule for observational expansion

Do **not** keep adding flexible observational models to Villavicencio in search of a positive natural-rewiring result.

The useful questions have been answered:

- Can the 18-period response be reconstructed? **Yes.**
- Can sampling effort be reconstructed? **Yes.**
- Is binary turnover materially effort-sensitive? **Yes.**
- Does equalizing effort destabilize states? **Yes.**
- Does current opportunity retain a universally reproducible increment on an effort-standardized census-rate response? **No; 4/6 folds only.**
- Can repeated censuses support a simple latent-state sensitivity model? **Yes, in 5/6 transitions.**
- Does current opportunity then show a general latent state-transition effect? **No; state support is 1/6 versus a frozen 5/6 requirement.**
- Is a detection/activity-side opportunity component more common? **Yes; 4/6 transitions.**

The observational program has therefore reached its stop rule. Further model searching for a positive natural-rewiring result would be specification hunting.

The next routeability evidence should come from the already designed controlled experiment or from a genuinely detection-standardized independent network dataset with an externally defined decision layer.

## Claim ceiling

The strongest defensible empirical statement is now:

> **Villavicencio provides a reproducible 18-period observed interaction-turnover surface whose sampling effort can be reconstructed well enough to show that binary link dynamics are materially detection-sensitive. A focal-response-excluded opportunity signal is strong on binary observed-link surfaces, small and temporally heterogeneous on an effort-standardized census-incidence response, and in a repeated-detection sensitivity maps more consistently to current detectability/activity (4/6 transitions) than to latent state transitions (1/6). Thus the public data support response feasibility, ecological activity/detection structure and a sharp rewiring-identification boundary—not a general natural rewiring mechanism or routeability.**

Do not claim:

- 853 true rewiring events;
- sampling-effort-corrected gain/loss;
- a universal current-opportunity mechanism;
- causal plant/pollinator control of network assembly;
- empirical routeability from Villavicencio.
