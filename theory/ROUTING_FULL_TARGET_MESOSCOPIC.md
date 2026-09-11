# Full-target mesoscopic routing accessibility

Status: stacked side theory on `theory/routing-full-target-mesoscopic`. This is not part of the frozen Theoretical Ecology submission.

## 1. Question

The local-routing side line already separates three objects:

```text
static task capability,
shortest local routing-edit distance,
stochastic waiting to the first positive realized gain.
```

The next question is stronger:

> Under the same uniform branch-mutation attempt process, how long does it take to realize the **full required routing gain** `r`, rather than merely the first positive gain?

For the required-gap star family, the biologically downstream specialization is `k=q+1` branches and target realized gain `r=q`.

No mutation-selection, fixation, demographic, or generation-time model is introduced here. One time unit is one declared mutation attempt.

## 2. Microscopic process

Use the same `k`-branch routing program as PR #15. Let

```text
x_i(t)
```

be the number of target-irrelevant acquisitions already pruned from branch `i` by attempt `t`.

To reach realized gain `r`, every branch must have received at least `r` pruning hits. Therefore only capped progress matters for this stopping problem:

```text
y_i(t)=min{x_i(t),r}.
```

A mutation attempt chooses one branch uniformly from `1,...,k`.

- if `y_i<r`, that branch advances by one capped level;
- if `y_i=r`, the capped state does not change.

The last case does **not** mean that the underlying biological/program mutation must literally be null. If `r<k-1`, further pruning of that branch may still be possible. It is a self-loop only in the quotient relevant to the hitting event `g>=r`, because extra pruning of an already target-saturated branch does not bring another branch closer to `r`.

Thus the capped microstate space contains

```text
(r+1)^k
```

states.

## 3. Exact mesoscopic lump

Let

```text
n_j = number of branches with capped progress j,
```

for `j=0,...,r`. Then

```text
n_0+...+n_r=k.
```

All branch labels are exchangeable under the uniform proposal kernel. From a histogram `n`, choosing one of the `n_j` branches at level `j<r` moves one count from bin `j` to `j+1`; choosing one of the `n_r` saturated branches leaves the histogram unchanged.

Therefore the microscopic chain strongly lumps exactly to the histogram chain

```text
P(n -> n-e_j+e_{j+1}) = n_j/k,   j<r,
P(n -> n)               = n_r/k.
```

The number of mesoscopic states is the stars-and-bars count

```text
C(k+r,r).
```

So the exact state reduction is

```text
(r+1)^k labelled capped microstates
-> C(k+r,r) occupancy mesostates.
```

This is an exact finite Markov reduction, not a diffusion or Fokker-Planck approximation.

## 4. Exact expected hitting-time recurrence

Let `E(n)` be the expected remaining mutation attempts until all branches are in bin `r`.

The absorbing state has

```text
E(0,...,0,k)=0.
```

For any other histogram, first-step analysis gives

```text
E(n)
= 1
+ (n_r/k) E(n)
+ sum_{j<r} (n_j/k) E(n-e_j+e_{j+1}).
```

Solving the self-loop,

```text
E(n)
= k/(k-n_r)
+ sum_{j<r} n_j/(k-n_r) E(n-e_j+e_{j+1}).
```

Every non-self transition increases total capped progress by one, so this recurrence is acyclic after the self-loop is removed and can be solved exactly with rational arithmetic.

The initial full routing program corresponds to

```text
n=(k,0,...,0).
```

Call the resulting expectation

```text
E_{k,r}.
```

For `r=1`, the chain reduces exactly to the first-gain coupon collector and

```text
E_{k,1}=k H_k.
```

For `r>1`, this is the classical multiple-copy coupon collector / double-Dixie-cup family. No probability-theory novelty is claimed.

## 5. Earliest possible completion

The deterministic shortest routing-edit distance from PR #15 is

```text
k r.
```

To finish in exactly `kr` mutation attempts, every branch must be selected exactly `r` times. Hence

```text
P(T_{k,r}=kr)
= (kr)! / [(r!)^k k^(kr)].
```

This separates three quantities:

```text
shortest local edit distance = kr,
expected stochastic attempts = E_{k,r},
earliest-path probability    = (kr)! / [(r!)^k k^(kr)].
```

The expectation can never be below the shortest path.

## 6. Canonical q=2 phase-entry example

For the manuscript's first stable-oscillation structural requirement,

```text
q=2.
```

Use the exact query-minimal star specialization from PR #15:

```text
k=q+1=3,
(worlds,queries,frontier_edges,depth)=(6,4,4,2).
```

Full realized gap `q=2` requires every branch to receive two pruning hits.

The accessibility layers are then:

```text
shortest elementary prunings = 6,
capped microstates            = 3^3 = 27,
occupancy mesostates          = C(5,2) = 10,
expected mutation attempts    = 347/36 ≈ 9.6388889,
stochastic overhead           = 347/216 ≈ 1.60648,
earliest completion prob.     = 10/81.
```

This is stronger than the first-gain result `E[T_first]=11/2`: the first selectable advantage appears before the routing architecture has accumulated the full structural gain required by the downstream phase.

## 7. Required-gap composition

For the query-minimal depth-two star family,

```text
k=q+1,
r=q.
```

Therefore the exact side-model chain is

```text
required local feedback phase
-> required structural gap q
-> exact static Pareto task
   (2q+2,q+2,q+2,2)
-> shortest routing distance q(q+1)
-> exact occupancy chain with
   (q+1)^(q+1) capped microstates
   and C(2q+1,q) mesostates
-> exact rational expected phase-entry attempts E_{q+1,q}.
```

For the first small values:

```text
q=1: E=3,
q=2: E=347/36,
q=3: E=38948987/1990656.
```

These values are model-specific waiting times in mutation attempts, not empirical generations.

## 8. Relation to the earlier four ideas

This extension makes the old conceptual connections more concrete:

- **small-jump:** static capability does not imply short local accessibility;
- **mesoscopic model:** exchangeable routing microstates admit an exact population-state compression before any continuum limit;
- **HK/bounded interaction:** remains a separate interaction-neighbourhood mechanism and is not used here;
- **informed-consent/declaration discipline:** the genotype-policy representation and mutation proposal kernel are declared before reading the waiting-time result.

The bridge is therefore structural rather than terminological.

## 9. Prior-art boundary

Do not claim novelty for:

- coupon collection;
- multiple coupon collection / double Dixie cup;
- occupancy chains;
- strong lumpability;
- first-step hitting-time equations;
- stars-and-bars state counts;
- neutral plateau crossing;
- exact rational dynamic programming.

The candidate research contribution remains the composition, if it survives broader prior-art review and receives a biological genotype-policy justification:

```text
required eco-evolutionary phase
-> exact finite sensing requirement
-> explicit heritable routing mutation geometry
-> exact finite stochastic accessibility to that phase.
```

No claim of priority is made here.

## 10. Executable audit

Implementation:

```text
adaptive_gain/routing_full_target_mesoscopic.py
```

Tests:

```text
tests/test_routing_full_target_mesoscopic.py
```

The tests independently verify strong lumping from labelled capped microstates, compare the histogram expectation to a separate microstate dynamic program, recover the `r=1` first-gain result, check the canonical `q=2` value `347/36`, and enforce an explicit mesostate resource limit.
