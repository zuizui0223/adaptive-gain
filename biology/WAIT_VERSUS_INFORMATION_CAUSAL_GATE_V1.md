# Causal timing control: an uninformative cue can look beneficial because time passes

**Status:** independent counterexample, correction of a failed CI assertion,
and a stricter information-specific comparator on adaptive-gain PR #67.
This is not a new V6 main theorem or observed evolutionary selection.

## 1. What failed, and why that matters

At commit a3d85be7, Python 3.10 and 3.11 CI failed only
test_uninformative_refresh_cue_never_creates_strict_routing_value:
the old selective_refresh() two-schedule comparison returned a
**positive conditional premium of 0.03419976772047084**
even when the refreshed cue was wholly uninformative
(symmetric error rate 0.5).

The implementation was performing its declared mathematical operations.
The false expectation was scientific: refreshing was also **waiting**.
Since the payoff-relevant environment continues to move while a query
takes time, a state-conditioned *delay* can change expected performance.
Thus the positive conditional premium was not proof of a useful new cue.

The original result is still a valid contrast between (i) immediate
action and (ii) an action delayed by a bundled query. It is **not**
a decomposition of that advantage into new information versus timing.

## 2. Three matched comparator actions

In a stationary binary CTMC, after an old (possibly imperfect) cue o,
let p_o be the posterior probability that the environment was in state 1
at the old cue time. Define state-1 prediction after elapsed time t as

p_o(t) = pi_1 + (p_o-pi_1) exp[-(alpha+beta)t],

and the optimal terminal expected payoff as
h(p) = max{r_0(1-p), r_1 p}.

At commitment time 0 the organism has three *operationally*
different possibilities:

- S_o: **SKIP** the new observation and act after a.
- W_o: **WAIT without measuring**, for the same acquisition duration r,
  then act after a; there is no per-query debit.
- Q_o(epsilon): **QUERY**, spend r acquiring a new cue of symmetric
  error epsilon, pay per-query debit K, then act after a after updating
  on both old and new observations.

With an independent ecological opportunity hazard mu,

S_o = exp(-mu*a) h[p_o(tau+a)],

W_o = exp(-mu*(r+a)) h[p_o(tau+r+a)],

Q_o(epsilon) = exp(-mu*(r+a))
  sum_y max{
    r_0 Pr(Y=y, X(r+a)=0 | old=o),
    r_1 Pr(Y=y, X(r+a)=1 | old=o)
  } - K.

The **gross information value of the refreshed measurement**,
holding terminal action time fixed, is

I_o(epsilon) = Q_o(epsilon)+K-W_o >= 0.

At epsilon=0.5, Y is independent of the current state, hence
I_o(0.5)=0 exactly; Q_o(0.5)=W_o-K.
With K>=0, QUERY is weakly dominated by matched WAIT when the new
cue is completely uninformative. This assertion is valid even
when WAIT itself is advantageous relative to immediate SKIP.

## 3. A numerical counterexample to the previous inference

Take alpha=0.8, beta=0.2, tau=0.1, r=a=0.15,
mu=0.25, reward ratios r_0:r_1=1:4,
K=0.015, perfect old cue, and **fully random refreshed cue**.

| Old report | SKIP | WAIT (no signal) | QUERY (no signal, cost K) |
|---|---:|---:|---:|
| 0, rare state | 0.792748137 | 0.978746976 | 0.963746976 |
| 1, common state | 3.682331390 | 3.466287201 | 3.451287201 |

The old two-schedule conditional premium between SKIP and QUERY
was +0.034199768. However:
- the net value of purchasing the fresh signal over matched WAIT is
  -0.015 in each branch;
- the gross information value is exactly zero;
- all true best conditional actions with a WAIT option are
  (WAIT after old 0, SKIP after old 1), *with no querying*.

This demonstrates that conditional delayed response can be adaptive
in the constructed ecology, without information acquisition at all.
The environmental state can drift toward a high-reward state during
waiting. The result is a comparison artifact if interpreted as sensing.

## 4. Stricter acquisition-control target

A no-new-cue controller can optimize timing conditional on old report:
M_o=max(S_o,W_o).
The sensor-enabled controller can instead pick Q_o(epsilon)
after seeing old report o.

Let w_o = Pr(old report=o), d_o=Q_o-M_o. We now isolate:

J_noquery = sum_o w_o M_o,
J_query_universal = sum_o w_o Q_o,
J_query_conditional = sum_o w_o max(M_o,Q_o).

The **strict information-acquisition-control premium** is

G_query(epsilon) = J_query_conditional
                  -max(J_noquery, J_query_universal)

= min {sum_o w_o (d_o)_+,
       sum_o w_o (-d_o)_+}.

This isolates conditional purchasing of a new measurement against
(1) an old-cue-conditional wait-or-skip controller that obtains no
new information and (2) universal querying, both with optimized
terminal actions. In particular G_query(0.5)=0 for K>=0.

The *query-access* benefit J_query_conditional-J_noquery is
nonnegative and weakly decreases with binary cue garbling.
It can be strictly positive when G_query=0 (all branches should query).
Do not conflate absolute information access, relative conditional
acquisition and the purely timing-based premium.

