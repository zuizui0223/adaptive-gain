# Joint readout correlations are an independent ecological-information assumption

Status: **supporting assumption audit for adaptive-gain PR #68**. No new general theorem, organismal measurement, fitness estimate or network-rewiring result is claimed. Frozen V5/V6 submission surfaces are unchanged.

## Question

Does a known **10% marginal error rate per cue** suffice to predict whether conditional cue acquisition repays its maintenance cost? No. A finite counterexample holds the target states, cue vectors, prior, deadline, per-cue error and payoff fixed, while changing only the **joint dependence of the error events**.

The construction reuses the five-state A/B targets `(0,1,1,0,0)` and three binary unit-cost cues from `experiments/DEADLINE_REWARD_ABSTENTION_AUDIT_V1.md`. The prior is `(1/3,1/6,1/6,1/6,1/6)`. At most two distinct cues can be acquired. Each query is acquired once and the errors have one latent realization **per encounter**. The participant observes noisy answers, not the true cue values or the error pattern. A correct target classification earns `v=1`, an incorrect one `-L`, and abstaining zero. The nonadaptive comparator selects an affordable subset before observing any outcomes, but is allowed partial-information decisions and abstention.

## Two channels with identical marginal accuracy

Let `E_j=1` mean cue `j` is flipped relative to its latent truth. In both channels `P(E_j=1 | world)=epsilon=1/10` for every cue and every world.

- **Independent:** all three errors are sampled independently, `P(E=e)=epsilon^sum(e) (1-epsilon)^(3-sum(e))`.
- **Fully shared:** a single hidden `E~Bernoulli(epsilon)` is drawn and `E_1=E_2=E_3=E`.

For intermediate dependence, with probability `rho` sample the fully shared vector and with probability `1-rho` sample independent errors. The resulting joint law has **the same univariate confusion matrix for every rho**, and its pairwise error correlation is exactly `rho` for `0<epsilon<1` and at least two cues. The mixture model is an abstract mechanism probe, not a fit to any bee's perceptual system.

## Exact reward comparison at L=4

