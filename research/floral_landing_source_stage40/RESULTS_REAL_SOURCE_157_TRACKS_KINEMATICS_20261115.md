# Stage40 — source-verified 3-D bumblebee landing speed under headwind

**2026-11-15. Existing original public 2016 data, independently reprocessed. NOT the paper's preselected 112-track mixed model; not a new experiment, natural flower pollination or fitness result.**

## Source and important correction to Stage39

Chang, Crall & Combes (2016), JEB DOI 10.1242/jeb.137976; exact original author Zenodo https://zenodo.org/records/60234, ZIP MD5 22bbc8286fecd2535d3f284679aed87b and SHA256 9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec.

Original 157 xyzpts CSV tracks have 95,153 total frame rows and 28 original bee-number filename B IDs. Contrary to a tempting interpretation of the Stage39 source missingness, the 4 rarely populated point-4 through point-7 XYZ sets are NOT four failed moving-body markers. **All 157 tracks have exactly one pt7 flower XYZ reference record**, which the original MATLAB selects and uses as the static coordinate origin. Moving body coordinates come from ONLY the first three BEETag markers.

Valid 3-tag frame rows: 84,774/95,153; consecutive physically observable 1-ms tag frame pairs: 84,617. The source's valid tag rows form one contiguous span per original track. The source MATLAB author script specifies fps=1000, Butterworth fifth-order cutoff 100Hz, filtfilt of first 9 tag columns, a per-track single pt7 flower origin, landing distance 0.015–0.03m, and approach distance 0.05–0.07m. B = bee number, S = stem stiffness, P = flower position, W = wind in original source filename parser.

## Genuine archived-data physical speed reconstruction (NOT author paper selection)

Independent Python/SciPy Butterworth filtfilt processing on the same verified original 3-tag streams computed mean ground speed via 3-point 1-ms 3D displacement. Each original source track must have at least 5 valid consecutive speed steps in both flower-relative physical stages.

Original archive wind W0: 56 files, 44 with both stages.
Original archive wind W1: 101 files, 98 with both stages.
**142 original tracks eligible (NOT 112 paper-selected trajectories).**

| Wind/kinematics | W0 (44 files) | W1 (98 files) |
|---|---:|---:|
| Approach speed 5–7cm | 0.26963947 m/s | 0.25621018 m/s |
| Near-flower speed 1.5–3cm | 0.10151403 m/s | 0.22636598 m/s |
| Landing minus approach speed | **−0.16812544 m/s** | **−0.02984420 m/s** |

The direction is aligned with the already published observation of strong deceleration in still air and reduced deceleration in 3.5m/s headwind. W0 is numerically close to the published −0.171m/s, whereas W1 differs from the published −0.004m/s, consistent with the unresolved 142-vs-112 selection and possible filtering differences. This is **not** an exact original R linear mixed model reproduction.

## Within-original-individual analysis: two levels of rigor

Step A — equal weight per 24 source B identifiers having both W0 and W1, average repeated tracks within each B/W first. Descriptive bootstrap resamples source B labels 10,000 times:

| B-paired W1−W0 endpoint | Mean difference | 95% B-bootstrap percentile, descriptive | Direction |
|---|---:|---:|---|
| Approach speed | −0.00567 m/s | −0.03604 to +0.02656 | 13 negative / 11 positive |
| Near-flower speed | **+0.13075 m/s** | +0.10500 to +0.15599 | 24/24 positive |
| Landing minus approach speed change | **+0.13641 m/s** | +0.09987 to +0.17039 | 21/24 positive |
| Source-style peak deceleration | −10.66395 m/s² | −14.07683 to −7.35925 | 23/24 negative |

Step B — stricter comparison within SAME source B (bee), SAME original S (stem stiffness) and SAME original P (flower position) BEFORE calculating wind W1−W0. This leaves **23 paired B labels** with valid same-condition W groups, one equal-weight result per bee after averaging the matched S/P cells:

| B×S×P matched W1−W0 endpoint | Mean difference | 95% descriptive bee bootstrap percentile | Direction |
|---|---:|---:|---|
| Approach speed | −0.01606 m/s | −0.04629 to +0.01483 | 15 negative / 8 positive |
| **Near-flower speed** | **+0.12143 m/s** | **+0.08906 to +0.15452** | **22/23 positive** |
| **Landing minus approach change** | **+0.13749 m/s** | **+0.09579 to +0.17868** | **21/23 positive** |
| Source-style peak deceleration | −9.98690 m/s² | −15.10405 to −5.66738 | 21/23 negative |

**The primary sign persists after same-bee, same flower-position, same stem-stiffness matching**, making simple treatment imbalance less compelling. However, these are descriptive sample-bee resampling intervals, NOT pre-registered independent-colony population CIs, p-values, causal effects or exactly reproduced author analysis.

## The unresolved reproducibility gate

The article reports **112 selected original paths** (N=31/27/29/25 across four primary conditions) from 28 bees; the archive exposes 157 files (W0=56, W1=101), with 142 meeting our pre-specified minimum-valid-window rule. The example author MATLAB iterates all xyzpts files and its case-by-case original trialType mapping is commented out. The publication's selected filename/acceptance ledger is unavailable, and do not assert our 142-eligible group equals paper's 112 used for its original R mixed-effects model.

Source filter edge handling and exact body/flower orientation may also differ from the author's final analysis; keep this sensitivity explicit. In particular, no number of failed approach attempts is observed, so reconstructed velocity cannot be translated into landing-success probability.

## Why this matters for information-based pollination

The actual source establishes a physically reconstructible near-flower MOTOR CONTROL cost of wind in Bombus impatiens, independent of the Stage37 observed positive male orchid-bee perfume-bait ARRIVAL association in naturally varying, much weaker winds. These are different species, experimental units and wind ranges. **DO NOT multiply them to estimate whole-flower pollination or a wind×odor benefit**. No original odor OFF, pollen deposition, nectar guide, visit choice, fruit/seed or plant-fitness data are present.

## Code, source checks and final status

New Stage40 content lives ONLY in the Draft analysis branch based on Stage39:
- audit_original_MATLAB.py — original author script source SHAs and selected method pointers, no full author code redistributed.
- static_landmark_gate.py — verifies one static flower origin per 157 tracks and real consecutive frame units.
- reconstruct_3d_approach_landing.py — reconstructed physical ground speeds, source-free robustness, bee B and B/S/P within-condition descriptive bootstrap.
- Three focused mock-only test suites: 18 tests (including constant synthetic 0.55m/s 1000Hz straight trajectory).
- GitHub Actions original-authenticated source run 43711962109 SUCCESS for matched 23-bee analysis; source ZIP retained only in ephemeral runner; only derived JSON artifact uploaded.

This is NOT a meta-analytic pooled fitness result. No original raw data redistributed. Whole repo Python 3.10–3.12 CI must be checked on the final head after documentation. Draft/unmerged, main restored to pre-accident content tree.
