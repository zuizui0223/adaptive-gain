# Empirical reproduction ledger v2 — trait-only OU causal-identifiability paper

## Status

This version supersedes v1 for gate accounting while retaining v1 as the pre-refit snapshot. The first independent numerical empirical reproduction is now closed in the fixed-optimum stratum.

Date: 2026-09-13.

## Direct empirical anchors currently tracked

### Moving optimum

**Voje, Saito-Kato & Spanbauer (2024), fossil *Cyclostephanos andinus*.**

- theorem stratum: moving hidden optimum (`evoTS::logL.joint.OU.BM`);
- current status: `PUBLISHED_SUMMARY_ANCHORED / RAW_REFIT_OPEN`;
- published OUBM result, reported 12-year half-life and published-summary reciprocal witnesses are frozen;
- Dryad archive DOI: `10.5061/dryad.bk3j9kdmj`;
- independent raw-data/script reproduction remains the dominant open gate.

### Fixed optimum — Hunt et al. (2008)

**Status: `INDEPENDENT_NUMERICAL_REFIT_PASS_WITH_SOURCE_VERSION_CAVEAT`.**

Using `cran/paleoTS@6fbc4f6fa35ef2c7de73e11b9f6dda8ba73e7bc6` and paper-matched preprocessing, this project independently reproduced the dorsal-spine fixed-OU half-life as `844.994` generations versus the published `853` generations, a relative difference of `0.94%`.

A `q=1/2` reciprocal witness evaluated on the same 57-population empirical schedule matched the observed mean to `2.22e-16` and covariance to `3.47e-18`. The direct-coupling half-life in that congruent witness is `1689.988` generations while the observed relaxation law is unchanged.

Full receipt: `theory/HUNT_2008_FIXED_OU_REFIT_V1.md` and `validation/hunt_2008_fixed_ou_refit_v1.json`.

### Fixed optimum — Lo Cascio Sætre et al. (2017)

- system: 19-year Maltese reed-warbler body-mass series;
- theorem stratum: fixed optimum;
- current status: `DATA_PROVENANCE_RESOLVED / RAW_REFIT_OPEN`;
- original study explicitly used PaleoTS and reported `alpha=0.39`, half-life `1.76 years`, together with independent ecological/genetic/fitness evidence;
- Dryad and the `layeranalyzer` mirror establish data provenance;
- an independent broader-model reanalysis on the same series selects a linear-trend OU, which is retained as a model-specification caution, not as a replacement for reproducing the original likelihood.

### Fixed optimum — Voje (2020)

- system: fossil Yellowstone diatom valve-diameter series;
- theorem stratum: fixed optimum;
- current status: `DIRECT_PRACTICE_ANCHOR / RAW_REFIT_OPEN`;
- fixed OU was the best candidate in the published analysis, with a reported half-life of approximately 1740 years and explicit optimum-tracking interpretation;
- the original study also reports model-adequacy caution, making it an informative example that separates model adequacy from causal attribution.

### Adjacent denominator candidate

**Gearty et al. (2018)** uses paleoTS Joint OU on fossil aquatic-mammal trait series, but mechanistic numerator coding remains unresolved because its fixed-time-series use and phylogenetic-OU interpretation are intertwined. It is not yet counted as a confirmed mechanistic fixed-OU example.

## Reproduction-count rule

A system increments `INDEPENDENTLY_REPRODUCED` only if this project has:

1. obtained the empirical data used in the fit;
2. reconstructed the observation schedule and sampling-error treatment;
3. numerically reproduced the relevant fitted law under a declared source/version contract;
4. stored fitted parameters and likelihood information;
5. evaluated an exact reciprocal witness on the same empirical schedule.

Published summaries, source documentation and external reanalyses do not increment the count.

## Current counts

- confirmed direct empirical anchors tracked: `4` systems (`1` moving, `3` fixed);
- independent fixed numerical refits: `1` (Hunt 2008 dorsal spines);
- independent moving numerical refits: `0`;
- exact empirical-time reciprocal witnesses after independent refit: `1`;
- broad saved-object model-class denominator: `125/630` empirical PETS series have fixed OU or moving OUBM as minimum-AICc model (`56` fixed, `69` moving).

The `125/630` value is model-class prevalence only. It is not a prevalence estimate for mechanistic interpretation.

## What changed relative to v1

The fixed empirical bridge is no longer literature-only. A published adaptive-peak analysis has now been reproduced numerically using preserved empirical data, a pinned current implementation and paper-matched preprocessing, and the exact reciprocal congruence has been verified at machine precision on that empirical schedule.

This materially strengthens the paper because the distinction between observed relaxation and one-way causal attribution is now demonstrated on a real fitted series rather than only through symbolic algebra or published parameter summaries.

## Remaining promotion gates

1. close at least one independent moving-optimum OUBM raw-data/script refit, with Voje et al. (2024) first priority;
2. execute denominator-defensible interpretation coding for the direct OU applications rather than relying only on model-class prevalence;
3. preserve cases with independent biological evidence as such—the theorem limits what the trait likelihood alone identifies and does not erase external causal evidence;
4. turn the common-shock bound into a practitioner-facing reporting workflow.

Further expansion to new theorem classes has lower information value than these gates.