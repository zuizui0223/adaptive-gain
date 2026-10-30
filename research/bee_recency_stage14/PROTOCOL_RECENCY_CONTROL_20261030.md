# Stage14: matched final cue recency in wind-dependent bee resource decisions

**2026-10-30. PROSPECTIVE SYNTHETIC-ONLY DESIGN. No real bee has been assigned or tested.** This is an alternative, separately versioned extension stacked on PR85. PR85 and its frozen manuscripts remain unchanged.

## Identification defect and proposed independent test
PR85 first reveals reward/handling information at t=2s and then handling/reward at t=4s, with both physical options opened at t=6s. Thus cue identity and exposure timing/recency are confounded. A significant PR85 wind×order effect would causally identify the randomized presentation-order/recency *bundle*, not the bee's internal order of acquiring information.

Stage14 adds a THIRD randomized factor: final informative refresh versus equally timed noninformative sham. In every trial:
- First predictive cue (reward OR handling, both potential flowers): t=2.00–2.75s; then hidden
- Second predictive cue (the other type): t=3.50–4.25s; then hidden
- Final 0.75s event t=5.00–5.75s: **both predictive cues simultaneously** OR photometrically matched neutral sham
- At t=6s, BOTH rigid, symmetric flowers become accessible. No predictive graphics, markings, or inadvertent sensory cues remain visible at release; first trial choice cannot occur earlier
- Measured intake window exactly 30s after release, including verified zero-intake and no-choice trials

The first two presentations both last 0.75s; in the informative refresher arm their most recent exposure time is the SAME, so reward-first and handling-first can be compared without different latest display time. The sham refresher matches physical display events but not informational content. **This DOES NOT isolate internal neural query order or eliminate initial-age/primacy, extra-exposure, attention, memory or cue-difficulty effects.** The refresh-versus-sham difference itself is NOT a pure recency-effect estimator because informative refresh adds cue exposures.

The actual feeder reward/concentrations and handling surfaces must be calibrated, externally indistinguishable until contact, and left/right balanced. Pilot validation must demonstrate separate bee learning of both visual cue dimensions and feasible recognition of reward/handling side mappings when predictive graphics disappear. Otherwise NO_GO, rather than showing cues at choice or changing the primary endpoint. Pilot sham events must have comparable luminance, flicker, noise and physical obstruction, and original high-speed video must confirm no cue leakage.

Prior study context: Guiraud et al. (2025), DOI 10.1007/s10071-024-01926-x (stimulus timing can change learning); Spaethe et al. (2026), DOI 10.1126/sciadv.adw9320 (bumblebee cue selection depends on discriminability). These are background observations, NOT new data from this branch.

## Eight-arm allocation and source units
One 2 × 2 × 2 factorial: order reward-first/handling-first × pilot-calibrated calm/crosswind × informative/neutral final refresh. Hypothetical QA illustration 24 independently recruited colonies × 12 uniquely identifiable bees/colony × 64 trials/bee = **18,432 simulated assignment records**. Four 16-trial wind blocks per bee, ABBA/BAAB counterbalanced. Each wind block has exactly 2 repeats of every order × refresh × high-reward side triplet (2×2×2×2=16), giving **8 trials per bee per order×wind×refresh cell** and four equal side allocations in each eight-trial cell. All trials are randomized before experiment with a genuinely new private, concealed seed; public seed 20261030 is ONLY synthetic QA. This is NOT animal ethics approval or an instruction to recruit 24 colonies. Humane feasibility, fatigue and wind level must be established independently without peeking at main outcomes.

## ONE primary real estimand when actual trial data exist
Outcome Y is verified sucrose consumed in mg / exact 30-second opportunity window (mg/s), NOT feeder mass loss without blank/spill/leak corrections and video-confirmed contact. Failed landing or choice with functional source instruments remains zero, sensor failure is MISSING (not a zero), all randomized trials retained.

For one bee b in original colony c and refresh treatment r, define

D(b,r) = {mean[Y(reward-first,crosswind,r)] − mean[Y(handling-first,crosswind,r)]}
       − {mean[Y(reward-first,calm,r)] − mean[Y(handling-first,calm,r)]}.

**Primary** D_ref is calculated ONLY among informative simultaneous-final-refresh trials, averaged equally over bees within colony and then equally across independent colonies, with two-sided Student-t CI/test across independent colonies (df C−1, alpha .05; C>=12 and nonzero between-colony variation required). It estimates randomized presentation-history×wind under matched FINAL display time, NOT neural optimization, cognition of information costs C_A/C_F or evolutionary fitness. Locked secondary descriptions only: D_sham and D_ref−D_sham; neither may replace a nonpositive primary. Do not select rewarding animals or successful landings.

## Source contract and STOP
Require original trial identity and actual concealed assignment, complete source telemetry, both cue types and all 7 true on/off/access clock events (tolerances pre-locked in code), closed predictive-graphic panels at release, both equally accessible options, measured 3D wind and turbulence and pilot-derived non-overlapping physical speed limits, measured refresh luminance with independent pilot-based acceptable ranges, source video/clock sync, feeder calibration, confirmed actual sucrose intake and spillage blank correction. Each of EIGHT original factorial cells must achieve >=98% physical compliance; no pooled-only success. Full source-trial identity or sensor failure is NO_GO. No missing trial is invented as a no-drink.

Assumed variance NOT estimated from real animals: 12 bees/colony, 8 trials per 2×2 refreshed cell, sigma_colony=.025 mg/s, sigma_bee=.030, sigma_trial=.080, hypothetical D_ref=.020 mg/s. For 24 independent colonies expected Gaussian t power is **85.5%**, versus **90.1%** in the original 16/cell PR85; with sigma_colony=.040 this falls to **56.8%**. Actual non-Gaussian zero-intake, carryover and heterogeneity may substantially change power. Blind pilot variance, behavior and welfare must determine any realistic recruitment plan.

**Scientific freeze:** No live animals, no empirical effect, no observed wind or cue processing data in Stage14. Do not merge this synthetic study as evidence into V5/V6, PR85, or Stage9b–13. If pilot fails, stop and describe why; do not tune the latest-display windows, cue intensity or colony subset after observing real experimental effects.