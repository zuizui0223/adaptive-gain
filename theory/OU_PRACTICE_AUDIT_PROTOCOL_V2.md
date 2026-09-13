# Systematic practice-audit protocol v2: trait-only OU causal attribution

## Status

**PROSPECTIVE TWO-STRATUM AUDIT RULES FROZEN.**

Freeze date: 2026-09-13.

Version 1 remains the frozen protocol for the moving-optimum evoTS/OUBM stratum. Version 2 adds a second direct stratum only after the fixed-optimum likelihood was independently shown to be an exact `v_optimum=0` corollary of the same observation-law construction. The two strata must be reported separately because the causal consequences differ.

## Stratum A — hidden moving optimum

Direct eligibility follows `OU_PRACTICE_AUDIT_PROTOCOL_V1.md`:

1. univariate evolutionary trait time series;
2. unobserved stochastic optimum / zero-mode latent state;
3. `evoTS::logL.joint.OU.BM` or proved-equivalent scalar observation law;
4. latent driver not independently observed for causal identification;
5. model used in an empirical result.

Primary mechanistic codes remain D0-D4. The key theorem consequence is that the same observed trait law admits both an exogenous stochastic-optimum representation and reciprocal latent feedback. The conventional OUBM half-life is therefore not a uniquely identified direct adaptation half-life without an additional innovation/coupling restriction.

## Stratum B — fixed optimum

A paper enters the fixed-OU direct denominator when all of the following hold:

1. an observed univariate evolutionary trait time series is analyzed;
2. the fitted model is the four-parameter joint fixed-optimum OU likelihood used by `paleoTS::logL.joint.OU`, or a mathematically demonstrated equivalent law;
3. `alpha` is estimated from the trait series rather than fixed externally;
4. the result is used empirically rather than only in simulation or software demonstration.

The fixed-OU theorem has a narrower consequence than Stratum A. The fitted `alpha` remains the model-conditional observed relaxation rate, and `log(2)/alpha` remains the expected relaxation half-life. What is not uniquely identified from the trait likelihood is attribution of the whole decay rate to a one-way direct attraction/selection coefficient, because congruent reciprocal realizations have `alpha=a+d`.

### Fixed-OU interpretation codes

- `F0_DESCRIPTIVE_RELAXATION`: alpha/half-life used only as a fitted relaxation timescale;
- `F1_ATTRACTION_OR_SELECTION`: alpha interpreted as strength of attraction, restraining force, stabilizing selection, or equivalent one-way mechanism;
- `F2_ADAPTATION_SPEED`: half-life/alpha interpreted as biological speed or time of adaptation;
- `F3_PARAMETER_TRANSLATION`: alpha is algebraically translated into population-genetic or fitness-landscape quantities;
- `F4_EXPLICIT_CAUTION`: authors explicitly state that trait-time-series likelihood alone does not uniquely identify the direct causal attraction/selection coefficient.

Codes may co-occur. In particular, F2 alone does not make the observed halfway time numerically wrong; the audit asks whether the observable decay parameter is promoted to a uniquely attributed biological mechanism.

## Common exclusions

Do not count as direct under either stratum without a separate theorem:

- phylogenetic/tree OU likelihoods;
- SURFACE or regime-shift tree models;
- multivariate OU analyses with a different observation map;
- analyses in which the relevant environmental or optimum trajectory is directly observed and used as an identifying predictor;
- nonlinear/higher-dimensional models without an exact reduction;
- generic statements about OU interpretation that do not correspond to an empirical fit.

## Evidence fields

For every eligible or near-eligible paper record:

- citation, DOI, year, system;
- software/package/function or likelihood description;
- direct stratum (`MOVING`, `FIXED`, `ADJACENT`, `EXCLUDED`);
- sample count / time span where available;
- reported alpha and/or half-life with units;
- interpretation codes and exact source location;
- whether independent ecological/genetic/fitness evidence is supplied;
- public data/code availability;
- whether this project reproduced the fit;
- whether an exact congruent reciprocal witness is attached.

## Reporting rule

Never pool Stratum A and Stratum B into a single prevalence fraction without displaying the two denominators separately. The moving-optimum result concerns causal direction of the latent adaptive landscape itself. The fixed-optimum result preserves the observed relaxation timescale and targets only one-way mechanistic attribution of its full rate.

## Promotion rule

Broad venue reassessment requires more than a theorem and a pair of examples. Before claiming a field-level practice problem, require:

1. denominator-complete or transparently bounded searches in both strata;
2. at least two independently reproduced empirical fits overall, with at least one direct fit in each stratum if both are used in the headline;
3. an explicit accounting of cases with independent biological evidence that may justify an adaptive interpretation despite trait-likelihood non-uniqueness;
4. a usable reporting replacement that separates observable relaxation, direct causal coupling, and sensitivity to hidden shared innovations.

Nature Ecology & Evolution scope should be reconsidered only after those gates close. The protocol may reveal that the correct venue is narrower; negative audit outcomes are valid results.

## Hard stops

- do not describe fixed-OU half-life as numerically unidentified;
- do not count phylogenetic OU as direct;
- do not infer that adaptive interpretations are false when external evidence exists;
- do not change direct eligibility after observing the denominator;
- do not merge this work into the frozen Theoretical Ecology finite-architecture submission.
