# Finite-population origin-fixation selection on routing genotypes

Status: stacked side theory on `theory/routing-origin-fixation-selection`. This is not part of the frozen Theoretical Ecology submission.

## 1. Why add this layer

The preceding routing side line now distinguishes:

```text
static sensing capability,
local mutational distance,
neutral mutation-attempt waiting to first gain,
neutral mutation-attempt waiting to full required gain.
```

Those results deliberately stop before selection and fixation. This note adds one explicit finite-population process rather than silently interpreting mutation attempts as evolutionary substitutions.

The question is:

> Once routing genotypes differ in realized sensing gain, how do finite-population selection and the large multiplicity of lower-gain routing genotypes compete at origin-fixation equilibrium?

The broad mutation-selection/free-fitness answer is established prior art. The repository-specific object is the exact routing genotype multiplicity induced by the required-gap coordinate `q`.

## 2. Declared genotype and population process

For required structural gap

```text
q>=1,
```

use the query-minimal star family with

```text
k=q+1
```

routing branches.

Represent a routing genotype by branch-local pruning progress

```text
x=(x_1,...,x_k) in {0,...,q}^k.
```

Its realized routing gain is

```text
g(x)=min_i x_i.
```

This is the same gain geometry used by the local-routing mutation results: gain `r` is realized exactly when every branch has accumulated at least `r` relevant pruning edits.

### Population assumption

Assume a monomorphic haploid population of fixed size

```text
N>=2
```

in the strong-selection/weak-mutation origin-fixation regime. One mutant lineage arises, fixes or is lost, and only then is the next mutation proposed.

A routing mutation proposal chooses one of the `k` branch coordinates and one direction `+1/-1` uniformly. Valid one-coordinate proposals have equal forward and reverse proposal probability. A direction that would leave `[0,q]` is a null proposal.

Assign fitness

```text
W(x)=a^g(x),
a>=1,
```

where `a` is the multiplicative fitness factor per unit of realized routing gain. Writing

```text
a=e^s
```

defines the per-gain log-fitness increment `s>=0`.

This is a declared side model. No empirical claim is made that a real organism has this genotype encoding or this value of `a`.

## 3. Moran fixation step

For a mutant with relative fitness

```text
R=W(y)/W(x),
```

in a well-mixed Moran population of size `N`, the fixation probability of a single mutant is

```text
rho(R)=(1-R^-1)/(1-R^-N)
```

for `R!=1`, with neutral limit

```text
rho(1)=1/N.
```

Algebraically,

```text
rho(R)
= (R-1)R^(N-1)/(R^N-1),

rho(1/R)
= (R-1)/(R^N-1).
```

Therefore

```text
boxed: rho(R)/rho(1/R)=R^(N-1).
```

This is classical Moran/origin-fixation algebra and is not a novelty claim.

## Theorem OF1 — exact reversible stationary law

Because the local mutation proposal is symmetric on every valid neighboring pair,

```text
Q(x,y)=Q(y,x).
```

Let

```text
theta=a^(N-1)=e^[(N-1)s].
```

Then the origin-fixation chain satisfies detailed balance with

```text
boxed: pi(x) proportional to theta^g(x).
```

### Proof

For neighboring genotypes `x,y`,

```text
P(x,y)=Q(x,y) rho(W(y)/W(x)).
```

Hence

```text
P(x,y)/P(y,x)
= [W(y)/W(x)]^(N-1)
= theta^[g(y)-g(x)].
```

Thus choosing

```text
pi(x) proportional to theta^g(x)
```

gives

```text
pi(x)P(x,y)=pi(y)P(y,x)
```

on every edge. Self-loops are automatic. Therefore the normalized law is stationary and the finite connected chain is reversible. QED.

The statistical-mechanical form is expected from classical origin-fixation/free-fitness theory; the new bookkeeping below is only the exact routing-layer degeneracy.

## 4. Exact gain-layer multiplicity

For gain `r`, every coordinate must lie in

```text
{r,...,q},
```

and at least one coordinate must equal `r`. Therefore

```text
boxed:
D_r=(q-r+1)^k-(q-r)^k,
```

for `r=0,...,q`.

At the full required gain,

```text
D_q=1.
```

The stationary unnormalized mass of gain layer `r` is therefore

```text
M_r(theta)=D_r theta^r.
```

The exact partition function is

```text
Z_q(theta)=sum_{r=0}^q D_r theta^r,
```

and

```text
P_pi(g=r)=D_r theta^r/Z_q(theta).
```

In particular, the unique full-phase genotype has stationary mass

```text
pi_full(theta)=theta^q/Z_q(theta).
```

## 5. Entropic barrier below the full phase

Measure layers by their distance `s` below full gain:

```text
r=q-s.
```

Their degeneracy is

```text
A_s=(s+1)^k-s^k.
```

### Lemma OF2 — sharp chain bound

For every integer `s>=1`,

```text
boxed: A_s <= (2^k-1)^s,
```

with equality at `s=1`.

### Combinatorial proof

`A_s` counts `k`-tuples

```text
z in {0,...,s}^k
```

whose maximum coordinate is exactly `s`.

Map such a tuple to the nested nonempty subset sequence

```text
B_t={i : z_i >= s-t+1},
t=1,...,s.
```

Because some coordinate equals `s`, every `B_t` is nonempty, and

```text
B_1 subseteq B_2 subseteq ... subseteq B_s.
```

There are exactly `2^k-1` nonempty subsets of the `k` branch labels. If the nesting constraint is discarded, there are `(2^k-1)^s` possible nonempty-subset sequences. Hence `A_s` cannot exceed that number.

For `s=1`, every nonempty subset occurs and

