# Stage 10 — measured 3D bee flight heading under original experimental wind

**2026-10-29 | Real original-data heldout result FROZEN | Outcome: measured early-heading increment is NOT supported**

## Exact statement

On the available Chang, Crall & Combes (2016) original tracked bumblebee landing trajectories, an added *early actually measured 2D translational heading* did not improve out-of-bee prediction of *later measured landing-phase 2D heading* beyond frozen environmental and early position/speed covariates. Instead the observed individual-equal squared-error contrast **M0−M1 = −0.014176991019060461** (negative = the added-heading model was **worse**), with only **8/28 original tagged bees** showing a positive gain.

This is a **negative outcome for a predeclared specific predictive comparison**, not a general proof that bees lack flight memory, cannot sense their direction, or cannot compensate wind. **It does not contradict** the independent positive Stage9b geometrically defined *between-flowers destination* predictor; the response and scale differ. The author paper itself already showed wind-related changes in landing dynamics; those are not credited as a new finding here.

## Original data, source semantics, exclusions

- Chang, Crall & Combes (2016), DOI https://doi.org/10.1242/jeb.137976, primary original source https://zenodo.org/records/60234.
- Original native archive `ChangCrallCombes_WindAltersLandingDynamicsInBumblebeeData.zip`, **3,361,411 bytes**, **published original MD5** `22bbc8286fecd2535d3f284679aed87b` (matched), **computed SHA256** `9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec`.
- Exact full source **157 original experiment/tracking CSV trial files**, 28 BEEtag individual identifiers mapping one-to-one onto 28 barcode IDs. Source data use real 1,000-Hz bee XYZ triples. Wind is W0 still air vs W1 original wind, while S0/S1 and P0/P1 label stiffness and flower orientation. Source contains **157 trials**, distinct from source-paper **112-trial** original figure subset. No original-trajectory raw rows committed.
- **Important original-source repair during source schema audit, before fitting any Stage10 scientific outcome**: file line endings may be CR-only, normalized in memory without changing a single value or original archive digest. Native `pt7` flower reference is **one finite 3D landmark per original trial in 157/157 source files**, NOT a flower position recorded at each frame. The original authors' own `analyzeTrackingData.m` subtracts this single reference from per-frame tracked tag vertices using MATLAB `bsxfun`. The first attempt to demand a concurrent per-frame flower value excluded all 157 source trials; it was a **source semantics NO_GO**, not a modeled null result. Source-only 157-trial diagnostic and a transparent pre-outcome amendment corrected the reader. No time series of actual flower displacement is measured, and none is fabricated.
- A valid bee centre requires finite original positions of all three tag vertices for that *original* frame; use the source trial-level observed flower landmark as radial origin. No imputation. Prespecified early distance ring **5–7 cm**, late ring **1.5–3.0 cm**, each at least **8 consecutive real 1000-Hz frames**, late strictly after early. Least-squares 3D track slopes (source frames only) provide early/late velocities; original finite XY speeds ≥0.02 m/s.
- **133/157 original trials eligible, 28/28 original bees**; 25 original bees have eligible still-air flights and 26 have wind flights, with **40 still-air trials and 93 wind flights**. Predeclared feasibility thresholds: ≥60 trials, ≥16 bees, ≥12 distinct bees per wind stratum — all PASS.
- Original 24 technical exclusions (one primary reason per original trial): no complete early ring **16**; XY speed too low **8**. Exclusions follow frozen source-validity gates, not wind/heading outcome labels. The complete eight S×P×W original counts and technical exclusion reasons are in the source machine-readable artifact. W=1 wind vs W=0 are imbalanced by original design and eligibility; do not compare naive trial-weighted means as independent bees.

## Four exact checks of source and methods

