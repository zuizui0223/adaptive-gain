# Empirical reproduction ledger v1 — trait-only OU causal-identifiability paper

## Status

This ledger distinguishes **published-summary anchors**, **materials-resolved workflows**, and **independently reproduced fits**. These categories must never be conflated in the manuscript or impact audit.

Date: 2026-09-13.

## R1 — Voje, Saito-Kato & Spanbauer (2024): moving optimum

**System:** fossil *Cyclostephanos andinus* trait series.

**Theorem stratum:** moving hidden optimum (`evoTS::logL.joint.OU.BM`).

**Current status:** `PUBLISHED_SUMMARY_ANCHORED / RAW_REFIT_OPEN`.

Already frozen:
- published OUBM model choice and reported fit summary;
- reported 12-year model-conditional half-life;
- exact reciprocal witnesses attached to the published observed-law parameters;
- source `evoTS` implementation matched algebraically.

Open reproduction task:
- obtain the archived `andinus.txt` and `main_analyses_andinus_biwa.R` files;
- reproduce preprocessing and time scaling;
- reproduce OUBM likelihood/AICc and the published parameter transformations;
- evaluate reciprocal witnesses on the exact empirical observation times.

The Dryad archive is publicly indexed, but this execution environment cannot currently materialize its file download through the available anonymous path. Do not count this as an independent reproduction until the archived workflow has actually been executed.

## R2 — Hunt, Bell & Travis (2008): fixed optimum

**System:** fossil threespine stickleback armor traits.

**Theorem stratum:** fixed optimum (`paleoTS` joint OU).

**Current status:** `MATERIALS_AND_WORKFLOW_RESOLVED / NUMERICAL_REFIT_OPEN`.

The current CRAN `paleoTS` source repository ships the empirical `dorsal.spines` object and a vignette that reproduces the analysis workflow:

1. load `dorsal.spines`;
2. remove levels without measured fossils;
3. restrict to post-invasion levels `tt > 4.4`;
4. reset time;
5. pool low-N variances using `pool.var(..., minN=5)`;
6. fit `fitSimple(..., model="OU")` using the default Joint likelihood.

Source contract:
`cran/paleoTS`, commit `6fbc4f6fa35ef2c7de73e11b9f6dda8ba73e7bc6`, `inst/doc/paleoTS_basics.Rmd`.

This is stronger than a literature-only anchor because the current package retains the exact data object and preprocessing recipe. It is not yet an independent numerical reproduction in this project: the `.rda` object has not been materialized in the present execution environment and R is not available locally.

Next closeable gate:
- materialize the package data object in an R-capable environment;
- reproduce the fixed-OU fit for at least one of the Hunt traits;
- save fitted `alpha`, `theta`, `vstep`, log-likelihood/AICc and the exact observation times;
- attach a reciprocal realization with identical mean/covariance on those times.

## R3 — Lo Cascio Sætre et al. (2017): fixed optimum

**System:** 19-year Maltese reed-warbler body-mass series.

**Theorem stratum:** fixed optimum (original analysis explicitly used PaleoTS).

**Current status:** `DATA_PROVENANCE_RESOLVED / RAW_REFIT_OPEN`.

Public provenance is unusually strong:
- Dryad DOI `10.5061/dryad.hj30r` contains `ReedWarblerData.xlsx` with annual mean log body mass, variance, sample size and year;
- the current `layeranalyzer` package independently mirrors the same dataset as `malta` and cites the Dryad DOI;
- the package vignette constructs the time series from exactly the four documented columns.

In this execution environment the Dryad data file and the GitHub `malta.rda` mirror cannot be materialized as usable tabular bytes through the available download interfaces, so the PaleoTS numerical refit remains open.

### Independent model-specification warning

The `layeranalyzer` vignette analyzes the same Malta series with a broader linear-SDE model family. Its reported best model in that search is a **linear-trend OU**, with example ML summary:

- log-likelihood `36.937`;
- AIC `-63.874`;
- AICc `-61.147`;
- characteristic time parameter approximately `2.518253` in that model's own parameterization.

This is not an independent reproduction of the original PaleoTS fit and must not be compared numerically as though the likelihoods were identical. It is scientifically useful for a different reason: it demonstrates that model specification for the same trait series is nontrivial.

Therefore the second paper must make its causal statement **conditional on the declared fitted OU observation law**. It should not rely on the stronger assumption that the original simple OU is the uniquely correct process model.

## Reproduction-count rule

A study counts as `INDEPENDENTLY_REPRODUCED` only after this project has:

1. obtained the empirical values used in the fit;
2. reconstructed the observation times and sampling-error treatment;
3. numerically matched the reported/package fit to a declared tolerance;
4. stored the fitted parameters and likelihood receipt;
5. evaluated a congruent reciprocal witness on the same observation schedule.

Published tables, package documentation, or an external reanalysis alone are not enough.

## Current counts

- direct empirical anchors: 3 systems;
- materials/workflow resolved beyond prose: 2 systems (Hunt; Lo Cascio Sætre provenance/mirror);
- independently reproduced numerical fits by this project: 0;
- exact reciprocal empirical-time witnesses after independent refit: 0.

## Consequence

The theory/practice bridge is now real, but empirical reproduction remains the dominant promotion gate. Further theorem growth has lower information value than closing R1–R3, especially one moving-optimum and one fixed-optimum fit.
