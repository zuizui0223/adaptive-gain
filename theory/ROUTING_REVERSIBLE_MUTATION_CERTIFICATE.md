# Reversible-mutation representation certificate

Status: stacked side theory on `theory/routing-reversible-mutation-certificate`. This is not part of the frozen Theoretical Ecology submission.

## 1. Why another representation result is needed

PR #24 proves by direct contrast that the same required gap `q`, the same phenotype gain set and the same phenotype-level fitness schedule can produce different mutational accessibility and different stationary phase occupancy under different genotype encodings.

The next question is not whether representation matters. That is established prior art in genotype-phenotype map theory. The useful question is:

> What is the minimal representation information that must be declared before accessibility or stationary occupancy can be inferred?

For the finite origin-fixation extension, two logically separate objects are required:

```text
1. support graph of the neutral mutation proposal -> accessibility,
2. neutral mutation stationary mass by phenotype -> stationary occupancy.
```

Raw genotype counts are only a special case of item 2.

## 2. General finite representation

Let `X` be a finite connected genotype set. Each genotype has a routing gain

```text
g(x) in {0,...,q}.
```

Let `Q` be a neutral mutation-proposal Markov kernel. Assume `Q` is reversible with respect to a strictly positive probability measure `mu`:

```text
mu_x Q_xy = mu_y Q_yx.
```

The proposal support graph is the undirected graph whose edges are pairs with positive proposal probability.

Declare a start genotype `x0` for accessibility questions.

As in PR #20, use a monomorphic rare-mutation Moran origin-fixation process in a population of size `N>=2`, with phenotype-level fitness

```text
W(x)=a^g(x),  a>=1.
```

Define

```text
theta=a^(N-1).
```

No claim is made that this process is a universal model of sensory evolution.

## Theorem RGC1 — exact selected stationary law under a reversible neutral proposal

For a proposed move `x -> y`, the Moran fixation probabilities satisfy

```text
rho(W_y/W_x) / rho(W_x/W_y)
= (W_y/W_x)^(N-1).
```

By reversibility of the neutral proposal,

```text
mu_x Q_xy = mu_y Q_yx.
```

Therefore the selected origin-fixation transition probabilities satisfy detailed balance with

```text
boxed: pi_x proportional to mu_x theta^g(x).
```

### Proof

For `x!=y`, write the off-diagonal selected transition probability as

```text
P_xy = Q_xy rho(W_y/W_x).
```

Then

```text
[mu_x theta^g(x)] P_xy
/
[mu_y theta^g(y)] P_yx
```

is the product of

```text
(mu_x Q_xy)/(mu_y Q_yx) = 1
```

and

```text
theta^(g(x)-g(y))
* rho(W_y/W_x)/rho(W_x/W_y).
```

Since `W_y/W_x=a^(g(y)-g(x))`, the fixation-probability ratio equals

```text
a^((N-1)(g(y)-g(x)))
= theta^(g(y)-g(x)),
```

so the product is one. Hence detailed balance holds. Connectivity gives a unique stationary law. QED.

This is a standard reversible mutation-selection result in a routing-specific notation, not a priority claim.

## 3. Neutral mutation mass, not raw multiplicity, is the stationary representation coordinate

Define the neutral mutation mass of gain layer `r` by

```text
B_r = sum_{x:g(x)=r} mu_x.
```

Aggregating RGC1 over a gain layer gives stationary layer weight

```text
boxed: M_r(theta)=B_r theta^r.
```

Thus the stationary gain distribution is

```text
P(g=r)=B_r theta^r / sum_j B_j theta^j.
```

If the neutral proposal is symmetric and therefore has uniform neutral measure, then

```text
B_r = (# genotypes in layer r)/(# all genotypes),
```

and raw genotype multiplicity is sufficient up to a common normalization. This is exactly the special case used in PR #20.

For a nonuniform reversible mutation proposal, equal genotype counts do not imply equal neutral mutation mass.

## Theorem RGC2 — exact full-phase modal inequalities

