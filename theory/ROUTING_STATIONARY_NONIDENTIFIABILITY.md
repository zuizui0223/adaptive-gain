# Stationary phase nonidentifiability under fixed local gain-path support

Status: stacked side theory on `theory/routing-stationary-nonidentifiability`. This is not part of the frozen Theoretical Ecology submission.

## 1. Question

The reversible-mutation certificate in PR #26 shows that selected stationary occupancy depends on the neutral mutation measure `mu`, while accessibility depends on mutation support.

A stronger identifiability question remains:

> If we hold the gain levels, phenotype fitness, raw genotype multiplicity and even the local mutation support fixed, is stationary phase occupancy then identified?

No.

Neutral mutation bias alone can generate any strictly positive stationary gain distribution under the declared reversible origin-fixation model.

This is an identifiability/no-go result, not a discovery of mutation bias. Mutation-selection balance and biased mutation effects are established prior art.

## 2. Hold almost everything fixed

Fix

```text
q>=1,
X={0,1,...,q},
g(r)=r.
```

So there is exactly one genotype per gain level.

Fix the local support graph

```text
0 <-> 1 <-> ... <-> q.
```

Fix an effective phenotype-selection tilt

```text
theta>=1.
```

The shortest support distance from gain 0 to full gain q is therefore always exactly `q`.

Now choose any strictly positive rational probability vector

```text
p=(p_0,...,p_q),
sum p_r=1.
```

The goal is to construct a reversible neutral mutation proposal on the same path whose selected stationary distribution is exactly `p`.

## Theorem RNI1 — arbitrary stationary occupancy under fixed gain-path support

Define unnormalized neutral weights

```text
mu_tilde_r = p_r theta^(-r),
```

and normalize them to a probability distribution

```text
mu_r = mu_tilde_r / sum_j mu_tilde_j.
```

Choose any fixed

```text
0<epsilon<=1
```

and on every adjacent pair set

```text
Q_{r,r+1}   = epsilon mu_{r+1},
Q_{r+1,r}   = epsilon mu_r.
```

Put all remaining row mass on the diagonal.

Then:

1. `Q` is stochastic;
2. every adjacent transition is positive, so its off-diagonal support is exactly the fixed local gain path;
3. `Q` is reversible with neutral stationary measure `mu` because

   ```text
   mu_r Q_{r,r+1}
   = epsilon mu_r mu_{r+1}
   = mu_{r+1} Q_{r+1,r};
   ```

4. under the Moran origin-fixation selection layer with effective tilt `theta`, the selected stationary law is exactly

   ```text
   boxed: pi_r = p_r.
   ```

### Proof of the last statement

PR #26 gives

```text
pi_r proportional to mu_r theta^r.
```

By construction,

```text
mu_r theta^r
proportional to
p_r theta^(-r) theta^r
= p_r.
```

Since `p` already sums to one, normalization gives `pi=p`. QED.

## 3. Consequence: a sharp nonidentifiability ceiling

Even the following data do not identify stationary phase occupancy:

```text
required gap q,
one genotype per gain level,
phenotype set {0,...,q},
local +/-1 gain-path support,
shortest full-phase distance q,
phenotype fitness schedule,
effective selection tilt theta.
```

For any desired strictly positive stationary answer `p`, some reversible mutation bias on that same local support reproduces it exactly.

Therefore a stationary phase claim requires additional information about neutral mutation proposal bias or an equivalent neutral stationary measure.

This is stronger than the two-encoding contrast in PR #24: here even the genotype count and support graph are held fixed.

## 4. Canonical q=2 contradiction at theta=2

Fix the same

```text
q=2,
gains=(0,1,2),
support 0-1-2,
theta=2,
shortest full distance=2.
```

### Mutation model A
Choose target selected stationary distribution

```text
p_plus=(1/10,1/5,7/10).
```

The full phase has stationary mass `7/10`, so it is a majority and the unique mode.

### Mutation model B
Choose

```text
p_minus=(7/10,1/5,1/10).
```

The full phase has stationary mass `1/10`, so it is a minority and nonmodal.

Both models have:

```text
identical required gap,
identical gain phenotypes,
identical one-genotype-per-gain multiplicity,
identical local path support,
identical shortest mutation distance,
identical phenotype fitness tilt.
```

They differ only in the neutral mutation proposal bias.

So the stationary biological interpretation can reverse while all of the above quantities remain fixed.

## 5. Mutation-rate scale versus mutation bias

The construction includes an edge scale `epsilon`.

Changing the common edge scale changes proposal rates and self-loop probabilities but not the reversible neutral measure `mu`. Consequently it does not change the selected stationary law.

This distinguishes two mutation features:

```text
relative bias / neutral measure -> stationary occupancy,
overall proposal scale          -> timing, not stationary proportions.
```

Absolute evolutionary timing still requires a mutation-rate/time model and is outside this theorem.

## 6. Relation to the declaration hierarchy

The extended adaptive-gain chain now has a hard separation:

```text
required eco-evolutionary phase
-> required gap q
-> finite sensing phenotype requirement
-> genotype-policy map
-> mutation support graph
-> neutral mutation bias / measure
-> selected stationary occupancy.
```

Removing the mutation-bias declaration makes the last arrow nonidentified even if all earlier objects are fixed.

For accessibility claims, support topology remains essential.
For stationary occupancy claims, neutral mutation mass remains essential.
For biological interpretation, issue #27 still requires system-specific qualification of both.

## 7. Prior-art ceiling

Do not claim novelty for:

- mutation bias affecting evolutionary outcomes;
- reversible mutation-selection equilibrium;
- mutation-selection balance;
- detailed balance;
- genotype-phenotype representation effects;
- neutral stationary measures.

The safe contribution is a claim-boundary theorem within this research program:

> phenotype-level phase requirements, fitness values and local mutation adjacency do not determine stationary phase occupancy; under the declared reversible origin-fixation model, unknown neutral mutation bias leaves the stationary gain distribution unrestricted over the positive simplex.

## 8. Executable audit

Implementation:

```text
adaptive_gain/routing_stationary_nonidentifiability.py
```

Tests:

```text
tests/test_routing_stationary_nonidentifiability.py
```

The tests use exact `Fraction` arithmetic to construct arbitrary positive rational target distributions, verify reversible local path support, confirm exact Moran-selected stationarity, freeze the q=2 opposite-outcome witness, and reject zero-mass or improperly normalized targets.
