# Stage 9 — causal cue-order × wind experiment for floral resource decisions

**Status: PROSPECTIVE EXPERIMENT DESIGN AND SYNTHETIC VALIDATION ONLY. No new bees have been tested. Date: 2026-10-29.** This document is not a retrospective preregistration for Stage 4–8 findings. Do not report simulations as empirical effects. The real protocol must be registered and allocation concealed **before** experimental data collection.

## Why this experiment is needed

Earlier source-verified work provides converging but *noncausal* observations at different levels:
- Stage 3 PoMS field FIT wind association: the 10-minute **single preselected target flower** survey had a strong-wind versus calmer-condition bumblebee-to-other-fly relative-visitation association, remaining after local Pan flowering richness and dominant botanical-family composition, but no individual-choice data or wind intervention.
- Stages 4–6 original tagged bees: 10 bees from **one colony** and a 10-flower fixed cage: previous flower had held-out predictive value but geometrical distances and incoming **endpoint-chord direction** explained much of the next-destination structure; residual first-order history was not consistently positive once heading was controlled. No source wind manipulation.
- Stage 7b independent robotic flowers: **16 qualifying colonies** showed 5-minute community-level reward-use temporal smoothness; individual bee IDs were absent.
- Stages 8–8b independent Cambridge tagged bees: 36 bees in **three colonies**, distinct-flower orientation predicted the next orientation beyond each bee's stationary choice preference, but most of that association was reproduced when predecessor states were shuffled *within uninterrupted bout segments*; only a residual **+0.0070244 nats/decision** remained against that conditional null. Immediate previously recorded *Drink* action added no clear conditional signal (p=.355). Source flower IDs were episodic identifiers, not positions.

The missing causal estimand is: **Does manipulating the *order in which physical floral information becomes available* change realized resource uptake, and is this effect modified by a calibrated wind exposure?**

A positive test would causally identify a *presentation-order effect under the controlled experiment*, not prove the precise internal cognitive computation, sensory-query costs `C_A,C_F` or evolutionary optimality.

## Experimental objects, contrast and observation grain

- Two equally distant, symmetrically placed **rigidly clamped** artificial flowers visible at decision time, left and right; physical XY position and incoming heading recorded by synchronized overhead/side video, so flower identity **is a persistent physical ID**, unlike the Cambridge Stage 8 original table. Both options available after the second cue, never one missing option disguised as a choice.
- One option contains **high-concentration sucrose with difficult/micro-rough handling**; the alternative offers **lower-concentration sucrose with easy/coarse-rough handling**. Reward class and surface class are a **deliberately conflicting menu**; side assignment counterbalanced *within each original bee×wind block×cue-order cell*. Nectar concentration and accessible reward volume must be weighed and calibrated, and identical across cue-order arms. Distinct cue graphics (one conveys reward class, one conveys handling class) must be pre-trained and pilot-validated for accuracy, color/brightness salience counterbalanced. Do not assume a flower's visual color reveals sucrose concentration unless a trained and verified cue does.
- **Cue order treatment `O`**: reward information first (`reward_first`) versus handling/friction information first (`handling_first`). At t=2 s reveal first predictive cue for both options; at t=4 s reveal the other predictive cue; at t=6 s open choice access simultaneously, giving a fixed 2 s between last information and choice. Keep total exposure, release gate movement, luminance and available decision options identical. Do not allow a bee to choose or reach either flower before both cues. Order necessarily alters recency as well as processing opportunity; measure the randomized total **order/recency** effect, not a uniquely identified cognitive computation.
- **Wind exposure treatment `W`**: instrumented `calm` versus a **pilot-locked, moderate, constant crosswind**. Flower movement mechanically clamped in both arms to isolate direct flight exposure from target motion. Wind speed, direction and turbulence measured by synchronized local anemometer. Wind intensity is set **in an independent feasibility pilot** before primary outcome unblinding; never tuned by primary data significance, and no wild/unsafe intensity used. Calm blower sham controls equipment noise and flow-control behavior.
- Experimental units: individual bee `bee_id` nested in independent original `colony_id`. Both order arms are randomized **trial-by-trial**; wind is randomized in **counterbalanced bee-level blocks** to avoid impractical blower transients and carryover. There are four bee blocks of 16 trials, wind sequences `calm,wind,wind,calm` (ABBA) or `wind,calm,calm,wind` (BAAB), assigned in balanced pairs across bees and colonies. In *each* 16-trial block, `(cue_order, high_reward_side)` has precisely 4 observations in each of four combinations, shuffled with a concealed allocation. Therefore each bee receives **16 randomized trials in every order×wind cell** (64 trials per bee); high/hard option appears on each side equally often.
- The number of independent colonies is a **design choice informed by explicit assumed-variance power scenarios**, not inferred from previous per-visit p-values. Baseline example: **24 independent colonies × 12 bees × 64 trials = 18,432 randomized trials**. This is a prospective planning scenario, **not an actual collected dataset**. Recruitment/animal welfare/feasibility and needed power must be confirmed before any ethics application and preregistration. A 12-colony smaller pilot could assess **blinded variance and equipment performance only**, not cherry-pick the wind×order effect.

