# Neutral-plateau mutation dynamics before the first routing gain

Status: stacked side theory on `theory/routing-neutral-plateau-dynamics`, based on the green PR #15 checkpoint `c0c2bf544bd8c8cf53058116931afee2d654441d`. This is **not** part of the frozen Theoretical Ecology submission.

## 1. Why add a stochastic process now

`LOCAL_ROUTING_MUTATION_ACCESSIBILITY.md` separates two deterministic objects inside the same fixed sensing task:

```text
task-level structural opportunity
!=
local routing-mutation distance needed to realize it.
```

For the `k`-branch extremal routing task, the full zero-saving branch program is exactly `k` elementary pruning edits from the first positive worst-path gain. But graph distance is not a waiting time.

This note adds the smallest explicit stochastic process needed to answer:

> If neutral routing edits are allowed and mutation attempts hit branches at random, how long does it take before the first positive realized routing gain appears?

No fixation, population size, ecological generation time, or empirical mutation rate is introduced. Time below means **mutation attempts under the declared proposal process**.

---

## 2. Declared mutation-attempt process

Start from the full routing program

```text
ell=(k,...,k),  k>=2.
```

At each discrete mutation attempt:

1. choose one of the `k` branch programs uniformly;
2. if that branch still contains a target-irrelevant acquisition occurrence, prune one;
3. if all redundant occurrences in that branch have already been removed, the attempt is null;
4. neutral changes persist;
5. stop when realized worst-path gain becomes positive.

The first positive gain occurs exactly when every branch has been pruned at least once. Deeper pruning within an already touched branch does not help the worst path until the last untouched branch receives its first pruning.

---

## Proposition NPD1 — exact Markov lumping before first gain

Let

```text
m = number of branches that have been pruned at least once.
```

For any microscopic routing state with the same `m<k`, the next mutation attempt has

```text
P(m -> m+1) = (k-m)/k,
P(m -> m)   = m/k.
```

State `m=k` is absorbing for the first-gain stopping problem.

### Proof

Exactly `k-m` branch labels have never been selected. A uniform branch proposal hits one of them with probability `(k-m)/k`, in which case `m` increases by one. Every other proposal hits a previously touched branch; regardless of whether that branch can still be pruned or the attempt is null, the number of distinct touched branches remains `m`. Therefore all microscopic states sharing `m` have the same transition probabilities between lumped classes. QED.

This is strong lumpability for this stopping problem. It is also the classical coupon-collector occupancy chain.

---

## Proposition NPD2 — exact first-gain distribution

Let

```text
T_first = mutation attempt on which every branch has been touched at least once.
```

Then for integer `t>=0`,

\[
\boxed{
P(T_{first}\le t)
=
\sum_{j=0}^{k}
(-1)^j {k\choose j}
\left(\frac{k-j}{k}\right)^t
}
\]

by inclusion-exclusion.

The PMF is the consecutive CDF difference

\[
P(T_{first}=t)
=P(T_{first}\le t)-P(T_{first}\le t-1).
\]

The support begins at `t=k`. At the earliest possible completion time,

\[
\boxed{P(T_{first}=k)=\frac{k!}{k^k}.}
\]

These are standard coupon-collector formulas, not new probability theory.

---

## Proposition NPD3 — exact expected mutation attempts

From lumped state `m`, the probability of acquiring a new branch label is `(k-m)/k`, so the waiting time to advance by one occupancy level is geometric with mean

\[
\frac{k}{k-m}.
\]

Summing the `k` stages gives

\[
\boxed{
E[T_{first}]
= k\sum_{j=1}^{k}\frac1j
= kH_k.
}
\]

Thus the deterministic shortest elementary-edit distance and stochastic mean waiting time are distinct:

```text
shortest routing-pruning distance to first gain = k,
expected uniform mutation attempts to first gain = k H_k.
```

Their ratio is exactly

\[
\boxed{H_k.}
\]

The excess is caused by repeated proposals to branches already represented on the neutral plateau, not by a fitness valley.

---

## 3. Required-gap star specialization

PR #15 links a required eco-evolutionary structural gap `q>=1` to the query-minimal depth-two star family by taking

```text
k=q+1.
```

The static sensing coordinates are

```text
(worlds, queries, frontier edges, depth)
=(2q+2, q+2, q+2, 2).
```

