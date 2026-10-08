# Systematic practice-audit protocol v1: mechanistic interpretation of moving-optimum OU fits

## Status

**PROSPECTIVE AUDIT RULES FROZEN BEFORE EXPANDING THE SEED SET.**

Freeze date: 2026-09-13.

This protocol prevents the second-paper impact claim from being defined after seeing which papers are convenient examples. It separates the exact theorem target from broader OU practice that is biologically relevant but not yet covered by the same likelihood proof.

## Primary question

Among empirical studies that fit a trait-only moving-optimum OU model in the exact evoTS/OUBM observation class, how often is the fitted relaxation parameter or half-life interpreted as a mechanistic adaptation speed and/or the hidden stochastic component interpreted as an exogenously moving adaptive optimum without an independently observed latent driver?

## Direct-theorem eligibility

A paper enters the **direct target denominator** only if all of the following are satisfied:

1. an observed univariate evolutionary trait time series is analyzed;
2. the candidate model contains an unobserved stochastic optimum or equivalent zero-mode latent state;
3. the likelihood is `evoTS::logL.joint.OU.BM` or a mathematically demonstrated equivalent observation law;
4. the optimum/latent driver is not independently observed as a time series used to identify the causal direction;
5. the paper reports enough model information to establish that the relevant fit was actually used in an empirical result.

If likelihood equivalence is uncertain, classify the paper `ADJACENT_UNPROVEN`, not direct.

## Exclusions from the direct denominator

Do not count the following as directly invalidated or qualified by the present theorem without a separate derivation:

- phylogenetic/tree OU likelihoods;
- SURFACE-style regime-shift models on trees;
- multivariate OU models whose observation map differs from the two-state scalar theorem;
- fixed-optimum OU fits;
- environmental predictor models in which the relevant latent driver is directly observed;
- nonlinear or higher-dimensional state-space models not reduced exactly to the proven observation class.

These may be recorded as **broad-practice context** only.

## Claim coding for each direct target

Code the strongest supported interpretation in the article, supplement, or official analysis documentation:

- `D0_DESCRIPTIVE`: alpha/half-life used only as a model-conditional descriptive timescale;
- `D1_ADAPTATION_SPEED`: alpha or half-life interpreted as the biological speed/time of adaptation toward an optimum;
- `D2_EXOGENOUS_OPTIMUM`: the hidden stochastic state is interpreted as movement of the adaptive landscape/optimum in a causal or mechanistic sense;
- `D3_BOTH`: both D1 and D2 are present;
- `D4_EXPLICIT_CAUTION`: authors explicitly state that the fitted trait-only law does not identify the causal origin/direction of the latent state.

A paper may carry `D4_EXPLICIT_CAUTION` alongside a descriptive category, but a caution that only says "models are simplified" is insufficient.

## Evidence fields

For every eligible or near-eligible paper, record:

- citation and DOI;
- publication year;
- organism/system;
- software/package and version if available;
- exact model/function name;
- whether trait data alone are observed;
- whether latent optimum/environment is independently measured;
- sample count/time-series length;
- reported alpha/half-life and units if present;
- exact text location supporting the coding;
- direct-target class (`DIRECT`, `ADJACENT_UNPROVEN`, `EXCLUDED`);
- claim code D0-D4;
- whether data/code are publicly reproducible;
- whether an exact reciprocal witness has been attached.

## Search strategy

The search ledger must preserve literal queries and dates. At minimum use combinations of:

- `evoTS` AND (`moving optimum` OR `evolving optimum` OR `OUBM`);
- `logL.joint.OU.BM`;
- `opt.joint.OUBM`;
- `"half-life"` AND `evoTS`;
- `"rate of adaptation"` AND (`moving optimum` OR `evolving optimum`) AND fossil/time series;
- forward citations of Hansen, Pienaar & Orzack (2008) when they use a trait-only stochastic-optimum fit;
- forward citations of Voje et al. (2024) and the evoTS package paper/documentation.

Search bibliographic databases and general web indexing separately. Deduplicate by DOI/title.

## Primary audit outcomes

Let `N_direct` be the number of direct-theorem empirical targets.

Report:

1. `N_direct`;
2. number and fraction with D1, D2, or D3 mechanistic interpretation;
3. number with D4 explicit causal-identification caution;
4. number with public data/code permitting exact reproduction;
5. number for which the present project independently reproduces the fitted law and attaches reciprocal congruent witnesses.

Do not treat the seed examples as denominator-complete.

## Seed handling

Voje et al. (2024) is a pre-existing direct positive discovered before this protocol. It remains in the ledger but cannot change the inclusion rules.

Phylogenetic examples already listed in `OU_HALFLIFE_PRACTICE_AUDIT_V1.md` remain broad-practice witnesses only. They must not inflate `N_direct` and must not be described as overturned by the current theorem.

## Promotion rules

- `N_direct = 1` with a fully reproduced fit: strong case-study/conceptual methods result, not a field-wide invalidation.
- several independent direct applications with the same mechanistic interpretation: supports a broader evolutionary-methods claim.
- a systematic audit showing that the interpretation is recurrent, plus exact empirical reproductions and the common-shock sensitivity replacement: reassess broad ecology/evolution venue scope.
- Nature Ecology & Evolution framing requires evidence that the issue materially changes a nontrivial body of published evolutionary inference, not merely that the theorem is mathematically exact.

## Hard stops

- no counting tree OU papers as direct until a tree theorem exists;
- no post-hoc broadening of `DIRECT` to increase the denominator or impact;
- no treating absence of an explicit caveat as proof that authors made a causal claim;
- no quoting abstracts or prose without preserving source location in the final ledger;
- no claiming a paper's numerical result is wrong when the theorem only establishes causal non-uniqueness.
