# Stage14 prospective cue-order × wind with matched final display recency

**2026-10-30 — NEW DESIGN AND SYNTHETIC VALIDATION ONLY. No real animal results.** This is an *alternative protocol* stacked on Stage9 PR #85. The existing PR85 hypothesis, empirical Stage9b–13 records, V5/V6 and main remain untouched.

## What was changed and what it identifies

Previous prospective PR85 starts the first cue at 2s and the second cue at 4s and opens the feeders at 6s. The cue that appears last is also more recent. A randomized PR85 order effect would therefore mix presentation order with information recency and, depending on visual persistence, unequal exposure duration.

The Stage14 randomized factors are **order (reward first/handling first) × instrumented calm/crosswind × final simultaneous informative reminder/sham**. The 2 original sequential predictive information presentations are now identically short (0.75 s each), then masked. At t=5.00–5.75 s both reward and handling cues appear together for the informative arm; identical-duration nonpredictive, photometrically matched display for the sham arm. At t=6 both physical feeder options become accessible without any visible predictive graphics. True consumption is measured for exactly 30s, including source-confirmed no-feed outcomes as zero.

In the informative refresher arm, the **last external exposure** to reward/handling is temporally matched between the two orders. This tests whether randomized initial **information-presentation history** has a wind-dependent effect on actual intake when last-exposure timing is matched. It **does not** prove bee-selected query order, cancel all mnemonic or primacy effects, or identify the mathematical cost advantage C_A/C_F. The informative vs sham arm changes number of information exposures and cannot be treated as pure “recency” mediation.

## Synthetic software validation

[Dedicated synthetic design Actions run #41043163683](https://github.com/zuizui0223/adaptive-gain/actions/runs/41043163683): **SUCCESS**, 14 tests. Sample 24 synthetic source colonies ×12 synthetic bees ×64 synthetic trials = **18,432 MOCK trial assignment records**. Eight treatment cells each contain **2,304 simulated assignments**; each bee has exactly 8 per order×wind×refresh cell. Wind is block-counterbalanced by original bee; within-block order×refresh×side are balanced 2 times each. Synthetic allocation SHA256 is `a9cdfcbc031cd5e70739ed841260bc36f13047081854f09e8ecba9433e0aed6d`. This is **NOT** a prospective clinical/animal randomization commitment: genuine study allocation requires a new private seed and ethical approval.

A synthetic-only injected estimator QA with hypothetical informative-refresher D=+0.018 mg sucrose/s, sham D=−0.004 mg/s recovered those exact values and a descriptive difference +0.022 mg/s. **All three numbers were injected into code, not discovered in bees.** Synthetic p-values and confidence intervals are therefore excluded from empirical claims.

Instrument/quality gate: 1,024 source-free mock trials across all 8 arms passed. The contract rejects predictive graphics visible at gate, wrong on/off cue timing, incorrect cue identities, a failed sensor masquerading as real zero intake, missing original 3D wind vector, luminance outside separately specified pilot tolerances, and a single factor cell below ≥98% hardware adherence. The synthetic speed/luminance values in mock telemetry are **fictional QA fixtures**, NOT calibrated real-study settings.

## Primary future outcome and analysis

If independently approved and collected, primary outcome is actual video and source-feeder-verified sucrose consumed (mg) per fixed 30s window, with spill/blank/evaporation corrections. **No landing/no choice** gets zero only when functioning instruments verify no intake; source failure is missing, not zero. All randomized animals and trials remain in the intention-to-treat population.

For each actual bee and independently recruited colony, compare **reward-first minus handling-first under crosswind** and **reward-first minus handling-first under calm**, **ONLY among informative final-refresh trials**. Average equally over bees within each original colony and equally over actual independent colonies. Student t CI/test with df=colonies−1 and two-sided alpha0.05; fewer than 12 independent colonies => descriptive pilot only. Sham-refresher order×wind and informative−sham are fixed **secondary** diagnostics and may not replace a null primary.

Every original trial must carry original colony/bee/trial identity, cue-shutter instrument clocks, actual labels and visibility, both options simultaneously open, 3D wind vector/turbulence, video clock sync, independent pilot wind/luminance ranges, feeder calibration, spillage blanks, and source-confirmed ingestion. No actual colony, feeder or bee observation is present in this repository.

## Assumption-only power (NOT measurements)

Assumptions inherited for *comparison only* from PR85: 12 bees/colony, 0.080 mg/s trial residual SD, 0.030 mg/s bee-level contrast SD, 0.025 or 0.040 mg/s colony contrast SD, hypothetical true refreshed-primary interaction +0.020 mg/s. With the added 2-level refresh randomization, each bee has **8** rather than 16 trials in each primary 2×2 cell at the same hypothetical total 64 trials/bee.

| Source independent colonies | New design power if σ_colony=.025 | If σ_colony=.040 |
| ---: | ---: | ---: |
| 12 | 52.9% | 30.1% |
| 16 | 67.2% | 39.7% |
| 24 | **85.5%** | **56.8%** |
| 32 | 94.1% | 70.1% |
| 48 | 99.2% | 86.9% |

The prior 2×2/16-per-cell assumed-case power at 24 colonies/σ_colony=.025 was 90.1%; extra factor reduces the assumed power to 85.5%. Gaussian/independence/constant outcome variance assumptions are **unvalidated**. Power does not reflect actual zero intake, fatigue, photometric learning failures or ethics constraints. **Do not recruit 24 colonies based on this table alone**.

## Pre-recruitment scientific and ethical STOP rules

1. Pilot must show individually learned **both** reward and handling cue dimensions and use of remembered left/right cue mappings when predictive graphics are hidden at choice. Recent bee studies indicate that multiple cue attributes need not all be learned, depending on discriminability (Spaethe et al. 2026, DOI 10.1126/sciadv.adw9320); timing can alter learned visual information (Guiraud et al. 2025, DOI 10.1007/s10071-024-01926-x).
2. Measure/instrument the two arm-specific refresh luminance and flicker, every stimulus duration, source 3D wind and the opening of both physical flower options. Clamp real flowers so wind does not move the target. Sham must match physical display motion/noise.
3. Independent animal welfare and equipment feasibility must approve exposure duration, trial fatigue, wind intensity and number of independent colonies. Genuine concealed assignment and preregistration must be created BEFORE real outcome data.
4. If any source gate fails or the primary effect is null/negative, **report and stop**; no changing cue timing, choosing responders or interpreting sham effects as a replacement primary.

**Scientific status:** a stronger identification *design*, not a positive empirical finding, and not a replacement for the published Stage9b–13 observations.