# Stage43 — original 2016 paper denominator audit and exact observed-bee deletion sensitivity

**Date 2026-11-16 JST. Status: original author Zenodo data reprocessed in GitHub Actions; this is a finite-source sensitivity exercise, NOT a new animal experiment, independently validated paper 112-trial replication, actual landing-success rate, or plant pollination effect.**

## Two original sources and the new provenance issue

**Original article:** Chang, Crall & Combes (2016), *Journal of Experimental Biology* 219:2819–2822, doi:10.1242/jeb.137976. Independent author-lab PDF: https://combeslab.faculty.ucdavis.edu/wp-content/uploads/sites/594/2020/01/Chang2016_WindBumblebeeLanding-1.pdf (pp. 2820–2821 manually reviewed). This document was read by a person/assistant; the Stage43 CI does **not** automatically download or SHA-verify the published PDF. The article contains more than one **potentially incompatible denominator statement**; neither statement licenses repair by guessing unseen trials.

**Original raw trajectory source:** https://zenodo.org/records/60234 ZIP original author SHA256 \`9a2881e5aaf4d7bb9556c9118c45d2e2ed6a2a8b22b80d4d762a5626fdd918ec\`. Original \`analyzeTrackingData.m\` SHA256 \`e05e565c13e70b043017fa5e88cfcd1789d81a4de0fd932fed1e6985b82475ce\` from that ZIP; original filenames parse B (bee number), S (stiffness), P (position), W (wind). There are 157 archived 3D xyzpts files, 28 source B numbers, W0=56, W1=101. The example script would write \`floralApproachBeeData.mat\` and \`flowerApproachDataForStats.csv\`, but neither is actually included in that archive, and no original selected 112-file roster was authenticated.

### Literal article denominators must not be silently conflated

| Original article location | Written or inferred source counts | Conditional implication |
|---|---|---|
| Results, p. 2820 | parallel still 31; perpendicular still 29; parallel wind 27; perpendicular wind 25 | four-cell total 112, still 60, wind 52 |
| Fig. 1 caption's **first clause**, p. 2820 | still 31 parallel / 27 perpendicular, wind 29 parallel / 25 perpendicular | same total 112, but 27 and 29 are associated with different conditions from the main text and caption's later clause |
| Fig. 1 caption's **later clause** and results prose | parallel 31 still / 27 wind, perpendicular 29 still / 25 wind | agrees with Results prose; treat this as primary interpretation while preserving the caption inconsistency |
| Fig. 2 caption, p. 2821 | still 60, wind 52 | matches Results prose/primary counts |
| Speed-change paired t-tests, p. 2821 | df 54 for still *and* df 54 for wind | standard paired/one-sample t implies 55 observations per separate test, which differs from the Fig. 2 60/52 labels. Could be distinct sample/endpoint semantics; no error allegation |

Original all-archive counts aggregated over S:

| Original P/W filename cell | All archived file count | Primary Results prose target | Fig. 1 first-clause target |
|---|---:|---:|---:|
| P0 W0 | 31 | 31 | 31 |
| P1 W0 | 25 | 29 | 27 |
| P0 W1 | 52 | 27 | 29 |
| P1 W1 | 49 | 25 | 25 |

**One-to-one, code-matching assumption ONLY:** at least **4** printed Results-prose P1W0 paths cannot be assigned to the available 25 P1W0 archive files; under the inconsistent first-clause caption reading, at least **2** are unavailable. This is not proof that 4 or 2 truly missing recordings exist, and neither reading authenticates actual 112-trial selection. The 55/55 denominator suggested by df=54 is also **not** the same as the paper's plotted 60/52 without further information. These are reasons to avoid paper-equivalent mixed model claims; NOT evidence of misconduct or a proven computational error.

## New exact finite-data removal result

Target: **original already-archived W1−W0 near-flower 3D ground-speed difference** (m/s), using physically identified static flower point, 1000 Hz 3-marker tracking, 5–7 cm approach / 1.5–3 cm near flower, and same B×S×P wind comparisons. Multiple original paths are averaged within condition, then one equal-weight signed W1−W0 difference is computed for each original B identifier. Each original B contributes only once. Same 6 prior Stage41 preprocessing combinations are used, cutoff 50/100/150 Hz × mean of 3 tags vs only tag2 speed.

For any integer k between 0 and n−1, the **exact minimum retained mean after deleting ANY k observed original B labels** is the mean of the smallest n−k per-B contrasts. This follows from the elementary exchange argument; no combinatorial Monte Carlo, cluster-incorrect per-frame bootstrap or chosen deletion subset is necessary.

