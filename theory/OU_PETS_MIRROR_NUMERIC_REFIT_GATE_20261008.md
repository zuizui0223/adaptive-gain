# Empirical gate update: independent PETS-mirror moving OUBM refit (2026-10-08)

## What changed
The previously open *moving* empirical route now has an **independent numerical refit of a public PETS mirror**, with a **separate remaining archival-provenance gate**. This does not overwrite `ou_second_paper_gate_v4.json` or claim a byte-verified original Dryad refit.

Source: `VildeBruhn/rate_time@718d603c49ae640e34a5c36c93bcd8ba36d1e389`, `empirical_data/timeseries.txt`, `tsID=582`. These are 266 *Cyclostephanos andinus* mean observations over 0.30941525 Myr. The first trait mean is 2.644626001, already on the log-micrometre scale used in the article; **do not apply `ln.paleoTS` to the PETS mirror again.**

The independent calculation implemented the two-state Gaussian Kalman likelihood equivalent to the published moving-optimum OUBM (Brownian optimum), with source innovation variances independent, ancestral state equal to the initial optimum, time normalized to [0,1], and `(sum (N-1)vv/sum(N-1))/N_i` as sampling-error variance.

## Refit result

| Quantity | Published | Independent PETS-mirror |
|---|---:|---:|
| n | 266 | 266 |
| AICc | -153.573 | **-153.65736454** |
| Half-life | about 12 yr | **12.00877258 yr** |
| Gaussian log-likelihood | inferred from reported AICc: 80.86312835 | **80.90531062** |

Independent maximum-likelihood parameters on normalized interval:
`anc=2.6519340142`, `vstep_trait=527.5416515`, `alpha=17859.4695403`, `vstep_optimum=2.5206495951`.

The difference in AICc from the published number is only **-0.0844**, not a published-source error. On exactly the same empirical schedule and fitted parameter vector, independent covariance-matrix/Cholesky likelihood was `80.90531062232341` against Kalman `80.90531062232422`, absolute difference **8.1e-13**. This is a strong independent numerical implementation check.

The unpooled fit (`AICc=-157.1969`, half-life 11.0262 years) is retained strictly as a preprocessing sensitivity check; it is **not** substituted for the pooled primary reproduction.

## Updated hierarchy of proof

1. **Exact stochastic observation-law congruence:** analytic, unchanged (pass).
2. **Independent likelihood reproducing published moving-OUBM numeric summary:** pass on PETS **mirror** (new).
3. **Independent likelihood implementation check:** pass, Kalman versus dense Gaussian.
4. **Re-execute authors' own Dryad archived files and exact R workflow:** **open**, file acquisition returns HTTP 403 / unauthenticated API 401.
5. **Reconcile Table 2 labels and original model-to-taxon parameter mapping:** open.
6. **Establish that the transformed latent coordinate represents a physically distinct ecological mechanism:** open; mere similarity/gauge transform is insufficient.
7. **Denominator-defensible audit of published mechanistic attributions:** open.
8. **NEE practice-invalidation claim:** not qualified yet.

The original paper's model support and relaxation timescale are **not invalidated** by this result. The unresolved issue is exclusive *causal attribution* of the decay coefficient to one-way adaptation when only the trait is observed.

## Reproduction
- Independent script: `scripts/refit_voje_2024_pets_ou.py` (numpy/scipy; fixed source commit). It should also be executed in a clean environment before upgrading its own test gate.
- Frozen numeric receipt: `validation/ou_pets_mirror_independent_refit_20261008_v1.json`.
- Repaired temporary R workflow: `.github/workflows/temporary_voje_2024_dryad_discovery.yml`, with optional plotly dependency isolated and PETS double-log avoided. Its GitHub Actions run status is separate from the independently evaluated numerical comparison.
