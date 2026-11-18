# Villavicencio phenology state stratification v1

> **SUPERSEDED INTERPRETATION — 2026-09-28.** The numerical state-stratification values below remain reproducible, but the "eligibility filter" interpretation is withdrawn. A support audit found that every non-zero value in the published phenological-overlap matrix belongs to a dyad observed as an interaction at least once over 2006–2011; none of 5,194 never-linked dyads has positive published overlap. Therefore the gain-side zero/non-zero separation is response-conditioned and cannot establish an independent ecological eligibility gate. See `validation/villavicencio_phenology_support_leakage_v1.json`. The retention-versus-loss association is retained only as a descriptive association among previously realized links, not as prospective or causal evidence.

Status: post-result ecological diagnostic for PR #65. This file does **not** modify the frozen Evolution Letters V5 submission surface.

## Main pattern

The annual fallback does not contain a year-specific phenology exposure. Dryad defines phenological overlap as the number of weeks across the **entire six-year sampling period** in which each plant-pollinator pair co-occurred. The same dyad-level matrix is therefore reused across annual transitions.

In the sampling-consistent 2008-2011 primary scope, pooled median overlap is:

- stable absent: 0
- gain: 12
- loss: 13
- retained: 20

Using the raw overlap value as a ranker gives:

- gain vs stable absence AUC = **0.9055**;
- retained vs loss AUC = **0.6613**;
- gain vs loss among changed dyads AUC = **0.4907**.

At first glance this looks like a strong continuous phenology effect on link formation. The zero-overlap audit shows that interpretation is too strong.

## The gain signal is almost entirely a zero/nonzero gate

Zero overlap occurs in:

- **87.2%** of stable absences;
- **6.3%** of gains;
- **5.2%** of losses;
- **2.0%** of retained links.

When all zero-overlap dyads are removed, phenological-overlap magnitude no longer ranks gains against stable absences:

- pooled positive-overlap-only AUC = **0.5058**;
- primary folds = **0.4643, 0.4570, 0.5678**.

So the large 0.9055 gain AUC is not evidence that progressively greater overlap continuously increases the chance that an eligible absent link will form. It is dominated by the coarse distinction between **no measured temporal overlap** and **some measured temporal overlap**.

This is not an absolute structural zero: 27 of 430 primary gains have overlap = 0 in the study-wide matrix. The safest language is therefore **near-binary eligibility filter**, not deterministic forbidden-link rule.

## Persistence is different

For established links, the signal does not disappear after zero-overlap dyads are excluded.

High overlap predicts retention rather than loss with:

- pooled positive-overlap-only AUC = **0.6568**;
- primary folds = **0.6593, 0.6598, 0.6563**.

Thus overlap magnitude carries moderate information about **persistence** once an interaction already exists.

By contrast, among changed dyads, phenology is nearly useless for distinguishing whether the change is a gain or a loss:

- pooled gain-vs-loss AUC = **0.4907**;
- primary folds = **0.4466, 0.4970, 0.5111**.

## Current interpretation — historical diagnostic only

The numerical state-stratification calculations above remain reproducible, but
their original ecological reading is superseded.

The published `phenological_overlap` matrix is response-conditioned for this
candidate-dyad use: non-zero support is nested inside dyads realized as links
at least once over the study. The strong gain-versus-stable-absence separation
therefore cannot establish an independent eligibility gate.

Subsequent raw-census analyses further show that binary link gain/loss is
materially effort- and detection-sensitive. Accordingly, the numerical
state-stratification surface should now be read only as a diagnostic of how the
published feature matrix relates to the observed network states from which its
support was constructed.

The positive-overlap retention-versus-loss association may be reported only as
a **descriptive association among previously realized links**. It is not a
prospective filter, a latent-state result, or a causal persistence mechanism.

## Relation to the routeability program

This historical diagnostic does **not** improve the evidential routeability
bridge.

The valid empirical sequence is now:

```text
published-overlap diagnostic
    -> support-leakage quarantine
    -> focal-response-excluded raw opportunity
    -> sampling-effort audit
    -> effort-standardized census incidence
    -> repeated-detection state-versus-observation decomposition
    -> observational stop rule
```

The final claim resolution is frozen in:

- `validation/villavicencio_rewiring_claim_resolution_v1.json`;
- `validation/villavicencio_subseason_effort_audit_result_v1.json`;
- `validation/villavicencio_latent_opportunity_decomposition_result_v1.json`;
- `validation/villavicencio_detection_overdispersion_result_v1.json`.

An independent decision layer must be tested on a detection-defensible response
or in the controlled experiment; it cannot be recovered from this published
phenology surface.

## Claim ceiling

Allowed:

- report the historical numerical stratification values as reproducible;
- state that the published feature surface strongly separates some observed
  binary network states;
- report the positive-overlap retention-versus-loss pattern as descriptive
  among previously realized links;
- explain why the original eligibility-filter interpretation was withdrawn.

Not allowed:

- call the published overlap surface an independent candidate-gain eligibility
  filter;
- use the 0.9055 gain-versus-absence AUC as ecological-filter evidence;
- infer annual phenological change caused link gain/loss;
- infer a latent persistence mechanism from the retention association;
- call observed gain/loss ecological rewiring;
- use this diagnostic as evidence for decision equivalence or routeability.

