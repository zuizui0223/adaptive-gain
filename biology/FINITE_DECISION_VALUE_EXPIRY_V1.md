# Finite decision-value expiry despite surviving information

**Status:** analytic ecological stress test / empirical falsification target.
Not V6 MAIN 4, not a new general value-of-information theorem, and not
deduced from the original stationary-world finite query problem.

## Mechanistic question

Does an old cue remain worth using merely because it still predicts the
environment better than chance? **No**, when the optimal no-cue action is
asymmetric. This requires comparing information *content* against
information's marginal *decision value* under the same action/payoff rule.

## Declared model

Let environmental state X(t) in {0,1} follow a homogeneous CTMC with rates
alpha: 0 -> 1 and beta: 1 -> 0. Assume alpha,beta>0 and that the environment
is in its stationary distribution at cue acquisition. Then

pi_1 = alpha/(alpha+beta), pi_0 = beta/(alpha+beta).

At time zero, a perfect cue reveals X(0). It cannot be refreshed. After lag
t, the organism must select action a in {0,1}; payoff equals 1 when a=X(t)
and 0 otherwise, irrespective of state. The alternative policy had **no
cue** but knows the stationary state prevalence and optimizes its action.

Define k=alpha+beta, z=exp(-kt). Conditional probabilities are

P[X(t)=1 | X(0)=0] = pi_1(1-z),
P[X(t)=1 | X(0)=1] = pi_1+pi_0 z.

The best cue-based action maximizes conditional success probability *for
each cue*. The best no-cue action always chooses the more common state.

\[
V_{\rm action}(t)
=\sum_{x=0}^1\pi_x\max_{a\in\{0,1\}}P[X(t)=a\mid X(0)=x]
-\max(\pi_0,\pi_1).
\]

This is incremental *expected decision accuracy*, not information in bits,
not reproductive fitness, and not the constitutive value of sensors.

## Exact finite expiry and its scope

For pi_1>pi_0, the cue-0 action switches from 0 to 1 at

\[
t_*=\frac{1}{k}\ln\frac{2\pi_1}{\pi_1-\pi_0}.
\]

The cue-1 action always selects 1. After t_*, both cue observations result in
the same action, and

\[
\boxed{V_{\rm action}(t)=0\quad(t\ge t_*).}
\]

The analogous expression holds with states interchanged if pi_0>pi_1.
If pi_0=pi_1=1/2, no finite expiry occurs: V_action(t)=e^{-kt}/2>0
for all finite t. The sharp switch therefore hinges on an asymmetric
stationary prevalence and the declared symmetric payoff.

Even for finite t>t_* the conditional distributions differ and the mutual
information I[X(0);X(t)] remains positive. Hence

\[
\boxed{\text{positive predictive information}\not\Rightarrow
\text{positive incremental optimal-action value}.}
\]

This is an instance of a standard Bayesian decision-theory principle:
statistics can be informative without changing the optimal decision.
The candidate ecological consequence is the *quantified timing boundary*
under independently measured state transition rates and action payoffs.
Do not assert priority for the general principle.

## Exact illustrative receipt

Set alpha=0.8, beta=0.2 per chosen time unit, so pi_1=0.8 and k=1.
Then t_* = ln(8/3) = 0.980829253.

| lag | V_action (extra expected correct-choice probability) | I nats | chosen actions after old cue 0,1 |
|---:|---:|---:|---|
| 0 | 0.200000 | 0.500402 | (0,1) |
| 0.5 | 0.074090 | 0.155375 | (0,1) |
| 0.8 | 0.023785 | 0.085754 | (0,1) |
| 1.2 | 0.000000 | 0.039547 | (1,1) |
| 2.0 | 0.000000 | 0.008456 | (1,1) |

These numbers are model outputs, not ecological measurements. At the exact
threshold the two actions tie for old cue 0; any tie-breaking is Bayes-optimal.

## Independent verification

