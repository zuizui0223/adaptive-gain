# Why maximal sensor precision need not maximize the benefit of contingent re-sensing

**Status:** supporting ecological model, not V6 MAIN 4, not field evidence of
evolutionary selection, and not a novel Blackwell or decision-theory theorem.

## Distinguish absolute sensory value from relative conditional-control value

A precise signal can improve attainable performance while decreasing the
*incremental premium of a conditional sensing policy* relative to a fixed
sensing schedule. These are different quantities with different comparators.

The currently modeled environment is a binary stationary continuous-time
Markov process, with transition rates alpha (0->1) and beta (1->0).
An old cue reports X(-tau) with optional symmetric error eps_old. The
subject may skip further observation and act after a, or spend r time
acquiring a refreshed binary cue Y of X(r) with symmetric error
eps_new, then act after the same a. At decision time the environment
may have changed again. The organism makes Bayes-optimal terminal actions
conditional on *all available cues*; it does not simply copy either
cue label. Correct actions earn r0/r1 and a mismatch earns zero.

Opportunity survival is exp(-mu*t), and re-sampling incurs a per-attempt
additive debit K. The hidden ecological world moves during cue sampling,
so the static V6 finite deterministic routing theorems do not directly
imply these results.

## Full noisy re-query objective

After observing old report o, define
p_o = Pr(X(r)=1|O=o), after propagating the Bayes posterior from
the old observation through tau+r.

The *joint* probability of refreshed report Y=y and final state Z=z is

\[
j_{oz}(y)=\sum_{x=0,1}
 Pr(X(r)=x\mid O=o)
 Pr(Y=y\mid X(r)=x)
 Pr(Z=z\mid X(r)=x).
\]

This retains information from O even when refreshed Y is noisy. The
optimized refresh payoff for that old report is

\[
Q_o(\epsilon_{\rm new})
=e^{-\mu(r+a)}\sum_{y=0,1}
 \max\{r_0j_{o0}(y), r_1j_{o1}(y)\}-K.
\]

If S_o is the optimal skip payoff, d_o=Q_o-S_o and w_o is the
actual prevalence of old **reports** (which differs from true state
prevalence when eps_old>0), then

\[
\boxed{
G(\epsilon_{\rm new})=
\min\{\sum_o w_o(d_o)_+,\,\sum_o w_o(-d_o)_+\}.
}
\]

This is the additional expected payoff of letting the old report
control whether to re-query, *relative to the better of always
refreshing and always skipping*, both allowed to optimize the final action.

It is strictly positive exactly when the branch-specific re-query
incentives have opposite signs, d_0*d_1<0, as long as both old reports
have positive probability.

## One strict negative control and one seemingly paradoxical result

Blackwell informativeness gives an important control. Increasing the
symmetric binary reporting error eps_new from 0 to 0.5 garbles an
otherwise more informative refreshed observation, so for fixed timing,
reward and cost, every Q_o is nonincreasing. The *absolute* optimized
conditional payoff J_conditional is therefore nonincreasing.

However, the fixed comparator can change from "always re-query" to
"never re-query" while the adaptive policy switches between them in a
report-dependent way. Consequently the *difference* G need not be
monotone in precision.

Example, in dimensionless parameters:
alpha=.8, beta=.2; true state 0 is rare at 20%;
old cue perfectly accurate at acquisition but age tau=1.2;
sampling r=.15, final action delay a=.1;
opportunity hazard mu=.25; per-re-query debit K=.03;
r0=r1=1.

At this old-cue age, the old report does **not** change the
optimal immediate terminal action compared with no cue:
tau>ln(8/3), the direct-action expiry threshold.

| Refreshed observation error eps_new | Conditional schedule for old reports (0,1) | Absolute optimized conditional expected reward | Strict premium over best fixed schedule |
|---:|---|---:|---:|
| 0.00 | (refresh,refresh) | 0.8808060 | 0 |
| 0.03 | (refresh,refresh) | 0.8543401 | 0 |
| 0.06 | (refresh,skip) | 0.8303438 | 0.0024697 |
| 0.09 | (refresh,skip) | 0.8251841 | 0.0237760 |
| 0.114 | (refresh,skip) | 0.8210563 | 0.0408084 |
| 0.12 | (refresh,skip) | 0.8200244 | 0.0397764 |
| 0.20 | (refresh,skip) | 0.8062652 | 0.0260172 |
| 0.30 | (refresh,skip) | 0.7890662 | 0.0088182 |
| 0.50 | (skip,skip) | 0.7802479 | 0 |