## Primary registered estimand and test (causal via random assignment only)

Outcome `Y` is **measured sucrose mass actually taken from a calibrated feeder (mg sucrose) divided by a fixed 30-second measurement window (mg/s)** after release. Source-delivery measurement must subtract instrument-detected spillage, leakage and evaporation using parallel equipment blanks; the feeder's decrease is NOT automatically bee intake. The **30 s clock starts at trial access release**; all assigned trials are included even if no flower is chosen, no landing occurs or no drinking is recorded (`Y=0`), provided functional sensors confirm zero. Do not condition the primary sample on successful landing or feeder contact. An instrument failure is *missing outcome*, not zero: flag and fail closed until fixed, with documented missingness sensitivity.

Randomized order indicator `O∈{handling_first,reward_first}` and wind `W∈{calm,crosswind}`; fixed outcome gain/time is never fitted using source models. Define, for each bee and independent colony:

```
Delta_bee = ( Ybar[reward_first, crosswind] - Ybar[handling_first, crosswind] )
          - ( Ybar[reward_first, calm]      - Ybar[handling_first, calm] )
Delta_colony = mean_bee_in_that_colony( Delta_bee )
Delta = mean_independent_colonies( Delta_colony ) [mg sucrose/s]
```

**Primary null** `H0: Delta=0` (two-sided α=0.05); report each original colony's Δ, independently equal-weighted overall Δ and a **Student-t confidence interval and t test with df = (# independent colonies−1)**. Do not use thousands of repeated bee×trial outcomes as independent colonies. Colony-level sign-flip sensitivity is descriptive and requires symmetry assumptions; the primary t test presumes independent source colonies and approximate normal colony-average contrast. If the number of actual colonies is <12, all outcomes are descriptive pilot findings, not a confirmatory general effect.

**Secondary, locked before main experimental data**: (1) order effect under calm and under wind separately; (2) trial choice of high-reward/difficult vs low-reward/easy, including `no_choice`; (3) whether any landing/contact occurs in 30s, and source-recorded slipping/hovering/contact times; (4) geometric flight direction, heading persistence and physical distance from high-speed video with explicit tracking confidence, not inferred from flower label; (5) per-bee temporal shifts across training and later trials; (6) sham-cue visual/robot noise negative-control pilot. These are diagnostics subject to multiplicity and cannot replace the primary contrast if negative. A behavioral mechanism claim would require direct manipulation of informational content vs recency in a separate experiment.

## Acquisition, IDs, integrity and blind controls

