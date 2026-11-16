# Stage42 — original archive/P-W-S compatibility and 100 Hz matched-B subgroup results

**Date:** 2026-11-16 JST. **Existing original author data, reprocessed; no new experiments.**

## Source, code, and reproducibility

Chang, Crall & Combes (2016), *J. Exp. Biol.* 219:2819–2822, doi:10.1242/jeb.137976, public author Zenodo 60234 original ZIP exact SHA256 \`9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec\`. Source MATLAB \`analyzeTrackingData.m\` SHA256 \`e05e565c13e70b043017fa5e88cfcd1789d81a4de0fd932fed1e6985b82475ce\` verifies source filename coding for B bee ID, F flower number, S stem stiffness, P flower position, T trial number, W wind. **S0/S1 cannot be labeled flexible/immobilized without an authenticated legend.** P0/P1 cannot safely be mapped to paper parallel/perpendicular without a checked codebook.

Dedicated real-source original 3D CI [run 43791535981](https://github.com/zuizui0223/adaptive-gain/actions/runs/43791535981) **SUCCESS**. Aggregate source receipt artifact ID **14192383002**, digest **sha256:cc729c3564dbaea532dc4779e51eb6c6d6914acde4a7e145429fb0044ca48741**. Source coordinates / author code not redistributed.

## Paper-to-archive one-to-one membership incompatibility

The publication's primary flexible-flower flight paths: **112** across 28 bees, four treatments by orientation P and wind W. Original counts from journal body text and Fig. 1 orientation-conditioned caption:

| Wind / position condition | Paper selected n | All available original archive n (both S codes) | Minimum additional source primary files required, if labels map exactly |
|---|---:|---:|---:|
| W0 / P0 | 31 | 31 | 0 |
| W0 / P1 | **29** | **25** | **4** |
| W1 / P0 | 27 | 52 | 0 |
| W1 / P1 | 25 | 49 | 0 |
| **Total** | **112** | **157** | **at least 4** |

Author MATLAB identifies W via \`filename(27)\`, P via \`filename(20)\`, S via \`filename(17)\`. This original ZIP contains **56 W0** vs **101 W1** source trajectories, so the paper's full 60 selected W0 cannot all be uniquely identified among the available 56 W0 files under a one-to-one, correctly-coded assumption. The discrepancy is localized to the original P1_W0 file count (25 vs paper 29), and does not mean exactly four missing files exist: recoding or other source selection could also explain the discrepancy. There is *no authenticated original 112-member file/trial roster* in the inspected archive, and no separate non-trajectory .csv/.mat/.r/.rds/.xlsx source summary was found by the source-manifest scan. **This is a provenance/selection nonidentification, NOT a claim that the 2016 authors made a statistical mistake.**

Actual source counts by S/P/W:

| Source stratum | W0 files | W1 files |
|---|---:|---:|
| S0 / P0 | 25 | 29 |
| S0 / P1 | 13 | 27 |
| S1 / P0 | 6 | 23 |
| S1 / P1 | 12 | 22 |

## Independently reconstructed 100 Hz 3-tag W1−W0 signal within condition codes

The Stage42 validator re-fetches exact 157 author trajectories and processes the original 1000-Hz 3D body markers, source static pt7 flower reference and fifth-order Butterworth 100 Hz. Each comparison matches the **same B bee ID × same S code × same P code**, then averages matched cells to **one value per B**, rather than treating files or 1-ms frames as independent biological replicates. Original 112 selected study paths are not imputed or recreated. Results below are exploratory and descriptive.

| Archive subset | Source file count W0 / W1 | n matched B | Positive B W1−W0 near-flower | Mean near-flower Δspeed (m/s) | Mean landing−approach Δspeed contrast (m/s) |
|---|---:|---:|---:|---:|---:|
| All S/P | 56 / 101 | 23 | 22/23 | **+0.121429** | **+0.137492** |
| S0 only | 38 / 56 | 19 | **19/19** | **+0.143022** | +0.132735 |
| S1 only | 18 / 45 | 10 | 8/10 | **+0.075389** | +0.123901 |
| P0 only | 31 / 52 | 20 | 19/20 | **+0.112141** | +0.077998 |
| P1 only | 25 / 49 | 17 | 15/17 | **+0.128880** | +0.204547 |
| S0/P0 | 25 / 29 | 16 | 16/16 | +0.128528 | +0.085571 |
| S0/P1 | 13 / 27 | 9 | 9/9 | +0.175129 | +0.250460 |
| S1/P0 | 6 / 23 | 4 | 3/4 | +0.046594 | +0.047709 |
| S1/P1 | 12 / 22 | 8 | 6/8 | +0.076850 | +0.152896 |

The sign is **positive in all four S×P source subgroups**, and also in both S margins and both P margins. However, the S1/P0 contrast has **just four matched B codes**, so its support is weak. S/P margins and cells reuse many of the same bees, not new independent populations. No claim of true clinical/causal/population-level significance, independent colonies or confidence intervals from these repeated contrasts.

## Biological claim ceiling and next external dependency

Strongest supported statement: **original archived bumblebee trajectories consistently show a higher final near-flower ground speed when filename-coded W1 wind is present, including after controlling for B×S×P and changing the signal-processing recipe across Stage41.** The paper itself established high ground-speed landing in wind; this is robustness and archive-source sensitivity, not a new biological phenomenon. The current data do not reveal failed flower approaches, true success probabilities, odor-on/off experimental effects, actual pollen transfer, seed set, or plant fitness.

**Remaining original-2016 replication gate:** an author-authenticated list of the primary 112 selected trials (including 60 still/52 windy with real P/S annotations) or a source archive with the missing W0/P1 trajectories is necessary to reproduce the exact paper LME. Without it, the source-coded 157-file sensitivity is independent exploratory evidence, NOT a reproduction of the authors' selected design. If an alternative coding scheme is found, re-open the source mapping rather than suppressing the discrepancy.

The source-only CI is successful at the initial code head; verify dedicated source test and complete Python 3.10–3.12 matrix independently on the final documentation head. Keep PR Draft; do not merge into main as if selected-source identification were closed.