The present stochastic result concerns **only the first positive realized routing gain**, not attainment of the full target gap `q`.

For that first improvement:

\[
\boxed{
E[T_{first}\mid q]
=(q+1)H_{q+1}.
}

The shortest possible number of elementary pruning attempts is `q+1`, so the stochastic overhead factor is

\[
H_{q+1}.
\]

This adds a third coordinate to the side-model hierarchy:

```text
static structural capability,
minimum routing edit distance,
stochastic waiting under a declared mutation proposal.
```

They answer different questions.

---

## 4. Canonical q=2 example

For the manuscript-linked side example,

```text
q=2,
k=3,
static Pareto point=(6,4,4,2).
```

PR #15 gives shortest elementary pruning distance `3` to the first positive realized gain.

Under uniform branch mutation attempts,

\[
E[T_{first}]
=3\left(1+\frac12+\frac13\right)
=\boxed{\frac{11}{2}}
=5.5
\]

attempts.

The mean/shortest ratio is

\[
\boxed{\frac{11}{6}}.
\]

Again, these are mutation attempts in the declared abstract process, not generations or substitutions in a biological population.

---

## 5. Why this is the mesoscopic connection — and where it stops

The full routing microstate records branch-specific pruning counts. For first-gain timing, these microscopic states collapse exactly to the `k+1` occupancy classes

```text
m=0,1,...,k.
```

So the side theory now has an explicit micro-to-mesoscopic reduction:

```text
branch-specific routing genotype state
-> occupancy count m
-> finite Markov chain
-> exact first-gain hitting law.
```

This is a genuine mathematical connection to the earlier mesoscopic-model motivation, but not a new mesoscopic formalism. The reduced chain is classical.

Do **not** replace it by a diffusion or Fokker-Planck equation unless a scaling limit is actually derived. At the present stage the finite Markov chain is exact and preferable.

---

## 6. Relation to small jump and Hegselmann-Krause

### Small-jump layer

PR #15 supplies the local mutation geometry. A one-branch elementary edit cannot improve the full program immediately; neutral accumulation is required. The present note converts that exact geometry into a waiting law under a declared random proposal process.

### HK / bounded-interaction layer

No bounded-confidence or interaction-neighbourhood assumption is used here. If routing phenotypes later interact only within an architecture-distance radius, that would be a separate population-interaction model layered on top of this mutation process.

Keeping these pieces separate avoids confusing mutation locality with interaction locality.

---

## 7. Prior-art boundary

Coupon collection, occupancy chains, Markov lumping, harmonic collection times, inclusion-exclusion distributions, neutral networks, and plateau crossing are established prior art.

Therefore do not claim novelty for:

- `k H_k`;
- the occupancy-number Markov chain;
- coupon-collector hitting distributions;
- strong lumpability as a general concept;
- neutral waiting caused by repeated mutation proposals.

The only research-program value here is the **composition** with the exact finite sensing landscape already derived in adaptive-gain:

```text
required feedback phase
-> required gap q
-> exact Pareto sensing task
-> local routing plateau
-> exact finite mutation-attempt Markov chain.
```

That composition remains side theory, not a priority claim.

---

## 8. Next nontrivial step

The first-gain process is deliberately selection-free because every state before first gain has the same declared worst-path routing reward.

A more substantive population extension would specify, before analysis:

1. a mutation proposal kernel on the full routing state graph;
2. population size or deterministic frequency dynamics;
3. a fitness lift from realized routing gain;
4. whether neutral mutations fix/drift according to an explicit process;
5. the target quantity: first passage, stationary occupancy, or phase-entry probability.

Only then should mutation-selection or mesoscopic population dynamics be studied. Generic mutation-selection chains and Gibbs laws are prior art, so any future novelty must still arise from the exact ecological sensing composition.

---

## 9. Executable verification

Implementation:

- `adaptive_gain/routing_neutral_plateau.py`

Tests:

- `tests/test_routing_neutral_plateau.py`

The tests verify:

- strong lumping across all microscopic pruning states through `k=4`;
- inclusion-exclusion CDF against independent exact Markov DP;
- PMF support and CDF increments;
- the harmonic expectation through the first-step recurrence;
- earliest completion probability `k!/k^k`;
- the canonical `q=2,k=3` value `11/2`;
- the required-gap family overhead factor `H_{q+1}`.