The library computes the CTMC transitions, policy and mutual information.
Tests compare the result with an independent enumeration of all four
deterministic old-cue -> action policies for 4x4x6=96 parameter/lag cases.
Local execution: four pytest tests passed. This checks finite-model
arithmetic, not real-world validity.

Executable files:
- ../adaptive_gain/decision_value_expiry.py
- ../tests/test_decision_value_expiry.py

## Why prior context-staleness models require a revision

Earlier CONTEXT_TURNOVER_DURING_SENSING_V1 compares *following* the remembered
state with following a refreshed state. That can be a meaningful constrained
architecture comparison, but it does **not** generally compare two
Bayes-optimized policies under a common asymmetric state prior.

If an old-cue policy is allowed to optimize its action instead of blindly
following the cue, its performance cannot be below the optimal no-cue
baseline. The ecological predictor must therefore name the actual
comparator (literal memory-following rule, optimally preindexed repertoire,
or fresh-query policy). Any claimed selection advantage without declaring
this comparator is blocked.

## What public data can presently identify

Candidate | source and recorded items | can estimate a decision-value expiry?
---|---|---
Kato-Namba et al. (2025), Scientific Reports, https://doi.org/10.1038/s41598-025-13427-z | CO2-dependent multisensory visual/olfactory motor responses in VR; source code/data linked via https://doi.org/10.60178/cbs.20250721-001 | **No direct expiry identification** without independently varied cue age, payoff-relevant state at action, and action-payoff record. Excellent cue-integration anchor.
Chandel et al. (2024), Nature, https://doi.org/10.1038/s41586-024-07848-5 | Time-resolved IR/CO2/odor host-seeking; Dryad https://doi.org/10.5061/dryad.547d7wmh3 | **No** state-switch plus rewarded decision contrast; behavioral timing only. Large video archive.
Yi et al. (2025), Dryad, https://doi.org/10.5061/dryad.pk0p2ngzs | Trial-wise odorCue, outcomeIdentity, outcomeProbability, stateTime, waterReward, behavioral timing, reversal metadata | **Partial**: can measure adaptation to changed cue-reward contingencies, not within-trial state-value decay or inherited architecture advantage. Schema verified in public Dryad README; download-level row audit is pending.
Ajuwon et al., GoFish, https://doi.org/10.3758/s13428-022-02049-2 | Goldfish acquisition/reversal/choice and response times, published per-trial outcome subset | **Partial**: reversal-learning benchmark, not within-trial cue staleness.

Data availability alone does not imply all required variables appear in the
same subjects and trials. A direct lifetime claim is on HOLD until a dataset
has, for each replicated encounter: (i) timestamped old cue and current state,
(ii) experimentally varied lag, (iii) action and actual outcome, (iv)
independently measured state prevalence/transition rates, (v) matched no-cue
(or statistically valid alternative) baseline. A full A versus P evolutionary
claim additionally requires real comparator interventions and architecture
costs.

## Falsification plan

1. Estimate state transition rates and stationary frequencies from
   independently recorded environmental state sequences.
2. Randomize time between the observed state cue and the payoff-relevant
   decision across a range spanning the preregistered t_* estimate.
3. Counterbalance state-specific rewards; record action and achieved payoff.
4. Contrast old-cue optimum, blind majority baseline, and, when feasible,
   postcommitment re-query intervention.
5. Fit the empirical lag-response *nonparametrically* with uncertainty,
   before confronting the fixed-parameter CTMC prediction.
6. If decisions still depend on the cue beyond t_*, test whether learning,
   conditional risk, asymmetric rewards, or a non-Markov environmental
   process explains the deviation rather than reclassifying it as
   "routeability."

A true selection claim needs the same architecture-contrast gate defined in
COMPARATOR_SEMANTICS_FITNESS_GATE.md. All quantities in this note are
immediate expected performance; not population-genetic selection coefficients.

## Manuscript governance

Leave V6 MAIN 1--3 untouched. Use as a supporting bridge only if real data
close the required causal/identifiability gates. No claimed empirical
validation, universal extinction, or new general decision-theory theorem.
