# Published-fit witness: Voje et al. (2024) *Cyclostephanos andinus*

## Status

**PUBLISHED-FIT ANCHOR ESTABLISHED; INDEPENDENT RAW-DATA REFIT REMAINS OPEN.**

This note attaches the exact evoTS moving-optimum congruence theorem to a real published empirical fit without pretending that the archived data have already been independently re-optimized in this repository.

## Published target

Voje, Saito-Kato & Spanbauer (2024), *Journal of Evolutionary Biology*, fit evolutionary time-series models to the fossil diatom *Cyclostephanos andinus*. The reported series contains 266 samples. The best-supported candidate is the four-parameter Ornstein-Uhlenbeck model whose unobserved optimum follows an unbiased random walk, with reported

- `AICc = -153.573`;
- `AICc weight = 1.000` within the candidate set;
- model-conditional half-life equivalent to **12 years**;
- stationary trait variance approximately **0.015 log(µm)^2**.

The paper then interprets the result biologically as rapid trait adaptation tracking a quickly and randomly moving optimum.

Primary article: DOI `10.1093/jeb/voae087`.

Archived data and scripts: Dryad DOI `10.5061/dryad.bk3j9kdmj` (published 2025-11-13). The archive identifies `Data/andinus.txt` and `R scripts/main_analyses_andinus_biwa.R` as the files required for the main *C. andinus* analysis.

## Exact source-model contract

The theorem in `EVOTS_MOVING_OPTIMUM_CONGRUENCE.md` was derived against the actual evoTS implementation at commit

`84c201258e35776b7e1ad87fd5563f0c68fceed1`.

`R/logL.joint.OU.BM.R` constructs the complete multivariate-normal likelihood of the observed sample means using the OUBM mean/covariance and adds `vv/nn` to the covariance diagonal. `R/opt.joint.OUBM.R` uses four parameters when the ancestral trait is constrained to start at the optimum. Its output passes `logL`, `K`, and `n` to `paleoTS::IC(..., method="AICc")`.

Therefore the theoretical congruence is matched to the same statistical observation model used by the published analysis, rather than to a generic OU caricature.

## Published-summary likelihood anchor

Under the standard AICc definition

`AICc = -2 logL + 2K + 2K(K+1)/(n-K-1)`,

using `n=266`, `K=4`, and the published `AICc=-153.573` gives

`logL = 80.86312835249042`.

`adaptive_gain/voje_2024_published_fit.py` and its tests freeze this arithmetic as a transparent published-summary witness. This is **not** an independent reconstruction of the optimizer or preprocessing.

## Exact causal consequence for the published fit

For any reciprocal response fraction `0<q<1`, the congruence construction leaves the complete observed-trait Gaussian law unchanged while decomposing the fitted relaxation rate as

`alpha = a + d`, with `a=q alpha`.

Hence the direct trait-response half-life is

`H_direct = H_OU / q`.

Taking the paper's reported `H_OU = 12 years`:

| Reciprocal member | Direct trait-response half-life | Observed-trait likelihood |
| --- | ---: | --- |
| `q=1/2` | 24 years | exactly unchanged |
| `q=1/4` | 48 years | exactly unchanged |
| `q=1/10` | 120 years | exactly unchanged |
| `q -> 0+` | unbounded | exactly unchanged |

Thus, **conditional on the published OUBM observation law**, the 12-year number is not uniquely identified as the mechanistic speed at which the observed trait responds to an exogenous optimum. It is the lower endpoint of a causal identified set unless an additional restriction on hidden shared innovations is justified.

This does not say the published statistical fit is poor, nor that a moving optimum is impossible. It says the trait series alone does not uniquely attribute the fitted relaxation scale to that one-way mechanism within the exact congruence class.

## Important source-table/time-scaling gate

The article states that the full time interval was scaled to unit length for fitting and separately reports the half-life as 12 years. The HTML rendering of Table 2 exposes parameter values whose naive conversion should **not** be treated as an independent verification of the 12-year transformation until the archived R script is executed exactly. The source table also renders a suspicious dataset label around the moving-optimum row in the machine-readable HTML while the surrounding Results unambiguously assign the continuously moving optimum to *C. andinus*.

Accordingly:

- do **not** call the published half-life a numerical error;
- do **not** relabel the Table 2 row from scraped HTML alone;
- reproduce the original time scaling and transformation from `main_analyses_andinus_biwa.R` before making any discrepancy claim.

## Independent-refit gate

Promotion from `published-fit witness` to `independent empirical reproduction` requires all of the following:

1. obtain the archived `andinus.txt` and `main_analyses_andinus_biwa.R`;
2. reproduce the exact construction of the paleoTS object and unit-time scaling;
3. run the same evoTS OUBM fitting contract, including ancestral-state convention and variance pooling;
4. match the reported OUBM AICc to a declared tolerance;
5. match the fitted parameter vector or explain any version-dependent difference;
6. reproduce the paper's 12-year and 0.015 transformations from the fitted scale;
7. attach at least three reciprocal `q` witnesses and verify identical mean/covariance/log-likelihood numerically on the empirical observation times.

Until these steps are complete, `independent_data_refit = OPEN`.

## What has changed scientifically

Before this anchor, the exact theorem had a plausible published target. After this anchor, it has a named empirical inference whose reported mechanistic half-life admits an exact continuum of observationally congruent causal decompositions. The remaining empirical-reproduction gate is important for auditability, but it is no longer necessary to argue that the theorem points at a real inferential practice.
