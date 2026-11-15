# Stage41 source-verified results: six kinematic preprocessing specifications

**2026-11-15. Original published measurements, independent reprocessing on GitHub Actions. Exploratory, NOT a new pollination experiment or a reproduction of the author-selected 112 paths.**

- Stacked Draft PR: https://github.com/zuizui0223/adaptive-gain/pull/121
- Final pre-report-head original-source CI SUCCESS: https://github.com/zuizui0223/adaptive-gain/actions/runs/43722512438
- Checksum-verified Chang, Crall & Combes 2016 author source: Zenodo 60234 (MD5 22bbc8286fecd2535d3f284679aed87b), 157 source xyzpts files, W0=56/W1=101, 28 B filename labels.
- Aggregate receipt artifact ID **14164823999**, digest **sha256:f279193e3e9ef23766f7ac76988a06d868216ce34a8a86d806113e995f9b6e94**. The source ZIP/track rows were ephemeral and not redistributed.

## Independently confirmed real-source result

Fifth-order Butterworth 50, 100, 150 Hz, both 3-marker mean speed and point2-only speed. All 6 cases had 44 eligible W0 tracks, 98 eligible W1 tracks; 23 matched source B IDs after same-B × stem-S × position-P matching. Each listed B ID contributes ONCE.

| Cutoff (Hz) | 3-marker mean: W1-W0 near flower (m/s) | point2-only: W1-W0 near flower (m/s) |
|---:|---:|---:|
| 50 | +0.121674957 | +0.120859607 |
| 100 | +0.121429363 | +0.120632663 |
| 150 | +0.121226729 | +0.120472880 |

Every method specification: **22/23 matched source B labels have positive near-flower W1-W0**, one negative; all 23 leave-one-B-out recalculated means remain positive. The minimum across all leave-one-B-out means/six methods is **+0.110931678 m/s**.

The separate W1-W0 landing-minus-approach *speed-change* endpoint remains positive in all six specifications, ranging **+0.136557013 to +0.137492214 m/s**. **21/23** B labels positive for all six. No actual colony sampling and no independent sign-test inference are claimed.

**Independent algorithm cross-check:** separate CSV parser, numerically stable SOS filter, and separate matched-B aggregation reproduce Stage40 original-formula 100 Hz near-flower W0=0.10151403 m/s, W1=0.22636598 m/s, within B-S-P effect +0.121429 m/s to tolerance 1e-5.

## What the result establishes and what it does not

The positive association of wind coding with higher near-flower **ground speed** in the available original Chang archive is not driven by these two particular preprocessing decisions. This is stronger algorithmic evidence than a single 100 Hz/3-point result, but the same 23 individuals and same wind experiment are reused six times — NOT six independent biological replications.

**Unresolved provenance:** the paper's 112 primary flexible-flower paths comprise 60 calm and 52 windy, while the archived file codes are W0=56, W1=101. Assuming each selected path corresponds one-to-one to an archived file and W0 is calm, the 60 calm paths cannot all be selected from 56 W0 files. The original selection/trial metadata must be reconciled before paper-level replication or confirmatory population inference. This finding does NOT establish any error by the source authors.

Neither the original nor Stage41 data establish the numerator/denominator for landing success, odor-on/off factorial interaction, floral pollen transfer, viable seeds, plant fitness, or causal mechanism. Higher landing impact is a physically plausible cost, not measured reduced plant reproduction.

**Software readiness:** the dedicated authenticated-source run passed; complete Python 3.10–3.12 CI on the final reporting commit requires its own check. Keep PR draft/unmerged.