```text
A_1=2^k-1.
```

QED.

This lemma is elementary combinatorics, not an independent priority claim.

## Theorem OF3 — sharp modal full-phase threshold

The unique full-gain layer has weight

```text
theta^q.
```

A layer `s` steps below full has weight

```text
A_s theta^(q-s).
```

The full layer weakly dominates that layer exactly when

```text
theta^s >= A_s.
```

By OF2,

```text
A_s^(1/s) <= 2^k-1,
```

and the bound is attained at `s=1`. Therefore

```text
boxed:
full phase is a stationary modal gain layer
iff
theta >= 2^k-1.
```

For the required-gap star `k=q+1`,

```text
boxed:
theta_mode(q)=2^(q+1)-1.
```

Since

```text
theta=e^[(N-1)s],
```

the equivalent log-fitness threshold is

```text
boxed:
(N-1)s >= log(2^(q+1)-1).
```

This is the cleanest population-level separation yet in the side line: larger required structural gap creates a larger near-target genotype multiplicity, so a stronger effective selection tilt is required before the unique full-phase genotype class becomes the most probable gain layer at stationarity.

Do not call this a universal biological selection law. It belongs to the declared routing genotype representation.

## 6. Full-phase half-mass window

Modal layer and majority stationary mass are different criteria.

Divide every lower layer by the full-layer weight. Then

```text
(1-pi_full)/pi_full
= sum_{s=1}^q A_s theta^-s.
```

Let

```text
A=2^k-1.
```

### Necessary condition

The nearest lower layer alone contributes

```text
A/theta.
```

Therefore

```text
pi_full>=1/2
=>
theta>=A.
```

### Simple sufficient condition

By OF2,

```text
sum_{s=1}^q A_s theta^-s
<= sum_{s=1}^q (A/theta)^s.
```

If

```text
theta>=2A,
```

then `A/theta<=1/2`, and the finite geometric sum is at most one. Hence

```text
boxed:
theta>=2(2^k-1)
=>
pi_full>=1/2.
```

Thus the exact half-mass threshold lies in a multiplicative factor-two window:

```text
2^k-1 <= theta_1/2 <= 2(2^k-1).
```

The window width in log tilt is at most `log 2`, independent of `q`.

## 7. Canonical q=2 example

For

```text
q=2,
k=3,
```

the gain-layer degeneracies are

```text
(D_0,D_1,D_2)=(19,7,1).
```

Therefore

```text
Z(theta)=19+7 theta+theta^2.
```

### Modal threshold

The full gain layer becomes modal at

```text
boxed: theta=7.
```

At exactly `theta=7`, gain layers 1 and 2 tie:

```text
weights=(19,49,49).
```

### Majority threshold

The full-phase stationary mass reaches one half when

```text
theta^2=19+7 theta.
```

Thus

```text
boxed:
theta_1/2=(7+5 sqrt(5))/2 ≈ 9.09017.
```

For exact rational audits:

```text
theta=9  -> pi_full=81/163 < 1/2,
theta=10 -> pi_full=100/189 > 1/2.
```

### Finite population example

If `a=2`, then

```text
theta=2^(N-1).
```

For `N=3`, `theta=4<7`, so the full phase is not modal.
For `N=4`, `theta=8>7`, so it is modal, with layer weights

```text
(19,56,64)
```

and full-phase mass

```text
64/139.
```

Again, `a=2` is an audit fixture, not a biological estimate.

## 8. Required-gap scaling

Because `k=q+1`,

```text
theta_mode(q)=2^(q+1)-1.
```

Therefore

```text
beta_mode(q)
= log theta_mode(q)
= log(2^(q+1)-1)
~ (q+1) log 2.
```

where

```text
beta=(N-1)s.
```

So under this side model, the effective finite-population selection tilt required to make the full target the stationary modal gain layer grows asymptotically linearly with the structural gap demanded by the eco-evolutionary phase.

The reason is entropic: the nearest lower layer contains

```text
2^(q+1)-1
```

distinct routing genotypes while the full layer contains only one.

## 9. Prior-art boundary

The following are established and are not claimed as new:

- well-mixed Moran fixation probability;
- SSWM/origin-fixation chains;
- fixation-ratio reversibility;
- Boltzmann/Gibbs stationary genotype laws;
- free fitness and fitness-entropy competition;
- genotype-phenotype degeneracy affecting stationary evolutionary outcomes;
- neutral networks and mutational robustness.

The exact candidate contribution is narrower:

```text
required eco-evolutionary phase
-> exact required gap q
-> exact Pareto routing genotype family
-> exact gain-layer multiplicities
-> finite-population origin-fixation threshold for stationary phase occupancy.
```

This remains a candidate composition, not a priority claim.

## 10. Relation to previous side layers

The stacked hierarchy is now:

```text
PR #15: structural capability -> shortest local edit distance
PR #17: neutral stochastic waiting -> first positive gain
PR #18: neutral stochastic waiting -> full required gain
this layer: finite-population origin-fixation selection -> stationary occupancy of gain layers
```

These answer different questions. In particular:

```text
first appearance,
first full realization,
fixation/substitution,
stationary occupancy
```

must not be conflated.

## 11. Executable audit

Implementation:

```text
adaptive_gain/routing_origin_fixation.py
```

Tests:

```text
tests/test_routing_origin_fixation.py
```

The tests use exact rational arithmetic to verify Moran fixation ratios, stochastic transition rows, edgewise detailed balance, `pi P=pi`, an independent linear stationary solve at `q=1`, gain-layer counts by enumeration, the sharp modal threshold, the half-mass bounds, and the canonical `q=2` values.
