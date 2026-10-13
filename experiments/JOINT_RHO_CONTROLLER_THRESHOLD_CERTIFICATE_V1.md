# Exact maintenance threshold under partially common sensory errors

**Status:** finite benchmark-specific supplementary result for adaptive-gain PR #68. No change to the V5/V6 frozen theorem surfaces, no claim of a new general Bayesian decision result, and no empirical sensory or fitness estimate.

## Fixed question

In the established five-state topology A (targets `0,1,1,0,0` and three binary unit-cost queries), keep encounter probabilities `(1/3,1/6,1/6,1/6,1/6)`, maximum two acquisitions, reward `v=1`, wrong-target loss `L=4`, free abstention, and constitutive extra controller cost `K=1/10`. The fair nonadaptive comparator selects a *precommitted partial query subset* with the same budget and may use the observations to choose a target or abstain.

Each cue has exactly 10% conditional misread probability for every ecological state. Vary only dependence among the errors. With probability `rho`, all three errors share one Bernoulli(1/10) flip; otherwise each error flips independently with the same probability. Conditional on a world, the error pattern is drawn once per encounter. No actor is given direct access to latent truth or to the hidden flip.

## Exact all-correlation reward envelopes

Let `A(rho)` be the highest expected reward with outcome-dependent next-query choice and `F(rho)` the highest reward with a precommitted budget-feasible cue subset. Every deterministic policy has an expected reward **affine** in `rho`, because the mixture changes only the weights of two fixed sensory channels. After enumerating all query trees, all permitted leaf actions, and all fixed subsets, there are 385 distinct adaptive reward lines and 208 distinct fixed reward lines. Checking each line against the candidate optimum at both endpoints of each segment proves its dominance on the *entire continuous interval* (not merely on sampled values).

The upper envelopes are:

| Correlation range | `A(rho)` | `F(rho)` |
|---|---|---|
| `0 <= rho <= 1/3` | `28/75 + (21/100)*rho` | `3/10 + (3/20)*rho` |
| `1/3 <= rho <= 3/8` | `97/300 + (9/25)*rho` | `1/4 + (3/10)*rho` |
| `3/8 <= rho <= 2/3` | `7/30 + (3/5)*rho` | `1/4 + (3/10)*rho` |
| `2/3 <= rho <= 1` | `7/30 + (3/5)*rho` | `3/20 + (9/20)*rho` |

For each policy-switch interval, the stated pair of lines is *attainable*; the Fraction oracle certifies every other candidate line falls below it at both interval endpoints. The intermediate adaptive policy on `1/3 <= rho <= 3/8` is **essential**. Omitting it falsely suggests a local dip in the adaptive advantage. Independent exhaustive enumeration catches that error.

Thus the **exact conditional-acquisition gross premium** is

```
Delta(rho) =
  11/150 + (3/50)*rho     0 <= rho <= 3/8,
  -1/60 + (3/10)*rho     3/8 <= rho <= 2/3,
  1/12 + (3/20)*rho      2/3 <= rho <= 1.
```

It is strictly increasing throughout this benchmark; its slope changes at policy switches. With controller cost `K=1/10`, the unique zero of `Delta-K` is at `rho=7/18`:

```
Net conditional-control value > 0  iff  rho > 7/18.
Net conditional-control value = 0  iff  rho = 7/18.
Net conditional-control value < 0  iff  rho < 7/18.
```

This threshold depends on the exact finite tasks, prior, error channel, budget, reward/loss, free abstention, and K. It does not establish that higher error correlation *always* favors contingent sensing in ecological systems.

## What calibration would identify (and what it would not)

**Univariate-only observations cannot identify the relevant dependence.** For every cue and world, `P(error_j=1)=epsilon=1/10` under every `rho`. Hence any likelihood formed only from separate single-cue error reports is exactly the same for every `rho`; collecting more such unpaired records cannot determine whether this benchmark's `Delta-K` is negative or positive.

Within this *specified* exchangeable common-mode mixture, **paired same-encounter errors** do identify `rho` at the population level if the truth of both cue bits is known and the internal reports are faithfully measured:

```
P(error_j=1, error_k=1) = epsilon^2 + rho*epsilon*(1-epsilon)
                            = 0.01 + 0.09*rho,
P(error_j != error_k)  = 2*epsilon*(1-epsilon)*(1-rho).
```

Therefore the model's viability threshold `rho=7/18` corresponds to a paired *co-error probability* of `9/200=4.5%` and an error-disagreement probability of `11/100=11%`. These thresholds are **not** valid for arbitrary joint error distributions; same marginal rates and even one pair's covariance do not uniquely identify the entire three-cue error law outside the mixture family. Actual bees' internal percepts are generally unobserved, so behavior-based cue reports require an independently validated measurement model.

Two protocols can be compared:

1. **Paired controlled calibration:** hold true visual/odor/other cues known on every trial, obtain separate verified behavioral cue reports within the same encounter, and estimate a joint confusion table by bee, target state, and environmental stratum. Include no-reports/no-choice and calibration failure outcomes; do not discard them by conditioning silently on choosing. Distinct cue reports must be proven to track the internal evidence relevant for foraging before treating them as latent error indicators.
2. **Causal mechanism test:** randomize independent versus common-mode *external signal perturbations* while keeping marginal discrimination difficulty, deadlines, target frequencies and payoffs constant. Randomize availability of conditional next-cue selection versus matched precommitted access, and record the actual sequence, correctness, wrong actions, abstention and times. Verify that external perturbations induce the intended **joint perceived-error** distribution; physical correlation alone does not guarantee perceptual error correlation.

Even a measured joint-error table cannot by itself tell whether the shared component came from weather, sensory organs, attention, motivation, or shared external perturbations. Causal attribution needs an independently manipulated source or appropriate repeated within-context designs. Do not infer internal error correlation from correct-choice or raw visitation percentages alone.

## Existing biological evidence and novelty ceiling

Jordan et al. (2024), *iScience* 27:108587, https://doi.org/10.1016/j.isci.2023.108587, experimentally studied bumblebees' responses to multimodal noisy floral-like stimuli using FMPER. That work supports sensory-noise ecological relevance but did not calibrate this three-cue error law or conditional-query controller cost. The article discusses extensive no-choice responses and limited resolution for subtle behaviors, emphasizing why response selection matters. Correlated sensory noise and Bayesian reject options are established prior art; this note presents a benchmark-specific quantitative bridge and a prospective validation contract, not a novel general theorem.

## Reproducibility

- `tests/test_joint_rho_maintenance_threshold.py` independently constructs rational reward lines for all feasible policy trees, conditional leaf actions and precommitted subsets; proves all continuous-`rho` intervals by linear endpoint dominance; validates against the implementation on a 101-point grid and checks marginal-error identifiability.
- Before this addition, PR #68 head `dec77bf6fda1a0f5aeb444f50958a5031068ba10` had successful full Python 3.10/3.11/3.12 CI (`38151614444`).
- The new focused certificate has 5 passing tests, and the local partial harness (not a full repository checkout) has **420 passed**. CI at the new head is a separate gate.
