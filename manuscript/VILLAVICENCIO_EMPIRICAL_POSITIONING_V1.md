# Villavicencio empirical positioning v1

Status: **REPAIRED AFTER SUPPORT-LEAKAGE AUDIT on 2026-09-28.** This file remains a post-freeze empirical revision reserve and does **not** modify the frozen Evolution Letters V5 submission surface.

Machine surfaces:
- `validation/villavicencio_phenology_support_leakage_v1.json`
- `validation/villavicencio_focal_excluded_opportunity_gate_v1.json`
- `validation/villavicencio_focal_excluded_opportunity_result_v1.json`
- `validation/villavicencio_current_opportunity_axis_audit_result_v1.json`
- `validation/villavicencio_siteweek_opportunity_audit_result_v1.json`
- `validation/villavicencio_raw_subseason_reconstruction_result_v1.json`

## 1. The original published-overlap interpretation is superseded

The original annual analysis treated the published `phenological_overlap` matrix as an outcome-independent ecological opportunity filter over all 45 × 135 candidate plant-pollinator dyads. A raw-surface audit showed that this assumption is false for that use.

Across all 6,075 dyads:
- 881 are observed as positive links in at least one annual network;
- 827 have non-zero published phenological overlap;
- all 827 non-zero-overlap dyads belong to the 881 ever-observed links;
- among the 5,194 never-observed dyads, zero have non-zero published overlap.

Thus `P(ever linked | published overlap > 0) = 1.0` on the workbook surface. The published overlap matrix cannot be used as an independent candidate-dyad predictor of link gain.

The historical full-model values remain numerically reproducible (gain AUC 0.8652, loss AUC 0.6505), but their phenology/gain-filter interpretation is quarantined. This does **not** invalidate Peralta et al. (2020); it invalidates this project's reuse of their observed-interaction phenology surface as a full candidate-dyad predictor.

## 2. Focal-response-excluded repair

The raw Figshare visitor records were used to reconstruct temporal opportunity without allowing the focal plant-pollinator link to define its own predictor.

For focal plant `p`, pollinator `i`, and year `y`:

1. **plant availability:** weeks in which `p` was observed flowering;
2. **pollinator activity:** weeks in which `i` was observed visiting at least one plant other than `p`;
3. **focal-excluded overlap:** weeks satisfying both conditions.

The focal `p-i` interaction is excluded from the pollinator-activity and overlap predictors. Undated positive visits may define the annual response link but never enter weekly opportunity predictors.

The raw positive-visit records reproduce the Stage-1 annual response exactly: response mismatch count = **0** across all 7,620 shared-dyad transition rows.

### Support is no longer response-conditioned

The repaired surface covers candidate dyads that never became links:

- total trait-subset dyads: **6,075**;
- ever linked: **881**;
- never linked: **5,194**;
- positive reconstructed opportunity in at least one year: **4,295**;
- opportunity-positive but never linked: **3,467**;
- `P(ever linked | repaired opportunity > 0) = 0.193`.

Therefore the repaired opportunity surface is not nested inside realized-link support.

## 3. Ecological result: current opportunity, not stable propensity

The primary sampling-consistent scope is 2008–2011, evaluated by leave-one-transition-out response holdout.

### Link gain

For 4,750 previously absent dyad-transition rows with 443 gains, the focal-response-excluded **current-year** opportunity model gives:

- ROC AUC = **0.7434**;
- relative held-out log-loss reduction = **0.1393**;
- held-out Brier improvement = **0.00908**;
- positive log-loss skill in **3/3** primary held-out transitions.

A binary descriptive contrast is also large: gain rate is **0.1147** when current focal-excluded opportunity is positive versus **0.0318** when it is zero, a ratio of **3.61**.

### Link loss

For 692 established dyad-transition rows with 343 losses:

- ROC AUC = **0.6684**;
- relative held-out log-loss reduction = **0.06825**;
- held-out Brier improvement = **0.02355**;
- positive log-loss skill in **3/3** primary held-out transitions.

The broad 4-transition and 5-transition sensitivity scopes retain positive full-model log-loss skill for both gain and loss in every held-out transition.

These are **retrospective current-state opportunity associations**. The current-year predictors are measured from the same ecological year as the response endpoint, so this is not prospective forecasting.

### Same-site same-week robustness

The signal is not created solely by pooling spatially separated observations within the same week. Requiring focal-plant flowering and focal-pollinator activity on other plants to occur in the **same site × ISO-week cell** gives, in the same primary scope:

- gain AUC = **0.7496**, relative held-out log-loss reduction = **0.1465**, positive skill in **3/3** transitions;
- loss AUC = **0.6894**, relative held-out log-loss reduction = **0.08721**, positive skill in **3/3** transitions.

Descriptively, previously absent dyads form links at **12.72%** when same-site same-week opportunity is positive versus **2.96%** when it is zero (rate ratio ≈ **4.29**). Established links are lost at **47.14%** with positive site-week opportunity versus **61.74%** when it is zero.

This strengthens the current-state opportunity interpretation, but the predictors and responses are still observed through the same sampling process. It does not remove sampling-effort confounding or make the result causal.

## 4. Pair-specific temporal matching is not the main result

