# Conditional re-sensing can survive the expiry of direct cue value

**Status:** ecological-process / source-of-gain stress test for PR #67.
Not V6 MAIN 4. Not a result about the static-world sharp
\((n,m,b)\) frontier; this model explicitly permits environmental
state changes during acquisition. No direct biological selection
validation is claimed.

## Mechanistic question

A cue may be too old to alter *the action taken now* and still matter for
*whether to buy another observation*. The two notions of information
value must not be conflated.

Likewise, increasing the relative cost of missing a rare dangerous state
can reverse which old observation triggers re-sampling. The mechanism is
not "rare event -> always sample": when an old danger cue already
justifies an immediate defensive response, re-checking that cue can waste
an opportunity; the apparently safe cue can instead warrant checking
because a missed late hazard is costly.

The general idea that sequential observations have value through subsequent
acquisition decisions predates this repository. Miller (1975), "The Value
of Sequential Information", Management Science 22:1-11, explicitly
recognized that an observation can be valuable because it changes whether
later observations are purchased:
https://doi.org/10.1287/mnsc.22.1.1.
Other prior art includes non-myopic value-of-information analysis
(Heckerman, Horvitz & Middleton 1993,
https://doi.org/10.1109/34.204912).
This note contributes an **audited finite ecological witness and a
measurable comparator experiment**, not a generic new theorem.

Predator error costs are well established: a recent risk-uncertainty review
notes that missing danger can have much greater consequences than losing a
safe foraging opportunity (Crane et al., Biological Reviews, 2024,
https://doi.org/10.1111/brv.13019). This existing ecology motivates the
payoff contrast but **does not validate the proposed resampling behavior**.

## Explicit moving-state protocol

- Environmental state \(X(t)\in\{0,1\}\) is a stationary, binary
  continuous-time Markov chain. State 0 is rare (e.g. danger) and
  state 1 is common (e.g. safety). Rates: \(\alpha:0\to1\),
  \(\beta:1\to0\), \(\pi_1=\alpha/(\alpha+\beta)\).
- A perfect old cue reports \(x=X(-\tau)\). Its acquisition cost is
  sunk and identical for all architectures.
- At time 0, the decision-maker may **skip** or **refresh**, as a
  function of old cue \(x\). Skip acts after terminal action
  delay \(a\). Refresh spends time \(r\), reveals \(Y=X(r)\)
  perfectly, then acts after the same \(a\).
- During \(\tau,r,a\) the environment continues to change.
  A correct action in state 0 pays \(r_0>0\), and in state 1
  pays \(r_1>0\); the alternative is zero. At terminal action,
  optimal action choice is permitted after whatever signal is
  available. No forced "follow the old cue" assumption.
- An independent ecological opportunity survives completion time
  \(t\) with probability \(e^{-\mu t}\). A refresh attempt costs
  \(K\) in additive expected-reward units **even if the opportunity
  subsequently closes**. This is not constitutive architecture
  maintenance cost.

Write

\[
p_x(s)=\pi_1+(x-\pi_1)e^{-(\alpha+\beta)s},\qquad
h(p)=\max\{r_0(1-p),r_1p\}.
\]

Then the two branch-local optimized values are

\[
\begin{aligned}
S_x &=e^{-\mu a}h[p_x(\tau+a)],\\
Q_x &=e^{-\mu(r+a)}
\big[
 (1-p_x(\tau+r))h[p_0(a)]
 +p_x(\tau+r)h[p_1(a)]
\big]-K.
\end{aligned}
\]

Here \(S\) means skip and \(Q\) refresh, not ecological survival
\(e^{-\mu t}\). The refresh posterior at the final action depends
only on the new signal \(Y\) by the Markov property.

## Exact precommitted-versus-conditional schedule advantage

Let \(d_x=Q_x-S_x\). A controller that reacts to old cue \(x\)
obtains

\[
J_{\rm conditional}=\sum_{x=0}^1\pi_x\max(S_x,Q_x).
\]

A **precommitted schedule** must choose refresh or skip before
learning the old cue's outcome (but may still choose its terminal
action optimally from its eventual information):

\[
J_{\rm fixed}=\max\big\{\sum_x\pi_x S_x,\sum_x\pi_xQ_x\big\}.
\]

The extra value due *only* to contingent re-sensing is therefore

\[
\boxed{
J_{\rm conditional}-J_{\rm fixed}
=\min\Big\{
\sum_x\pi_x(d_x)_+,
\sum_x\pi_x(-d_x)_+
\Big\}.}
\]

With positive occupancy of both old-cue states it is **strictly
positive exactly when** \(d_0 d_1<0\). This is an elementary
weighted option-value decomposition, not an original optimization
theorem. It is useful because any claimed biological gain from
"flexibility" now has to demonstrate opposite branch-local net
incentives, not merely a time-varying motor response.

## Witness A: which cue triggers the next sample reverses

Common environment/operational parameters are
\(\alpha=.8,\beta=.2,\tau=.1,r=a=.15,\mu=.25,K=.015\).
Hence state 0 is rare (20%). Only the reward ratio changes.

| \(r_0:r_1\) | Old cue 0 (danger) | Old cue 1 (safe) | \(J_{\rm conditional}\) | \(J_{\rm fixed}\) | strict gain |
| --- | --- | --- | ---: | ---: | ---: |
| 1:1 | refresh | skip | 0.901082770 | 0.895015905 | 0.006066864 |
| 2:1 | skip | skip | 1.053565533 | 1.053565533 | 0 |
| 4:1 | skip | refresh | 1.428499894 | 1.370664788 | 0.057835106 |

Thus merely increasing the importance of the rare state changes
the favored **acquisition program**, not just the final action.

In a declared local sensitivity grid varying \(\tau\) across
(.08,.10,.12), \(r,a\) each across (.13,.15,.17), \(\mu\) across
(.22,.25,.28), and \(K\) across (.013,.015,.017), all \(3^5=243\)
configurations retain the 1:1 versus 4:1 schedule reversal
and positive conditional gain. This is not a random sample of
nature or a global robustness theorem.

## Witness B: zero value for acting, positive value for routing

Maintain \(\alpha=.8,\beta=.2,\ r_0=r_1=1\).
The earlier direct-action experiment establishes that at lag

\[
\tau\ge\ln(8/3)\approx.980829,
\]

the optimal immediate action ignores old cue \(x\), because
both posteriors assign state 1 a probability above one-half.
For \(\tau=1.2\), direct old-cue action value is **zero**.

Now set \(r=a=.15,\ \mu=.25,\ K=.1\). The exact
conditional schedule is **refresh after old danger cue 0,
skip after old safety cue 1**.

\[
\begin{aligned}
J_{\rm always\ skip} &=0.770555534,\\
J_{\rm always\ refresh}&=0.786390761,\\
J_{\rm conditional}&=0.810458296,\\
J_{\rm conditional}-J_{\rm fixed}&=0.024067535>0.
\end{aligned}
\]

The old observation therefore still has **positive control value**
for choosing whether to acquire *new* information despite
having **zero direct terminal-action value**. Its posterior
predictivity is not zero; rather, the posterior differences
remain insufficient to change the terminal action but
sufficient to change the expected value of sampling again.
This is one instance of a known non-myopic information value
mechanism, not a contradiction of standard decision theory.

In the limit \(\tau\to\infty\), old-cue posteriors coincide
and the conditional advantage vanishes.


## Cue reliability is a real constraint (not a cosmetic caveat)

The perfect old-cue assumption can be relaxed to a symmetric binary
misclassification probability \(\varepsilon\in[0,1/2]\). The new
re-query remains perfect in this sensitivity model, and its cost and
time burden stay fixed.

The probability of the observed old cue \(O=1\) is now

\[
q_1=\pi_1(1-\varepsilon)+\pi_0\varepsilon,
\]

and the initial state-1 posterior used in the skip/refresh branch is

\[
p_{O=1}={\pi_1(1-\varepsilon)\over q_1},\quad
p_{O=0}={\pi_1\varepsilon\over 1-q_1}.
\]

Subsequent Markov transitions operate on these posterior values
instead of treating the reported old state as known exactly.
The unconditional branch weights are \(1-q_1,q_1\), not
\(\pi_0,\pi_1\).

At the Witness A parameter settings, the cue-driven direction
reversal persists at symmetric old-cue error probabilities
0, .01, .03, .05 and .08. The reported 4:1 reversal is **not**
robust at .10: both old-cue outcomes then favor refreshing,
and the conditional-over-precommitted gain becomes zero.
With \(\varepsilon=.5\) the old cue conveys no state
information, so conditional acquisition cannot improve on
the best precommitted schedule.

This is **not** a universal .08/.10 biological threshold.
It shows that measurement reliability is an indispensable
dimension, and identifies a falsifiable negative-control
boundary for the displayed hypothetical ecology.
Independent brute-force evaluation enumerates the latent old
state, imperfect old observation, new state and terminal
state across seven error values.

## Test and scope receipt

Executable:
- ../adaptive_gain/selective_refresh.py
- ../tests/test_selective_refresh.py

The suite independently enumerates terminal action choices and
all four refresh/skip schedules, using the Markov transition
matrix over initial, resampled and final states. A 512-condition
Cartesian grid checks the policy values against separate
enumeration. Another 243-case neighborhood audits the
payoff-driven direction switch. A 7x3x3x4 grid checks the
mixed-sign decomposition. Local eight-test suite passed
before GitHub commits; latest head CI must be checked separately.

The old cue's *acquisition cost is sunk*. Both old and refreshed
binary reports can now have independent symmetric misclassification
errors, with their Bayes posteriors combined at the terminal decision.
The original witness assumes zero errors. See
`SENSOR_PRECISION_ADAPTIVE_PREMIUM_V1.md` for the refreshed-cue
precision threshold and an independent 320-scenario path-enumeration
audit. Stochastic refresh delays, nonbinary observations,
context-dependent opportunity survival, additional refresh rounds
and genotype-specific equipment costs remain outside this model. Static V6 MAIN 1–3 remain
unchanged.

## Biological experiment with falsification criteria

Use an experimentally controlled environment with two states,
a randomized old warning/safety cue, an independent
state-switching schedule, and an optional **explicit re-query
action** that costs time or reward. Factorially manipulate
(i) cue-to-action lag, (ii) false-negative versus false-positive
payoff contrast, and (iii) refresh latency. Record within
individuals *which next cue was acquired*, final state,
selected final action, realized payoff and available
opportunity. A nonharmful simulated threat or safe/unsafe
resource signal is sufficient for this mechanism test; a
real predator attack is neither required nor desirable.

Main prediction: under a suitable common environment,
raising the relative cost of missed danger switches
the re-query trigger from old danger to old safety.
Controls:
- terminal actions may optimize in all arms, not be forced
  to mirror prior cues;
- compare conditional refresh with both uniformly refresh
  and uniformly skip, **not** just one deliberately weak
  control;
- document nondecision motor priming separately from cue
  *acquisition*;
- pre-register the sign of both branch-specific incremental
  values \(d_0,d_1\) before analyzing the observed advantage;
- do not claim evolutionary selection unless long-run
  reproductive consequences and genotype-specific
  maintenance/developmental costs are measured.

The current public Aedes and bumblebee datasets do not
satisfy this full contract. This is a prospective,
falsifiable ecological process prediction.