1. Original source archive byte hashes verified before *any* CSV extraction.
2. Native source README identifies B/BC/F/S/P/W exactly and original MATLAB confirms 1000Hz; original 157 files and original bee IDs reconciled.
3. Synthetic controls and regression tests: **17/17** passed, including chronology, nonleaking early velocity slopes, all-trials-from-one-bee holdout, source hash mismatch and one-per-trial flower reference.
4. Original-source CI successfully executed predeclared **leave-one-BEE-ID-out** modeling. Each of 28 folds holds out all original trials of that individual, fits train-only ridge with frozen **α=5**, and reports two-model squared error on the same heldout late-XY-unit-velocity targets. Same original 133 eligible tracks in both models; individual bee is repeat unit, not 133 independent bees or thousands of frames.

### Primary real holdout endpoint

M0 controls: wind W, flower orientation P, source stiffness S and W×P×S interactions; early 3D position relative to source flower, radial distance and early planar speed.

M1 = M0 + actually measured **early planar direction (two unit-vector coordinates) and W interactions**. Frozen coefficients and early-ring measurement do not read late outcome of the heldout bee.

| Recorded original outcome | Actual result |
| --- | ---: |
| Genuine source trials with usable early and late measured headings | **133** |
| Original tagged individuals (all-bouts leave-one-bee-out) | **28** |
| Mean individual gain M0 squared error − M1 squared error | **−0.014176991019060461** |
| Individuals with positive M1 gain | **8/28** |
| Still air: original source bees / eligible flight trials | **25 / 40** |
| Still-air individual-equal model gain | **−0.024897922929296077** |
| Wind: original source bees / eligible flight trials | **26 / 93** |
| Wind individual-equal model gain | **−0.012619791855197795** |
| Difference wind minus still, descriptive | **+0.012278131074098282** |

Both wind-specific *individual-equal* increments are negative; their difference is not a significant causal wind×heading interaction estimate. No formal bee-cluster confidence interval or preregistered null test of wind interaction was performed, so neither a positive nor negative population-level moderation conclusion is licensed. The prespecified hypothesis of a positive added-heading gain is **not supported**. The proposed second hypothesis (a smaller *positive* heading gain under wind) is also **not supported**, even though the descriptive subtraction of two negative gains is positive.

## Interpretation and falsification boundary

- **Supported:** real 2016 original 3D tracking plus one observed trial-level target landmark can support source-native, chronologically defined early/late heading calculation in 133 original files. The heldout evaluation has a concrete direction: the frozen extra-heading features *hurt* the chosen predictive loss, while environmental/position/speed baseline was already available.
- **Not established:** actual trajectory inertia does not exist; bees have no heading memory; the final approach is dynamically reoriented because of wind; exact response of flight steering to physical flower swaying (flower movement was not measured time-resolved); optimal allocation of sensory cues, interspecific information use, reward intake, fitness or natural ecological niche shifts.
- **Comparison with PR87:** Stage9b's positive 2017 experiment targets **next physical flower identity** from flower-to-flower chords and bee’s earlier B→C visitation history. Stage10 targets **late translational heading** during *approach to ONE actual flower*. They do not share source colony, task, response, 3D heading recording, or fixed κ. The different results delimit overgeneralization across scales; they **do not** imply statistical proof of a cross-scale difference or two experimentally distinguished cognitive mechanisms.

### Source execution receipt and stop

- [Original 2016 source MD5, exact native-schema and one-per-trial flower point7 QA, fixed 17 tests, and Stage10 genuine bee-heldout scoring SUCCESS (GitHub Actions #40866068451)](https://github.com/zuizui0223/adaptive-gain/actions/runs/40866068451).
- Source-only original-schema failure before scoring and correction documented explicitly in `PROTOCOL_TRUE_HEADING_HOLDOUT_2026_10_29.md` and `audit_landmark_semantics.py`.
- **Do not** alter 5–7 cm/1.5–3 cm source rings, 8-frame minimum, ridge α, feature grid, heldout bee splits, or original exclusions after the observed negative result. The 199 within-bee×W×P×S predecessor-heading shuffle is **secondary predeclared conditional diagnostic** and remains unevaluated, not a hidden positive significance claim.
- Frozen V5/V6, original theoretical main and Stage9b PR87 unchanged. Stage10 is a distinct draft branch and must remain descriptive until independent source/experimental validation is available.
