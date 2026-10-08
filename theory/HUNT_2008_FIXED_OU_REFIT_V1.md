# Hunt et al. (2008) fixed-OU empirical refit v1

## Status

**INDEPENDENT NUMERICAL REFIT PASS, WITH SOURCE-VERSION CAVEAT.**

This receipt closes the first fixed-optimum empirical-reproduction gate for the trait-only OU causal-identifiability paper. The result was produced independently in this repository's audit environment from the empirical `dorsal.spines` data bundled with `paleoTS`, using a pinned current source revision and preprocessing matched as closely as possible to Hunt, Bell & Travis (2008).

It is not claimed to be a bit-for-bit reconstruction of the authors' 2008 software environment.

## Source contract

- empirical system: fossil threespine stickleback dorsal-spine trait series;
- paper: Hunt G, Bell MA, Travis MP. 2008. *Evolution toward a new adaptive optimum: phenotypic evolution in a fossil stickleback lineage*. Evolution 62:700-710;
- DOI: `10.1111/j.1558-5646.2007.00310.x`;
- package source: `cran/paleoTS`;
- pinned package commit: `6fbc4f6fa35ef2c7de73e11b9f6dda8ba73e7bc6`;
- package version: `0.6.2`;
- R version used by the audit: `4.4.1`;
- temporary audit run: GitHub Actions run `34750002693`, job `103704711585`;
- temporary workflow was removed after the result was captured.

The package documents `dorsal.spines` as the Hunt/Bell fossil stickleback series and retains the current Joint-OU fitting workflow.

## Two refits were deliberately separated

### A. Current paleoTS vignette recipe

The current package vignette uses:

1. retain measured populations (`nn > 0`);
2. retain the post-invasion segment (`tt > 4.4` Kyr);
3. reset time;
4. replace low-N variances using `pool.var(..., minN=5)`;
5. fit fixed OU with the Joint likelihood.

Pinned-source result:

- `N = 60`;
- `anc = 1.3599167285866207`;
- `vstep = 0.004074958359653364` per Kyr;
- `theta = 0.7851171553920003`;
- `alpha = 0.4030734201553071` per Kyr;
- `logL = 93.44169282389461`;
- `AICc = -178.1561129205165`;
- half-life `log(2)/alpha = 1.7196548963533014` Kyr;
- with 2 years per generation, `1 Kyr = 500 generations`, giving `859.8274481766507` generations.

This is already close to the published dorsal-spine half-life of 853 generations, but it uses the current vignette's low-N pooling convention rather than the original paper's preprocessing.

### B. Paper-matched preprocessing

The second audit follows the 2008 Methods more closely:

1. use the post-invasion dorsal-spine sequence (`tt >= 4.5` Kyr);
2. omit samples with `n < 5`;
3. reset time;
4. replace the single retained zero within-sample variance by the pooled within-sample variance;
5. convert Kyr to generations using 2 years per generation, so `1 Kyr = 500 generations`;
6. fit the fixed-optimum OU model with the Joint likelihood and without further variance pooling.

Audit result:

- `N = 57` populations;
- zero within-sample variances replaced: `1`;
- pooled variance used for that replacement: `0.04073338588884509`;
- empirical schedule: `0` to `7375` generations;
- parameter order: `(anc, vstep, theta, alpha)`;
- `anc = 1.3608894391782618`;
- `vstep = 7.043556217523495e-06` per generation;
- `theta = 0.7927588486238825`;
- `alpha = 0.0008202984275902434` per generation;
- `logL = 94.96063917217212`;
- `AICc = -181.15204757511347`;
- reproduced half-life = `844.9939159290783` generations;
- published dorsal-spine half-life = `853` generations;
- absolute difference = `8.006084070921702` generations;
- relative difference = `0.009385796097211843` (`0.94%`).

We therefore classify the empirical fixed-OU fit as independently numerically reproduced to within 1% in the biologically central reported half-life under paper-matched preprocessing using the pinned current package implementation.

The residual discrepancy is not treated as an error in either source. The original 2008 optimization code/environment is not the current 2024 `paleoTS` source, so optimizer, initialization, or implementation changes can account for a small difference.

## Exact reciprocal witness on the empirical schedule

Using the paper-matched fitted law and `q = 1/2`, define

`a = q alpha`, `d = (1-q) alpha`.

The exact reciprocal realization gives:

- `a = 0.0004101492137951217` per generation;
- `d = 0.0004101492137951217` per generation;
- hidden initial state `Y0 = 0.22462825806950307`;
- observed relaxation half-life = `844.9939159290783` generations;
- direct-coupling half-life `log(2)/a = 1689.9878318581566` generations.

On all 57 empirical observation times, including the same sampling-error diagonal:

- maximum absolute mean difference = `2.220446049250313e-16`;
- maximum absolute covariance difference = `3.469446951953614e-18`.

The audit imposed hard tolerances of `1e-10` for the mean and `1e-9` for covariance and passed both.

Thus the fitted trait likelihood cannot distinguish the conventional one-way fixed-peak representation from this reciprocal realization even on the actual empirical sampling schedule.

## Interpretation boundary

This result does **not** invalidate the approximately 845-853-generation observed relaxation timescale. That quantity is retained as the fitted OU decay timescale.

What changes is causal attribution. The same empirical likelihood is compatible with a reciprocal realization in which only half of the fitted decay rate is the direct trait-to-latent attraction coefficient, yielding a direct-coupling half-life near 1690 generations. Other `q` values generate the full congruence family.

The empirical refit therefore demonstrates on a real published system exactly the paper's distinction between:

- identifiable/model-conditional **observed relaxation**, and
- non-unique **one-way mechanistic attribution** of the entire fitted `alpha`.

## Gate consequence

- fixed-optimum independent numerical refits: `1`;
- fixed-optimum empirical-time reciprocal witnesses after refit: `1`;
- moving-optimum independent numerical refits: `0`.

The dominant remaining empirical gate is now the Voje et al. (2024) moving-optimum OUBM raw-data refit.