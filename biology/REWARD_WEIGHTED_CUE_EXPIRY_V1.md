# Ecological consequence: payoff thresholds, not information entropy, determine cue lifetime

**Status**: supporting decision/ecology bridge; not V6 MAIN 4, not a
new general result in Bayesian value-of-information theory, and not
empirical evidence of evolved routing.

## Question

If a state is rare but extraordinarily costly to miss, must old context
information become useless on the same schedule as when both states
matter equally? No. Holding environmental state-transition rates and
stationary prevalence fixed, altering the **state-specific payoff ratio**
can move the optimal-action expiry time, or eliminate finite expiry
altogether.

This is a useful *ecological mechanism and experiment-design
prediction*, but Bayesian posterior decision boundaries and value
of information are prior art. In particular, De Lara & Gossner (2020),
"Payoffs-Beliefs Duality and the Value of Information",
https://doi.org/10.1137/18M1230049,
already characterize positive information value through payoff/action
geometry. Do not promote a corollary of that framework as a new general
theorem.

## State and payoff contract

Let X be a stationary two-state continuous-time Markov chain.
Transition rates are alpha: 0 -> 1 and beta: 1 -> 0;
k=alpha+beta, pi_1=alpha/k, pi_0=beta/k.
A perfect cue at time 0 reveals X(0). At lag t, the agent chooses action
0 or 1, earning **r_0>0** if it selects action 0 in state 0 and **r_1>0**
if it selects action 1 in state 1; otherwise the payoff is zero.
The comparator knows pi but never receives the cue.
The cue user optimizes its action conditional on the *old* cue (not
necessarily naively following the old state).
Both actors have the same action set and payoff matrix.

Let theta=r_0/(r_0+r_1). After observing a cue, the optimal action is
1 iff P[X(t)=1 | cue] >= theta. This is a payoff-sensitive decision
boundary, which need not be at 1/2.

The old-cue conditional state probabilities are
p_0=pi_1(1-z), p_1=pi_1+pi_0 z, z=exp(-kt).

## Exact rectified-exponential decision value

With V(t) the incremental maximal *expected reward* from knowing X(0),

\[
\boxed{V(t)=\max\{0,Ae^{-kt}-B\},}
\]

where

\[
A=(r_0+r_1)\pi_0\pi_1
\]

and

\[
B=(r_0+r_1)
\begin{cases}
\pi_0(\pi_1-\theta),&\pi_1>\theta,\\
0,&\pi_1=\theta,\\
\pi_1(\theta-\pi_1),&\pi_1<\theta.
\end{cases}
\]

Proof sketch: if pi_1>theta, the no-cue policy chooses action 1.
The only possible gain from the old cue comes from cue 0, where
choosing action 0 beats action 1 exactly when p_0<theta. Its gain
is pi_0[r_0-(r_0+r_1)p_0]. Substitute p_0=pi_1(1-z).
If pi_1<theta the analogous possible gain is from cue 1; its
expression is pi_1[(r_0+r_1)p_1-r_0]. When pi_1=theta both
branches still select opposite actions for any finite t.
All three cases simplify to the stated formula.

If B>0, the finite expiry time is

\[
\boxed{t_*={1\over k}\log(A/B).}
\]

If B=0 (the *reward-sensitive* decision threshold equals the
stationary state prevalence), V(t)=A exp(-kt)>0 for every finite
t, even when the stationary state prevalence is highly skewed.
Thus **unequal prevalence does not imply finite action-value expiry**:
unequal rewards can exactly compensate it.

For additive per-decision cue-use debit K>=0 in the same expected-payoff
units, positive net benefit holds only for

\[
\boxed{t<{1\over k}\log{A\over B+K}}
\]

when 0<=K<A-B. If K>=A-B, no age is profitable; if K=B=0,
every finite cue age gives positive benefit. A positive K therefore
produces a finite **economically actionable** horizon even when
statistical and intrinsic decision value remain positive at every
finite t. Do not identify K with PAYOFF's constitutive architecture
cost without an explicit fitness-currency conversion.

## Worked counterfactual at fixed ecology

Keep alpha=.8, beta=.2: state 1 prevalence 80%, state 0 prevalence
20%, environmental relaxation rate k=1.

| Reward state 0 | Reward state 1 | action threshold theta | no-cost decision expiry |
|---:|---:|---:|---:|
| 1 | 2 | 0.3333 | 0.538997 |
| 1 | 1 | 0.5000 | 0.980829 |
| 2 | 1 | 0.6667 | 1.791759 |
| 4 | 1 | 0.8000 | no finite expiry |

At r_0=4 and r_1=1, the rare state has fourfold reward. Then
V(t)=0.8 exp(-t), and the cue still changes the optimal action
at every finite lag. For K=.1 expected-reward units, its *net*
use horizon is ln(8)=2.07944.

Changing only the payoff matrix therefore moves the information-use
boundary even though the state frequencies, stochastic transitions
and mutual information are unchanged.

**Interpretation:** a rare but highly consequential state
(e.g. exposure to a predator) can preserve the behavioral utility
of an old signal. This is conditional on the measured payoff
structure; rarity alone does not do it.

## Existing work and priority ceiling

Classical Blackwell informativeness and decision-dependent information
value are established (Blackwell 1951/1953; De Lara & Gossner 2020).
This note is not offered as a new decision-theory theorem. Its
purpose is to force ecological analyses to specify and measure:
- the state transition kernel,
- relative consequences of correct/incorrect actions,
- acquisition/usage delay and payoff,
- the policy comparator (no cue, old cue, new cue, or pre-indexing).

Without these, "high heterogeneity increases adaptive sensing" is
not an identified inference.

## Data requirement and falsification

Test this mechanism by **independently varying the loss of missing
a rare state while holding its occurrence frequency and transition
statistics fixed**. Measure the old-cue conditional action choice
and realized payoff across randomized cue-to-decision lags.
Prediction: estimated t* changes as above; when
theta is close to pi_1 the finite cutoff becomes late, and at equality
the model predicts an exponentially decaying positive value at every
finite lag. A control with no cue must be optimized under the same
rewards. Compare the nonparametric age-response estimate with the
exponential model; a different lag kernel falsifies the Markov model,
not the existence of payoff-dependent Bayesian decisions.

Public Yi et al. (2025) mouse reversal dataset is useful for
behavioral adjustment to updated contingencies, but its existing
design does not independently vary old cue age, stationary ecological
switch rates, and the realized matched-action payoff.
The public data are at
https://doi.org/10.5061/dryad.pk0p2ngzs.
Its Dryad README establishes behavioral fields including odorCue,
outcomeIdentity, outcomeProbability, stateTime, waterReward;
this is a **schema** audit, not a record-level analysis, nor a direct
A-versus-P demonstration. A direct test remains on HOLD.

## Reproducibility and governance

Implementation: ../adaptive_gain/reward_weighted_decision_value.py
and ../tests/test_reward_weighted_decision_value.py.
The tests brute-force all four old-cue-to-action maps across 486
multi-parameter conditions, plus an independent 1,152-case
cross-check of the rectified-exponential formula, finite/infinite
expiry, reward exchange, and additive cost horizon.

Keep this outside the V6 MAIN 1--3 novelty spine until a
genuine empirical identifying experiment is available.
