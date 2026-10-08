# Post-query timing: ecological hypothesis and identification contract

**Status:** side mechanism in adaptive-gain PR #67. The static, deterministic
V6 MAIN 1--3 are unchanged. This is NOT a new evolutionary theorem or
real-world validation.

## Strongest matched decision process

All policies receive the same old observation O (possibly noisy) of a
binary ecological state X(-tau). The environmental state changes as a
stationary binary continuous-time Markov chain while the animal decides,
waits, acquires a cue and acts. The two action-specific correct-response
payoffs r0 and r1 and independent opportunity-closure hazard mu are
declared before examining outcomes.

The no-new-information controller P can use O to choose *any* delay
t in [0,T] and then choose its terminal action optimally.

The new-information controller Q spends r <= T acquiring a calibrated,
possibly noisy current-state cue Y at acquisition time r, pays additive
per-attempt cost K, then chooses a further delay d(O,Y) in [0,T-r].
It chooses its terminal action optimally from the updated posterior
after the delay. Thus the two controllers share a common maximal
elapsed decision window T. The query controller is not artificially
forced to act immediately after receiving new information.

Let M_o be the optimal P branch payoff and let
q_{o,y}=Pr(Y=y|O=o). At time r, let p_{o,y}=Pr(X(r)=1|O=o,Y=y).
With H(p;L) the maximum reward obtainable using posterior p
without another observation, after an optional passive delay in
[0,L] and a fixed terminal delay a, define

Q_o = exp(-mu*r) sum_y q_{o,y} H(p_{o,y};T-r) - K.

The H optimizer is obtained exactly by checking the endpoints
and the eligible stationary points of each reward-action branch
against the two-state Markov transition kernel.

Define

J_noquery = sum_o w_o M_o,
J_universal_query = sum_o w_o Q_o,
J_contingent = sum_o w_o max(M_o,Q_o).

The premium specifically attributable to conditioning the **purchase
of fresh information** on O is

G = J_contingent - max(J_noquery,J_universal_query).

Its positive values do not automatically identify biological
fitness or heritable sensory architecture cost. Nor should the
fixed comparator be interpreted as a state-preindexed repertoire
that the focal biology does not possess.

## Strong negative controls

1. At refreshed cue error 0.5, Y carries no new state information.
   Because the passive controller can wait r and beyond without
   buying the cue, query cannot improve upon P for K>=0:
   G=0 and the query-access premium is zero.
2. Higher symmetric binary observation error is a Blackwell
   garbling; at fixed times, payoff structure and costs, absolute
   optimal query and conditional performance cannot increase.
   The relative premium over the best fixed schedule may still
   be unimodal because the fixed comparator changes.
3. A physically frozen environment at positive opportunity
   hazard gives no benefit from passive waiting alone. A
   signal's value is then distinguished from the "good things
   happen while waiting" explanation.
4. The environmental process is assumed independent of the
   act of querying. If reaching a flower, probing a host, or
   receiving a reward physically alters the target, the
   observation changes the environment and must be modeled
   as an intervention rather than a passive measurement.

## Two illustrative process witnesses

**Witness A: existing conditional value survives.**

Use alpha=.8, beta=.2, tau=1.2, sampling duration r=.15,
terminal delay a=.1, maximum total passive waiting T=.5,
opportunity hazard mu=.25, r0=r1=1, K=.03, no old
report error, refreshed report error .11.

With a passive-timing controller as comparator, conditionally
purchasing the new cue still provides positive incremental
expected reward. In this setting, the chosen post-query
delays happen to be zero near the optimal-quality window,
so allowing post-query waiting does not create the original
effect through an unfair timing constraint.

**Witness B: information affects when to act before it changes
the best immediate action.**

Set alpha=beta=.2, tau=.1, r=.03, a=.02, T=.5,
mu=.01, r0:r1=1:4, K=.005 and refreshed cue
error .10, with perfect old observation.

After old report O=0, the optimal strategy is to query.
For the two possible updated cue labels Y=0 and Y=1,
the best terminal action **if acting immediately after the
fixed terminal delay a** is the same action 0. Nevertheless:

- refreshed label Y=0: optimal extra delay d=0;
- refreshed label Y=1: optimal extra delay d=.47.

At the latter delayed action time, a different terminal
action can become optimal as the ecology changes. This
example therefore demonstrates information-dependent timing
and eventual choice, NOT unchanged terminal action at all
times. It is one model instance of a known dynamic decision
principle, not a discovery of a universal law.

## Closest prior art

Dunlap, Papaj & Dornhaus (2017), *Interface Focus*,
https://doi.org/10.1098/rsfs.2016.0149, studied bumblebee
revisits to a fluctuating reward source under manipulations
of environmental persistence and error costs. Their
supplementary analyzed data are public:
https://doi.org/10.6084/m9.figshare.4769539.

This preempts general novelty claims about bumblebees
adjusting resource sampling to environmental volatility or
payoffs. In their ecological task, sampling a reward source
can itself change exploitation and handling outcomes. That
does not provide the time-matched, non-rewarding cue
intervention needed to identify marginal new information
in the present protocol. The current study is therefore a
prospective proposal, not a reanalysis of Dunlap's data.

## Prospective falsification: three experimentally separated actions

A viable controlled foraging experiment could program two
resource states with known transitions and independently
show old and new state cues. Within individuals, randomize:

- **PASSIVE**: no new cue, optional wait chosen within a
  predeclared horizon T, then one terminal choice;
- **SHAM**: an identically timed/situated cue port produces
  a meaningless, independent label and no extra reward;
- **QUERY**: the same port produces a label of the true
  state at the cue time, flipped with known probability
  epsilon, then permits optional waiting until T.

Using non-rewarding visual information at the observation
port helps separate observation from sampling a new reward
source. The SHAM arm must match travel effort and delay;
reward acquisition occurs only at the final resource.

Record subject/colony, old cue true state and its report,
sample decision and latency, actual information from Y,
post-query waiting, final state at action, terminal choice
and reward. Randomize the query availability and signal
quality across blocks, while estimating natural error
separately from imposed label flips. Environmental state
transitions must be logged independently of animal
behavior.

Primary causal targets:

1. Branch-conditional effect of informative QUERY over
   SHAM at equal decision time and equal handling cost.
2. Additional conditional-QUERY policy value over both
   (a) a no-query policy optimizing waiting conditional on
   O and (b) universal-query policy.
3. Behavioral report-by-quality interactions in the
   *decision to acquire the next cue* and in post-cue
   waiting, with final reward as a separate endpoint.

Estimate outcome means and policy value with trialwise
randomization/known propensities. Use cross-fitting and
held-out individuals/colonies to avoid selecting the
best policy and estimating its gain from the same
noise. The model's predicted signs and relative
policy-ordering should be frozen before testing the
held-out sample. Cluster uncertainty by individuals
and colonies; do not treat visits as independent replicates.

A no-query controller must be allowed a range of waiting
times, not only an immediate action. A passive control
that cannot choose the timing available to the query
controller will overestimate fresh information benefit.

## STOP / go

The executable model can establish only *possibility* and
source-of-gain under declared idealizations. Direct
ecological validation requires the intervention above.
Do not append another headline theorem to V6 solely
on the basis of these examples. Stronger ecological
novelty is conditional on a held-out experimental
reversal not already entailed by signal-decision
optimization and a demonstrated connection to
natural history or heritable selection.

Code:
- adaptive_gain/post_query_timing.py
- tests/test_post_query_timing.py
- adaptive_gain/optimal_passive_wait.py
