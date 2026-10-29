# Stage 9 — verified PROSPECTIVE randomized bee cue order × wind experiment package

**Date: 2026-10-29. Status: PROTOCOL, SYNTHETIC RANDOMIZATION, ASSUMED-VARIANCE POWER, FUTURE TRIAL SENSOR CONTRACT and COLONY-LEVEL ANALYSIS IMPLEMENTED AND TESTED; NO REAL ANIMAL EXPERIMENT HAS BEEN CONDUCTED.**

This Stage 9 package provides a falsifiable causal next experiment after the original-data PoMS observational wind association and independent bee movement, choice-history and colony-level source analyses. It must not be treated as evidence that manipulating cue-revelation order has *already* changed real insects or energy intake.

[Stage 9 experimental source/protocol](PROTOCOL_CAUSAL_CUE_ORDER_WIND_2026_10_29.md) — freeze actual treatment cues, wind pilot, animal sample, colony recruitment, and concealed random allocation before any real experimental source observations.

## 1. The one decisive randomized causal estimand

**Order `O`:** show reward-information cue first vs show floral handling/friction-information cue first. **Wind `W`:** equipment-sham calm vs instrumented, independently pilot-calibrated moderate crosswind. Both artificial flowers are equally distant and symmetrically located, with a reward/handling trade-off; high-reward difficult option is left/right counterbalanced in every bee/condition block.

Cue 1 revealed at t=2s, cue 2 at t=4s, both physical flower options simultaneously available at t=6s; all trials use the same fixed 30s post-release outcome window. All cue information is available by choice time, so the treatment varies **presentation order/recency, not the total information ultimately presented**. Sensory salience, physical handedness and shutter sounds require blinded mechanical pilot verification.

**Primary outcome** is verified actually consumed **mg sucrose in 30s /30s (mg/s)**. No drink/no successful landing/no choice with functioning source instruments is **true zero intake**, not missing. Calibration, feeder leak and spillage, video-confirmed contact and hardware timing are preconditions to classifying a mass decrement as ingestion. Device failures must never silently become zero or complete-case exclusion.

Primary signed colony-equal contrast:

```
Delta = mean independent colony c [
     mean bee b in c [
       (Ybar[reward_first, crosswind] - Ybar[handling_first,crosswind])
       -
       (Ybar[reward_first, calm] - Ybar[handling_first,calm])
     ]
   ]
```

**H0: Delta=0 (two-sided α=.05)**, t confidence interval and t p-value across actual **independent experimental colonies**, df=number of independent colonies−1. The full analyzed dataset includes *every assigned trial*. No thousands-of-trials-as-independent-animals model. If independent colonies <12, report descriptive pilot only. This estimates the causal effect of **randomized cue presentation order under a crosswind relative to calm** if assignment, adherence and measurement are valid. It **cannot** distinguish cognitive search/query order from stimulus recency, expectancy, attention or other intervening states without further experimental controls.

## 2. Deterministic synthetic-only allocation — no future experimental secrecy leak

Source implementation `randomization.py`; frozen QA pseudorandom seed 20261029, but **real experiment requires a newly generated private seed and concealed trial assignments in an external study register**, not the public seed or publicly posted schedule.

The example scheduling configuration was successfully checked:

| Randomization property | Prospective example count |
| --- | ---: |
| Independent original colonies | **24** |
| Tagged bees per colony | **12** |
| Source 16-trial wind blocks per bee | **4** |
| Real randomized trials *planned* per bee | **64** |
| Assigned trials per bee per order×wind cell | **16** |
| **Synthetic allocation records tested — not actual animal trials** | **18,432** |
| Balanced total QA records per 2×2 cell | **4,608** |

Each bee's four wind blocks follow `calm–crosswind–crosswind–calm` or the reverse in an ABBA/BAAB-style counterbalanced crossover. Each 16-trial wind block independently shuffles four copies of every `(reward-first/handling-first) × (high-reward difficult flower left/right)` pair. Hardware timing is identical across cue-order arms and both flowers become available only after the second reveal.

Automated hard failures: duplicated or missing trial IDs, erroneous arm labels, unbalanced order/side cells, changed cue-reveal or gate times, wind switching inside a block, wrong bee/colony replication, or unequal 2×2 cell sizes. **Only SHA256 digest and aggregate counts of the *synthetic* QA allocation are uploaded, not a real or simulated participant-by-trial assignment file.**

## 3. Independent-colony power calculations — purely hypothetical

Implementation `power_assumptions.py` evaluates **noncentral Student t** power for independent colony-level interaction contrasts. These are **assumed** standard deviations in mg/s, not empirical estimates from previous bee papers:

