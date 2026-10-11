# The stronger no-information comparator: optimize when to act

**Status:** third comparator audit for adaptive-gain PR #67. It strengthens
WAIT_VERSUS_INFORMATION_CAUSAL_GATE_V1.md. This is a mathematical
counterfactual, not a field validation or a new V6 MAIN theorem.

## Why one fixed sham wait is still not the strongest comparator

The original conditional acquisition model compared SKIP (act after a)
with QUERY (observe after r, then act after a). The CI failure proved
that an uninformative QUERY could appear beneficial because **waiting
itself** changed the payoff-relevant environment.

The first repair offered SKIP and a matched WAIT of exactly r with no
signal. However a real animal may be able to choose how long to wait,
rather than choosing only 0 or r. To avoid giving the query an artificial
timing advantage, permit a no-query decision policy to choose *any
passive delay* d in a preregistered interval [0,T], conditional on its old
cue O. This comparison is intentionally harder to beat.

## Exact analytic waiting optimizer (binary CTMC)

Let alpha denote 0->1 and beta denote 1->0, k=alpha+beta,
pi1=alpha/k, pi0=beta/k. At time -tau an old cue yields
posterior p_o about the environment. With terminal action duration a,
opportunity survival exp(-mu*(a+d)) and state-dependent rewards r0,r1
for correct final action, waiting d without taking another observation
achieves

\[
W_o(d)=e^{-\mu(a+d)}
\max\{r_0[1-p_o(\tau+a+d)],\,r_1p_o(\tau+a+d)\},
\]

where p_o(t)=pi1+(p_o-pi1)exp(-kt).

For either fixed final action j in {0,1}, its unnormalized reward
trajectory in d is

\[
f_j(d)=e^{-\mu(a+d)}[A_j+B_je^{-kd}],
\]

with
\[
(A_0,B_0)=
(r_0\pi_0,\ r_0(\pi_1-p_o)e^{-k(\tau+a)}),
\]

\[
(A_1,B_1)=
(r_1\pi_1,\ r_1(p_o-\pi_1)e^{-k(\tau+a)}).
\]

For mu>0 each f_j has at most one interior positive stationary
point, when B_j<0 and

\[
e^{-kd_j^*}=-\frac{\mu A_j}{(\mu+k)B_j}\in(0,1).
\]

Evaluate d=0, d=T, and every eligible stationary point inside [0,T],
selecting the maximum of W_o(d). This gives the exact optimum of
the declared finite continuous-time waiting problem up to floating
arithmetic, rather than scanning a time grid.

If mu=0, each branch is monotone or flat, so endpoints suffice.
If mu>0 and the maximum finite stationary point is interior and
T covers it, the solution also solves the unbounded waiting problem,
because both action rewards converge to zero as d->infinity.

## Which quantity isolates optional information?

Let M_o=max_{0<=d<=T} W_o(d), and Q_o(epsilon) be the
Bayes-optimized paid query at its declared time r.
The sensor-enabled controller compares Q_o with M_o, whereas the
no-sensor controller already enjoys full old-cue-dependent
timing flexibility.

\[
J_{\rm noquery}=\sum_o w_o M_o,\qquad
J_{\rm univquery}=\sum_o w_o Q_o,
\]

\[
J_{\rm conditional}=\sum_o w_o\max(M_o,Q_o).
\]

The **strict premium for a conditionally deployed measurement**
over the better of (i) the strongest passive-timing-only
policy and (ii) universal querying is

\[
G_{\rm flexible}=
J_{\rm conditional}
-\max(J_{\rm noquery},J_{\rm univquery}).
\]

At epsilon=0.5, a cue is uninformative, and Q_o<=W_o(r)<=M_o
for K>=0. Therefore the strict premium is zero, even if the
mere passage of time would be rewarded.

Along a Blackwell-ordered series of refresh signals,
Q_o(epsilon) is nonincreasing and M_o is independent of
epsilon. The existing min(P,N) unimodality argument remains
valid for the premium relative to this stronger comparator.

## Numerical stress test

For the canonical example (alpha=.8,beta=.2,tau=1.2,
r=.15,a=.1,mu=.25,r0=r1=1,K=.03, perfect old cue),
allow no-query waiting for any d in [0,.5].

- After old report 0, optimal passive wait is d=0.3094379124,
  longer than the sensor's acquisition time r=.15.
- After old report 1, optimal passive delay is d=0.
- Expected no-query performance is 0.782273056, compared with
  0.781775564 when only d=0 or d=.15 is allowed.

