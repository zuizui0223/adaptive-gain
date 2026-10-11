# Empirical decision gate: frozen policies, ecological frequency and independent validation

Status: supporting ecological-analysis companion to Evolution Letters V6 MAIN 1–3.
No new general decision-theory theorem, no observed adaptive fitness, and no
power/sample-size recommendation for real bumblebee experiments.

## 1. Exactly which value has to survive the experiment?

From independently randomized within-old-report PASSIVE, SHAM, QUERY
assignments, learn a two-branch rule pi(O) using independent training
colonies. Do not use final validation colonies to select pi or alter
the reward definition.

On held-out colonies, calculate J_C for that frozen rule and both
best fixed alternatives J_P and J_Q, with externally declared
deployment old-report weights omega_o. The strict relevant statistic is

G_out = J_C - max(J_P,J_Q) = min(J_C-J_P,J_C-J_Q).

A positive query-vs-sham effect alone does not establish G_out>0.
The old report must select different acquisition decisions AND the
selected program must improve performance against both fixed ones.

The code adaptive_gain/randomized_policy_trial.py requires recorded
assignment probabilities, source-independent cluster splitting, all
six old-report-by-arm cells, and positivity checks. The approximate
held-out bootstrap decision requires positive one-sided 97.5%
lower limits for BOTH fixed comparisons. It cannot substitute for
actual instrumented randomization, and bees are not independent
biological clusters if they share colony effects.

## 2. Why in-sample maximization is misleading: repeated null controls

An independent synthetic Monte Carlo stress test was run with the
following explicit *hypothetical* design:
- 30 independent TRAINING and 30 HELDOUT clusters;
- two old reports x three arms x 12 Bernoulli encounters per cluster;
- common Gaussian colony random logit intercept, sigma=0.55;
- a target old-report distribution (0.2,0.8);
- a frozen policy learned from training-arm mean rewards;
- cluster-bootstrap 400 times within HELDOUT data, per replication;
- 250 separate experimental replications under a null and a mixed
  policy alternative.

For the null, PASSIVE and QUERY both have probabilities (0.70,0.80)
across the two reports, so *no conditional policy is genuinely
preferable*. An independently implemented NumPy diagnostic gave:
- 51.6% positive in-sample extra policy gain (ordinary selection optimism);
- 13.6% positive held-out *point* gain;
- 0/250 replications with both bootstrap lower limits >0.

For the alternative, PASSIVE probabilities (0.70,0.80) and QUERY
probabilities (0.90,0.75) give nominal no-colony conditional benefit
0.04, while always P and always Q have equal 0.78.
- 94.0% positive in-sample extra gain;
- 90.0% positive held-out point gain;
- only 95/250 (38%) with BOTH bootstrap limits positive.

These numbers are **simulation diagnostics, not calibrated real-experiment
error rates**. With Gaussian colony random intercept sigma=0.55,
marginalizing the Bernoulli probabilities shifts the alternative true
population gain slightly to approximately 0.03953. The null retains
true gain zero. Different random seeds, implementation languages,
cluster dependence, sampling allocation and confidence procedures
change numerical acceptance rates.

The new standard-library executable
scripts/simulate_randomized_query_policy_validation.py
is intended to reproduce the same experimental *mechanism* using a
separate Python RNG implementation. Do not assume its exact draws
match the independent NumPy scratch run. The latter's raw toy result
is a provenance-qualified exploratory check, not a frozen empirical
source-data receipt.

Main interpretation: an in-sample positive maximization is cheap;
a credible dual-comparator held-out demonstration can be extremely
difficult even when the biological opportunity is real. A negative
small-pilot test is not enough to falsify the opportunity mechanism.

## 3. New ecological transport result: control value has a frequency window

Suppose independent randomized assays establish branchwise expected
reward differences in a FIXED conditional kernel:

a=E[R|old0, QUERY]-E[R|old0, PASSIVE]>0,
b=E[R|old1, PASSIVE]-E[R|old1, QUERY]>0.

Let w be the frequency of the old **REPORT 0** in the deployment
environment. The frozen conditional rule chooses QUERY after old0
and PASSIVE after old1. By exact averaging,

J_C-J_P=w*a,
J_C-J_Q=(1-w)*b,

therefore

G(w)=min(w*a,(1-w)*b).

This elementary two-branch policy-value identity implies

w_star=b/(a+b),
G_max=a*b/(a+b).

If the additional controller maintenance cost has been independently
translated into a *per-encounter additive expected-reward* equivalent
K, strict advantage is possible only when K<G_max and

K/a < w < 1-K/b.

For the constructed example a=.20, b=.05,
w_star=.20 and G_max=.04.
With K=.01, the toy controller has positive net benefit only
for 0.05 < w < 0.80. At old0 frequency 0.01, G=.002
and it cannot repay that cost, even though the branch-specific
QUERY advantage after old0 remains .20.

**Critical ecological identification caveat:** reweighting old
REPORT frequency while keeping a and b fixed is a
*covariate-shift/transport* calculation, not a natural-history
law that can be applied when stationary environmental occupancy
changes. Changing nature's state occupancy often also changes
state transitions, cue posteriors, and a,b. Moreover, old
report prevalence differs from true state prevalence under cue
misclassification. To estimate this viability window empirically,
measure all three separately: report prevalence, conditional
arm effects, and architecture maintenance burden in a common
fitness-relevant currency.

This is a test of *deployment opportunity*, not the evolution
of an architecture. Even a positive G remains conditional
on a real biological controller and an appropriate comparator.

Source/tests:
- adaptive_gain/conditional_policy_transport.py
- tests/test_conditional_policy_transport.py
- scripts/simulate_randomized_query_policy_validation.py
- tests/test_simulate_randomized_query_policy_validation.py
- adaptive_gain/randomized_policy_trial.py
- tests/test_randomized_policy_trial.py

## 4. Experimental next step and go/no-go

Before a confirmatory bee assay, run a separately documented pilot
to measure:
1. transition rate and duration of target environmental states;
2. old report distribution **and** true state occupancy;
3. matched QUERY/SHAM/passive motor timing and reward costs;
4. after each old report, experimental arm effects in a common
   net reward scale and their colony-level uncertainty;
5. whether the old cue genuinely alters the NEXT information
   acquisition decision (not just the terminal motor action);
6. effective independent colony count and feasible reward/time
   burden for a held-out colony-level evaluation.

Stop if target state transitions or sensor reliability cannot be
calibrated independently, if any old-report/arm cell lacks overlap,
or if signal access is inseparable from collecting resources.

Pass only if a predeclared conditional acquisition policy improves
held-out reward over both fixed alternatives, matched SHAM supports
an information-specific effect, and animal voluntary free-choice
trials show the policy is behaviorally accessible.

To claim selection/evolution further requires competing heritable
control strategies, maintenance costs, and reproductive outcomes.
No fourth V6 MAIN result is proposed from these dynamic experiments.

Related established work:
- He et al. 2026 (bumblebee information purchasing preprint),
  https://doi.org/10.64898/2026.09.15.751944
- Dunlap, Papaj & Dornhaus 2017 (dynamic reward-resource sampling),
  https://doi.org/10.1098/rsfs.2016.0149
- Athey & Wager 2021 (policy learning and honest inference),
  https://doi.org/10.3982/ECTA15732
