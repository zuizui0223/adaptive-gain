# Mutation-bias nonidentifiability on fixed gain support

Status: stacked side theory on `theory/routing-reversible-mutation-certificate`. This is not part of the frozen Theoretical Ecology submission.

## Question

The reversible representation certificate shows that, for neutral mutation measure `mu`, phenotype gain `g` and finite-population tilt `theta`, the selected stationary law is

```text
pi_x proportional to mu_x theta^g(x).
```

A remaining identifiability question is stronger:

> If the required gap `q`, phenotype-level fitness schedule and even the local mutation support graph are fixed, is stationary phase occupancy identified without the neutral mutation probabilities?

No.

## Theorem RGC3 — arbitrary stationary occupancy on fixed path support

Fix gain levels

```text
0,1,...,q
```

and the path support

```text
0 <-> 1 <-> ... <-> q.
```

Fix any finite-population fitness tilt

```text
theta>0.
```

Let

```text
p=(p_0,...,p_q)
```

be any strictly positive target stationary distribution.

Choose the neutral mutation measure

```text
mu_r proportional to p_r theta^{-r}.
```

Then choose positive conductance on each adjacent path edge, for example

```text
c_r = epsilon min(mu_r,mu_{r+1}),
0<epsilon<=1/2,
```

and define

```text
Q_{r,r+1}=c_r/mu_r,
Q_{r+1,r}=c_r/mu_{r+1},
```

with the diagonal completing each row to one.

The kernel is connected and reversible because

```text
mu_r Q_{r,r+1}=c_r=mu_{r+1}Q_{r+1,r}.
```

Under Moran origin-fixation selection,

```text
pi_r proportional to mu_r theta^r
                proportional to p_r.
```

After normalization,

```text
boxed: pi=p.
```

Therefore `q + W(g) + local +/-1 path support` does **not** identify stationary phase occupancy. The neutral mutation measure is an additional required input.

## Fixed-support contradiction witness

Take `q=2` and `theta=2`, with the same gain path

```text
0 <-> 1 <-> 2.
```

Two admissible reversible neutral kernels can be constructed with selected stationary distributions

```text
A=(1/10,1/10,4/5),
B=(9/20,9/20,1/10).
```

Both models have:

```text
same q=2,
same phenotype gains,
same phenotype fitness tilt theta=2,
same local support graph,
same shortest support distances (0,1,2).
```

Yet in A the full phase has 80% stationary mass, while in B it has only 10%.

So even fixing mutation *locality* is insufficient; mutation *bias* remains causally relevant.

## Separation of representation coordinates

The extended adaptive-gain chain therefore requires at least two distinct representation coordinates:

1. **support graph** — determines which gains are reachable and shortest mutational distances;
2. **neutral mutation measure / reversible proposal weights** — determines stationary abundance bias once combined with finite-population selection.

Neither coordinate is recoverable from the required structural gap `q` alone.

The correct declaration chain is

```text
required eco-evolutionary phase
-> required structural gap q
-> finite sensing phenotype requirement
-> genotype-policy map
-> mutation support graph
-> neutral mutation measure / proposal kernel
-> accessibility and stationary phase occupancy.
```

Deleting either of the last two representation inputs can change the evolutionary conclusion.

## Prior-art ceiling

Do not claim novelty for:

- mutation bias affecting stationary distributions;
- reversible mutation-selection chains;
- genotype-phenotype maps;
- phenotype abundance bias;
- free fitness;
- neutral networks;
- representation-dependent evolvability.

The result is best used as an exact identifiability/claim-boundary theorem inside the adaptive-gain extension.

## Executable audit

Implementation:

```text
adaptive_gain/routing_mutation_bias_nonidentifiability.py
```

Tests:

```text
tests/test_routing_mutation_bias_nonidentifiability.py
```

The tests construct arbitrary target stationary laws exactly with `Fraction` arithmetic, verify the same path distances, and connect a `theta=2` construction back to the full Moran origin-fixation detailed-balance implementation.
