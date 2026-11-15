# Stage39 — authenticated 157 original bee tracks, 95,153 frame rows

**2026-11-15. REAL source-data quality reanalysis, NOT a physical m/s kinematic effect estimate.**

Source: Chang, Crall & Combes (2016), doi:10.1242/jeb.137976, exact author public Zenodo record 60234; actual archive checksum md5 22bbc8286fecd2535d3f284679aed87b. Original source confirmed via isolated GitHub Actions source-quality run **43707968830 SUCCESS** (10 synthetic-only QA tests passed, original ZIP read).

## Verified original source data

| Source profile | Verified original number |
|---|---:|
| Number of 3-D xyzpts CSV trajectory files | 157 |
| Source tracking rows across all files | **95,153** |
| Original B filename ID tokens | **28** |
| Original F filename tokens | 22 |
| Original S/P codes | 2 each |
| W0 / W1 filename counts | **56 / 101** |
| Frame rows per track | min 221, median **529**, max 1,387, mean 606.07 |
| Inferred source coordinate header | 21 columns = 7 points × X/Y/Z |
| Original source native coordinate X range | −0.01741 to +0.061082 |
| Original native Y range | −0.04644 to +0.10914 |
| Original native Z range | −0.052267 to +0.095519 |

The ZIP's original CSVs include legacy CR-only line endings, discovered on first real-source parse. The corrected parser preserves newline semantics without altering source bytes or inventing field splits. Original source MATLAB contains analyzeTrackingData.m with timing, low-pass Butterworth and XYZ token references, plus DLT tracking scripts; source-code token presence is NOT a full interpretation of all selection choices.

### The main novel QA finding: four nearly empty markers

Across all 95,153 original frame rows:
- Three-dimensional coordinates of source point 1, 2 and 3 are EACH valid in **89.09230397%** of rows.
- Three-dimensional coordinates of source points 4 through 7 are EACH valid in **0.16499743%** of rows.
- All seven have complete XYZ in only **0.154488%** of original frames.

This is a **major source-grain hazard**: building a 7-point complete-case body center would remove over 99% of source time rows. The paper says it tracked three points on the bee's mounted BEETag, so the plausible physically meaningful input is source points 1–3; use their independently verified geometry and the authors' calibration, not an arbitrary 7-marker average. Missing point coordinates are NOT observed zeros or body positions.

### A second major QA finding: published sample is smaller than archive

Paper describes 28 individual bees, with **112 selected landing paths** for its four principal conditions, split 31 still-parallel, 27 wind-parallel, 29 still-perpendicular, 25 wind-perpendicular (two still condition descriptions sum 60 and two wind 52). The 157 original archived filename set has different W0=56 and W1=101 file counts. It cannot be equated with those 112 paper-analyzed paths without the author's inclusion and orientation rules.

The original archived filename cross-tab is:

| Filename source code | Files |
|---|---:|
| S0/P0/W0 | 25 |
| S0/P0/W1 | 29 |
| S0/P1/W0 | 13 |
| S0/P1/W1 | 27 |
| S1/P0/W0 | 6 |
| S1/P0/W1 | 23 |
| S1/P1/W0 | 12 |
| S1/P1/W1 | 22 |
| **All** | **157** |

There are 28 unique B filename tokens, consistent numerically with the paper's reported N=28 marked bees. Still, a filename token is not automatically a verified individual without the source mapping, and the W tokens must be authenticated as actual wind treatments. Different trial numbers and flower orientation/stem fixation controls may explain the 45-file selection difference; this explanation remains UNVERIFIED and is not assigned as fact.

## Physical inference requirements

The author paper states two high-speed cameras at 1000 frames/s, 5th-order 100-Hz Butterworth filtering, approach/landing spatial windows 5–7cm and 1.5–3cm from flower, and last-100ms maximum deceleration. **We have NOT verified that the 157 CSV rows are consecutive 1-ms frames, raw coordinates are in meters and correctly flower-centered, or which trials meet the published selection.** Source XYZ ranges make one interpretation plausible but cannot prove calibration.

Before a new physically meaningful wind speed effect, recover original analyzed track IDs, original spatial unit/frame-clock and flower-center coordinate, author filter implementation/edges, and bee-level covariance. No 157-trial independent samples, source wind-speed means, 2016 m/s deltas, approach failure rates, pollination metrics, or plant fitness values are estimated in this Stage39.

## Why this matters for the larger floral-information project

Stage37 independently confirmed a *positive observational association* of wind with male orchid-bee arrivals at perfume bait, whereas the Chang source concerns headwind biomechanics of successful flower landings. These are different species, wind regimes and experiments. The data-quality improvements prevent an attractive but erroneous multiplication into a whole-flower net fitness effect.

**Software status:** original source-locked focused CI green run 43707968830. Stage39 newest documentation commit and Python 3.10/3.11/3.12 all-repository CI must be checked independently. Stage39 remains Draft / unmerged.
