# Villavicencio gain-loss asymmetry note v1

Status: post-result robustness note for PR #65. This file does **not** modify the frozen Evolution Letters V5 submission surface.

## What survives the audit

The annual Villavicencio fallback has sharply different event prevalences in its two risk sets, so the pooled relative log-loss reductions (gain 0.2257; loss 0.0563) must not be compared as if they were on a common prevalence scale.

A prevalence-insensitive ranking diagnostic gives a narrower but cleaner result. In the sampling-consistent 2008-2011 primary scope, ROC AUC is higher for gain than loss in every held-out transition:

| held-out transition | gain AUC | loss AUC | gain - loss |
| --- | ---: | ---: | ---: |
| 2008->2009 | 0.8283 | 0.6542 | +0.1741 |
| 2009->2010 | 0.8918 | 0.7000 | +0.1918 |
| 2010->2011 | 0.9172 | 0.6113 | +0.3059 |

The unweighted mean fold difference is +0.2239. The direction remains 4/4 in the 2007-2011 sensitivity and 5/5 in the full 2006-2011 annual sensitivity.

This supports one specific ecological statement:

> **The frozen conventional filters rank candidate link gains more cleanly than they rank candidate link losses across these annual transitions.**

It does **not** support the broader statement that gains are universally “more predictable” than losses. Brier skill favors gain in only 1/3 primary folds, so the asymmetry is a discrimination result, not a metric-general forecasting law.

## What phenology means here

Phenological overlap remains the only prespecified predictor block whose removal worsens held-out log-loss for both endpoints in every primary fold. That is a strong replication of a conventional ecological filter.

However, the annual fallback joins a single dyad-level phenological-overlap matrix to each transition. It therefore does not estimate the effect of **year-to-year phenological change** on rewiring.

The defensible interpretation is:

> **Pairs with greater underlying temporal overlap are more consistently distinguishable as candidates for annual link formation or persistence/loss.**

Do not rewrite this as “phenological shifts caused rewiring.”

## Relation to the source paper

Peralta et al. (2020) already reported that well-matched phenologies were associated with more stable interactions and argued that phenological overlap could help predict changes in species interactions. The present reanalysis therefore does not claim novelty for “phenology matters.”

The additional information in PR #65 is narrower:

1. gains and losses are modeled as separate risk sets;
2. prediction is evaluated on held-out annual transitions rather than fitted association alone;
3. phenology is tested by effect-blind block ablation against abundance and raw morphology;
4. the gain endpoint shows consistently stronger held-out ranking discrimination than the loss endpoint.

The first three strengthen the empirical bridge; the fourth is a post-hoc ecological pattern that requires independent replication before promotion as a general assembly/disassembly hypothesis.

## Routeability boundary

None of these results identify routeability. They do not contain independently measured decision-equivalence classes, cue hierarchy, contingent query cost, or a manipulated routing architecture.

The correct evidence ladder remains:

**conventional ecological filters -> gain/loss predictive asymmetry -> independent decision layer -> direct routeability manipulation**

The first two are now supported in the Villavicencio fallback. The latter two are not supplied by these annual network data.

## Claim ceiling

Allowed:

- phenological overlap is a reproducible held-out predictive filter for both annual gain and loss;
- conventional filters show consistently higher ROC discrimination for gain than loss in the sampled annual transitions;
- this asymmetry is a candidate ecological hypothesis for independent testing.

Not allowed:

- phenology is the causal primary driver of rewiring;
- year-to-year phenological shifts caused the observed link changes;
- assembly and disassembly are proven to be different causal processes;
- the Villavicencio analysis validates routeability;
- the gain/loss asymmetry is a prospectively specified confirmatory result.
