# Ordered cue quality makes the conditional-sensing premium single-peaked

**Status:** ORIGINAL TWO-SCHEDULE SHAPE CERTIFICATE; read alongside
WAIT_VERSUS_INFORMATION_CAUSAL_GATE_V1.md. With a moving
payoff-relevant environmental state, the original bundled query can
also work as a state-conditioned delay. The algebra below remains
correct for that narrower bundled comparator, but its numerical G
cannot be attributed entirely to new information. For the
matched-WAIT information-acquisition control, replace S_x with
M_x=max(SKIP_x,WAIT_x) in the same derivation; this retains the
weak unimodality guarantee, but changes the active window and peak.
Analytic falsification constraint for the dynamic re-query model on PR #67, *not* a V6 MAIN 4 or a claim of new general sequential-decision theory. The source of the argument is classical Blackwell informativeness + an elementary two-schedule option-value identity; conditional information procurement is also established (Miller 1975, https://doi.org/10.1287/mnsc.22.1.1). Blackwell ranking has extensive prior art; see Athey & Levin's discussion (1998/2001, https://papers.ssrn.com/abstract=140591) and the decision-theory background in V6.

## Biological question

Could a real sensory system have its **highest premium from contingent cue acquisition** at intermediate cue accuracy, even though the organism's best achievable absolute performance is greater at higher accuracy?

The previous SENSOR_PRECISION_ADAPTIVE_PREMIUM_V1 gives one positive finite Markov witness. Here the stronger result is a **falsifiable shape constraint**: under a quality family ordered by Blackwell garbling with sampling time, costs, natural-history state process and payoff fixed, that *relative* premium must be weakly single-peaked. It cannot have multiple separated positive windows or two distinct peaks separated by a genuine dip.

## General finite-branch calculation

Let x in X denote an old cue observation, with probabilities w_x>0 summing to one. The old cue is available for terminal decisions in both comparator policies. Let S_x be the optimized performance conditional on x when no refresh is attempted. Let Q_x(q) be the optimized performance when a new cue of quality index q is bought. Define q increasing toward **worse** observations (greater imprecision); suppose for q_1<q_2, the q_2 signal is a Blackwell garbling of q_1. All signal-dependent policies permitted at q_2 can therefore be implemented at q_1 by simulating the garbling; costs, terminal actions, signal-access timing and encounter law stay equal. Consequently Q_x(q) is nonincreasing for every x. S_x is independent of q.

Set d_x(q)=Q_x(q)-S_x. The contingent controller attains J_C(q)=sum_x w_x max(Q_x(q),S_x).
The best universally precommitted schedule attains J_F(q)=max(sum_x w_x Q_x(q),sum_x w_x S_x).
A controller that can see x before choosing the next acquisition but pays no separate controller overhead therefore gets additional value

\[
G(q)=J_C(q)-J_F(q)
 =\min\{P(q),N(q)\},
\]
\[
P(q)=\sum_xw_x[d_x(q)]_+,\qquad
N(q)=\sum_xw_x[-d_x(q)]_+ .
\]

By monotonicity of each d_x, P is nonincreasing, and N is nondecreasing. Therefore G(q) is **weakly unimodal**, possibly identically zero or attaining its maximum on an interval or boundary. Moreover, G(q)>0 iff at least one branch has d_x(q)>0 and another has d_y(q)<0; this is one interval (possibly empty) along the ordered quality family.

If an interior crossing P=N with G>0 occurs, every point of the crossing plateau maximizes G. But

\[
P(q)-N(q)=\sum_x w_xd_x(q)
        =J_{\rm always\ refresh}(q)
         -J_{\rm always\ skip}.
\]

Hence the peak occurs **where the two best fixed schedules are indifferent**. If no crossing occurs in the active interval, the maximum is at one of its boundaries, not necessarily at a fixed-schedule tie. There is no claim of unique strict peak without additional regularity.

## Numeric example and controls

Use the same two-state Markov scenario as SENSOR_PRECISION_ADAPTIVE_PREMIUM_V1.md:
alpha=.8, beta=.2, old cue age=1.2, sampling time=.15, terminal action delay=.1, opportunity hazard=.25, r0=r1=1, per-attempt refresh debit K=.03, old cue accurate.