When the refreshed signal is Blackwell-degraded while all times,
costs and state dynamics remain unchanged, Q_o is nonincreasing,
M_o is constant, so the same weak-unimodality proof applies to
G_query using d_o=Q_o-M_o. Its peak (if interior) is where
J_query_universal=J_noquery.

## 5. Corrected accuracy window and PAYOFF lift

For the same illustrative alpha=0.8,beta=0.2, tau=1.2,
r=0.15,a=0.1,mu=0.25,K=0.03,r_0=r_1=1:

| Object | Without matched-WAIT control | After matched-WAIT control |
|---|---:|---:|
| Strict query conditional window, epsilon | (0.05652258, 0.35127167) | (0.05652258, 0.34238957) |
| Maximum conditional premium | 0.04081084 | 0.03958103 |
| Precision error at maximum | 0.11398574 | 0.11225411 |
| Max log constitutive controller cost at w0=1 | 0.02266543 | 0.02197123 |

The corrected peak refers to a **stricter comparator** than the older
two-schedule result. Neither table entry estimates true fecundity
or inherited architecture costs. Both are one-encounter model outputs.

## 6. Experimental causal controls

Use a three-arm design matched to the timeline of a trial:

1. **SKIP** — immediate terminal action, no new cue.
2. **SHAM WAIT** — identical waiting time and handling as the query,
   but no state-informative signal. Separately assess a sham cost
   matching the true query if handling/sensing costs are measurable.
3. **QUERY** — equally long observation period and a
   calibrated-informativeness new cue.

Randomize the old observation, the new cue's conditional accuracy,
and the delay. Measure environmental state at old cue,
new cue and final action, as well as achieved reward/loss and
whether individuals actively acquire the optional new cue.

Do not infer information value by comparing QUERY solely against SKIP.
The QUERY-versus-WAIT difference with matching duration identifies
the **fresh cue's performance increment** at fixed action time.
The best conditional policy must also be compared with universal
QUERY and the old-cue-conditional no-query WAIT/SKIP baseline,
not merely an artificially weak fixed schedule.

Public mosquito and pollinator archives in the current repository
generally do not include these matched-WAIT acquisitions and payoff
contrasts in the same individuals. Experimental validation remains
on HOLD; neither the failed CI nor the corrected algebra establishes
natural selection for one sensory architecture.

## Related experiments and novelty boundary

The idea of separating the influence of time from information is
**not** new:

- A 2002 gray-jay study explicitly compared longer delays with and
  without opportunity to inspect rewards, using opaque covers to
  determine whether improved choice was merely caused by further
  information processing (https://pubmed.ncbi.nlm.nih.gov/12461598/).
  It is a strong precedent for the WAIT/sham intervention.
- A 2024 pigeon experiment differentiated manipulating reward
  probability, reducing time until reward, and obtaining earlier
  information about an outcome
  (https://doi.org/10.3389/fpsyg.2024.1426434).
  Therefore neither "delay can matter" nor "measure information
  separately" can carry a novelty claim.
- Canessa et al. 2015
  (https://doi.org/10.1111/2041-210X.12423) emphasize
  that additional environmental information is valuable for a
  decision only relative to explicitly defined actions and
  management objectives.

The *current corrective contribution* is narrower:
a state-transition calculation that concretely exposes an
uninformative-sensor false positive in the existing
conditional-acquisition comparator, an operational WAIT
baseline that removes it, and an exactly reproducible change
in the sensor-quality window. The wider literature already
anticipates why such a control matters.

### The exact timing-versus-opportunity criterion

Even if the sensor returns zero new information, a delayed
action can improve performance conditional on old report o
precisely when

\[
 e^{-\mu r}
 h\!\left[\pi_1+(p_o(\tau+a)-\pi_1)
 e^{-(\alpha+\beta)r}\right]
 > h[p_o(\tau+a)].
\]

That is a state-drift-versus-opportunity-loss inequality,
not an information-value theorem. In the limit of an
effectively frozen environment, the conditional state
distribution does not change during r; with \(\mu>0\),
the criterion cannot hold, so WAIT is dominated by SKIP.
Independent regression tests include this frozen-environment
negative control.

The planned experiment should **not** simply maximize
differences between wait and query at different times.
It needs identical observation/decision times, matched
handling and opportunities, and independently measured
post-cue environmental change. Otherwise chemical cue
degradation, decision preparation and background reward
dynamics remain confounded.

## 7. Reproducibility and claim boundaries

- adaptive_gain/waiting_control.py implements SKIP/WAIT/QUERY,
  gross information and timing decomposition, the adjusted precision
  window and a model-specific log maintenance ceiling.
- tests/test_waiting_control.py independently enumerates 192
  old-state/old-report/new-state/new-report/final-state cases,
  including terminal action maps and fixed/conditional schedules.
- tests/test_selective_refresh.py replaces the invalid
  uninformative-cue assertion with the corrected negative control.
- biology/SENSOR_PRECISION_ADAPTIVE_PREMIUM_V1.md and
  biology/BLACKWELL_ORDERED_SENSING_WINDOW_V1.md require
  interpretation alongside this matched-WAIT correction.

The static finite deterministic query frontier (V6 MAIN 1–3)
remains separate. This note is a **retraction of a biological
interpretation**, not a rejection of the original arithmetic.
