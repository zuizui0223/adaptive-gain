# Finite noisy evidence changes the high-loss reward limit

Status: support audit for PR #68, not a new MAIN theorem or an empirical result.
Reader path: this note, `adaptive_gain/deadline_noisy_reward.py`, and
`tests/test_deadline_noisy_reward.py`. The deterministic solver is unchanged.

## Question

The previous error-free benchmark gives a two-query adaptive reward premium
`q*min(v+L,2v)`. Can the positive high-loss plateau be extrapolated to imperfect
perception? No: full-support finite noisy evidence changes that limit.

We retain the same latent five-state task, target vector `(0,1,1,0,0)`, and
binary query vectors A/B from the previous reward audit. Each query is acquired
at most once. Conditional on the latent state, its perceived bit is flipped
independently with common probability `epsilon`. Known priors and the channel
are used by both optimizers. Adaptive queries depend on **perceived** outcomes,
never on latent truth. The nonadaptive control precommits any affordable partial
subset, can classify from it, and can abstain. It is not forced to buy a full
universal-resolving bundle. Query costs consume budget but carry no extra payoff
debit. Correct choices pay `v>0`, errors `-L`, and abstention zero.

This fixes latent cue partitions, not the entire observation model: adding
noise explicitly changes the stochastic information available to the actor.
The error-free `(C_A,C_F)` values must not be treated as guarantees under noise.

## 1. Shared all-abstention boundary

For a feasible observation history h and target y let

`m_y(h) = P(Y=y, h)` and `r(h,y) = m_y(h) / sum_{z!=y} m_z(h)`.

Define `R_star(B)` as the maximum of r over all budget-feasible histories and
targets, including the empty history. For finite binary readouts, positive
priors on at least two target classes, and `0<epsilon<=1/2`, every history has
positive mass under every latent state. Thus no history certifies the target,
and `R_star(B)` is finite in exact arithmetic.

Because the payoff for choosing y at h is `v*m_y(h)-L*sum_{z!=y}m_z(h)`,

```
optimal gross reward is zero in BOTH policy classes iff L/v >= R_star(B).
```

Proof: above the bound all target actions are nonpositive at every terminal
history; abstention achieves zero. Conversely, below the bound choose the
precommitted subset of a history attaining the maximum, act on that history,
and abstain otherwise. It has positive expected reward; adaptive access contains
that same policy. Every history of an adaptive tree is an observation of one
such subset, so adaptivity cannot change this **positivity boundary**. It can
change how often valuable histories are reached and hence their total reward.
At equality a zero-reward action can tie abstention; only strictly above the
bound is every target action strictly worse. No unique action rate is inferred
at ties. A fixed subset may use a terminal decision depending on its observations.

This argument requires finite/bounded evidence, not just the word "noise".
It does not extend to unbounded likelihood ratios from continuous observations,
unbounded repeated sampling, or different outside-option/acquisition payoffs.

## 2. The deterministic plateau is a singular limit

Let `Delta_epsilon(L)` be A's two-query adaptive-minus-fixed gross premium for
the old prior family `p=(t,q,q,q,q)`, `q=(1-t)/4`, `1/5<t<1`.
For every strictly positive epsilon, section 1 gives
`lim_{L->infinity} Delta_epsilon(L)=0`. At zero noise, the previous audit proved
`lim_{L->infinity} Delta_0(L)=2vq`.

At fixed finite L, expected reward for any one of the finitely many policies
is continuous in epsilon. Their maximum is continuous as well. Consequently,

```
lim_{epsilon->0+} lim_{L->infinity} Delta_epsilon(L) = 0,
lim_{L->infinity} lim_{epsilon->0+} Delta_epsilon(L) = 2vq.
```

The previous plateau is valid within its error-free assumptions, but it is not
a noise-robust high-danger prediction. This is an assumption audit, not a claim
of novelty for generic Bayesian rejection or order-of-limits phenomena.

## 3. A fully enumerated example with a bounded viability interval

Set `t=1/3`, `q=1/6`, `epsilon=1/10`, budget B=2 and v=1. These are illustrative
model inputs, NOT fitted sensory-error or fitness estimates.

An independent rational oracle enumerates every full perceived cue vector,
every feasible query tree, and every terminal action (target 0, target 1,
abstention). A yields 391 distinct adaptive `(correct,error)` mass pairs and
208 nonadaptive pairs. Each pair defines a reward line `C-L*E`. The upper
envelopes of these lines below are certified on **whole intervals**: every
candidate line is below the stated active line at both interval endpoints.
For the final ray the active line is zero and all competing slopes are
nonpositive. This proves global optimality here, rather than a grid-only fit.