For a symmetric binary refreshed-signal error epsilon in [0,.5], higher epsilon is a Blackwell garbling of lower epsilon, with all operational quantities held fixed.

For the original two-schedule bundled comparison, the precise
active window (to approximate 1e-8) is

\[
0.05652258<\epsilon<0.35127167.
\]

This original bundled relative premium peaks at the crossover of expected values of *always refresh* and *always skip*, at epsilon approximately .113985736, where G is approximately 0.040810843 in expected-payoff units. At perfect new sensing, both branches favor refresh, so no conditional schedule gain is left; at uninformative sensing, both favor skip, also giving zero conditional gain. Throughout this process the absolute optimized conditional expected payoff is nonincreasing with epsilon. This does **not** favor worse sensing per se.

The matched-WAIT corrected numbers, computed by waiting_control.py,
are 0.05652258 < epsilon < 0.34238957 and the maximum
0.03958103 at epsilon=0.11225411. Only the latter comparison
isolates genuine optional information acquisition relative to a
no-query controller that may conditionally WAIT or SKIP.

The ordered_accuracy_window.py module estimates the two branchwise crossings and the fixed comparator's tie by monotone bisection. It returns a numerical root *estimate*, not a formal interval-arithmetic proof. Tests independently inspect a dense error grid, verify the branchwise Blackwell monotonicity, and check the shape theorem for general 3-branch synthetic monotone payoffs.

## Ecological hypotheses with genuine failure conditions

**H1 (single sensing channel, ordered precision).** Manipulate the accuracy of one new cue while holding the cue-age distribution, observation duration, per-query cost, ecological transition process, payoff matrix and old cue unchanged. Estimate two old-cue-conditional refresh incentives d_0(q),d_1(q) independently and calculate the contingent premium over the best fixed schedule. The expected gain curve must be weakly single-peaked, and the plateau/peak of an interior case must align with fixed-schedule indifference.

**H2 (multi-regime failure diagnostic).** If the empirical relative premium has two statistically supported separated maxima with a genuine valley, at least one listed assumption fails: e.g. quality manipulations also change acquisition latency, metabolic cost, cue identity/context, motor behavior, payoff, or the cue-family Blackwell order. Such data would falsify the narrow single-channel model, not the general concept of adaptive sensing.

**H3 (ecological comparator gate).** Even an observed G>0 only shows benefit relative to *these two precommitted acquisition schedules*. A context-preindexed repertoire with other accessible programs could dominate the routed architecture (see COMPARATOR_SEMANTICS_FITNESS_GATE.md). Only comparable long-run performance plus heritable controller maintenance costs would license an evolutionary fitness claim.

Data contract: for every animal/trial, record the realized old cue, optional new cue, its calibrated error probability, true environmental state at acquisition and action, cue timestamps, opportunity closure, terminal action, reward, and either randomized assignment or independent estimates for *both* fixed-comparator regimes. Uncertainty must include individual clustering and independently measured cue classification errors.


## Closest ecological experiments found, and why they do not close this gate

The strongest nearby work is not yet a direct validation:

