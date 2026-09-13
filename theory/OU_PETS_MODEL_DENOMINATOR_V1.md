# PETS empirical model-denominator audit v1

## Status

**DIRECT SAVED-OBJECT AUDIT COMPLETE.**

Date: 2026-09-13.

This audit answers a narrower question than the literature interpretation audit:

> In a broad compiled set of empirical phenotypic time series analyzed with the same evoTS model family, how often is a fixed- or moving-optimum OU model the minimum-AICc model among the nine fitted candidates?

It does **not** measure how often authors make a mechanistic adaptation claim.

## Source

Bruhn Kinneberg et al. (2026), *Rate–time scaling in phenotypic evolution: Limitations of current models in capturing temporal dynamics*, analyzed 643 empirical phenotypic time series from PETS with nine evoTS models.

The public analysis repository is:

- `VildeBruhn/rate_time`;
- audited source SHA: `a08b97d2153c797f4825b9d03ec9361ca9921caf`;
- saved fit object: `empirical_data/model_test.Rdata`;
- analysis source: `empirical_data/empirical.R`.

The model order was independently pinned to `evoTS::fit.all.univariate` at evoTS commit `84c201258e35776b7e1ad87fd5563f0c68fceed1`:

1. GRW;
2. URW;
3. Stasis;
4. Strict Stasis;
5. Decelerated evolution;
6. Accelerated evolution;
7. fixed-optimum OU;
8. moving-optimum OUBM, ancestral state fixed at the optimum;
9. moving-optimum OUBM, ancestral optimum free.

## Audit execution

A temporary GitHub Actions job downloaded the public saved R object, loaded it under R 4.4.1, and computed `which.min(AICc)` for every saved model-comparison entry.

Audit run:
- workflow run `34741902818`;
- job `103682892068`;
- audited adaptive-gain commit `132e8e9f3b6e8d56d4540da84e9b71d2651f5a9b`.

The temporary workflow was removed immediately after the result was recovered; only this durable receipt remains on the research branch.

## Exact saved-object denominator

`model_test.Rdata` contains **630** model-comparison entries, and all 630 contain a valid minimum AICc among the nine models.

| Best AICc model | Count | Percent of 630 |
|---|---:|---:|
| GRW | 50 | 7.94% |
| URW | 164 | 26.03% |
| Stasis | 135 | 21.43% |
| Strict Stasis | 114 | 18.10% |
| Decelerated evolution | 20 | 3.17% |
| Accelerated evolution | 22 | 3.49% |
| **Fixed OU** | **56** | **8.89%** |
| **OUBM, ancestor = optimum** | **30** | **4.76%** |
| **OUBM, free ancestral optimum** | **39** | **6.19%** |

Therefore:

- **any OU model best:** `125/630 = 19.84%`;
- **fixed OU best:** `56/630 = 8.89%`;
- **moving OUBM best:** `69/630 = 10.95%`.

The moving total is `30 + 39 = 69`.

## Why this matters

This closes an important scope question. The exact likelihood classes targeted by the present causal-congruence work are not confined to one hand-picked fossil example. In this large saved empirical comparison object, an OU likelihood is the minimum-AICc candidate for about one fifth of successfully represented series, with both fixed and moving-optimum classes contributing materially.

That establishes **model-class prevalence**, not **mechanistic-interpretation prevalence**. A time series whose best AICc model is OU need not have been published with claims about stabilizing selection, adaptation speed, or an exogenous moving optimum. Those claims remain the separate prospective practice-audit numerator.

## 643 versus 630 scope boundary

The associated paper describes a complete empirical collection of **643** time series. The public saved `model_test` object audited here contains **630** entries.

Do not silently use 643 as the denominator for the counts above. The present exact denominator is 630 saved successful model comparisons.

The paper also reports 163 time series in its URW relative-fit subset, while direct `which.min(AICc)` on the saved `model_test` object gives 164 URW minima. This one-series difference is recorded as a processing/version/filtering discrepancy to reconcile from the full paper workflow; it is **not** treated as an error in either source.

## Interpretation boundary

The 19.84% value supports the statement:

> OU likelihoods are a nontrivial part of the empirical evolutionary time-series model space in this broad PETS compilation.

It does not support:

- `19.84% of evolutionary studies make invalid causal claims`;
- `125 published papers are affected`;
- `all OU-best time series imply adaptation`;
- `OU is the true process for 125 series`.

The causal theorem is conditional on a declared fitted observation law. Model adequacy, model selection, and independent biological evidence remain separate gates.

## Consequence for the second paper

The practice-relevance problem has split into two now-quantifiable layers:

1. **model-class denominator:** now directly established as 125/630 OU-best saved comparisons in this broad dataset;
2. **mechanistic-interpretation numerator:** still requires prospective coding of how fixed and moving OU parameters are biologically interpreted in empirical publications.

This materially raises the plausible scope of the paper, but Nature Ecology & Evolution should still not be claimed until the interpretation audit and independent empirical reproductions close.