### Main six-method original-source outputs

| Preprocessing | n original matched B | Positive B | W1−W0 all-B mean (m/s) | Worst any one B deletion (m/s) | Worst any 3 deletions (m/s) | Minimum whole-B deletions needed to make mean non-positive |
|---|---:|---:|---:|---:|---:|---:|
| 50 Hz, 3-point speed | 23 | 22 | +0.121675 | +0.112001 | +0.101704 | 22 |
| 50 Hz, point2 speed | 23 | 22 | +0.120860 | +0.111172 | +0.100903 | 22 |
| 100 Hz, 3-point speed | 23 | 22 | +0.121429 | +0.111900 | +0.101681 | 22 |
| 100 Hz, point2 speed | 23 | 22 | +0.120633 | +0.111069 | +0.100878 | 22 |
| 150 Hz, 3-point speed | 23 | 22 | +0.121227 | +0.111716 | +0.101506 | 22 |
| 150 Hz, point2 speed | 23 | 22 | +0.120473 | +0.110932 | +0.100742 | 22 |

**Strictly within these 23 already observed, matched original bee IDs and their existing fixed individual contrasts**, ANY deletion of at most **21** bee IDs leaves a positive retained near-flower speed mean in all six specifications. Removing 22 can leave just the one negative source B contrast, so sign can then reverse. This is a purely **finite observed list** guarantee and *does not cover selecting different original paths within the same B, adding unarchived experiments, changing B×S×P pairing or original author 112 membership*.

For the distinct landing-minus-approach change endpoint at 100 Hz/3-marker, mean +0.137492 m/s (21/23 matched B positive), the minimum strategic entire-B exclusions needed for a non-positive retained mean is **18**. This is not independent biological evidence of wind benefit.

### Subgroup fragility revealed alongside the positive main result

100 Hz/three-marker main subsets:

- S0: near-flower +0.143022 m/s, 19/19 positive, no deletion of observed labels can invert the sign while retaining ≥1 B.
- S1: +0.075389 m/s, 8/10 positive; 7 worst-case B removals are required to make the retained mean non-positive.
- P0: +0.112141 m/s, 19/20 positive; needs 18 whole B removals for possible non-positive mean.
- P1: +0.128880 m/s, 15/17 positive; needs 14 removals.
- **S1/P0: only four original matched B labels**, +0.046594 m/s, 3/4 positive; adversarial removal of just **two** labels gives −0.002157 m/s. This subgroup is fragile despite positive observed mean.

Subgroups overlap by B label, so multiple subgroup rows are not independent replication. The S0/S1 and P0/P1 filename labels do not by themselves resolve physical flexible/fixed or parallel/perpendicular provenance.

## Inference firewall / journal suitability

The article **already discovered** wind-dependent deceleration and contact kinematics in Bombus. The new contribution is reproducibility, partial identification and exact sensitivity of the **available original dataset**, not discovery of a novel ecomechanical phenomenon.

This stage neither tests the proposed scent-driven detection advantage nor measures approach failures, landing-success probability, flower pollen transfer, seed production or actual plant fitness; do **not** multiply these original Bombus 3.5 m/s wind-tunnel speeds with Crall orchid-bee low-speed scent-bait visitation associations from a different species and experiment.

### Code/source gates

- \`selection_robustness.py\` independent source downloader and source-locked finite-B deletion bounds across 6 preprocessing variants × 9 subsets × 2 endpoints.
- \`test_selection_robustness.py\` has 10 mock/arithmetic regression tests; first 2026-11-16 source-free run found an intentionally near-zero floating-point test fixture problem, corrected by using an explicitly negative mock. No original source measurement or hypothesis sign was changed.
- Dedicated original ZIP/MATLAB source [Actions run 43797660395](https://github.com/zuizui0223/adaptive-gain/actions/runs/43797660395) **SUCCESS** after repair.
- Source-derived aggregate artifact ID **14195037815**, digest \`sha256:c4cbf505a7b98a1cddc8099261cd4a56d4793435ab588ebb935dfecbf7cf7068\`.
- Original trajectories / MATLAB scripts are downloaded in the ephemeral CI runner and not redistributed. Only derived numeric summary JSON is uploaded.

**Next gating task:** original author selected-path membership/analysis outputs, including S/P/W codebook and treatment-time trial-level eligibility, or a separately accessible original archive. Without this, neither publication-selected reanalysis nor inferential bounds for those unobserved paths are identified. Keep Draft, not main-merged.
