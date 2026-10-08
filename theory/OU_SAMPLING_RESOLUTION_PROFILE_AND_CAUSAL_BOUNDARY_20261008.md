# Sampling-resolution saturation and half-life profile gate — 2026-10-08

## Direct result, not a new theorem of statistical inference

The *Cyclostephanos andinus* PETS-mirror series (tsID582) has **266 sample times** across 309,415.25 years. Consecutive sample gaps in this same series range from **28.232 years** to **25,524.031 years**, with median **490.28 years**. The fitted OUBM model-conditional half-life is about **12.009 years**.

This implies the direct trait relaxation process under the *fitted model* is often faster than the temporal resolution. A point estimate of 12 years does not imply that the fossil data can discriminate 12 years from much faster half-lives. Voje et al. (2024) explicitly acknowledge that the confidence region does not exclude immediate adaptation, so the *existence* of that uncertainty is prior art, not this project's novel result.

## Independent Gaussian likelihood profiling

The pinned PETS mirror has n=266, first trait mean 2.644626001 (already in source log size units), pooled within-sample variance 0.15972760449. For fixed half-life `H`, set
`alpha = log(2)*309415.25/H` on the unit-length source time interval. Maximize the independent two-state Gaussian Kalman observation likelihood over ancestral mean, stationary trait variance `S=v_trait/(2 alpha)`, and moving-optimum diffusion `v_optimum`.

| Fixed half-life (yr) | profile logL minus grid maximum |
|---:|---:|
| 0.01 | -0.03344 |
| 0.1 | -0.03342 |
| 1 | -0.03321 |
| 3 | -0.03271 |
| 10 | -0.00413 |
| 12 | 0 |
| 20 | -0.07387 |
| 24 | -0.15904 |
| 30 | -0.32493 |
| 48 | -0.93268 |
| 60 | -1.35623 |
| 80 | -2.05561 |
| 100 | -2.74833 |

The near-zero half-life edge is almost as likely as the grid optimum. This is a **profile likelihood grid, not a validated frequentist confidence interval**: a formal cutoff requires calibration near the non-regular rate-at-infinity boundary, and these grid values do not account for uncertainty in the source mapping against authors' Dryad archive.

The independent published-summary OUBM reproduction from the PETS mirror (AICc -153.657 vs published -153.573 and H=12.009 yrs) remains distinct from this inferential sensitivity result.

## Analytic saturation mechanism

For distinct fixed positive sampling times, the exact moving-optimum Gaussian covariance has limit as `alpha->infinity` with `S=v_trait/(2 alpha)` fixed:

- Off diagonal `Cov(X_s,X_t) -> v_optimum * min(s,t)` (Brownian latent optimum).
- On a diagonal at t>0, `Var(X_t) -> v_optimum*t+S`.
- At t=0, the initial X is fixed and the process variance remains zero.
- Additional known sample-mean measurement variance stays on the diagonal.

Thus at the actual finite set of observation times the rapid OU becomes observationally close to a Brownian random walk with an extra nugget process variance S. The fast relaxation parameter no longer appreciably changes the observation law. This is a standard sampling-resolution and parameter-boundary phenomenon; neither the limit nor generic time-scale nonidentifiability is claimed as new.

Code: `adaptive_gain/ou_sampling_saturation.py`, `tests/test_ou_sampling_saturation.py`, `scripts/profile_voje_2024_pets_half_life.py`.

## The crucial inferential separation

**Layer A — within fitted one-way OU:** A finite optimum MLE exists, but very fast alternatives are weakly distinguishable from the observed fossil means. This is statistical resolution uncertainty; the paper already acknowledges it.

**Layer B — broader hidden-state causal representations:** Even if the fitted observation law were known without statistical error, a coordinate-mixing state-space realization gives the exact same trait law while partitioning observed `alpha=a+d`. This is structural but physical interpretation of the transformed Y is *not established*.

Neither layer alone proves that a published ecological/adaptation mechanism is biologically false. Layer B may reduce to a state-coordinate gauge unless Y is independently physically anchored. Nature-family practice invalidation remains unqualified without a concrete independently meaningful ecological countermodel or external causal evidence.

## Exact semantic obligation

In the current reciprocal family `Y=(Theta-(1-q)X)/q`. Therefore `Y` is not automatically the *same* adaptive optimum `Theta` inferred under the original model. The intervention `do(Y=constant)` is not the same intervention as `do(Theta=constant)`. The ratio `H_direct/H_OU=1/q` reflects this distinction: it is a coordinate-dependent intervention response unless the physical coordinate is independently fixed.

A defensible mechanism-level study must declare what Y measures and how an external dataset or experiment anchors it. Further algebra without that anchor does not constitute evidence of a new ecological mechanism.

### Decisions
- Keep the first finite-architecture paper isolated.
- Keep the second-paper PR in draft.
- Do not count the previous 125/630 model-class frequency as a mechanistic overinterpretation count.
- Next empirical target: independently anchored environmental/fitness optimum time series with explicit process innovation covariance or credible perturbation, **or** an empirically defensible bound excluding the extreme correlations needed by the reciprocal witness.
