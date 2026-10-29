# Stage10: true measured incoming heading versus flower geometry under wind

**Locked 2026-10-29 AFTER real original source checksum/native-schema inspection but BEFORE any Stage10 heading-model outcome calculation.** This is a *new reanalysis of an existing published wind experiment*, not an independent experimental replication of its authors' wind result; original authors established directional funneling and harder landings.

## Verified native source
- Chang, Crall & Combes (2016), JEB 219:2819–2822, DOI 10.1242/jeb.137976. Zenodo 60234 verified original archive MD5 `22bbc8286fecd2535d3f284679aed87b`; SHA256 `9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec`.
- Original author README and `analyzeTrackingData.m`: 1000 recorded frames/s, filename `B##_BC####_F##_S#_P#_T##_W#...`; B=individual bee, BC=BEEtag ID, S=stiffened flower, P=flower parallel/perpendicular, W=wind off/on; original columns `pt1_X..pt7_Z`. First THREE xyz points are bee BEEtag triangle; point 7 is flower landmark. Units original position metres (paper reports cm but native example coordinates in metres; require frame and range QA rather than silent rescaling).
- Zip contains **157 real trial CSV files for 28 original individually tagged bees** (28 unique B-to-BC bijections). This is the **available full source**, including extra stiffened-flower tests; it is NOT the 112-flight primary figure sample and those extra trials are NOT invented independent bees.
- Original paper uses wind 0 vs 3.5m/s, flower parallel vs perpendicular, and random treatment order. Source trials are repeated within bee. No synthetic trial rows, no guessed session/day identities.

## Scientific target
Does an **actually tracked incoming translational direction early in one bee's flight** improve prediction of the later **landing-phase translational direction** beyond environmental condition and flower geometry? Does that extra predictive information become smaller under headwind (hypothesized directional funneling)?

This directly measures trajectories, unlike Stage9b's discrete flower-to-flower chords. But it does NOT measure simultaneous alternative flowers, sensory cue acquisition order, actual cognitive memory, adaptive search cost, resource choice, interspecific interactions or Darwinian fitness. Early-to-late physical velocity autocorrelation by itself would NOT establish those mechanisms.

## Predeclared real observation extraction
1. Read each original CSV once. Timestamp = original frame index / 1000 seconds (native time 0 not necessarily absolute). Reject malformed, nonunique original source trial file names; NEVER concatenate distinct trials. Source original XYZ units metres, expect 21 columns with exact original names.
2. At each frame use mean of the **three** original bee-tag point xyz vectors ONLY when all three finite, and actual `pt7` flower xyz in that frame ONLY when all finite. No zero imputation, no interpolation, no model-based pseudo-position. Use the *time-varying actual observed point7 flower coordinates at the same frame*, not a trajectory-wide median or a stability-only subset; flexible flowers can move under wind. Reject a frame only if actual point7 is missing, never interpolate. Do not make dynamic flower movement itself an exclusion condition.
3. Define exact source-published radial distance rings using true 3D Euclidean distance bee centre–flower: **early 0.05–0.07 m**, **late 0.015–0.030 m**. Find contiguous valid frame runs in each ring, minimum **8 consecutive 1000Hz observations per ring**. Choose first eligible early run, then last eligible late run strictly after the early run. No across-trial joins; require early end < late start.
4. Compute early and late 3D translational velocity as a least-squares slope of original frame index vs xyz in the corresponding window; never derive new velocity by using frames beyond the early ring. For the target use late XY unit velocity, reject if XY speed <0.02m/s; reject early XY speed <0.02m/s. Outcome is **future measured XY direction**, not flower identity or success rate.
5. Include every native source trial that meets these *source-quality* gates, independent of its wind, P, S, bee or observed heading value. Report totals and exclusion reasons by full S×P×W stratum, per-bee support and whether all 28 bee tags occur. No refilling source failures or changing ring thresholds after outcomes.
6. Predeclared minimum for scientific scoring: **at least 60 eligible genuine trajectories, 16 distinct source bees, at least 12 individual bees per W stratum**. If not met, source-analysis NO_GO and no substitute model.

## Predeclared two models, fixed holdout and metric
Single **leave-one-original-bee-out** (LOBO) evaluation across the full available subset, with ALL genuine trials from one original B bee fully held out. Same 157 candidate trials, same eligible trials, same heldout folds, identical target and no source test labels in fitting.

Model M0: fixed intercept; original wind W, flower orientation P, stiffness S, W×P, W×S, P×S, W×P×S; early relative position (x,y,z), early radial distance and early XY speed. Model M1: M0 plus **early measured XY unit velocity** and its W interactions. No lagged landing-dependent predictor. Both models use ridge least-squares with **alpha=5.0** and training-only feature centering/scaling; no hyperparameter search or posthoc feature selection. Multivariate response is the observed late XY unit-velocity vector (x,y).

Primary loss: squared error of 2D unit-vector conditional-mean prediction `(observed_x − predicted_x)^2+(observed_y − predicted_y)^2` (proper for the conditional vector mean, not directional categorical NLL). Positive `MSE(M0)−MSE(M1)` is a *predictive* increment; average scores per bee, then equally over heldout bees. Report additionally wind-stratum means, a descriptive W1−W0 difference, and separately per-eligible bee sign of gain. Bee-count is inferential unit; frames/trials are nested and **not independent biological replicates**. Do not label 28 bees 28 colonies.
- H1: M1 expected positive heldout mean gain compared with M0.
- H2: heading increment smaller under wind W1 than still W0 (wind compresses possible headings); **negative/zero is a valid outcome, not a tuning opportunity**.
- No formal out-of-study generalization: one original experimental source and possibly one supplier colony.
- Observed wind coefficient or interaction is experimentally conditioned here, but the observational within-flight lag cannot identify how an animal sensed/used heading or whether it is intentionally adjusted.

## Diagnostics (prelocked)
199 fixed seed 20261029 shuffles of early measured XY headings within **same W/P/S and bee** among genuine heldout test trials, keeping actual future late XY outcomes, original geometry, wind, and training model unchanged; if insufficient exchangeable strata, report NO_GO_PERMUTATION but retain primary. The shuffle is a *statistical source label null*, not a physically possible flight.
Bounded sensitivity: no coordinate smoothing beyond original tracking; accept only the fixed 8-frame threshold. Unstable flower landmark or insufficient NaN-complete rings are explicit excluded technical observations. No alternate rings, lag, alpha, outcome, colony or wind subgroup may be searched after Stage10 outcomes.

## Stop rule
If actual original support fails the minimum, freeze NO_GO and report *why*. Regardless of successful prediction, do not label result a direct validation of Stage9b κ=1.0 or of finite adaptive information theory. The 2016 original already demonstrated increased upwind alignment in wind and wind effects on landing; do not rebrand that published association as new. Frozen V5/V6 and PR #87 unchanged.

## Pre-outcome source-physics clarification (same date)
The authors' flowers can move and their original time-varying point7 is the observed flower landmark. A static median would silently erase an important environmental component and condition on low-motion flowers. This wording correction is committed **before executing any Stage10 trajectory outcome or evaluating any model**. All remaining fixed rings, predictors, heldout splits and estimands are unchanged.
