# Deadline, error cost, and abstention: reward audit v1

Status: exact finite-model extension to PR #68. This is neither a biological
observation nor a new general theorem about Bayesian rejection. The frozen
submission files and the MAIN 1–3 novelty spine are not changed.

## 1. Question and fixed scope

The previous five-world example ranked architectures differently under certain
identification and guess-permitting accuracy. Can a *single* declared payoff
model connect those endpoints and expose which biological assumption matters?

Hold targets `(0,1,1,0,0)` and the existing three binary unit-cost query vectors
fixed:

```
                 w0 w1 w2 w3 w4
A root            0  0  1  1  0
A left            0  1  0  0  0
A right           0  0  0  1  0

B first           1  0  0  0  0
B second          0  0  0  1  0
B third           1  1  1  1  0
```

Let `p=(t,q,q,q,q)`, `q=(1-t)/4`, with `1/5<t<1`. Thus `t>q>0`.
The finite guaranteed complexities remain A: `(C_A,C_F)=(2,3)` and B: `(3,3)`.
The architectures have the same world/target marginals and query count/arity;
**individual cue marginals and informativeness are NOT all matched**. In
particular, their one-cue contrast must not be called a pure adaptivity effect.

A correct target choice pays `v>0`, a wrong choice pays `-L` with `L>=0`, and
abstaining pays zero. Set `r=L/v`. This symmetric classification payoff is an
idealization, not a calibrated flower-visit or fitness model. Both terminal
target labels are actions; abstention is a third, separate action. A target
label meaning "reject a flower" must not be confused with abstaining from
classification. Query acquisition uses the hard budget; no further per-query
payoff debit is assumed. Policies may reoptimize when the deadline or payoffs
change.

The nonadaptive comparator chooses any budget-feasible query subset *before*
observing outcomes. It can classify using partial information or abstain. It is
not forced to purchase the universal guaranteed-resolving three-query bundle.

## 2. Terminal payoff and the necessary outside option

For a cue-history group with unconditional masses `m0,m1`, the optimal terminal
reward is

```
max(0, v*m0-L*m1, v*m1-L*m0).
```

Equivalently, act on the most probable target only when its posterior
probability is at least `L/(v+L)`; equality allows a tie with abstention.
This is a standard Bayesian rejection decision, not a novelty claim [1].

**Negative control: forced choice.** If abstention is prohibited, every world
ends in a choice and any policy with correct-choice probability `C` has

```
W = v*C - L*(1-C) = (v+L)*C - L.
```

Since `v+L>0`, changing `L` cannot change the ranking induced by accuracy,
including after optimizing policies. An error-cost-induced ranking reversal
therefore cannot arise here merely by relabeling accuracy as fitness. It needs
the outside option (or a different, explicitly declared payoff structure).

## 3. Exact one-cue reward functions

Write `[z]_+=max(z,0)`. Over the stated prior family,

```
V_A(1)/v = q + [t + (2-r)*q]_+
V_B(1)/v = t + 2*q*[1-r]_+.
```

These values apply to both adaptive and nonadaptive access: with at most one
acquisition there is no next-query choice to make conditional.

### Direct finite proof

A's left query isolates a target-1 world of mass `q`; the remaining branch has
target masses `t+2q` and `q`. Its value is the displayed A formula. A's right
query gives `q+[t+(1-2r)q]_+`, which cannot exceed the left query for `r>=0`.
The root gives `[t+(1-r)q]_+ + q*[1-r]_+`: the left query dominates it for
`r<=1` by `(1+r)q`, and for `r>=1` by monotonicity of the positive part.
Stopping without querying gives `[t+(2-2r)q]_+`, also no greater than the left
query. These exhaust the one-query policies.

B's first query isolates the common target-0 world of mass `t`. Its remaining
branch is balanced, with mass `2q` per target, giving the displayed B formula.
Each other query gives `q+[t+(1-2r)q]_+`. For `r<=1`, this ties the first query
or is smaller; for `r>=1`, it is at most `t` because `t>=q`. The no-query
option cannot improve on it. These exhaust B's policies.

### Ranking boundary

Subtract the two formulas. Their normalized difference is

```
(V_A(1)-V_B(1))/v =
    (1+r)*q                  for 0 <= r <= 1,
    (3-r)*q                  for 1 <= r <= 2+t/q,
    q-t                      for r >= 2+t/q.
```

Because `t>q`, the last breakpoint exceeds 3. Consequently, for **every**
`1/5<t<1`,

```
L < 3v:  A has larger expected reward;
L = 3v:  the two are tied;
L > 3v:  B has larger expected reward.
```

The factor 3 is exact for this task/prior family, not a universal biological
constant. At `t=1/5`, high-cost rewards tie rather than strictly favoring B.
At `t=1`, the strictly-positive-support assumption fails.

For `t=1/3`, `q=1/6`, and `v=1`:

| Error cost L | A, budget 1 | B, budget 1 | Reward winner |
|---:|---:|---:|---|
| 0 | 5/6 | 2/3 | A |
| 1 | 2/3 | 1/3 | A |
| 2 | 1/2 | 1/3 | A |
| 3 | 1/3 | 1/3 | tie |
| 4 | 1/6 | 1/3 | B |

This is a reversal of *optimal expected reward under one payoff family*, not
just a comparison of two unrelated summary metrics. Optimal action rates may
be nonunique at ties; the value function does not identify a unique policy or
observed acceptance/abstention frequency.

