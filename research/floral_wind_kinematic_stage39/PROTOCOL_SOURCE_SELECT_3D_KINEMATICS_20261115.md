# Stage39 — 2016 original 3-D landing tracks: source selection and calibration gate

**2026-11-15. Real public Zenodo original-trial file audit, not yet a reconstructed flight-speed or plant-pollination effect.** Draft stacked on Stage38 PR #118; prior Stages22–38 and main untouched.

## Essential author methodology and source identity

Chang, Crall & Combes (2016), JEB DOI 10.1242/jeb.137976, original Zenodo #60234, authenticated original archive MD5 22bbc8286fecd2535d3f284679aed87b.

The article specifies 28 marked Bombus impatiens animals, two cameras filming at **1000 Hz**, 3-D DLT-tracked body/tag coordinates, fifth-order Butterworth smoothing with **100-Hz low-pass cutoff**, ground speed by numerical differentiation, approach region 5–7 cm from the target flower and landing region 1.5–3 cm from the flower; peak contact deceleration is the largest negative derivative of speed in the final 100ms.

**Critical study-grain discrepancy:** The article reports **112 selected primary-condition flight paths** divided into (still-parallel 31, wind-parallel 27, still-perpendicular 29, wind-perpendicular 25) from 28 original bees. The public ZIP contains **157 source xyzpts CSV trajectory files** with filename W0/W1 tokens counted 56/101, and 28 distinct filename B-token labels. These cannot automatically be treated as the article's 112 selected flight paths, 157 independent bee subjects, or 157 available approach opportunities. Some files may relate to additional immobilized-flower trials or selection exclusions; this must be resolved by authors' source methodology, not guessing.

## What the new original source audit checks

- Fetches the actual source archive through the official Zenodo record and validates the original declared checksum before reading internal data.
- For all 157 source trajectories, checks exact 21-column XYZ point schema (pt1_X/Y/Z through pt7_X/Y/Z), frame counts, 3D marker completeness and NaN patterns, native XYZ numerical range, and filename-label tuples B, F, S, P, T, W and BC.
- Scans source MATLAB scripts for known timing, coordinate conversion, filtering and selection tokens while outputting only short filename-level markers and counts; original author code is never republished.
- Writes only aggregate JSON, preserving the raw-data units and independent-bee status as UNVERIFIED until authenticated. Recording 1000 Hz from the paper does NOT automatically prove every archived CSV row is a consecutive 1-ms frame or that native XYZ columns are meters.
- Refuses to output a reconstructed m/s difference or a confidence interval when the correct subset of 112, coordinate calibration, flower center and complete repeated-bee mapping are not established.

## Gate for actual kinematic reanalysis

1. Map each original 157 filename to the paper's 112 selected tracks, using original exclusion and flower orientation logic and exact animal identifiers.
2. Confirm actual original frame interval, missing frame index retention, native 3D spatial scale, and coordinates of flower center. Source header only says XYZ.
3. Apply authors' 5th-order 100-Hz Butterworth filter with validated end handling. Reconstruct ground speed in published approach 5–7cm and landing 1.5–3cm regions and peak deceleration from the last 100ms of each actual trial.
4. Fit original bee-level repeated-measures model, not independent 112/157 trajectory t tests. Check flower orientation and stem-fixation controls separately.
5. NEVER infer an original landing-success probability from these successful-landing tracks; no total number of aborted approaches is available. Never infer stigma contact, seed set, evolution of nectar guides, or wind-by-scent interactions.

## Context and scientific ceiling

Stage37 reanalyzed male Euglossini visits to artificial fragrant baits under natural wind 0.02–0.73m/s and found a within-site observational positive visit association. The 2016 wind tunnel used Bombus impatiens and a 3.5m/s HEADWIND, with different experiments and outcomes. Both are relevant to a proposed multimodal decision hierarchy but **must not be multiplied to claim a same-cohort net plant fitness effect**.

No new biological effect or causal claim is introduced by this source-quality protocol.
