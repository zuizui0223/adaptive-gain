# Stage40 — Original 2016 wind landing tracks: physical 3-D speed reconstruction

2026-11-15. NEW ANALYSIS OF EXISTING PUBLISHED PUBLIC DATA, not newly measured bees. The original manuscript's selected 112 trajectories were not individually authenticated in the publicly archived 157 tracks. Results are exploratory source-archive estimates, not the original paper's mixed-effects refit.

## Source provenance and a major data-schema correction

Chang, Crall & Combes (2016), Journal of Experimental Biology, DOI 10.1242/jeb.137976. Original public Zenodo https://zenodo.org/records/60234. Exact source archive md5:22bbc8286fecd2535d3f284679aed87b and SHA256 9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec.

The 157 original xyzpts CSV trajectories have 95,153 physical frame rows and 28 original filename B label IDs. Stage39 confirmed that source points 1–3 have nonmissing XYZ for 89.09% of frame rows, whereas points 4–7 have only 0.165% each. STAGE40 EXPLAINS THAT SPARSENESS: every one of the 157 original files contains EXACTLY one point-7 XYZ record. The author MATLAB analyzes the flower location as a single static point-7 reference subtracted from every moving tag position. Points 4–7 are NOT four failed time-varying body markers; they encode sparse fixed reference landmarks. This corrects the interpretation of the previous stage's missingness report, without rewriting old frozen files.

Of the 95,153 source time rows, 84,774 have valid XYZ for all three moving tag markers. There are 84,617 immediately adjacent pairs of valid time rows, exactly (84,774 minus 157); each trajectory has one contiguous valid segment and no artificially interpolated gap.

The author's original analyzeTrackingData.m specifies 1000 frames/s, fifth-order Butterworth low-pass 100 Hz, filtering only the first 9 XYZ columns, source point 7 as the flower origin, near-flower distances 0.015–0.03m and approach distances 0.05–0.07m. Filename parser explicitly names B beeNumber, S stiffness, P position and W wind.

## Reconstructed original 3D kinematics (exploratory archived sample)

An independently implemented Python/SciPy filtfilt 5th-order 100Hz filter and 1000Hz original time index reconstruct point 1–3 speeds in original meters per second. Each speed is the mean of the three individual marker consecutive-frame displacement magnitudes times 1000. Point 2's Euclidean distance from the single static point 7 defines the same physical stage windows as the author code. Tracks must contain at least five valid speed steps in BOTH windows. Do not average seven marker coordinates; no raw track time series are redistributed.

Original source archive W0: 56 tracks, of which 44 have both stages.
Original source archive W1: 101 tracks, of which 98 have both stages.
Total stage eligible: **142 tracks** (not the paper's independently selected 112).

| Derived source-stage endpoint | W0 available tracks (44) | W1 available tracks (98) |
|---|---:|---:|
| Approach velocity, 5–7cm | 0.26963947 m/s | 0.25621018 m/s |
| Near-flower velocity, 1.5–3cm | 0.10151403 m/s | 0.22636598 m/s |
| Landing minus approach speed change | **−0.16812544 m/s** | **−0.02984420 m/s** |

The pattern agrees qualitatively with the 2016 publication: calm-flight approaches slow strongly before contact whereas bees in 3.5m/s headwind maintain faster near-flower speed. The W0 mean closely resembles the paper's already published −0.171m/s, while W1 −0.0298 differs from paper's −0.004m/s: the 142-track source inventory is NOT the 112 selected paper dataset, and Python/MATLAB filter edge conventions or source metadata may also differ.

### Repeat-aware comparisons: original bee label as unit (24 labels with both conditions)

For each original bee source B label, average its qualifying tracks within W0 and W1 BEFORE computing wind minus calm; each bee contributes once. A fixed-seed 10,000-replicate B-label bootstrap gives descriptive percentile intervals, NOT independently replicated colonies or fully adjusted experimental CIs.

| Wind W1 minus calm W0 | Mean B-level difference | Descriptive B-bootstrap 95% interval | B-label directions |
|---|---:|---:|---|
| Approach speed | −0.005667 m/s | −0.03604 to +0.02656 | 13 negative, 11 positive |
| **Near-flower speed** | **+0.130746 m/s** | **+0.10500 to +0.15599** | **24/24 positive** |
| **Landing minus approach speed change** | **+0.136413 m/s** | **+0.09987 to +0.17039** | **21/24 positive** |
| Exploratory last-100ms peak speed deceleration | −10.66395 m/s² | −14.0768 to −7.3593 | 23/24 negative |

Source flower position P and stem stiffness S have not been balanced in this B-level summary; the original experiment has repeated trajectories within bees and the archived-to-paper trial selection is unresolved. These numerical bounds are descriptive for the available archived tracks only.

## Unresolved published-subset source identification

The paper reports 112 selected flight paths from 28 bees in four principal treatment combinations (N=31,27,29,25). The archive has 157 available xyzpts files, of which the W0/W1 flags are 56/101. The author example MATLAB loops over ALL xyzpts files but its detailed trial-type classification statements are commented out, and no verified list of 112 selected original filenames is bundled. Consequently neither a paper-exact data denominator nor original random-intercept likelihood is reproduced here. This does not imply an error in the paper; archived file composition, additional flower-stiffness controls and source screening may account for the difference.

## Why this is relevant to a broader floral-information theory

The actual data show a physical impairment of smooth deceleration and stronger impact deceleration in a wind-tunnel Bombus impatiens system. The earlier Crall 2020 source measured male orchid-bee arrivals at scented artificial bait stations under much weaker natural winds. These distinct ecosystems, wind ranges and receiver taxa MUST NOT be multiplied into a same-cohort net pollination success or an evolutionary plant-fitness effect.

No natural odor ON/OFF factorial, stigma deposition, nectar-guide adaptation, seeds, failed approach opportunity counts or reproductive fitness outcomes were measured in this Stage40. Sensory learning and wind-compensation ability still need independent within-receiver data.

## Reproducibility and status

- audit_original_MATLAB.py: immutable source-code file hashes, author analysis method and selection identifier audit, with original code excerpts limited to console logs, never uploaded.
- static_landmark_gate.py: verified the 157 unique one-row static flower centers and contiguous tag-frame runs.
- reconstruct_3d_approach_landing.py: actual physics from the source-verified public ZIP, stage-conditioned per-track speeds and bee-paired exploratory bootstrap; author original data never copied to GitHub.
- 17 mock-only mathematical/source-grain tests, including synthetic 0.55m/s constant speed (1000Hz), stale source/duplicate flower landmark/missing interior frame stops, and repeated-identifier aggregation.
- Dedicated original-source CI run 43711480790 SUCCESS after correcting a Python codec-name typo. This result was computed on source-identical authentic Zenodo archive and publishes only derived JSON.
- The whole repo's Python 3.10/3.11/3.12 CI must still be verified on the final documentation commit. Draft/unmerged, previous stages/main untouched.
