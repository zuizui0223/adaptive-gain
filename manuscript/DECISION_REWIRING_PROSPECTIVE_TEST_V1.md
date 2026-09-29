# Prospective rewiring test v1 — decision-structural turnover as a constraint on network rewiring

Status: post-freeze empirical revision reserve. This file does **not** modify the frozen Evolution Letters V5 submission surface.

## Purpose

The frozen V5 routeability paper makes a deliberately narrow mechanistic claim: ecological change matters for a focal interaction when it changes the distinctions that must be resolved, not merely when it changes richness or composition.

The existing ecological-novelty extension connects this claim to network rewiring but stops one step before a prospective empirical test. This document freezes that next step.

The central empirical question is:

> **Among ecological-network changes with similar species turnover and similar opportunity to rewire, does crossing a decision-equivalence boundary predict more interaction rewiring than turnover that remains within the same decision-equivalence structure?**

This is not a new theorem. It is a falsifiable ecological translation of the existing target-relevant quotient result.

## Causal ordering to preserve

The quantities must be defined in the following order:

1. **availability / compatibility:** which partners could in principle interact, based on co-occurrence, morphology, phenology and other hard filters;
2. **decision structure:** which distinctions a focal organism must resolve among those permitted alternatives;
3. **behaviorally accessible set:** which permitted alternatives remain reachable under the frozen decision structure;
4. **observed interaction network:** realized links after abundance, encounter, energetic, competitive and demographic filters.

Decision-equivalence classes must therefore be defined independently of the observed rewiring response. Inferring them from the same link changes used as the outcome would be circular.

## Primary unit of analysis

Use repeated ecological networks from the same system across time, space, or experimentally manipulated environments.

The primary analysis is restricted to **shared species pairs or shared focal species with a non-zero shared partner pool**, so that rewiring is observable separately from pure species turnover.

For each transition from network (t) to (t+1), freeze:

- species turnover;
- number and identity of shared species;
- shared-partner opportunity set;
- abundance or encounter-rate covariates where available;
- morphology / phenology compatibility;
- environmental change;
- decision-equivalence structure at (t) and (t+1);
- observed link additions, losses, and rewiring among shared species.

## Primary exposure

Define a transition-level indicator:

[
D_{t,t+1}=1
]

when the transition creates, removes, merges, or splits at least one decision-equivalence class for the declared focal interaction.

Define

[
D_{t,t+1}=0
]

when taxonomic replacement occurs only within the frozen class structure.

A richer secondary exposure can count the number of equivalence-boundary events, but the binary boundary-crossing variable is the confirmatory exposure because it follows most directly from the exact quotient logic.

## Confirmatory prediction P1 — low-turnover diagnostic regime

The cleanest test uses transitions with low taxonomic turnover and a substantial shared-species pool.

> **P1.** Conditional on shared-partner opportunity and conventional compatibility filters, transitions with (D=1) will show greater rewiring among shared species than matched transitions with (D=0).

This is the most diagnostic regime because a positive result cannot be explained merely by wholesale species replacement.

The prediction concerns **rewiring magnitude or probability**, not the direction of particular link gains or losses.

## Confirmatory prediction P2 — within-class turnover as a structural negative control

> **P2.** High taxonomic turnover that remains within corresponding decision-equivalence classes can produce less rewiring than taxonomic distance alone would predict.

Operationally, among transitions matched on species-turnover magnitude and shared-partner opportunity, within-class turnover should have a lower rewiring response than boundary-crossing turnover.

A null result here does not invalidate the theorem. It rejects the proposed ecological bridge if observed networks do not retain the predicted structural distinction.

## Confirmatory prediction P3 — final-representative threshold

Decision-equivalence multiplicity motivates a sharper event-level empirical test. The exact quotient guarantees invariance for non-final within-class loss at the declared decision level; it does not guarantee that final-representative loss must change observed rewiring.

For a class with multiple represented partners, distinguish:

- loss of a **non-final representative**, after which the class remains represented;
- loss of the **final representative**, after which an entire decision branch disappears.

> **P3.** Loss of the final representative is predicted to be more likely to alter the focal rewiring opportunity structure than loss of a non-final representative, after conditioning on the same one-species richness decrement.

This is the strongest threshold-like prediction in the extension.

This direction is an ecological hypothesis layered on the exact non-final-loss invariance result. It is explicitly a prediction about the **accessibility architecture**, not ecosystem stability.

## Confirmatory prediction P4 — same species, changed decision structure

The converse regime is equally important.

