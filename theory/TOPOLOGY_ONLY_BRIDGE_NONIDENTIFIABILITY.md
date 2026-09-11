# Topology-only sensing bridge is underdetermined

Status: side-theory negative result. This note is **not** part of the frozen Theoretical Ecology submission.

## Question

Issue #13 asks for a biologically justified bridge

```text
psi: PAYOFF topology T -> finite sensing task S(T).
```

Before searching for a particular bridge, ask a more basic identifiability question:

> Does the bare PAYOFF topology state already determine the adaptive/fixed sensing gap?

The answer under the current source semantics is no.

## What a bare PAYOFF topology contains

PAYOFF topology states encode retained/released developmental, genetic, or structural coupling among fitness-relevant functions. PAYOFF additionally supplies quantities such as intrinsic optimized payoff, topology distance, mutation adjacency, fixation quantities, and valley depth.

Those objects do **not** specify the finite sensing-task ingredients used by `adaptive-gain`:

```text
represented worlds,
target map,
query vocabulary,
query outcome map,
query costs,
branch-dependent physical availability.
```

Therefore a topology state does not, by itself, define

```text
C_A,
C_F,
g = C_F-C_A.
```

This is a source-semantics statement, not a claim that biological topology can never affect sensing.

---

## Proposition TOB1 — topology alone does not identify the structural gap

Under the current PAYOFF/adaptive-gain bridge contract, there is no value of the structural gap `g` that is logically determined by a bare topology state `T` alone.

More strongly, even fixing the following coarse finite-task descriptors does not identify `g`:

```text
number of represented worlds = 4,
number of declared queries = 3,
all query costs = 1,
every query binary,
two target classes with multiplicities 2 and 2.
```

### Witness A — strict adaptive gain

The registered PAYOFF routing witness has

```text
n = 4,
m = 3,
all costs = 1,
all query arities = 2,
target multiplicities = (2,2),
C_A = 2,
C_F = 3,
g = 1.
```

It is `adaptive_gain.witnesses.payoff_routing_task()`.

### Witness B — no strict adaptive gain

The registered routing-bypass control has the same coarse descriptors:

```text
n = 4,
m = 3,
all costs = 1,
all query arities = 2,
target multiplicities = (2,2),
```

but

```text
C_A = 2,
C_F = 2,
g = 0.
```

It is `adaptive_gain.witnesses.routing_bypass_control()`.

### Proof

The two finite tasks agree on all coarse descriptors listed above but have different exact adaptive/fixed gaps. The difference is carried by the detailed relation among worlds, targets, and query outcomes.

Current PAYOFF topology semantics contain no rule that selects one of these finite sensing relations, rules out the other, or otherwise reconstructs the missing outcome/target incidence structure. Thus pairing the same bare topology label with either finite sensing completion is not contradicted by topology-only information.

Consequently no topology-only value `g(T)` is identified by the current source semantics. QED.

### Important interpretation

`compatible with the bare topology information` does **not** mean `biologically realized by that topology`. The proposition is an underdetermination result: the source state lacks enough sensing semantics to choose among multiple finite completions.

---

## Corollary TOB1.1 — topology distance does not determine sensing-gap distance

Without additional bridge semantics, neither Hamming distance on the PAYOFF topology graph nor any topology-only metric determines

```text
|g(T')-g(T)|.
```

Therefore quantities such as a structural jump modulus

```text
J_g = max_{T~T'} |g(T')-g(T)|
```

cannot be inferred from topology adjacency alone.

This blocks an otherwise tempting but unsupported claim that one edge release corresponds to one bounded change in sensing complexity.

---

## Corollary TOB1.2 — the bridge must be an enriched architecture object or a declared generative rule

A licensed bridge must add sensing semantics beyond bare topology. Two equivalent organizational choices are:

### Enriched state

Use an architecture state such as

```text
T_tilde = (T, Omega, tau, Q, O, c, A),
```

where, schematically,

```text
T      = biological coupling topology,
Omega  = represented ecological alternatives,
tau    = target distinction,
Q      = cue/query resources,
O      = topology-conditioned cue outcome map,
c      = acquisition costs,
A      = topology-conditioned physical availability/dependency rules.
```

Then the finite sensing task is derived from `T_tilde`, not from `T` alone.

### Generative rule

Alternatively declare a biological mechanism

```text
Gamma(T) -> (Omega_T, tau_T, Q_T, O_T, c_T, A_T)
```

before computing adaptive/fixed gaps.

Either route makes the missing assumptions auditable.

---

## Relation to informed-consent / declaration discipline

This negative result is where the earlier declaration principle becomes operational rather than rhetorical.

The missing sensing semantics must be declared before computing the joint mutation/sensing reachability quantities. Otherwise the bridge can be chosen after seeing the desired `g(T)` pattern.

Thus the correct order is

```text
biology declares Gamma or T_tilde
-> adaptive-gain computes g(T)
-> target regime fixes q
-> V_q, d_q, B_q are computed prospectively.
```

Do not reverse this order by selecting a topology-to-cue interpretation because it produces the desired phase-reachability result.

---

## Consequence for issue #13

The completion criterion is now sharper.

It is **not enough** to enumerate PAYOFF topologies and assign finite tasks to them. A valid completion must justify the additional mapping from biological integration state to cue/decision structure.

The strongest useful future witness would provide:

1. one predeclared biological rule `Gamma`;
2. at least two topology states whose induced finite tasks are non-isomorphic in a biologically interpretable way;
3. exact `C_A(T), C_F(T), g(T)`;
4. a predeclared target threshold `q`;
5. a nontrivial joint result such as `V_q != empty` but `B_q>0` from a resident state.

Until such a rule exists, the executable topology-regime module remains correctly conditional on externally supplied gaps.

---

## Novelty boundary

The logical fact that omitted variables make a mapping non-identifiable is not a broad mathematical novelty claim. The value of TOB1 is narrower: it gives an explicit exact witness inside the current repository showing that PAYOFF topology semantics, even supplemented by coarse finite-task counts, are insufficient to determine the adaptive/fixed sensing gap.

Do not advertise this as a general impossibility theorem for network structure and information processing.
