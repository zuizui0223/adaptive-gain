# Stage 6 — original tracked bee route-turning geometry versus individual previous-flower history

**Date 2026-10-28. Status: ORIGINAL-DATA MODELS COMPLETED; POSITION-CHORD TURNING INFORMATION REPLICATES WITHIN THE HELD-OUT FINAL DAY, WHILE FIXED FIRST-ORDER INDIVIDUAL HISTORIES ADD NO CONSISTENT PREDICTIVE VALUE ONCE TURNING IS INCLUDED.**

Dedicated verified [GitHub Actions run 40609900467](https://github.com/zuizui0223/adaptive-gain/actions/runs/40609900467), **SUCCESS**, all **8 Stage6 synthetic numerical/source-grain tests passed**, original publisher supplementary S1 and original Fig2 SHA-256 checks passed. Original source raw data are not stored in Git. [Pre-outcome Stage6 protocol](PROTOCOL_TURN_INERTIA_2026_10_28.md).

## 1. Specific test

The original publication Pasquaretta et al. (2019), *Movement Ecology* 7:4 (https://doi.org/10.1186/s40462-019-0150-z), source **Dataset S1** contains physical flower visitation *order* within 881 complete original tagged-bee foraging bouts: 6,205 visits, 5,324 adjacent **within-bout** flower pairs, 10 individuals, day 1–5. Source CSV exactly 61,316 bytes, SHA-256 `0d30b0957c4b18602beebf60a915e03bee26142a8593f252badd77881b5e9dfe`.

An additional independent source, the original journal **Figure 2**, gives actual Cartesian coordinates in metres for each of the ten artificial flowers. Figure original PDF SHA-256 `7f275a219fe0128d30f70cf6d812ab41d4b64727a740102549e8362b83d4ff8b`. Frozen verified coordinate map is in `../bee_behavior_stage5/flower_positions_figure2_verified.json`.

Unlike Stage4's previous-flower `A→B` prediction and Stage5's pure `d(B,C)` distance prior, **Stage6 tests three successive original visits** `A→B→C`, all in **the same source foraging bout** with `A≠B` and `B≠C`. The two physical endpoint chords define a position-derived direction cosine `cosθ = (B−A)·(C−B)/(|B−A||C−B|)`. This can represent geometrically continuing forward (cosθ>0) versus turning back (cosθ<0), not observed physical flight heading or an individual bee's own measured visual information.

## 2. Verified denominator and exclusions

| Exact original source quantity | Value |
| --- | ---: |
| Original recorded day1–5 visits / bouts | **6,205 / 881** |
| All original within-bout flower pairs | **5,324** |
| Earlier day1–4 bouts/visits/pairs | 667 / 4,441 / 3,774 |
| **Earlier day1–4 eligible heading triplets** (both adjacent flower steps nonzero) | **2,824** |
| Day5 bouts/visits/pairs | 214 / 1,764 / 1,550 |
| Day5 all within-bout triplets (without filtering) | 1,336 |
| Day5 triplets with repeated first adjacent flower | 71 |
| Day5 triplets with repeated second adjacent flower | 74 |
| **Day5 eligible actual two-step flower triplets** | **1,203** |
| Day5 independently tagged bees with support ≥5 triplets | **10/10** |

The 71 and 74 repeat-exclusion categories overlap and must not be summed as disjoint losses. There were no new cross-bout transitions, no source-level flight-trajectory observations and no inferred flower arrival times. Every considered destination is one of the **nine different physical flowers** from the current B, with strictly positive model probability including beyond the source's rough visual-radius threshold.

## 3. Locked prospective model comparison and training-only regularisation

Exactly the same 1,203 final-day `A→B→C` records enter **all four models**. Per-bee stationary flower margins with fixed Dirichlet α=0.5, the Stage5 Euclidean spatial scale **λ=0.05/m** and bee-specific earlier-day transition history with β=5 are held constant from earlier Stage4/5 protocols.

Stage6's **only newly fitted free coefficient** is a single shared nonnegative direction strength **κ**, which multiplies `cosθ(A,B,C)` in a normalized nine-candidate destination model. κ was chosen **solely on the 2,824 day1–4 source triplets**, before examining day 5, from frozen grid `{0,0.25,0.5,1,2,4}`.

| Training-only κ | Earlier-day mean conditional NLL (nats/triplet) |
| --- | ---: |
| 0.0 | 1.9240 |
| 0.25 | 1.8579 |
| 0.5 | 1.8115 |
| **1.0** | **1.7770** |
| 2.0 | 1.9093 |
| 4.0 | 2.6625 |

Selected **κ=1.0**. This is **not** selected from final-day losses, nor re-fitted per bee. Four model definitions:

- **Mgeo:** source-validated bee-specific static flower preference × `exp(−0.05 d(B,C))`, renormalized over nine alternative flowers.
- **Mgeo+history:** exactly the Stage5 bee-specific learned `B→C` transition counts with β=5 shrinking toward Mgeo, conditional on switching.
- **Mturn:** Mgeo multiplied by `exp[1.0 cosθ(A,B,C)]`, renormalized over nine alternative flowers. A and B are observed previous source flowers; their positions yield an endpoint vector.
- **Mturn+history:** same directional multiplier, same fixed κ=1.0, starting from **Mgeo+history** instead of Mgeo. No extra coefficient or future-state learning.

## 4. Prospective test: direction is the dominant incremental predictor

Primary score is **individual-bee-equal mean held-out proper negative log-likelihood (nats/eligible triplet)**. Lower is better.

| Same day5 source triplets, equal 10-bee weights | Held-out NLL |
| --- | ---: |
| Mgeo | **1.870370** |
| Mgeo+history | **1.833806** |
| Mturn | **1.678962** |
| Mturn+history | **1.754716** |

**Positive directional result (secondary preregistered comparison):**

- Mgeo→Mturn: **+0.1914078 nats/triplet** in bee-equal mean NLL, **9/10** tagged bees positive, one negative; exact within-one-colony sign-flip p=**0.009765625** (descriptive).
- Fitted κ is shared and frozen from the earlier-day subset, so a successful final-day directional result is **genuinely out-of-sample** with respect to that scale parameter.
- A separate source-preserving conditional heading permutation (below) reinforces that the alignment is not only due to fixed current flower B, next flower C, or the bee's marginal incoming-flower use.

**Primary residual history comparison, now geometry+turn corrected:**

- Mturn→Mturn+history = **−0.0757540 nats/triplet** (negative means the historical model actually gives *worse* held-out NLL), with **4/10** bees positive and **6/10** negative; exact within-one-colony sign-flip p=**0.271484375** (descriptive).
- Mgeo→Mgeo+history on the **same 1,203 triplets** = **+0.0365642 nats/triplet**, only **4/10** positive, sign-flip p=0.5703125.
- Adding direction to Mgeo+history improves held-out NLL by +0.0790896 nats/triplet, 7/10 positive, p=0.17969, also imprecise.

**Scientifically supported boundary:** the fixed, source-specified previous-flower history model did **not** add reproducible predictive information to a geometry-plus-incoming-direction model on the final day in these ten bees. This is *not* proof that real bees lack memory. β=5 shrinkage, one static source layout, unknown sensory landmarks, one colony and individual route variation all constrain that negative comparison.

## 5. Separate conditional direction null fixed before empirical test

The original day5 *incoming previous-flower identity A* was permuted **199 times** with fixed RNG seed **20261028**, **within each (bee tag, current flower B)**. This preserves every actual (B→C) outcome, all source B/C relative-distance effects, each bee's source flower-use record, all original day1–4 fitted models, each original model parameter and the number of incoming flower labels among the B-specific visits. It selectively removes *which specific prior direction* preceded each next destination.

| Within-source conditional direction test | Value |
| --- | ---: |
| Day5 eligible source triplets | 1,203 |
| With incoming A realistically exchangeable in their (bee,B) group | **1,176** |
| Bee tags with ≥5 eligible exchangeable incoming triplets | **10/10** |
| Real Mgeo→Mturn bee-equal improvement | **+0.191408 nats/triplet** |
| Randomized incoming directions, 199-shuffle mean | **−0.020412 nats/triplet** |
| Real minus shuffled mean | **+0.211820 nats/triplet** |
| Shuffle-null 5–95% | −0.048936 to +0.007911 |
| Randomized-heading positive-tail Monte Carlo p | **0.005** (one exceedance correction; min 1/200) |
| Mean original incoming labels changed per permutation | 773.1 |

Observed direction-conditioned predictive gain is larger than all 199 predeclared shuffles. This supports **route-order-specific geometric alignment** beyond the previous-flower frequency conditioned on animal and current physical flower. It is **not** a randomized manipulation of animal flight bearing, cognitive information-processing order or physiological decision cost.

## 6. What this changes about the Stage 4 → Stage 6 claim hierarchy

1. **Stage 4:** observed previous flower improves next flower prediction beyond each bee's stationary flower frequency; +0.2065 nats/test transition over all 1,550 within-bout source pairs. This is a real held-out prediction but includes repeat-flower behaviors and physical geometry.
2. **Stage 5:** original Fig2 physical distances improve genuine switched-flower destination prediction; on the 1,462 switched records, +0.1302 nats/switch, 10/10 bees positive. After geometry, a learned first-order historical increment is heterogeneous (5/10).
3. **Stage 6:** source-position **two-step direction** predicts the genuinely distinct next destination in the 1,203 eligible source triplets, beyond static preference and Euclidean distance; directional +0.1914 nats and 9/10 bees positive. Conditional shuffle p=0.005. On those same triplets, adding learned first-order history to direction **does not yield consistent incremental benefit** and on average worsens prediction under fixed β=5.

**The nontrivial surviving result is geometric route continuation, not proven adaptive cognition.** Simply considering physical distance from B to C is insufficient: **the direction from A to B changes which next destinations are predicted** even when B, the bee and Euclidean distances are held fixed. This is more informative than a first-order static spatial kernel and provides a concrete criterion for future ecological movement models.

## 7. Critical inference restrictions and next work

- The source records **flower IDs and bout-level times** only. Triplet-chord orientation is **not a measured individual flight heading, speed, within-flight path, wind, visual cone or perceptual event sequence**. Route continuation can arise from unmeasured landmarks, motion persistence or learned repeatable spatial routes. These are alternative mechanisms, not newly established causes.
- Single bee species, **one colony**, one cage, **one fixed physical arrangement**: 10 bee tags are not ten independent populations/colonies. The p-values here are within-colony temporal/conditional diagnostics only. No ecological microclimate or cross-species generalization.
- All artificial flower rewards were controlled, but **realized reward intake**, fitness and costs of inspecting or choosing flower alternatives were not measured per source visit. No general routeability `C_A,C_F` or evolutionary adaptive-gain inference.
- The original Pasquaretta et al. paper already reported space-use compartmentalization and learned route tendencies. New analysis is an independent prospective *model/control comparison*, **not** a discovery that the paper never established movements to adjacent flowers.
- **Do not respecify κ, smoothing β or select “responsive bees” by held-out results** to rescue significance. Accept the primary negative incremental history and report 4/10 positives alongside direction +9/10 positives.
- The next independent experimental gate is replicating multiple colony/flower-array layouts with *direct flight-camera headings and flower-specific visibility* to distinguish geometric motor persistence, route learning and experimental sensory cue access. PoMS field wind association is a separate ecological finding, not replicated here.

## Reproduction and provenance
- Stage6 dedicated GitHub Actions run [40609900467](https://github.com/zuizui0223/adaptive-gain/actions/runs/40609900467), original publisher SHA256 S1 and actual Figure 2 both validated, all 8 focused synthetic tests passed, exact source and 199-shuffle original result.
- `research/bee_behavior_stage6/turn_inertia_heldout.py`, `run_turn_inertia.py`, `test_turn_inertia_heldout.py`.
- CI artifact `bee_stage6_heldout_turn_inertia.json` contains the full source test, training grid and 10-bee per-model NLL and conditional shuffle receipt. The exact publisher source CSV was not vendored.
- Frozen Stage 4/5 and V5/V6 manuscript outputs not changed.

**Attribution:** Pasquaretta et al. (2019), *Movement Ecology* DOI 10.1186/s40462-019-0150-z; paper CC BY 4.0 with original source attribution and the supplementary dataset's stated terms.
