# Villavicencio phenology state stratification v1

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

## Ecological interpretation

The most defensible two-stage reading is:

> **Phenology first gates interaction eligibility through temporal co-occurrence; among established temporally compatible links, greater overlap is associated with persistence. Phenology does not determine the direction of rewiring among links that change.**

This is more precise than the earlier phrase “phenology predicts rewiring.” It also explains much of the gain/loss discrimination asymmetry without requiring a claim that assembly and disassembly have different causal machinery. The gain risk set contains thousands of zero-overlap dyads that can be screened out immediately, whereas existing links have already largely passed that eligibility filter.

## Relation to Peralta et al. (2020)

The source paper already showed that phenologically well-matched interactions form a more stable backbone and argued that phenological overlap can help predict changes in species interactions. No novelty is claimed for “phenology matters.”

The useful addition here is the directional-state decomposition plus the zero-overlap sensitivity:

- **eligibility:** zero versus positive overlap explains most gain discrimination;
- **persistence:** overlap magnitude still separates retention from loss among positive-overlap links;
- **direction:** gain versus loss among changed links is not resolved by phenology.

That decomposition tells us what the conventional ecological filter is doing and, importantly, what remains unexplained.

## Link to the routeability program

This result improves the empirical bridge without validating routeability.

The conventional layer now has a concrete role:

**temporal co-occurrence -> eligible interaction surface -> persistence gradient**

but the residual direction of change remains unresolved:

**eligible changing link -> gain or loss**

An independently measured decision layer would have to add information at that residual stage. It cannot be inferred from this phenology surface.

## Claim ceiling

Allowed:

- study-wide phenological overlap behaves primarily as a near-binary eligibility filter for candidate gains;
- among positive-overlap established links, greater overlap is associated with retention;
- phenology does not distinguish gain from loss among changing links in this annual fallback;
- the gain-discrimination advantage is largely compatible with prior filtering of candidate links.

Not allowed:

- annual phenological change caused rewiring;
- progressively greater overlap continuously predicts gain among already eligible dyads;
- zero overlap is a deterministic forbidden-link condition;
- assembly and disassembly are proven to be distinct causal processes;
- this result validates routeability.
