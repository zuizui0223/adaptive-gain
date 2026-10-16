# On-policy equivalence and randomized off-policy support for cue acquisition

**Status:** supporting identification and prospective experiment-design audit for `adaptive-gain` PR #68. This is not a new general causal inference result, a fitted bee sensory model, or evidence of natural selection. The frozen V5/V6 manuscript surfaces are not changed.

## 1. Question

The previous ordered-readout result showed that measuring cues separately or simultaneously does not recover how actively inspecting one cue affects the next cue. A second identification obstacle remains: **even genuine sequential logs are insufficient when the historical organism never tries the counterfactual next cue.**

The reason is standard *sequential positivity* (support) in causal policy evaluation, not a newly discovered statistical impossibility. Knowing exactly what happened under one deployed strategy does not reveal potential observations from an untried strategy without additional invariance assumptions. See the discussion of positivity, consistency and sequential randomization in the 2024 *JRSS B* paper [1].

## 2. A sharp, restricted partial-identification witness

Use two equally common fixed target worlds `Y=0` and `Y=1` and three binary unit-cost cues, with budget two:

- **A**, the context cue, produces a fair bit regardless of target and has no target information.
- **B** has correct readout probability `3/4` whether first or after A.
- **C** has correct probability `3/4` when acquired first; when acquired after A, it has correct probability `s` following `A=0` and `3/2-s` following `A=1`, for unknown `1/2 <= s <= 1`. All other cue histories retain `3/4` accuracy.
- These are stipulated intervention kernels: a readout after actively requesting A is not presumed identical to a passive simultaneous presentation.

Suppose a historical policy **always acquires A then B**, observes both cue reports, and makes a target decision using B. The *entire* population joint log, even with known true targets, is invariant in `s`:

```
P(Y=y,A=a,B=b) = 3/16   when b=y;
                = 1/16   when b!=y.
```

Likewise, first-position calibration of C is `3/4`, and a separate A-then-C experiment reporting only the **pooled** second-cue accuracy gives `(s+(3/2-s))/2=3/4` for every `s`. The unobserved conditional C readout probabilities differ, but these recorded statistics cannot show it.

An independent rational exhaustive oracle enumerates every affordable acquisition tree and optimal terminal target choice. Because wrong actions have zero penalty in this specific accuracy benchmark (`v=1, L=0`, abstention permitted),

```
V_precommitted^*(s) = 3/4;
V_contingent^*(s) = 3/4 + |s-3/4|/2;
Delta(s) = |s-3/4|/2.
```

The best conditional route acquires A and then selects C on whichever A outcome makes C more accurate than B. Fixed acquisition of A followed by C averages back to `3/4`; taking B then C without A yields two symmetric, independent 75%-accurate reports and achieves no better than 75% under 0–1 loss.

Therefore the **sharp identified set for this explicitly restricted s-family**, given the deployed policy plus the stipulated pooled accuracies, is

```
Delta in [0,1/8].
```

If contingent control incurs additional maintenance debit `K=1/20`, its payoff difference is only partially identified:

```
Delta-K in [-1/20,3/40].
```

At `s=3/4` the controller loses `1/20`; at `s=9/10` its value is `33/40` versus fixed `3/4`, and its net gain is `1/40`; at `s=1/2` or `1` it earns `3/40` net. These distinct worlds are **observationally identical under the historical A->B policy**, not merely similar in sample. The interval would not remain sharp outside the stated response-kernel and accuracy-range assumptions.

## 3. Randomized second-cue assignment: what resolves the gap

After observing A, randomly assign the second cue J to B or C, logging the **known experimental assignment probability** `mu(J|A=a)` and retaining the context label. Require `0<mu(C|A=a)<1` for both `a=0,1`, with known target truth, no unrecorded cue reports, and cue-report consistency under the randomized intervention.

For a **prespecified** outcome-contingent evaluation policy `pi(a)` and the terminal rule `predicted target = reported second-cue bit`, the standard inverse-propensity-weighted evaluation estimand is

```
V_pi = E_mu[ I(J=pi(A)) / mu(J|A) *
             (v*I(Z_J=Y) - L*I(Z_J!=Y)) ].
```