The full model contains pair-specific focal-excluded overlap plus two marginal quantities:
- plant flowering weeks;
- pollinator activity weeks on other plants.

Removing the pair-specific overlap term leaves almost all of the predictive skill.

Primary scope:

- gain marginal-only AUC = **0.7400**, relative log-loss reduction = **0.1353**;
- loss marginal-only AUC = **0.6647**, relative log-loss reduction = **0.06268**.

The pair-specific overlap term improves primary log loss in 3/3 folds, but the pooled increment is small:
- gain Δ log loss = **+0.00128** when overlap is removed;
- loss Δ log loss = **+0.00389**.

More importantly, this increment becomes fold-unstable in broader temporal sensitivities:
- gain: 3/4 and 4/5 positive folds;
- loss: 3/4 and 3/5 positive folds.

Therefore the ecological headline is **availability/activity opportunity**, not pair-specific phenological matching.

## 5. Past-only negative control

The same opportunity variables were reconstructed using the **previous year only** and used as a past-only negative control.

Primary scope:

### Gain
- lagged AUC = **0.5278**;
- relative log-loss reduction = **0.01039**.

### Loss
- lagged AUC = **0.4059**;
- relative log-loss reduction = **−0.02712**;
- Brier performance is also worse than the null.

Current-year log-loss skill exceeds the lagged model in **3/3 primary folds for both endpoints**, **4/4** folds in the near-core sensitivity, and **5/5** folds in the full annual sensitivity.

Thus the repaired signal is not well described as a stable dyad propensity that can simply be carried forward one year. It is much more consistent with **current ecological opportunity**.

## 6. Current opportunity is itself asymmetric across endpoints

A post-result decomposition asks which of the two clean marginal opportunity axes carries more held-out information:

- **plant availability:** focal-plant flowering weeks;
- **pollinator activity:** weeks in which the pollinator visits other plants.

Both axes add reproducible information in the primary scope, but their relative contributions reverse between link gain and link loss.

### Gain

Removing pollinator activity from the two-axis marginal model worsens held-out log loss by **0.02620**, whereas removing plant availability worsens it by **0.01169**. The pollinator-activity increment is larger in **3/3** primary folds and **4/4** near-core folds; the same direction persists in **5/5** annual folds.

### Loss

Removing plant availability worsens held-out log loss by **0.03671**, whereas removing pollinator activity worsens it by only **0.00506**. The plant-availability increment is larger in **3/3** primary folds and **4/4** near-core folds. In the all-annual sensitivity it remains larger in **4/5** folds; the exception is 2006→2007, the transition already isolated as sampling-sensitive because 2006 used an expanded site pool.

The resulting ecological hypothesis is therefore more specific:

> **Formation appears more pollinator-activity weighted, whereas loss appears more plant-availability weighted.**

This wording is deliberately predictive rather than causal. The decomposition was motivated after the repaired result was seen, both axes are measured through the observational sampling process, and the 2006 sensitivity demonstrates that the contrast is not immune to sampling design. It is a hypothesis-generating endpoint asymmetry for independent replication, not evidence that pollinator behaviour causes link formation or that plant phenology causes link loss.

## 7. What is now supported

The strongest defensible empirical statement is:

> **Plant-pollinator link dynamics are strongly conditioned by current ecological opportunity. Independently reconstructed plant availability and pollinator activity discriminate link formation and, more moderately, link loss even when the focal interaction is excluded from predictor construction. The same variables measured one year earlier do not recover that signal.**

This is more specific than saying that “phenology predicts rewiring.” It separates:
- current availability/activity;
- pair-specific temporal matching;
- stable past-only propensity.

The first is supported; the second is small and sensitivity-dependent; the third is not supported as a useful forecasting explanation.

## 8. What remains unresolved

This analysis does not establish:
- a causal effect of phenology or temporal opportunity;
- causal primacy of availability/activity;
- strict future-link forecasting;
- a universal assembly-versus-disassembly mechanism;
- pair-specific phenological matching as the dominant driver;
- sampling-effort-corrected true rewiring;
- decision-equivalence classes;
- environmental routeability.

The response remains detection-sensitive. However, the higher-resolution target is no longer blocked on RData bytes: the Dryad-documented date boundaries applied to the public raw visitor records reconstruct **18 non-empty subseason networks and 12 within-year transitions**, with **4,581 shared-dyad rows and 853 changed links (422 gains, 431 losses)**.

Dated records fully recover annual link support for 2006–2010. In 2011, 433 of 440 annual links are date-reconstructable and seven occur only in undated positive rows, so a dated-complete sensitivity excluding 2011 is required for subseason analyses. The reconstruction does not claim byte-for-byte identity with the unavailable RData object.

## 9. Relation to routeability

The Villavicencio repair now supplies a valid **ecological baseline layer**:

`species persistence -> current availability/activity opportunity -> realized link dynamics`.

Routeability, if tested later, must add information beyond this clean baseline using an independently measured decision layer. The network data alone still do not validate routeability.

## Claim ceiling

The repaired Villavicencio result is a retrospective current-state ecological opportunity result. It establishes that focal-response-excluded availability/activity contains reproducible information about annual link gain and loss, especially gain formation. It does **not** establish causality, strict forecasting, pair-specific temporal matching as the dominant mechanism, decision equivalence, or routeability.
