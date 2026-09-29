# Villavicencio empirical positioning v1

Status: post-freeze empirical revision reserve. This file does **not** modify the frozen Evolution Letters V5 submission surface.

## Current position

The Villavicencio bridge has now passed through three distinct stages:

1. the original published phenological-overlap reanalysis produced strong gain discrimination but was found to reuse a response-conditioned support surface;
2. that interpretation was quarantined rather than defended;
3. a focal-response-excluded opportunity surface was rebuilt from public raw dated records and independently validated.

The valid ecological result is therefore the repaired raw-record result, not the historical published-overlap model.

## 1. Leakage repair

The published `phenological_overlap` matrix cannot be used as an independent full candidate-dyad gain predictor in this project. Every dyad with non-zero published overlap was observed as an interaction at least once over the six-year study, while none of the 5,194 never-linked dyads had positive published overlap.

That support leakage explains why the historical full model reached gain AUC 0.865. Removing the published overlap term collapses gain AUC to about 0.514 and proper-score skill to slightly below the null.

The historical result is retained numerically but is not ecological evidence.

## 2. Repaired current-state opportunity

Opportunity was rebuilt from raw dated visitor records without allowing the focal dyad response to construct its own predictor.

For each focal plant-pollinator dyad, current-year opportunity is based on:

- focal-plant flowering availability;
- focal-pollinator activity on **other** plants;
- their focal-response-excluded temporal overlap.

The repaired support is broad: 3,467 never-realized dyads have positive reconstructed opportunity, so opportunity is no longer nested inside realized-link support.

In the sampling-consistent annual primary scope:

- **gain:** AUC = **0.7434**, relative held-out log-loss reduction = **0.1393**;
- **loss:** AUC = **0.6684**, relative held-out log-loss reduction = **0.0682**;
- proper-score skill is positive in every primary held-out transition for both endpoints.

The same variables measured one year earlier do not recover the current-state signal:

- gain lagged AUC = **0.5278**;
- loss lagged AUC = **0.4059**, with log-loss worse than the null.

So the result is about **current ecological opportunity**, not a stable dyad propensity or a useful past-only forecasting rule.

## 3. Spatiotemporal robustness

The result remains when opportunity is made stricter: the focal plant must be flowering and the focal pollinator must be active on another plant in the **same site and ISO week**.

Primary same-site same-week results:

- **gain:** AUC = **0.7496**, relative log-loss reduction = **0.1465**, positive proper-score skill in 3/3 folds;
- **loss:** AUC = **0.6894**, relative log-loss reduction = **0.0872**, positive skill in 3/3 folds.

A previously absent dyad with positive same-site same-week opportunity forms a link at **12.72%**, versus **2.96%** when opportunity is zero, a rate ratio of about **4.29**.

Among established links, loss occurs at **47.14%** with positive same-site same-week opportunity versus **61.74%** when opportunity is zero.

This rules out the simple explanation that the repaired result exists only because spatially separated observations were pooled within the same week.

It does **not** remove shared sampling-process dependence or establish causality.

## 4. Pair-specific overlap is not the main result

The clean current-state model separates two marginal opportunity axes:

- plant flowering availability;
- pollinator activity on other plants.

Adding the dyad-specific weekly-overlap term on top of those marginals yields only a small increment:

- gain primary delta log-loss = **0.00128**;
- loss primary delta log-loss = **0.00389**;

and the increment becomes fold-unstable in broader temporal sensitivities.

Therefore the empirical bridge should **not** be framed as “fine pairwise phenological matching explains rewiring.”

The stronger result is that the current availability/activity state of the two sides constrains link dynamics.

## 5. Villavicencio endpoint-axis decomposition

Within Villavicencio, a post-result decomposition suggested an endpoint asymmetry:

- link **gain** carries more predictive information from pollinator activity on other plants than from plant availability;
- link **loss** carries more predictive information from focal-plant availability than from pollinator activity.

