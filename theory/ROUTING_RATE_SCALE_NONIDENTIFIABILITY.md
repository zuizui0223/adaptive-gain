# Absolute mutation-rate scale and routing phase-entry time

Status: stacked side theory on `theory/routing-rate-scale-nonidentifiability`. This is not part of the frozen Theoretical Ecology submission.

## Question

The stationary-nonidentifiability layer separates relative mutation bias from phenotype fitness. A final timing coordinate remains:

> If the gain map, support graph, neutral mutation measure, selected stationary distribution and shortest path are all fixed, is stochastic phase-entry time identified?

No. An overall mutation/proposal-rate scale changes waiting time while leaving stationary proportions and support distance unchanged.

## Fixed construction

Use the gain-path certificate from PR #29 with gain states

```text
0 <-> 1 <-> ... <-> q,
```

a fixed target selected stationary distribution `p`, neutral measure `mu`, and selected tilt `theta`.

For common edge scale

```text
epsilon in (0,1],
```

define the neutral proposal kernel by

```text
Q_epsilon[r,r+1] = epsilon mu[r+1],
Q_epsilon[r+1,r] = epsilon mu[r],
```

and put the remaining probability on the diagonal.

All `epsilon` share:

- the same gain map;
- the same path support;
- the same neutral stationary measure `mu`;
- the same selected stationary distribution `p`;
- the same shortest support distances.

## Theorem RTS1 — exact lazy scaling of the selected chain

Let `P_epsilon` be the Moran origin-fixation selected transition matrix at proposal scale `epsilon`, and let `P_1` be the scale-one matrix.

Every off-diagonal proposal probability is multiplied by `epsilon`; the missing probability is added to the resident self-loop. Failed fixation probabilities are unchanged. Therefore

```text
boxed: P_epsilon = (1-epsilon) I + epsilon P_1.
```

This is an exact finite-state identity.

## Corollary RTS1.1 — expected hitting time scales as 1/epsilon

For any target set and any start state outside it, let `H_epsilon` be expected proposal attempts to hit the target under `P_epsilon`.

The first-step equation is

```text
H_epsilon
= 1 + (1-epsilon) H_epsilon + epsilon P_1 H_epsilon
```

on transient states. Cancelling the common factor gives

```text
boxed: H_epsilon = H_1 / epsilon.
```

Thus an arbitrary slowdown of the absolute proposal rate makes phase entry arbitrarily slow without changing stationary phase occupancy or mutational graph distance.

## Canonical q=2 fixture

Use the fixed target stationary law

```text
p=(1/10,1/5,7/10),
theta=2.
```

For the scale-one selected chain, exact Fraction linear solving gives

```text
H_1 = 585/56.
```

Therefore

```text
epsilon=1/2 -> H=585/28,
epsilon=1/3 -> H=1755/56.
```

For all of these scales:

```text
stationary distribution = (1/10,1/5,7/10),
shortest full-phase support distance = 2.
```

Only the stochastic timing changes.

## Identifiability consequence

The downstream declaration ladder now separates three different representation/rate coordinates:

1. **support graph** — determines reachability and shortest edit distance;
2. **relative mutation bias / neutral measure** — determines stationary abundance bias together with selection;
3. **absolute proposal-rate scale** — determines waiting-time scale.

Thus even after fixing

```text
required gap q,
phenotype fitness,
genotype/gain map,
support topology,
relative mutation bias,
stationary phase occupancy,
```

absolute phase-entry time is not identified without a rate scale.

Do not translate proposal attempts into biological generations without an empirical mutation-rate model.

## Prior-art ceiling

Markov-chain laziness, stochastic time rescaling, mutation-rate effects on waiting times, origin-fixation timing and hitting-time linear systems are established prior art. No novelty claim is made for `1/epsilon` scaling.

This result is only a declaration/claim-boundary theorem for the adaptive-gain extension.

## Executable audit

Implementation:

```text
adaptive_gain/routing_rate_scale_nonidentifiability.py
```

Tests:

```text
tests/test_routing_rate_scale_nonidentifiability.py
```

The audit verifies the exact matrix identity, exact stationary invariance, support-distance invariance and exact Fraction hitting-time scaling for multiple small cases.