| Quantity | Original SKIP/QUERY comparator | Matched WAIT comparator | Optimized wait d in [0,.5] |
|---|---:|---:|---:|
| Lower sensor-error boundary | 0.05652258 | 0.05652258 | 0.05652258 |
| Upper sensor-error boundary | 0.35127167 | 0.34238957 | 0.33949701 |
| Sensor error maximizing conditional premium | 0.11398574 | 0.11225411 | 0.11169019 |
| Maximum conditional premium | 0.04081084 | 0.03958103 | 0.03918053 |
| Pairwise log maintenance ceiling, w0=1 | 0.02266543 | 0.02197123 | 0.02174531 |

The third column is a **strictly stronger no-information
comparator** in this model. The qualified conclusion persists:
the extra benefit of conditionally acquiring a signal can
peak at intermediate quality even when a no-sensor policy may
choose its action time optimally based on the old report.

Do **not** interpret the fall in these premiums as evidence
that natural organisms have that precise cost/accuracy
trade-off or can actually implement the no-query optimum.

The "no-query optimized timing" architecture already has
access to the old cue and conditional waiting control. The
pairwise maintenance-cost ceiling therefore compares the
marginal addition of *optional fresh-signal acquisition* to
a capable baseline controller, not the complete costs of
decision machinery versus reflexive behavior.

## Closest ecological precedent: the main sampling question is already tested

Dunlap, Papaj & Dornhaus (2017), *Interface Focus* 7:20160149,
[DOI: 10.1098/rsfs.2016.0149](https://doi.org/10.1098/rsfs.2016.0149),
tested how bumblebee sampling of a fluctuating nectar resource
depends on environmental persistence and relative losses of sampling
versus failing to notice improved reward. Their factorial experiment
used four persistence levels (0.99, 0.86, 0.73, 0.60) and three reward
error-cost ratios, with sampling operationalized as a return to the
fluctuating resource after its last known state was poor. Bees
changed their sampling frequency with environmental persistence
and reward but often tracked the best current resource suboptimally.

**This directly preempts broad claims that environmental
persistence, information age and reward asymmetry governing
sampling are unexplored.** The study already tested such
ecological factors against established foraging theory.

The authors supplied a public **analyzed-data spreadsheet**
([Figshare DOI 10.6084/m9.figshare.4769539](https://doi.org/10.6084/m9.figshare.4769539),
22.9 kB). The publicly described source is “Bee choice data,”
but the current audit has not established trialwise simultaneous
timestamps of cue acquisition, calibrated observation noise and
matched waiting-without-information controls. A public spreadsheet
exists, but its rows were **not reanalyzed here**.

In that experiment, sampling is itself a visit to a reward-bearing
resource; it may jointly alter expected sucrose gain and knowledge.
This is **not a criticism of the original authors' question or
analysis**; it is a different estimand. Our stricter three-way
comparison asks a narrower causal question: Does the animal benefit
from paying for *fresh information*, beyond the best payoff obtained
by timing a no-new-information action?

The useful prospective differentiator is a randomized three-arm
SKIP / duration-matched SHAM WAIT / informative QUERY contrast,
with optional querying contingent on the prior cue and a measured
error/latency trade-off. Dunlap et al.'s study is a strong baseline
for experiment design and expectation-setting, not a direct
confirmation of this information-specific comparator.

## Independent tests and empirical constraints

Implementation:
- adaptive_gain/optimal_passive_wait.py
- tests/test_optimal_passive_wait.py

The passive optimizer is checked against a directly evaluated
dense waiting-time grid under 960 parameter sets. Its
source-independent numerical candidate check evaluates both
fixed terminal actions, their interior stationary points and
timing interval boundaries. Additional tests compare
peak/error boundaries, a separate 64-environment sensor grid
and uninformative-cue negative controls.

A proper ecological experiment should randomize the
information intervention *at the same time as* a sham
observation and explicitly allow or manipulate when the
terminal action may occur without observing. Otherwise
one can only estimate the value of a bundled action
(schedule + sensing), not the marginal value of sensing.
Contrasts require the same reward table and an independently
estimated environmental transition process.

The literature already recognizes the importance of
information versus delay controls, for example the
gray-jay inspection-versus-interruption manipulation
(https://pubmed.ncbi.nlm.nih.gov/12461598/).
The present exercise supplies a precise decision-process
comparator to prevent unjustified biological interpretations;
it is not a new general principle about patience or sensing.

V6 MAIN 1–3 stay unchanged.
