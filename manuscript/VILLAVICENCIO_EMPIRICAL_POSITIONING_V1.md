# Villavicencio empirical positioning v1

Status: post-freeze empirical revision reserve. This file does **not** modify the frozen Evolution Letters V5 submission surface.

## Current position

The Villavicencio work has now resolved the two largest observational ambiguities that were previously left open:

1. the published phenological-overlap surface was response-conditioned for the candidate-gain task and was quarantined;
2. raw 5-min census effort was reconstructed and showed that binary link gain/loss is materially detection-sensitive.

The resulting conclusion is narrower, but much more defensible:

> **The public Villavicencio data provide a reproducible observed-link turnover and sampling-effort test bed. They do not presently identify natural ecological rewiring. A focal-response-excluded current-opportunity signal is visible on binary link surfaces, but its incremental information becomes small and temporally inconsistent after the response is standardized by focal-plant census effort.**

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

Not allowed without a latent-detection model or a better standardized response:

- true interaction gain;
- true interaction extinction;
- ecological rewiring event;
- sampling-effort-corrected rewiring.

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

## 11. External 12-site result

The independent Domínguez-Garcia et al. dataset remains useful as a cross-system predictive test, but it also uses observational network states and should not be treated as a latent-detection validation of Villavicencio.

The pre-frozen external axis test was mixed:

- Villavicencio gain-side pollinator dominance did **not** replicate;
- the plant-side loss direction replicated under the clean focal-excluded external definition.

Measurement-mapping sensitivities showed that exact plant-versus-pollinator axis dominance changes with variable definition.

The cross-system lesson is therefore not a universal assembly/disassembly mechanism.

## 12. Relation to routeability

None of these observational analyses validates routeability.

The observational chain reaches only:

`sampling process + ecological opportunity -> observed interaction incidence / observed link states`.

Routeability requires an independent layer:

`cue / decision architecture -> additional effect beyond ordinary opportunity`.

The network response cannot be used to manufacture that decision structure.

## 13. Stop rule for observational expansion

Do **not** keep adding flexible observational models to Villavicencio in search of a positive natural-rewiring result.

The useful questions have been answered:

- Can the 18-period response be reconstructed? **Yes.**
- Can sampling effort be reconstructed? **Yes.**
- Is binary turnover materially effort-sensitive? **Yes.**
- Does equalizing effort destabilize states? **Yes.**
- Does current opportunity retain a universally reproducible increment on an effort-standardized census-rate response? **No; 4/6 folds only.**

Further observational model searching risks turning a useful failure-boundary result into specification hunting.

The next routeability evidence should come from the already designed controlled experiment or from a genuinely detection-standardized independent network dataset with an externally defined decision layer.

## Claim ceiling

The strongest defensible empirical statement is now:

> **Villavicencio provides a reproducible 18-period observed interaction-turnover surface whose sampling effort can be reconstructed exactly enough to show that binary link dynamics are materially detection-sensitive. A focal-response-excluded opportunity signal is strong on binary observed-link surfaces but becomes small and temporally heterogeneous when interaction incidence is standardized by 5-min census effort. Thus the public data support response feasibility and a detection boundary, not identified ecological rewiring or routeability.**

Do not claim:

- 853 true rewiring events;
- sampling-effort-corrected gain/loss;
- a universal current-opportunity mechanism;
- causal plant/pollinator control of network assembly;
- empirical routeability from Villavicencio.