- Leadbeater, Chittka and collaborators' bumblebee cue-weighting
  experiment ("Foraging Bumble Bees Weigh the Reliability of
  Personal and Social Information", Current Biology 2016,
  https://doi.org/10.1016/j.cub.2016.03.009) manipulated the
  reliability of personal and social floral reward information
  (100%, 83%, 50%). It documented behavioral cue preference,
  but not the *optional acquisition* of a new sample with a
  measured runtime cost and two optimized fixed-schedule
  controls. Therefore it cannot validate the G(q) peak.
- Austin, Horack and Dunlap (Behavioral Ecology 2018/2019),
  https://doi.org/10.1093/beheco/ary190,
  published the Dryad spreadsheet
  https://doi.org/10.5061/dryad.0rh6sg5.
  Its individual/block-level schema includes manipulated
  reward reliability, signal complexity and number of floral
  types, with foraging efficiency, selectivity and decision
  latency. This is a **usable public timing and performance
  sensitivity anchor**. It does *not* record a randomized
  "refresh or skip" information-acquisition action against
  both fixed regimes; published metadata do not establish
  per-trial refreshed cue reliability. Thus direct phase-window
  inference is currently **HOLD**.
- Baracchi et al. (Behavioral Ecology 2017),
  https://doi.org/10.5061/dryad.743g3,
  provide per-bee correct-choice traces across easy and hard
  discrimination tasks, including social/personal cue
  conditions. These can test cue-use correlations and learning,
  not a precommitted-versus-conditional **acquisition** advantage.

This screening is based on the official publication
descriptions and public Dryad dataset schemas; it is not a
completed row-level reanalysis. The scientific gap is not
that bumblebees are known to respond to reliability (they are),
but whether the *acquisition-control premium* exhibits the
specific bounded unimodal behavior after holding common
ecological and operating costs constant.

### Crucial empirical distinction: accuracy is not Blackwell order

A mere ranking of classification accuracies does **not**
guarantee Blackwell nesting. Changing signal modalities,
nonstationary calibration, correlated errors between old
and new cues, or condition-specific detection failure may
make the new signals incomparable as experiments,
especially **conditional on the old cue**. Without
pre-validated conditional garbling kernels, failure of
unimodality is not evidence for selection against the
theoretical prediction; it signals that the model's
assumptions are unverified.



## Explicit bridge to PAYOFF: a controller-cost ceiling, not a fitness observation

Separate per-decision acquisition debit K (already included in J_C
and J_F) from constitutive maintenance costs kappa_C and kappa_F.
If a biological architecture has a shared baseline gross fitness
w0>0, and timely per-decision reward is assumed to contribute
to gross fitness in the same additive currency, write

\[
W_C(q)=e^{-\kappa_C}[w_0+J_C(q)],
\qquad
W_F(q)=e^{-\kappa_F}[w_0+J_F(q)].
\]

The log-selection coefficient in this declared pairwise comparison is

\[
s_{C:F}(q)=\log\left(
1+\frac{G(q)}{w_0+J_F(q)}
\right)-(\kappa_C-\kappa_F).
\]

With fixed w0 and costs, the same accuracy that maximizes
the conditional premium G also maximizes this log-fitness
allowance. Proof: before the fixed-schedule tie, G=N
increases while J_F=J_always_refresh decreases; after the
tie, G=P decreases while J_F=J_always_skip is constant.
If no tie occurs inside the active window, both maxima
occur on its same relevant boundary.

Consequently the **maximum log-maintenance difference that
can be repaid by contingent control** under the declared
sensor-quality family is

\[
\boxed{\kappa^{\rm crit}_{C:F}
=\max_q\log[1+G(q)/(w_0+J_F(q))].}
\]

This does not make the controller selectively advantageous
without a biologically justified comparator, measurable
maintenance costs, heritable variation and an empirical
fitness link.

For the **original two-schedule bundled comparison**, the
illustrative Markov settings of this note and
chosen gross baseline w0=1 expected-reward unit, the
fixed schedule's performance at the peak is 0.78024793,
G_peak=0.040810843 and therefore

\[
\kappa^{\rm crit}_{C:F}\approx0.022665434
\]

in log-fitness cost units. Above this **model-specific**
maintenance contrast, no sensor precision within [0,.5]
can repay the controller relative to the declared fixed
schedules. This is a conditional resource ceiling,
not a measured selection coefficient or a separate
novelty theorem. Different w0 changes the numerical ceiling.

With an explicit matched-WAIT comparator, the corrected w0=1
log-maintenance ceiling is 0.02197123, not 0.02266543.
The first number bounds the extra cost of conditional querying
*after removing timing-only optionality*; neither is measured
biological selection.

Executable bridge: controller_log_cost_ceiling in
adaptive_gain/ordered_accuracy_window.py; regression tests
evaluate the log ratio on a separate dense precision grid.


## Stop rule

Do not elevate this to a fourth V6 headline result. A new monotonicity or Blackwell-value theorem is not claimed. This is a compact source-of-gain certificate and a precise *ecological falsification target* where the extra value of conditional acquisition is isolated from absolute accuracy.

Source / regression:
- adaptive_gain/ordered_accuracy_window.py
- tests/test_ordered_accuracy_window.py
- adaptive_gain/selective_refresh.py
