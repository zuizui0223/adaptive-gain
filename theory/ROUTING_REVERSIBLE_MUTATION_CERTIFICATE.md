# Reversible mutation representation certificate

Status: stacked side theory on `theory/routing-reversible-mutation-certificate`. This is not part of the frozen Theoretical Ecology submission.

## 1. Question

The representation-dependence line shows that the same required gap `q` and the same phenotype-level fitness schedule can lead to different mutational accessibility and stationary phase occupancy under different genotype-policy encodings.

The minimal declaration needed for the finite-population extension is:

- a finite genotype set `X`;
- a gain map `g:X->{0,...,q}`;
- a connected neutral mutation proposal kernel `Q`;
- a positive neutral stationary measure `mu` satisfying detailed balance;
- a declared start genotype for accessibility questions.

The aim is not to discover mutation-selection balance, but to state exactly which representation inputs are required before the adaptive-gain extension can make population-level claims.

## 2. Neutral mutation certificate

Require

```text
mu_x Q_xy = mu_y Q_yx
```

for all genotype states `x,y`.

Thus `Q` is reversible with neutral stationary measure `mu`.

The support graph of `Q` and its stationary measure play distinct roles:

- support graph -> mutational reachability and shortest distance;
- neutral stationary measure -> mutation/representation bias among genotypes.

## 3. RGC1 — selected stationary law

Use the same Moran origin-fixation rule as the routing population layer and phenotype fitness

```text
W(x)=a^g(x),
```

with population size `N` and

```text
theta=a^(N-1).
```

The Moran fixation-ratio identity gives

```text
rho(W_y/W_x) / rho(W_x/W_y)
= (W_y/W_x)^(N-1)
= theta^(g(y)-g(x)).
```

Combining this with neutral reversibility gives selected detailed balance for

```text
boxed: pi_x proportional to mu_x theta^g(x).
```

Therefore stationary gain-layer weight is

```text
B_r theta^r,
```

where

```text
B_r = sum_{x:g(x)=r} mu_x.
```

Raw genotype multiplicity is only the special case in which `mu` is uniform.

## 4. RGC2 — exact modal inequalities

Let `q` be the full required phase. The full phase is stationary-modal exactly when, for every `r<q`,

```text
B_q theta^q >= B_r theta^r.
```

Equivalently,

```text
boxed: theta^(q-r) >= B_r/B_q  for every r<q.
```

Thus `q` and phenotype fitness alone do not identify stationary occupancy. The neutral gain-mass vector

```text
(B_0,...,B_q)
```

is an additional required representation coordinate.

## 5. Accessibility coordinate

Stationary mass does not determine shortest mutational access.

Define the support graph of `Q` by an edge whenever either direction has positive proposal probability. Starting from the declared genotype `x_0`, shortest access to gain `r` is

```text
d_Q(x_0,{x:g(x)>=r}).
```

The tests include two symmetric four-state kernels with identical gain labels and the same uniform neutral measure, hence identical selected stationary layer distributions, but different support distances to the full phase.

So accessibility and stationary occupancy require different parts of the representation declaration.

## 6. Nonuniform mutation-bias witness

Consider one genotype at each gain level `0,1,2` and neutral proposal

```text
[[1/2,1/2,0],
 [1/4,1/2,1/4],
 [0,1/2,1/2]].
```

Its neutral reversible measure is

```text
mu=(1/4,1/2,1/4).
```

At `theta=2`, selected weights are

```text
(1/4, 1, 1),
```

so normalized stationary gain mass is

```text
(1/9,4/9,4/9).
```

A symmetric gain chain with the same raw multiplicity `(1,1,1)` instead has

```text
(1/7,2/7,4/7).
```

Therefore raw genotype count alone is insufficient; mutation bias changes stationary phase occupancy.

## 7. RGC3 — fixed-support nonidentifiability under unspecified mutation bias

A stronger result holds even when the support graph is fixed.

Fix gain levels

```text
0,1,...,q
```

with the same local path support

```text
0 <-> 1 <-> ... <-> q,
```

and fix any positive finite-population tilt `theta`.

For **any strictly positive target stationary distribution**

```text
p=(p_0,...,p_q),
```

choose

```text
mu_r proportional to p_r theta^{-r}.
```

Then place any positive reversible conductance on every adjacent path edge, for example

```text
c_r = epsilon min(mu_r,mu_{r+1}),
0<epsilon<=1/2,
```

and set

```text
Q_{r,r+1}=c_r/mu_r,
Q_{r+1,r}=c_r/mu_{r+1},
```

with diagonal entries completing each row to one.

This keeps the **same path support** and satisfies

```text
mu_r Q_{r,r+1}=c_r=mu_{r+1}Q_{r+1,r}.
```

The selected law is therefore

```text
pi_r proportional to mu_r theta^r
                proportional to p_r,
```

hence after normalization

```text
boxed: pi=p.
```

So even the combined information

```text
q + phenotype fitness schedule + local +/-1 mutation support
```

still does not identify stationary phase occupancy. The neutral mutation measure / proposal bias is an additional causal input.

### Exact contradiction witness

For `q=2`, `theta=2`, and the same path support `0<->1<->2`, two valid reversible mutation kernels can have selected stationary laws

```text
A=(1/10,1/10,4/5),
B=(9/20,9/20,1/10).
```

Both have the same shortest support distances

```text
(0,1,2),
```

but the full phase has stationary mass `4/5` in A and `1/10` in B.

Thus fixing mutation locality still does not fix the evolutionary conclusion unless proposal bias is also declared.

## 8. Declaration contract

The extended chain should therefore be written as

```text
required eco-evolutionary phase
-> required structural gap q
-> finite sensing phenotype requirement
-> genotype-policy map
-> mutation support graph
-> neutral mutation measure / proposal kernel
-> accessibility / stationary phase occupancy.
```

The support graph and neutral mutation measure are logically distinct representation inputs.

## 9. Prior-art ceiling

Do not claim novelty for:

- reversible mutation-selection laws;
- mutation bias;
- Moran origin-fixation stationary distributions;
- genotype-phenotype maps;
- phenotype abundance bias;
- neutral networks;
- free fitness;
- representation-dependent evolvability.

The value of this side line is as an exact declaration/identifiability theorem for the adaptive-gain extension.

## 10. Executable audit

Core certificate:

```text
adaptive_gain/routing_reversible_certificate.py
```

Fixed-support nonidentifiability construction:

```text
adaptive_gain/routing_mutation_bias_nonidentifiability.py
```

Tests:

```text
tests/test_routing_reversible_certificate.py
tests/test_routing_mutation_bias_nonidentifiability.py
```

All calculations use exact `Fraction` arithmetic in the audited finite examples.
