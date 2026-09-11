# Two-sided factorization of the adaptive/fixed structural gap

Status: side-theory exact structural statement. This is not part of the frozen Theoretical Ecology submission and is not presented as an independent priority claim.

## Objects

For a finite deterministic sensing task `S`, write

```text
K_A(S)
```

for its cost-labelled adaptive continuation root structure, and

```text
H_min(S)
```

for its minimal productive frontier with physical query costs.

The earlier repository theorems give exact scalar evaluations

```text
V_A[K_A(S)] = C_A(S)
```

and

```text
tau_c[H_min(S)] = C_F(S).
```

Therefore

```text
g(S)
= C_F(S)-C_A(S)
= tau_c[H_min(S)]-V_A[K_A(S)].
```

---

## Theorem TGF1 — exact joint factorization, failure of either one-sided factorization

Across the declared finite deterministic task class:

1. the structural gap factors exactly through the pair `(K_A,H_min)`;
2. there is no function of `K_A` alone that recovers `g` for every task;
3. there is no function of `H_min` alone that recovers `g` for every task.

Equivalently,

```text
(K_A,H_min) -> g
```

is exact, while neither projection

```text
K_A -> g
```

nor

```text
H_min -> g
```

is valid on the full task class.

### Proof of joint factorization

Continuation sufficiency gives `C_A=V_A[K_A]`. Productive-frontier sufficiency gives `C_F=tau_c[H_min]`. Hence

```text
g=tau_c[H_min]-V_A[K_A].
```

### Counterexample to `K_A -> g`

Use `continuation_fixed_cost_collision()`.

The two tasks have the same adaptive continuation root class and

```text
C_A=2
```

in both tasks, while

```text
C_F=3
```

and

```text
C_F=2.
```

Thus their gaps are 1 and 0 despite identical `K_A`.

### Counterexample to `H_min -> g`

Use `same_frontier_different_adaptive_cost_collision()`.

The two tasks have identical minimal productive frontier

```text
{{q0},{q1},{q2}}
```

with unit costs, so

```text
C_F=3
```

in both tasks. Their adaptive costs are 3 and 2, so their gaps are 0 and 1 despite identical `H_min`.

QED.

---

## Interpretation for the topology bridge

A heritable architecture state cannot be mapped to the structural gap by supplying only a local contingent-routing description or only a global fixed-resource obligation description.

A sufficient bridge target is

```text
Gamma_K(T)
->
(K_A(T),H_min(T),resource costs),
```

after which

```text
g(T)
=tau_c[H_min(T)]-V_A[K_A(T)]
```

is exact.

This is stronger than saying that two summaries are convenient. The paired collisions show that each side can vary while the other is held fixed and can change the gap.

The result does **not** prove that `(K_A,H_min)` is a universally minimal categorical representation. It proves exact joint sufficiency plus non-sufficiency of either of these two projections.

---

## Biological reading

The two factors correspond to different natural-history questions.

### Adaptive side

```text
What outcome-contingent cue continuations are physically available, and at what cost?
```

This controls `V_A[K_A]`.

### Fixed side

```text
Which physical cue resources are globally unavoidable for separating all target-mixed situations without outcome-contingent routing?
```

This controls `tau_c[H_min]`.

A single coarse descriptor such as sensor number, average informativeness, cue arity, or ordinary network modularity need not determine both.

---

## Verification

The two counterexamples and the exact cost reconstruction are regression-tested in

```text
tests/test_topology_sensing_sufficient_kernel.py
```

using the repository's independent continuation and productive-frontier machinery.

---

## Claim boundary

Do not present TGF1 as a new theorem in decision-tree or hitting-set theory. Its role is internal structural clarification for the proposed biological topology-to-sensing bridge.
