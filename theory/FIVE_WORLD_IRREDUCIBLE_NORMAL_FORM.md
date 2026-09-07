# Unique irreducible five-world strict-gain normal form

This note closes the complete finite scope

```text
5 represented worlds
2+3 target multiplicity
3 labeled binary unit-cost queries
```

There are `32^3 = 32,768` labeled query triples. This is a finite structural
classification, not an empirical prevalence estimate.

## Complete exact enumeration

Using the repository's exact adaptive and fixed solvers, the complete universe is

| `(C_A,C_F)` | labeled tasks |
|---|---:|
| unresolved | 17,928 |
| `(1,1)` | 5,768 |
| `(2,2)` | 6,336 |
| `(3,3)` | 720 |
| **`(2,3)`** | **2,016** |

Thus every strict case in this scope has

\[
\boxed{C_A=2<C_F=3},
\qquad
\boxed{\max C_F/C_A=3/2}.
\]

## Canonical separator signatures

Put the two worlds of the size-2 target class in canonical positions `0,1` and
the three worlds of the size-3 class in positions `2,3,4`. The six cross-target
pairs are ordered as

\[
(0,2),(0,3),(0,4),(1,2),(1,3),(1,4).
\]

Each binary query is represented by the 6-bit mask of cross-target pairs it
separates. Independent outcome flips do not change this mask. We then quotient
within-target world permutations and query order.

Because the cross-target graph is the connected complete bipartite graph
`K_{2,3}`, the cross-target equality/inequality pattern determines a binary query
labeling up to one global outcome flip. Therefore this separator representation
is complete for the declared binary-query symmetry, not merely a heuristic
feature.

Exactly five canonical signatures occur among strict tasks:

| canonical signature | labeled tasks | strict balanced 4-world deletions |
|---|---:|---:|
| `(7,9,49)` | 288 | 2 |
| `(7,14,54)` | 288 | 2 |
| `(7,27,42)` | 576 | 1 |
| `(14,21,45)` | 576 | 1 |
| **`(7,28,42)`** | **288** | **0** |

No non-strict task has any of these five signatures. Therefore, in this declared
scope,

\[
\boxed{
C_A<C_F
\iff
\sigma\in
\{(7,9,49),(7,14,54),(7,27,42),(14,21,45),(7,28,42)\}.
}
\]

## Deletion irreducibility

A five-world strict task is **world-deletion irreducible** here if deleting any
one represented world removes strict adaptive gain. It is **query-deletion
minimal** if deleting any one query also removes strict gain.

For the size-3 target class, deleting one world leaves a balanced 2+2 four-world
task. Across all 2,016 strict tasks, the exact count of strict balanced deletions
is

| number of strict balanced deletions | labeled tasks |
|---:|---:|
| **0** | **288** |
| 1 | 1,152 |
| 2 | 576 |

The 288 zero-deletion tasks all have the single canonical signature

\[
\boxed{\sigma_5=(7,28,42)}.
\]

For this signature, deleting either world from the size-2 target class also
removes strict gain: the resulting 1+3 four-world tasks have no strict gain. Thus
all five single-world deletions are non-strict.

Deleting any one query leaves only two query identities, while strict gain in the
finite deterministic model requires at least three. Hence the same standard form
is query-deletion minimal as well.

Consequently, within this declared scope,

\[
\boxed{
\text{world/query deletion-minimal strict gain}
\iff
\sigma=(7,28,42).
}
\]

The declared symmetry orbit of the standard representative contains exactly 288
labeled tasks, matching the complete irreducible count. Hence the irreducible set
is one symmetry orbit.

## Standard representative

Take

\[
T=(0,0,1,1,1)
\]

and queries

\[
q_0=(0,1,1,1,1),
\]
\[
q_1=(0,1,0,0,1),
\]
\[
q_2=(0,1,0,1,0).
\]

Their canonical separator masks are respectively `7`, `28`, and `42`.

An optimal adaptive policy can use `q1` first:

```text
q1
  outcome 0 -> q0
  outcome 1 -> q2
```

Every path has cost two, so

\[
C_A=2.
\]

The six cross-target pair separator rows are

\[
(1,2,3,4,5,6).
\]

In particular singleton rows `1`, `2`, and `4` make each of the three queries
uniquely necessary for at least one cross-target pair. Therefore every fixed
resolver buys all three queries:

\[
C_F=3.
\]

For the three deletions from the size-3 target class the exact costs are all

\[
(C_A,C_F)=(2,2).
\]

For the two deletions from the size-2 class the exact costs are `(2,2)` and
`(1,1)` for this representative. Thus every one-world deletion removes strict
gain.

## The new structure is adaptive-side, not a stronger fixed obstruction

The unique four-world minimal strict-gain normal form has raw cross-target pair
rows

\[
(1,2,4,7),
\]

whereas the five-world irreducible form has

\[
(1,2,3,4,5,6).
\]

After exact pair-obligation dominance, however, both reduce to

\[
\boxed{(1,2,4)}.
\]

So the new irreducible five-world mechanism does **not** arise because the fixed
pair-cover obstruction became stronger. The inclusion-minimal fixed-side kernel
is identical. What changes is the hidden-world partition geometry available to
the adaptive policy.

This is an important separation:

\[
\boxed{
\text{same minimal fixed obstruction}
\not\Rightarrow
\text{same adaptive routing geometry}.
}
\]

The four-world and five-world cores therefore share the same minimal fixed
certificate while belonging to different adaptive normal forms.

## Positive direct root information

Under uniform weights on the five represented worlds, the selected routing root
`q1` has strictly positive direct target information:

\[
I(T;q_1)\approx 0.0199730940\ \text{bits}.
\]

The full adaptive policy resolves the target, while its first result changes the
useful continuation. Therefore the first genuinely new deletion-minimal normal
form also provides a stronger control against treating zero direct root
information as essential to adaptive gain.

In particular,

\[
\boxed{I(T;Q_{\rm root})=0}
\]

is neither necessary for strict gain nor necessary for deletion-minimal strict
gain in these finite deterministic scopes.

## Validation

`adaptive_gain/five_world_normal_form.py` exposes:

- the five strict canonical signatures;
- the unique irreducible signature `(7,28,42)`;
- one standard representative;
- balanced and all-world deletion audits;
- query-deletion minimality;
- the standard raw symmetry-orbit count; and
- the complete 32,768-task enumerator.

Regression tests require:

```text
strict tasks                         = 2,016
irreducible strict tasks             = 288
irreducible canonical signatures     = 1
strict classification disagreements = 0
irreducible disagreements            = 0
standard all-world strict deletions  = 0
standard query strict deletions      = 0
```

against the exact adaptive/fixed solver.

## Scope boundary

This is an exact theorem for a declared finite binary deterministic universe. It
does not show that five biological states are intrinsically special, that the
same normal form survives noisy or continuous measurement models, or that the
288/32,768 labeled-task ratio is a natural prevalence. It identifies the first
new deletion-minimal finite decision structure found after the four-world minimal
core.