| L interval | Adaptive A value | Nonadaptive A value |
|---|---|---|
| 0 to 6/5 | 127/150 - 23L/150 | 77/100 - 23L/100 |
| 6/5 to 7/5 | 127/150 - 23L/150 | 3/4 - 16L/75 |
| 7/5 to 3/2 | 127/150 - 23L/150 | 44/75 - 29L/300 |
| 3/2 to 5/2 | 127/150 - 23L/150 | 167/300 - 23L/300 |
| 5/2 to 41/14 | 209/300 - 7L/75 | 167/300 - 23L/300 |
| 41/14 to 42/5 | 14/25 - 7L/150 | 21/50 - 3L/100 |
| 42/5 to 14 | 21/50 - 3L/100 | 21/50 - 3L/100 |
| 14 onward | 0 | 0 |

Shared endpoints have the same value from either formula; optimal policies
can tie there. Subtracting gives the exact gross premium:

```
Delta(L) =
  23*(1+L)/300             0 <= L <= 6/5
  29/300 + 3L/50          6/5 <= L <= 7/5
  13/50 - 17L/300         7/5 <= L <= 3/2
  29/100 - 23L/300        3/2 <= L <= 5/2
  7/50 - L/60            5/2 <= L <= 42/5
  0                      L >= 42/5.
```

Its maximum is **271/1500**, attained at **L=7/5**. Thus controller costs at
least 271/1500 cannot be repaid at any L in this particular B=2 example.
For K=1/10 the exact condition for positive net controller value is

```
Delta(L)-K > 0  iff  7/23 < L < 57/23
                         (~0.30435 < L < ~2.47826).
```

The following three thresholds must remain separate:

- Above 57/23, conditional acquisition no longer repays K=1/10.
- At 42/5=8.4, its extra gross benefit vanishes, while both policies still
  obtain positive gross reward (21/125 at the boundary).
- At 14, both policy classes reach zero optimal gross reward. The maximum
  posterior confidence is 14/15, equivalently posterior odds 14. An exact
  scan of all 19 affordable subset/outcome histories gives that bound for
  each of A and B. At L>14 both strictly prefer abstaining at every history.

For reference:

| L | Adaptive reward A | Nonadaptive reward A | Gross premium | Net with K=0.1 |
|---:|---:|---:|---:|---:|
| 0 | 0.846667 | 0.770000 | 0.076667 | -0.023333 |
| 1 | 0.693333 | 0.540000 | 0.153333 | 0.053333 |
| 1.4 | 0.632000 | 0.451333 | 0.180667 | 0.080667 |
| 3 | 0.420000 | 0.330000 | 0.090000 | -0.010000 |
| 8.4 | 0.168000 | 0.168000 | 0 | -0.100000 |
| 14 | 0 | 0 | 0 | -0.100000 |

K is a constitutive differential cost, so it remains payable when abstaining.
No reproductive-fitness or invasion-dynamics mapping has been established.

## 4. Ecological interpretation and experimental boundary

The mechanistic prediction is not "danger always favors more information."
With limited, imperfect evidence, conditional cue acquisition can pay for
itself only over an intermediate error-loss range. Its maintenance can cease
to pay before its information benefit vanishes, and the information benefit
can vanish before all reward-bearing actions cease. The exact ordering above
is demonstrated for the declared benchmark, not claimed for every ecology.

Existing honey-bee experiments independently manipulated evidence quality and
reward likelihood [1]. They support treating those variables separately, but
do not measure this task's bit-flip rate, branching architecture, controller
cost, or threshold. Their accept/reject flower actions must not automatically
be equated with our separate third-action abstention option.

A prospective test would independently calibrate cue confusion, retain trial
histories and abstentions, and compare conditional next-cue access with a
budget-matched precommitted subset. Latent target truth must not replace the
actor's perceived cue history. Without those measurements, reduced visitation
alone cannot distinguish avoidance, costly information acquisition, missed
observations or lower opportunity. No natural network rewiring is identified.

## 5. Verification and provenance

Baseline: PR #68 at `47b6ff767bbd7cf6dfa99104d0f46402e95673cf`.
Full baseline CI run `38147950246` is successful on Python 3.10/3.11/3.12.

The attached previous-turn ZIP supplies a local harness. Baseline core.py and
deadline_reward.py were byte-verified against Git blob IDs
`93e91ef08097e91cb9003823601bc5d706452ba7` and
`3f72efe4d53190cbbd245e991208945127c220e7`. A complete clone was not available
in the container; this is not a local full-repository-suite claim.

- New tests: 145 passed, including 1,158 Fraction-oracle reward comparisons.
- Local harness: 233 passed (the new 145 and previous 88 reward tests).
- Continuous-L envelope certificate: all 599 distinct reward lines checked.
- Model boundaries: zero noise, uninformative noise, zero budget, unequal costs,
  invalid inputs, and floating-point support underflow explicitly checked.
- Extreme underflow raises an arithmetic error rather than fabricating certainty.
- New-head full repository CI is separate from these local results.

No existing file or frozen manuscript is modified. Code, tests and this note
are a narrow robustness audit, not a new general-purpose inference system.

## Source

[1] MaBouDi, H., Marshall, J. A. R., Dearden, N. & Barron, A. B. 2023.
How honey bees make fast and accurate decisions. eLife 12:e86176.
https://doi.org/10.7554/eLife.86176
