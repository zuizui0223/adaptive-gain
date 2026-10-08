# Held-out randomized query-policy test: the causal comparator

Status: prospective protocol and executable analysis gate for adaptive-gain PR #67. Not an animal experiment, not V6 MAIN 4, not an evolutionary selection coefficient. Policy learning and unbiased out-of-sample validation are established methods (Athey & Wager, 2021, Econometrica, https://doi.org/10.3982/ECTA15732).

## Why separate training and validation

Selecting a query/passive choice for each old report O using noisy data, then valuing that choice on the SAME data, generates an upward-biased adaptive premium. This can happen when true query and passive rewards are identical. Freeze the learned policy on TRAINING colonies and test on disjoint HELD-OUT colonies. If bees from a colony are dependent, colony, not individual bee, is the required independent unit.

The source 2026 bumblebee information-purchase dataset does not include a randomized PASSIVE/SHAM/QUERY dynamic-world experiment; its 19,200 trials cannot supply the following causal contrast.

## Three-arm trial with logged randomization

All trials give the same old information report O before arm assignment, then randomize within O, logging a fixed, strictly positive probability for each arm:

- PASSIVE: no new cue, organism may choose an action time inside [0,T].
- SHAM: matched cue port, motor handling, cue display length, but a calibrated uninformative label; waiting choices permitted.
- QUERY: matched cue port with an informative label of the current target state; post-query waiting permitted.

Environment state transitions are generated independently of animal activity. The reward in all arms must be in the SAME currency: realized terminal food/reward, missed-opportunity penalties and actual cue-acquisition costs, not binary choice accuracy alone if food amounts differ. A cue port that changes the target's state violates the information-only treatment interpretation.

Assigning an arm does not prove that the animal can voluntarily implement the desired report-conditioned acquisition policy. Forced-arm policy value and a later animal free-choice test are distinct research endpoints.

## Policy values and target frequencies

Specify the deployment old-report probabilities omega_0 and omega_1 independently of the experimental frequency. Balanced old-report trials may be useful to measure the rare branch but must not change the ecological weighting.

Let mu(o,a) denote the randomized held-out mean reward in old-report group o and assignment arm a (P=passive, S=sham, Q=query). Freeze from training animals pi(o) in {P,Q}; do not retune the policy or reward scale in held-out animals.

Then:

J_C = sum_o omega_o mu(o,pi(o))
J_P = sum_o omega_o mu(o,P)
J_Q = sum_o omega_o mu(o,Q)
J_S = sum_o omega_o mu(o,S)

The conditional-control premium over the BEST fixed acquisition alternative is

G_heldout = J_C - max(J_P,J_Q)
          = min( J_C-J_P, J_C-J_Q ).

DO NOT clip negative held-out G to zero. The sham contrast J_Q-J_S may indicate a signal-content benefit if QUERY and SHAM match in timing/attention/effort/cost; it does not itself measure conditional control.

For an approximate conservative simultaneous 95% lower confidence statement, cluster-bootstrap the HELD-OUT colonies and take one-sided 2.5% percentile lower bounds of each of J_C-J_P and J_C-J_Q. Require BOTH lower limits >0. This Bonferroni construction is an approximate large-sample guard, not an exact randomized-inference or power guarantee. Reject the analysis if any report-by-arm cell has zero support, if cluster-level bootstrap positivity regularly fails, or if randomization probabilities differ from preregistered values.

## Exact toy design counterexample: average null, positive conditional premium

Illustrative **constructed** expected net reward table:

| Old report | Deployment weight | P | Sham | Q |
|---|---:|---:|---:|---:|
| 0 | 0.20 | 0.70 | 0.65 | 0.90 |
| 1 | 0.80 | 0.80 | 0.70 | 0.75 |

The best conditional schedule is QUERY after old report 0, PASSIVE after report 1. Its expected reward J_C=0.82; both universally PASSIVE and universally QUERY achieve 0.78, while SHAM achieves 0.69. Hence conditional-control G=0.04 although universal Q minus universal P equals zero. Query minus matched sham is positive, +0.09. The query regime can lose to immediate/passive behavior after common reports when acquisition time/handling costs outweigh informational benefits. This is a standard heterogeneous-policy phenomenon, NOT an original theorem.

An aggregate Q-vs-P null cannot rule out a positive old-report-contingent information-acquisition value.

## Nonidentification and experimental stop rules

The evaluator in adaptive_gain/randomized_policy_trial.py measures EXECUTED forced-regime performance, not the theoretical Bayes-optimal payoff envelope. It requires known assignment probabilities constant within old-report strata; if propensities depend on additional covariates/history, the cell-mean estimator is invalid without appropriate inverse-propensity or augmented estimation.

Test the free-choice condition separately to determine whether animals express the conditional schedule. If only experimenter-imposed selection improves payoff, the result establishes an available opportunity, not evolved behavioral implementation. To claim natural selection, additionally estimate genotype-dependent costs and long-run reproductive consequences.

Potential failure modes that trigger HOLD:
- target old-report weights obtained from intentionally balanced lab samples rather than independent ecological frequencies;
- treatment arms differ in available waiting horizon or unrecorded food reward;
- using the same animal/colony to learn and evaluate the policy;
- interpreting external randomized cue delivery as self-chosen acquisition;
- reporting a positive in-sample maximum as ecological adaptivity;
- assuming bee visits within a colony are independent units;
- using the existing He et al. 2026 public dataset as if it recorded synchronized state transitions, optional wait timing and matched sham signals.

No defensible power target is available without empirical pilot variance, within-colony correlation and positivity measurement. Data must include independent colony/bee IDs, globally unique encounters, old-report timing, randomized assignment and probabilities, query attempts, cue delivery, sham condition, actual final action timestamp/state and realized net reward.

Sources:
- Athey & Wager, Policy Learning With Observational Data, Econometrica (2021): https://doi.org/10.3982/ECTA15732
- He et al. 2026 bumblebee information-purchase preprint: https://doi.org/10.64898/2026.09.15.751944
- Dunlap, Papaj & Dornhaus 2017 dynamic bumblebee sampling: https://doi.org/10.1098/rsfs.2016.0149

Implementation: adaptive_gain/randomized_policy_trial.py
Regression: tests/test_randomized_policy_trial.py