## 4. Genuine conditional-query value at budget two

At two acquisitions A can identify every target, giving `V_A,adaptive(2)=v`.
For a precommitted two-query subset, choosing root+left certifies mass `t+2q`
and leaves a balanced `q:q` branch; its value is

```
v * (t+2q + q*[1-r]_+).
```

The other two-query subsets certify mass `2q` and leave target masses `t+q`
and `q`, giving `v*(2q+[t+(1-r)q]_+)`. The first is at least as good for
`r>=1`, and the alternatives tie it for `r<=1`. Fewer acquisitions do not
improve it. Thus the **fair adaptive-minus-nonadaptive reward premium** is

```
Delta_A(2) = v*q*min(1+r,2) = q*min(v+L,2v).
```

For B, the best two-query plan isolates the common zero and one other zero,
leaving target masses `q` and `2q`. Both policy classes attain

```
V_B(2)/v = t+q + q*[2-r]_+,
Delta_B(2) = 0.
```

Why no hidden adaptive improvement? Every B query only isolates one of the
three target-0 states; once such a singleton is found, no further information
is needed. The only still-mixed branch therefore follows one precommitted
sequence. Adaptivity can stop early but cannot add a branching advantage to
the terminal reward at a common hard budget. The best pair isolates masses
`t` and `q`; isolating the two rare zeros cannot do better when `t>=q`.

At budgets 1 and 3 both architectures have zero *gross* adaptive-over-fixed
premium. At budget 2, A's premium increases from `vq` at zero loss to `2vq`
once `L>=v`, then saturates. No prediction of an unbounded benefit under
increasing danger is licensed.

## 5. Additive controller cost: an explicit selection-proxy boundary

If conditional control carries an additional constitutive cost `K>=0`, in the
**same expected-payoff units**, A's two-query net difference is

```
Phi_A(2) = q*min(v+L,2v) - K.
```

For `K>=2vq`, no error cost can make this quantity positive. For
`vq<=K<2vq`, positive net advantage requires `L>K/q-v`. For `K<vq`, it is
already positive at `L=0`. Equality means zero net advantage, not selection.

At `t=1/3`, `v=1`, `K=1/4`, net differences are `-1/12` for `L=0`, zero for
`L=1/2`, and `+1/12` for `L>=1`. Thus rising error cost can repay conditional
control without changing the species-state composition or cues. Calling this
natural selection additionally requires a justified mapping to reproductive
fitness and heritable competing architectures; neither is supplied here.

## 6. Ecological interpretation and falsification

The additional biological quantity is **the cost of a wrong interaction
relative to leaving without acting**. A potentially useful controlled contrast
holds the cues, target frequencies, and deadline fixed, but crosses error
penalty with availability of a no-action option. Forced-choice trials are an
explicit negative control for the symmetric-payoff mechanism.

At budget 1, test the reward-ranking reversal, not adaptive cue sequencing.
At budget 2, test the additional value of outcome-dependent *next* cue choice
against the fair partial-subset comparator. Record correct/wrong/abstain
outcomes, the full cue history, acquisition times, and the payoff schedule.
The model assumes known priors and calibrated deterministic cues; changes in
cue perception, learning, reward expectation, or outside-option value can
invalidate a clean payoff-only interpretation.

Honey-bee acceptance/rejection decisions under differing evidence and reward
likelihood have already been studied [2]. That precedent supports these as
relevant experimental variables, but it neither validates this five-state
architecture nor establishes the `L=3v` boundary. Its flower rejection action
also need not be the third-action abstention defined here.

Novelty ceiling: Bayesian rejection, reward-dependent decisions, and the
accuracy-risk tradeoff are established [1,2]. The contribution of this audit is
an explicit, falsifiable payoff bridge and a fair-controller-cost bound within
the already declared finite benchmark. It is support material, not MAIN 4.

## 7. Reproducibility and verification scope

- Baseline PR head: `96cfe2fab5f063f4d7fbf74ac8db9abcaf2b83d7`.
- Baseline GitHub Actions run `38109749159`: Python 3.10/3.11/3.12 successful,
  including repository tests and both example audits.
- New solver: `adaptive_gain/deadline_reward.py`.
- New tests: `tests/test_deadline_reward.py`.
- Receipt: `validation/deadline_reward_abstention_v1.json`.

The local harness uses a byte-verified copy of the baseline `core.py` (Git blob
`93e91ef08097e91cb9003823601bc5d706452ba7`). It contains the new tests, **not**
the full repository suite: whole-repository verification of the new head is a
separate CI result and must not be inferred from baseline success.

There are 1,920 exact-oracle comparisons across six rational prior settings,
ten error costs (including both sides of 3), four deadlines, two architectures,
two policy classes, and both abstention conditions; a separate multiclass,
unequal-cost task adds 48 comparisons. The oracle enumerates attainable
(correct, wrong, abstain) outcome vectors with Fraction arithmetic before
applying rewards, independently of the production reward dynamic program.
The continuum claim rests on the finite proof in section 3, not just this grid.

## References

[1] Chow, C. K. (1970). On optimum recognition error and reject tradeoff.
IEEE Transactions on Information Theory 16(1), 41–46.
https://doi.org/10.1109/TIT.1970.1054406

[2] MaBouDi, H., Marshall, J. A. R., Dearden, N., & Barron, A. B. (2023).
How honey bees make fast and accurate decisions. eLife 12:e86176.
https://doi.org/10.7554/eLife.86176