Both policies are reoptimized for each channel and use the *same channel model* (no mismatch in the observer's prior or expectations).

| Model, topology A | Optimal adaptive reward | Optimal fixed-subset reward | Conditional premium | Net with K=0.1 |
|---|---:|---:|---:|---:|
| Independent (rho=0) | `28/75` | `3/10` | **`11/150`** | `-2/75` |
| Perfect shared (rho=1) | `5/6` | `3/5` | **`7/30`** | `2/15` |

Both channels give **90% correct single-cue readouts**, yet the independent channel fails to repay a controller cost of 0.1 and the fully shared channel repays it. This is *not* caused by changing the biological state vector, the number of cues, the target mapping, the available budget, or the reward function.

The difference is not confined to a discontinuous endpoint: under the fully supported mixture at `rho=1/2`, the same A premium at `L=4` is `2/15`, exceeding 0.1. Thus the cost-repayment sign already changes at an interior, full-support correlated channel.

**Prior-art boundary.** Common-mode noise cancellation and beneficial noise correlation in codes are known phenomena (for example [1]). The specific finite-routeability consequence above is a model-level assumption audit, not a new general principle of sensory coding.

## Why an apparent positive-error no-go may fail

With a common hidden flip, simultaneous readouts satisfy

```
observed_bit[j] XOR observed_bit[k]
= true_bit[j] XOR true_bit[k].
```

The shared error **cancels from the pairwise contrast**, even though neither single readout is error-free. The A policy may query `root`, then choose `left` or `right` according to the perceived root answer. At `L` sufficiently large (when only target-certain classifications have positive value), this policy certifies probability mass `3/5`. The best budget-matched precommitted subset certifies only `1/2`. Both values are independently verified by complete enumeration of all feasible two-query trees and partial subsets. Their *high-loss conditional premium* is therefore `1/10` rather than zero.

Under independent, full-support flip noise, **every** affordable history remains possible under every world. With fixed strictly positive priors, the maximum posterior odds is finite (`14` for this task, epsilon=0.1, budget=2), so for `L >= 14` both policies obtain zero gross reward and the conditional premium vanishes.

Under the shared law, some joint histories **exclude** the opposite target, giving infinite posterior odds and nonzero certified value even as `L` grows without bound. **Positive marginal error is not equivalent to full-support joint evidence.** The previous full-support no-go remains mathematically correct, but cannot be invoked from single-cue calibration accuracy alone.

## Near-shared channels and a second noncommuting limit

For `0 <= rho < 1`, the independent component gives every binary joint error pattern strictly positive probability (when `0<epsilon<1`). Therefore all finite feasible posterior odds are finite, and both policies eventually abstain at sufficiently large error cost.

The A all-abstention threshold for the particular `t=1/3,epsilon=1/10,B=2` setup, from exact subset/outcome enumeration, is:

| rho | Largest attainable posterior odds for topology A |
|---:|---:|
| 0 | `14` |
| 0.1 | `47/3` |
| 0.5 | `29` |
| 0.9 | `149` |
| 1 | `infinity` |

This matches `(14+rho)/(1-rho)` on the four audited finite values; the displayed equality is **not promoted as a theorem over all rho** here. The finite-state oracle, rather than an assumed smooth extrapolation, establishes every shown number.

As `rho` approaches one from below, its finite all-abstention cutoff can become very large. Nevertheless, at every `rho<1` its **eventual** high-loss conditional premium is zero. At `rho=1` the same premium tends to `1/10`. This gives the following model-specific noncommuting limits:

```
lim_(rho -> 1-) lim_(L -> infinity) Delta_rho(L) = 0
lim_(L -> infinity) lim_(rho -> 1-) Delta_rho(L) = 1/10
```

Finite policies and finite joint probabilities are continuous in `rho` at fixed finite `L`. The difference arises solely because perfect common-mode dependence removes some opposite-target observation histories from the support. This is a *support change*, not a smooth increase in individual cue reliability.

## Biological test and interpretation gates

A controlled experiment should compare the full **joint confusion matrix** of two or more cues (estimated from matched-trial perception calibration), rather than just two separate 90%-accuracy scores. Candidate settings include environmental disturbances that affect multiple visual cues together, but these exact all-flip patterns are an abstract coding example and **are not known to describe visual–olfactory errors in bees**.

To isolate the mechanism, manipulate common-mode versus independent errors while preserving per-cue marginal confusion, target prevalence, offered payoff, and query acquisition cost. Randomize within actors and include an explicitly precommitted partial-subset control. Record *which cue was requested next after each perceived outcome*, correct/incorrect/abstain, and query latency. Observe the animal's received cues directly or use independently verified external stimuli; inferring internal cue outcomes from its eventual flower choice would be circular.

Do not interpret noisy-readout cue partitions as perfect deterministic `(C_A,C_F)` guarantees, nor read a change in observed visitation as network rewiring without correcting detection and ecology. The sign of `Delta-K` is a **decision-payoff comparison**, not evidence of heritable fitness differences or natural selection. If future experiments find no effect of experimentally varied noise dependence despite verified cue discrimination, the animal may not exploit the ideal conditional policy and the theoretical bound is not a behavioral prediction.

## Reproducibility and verification

- Added `adaptive_gain/joint_bitflip_reward.py`: independent/shared error mixture, finite joint-noise reward optimizer, and all-abstention threshold.
- Added `tests/test_correlated_bitflip_reward.py`: 169 focused tests, comparing the production solver with a **separate exact Fraction oracle** over full latent-world × joint-error response tables, including independent recovery, mixed channels, baseline and high-loss controls.
- Local harness contains current and previous two reward modules and their tests: **402 tests passed**, all from the small local bundle; the **full repository CI at the new commit is a separate gate**.
- Earlier PR #68 commit `43919232bd39ca881df2459f533cfb1725d4bfcf` has a complete successful Python 3.10/3.11/3.12 matrix.
- This audit does not modify the frozen manuscripts or the earlier noisy-reward implementation.

## Relevant previous work

[1] *Correlated Neuronal Discharges that Increase Coding Efficiency during Perceptual Discrimination*. *Neuron* 38 (2003), 649–657. https://doi.org/10.1016/S0896-6273(03)00287-3.

[2] Jordan, K. A., Sprayberry, J. D. H., Joiner, W. M. & Combes, S. A. (2024). *Multimodal processing of noisy cues in bumblebees*. *iScience* 27, 108587. https://doi.org/10.1016/j.isci.2023.108587.

The former shows why positively correlated noise can sometimes be useful in sensory coding; the latter is an ecological motivation for testing noisy multisensory responses. Neither demonstrates that pollinators use the fully shared-flip channel in this audit or identifies the predicted maintenance-cost switch.
