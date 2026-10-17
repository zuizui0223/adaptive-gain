# Missing outcomes, no-choice behavior and the routeability experiment

**Status:** Supporting ecological observation/identification audit for `adaptive-gain` PR #68. Synthetic data only, not a measured pollinator effect, new theorem family, or submission-surface revision.

## 1. The problem after randomized cue access

Previous PR #68 work identified an untried branch in a historical `A -> B` policy. Randomizing the second cue B/C conditional on the first observed A, and logging its propensity and result, permits evaluation of a **prespecified** second-cue policy under consistency and sequential randomization. The existing `adaptive_gain/policy_support.py` intentionally refuses any missing binary cue report rather than declaring an effect from complete cases.

A further ecological distinction is necessary: **no-choice/no-action is a possible observed behavior**, while **unobserved** means camera failure, lost trial metadata, occluded response, or other inability to score the action. No-choice is not a latent cue misread, and neither state should silently disappear from the analysis.

An example in published bumblebee work: Yousry, Henderson & Sprayberry (2023) defined a no-choice category after repeated approaches without a response, and specified exclusions tied to whole experimental sessions with no choices (DOI [10.3390/agrochemicals2020013](https://doi.org/10.3390/agrochemicals2020013)). These decisions are specific to that study and cannot substitute for a preregistered outcome ontology in this one. General missing-outcome bounds and sensitivity analysis are established methods (e.g. [Addressing missing data in randomized clinical trials: A causal inference perspective](https://pmc.ncbi.nlm.nih.gov/articles/PMC7337281/)). **Neither precedent is a novel finding of this repository.**

## 2. Explicit outcome ontology and biological estimand

The primary randomized *access-policy* experiment should compare the actual offer of outcome-dependent next-cue choice versus the offer of a precommitted matched-cost cue schedule, with every randomized trial retained. Separately, a randomized second-cue **exploration** experiment can value a specified hypothetical cue-selection rule. Those are different causal estimands.

Each randomized exploration trial carries a known true target `target`, preceding perceived/reported context `context_bit`, assigned next cue `second_cue` and its **known assignment probability** `assignment_probability`. It also has independent `trial_id`, `bee_id`, and one of the mutually exclusive **final-action** statuses:

| `outcome_status` | `final_action` | Meaning | Scored payoff |
|---|---|---|---|
| `choice` | target label `0` or `1` | Valid observed final choice | `+v` if correct, `−L` if wrong |
| `abstain` | `None` | Confirmed observed no-action/no-choice **within a declared exposure deadline** | `0` by explicit model assumption |
| `unobserved` | `None` | Final action not observable/scorable | Unknown, conservatively `[−L,+v]` |

**Action observation is distinct from cue-report observation.** A bee might show an observable final visit despite an unobservable internal cue experience. The new module bounds final-action reward only. The prior `policy_support.py` remains the fail-closed evaluator of separately reported cue responses and does not impute missing perceptual reports. Neither should infer internal perceptual error from final choice.

The `abstain=0` payoff is a **declared theoretical convention**, not a demonstrated opportunity-cost-free bee behavior. Latency or energetic costs of avoidance require a different payoff model and separate measurement. Confirmed timeout without an identifiable decision must be defined prospectively, not arbitrarily relabeled as a voluntary abstention.

## 3. What a finite randomized log does—and does not—identify

Fix a **prespecified** cue policy `pi(context)` and a logged exploration randomization probability `mu(assigned_cue | context)`. For a complete final action score `R_i`, the conventional Horvitz–Thompson sample score is

\[
\widehat V_\pi=\frac1n\sum_{i=1}^n\frac{1\{J_i=\pi(A_i)\}}{\mu(J_i\mid A_i)}R_i.
\]

If a policy-matched row is unobserved, the unobserved final action can yield any allowed payoff between `−L` and `+v`. Replace those missing matched outcomes by their extremes while retaining **all randomized trials in the denominator**. This gives two **sharp completion endpoints for the realized sample HT score**. It does **not** give a confidence interval, sharp population causal identified set, randomization-inference coverage interval, or estimate of evolutionarily realized fitness. Inverse weighting can produce finite-sample scores outside the per-action payoff range; do not clip the raw HT result and mislabel it a population probability.

There are two distinct problems: (i) missing action outcomes, handled here only by worst/best-case completion; and (ii) the randomization mechanism or action-consistency assumption itself, **not tested** here. A nominally positive propensity on a design sheet does not guarantee observed policy-arm support, nor does recording `bee_id` eliminate correlation from repeated trials.

The code rejects duplicate trials, illegal status/action combinations, invalid or unknown assignment probabilities, missing policy-matched support in either context, and unknown final actions masquerading as `abstain`. It returns sample counts, weighted endpoints, match counts by context, importance-weight effective sample size and the number of distinct bee IDs. It intentionally does not calculate cluster bootstrap intervals, infer target-choice preferences, or estimate a selection coefficient.

## 4. Independent synthetic counterexample

Construct 200 **synthetic randomized trial records, not 200 independent bees**, with 50 records per `(A-context, assigned second cue)` combination (25 trials for each experimentally known target label in every combination) and `mu=.5`. Exactly 100 records match the target policy `pi(0)=C, pi(1)=B`.

Case I: 80 matched actions recorded (72 correct, 8 wrong), 20 matched actions unobserved. Correct fraction among recorded actions: **90%**. With payoff `v=1,L=0`, the worst/best completed HT scores are **`0.72` to `0.92`**, both attainable by making all missing matched actions wrong or correct. Against a *stipulated* comparison value `0.75` and controller cost `K=0.05`, the score contrast lies in **`[-0.08,+0.12]`**. **The sign is not established by this log.**

Case II: retain 20 missing, but observe 63 correct, 7 wrong, and 10 **confirmed abstentions** among the other 80 matched records. Accuracy among the 70 *choosers* is still **90%**, but the reward-score completion range becomes **`[0.63,0.83]`**. Treating the 10 no-choices as technical missing would widen this range and invent uncertainty; discarding them and quoting 90% would overstate action success.

At error penalty `L=3` in Case I, the sample HT payoff-score interval widens to **`[-0.12,0.68]`**, because every unknown action might be wrong. This is a sensitivity result, not evidence that the unknown bees actually made mistakes.

A separate exact 200-row synthetic design with nonuniform known randomization probabilities also recovers its prespecified policy score when all actions are observed. The regression suite confirms that the original `policy_support.py` point estimator agrees with the new bounds when final actions are fully observed and identical to separately elicited cue reports.

## 5. Field protocol and stopping rules

Record for **every randomized offer**, regardless of whether the bee visits: trial/bee/colony identifiers, time block and learning stage, context stimulus truth and independently elicited first response, experimentally assigned second cue and actual assignment propensity, full cue identity/order/readout timestamps, independently observed final choice (or confirmed no-action), observation completeness and explicit technical failure reason. Camera/observer disagreement should remain visible. Time since last reward, motivation and access to the opportunity must be recorded if they may affect no-choice.

- **Primary outcome (policy access intervention):** reward or probability of correct final action under randomized access to conditional cue selection versus randomized precommitted cue access, including observed no-choice trials; analyze intention-to-treat with bee/colony clustering and prospectively defined missingness sensitivity.
- **Mechanistic endpoint:** response probability of the *next* cue conditional on known true world, previous cue identity/outcome, lag and order; validate any behavioral cue report as a measure of relevant perceived information rather than equating a final flower choice with cue perception.
- **Secondary hypothetical-policy evaluation:** predeclare `pi`, randomize actual next-cue assignment with positivity in every relevant context and evaluate with logged propensity. Estimate a held-out policy when using the same data to learn `pi`; the toy bounds are not a substitute for confidence intervals.
- **No-go:** if the distinction between confirmed no-choice and recording failure is unavailable, or if a relevant context/assigned-cue arm has zero observed support, do not claim an identified adaptive routing advantage. If missingness completion bounds include the maintenance-cost crossover, report the sign as unresolved.
- **Novelty ceiling:** no-choice accounting, Horvitz–Thompson weighting, and missing-outcome worst/best bounds are standard statistical methods; the useful contribution is a reproducible observation and falsification contract for the biological routeability prediction.

## 6. Reproducibility and exclusions

- `adaptive_gain/action_outcome_bounds.py`: strict action-status intake and finite-sample HT missing-outcome score bounds.
- `tests/test_action_outcome_bounds.py`: 27 synthetic tests, including two extreme missing completions, abstention separation, error-loss widening, invalid data, nonuniform assignment and agreement with the prior cue-report estimator on complete records.
- Previous PR #68 commit `0074a6b3cc0d4bb94baa2c6a386503cd3d1e1c17` passed full Python 3.10/3.11/3.12 CI.
- Local partial reproduction environment: **579 tests passed** (includes the 27 new tests). The local environment is **not** a full GitHub clone; the new-head full CI is a separate gate.
- No existing solver, frozen manuscript or main novelty theorem is modified.