> **P4.** Rewiring can increase under low taxonomic turnover when environmental change alters cue reliability, encounter context, or another frozen component of the focal decision structure.

This prediction separates decision-structural turnover from compositional turnover. It is especially useful in systems with repeated observations of largely stable species assemblages across environmental variation.

## Outcome definitions

At least one primary rewiring outcome must be frozen before looking at the focal contrast.

Allowed primary outcomes include:

- probability that a shared-species dyad changes interaction state;
- number or proportion of changed links among compatibility-permitted shared dyads;
- an established rewiring component of network beta diversity calculated only after the species-turnover component has been separated.

Do not define a new response metric after inspecting which version yields the strongest effect.

## Decision-equivalence measurement

The empirical bottleneck is not the network statistic. It is the independent construction of decision-equivalence classes.

Acceptable sources, in descending evidential strength:

1. controlled cue-choice or discrimination experiments;
2. pre-existing behavioral assays defining accept / reject or route-choice structure;
3. mechanistically justified cue-response models trained on independent data;
4. externally frozen trait combinations with explicit biological justification.

Not acceptable for the confirmatory test:

- clustering partners by their observed network links in the response dataset;
- choosing class boundaries to maximize association with rewiring;
- redefining equivalence after seeing the transition outcome.

The classes are **focal-interaction specific**. A plant pair can be equivalent for one pollinator and decision-distinct for another.

## Minimal confirmatory model

For dyad-level data among compatibility-permitted shared species, a minimal model is:

[
Pr(	ext{link change}_{ijt}=1)
=
g^{-1}(
alpha
+eta_D D_{it}
+eta_T T_t
+eta_O O_{ijt}
+eta_E E_t
+mathbf{z}_{ijt}^{	op}oldsymbol{gamma}
+u_i+v_j+w_s
),
]

where:

- (D): frozen decision-structural boundary crossing;
- (T): taxonomic turnover;
- (O): partner opportunity / shared-pool term;
- (E): environmental change;
- (mathbf{z}): abundance, phenology, morphology and other prespecified controls;
- (u_i,v_j,w_s): focal-species, partner-species and site/network random effects as appropriate.

The coefficient (eta_D) is the primary ecological bridge. It is not interpreted as a universal causal effect unless the study design supports that claim.

For network-level data, replace the dyad outcome with a prespecified rewiring component and keep the same ordering of controls.

## Stronger matched design

When enough transitions exist, the preferred confirmatory contrast is matched or stratified:

- similar taxonomic turnover;
- similar number of shared species;
- similar shared-partner opportunity;
- similar sampling effort;
- similar abundance / encounter opportunity;
- different (D) status.

This directly targets the question: does decision-structural turnover explain differences left over after ordinary opportunity to rewire is held approximately constant?

## Null and negative-control models

The prospective test should be compared against at least four alternatives:

1. **taxonomic-only:** species turnover + shared-pool opportunity;
2. **functional-trait-only:** frozen trait distance without decision classes;
3. **environment-only:** environmental distance / anomaly;
4. **class-label null:** decision-equivalence labels permuted while preserving class-size distribution.

A useful result requires the decision-structural model to add predictive or explanatory value relative to these frozen alternatives.

## Non-circular permutation test

A direct randomization check can preserve:

- species identities;
- network degree where feasible;
- shared-partner pool;
- number and sizes of decision classes;

while permuting class membership among compatible partners.

The observed association between boundary crossing and rewiring is then compared with the distribution under structurally comparable but biologically meaningless class assignments.

This tests whether the ecological signal depends on the declared decision structure rather than merely on having grouped species into classes.

## Current Stage-1 empirical status — candidate-filter result quarantined

The raw-source audit changes the interpretation of the annual Villavicencio fallback.

The published `phenological_overlap` matrix is **not** an outcome-independent opportunity surface over all 45 × 135 candidate dyads. Across all 6,075 dyads, every one of the 827 dyads with non-zero published overlap appears as a realized interaction in at least one annual network, while none of the 5,194 never-linked dyads has positive published overlap.

Therefore the earlier annual gain result cannot be used as evidence that phenology independently filters candidate interaction formation. The arithmetic remains reproducible, but its ecological interpretation is quarantined.

The already-fitted model with phenology removed makes the consequence explicit in the sampling-consistent 2008–2011 annual scope:

- gain AUC falls to 0.5142 and relative held-out log-loss reduction versus null becomes -0.00759;
- loss AUC is 0.5995 with relative reduction +0.01307.

Thus the previously reported strong gain discrimination and gain-over-loss asymmetry are properties of the original feature surface, not established biological asymmetries in assembly versus disassembly.