```
sigma_colony_interaction = 0.025 mg/s (high-heterogeneity sensitivity 0.040)
sigma_bee_interaction    = 0.030 mg/s
sigma_single_trial      = 0.080 mg/s
B=12 bees/colony, T=16 trials per bee per 2×2 cell
Var(Delta_colony) = sigma_colony_interaction²
                 + sigma_bee_interaction² / B
                 + 4*sigma_single_trial² / (B*T)
```

| Distinct original colonies | Power if true Δ=.020 mg/s and σ_colonyΔ=.025 | Power if σ_colonyΔ=.040 |
| --- | ---: | ---: |
| 8 | 39.5% | 21.1% |
| 12 | 59.0% | 31.9% |
| 16 | 73.6% | 42.1% |
| **24** | **90.1%** | **59.8%** |
| 32 | 96.7% | 73.2% |
| 48 | 99.7% | 89.1% |

The original script also evaluates assumed Δ=.010 and .030 mg/s and the entire 8–48 colony grid. These exact powers only hold under **independent Gaussian colony contrasts with those assumed variances**. Actual success/no-intake zeros, effect heterogeneity, carryover, unreliable cameras, physical wind, welfare/feeder issues and independent-colony recruitment may change detectability dramatically. **24 colonies are not intrinsically sufficient**, particularly at σ_colonyΔ=.040. An *independent, outcome-blinded* mechanical/feasibility pilot must lock the physical wind speed and realistic variance before preregistration. The outputs are not real effects nor an achieved prospective power commitment.

A separate Gaussian-only synthetic QA injected hypothetical **+0.020 mg/s** and recovered **+0.020167 mg/s**, with a *synthetic-only* t confidence interval **[+0.009496,+0.030837]**. Its mock p-value **must not be used in a manuscript or presented as measured insect behavior**; it validates mathematical and coding consistency only.

## 4. Original-data acquisition contract ready for future actual execution

Implementation `future_source_contract.py` requires, for **every randomized and source-labelled trial**, before applying the ITT estimator:

- Original assignment ID and exactly one outcome per ID; no missing source device records, fabricated successful events or duplicate trial IDs.
- Actual instrument-recorded first-cue reveal, second-cue reveal, and both-flowers access clock; configured 2s, 4s, 6s with **±0.20s** hardware tolerance. Actual cue1 < cue2 < access gate is mandatory.
- Real **measured wind 3D vector**, scalar vector speed, turbulence SD and synchronized camera/anemometer clocks; measured wind exposure range obtained from a **separately pilot-locked calibration**. The input parser rejects missing/overlapping pilot calm/crosswind ranges, nonexistent wind measurements and inconsistent vector speed.
- Both physical flowers must be available at release; all hardware adherence failures retained by *assigned randomized condition* rather than deleting those outcome trials. **≥98%** protocol adherence in *every* 2×2 cell is a locked condition for promoting the designed mechanistic analysis; below this return an explicit NO_GO without retuning thresholds, although the assignment ITT population remains present.
- Positive feeder mass loss is called actual sucrose ingestion only with validated source animal feeding contact, mass calibration and spillage correction. No contact or no choice cannot silently receive a positive amount. A verified zero remains zero; a failed sensor returns NO_GO rather than a bogus biological non-visit.
- Analyzable outcomes go to `colony_contrast.py` for exact original colony clustering and Student-t df. Secondary high-frequency video flight heading, flower contact/hover/slip, and alternative availability are recorded for mechanistic follow-up but never substituted for the primary `Delta` after results.

These are **future data acceptance gates**. The current CI uses *generated mock telemetry only* and explicitly labels it nonempirical.

## 5. Verification and scientific stopping rule

Dedicated original-code (NOT animal data) GitHub Actions CI [run 40842131461](https://github.com/zuizui0223/adaptive-gain/actions/runs/40842131461) **SUCCESS, all 33 focused randomized design, source contract, independent-colony inference and exact t-power tests passed**. Uploaded machine-readable QA receipts:
- `cue_order_wind_randomization_qa_receipt.json` — fake assignment cell counts, SHA256-only commitment; no per-trial schedule.
- `bee_stage9_assumption_only_power.json` — full independent-colony assumed-variance and target-sample grid.
- `bee_stage9_synthetic_colony_estimator_QA.json` — injected synthetic effect recovery/CI marked no real animals.

**Ecological conclusion today:** Stages 3–8b contain bounded observational evidence that wind, geometry, orientation and temporal order organize different aspects of pollinator visits. Stage9 now has an **executable causal identification plan** for wind-dependent cue presentation order, but **the causal hypothesis has not yet been tested on living bees**. No fitness, C_A/C_F, cross-species response, wild flower community competition, or neural cognitive query-order effect is yet established. Report null future Delta if observed; do not rescue it by changing wind speed, cue order times, colony inclusion or sensory stimulus after peeking.

Do not fold this mock design into frozen V5/V6 theoretical submission papers or claim sample-size projections are empirical. Future animal-welfare approvals, concealed allocation, instrument procurement and independent colony recruitment are **external human actions**.