This evaluates the *specified report-and-choice policy*, not automatically the Bayes-optimal policy and not heritable fitness. Under the stated randomized assignment and consistency assumptions, its expectation equals the interventional policy reward. Statistical uncertainty for actual bee data must cluster at least by bee (and colony where appropriate), and a discovered policy should be assessed on held-out trials rather than the same data used to choose it.

At `s=9/10`, the prespecified policy `pi(0)=C, pi(1)=B` has value `(9/10+3/4)/2=33/40`, independent of the exploration probabilities as long as the action support is positive. In the static world (`s=3/4`) its value is `3/4`. A fully synthetic 160-row enumeration of the randomized population table, **not 160 independent bees**, reproduces these exact values with the IPW estimator.

### Randomization by itself is not enough if the log loses context

For equal random assignment of B/C in both contexts, overall correct-cue-report probability stays exactly **75% in both environments**, and even the accuracy pooled by second-cue identity stays at 75%. Only the stratified quantities distinguish them:

| After observed A | B correct rate | C correct rate, static | C correct rate, reactive (`s=0.9`) |
|---|---:|---:|---:|
| A=0 | 75% | 75% | 90% |
| A=1 | 75% | 75% | 60% |

A useful causal experiment therefore needs **assignment randomization and complete ordered history logging**. Randomizing choices and then discarding A's earlier report reintroduces the identification failure.

## 4. Runnable intake gate and source discipline

The new `adaptive_gain/policy_support.py` is a deliberately limited two-stage evaluator. It requires rows with: `trial_id`, `bee_id`, known experimental `target`, perceived/reported `context_bit`, experimentally `second_cue` (1=B, 2=C), independently obtained binary `second_report`, and the actual assigned arm's `assignment_probability`. It rejects missing reports, missing policy-arm observations for either context, invalid propensities and duplicate trial IDs. It reports both raw Horvitz–Thompson and self-normalized point estimates, match counts and an importance-weight effective sample size. **It does not supply confidence intervals, support causal interpretation without randomized assignment, or correct selection into responders.** The inverse-probability effective sample size is not a biological sample size and cannot replace bee-/colony-clustered inference.

For a real pollinator, the *internal perception* of a cue is not directly observable. A separate behavioral reporting assay or independently validated surrogate is needed before a `second_report` can stand for perceived evidence. Merely recording the final flower visited and inferring what was perceived from that final action would be circular. If a trial has no valid report, keep it in the protocol accounting and specify a detection/missingness model or a no-response endpoint; do not drop it and claim a calibrated report-level effect. Likewise, a planned randomized cue arm that does not occur in one A context fails the observed-support gate even though its design probability is positive.

Each cue-request timestamp and bee/colony/block identity should be retained in the raw study dataset (outside the minimal estimator), along with training phase, experimenter/blinded scoring, target, stimulus side, no-choice, and failure reasons. Acquisition changes that depend on elapsed time or cross-trial learning should be explicitly stratified or modeled. No number in the 2-world artificial benchmark is an a priori natural bee effect size.

## 5. Relation to existing ecology and novelty boundary

Jordan et al. (2024, *iScience*, DOI [10.1016/j.isci.2023.108587](https://doi.org/10.1016/j.isci.2023.108587)) measured multimodal responses to noisy bumblebee stimuli; it does **not** recover the counterfactual sequential kernel required here. Robert et al. (2024, *Behavioral Ecology and Sociobiology*, DOI [10.1007/s00265-024-03432-z](https://doi.org/10.1007/s00265-024-03432-z)) report learning-related changes in bee visual attention, motivating why acquisition history may matter. Standard sequential causal inference already recognizes the consistency, sequential randomization and positivity requirements [1]. This addition is an **audit of what the routeability ecological test must record**, not an independent method claim or an inference from existing pollinator data.

## 6. Reproduction and promotion gate

- `tests/test_ordered_policy_support.py` provides 21 exact Fraction tests, independent full policy-tree checks and logged-distribution equality.
- `tests/test_ordered_policy_support_estimator.py` provides 8 intake-gate and randomized-exploration tests for the small report estimator.
- Local partial harness (previously 523 tests) runs with **552 passed**, zero failures. This is not a complete GitHub checkout.
- New-head full GitHub Actions CI must be checked separately. No frozen manuscript or other existing file is edited.

[1] *Policy evaluation for temporal and/or spatial dependent experiments*. Journal of the Royal Statistical Society, Series B (2024). https://academic.oup.com/jrsssb/article/86/3/623/7511800