Machine audit:
- `validation/villavicencio_phenology_support_leakage_v1.json`

This finding does **not** invalidate Peralta et al. (2020), which used phenology to study stability and functionality of observed interactions. It invalidates this project's reuse of that published overlap matrix as if it independently covered the full gain-risk dyad surface.

### Revised Stage-1 route

Public Figshare visitor records now provide a direct way forward. They reproduce every cell of the six published annual interaction matrices for the 45 × 135 trait subset exactly. The next Stage-1 task is therefore to reconstruct an opportunity surface from raw dated records without importing the focal dyad's own realized-link history.

The preferred observational construction is:

1. derive plant flowering/observation availability from dated plant census records;
2. derive pollinator activity from visits to **other** plants, excluding the focal plant-dyad response;
3. combine these at a prespecified site/time grain to define candidate-dyad temporal opportunity;
4. build within-year subseason transitions from the raw dates;
5. test gain and loss on held-out transitions using this leakage-controlled opportunity surface plus raw morphology.

Until that reconstruction is frozen and validated, the Villavicencio work establishes **response feasibility and source recoverability**, not a validated conventional-filter baseline.

## Evidence ladder

### Level 0 — descriptive compatibility

Observed rewiring is associated with decision-boundary crossing, but classes and outcomes are measured in the same observational dataset.

Interpretation: descriptive only.

### Level 1 — independent decision classes

Decision classes are frozen from independent assays or prior data, and predict a **detection-defensible interaction response** in held-out network transitions.

For observational visit networks, "detection-defensible" means at least one of:

- the response is an effort-standardized interaction-incidence quantity whose denominator is the repeated observation effort;
- a repeated-detection model separates latent interaction state from the observation process and the decision exposure adds information to the **state** component rather than only to detection;
- an externally validated design establishes sufficiently stable link detection for the declared response.

A predictor of raw binary link gain/loss does not meet Level 1 merely because it generalizes out of sample. It can predict the probability that an interaction is **recorded** without predicting the probability that the latent ecological interaction state changed.

Interpretation: prospective association consistent with the routeability bridge only after the response-side detection gate is met.

### Level 2 — perturbation

An experiment changes cue reliability or branch structure while holding species composition approximately fixed, and rewiring changes as predicted.

Interpretation: direct evidence that decision structure can constrain rewiring.

### Level 3 — threshold perturbation

A manipulation removes non-final versus final class representatives with the same richness decrement.

Interpretation: direct test of the equivalence-boundary threshold prediction.

The frozen V5 paper requires none of these levels for validity. They govern whether the network-rewiring extension should be promoted in a revision or follow-up paper.

## Falsification criteria

The ecological rewiring bridge should be treated as unsupported if, in a preregistered or honestly prospective test:

- (D) adds no reproducible information beyond taxonomic turnover, partner opportunity and compatibility;
- within-class and boundary-crossing turnover have indistinguishable rewiring responses across adequately powered contrasts;
- final-representative loss does not differ from comparable non-final loss in the predicted accessibility outcome;
- shuffled class labels perform as well as or better than biologically frozen decision classes;
- the declared decision exposure improves only the observation/detection component of a repeated-detection model, with no reproducible state-side information;
- the apparent boundary-crossing effect disappears when the interaction response is standardized for observation effort.

A failed empirical bridge does **not** falsify the exact target-relevant quotient theorem. It falsifies the claim that this formal structure is an important driver of rewiring in the tested ecological system.

## Promotion rule

Keep this file outside the initial V5 submission.

Promote it only if:

1. a reviewer asks how routeability could be tested in real interaction networks;
2. an empirical dataset with independently measurable decision structure is identified; or
3. a follow-up paper is explicitly framed around network rewiring.

If promoted, use the low-turnover (D=1) versus (D=0) contrast as the first empirical test. Do not broaden the initial V5 headline.

## Claim firewall

- Do not say decision-structural turnover is a third additive component of network beta diversity.
- Do not say routeability determines observed rewiring.
- Do not infer decision-equivalence classes from the same rewiring response used to test them.
- Do not call the final-representative prediction ecosystem resilience or biodiversity insurance.
- Do not treat a positive (eta_D) as causal without a design that manipulates or otherwise identifies decision structure.
- Do not promote the reserve into V5 merely because the prediction is interesting.
- Do not call a held-out predictor of raw zero/non-zero links a rewiring mechanism until sampling effort and imperfect detection are explicitly separated from latent interaction state.
- Do not treat state-versus-detection model decomposition as causal identification; it is a response-validity gate.