In this example, strict conditional value exists only for approximately
0.05652 < eps_new < 0.35127. A grid search with eps_new steps of 0.001
places the relative-premium maximum near eps_new=0.114, with
G approximately 0.04081.

**Do not misread the result** as sensory imprecision increasing organism
performance: total optimized expected reward declines from 0.880806
at perfect refreshed sensing to 0.821056 at eps_new=.114 and to
0.780248 at uninformative refreshed sensing.

Nor can G be read as a population-genetic selection coefficient:
heritable differences in sensing/control maintenance, equipment cost
versus precision, natural encounter frequencies and fitness consequences
are not measured here.

## Negative controls and robustness boundaries

- eps_new = 0.5: a refreshed observation is independent of the
  refreshed state. Under a nonnegative time penalty and nonnegative K,
  it cannot improve the decision relative to immediate skip;
  G=0.
- eps_old = 0.5: the old report carries no contextual information,
  so contingent acquisition offers no benefit over the best fixed schedule.
- For any fixed old report, increasing eps_new weakly decreases Q_o;
  it cannot *create* a positive re-sampling incentive where one was
  previously absent. The relative gap G can still rise when a
  formerly positive incentive in one branch becomes negative while
  another remains positive.
- If the signal error rate changes together with equipment,
  detection/maintenance costs or acquisition duration, these must
  be modeled together; the fixed-cost precision result no longer
  determines the evolutionary comparison.

These are model statements, not a universal numerical ecological
threshold for 5%, 10%, 35% or 50% cue error.

## Prior art and prospective ecological test

Do not claim novelty for optimal sampling, speed-accuracy trade-offs,
Blackwell monotonicity or nonmyopic acquisition value.

- Abbott & Sherratt (2013), "Optimal sampling and signal detection:
  unifying models of attention and speed-accuracy trade-offs",
  Behavioral Ecology, https://doi.org/10.1093/beheco/art001:
  established payoff/time/error dependent optimal sampling.
- "What makes information valuable: signal reliability and
  environmental uncertainty", Animal Behaviour 71 (2006),
  https://doi.org/10.1016/j.anbehav.2005.09.006:
  captive blue-jay experiment varying environmental uncertainty
  and signal reliability.
- Dall et al. (2005), "Information and its use by animals in
  evolutionary ecology", Trends in Ecology & Evolution,
  https://doi.org/10.1016/j.tree.2005.01.010.

The narrower ecological question worth testing is the joint prediction
that the *next cue acquisition decision* changes with old cue identity,
state turnover, reward asymmetry, refresh precision and elapsed time,
even where old information cannot change the terminal action directly.

A realistic falsification test would manipulate false-negative loss,
old-cue reliability, refresh-cue quality and acquisition latency
orthogonally, measuring both the selected *next cue* and realized
payoff; the assay must compare optimized conditional acquisition with
**both** always-refresh and never-refresh regimes. The prior literature
makes explicit optimal-policy and ecological-process comparisons
necessary, not optional.

## Audit

- ../adaptive_gain/selective_refresh.py: exact joint-state
  computation for noisy refreshed observations; posterior from old
  observation retained.
- ../tests/test_selective_refresh.py: an independent path enumerator
  maximizes over four refreshed-report-to-action maps, then four
  old-report-to-acquisition schedules, for 320 combined old/new
  error/transition/reward/age scenarios.
- Independent 320-case arithmetic comparison produced zero
  mismatches, maximum absolute difference 1.8e-15.
- Additional tests check the intermediate-precision premium, old
  direct-value extinction, Blackwell monotonicity of absolute
  expected reward, uninformative new cues and cue fusion.

No empirical fitness test is claimed; no promotion to a V6
MAIN theorem without changed substantive novelty and evidence.
