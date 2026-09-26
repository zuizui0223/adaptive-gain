# A sufficient structural target for the topology-to-sensing bridge

Status: side-theory bridge refinement. This note is not part of the frozen Theoretical Ecology submission.

## 1. Full finite tasks are sufficient but unnecessarily rich

Issue #13 originally asked for a map

```text
psi: PAYOFF topology T -> finite sensing task S(T).
```

A complete `FiniteTask` certainly determines the adaptive/fixed structural gap, but the earlier `adaptive-gain` theory proves that much less information is sufficient when the desired downstream output is only

```text
(C_A, C_F, g=C_F-C_A).
```

This matters biologically: a future bridge should not be required to invent world identities, query labels, or transition wiring that are irrelevant to the scalar structural gap.

---

## 2. Adaptive-side sufficient object

`CONTINUATION_BISIMULATION.md` proves that the cost-labelled recursive continuation type preserves the exact minimum adaptive worst-path cost.

Schematically, for a residual state `s`,

```text
Type_A(s)
= terminal
```

when resolved, and otherwise

```text
Type_A(s)
= {
    (query cost,
     set of mixed-child continuation types)
  : productive actions at s
  }.
```

If two states have the same continuation type, they have the same adaptive value.

Therefore the root continuation object determines

```text
C_A.
```

It deliberately forgets query identity, outcome labels, pure children, and multiplicities that do not affect the deterministic min-max objective.

It does **not** determine `C_F`.

---

## 3. Fixed-side sufficient object

`PRODUCTIVE_FRONTIER_SUFFICIENCY.md` proves that a fixed bundle resolves exactly when it hits every reachable productive set. Inclusion-nonminimal productive sets may be discarded.

Let

```text
H_min
```

be the minimal productive frontier together with physical query costs. Then

```text
C_F
=
minimum weighted hitting-set cost of H_min.
```

Thus the minimal productive frontier determines the exact fixed comparator without retaining world-pair identities, used-query histories, or child wiring.

---

## Proposition TSK1 — joint structural sufficiency for the gap

Suppose a biological bridge associated with topology `T` supplies:

1. a valid cost-labelled adaptive continuation object `K_A(T)` sufficient for `C_A(T)`;
2. a valid minimal productive frontier `H_min(T)` with its physical resource costs, sufficient for `C_F(T)`.

Then the structural gap is identified exactly as

```text
g(T)
= C_F[H_min(T)] - C_A[K_A(T)].
```

### Proof

The continuation preservation theorem gives a unique exact adaptive minimum from `K_A(T)`. The productive-frontier hitting-set theorem gives a unique exact fixed minimum from `H_min(T)`. Subtracting the two exact scalar costs gives `g(T)`. QED.

This is a composition of already established repository theorems. It is not presented as a new generic sufficiency theorem.

---

## 4. Why both halves are needed

The two kernel components are independently necessary for the current exact scalar representation in the sense that either one can be held fixed while the other changes the resulting gap.

### 4.1 Same adaptive continuation, different productive frontier

`CONTINUATION_BISIMULATION.md` contains an exact four-world collision. Two tasks have the same recursive root continuation class and

```text
C_A=2
```

in both cases, but their fixed costs are

```text
C_F=3
```

and

```text
C_F=2.
```

Hence their gaps are 1 and 0. The difference resides entirely in fixed-side resource co-location / productive-frontier structure.

The repository also contains stronger negative layers showing that several richer resource summaries still fail to determine `C_F`, including continuation structure augmented by resource-orbit capacities or per-resource role profiles.

### 4.2 Same productive frontier, different adaptive continuation

The side-theory witness

```text
same_frontier_different_adaptive_cost_collision()
```

provides the converse collision.

Both tasks have:

```text
5 represented worlds,
2+3 target balance,
3 unit-cost binary queries,
H_min = {{q0},{q1},{q2}},
C_F = 3.
```

But their adaptive costs are

```text
C_A = 3
```

and

```text
C_A = 2,
```

so their gaps are 0 and 1.

Thus the productive frontier alone does not determine adaptive routing value.

The exact regression is in `tests/test_topology_sensing_sufficient_kernel.py`.

### Consequence

Therefore a topology-to-gap bridge must carry information for both:

```text
adaptive continuation
and
fixed global separation obligations.
```

This is the precise structural meaning of the earlier warning that local routing structure and fixed-bundle burden are different objects.

The paired collisions do not establish universal categorical minimality of this representation. They do establish that neither component can simply be dropped from the current exact scalar bridge target.

---

## 5. Revised bridge target

Instead of requiring a biologically overcomplete map

```text
psi_full(T) -> S(T),
```

future work can target the compressed map

```text
Gamma_K(T)
->
(K_A(T), H_min(T), resource costs).
```

Once this is supplied prospectively,

```text
Gamma_K(T)
-> g(T)
-> V_q={T:g(T)>=q}
-> d_q, B_q
```

becomes an exact chain.

The executable `topology_sensing_reachability.py` already handles the last arrow after `g(T)` has been supplied.

---

## 6. Biological meaning of the two bridge halves

A legitimate biological mechanism would need to explain two different things.

### Adaptive continuation mechanism

It must determine why the organism can condition later cue acquisition/action on earlier cue outcomes, including the relevant costs and mixed continuations.

This is local/contingent architecture.

### Productive-frontier mechanism

It must also determine which physical cue resources are globally indispensable alternatives for separating every target-mixed ecological situation when acquisition cannot be conditioned on realized outcomes.

This is global resource co-location / obligation structure.

A biological description that gives only local module connectivity or only the number of available sensors is not enough in general.

---

## 7. Relation to topology-only nonidentifiability

`TOPOLOGY_ONLY_BRIDGE_NONIDENTIFIABILITY.md` shows that bare PAYOFF topology does not determine `g`, even when coarse finite-task counts are fixed.

TSK1 identifies a constructive way out:

```text
bare topology T
    insufficient

T + biologically generated joint structural kernel
    sufficient for g.
```

This does not prove that the joint kernel is universally minimal. `PRODUCTIVE_FRONTIER_SUFFICIENCY.md` explicitly calls it the smallest proved joint scalar-cost representation currently in the repository, not a categorical or information-theoretic minimum.

---

## 8. Stronger completion criterion for issue #13

A successful bridge no longer needs to reconstruct irrelevant full-task detail. It is enough to provide, for every topology in a predeclared architecture family:

```text
K_A(T),
H_min(T),
resource costs,
```

with a biological derivation that is fixed before `q`, `V_q`, or `B_q` are inspected.

The bridge should then be validated by constructing at least one explicit full finite task for a subset of topologies and checking that its direct exact costs agree with the compressed-kernel costs. This prevents the compressed biological interpretation from becoming a free-floating abstract assignment.

---

## 9. Novelty discipline

Do not claim novelty for continuation bisimulation, hitting sets, productive frontiers as a classical invariant, or the abstract fact that two sufficient statistics can be composed.

Potential future novelty would have to lie in a biologically justified map from heritable architecture to these exact finite sensing structures, especially if it yields a nontrivial joint statement about mutation accessibility and required eco-evolutionary phase reachability.
