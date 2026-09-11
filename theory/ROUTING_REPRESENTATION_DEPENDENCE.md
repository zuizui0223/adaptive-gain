# Exact representation dependence of routing phase accessibility

Status: stacked side theory on `theory/routing-representation-dependence`. This is not part of the frozen Theoretical Ecology submission.

## 1. Question

The current side-theory stack now contains an exact required-gap coordinate `q`, an explicit branch-product routing genotype, local mutation geometry, neutral accessibility times and a finite-population origin-fixation stationary law.

The remaining identifiability question is:

> Are mutational accessibility and stationary phase occupancy determined by the ecological required gap `q` and phenotype-level fitness schedule alone, or do they additionally depend on the genotype-policy representation?

They depend on the representation.

This is not a generic novelty claim. Genotype-phenotype maps, neutral networks, phenotypic bias, representation locality and representation-dependent evolvability are established subjects. The point here is to make the dependence exact inside the adaptive-gain `q` coordinate.

## 2. Hold phenotype-level biology fixed

Fix an integer

```text
q>=1
```

and the same phenotype/gain set

```text
G={0,1,...,q}.
```

Assign the same phenotype-level fitness schedule in both models:

```text
W(g)=a^g,  a>=1.
```

Under a population size `N` origin-fixation process, define the same effective tilt

```text
theta=a^(N-1).
```

Only the genotype representation and its local mutation graph differ.

## 3. Encoding A: branch-product routing genotype

Use the representation already declared in PR #20:

```text
X_prod={0,...,q}^k,
k=q+1,
g(x)=min_i x_i.
```

One local mutation changes one coordinate by `+/-1`.

Exact results already established are:

```text
shortest distance to gain r = k r,
D_r=(q-r+1)^k-(q-r)^k,
stationary layer weight = D_r theta^r,
full-phase modal threshold = 2^k-1.
```

The full-gain genotype is unique, but the layer directly below it contains

```text
D_{q-1}=2^k-1
```

genotypes.

## 4. Encoding B: compressed gain-chain genotype

Now declare a minimal phenotype-faithful encoding:

```text
X_chain={0,1,...,q},
g(r)=r.
```

One local mutation changes the coordinate by `+/-1`; invalid boundary proposals are null. The same Moran origin-fixation rule and the same phenotype fitness `W(r)=a^r` are used.

There is exactly one genotype per gain level. Therefore

```text
shortest distance to gain r = r,
stationary layer weight = theta^r.
```

The full phase is a modal layer iff

```text
theta>=1,
```

and is uniquely modal for `theta>1`.

The stationary full-phase mass is

```text
P_chain(full)=theta^q / sum_{j=0}^q theta^j.
```

For `q>1` and `theta>1`, the half-mass boundary is the unique nontrivial root of

```text
theta^(q+1)-2 theta^q+1=0.
```

For `q=2`, this reduces to

```text
theta^2-theta-1=0,
```

so the positive nontrivial threshold is the golden ratio.

## Theorem RDN1 — exact accessibility inflation from representation alone

For every

```text
1<=r<=q,
```

the two encodings represent the same gain target `r`, but

```text
d_prod(r)=(q+1)r,
d_chain(r)=r.
```

Hence

```text
boxed: d_prod(r)/d_chain(r)=q+1.
```

In particular, full gain `q` is

```text
q(q+1)
```

local edits away in the branch-product encoding but only

```text
q
```

edits away in the compressed encoding.

This is a representation statement, not an intrinsic lower bound for the ecological task.

## Theorem RDN2 — exact stationary mode-threshold inflation

The compressed full-phase modal threshold is

```text
theta_chain=1,
```

whereas the branch-product threshold is

```text
theta_prod=2^(q+1)-1.
```

Therefore

```text
boxed: theta_prod/theta_chain=2^(q+1)-1.
```

For every

```text
1<theta<2^(q+1)-1,
```

the same phenotype fitness schedule makes the full phase uniquely modal in the compressed encoding while it is nonmodal in the branch-product encoding.

Thus `q` plus `W(g)` does not identify stationary phase occupancy.

## Corollary RDN2.1 — a universal theta=2 contradiction witness

Take

```text
theta=2.
```

For every `q>=1`, the compressed encoding has

```text
P_chain(full)=2^q/(2^(q+1)-1)>1/2,
```

so the full phase is both the unique mode and a stationary majority.

But

```text
2 < 2^(q+1)-1,
```

so in the branch-product encoding the full phase is not even modal.

Therefore the same

```text
required gap q,
phenotype levels,
fitness schedule,
population-level tilt theta=2
```

produces qualitatively opposite stationary conclusions solely because the genotype representation differs.

## 5. Canonical q=2 witness

Both encodings have the same gain set

```text
{0,1,2}
```

and the same fitness schedule. At `theta=2`:

### Compressed chain

```text
layer weights = (1,2,4),
full mass = 4/7 > 1/2,
full phase = unique mode,
shortest full-gain distance = 2.
```

### Branch-product routing

The exact layer degeneracies are

```text
(19,7,1),
```

so stationary weights are

```text
(19,14,4),
full mass = 4/37,
full phase = nonmodal,
shortest full-gain distance = 6.
```

The compressed half-mass threshold is the golden ratio, while the branch-product exact half-mass boundary from PR #20 is

```text
(7+5 sqrt(5))/2.
```

So representation changes both accessibility and the amount of finite-population selection needed to make the same phenotype dominate.

## 6. What is and is not identified

The upstream finite-sensing theorem identifies, under its declared task model, the minimum/Pareto structural requirement needed for a feedback phase.

It does **not** by itself identify:

```text
how that sensing phenotype is encoded heritably,
which local genotype edits are possible,
how many genotypes realize each routing phenotype,
how mutation proposals are distributed among them.
```

Those are additional causal/modeling inputs.

Therefore the extended chain should now be written as

```text
required phase
-> q
-> finite sensing phenotype requirement
-> [additional genotype-policy map]
-> mutation accessibility / stationary occupancy.
```

The bracketed map cannot be deleted without changing the answer.

## 7. Relation to prior art

This result should not be advertised as discovering representation dependence. Empirical and theoretical GP-map work already shows that genotype-network architecture influences mutational accessibility, findability, robustness and evolutionary dynamics; phenotypic bias and free-fitness work likewise establishes abundance-selection competition.

The safe repository-level contribution is narrower:

> Within one exact eco-evolutionary required-gap coordinate, two explicitly declared genotype encodings with identical gain phenotypes and fitness values give exact, qualitatively opposite accessibility and stationary phase conclusions.

This is best treated as an identifiability/claim-boundary theorem for the adaptive-gain extension unless broader prior-art review supports something stronger.

## 8. Executable audit

Implementation:

```text
adaptive_gain/routing_representation_dependence.py
```

Tests:

```text
tests/test_routing_representation_dependence.py
```

The tests compare product distances to independent BFS, verify the compressed origin-fixation stationary law exactly, check the all-q `theta=2` contradiction witness, and freeze the canonical `q=2` masses `4/7` versus `4/37`.