Required source record per randomized trial: `colony_id, bee_id, trial_id, block, trial_in_block, assigned_wind, assigned_order, assigned_high_reward_side, physical_L/R flower coordinates, cue1/2 reveal hardware clocks, trial_release_time, 3D wind vector and turbulence, individual video track confidence, feeder calibration ID, initial/final weights, actual consumed sucrose mass, sucrose w/w concentration, leak/spill blanks, landing/contact/handling failures, data-quality status, operator_id, treatment compliance`. Explicit no-data and censoring states are not fabricated success zeros.

- Hardware clock synchronization is measured; require cue1 < cue2 < gate release and both options accessible at release; videos and balances checked. All assignment and measurement artefacts have raw digest receipts. Camera/observer automated scorer must be blinded to assigned cue-order and trial outcome during validation; recording software can know treatment for event markers.
- One flower-location and cue-icon rotation system; per-block balanced lateral assignments are the *observable randomized design*, do not hand-pick favorable bee or reward pairings.
- Data recorded to append-only files; pre-registered ID/field validation and randomization hash check prior to outcome model. Any missing outcome/different actual wind is reported by assigned arm, and analysis retains intention-to-treat assignment. **Do not silently discard an unsuccessful landing, low activity, strange flight path, and no-drink trial.**
- Freeze seed and full allocation in a **private, access-controlled study register** before animal testing. Public CI uses only **synthetic colony/bee IDs and a fixed QA seed**, publishes only summary counts and a schedule digest, *not actual concealed randomized assignments*.

## Precision/power planning — assumed, not fitted, parameters

Power is evaluated analytically on the **independent colony-average 2×2 interaction estimator** for a balanced design with `B=12 bees/colony`, `T=16 trials per bee per cell` and variance assumptions:

```
sigma_colony_Delta = 0.025 mg/s
sigma_bee_Delta    = 0.030 mg/s
sigma_trial        = 0.080 mg/s
Var(Delta_colony)  = sigma_colony_Delta^2
                   + sigma_bee_Delta^2/B
                   + 4*sigma_trial^2/(B*T)
```

Power scenarios explicitly span independent colonies **8,12,16,24,32,48**, hypothesized true wind×cue-order interactions **Δ={0.010,0.020,0.030} mg sucrose/s**, and a high colony-heterogeneity stress case `sigma_colony_Delta=0.040`. These are **illustrative and uncalibrated**; the per-trial outcome has a zero mass and may be non-Gaussian. Use noncentral Student-t power (independent colonies, df=C−1), not a naïve independent-visit Z-test. This analysis does not manufacture an empirical effect and is not sufficient for animal ethics approval without a real feasibility pilot.

## Identifiability and nontrivial predictions

A two-factor randomized experiment can estimate:
1. `wind×cue-order interaction Δ` in realized feeding rate, even after holding physical alternatives and total final information fixed.
2. Whether geometrical route continuation (pre-choice heading) and handling difficulty are associated with **measured choices** or actual measured feeder intake and whether they mediate cue-order response (mediation remains observational without further intervention).
3. Whether an order effect is present when no actual information differs (separately randomized sham) and whether effects persist in separate colonies, distinguishing true cue content from generic shutter timing and laboratory apparatus.

It cannot infer a neural algorithm, cognitive optimal cue order, individual fitness, cross-species competitive replacement, natural ambient-wind responses, or a universal `C_A/C_F` without additional studies. If the primary Δ is null, **report it**; do not change wind strength or cue timing after inspecting outcomes. If the order effect is present only in wind despite constant post-reveal information, the narrow causal claim is a context-dependent benefit/cost of cue presentation order under controlled flight stress, **not automatically evolutionary adaptation**.

## Stopping condition

This branch creates a **simulation/validation-ready prospective design, not an actual field or laboratory execution**. No real trial results, colony assignments, power findings derived from animals, or treatment causality are claimed. Do not merge this into frozen V5/V6 manuscript results as evidence; it belongs in a future experimental protocol or preregistration.
