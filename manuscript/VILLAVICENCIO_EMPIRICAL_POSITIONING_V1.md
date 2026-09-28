# Villavicencio empirical positioning v1

Status: **SUPERSEDED FOR GAIN-FILTER INTERPRETATION on 2026-09-28.** This file remains a post-freeze empirical revision reserve and does **not** modify the frozen Evolution Letters V5 submission surface.

Superseding machine audit:
- `validation/villavicencio_phenology_support_leakage_v1.json`

## What changed

The original annual analysis treated the published `phenological_overlap` matrix as an outcome-independent ecological opportunity filter over all 45 × 135 candidate plant-pollinator dyads. A raw-surface audit shows that assumption is false for this use.

Across all 6,075 dyads:
- 881 dyads are observed as positive links in at least one annual network;
- 827 dyads have non-zero published phenological overlap;
- **all 827 non-zero-overlap dyads belong to the 881 ever-observed links**;
- among the 5,194 dyads never observed as links, **zero** have non-zero published overlap.

Thus `P(ever linked | published overlap > 0) = 1.0` on this workbook surface. The overlap matrix cannot be used as an independent candidate-dyad predictor of link gain.

## Consequence for the earlier result

The full frozen model is still numerically reproducible:
- gain AUC = 0.8652;
- loss AUC = 0.6505.

But the strong gain result is **quarantined for ecological interpretation**.

The already-fitted drop-phenology model provides the cleanest immediate check:

- **gain:** AUC = 0.5142; relative held-out log-loss reduction versus null = **-0.00759**;
- **loss:** AUC = 0.5995; relative reduction = **+0.01307**.

For gain, removing the interaction-conditioned phenology surface collapses discrimination to approximately chance and makes proper-score performance slightly worse than the null. The earlier gain-over-loss asymmetry therefore cannot be presented as evidence that natural interaction formation is intrinsically more predictable than interaction loss.

## What remains valid

Three things survive.

1. **Response feasibility.** Repeated link gains and losses among shared species are observable in the Villavicencio data.
2. **Raw-source recovery.** Public Figshare visitor records reproduce every cell of the six annual interaction matrices for the 45 × 135 trait subset exactly.
3. **A usable route forward.** The raw dated records allow an opportunity surface to be reconstructed without using the focal dyad's realized-link history.

The historical matched-information and state-stratification analyses remain useful as diagnostics of how the published feature surface behaves, but **not as biological evidence for an eligibility gate, gain-loss process asymmetry, or routeability**.

## What this does not say about Peralta et al. (2020)

Nothing here invalidates the source paper. Peralta et al. analyzed the stability and functionality of observed interactions and reported that well-matched phenologies were associated with a stable network backbone. The problem arose only when this project reused the published overlap surface as though it were defined independently for the entire candidate-dyad gain risk set.

## Replacement empirical question

The next valid question is:

> **Can an opportunity surface reconstructed from raw dated flower observations and pollinator activity, while excluding the focal dyad response, predict link gain or loss in held-out subseason transitions?**

Only after that baseline is frozen should an independent decision-structure layer be compared against it.

## Claim ceiling

Do not use the annual full-model gain skill, the matched gain-loss asymmetry, or the zero-versus-positive published-overlap pattern as evidence for:
- ecological filtering of candidate gains;
- prospective forecasting;
- causal primacy of phenology;
- distinct assembly versus disassembly mechanisms;
- routeability or decision-equivalence structure.

The present empirical contribution is **source validation plus identification and correction of a leakage failure mode**. A new ecological result must come from the raw-record reconstruction.
