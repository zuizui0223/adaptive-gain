# Stage41 — robustness of original Bombus headwind-landing reconstruction

**Status: original-source runtime is required. This file states a fixed analysis plan, not a biological result.** 2026-11-15.

## Registered sensitivity before reading the new result

Original source: Chang, Crall & Combes (2016), *J. Exp. Biol.*, DOI 10.1242/jeb.137976; Zenodo record 60234. Reuse original source-checksum gate and 157 archived xyzpts CSVs (95,153 frames, 28 source B identifiers). Never redistribute raw source CSV rows.

Factor 1 is the low-pass fifth-order Butterworth cutoff **50, 100, or 150 Hz**. Factor 2 is physical 3D ground speed as the **mean Euclidean velocity of three BEETag markers** or **point2-only Euclidean velocity**. Six configurations are fixed in code and tested on invented constant-speed tracks. The original publication used 100 Hz. Stage40 used 100 Hz and three-marker mean. The new analysis uses SciPy's numerically stable SOS filter form, a separate parser and standalone within-bee matching, rather than calling the Stage40 speed function.

Hold fixed: original 1000 fps; one pt7 static flower landmark; 5–7 cm approach and 1.5–3 cm near-flower stage defined from filtered point2; minimum 5 valid 1-ms derivative steps per region; same source filenames; comparisons **within source B identifier × stem code S × position code P**, averaged to one matched difference per B, not per frame or trajectory.

Evaluate **near-flower W1–W0 speed** and **landing-minus-approach W1–W0 speed**, the number of paired B labels, signs across labels, and extrema of leave-one-B-out means. Negative or null effects are retained rather than failed as a software test. The 100 Hz three-tag configuration must independently reproduce Stage40's published source-archive aggregate to tolerance 1e-5 m/s.

## Source-selection stop and interpretation

Original journal: flexible-flower main-condition flights = **60 still-air + 52 wind = 112** from 28 bees; archived source filenames = **56 W0 + 101 W1 = 157**. Under the *assumption* that archival W0 means all still-air flights and that every selected path corresponds one-to-one to an archived source file, all 60 published still-air paths **cannot** be a subset of just 56 W0 files. This is a provenance/selection inconsistency that cannot be repaired with statistical significance, nor is it proof of an original-author error: original trial selection, missing files, the semantics of source W codes, and the archived-vs-published denominator remain unknown.

The 6-specification original-source sensitivity tests the **archived-file numerical result**, not a reproduction of the published 112-selected-track mixed model. Bee labels are not independent colony units, and original unrecorded failed landings are not counted. Neither positive velocity difference nor a successful CI run measures flower pollen delivery, seed set, actual fitness or odor-by-wind causal interaction.

CI may complete successfully even if some method specifications change the biological sign; inspect the uploaded numeric receipt before interpreting robustness.