The primary and near-core folds are directionally consistent.

This was explicitly treated as hypothesis-generating rather than promoted to a mechanism.

## 6. Independent 12-site external test

The endpoint-axis direction was then frozen **before** opening dyad-level gain/loss effects in an independent eight-year, 12-site plant-pollinator dataset (Domínguez-Garcia et al. 2026).

The external test used leave-one-site-out validation and a focal-response-excluded pollinator-side activity measure.

### Gain: does not replicate

External gain:

- full AUC = **0.6449**;
- plant-availability increment = **0.01549**;
- pollinator-activity increment = **0.00410**;
- frozen pollinator-minus-plant contrast = **-0.01139**;
- only **2/12** held-out sites match the Villavicencio gain direction.

Thus the Villavicencio statement “formation is more pollinator-side weighted” does **not** generalize under the pre-frozen external measurement.

### Loss: directionally replicates

External loss:

- full AUC = **0.6118**;
- plant-availability increment = **0.02161**;
- pollinator-activity increment = **-0.00153**;
- frozen plant-minus-pollinator contrast = **+0.02314**;
- **10/12** held-out sites match the Villavicencio loss direction.

This provides cross-system support for a plant-availability-weighted loss/persistence pattern under the clean focal-excluded definitions.

## 7. Measurement mapping is itself part of the result

A post-result external sensitivity replaced the focal-excluded pollinator activity proxy with published pollinator abundance or phenology.

The exact axis dominance changed substantially:

- gain ranged from plant-dominant to approximately tied to weakly pollinator-dominant;
- loss became pollinator-dominant under the published pollinator metrics.

Because those published pollinator metrics may share observation support with focal interaction detection, they cannot replace the clean primary external test.

But they show something important:

> **the existence of an ecological-opportunity signal is more portable than the exact allocation of predictive information between plant and pollinator axes.**

Axis dominance is therefore not a universal mechanism in the present evidence.

## 8. Revised ecological result

The strongest defensible empirical statement is now:

> **Annual plant-pollinator link dynamics contain a reproducible current-state opportunity signal after focal-response leakage is removed. This signal survives same-site same-week matching, is substantially stronger than a one-year-lagged control, and is carried mainly by marginal plant availability and pollinator activity rather than by fine dyad-specific temporal matching. Which side dominates link formation is not cross-system invariant. Plant-side availability shows more consistent support for link persistence/loss under the focal-excluded definitions, but even this is not yet a causal mechanism.**

This is a stronger ecological position than the earlier “phenology predicts rewiring” claim because it specifies:

- what the valid opportunity exposure is;
- what information is excluded from it;
- what temporal and spatial controls it survives;
- which component does **not** generalize.

## 9. Relation to routeability

None of these analyses validates routeability.

The empirical hierarchy is:

`current ecological opportunity -> realized link dynamics`

The missing routeability layer is still:

`independent cue / decision structure -> incremental information beyond ecological opportunity`

Decision-equivalence classes must therefore come from independent cognition or cue-choice evidence, or from the controlled routeability experiment already designed in PR #65.

The network analyses cannot manufacture that layer from the same links they predict.

## Claim ceiling

Allowed:

- focal-response-excluded current ecological opportunity discriminates annual link gain and loss;
- the result survives a same-site same-week opportunity definition;
- a one-year-lagged opportunity surface does not recover the same signal;
- dyad-specific overlap adds only small, sensitivity-dependent information beyond marginal opportunity;
- the Villavicencio gain-side axis dominance does not generalize in the pre-frozen external test;
- the plant-side loss direction is cross-system consistent under the focal-excluded primary definitions.

Not allowed:

- the published aggregate phenology surface is an independent gain filter;
- current opportunity causally determines rewiring;
- gain and loss have universally distinct causal mechanisms;
- pollinator-side control of formation is universal;
- plant-side control of persistence is a universal mechanism independent of measurement;
- these results validate decision equivalence or routeability.