The full gain layer `q` is stationary-modal if and only if, for every `r<q`,

```text
B_q theta^q >= B_r theta^r.
```

Equivalently,

```text
boxed: theta^(q-r) >= B_r/B_q  for every r<q.
```

So `q` and phenotype fitness alone do not identify the stationary mode. The additional representation input needed is the neutral layer-mass vector

```text
(B_0,...,B_q).
```

The product-routing modal threshold `2^(q+1)-1` is one special evaluation of these inequalities under the branch-product uniform proposal.

## 4. Accessibility is a different representation coordinate

Stationary layer masses do not determine mutation distance.

For a declared start genotype `x0`, shortest access to gain at least `r` is

```text
d_Q(x0,r)
=
shortest support-graph distance from x0 to {x:g(x)>=r}.
```

This depends on the support graph of `Q`, not only on its neutral stationary measure.

The executable audit includes two symmetric mutation kernels with:

```text
same genotypes,
same gains,
same uniform neutral measure,
same stationary layer distribution,
```

but full-phase support distances `3` and `1`, respectively.

Therefore the representation declaration cannot be compressed to a single scalar or to phenotype multiplicities alone.

## 5. Exact nonuniform-mutation witness

Consider three genotypes with gains

```text
(0,1,2)
```

and reversible neutral proposal

```text
Q =
[1/2  1/2   0 ]
[1/4  1/2  1/4]
[ 0   1/2  1/2].
```

Its neutral stationary measure is

```text
mu=(1/4,1/2,1/4).
```

There is still exactly one genotype per gain level, but at `theta=2` the selected raw layer weights are

```text
(1/4, 1, 1),
```

so the normalized stationary distribution is

```text
(1/9,4/9,4/9).
```

The full phase only ties the middle gain layer.

By contrast, the symmetric compressed gain chain from PR #24 has uniform neutral measure, giving at the same `theta=2`

```text
(1,2,4)/7,
```

so the full phase is uniquely modal with mass `4/7`.

This shows that even raw phenotype multiplicity is not enough when mutation proposal bias changes the neutral stationary measure.

## 6. Representation certificate for downstream claims

The extended adaptive-gain chain should therefore be written as

```text
required local feedback phase
-> required structural gap q
-> finite sensing phenotype requirement
-> declared genotype-policy representation
   - support graph of Q
   - reversible neutral measure mu
   - gain map g(x)
-> mutation accessibility / finite-population stationary occupancy.
```

For stationary occupancy, the sufficient compressed object is the neutral gain-mass vector `(B_r)` under the reversible origin-fixation assumptions.

For mutational accessibility, the support graph remains necessary.

Neither object is identified by the upstream finite-sensing theorem.

## 7. Prior-art ceiling

Do not claim novelty for:

- reversible mutation-selection chains;
- mutation bias in equilibrium distributions;
- Moran origin-fixation stationary laws;
- genotype-phenotype redundancy;
- phenotype abundance bias;
- neutral networks;
- representation-dependent accessibility or evolvability;
- free fitness / fitness-entropy competition.

Relevant established context includes Sella & Hirsh (2005) on statistical-physics formulations of finite-population evolution and the extensive GP-map literature on redundancy, phenotypic bias, neutral networks and accessibility. The `arrival of the frequent` literature likewise shows that common phenotypes can dominate evolutionary outcomes even when rarer alternatives are fitter.

The value here is therefore a model-declaration result:

> the adaptive-gain extension requires two additional representation certificates beyond the ecological required gap: a mutation support graph for accessibility and a neutral mutation mass by gain layer for stationary occupancy.

## 8. Executable audit

Implementation:

```text
adaptive_gain/routing_reversible_certificate.py
```

Tests:

```text
tests/test_routing_reversible_certificate.py
```

The tests use exact `Fraction` arithmetic to verify reversibility, selected detailed balance, `pi P=pi`, the nonuniform three-state witness, the uniform branch-product special case and the independence of support distance from neutral layer mass.
