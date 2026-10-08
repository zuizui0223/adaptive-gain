# Source consistency and biological-semantic gate for the OU second paper (2026-10-08)

## Scope and non-reclassification rule
This is a source-level audit attached to the existing **frozen two-stratum protocol v2**. It adds neither direct studies nor a new denominator. It does not revise previously reproduced fits or claim an error in any source.

## A. Voje, Saito-Kato & Spanbauer (2024): pre-refit table label conflict
Primary article: https://academic.oup.com/jeb/article/37/12/1551/7714595 (DOI 10.1093/jeb/voae087).

- Methods and Results, "Trait dynamics in Cyclostephanos andinus": *C. andinus* favors an OU model with an optimum following a random walk. Table 1: evolving-optimum AICc **-153.573** and weight **1.000** for *C. andinus*.
- "Trait dynamics in Biwa Stephanodiscus": the Biwa lineage favors an OU model with **two fixed optima**. Table 1: two-fixed-optima AICc **-289.521**, weight **1.000** for Biwa.
- However the displayed **Table 2** labels the two-fixed-optima parameter row as **C. andinus** and the moving-optimum parameter row as **Biwa Stephanodiscus**, reversing the assignments supported by the surrounding text, Table 1, and figure captions.
- Table 2 reported moving-optimum parameter row includes z0/theta0=2.645, sigma_z^2=2152.526, sigma_theta^2=2.532, alpha=73318.010. **Do not attribute this parameter vector to a named lineage solely from Table 2's printed label** before checking the archived analysis script and data files.
- The prose and Figure 2 caption report *C. andinus* moving-optimum best-fit half-life **12 years**, but the Results explicitly state that the confidence region **does not exclude immediate adaptation (half-life 0)**. The quoted 12 years is thus a point estimate, not a narrowly measured physical timescale.
- DRYAD dataset https://doi.org/10.5061/dryad.bk3j9kdmj includes `Supplemental_files.zip` with `Data/andinus.txt` and the manuscript's `main_analyses_andinus_biwa.R` (as documented by its 2025-11-13 README). Audit environment retrieval of the ZIP was blocked (HTTP 403); therefore **independent moving empirical refit remains OPEN**.
- Gate to close: read the archived R script *and* both trait files, reconstruct the time scaling, identify whether Table 2 has only display-label inversion or whether there is a deeper parameter/time-unit mismatch, and recover published OUBM fit and log-likelihood before attaching reciprocal witness.

## B. Hunt, Bell & Travis (2008): one-way causal reading is explicit, but external evidence exists
Primary full article https://onlinelibrary.wiley.com/doi/full/10.1111/j.1558-5646.2007.00310.x (DOI 10.1111/j.1558-5646.2007.00310.x).

- Under "Microevolutionary interpretation of the OU model", alpha is explicitly construed as a *restraining force* attributable to stabilizing selection; the paper maps fitted alpha into quantitative-genetic/fitness-surface expressions under stated Gaussian and weak-selection assumptions.
- It also refers to **independent lines of indirect natural-history evidence** implicating natural selection and treats parameter-derived effective-population-size consistency as a model check.
- Coding: DIRECT_FIXED_OU; F1=YES; F2=YES; F3=YES; F4 direct-causal-nonuniqueness warning NOT FOUND in the checked sections; external evidence=INDIRECT_SUPPORT; independent model-matched numerical refit=PASS (existing receipt).
- Supported critique: the **trait likelihood alone** does not identify alpha as an entirely direct, one-way selection coefficient. Unsupported critique: "the paper's natural-selection interpretation is disproven."

## C. Lo Cascio Sætre et al. (2017): robust independent evidence must be preserved
Primary article https://www.nature.com/articles/ncomms14159 (DOI 10.1038/ncomms14159).
- Results "Time-series analysis" explicitly interpret alpha as the restraining force, half-life 1.76 years as rapid adaptation, and the OU fit as ascent toward an adaptive optimum.
- The article also reports fitness/recapture association, a body-mass survival contrast, a selection gradient, parent–offspring body-mass correlation, and consistency among independent effective population-size estimates. Authors acknowledge that heritable and environmental components cannot be definitively partitioned without direct heritability evidence.
- Coding: DIRECT_FIXED_OU; F1=YES; F2=YES; F3=NO_NOT_YET_DOCUMENTED; F4 specific hidden-state nonuniqueness NOT FOUND; external evidence=INDEPENDENT_SELECTION_GENETIC_AND_DEMOGRAPHIC_INDICATORS; own exact empirical refit=OPEN.
- Supported critique: an OU **model conditional** half-life does not itself establish that the full rate is a one-way causal selection coefficient. Unsupported critique: "selection/rapid adaptation is refuted."

## D. Hidden-state semantics: exact Gaussian congruence is not itself a biological existence proof
Let the exogenous OUBM be
  dX=alpha(Theta-X)dt+sqrt(v_x)dW1; dTheta=sqrt(v_o)dW2.
For q in (0,1), set a=q alpha and d=(1-q)alpha. The exactly congruent reciprocal coordinate is
  Y = (alpha/a) Theta - (d/a) X = (Theta-(1-q)X)/q.
Therefore Y is *explicitly a transformed latent coordinate mixing the original optimum with the observed trait*.

Consequences:
1. A mathematically admissible feedback term d(X-Y) does **not** on its own establish that Y is a realizable independently defined ecological or selective variable. Reciprocal causality is coordinate-dependent until the latent physical meaning, intervention target, and innovation structure are anchored.
2. q->0 constructions also imply increasingly extreme latent scales and shared-innovation covariance. The unbounded H_direct identified set is correct for the declared algebraic congruence family, not necessarily for a physically constrained ecological model class.
3. A scientifically defensible practice-invalidation claim must specify independently meaningful latent variables and feasible bounds, rather than merely showcasing a similarity transform.
4. An independently measured environment, fitness optimum, intervention, or justified shared-innovation restriction can invalidate members of this equivalence class.

## Verdict / promotion gate
- Exact statistical observation-law congruence: PASS in the declared Gaussian class.
- Biological reciprocal-feedback countermodel feasibility: UNPROVEN WITHOUT LATENT SEMANTIC ANCHOR.
- Published interpretation audit: partial source-supported coding, not a frequency estimate.
- Independent moving OUBM numerical reproduction: OPEN (Dryad archive ZIP not obtained in the present audit environment).
- Nature-family practice-invalidation claim: NOT QUALIFIED. Do not claim a source error from Table 2 without consulting the archived original scripts.

This note intentionally protects the theoretical observation-law result while refusing to turn a coordinate gauge into an empirically established ecological mechanism.