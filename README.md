# adaptive-gain

A finite theory repository for **when outcome-contingent measurement choice is strictly better than a fixed measurement bundle**.

It was extracted from a cross-repository comparison of:

- [`zuizui0223/mrod`](https://github.com/zuizui0223/mrod) — an initial observation can route the next assay;
- [`zuizui0223/payoff`](https://github.com/zuizui0223/payoff) — an initial payoff contrast can route the next architecture distance;
- [`zuizui0223/balance`](https://github.com/zuizui0223/balance) — under the current threshold-span objective, branch labels change interval location but not the sufficient future-value state, giving a no-routing control.

The source repositories retain ownership of their scientific models. `adaptive-gain` abstracts only the finite decision structure and has no runtime dependency on those repositories.

## Core theorem

Let `W` be a finite hidden-world set, `T:W->labels` the declared target, and every query have a positive integer acquisition cost plus one deterministic outcome in every represented world.

Define

```text
C_A = minimum worst-path cost of guaranteed target resolution by an adaptive tree
C_F = minimum cost of a fixed resolving bundle
```

Every fixed bundle is an adaptive policy that ignores intermediate outcomes, so

\[
\boxed{C_A\le C_F}.
\]

Strict adaptive gain exists exactly when

\[
\boxed{C_A<C_F}.
\]

For integer acquisition budget `B`, the adaptive-only guaranteed-resolution window is

\[
\boxed{C_A\le B<C_F}.
\]

## Where potential gain goes

For one selected optimal adaptive tree, let

```text
U   = cost of every distinct query used anywhere in the tree
C_U = cheapest fixed resolver restricted to that tree union
```

Then

\[
C_A\le C_F\le C_U\le U
\]

and exactly

\[
\boxed{
U-C_A=(C_F-C_A)+(C_U-C_F)+(U-C_U)
}.
\]

Interpret the terms as

```text
branch-exclusive overhead = U-C_A
realized adaptive gain     = C_F-C_A
external shortcut discount = C_U-C_F
internal union redundancy  = U-C_U
```

so

\[
\boxed{
\text{adaptive gain}
=
\text{branch-exclusive overhead}
-
\text{internal redundancy}
-
\text{external shortcut}
}.
\]

Bypass is a discount, not a binary veto.

## Representation boundary: full pair incidence versus fixed kernel

For every query `q` and every pair of worlds with different targets, record whether `q` separates that pair.

The **full identity-indexed target-pair incidence**, together with target labels and query costs, is sufficient to recover both exact costs:

\[
\boxed{
\text{full target-pair incidence}
\Longrightarrow
(C_A,C_F).
}
\]

For one query, the cross-target pairs that are *not* separated reconstruct every target-mixed outcome cell as a connected component. Target-pure cells are already resolved, so their internal same-target partition is continuation-irrelevant.

This is implemented in `target_pair_incidence.py` and validated against the direct solver on all `15^3=3,375` triples of arbitrary set partitions of four worlds.

The important boundary is what happens after further compression. Pair-obligation dominance may reduce a fixed cover to an inclusion-minimal kernel. That kernel remains sufficient for `C_F`, but need not preserve adaptive routing geometry.

The four-world and five-world deletion-minimal strict-gain cores both reduce to the same minimal fixed kernel

\[
\boxed{(1,2,4)}
\]

while having different adaptive normal forms. Therefore

\[
\boxed{
\text{same minimal fixed obstruction}
\not\Rightarrow
\text{same adaptive routing geometry}.
}
\]

So the representation ladder is

\[
\boxed{
\text{full world/outcome model}
\to
\text{full identity-indexed target-pair incidence}
\to
\begin{cases}
\text{adaptive-safe state-local compression},\\
\text{aggressive fixed-cover kernel}.
\end{cases}
}
\]

See `theory/TARGET_PAIR_INCIDENCE_SUFFICIENCY.md`.

## Adaptive-safe state-local compression

`adaptive_safe_compression.py` now provides two exact adaptive-specific reductions.

### Continuation equality

At a current world set `A`, let

\[
\mathcal M_A(q)
\]

be the family of target-mixed outcome cells induced by query `q`. Pure-target cells are omitted because they terminate immediately.

If

\[
\mathcal M_A(q)=\mathcal M_A(r)
\]

and `q` costs no more than `r`, one cheapest representative is sufficient.

### Target-relevant refinement dominance

The stronger rule works directly on the active cross-target separation sets. Let

\[
S_A(q)
\]

be the cross-target pairs inside `A` separated by `q`.

If

\[
\boxed{S_A(q)\supseteq S_A(r),\qquad c(q)\le c(r),}
\]

then `q` is target-relevantly at least as fine as `r`. Every unresolved `q`-child lies inside one `r` outcome cell, so `r` is constant after `q` on every mixed child. Thus `q` safely dominates `r` at that Bellman state.

This strictly generalizes continuation equality: equal active separation masks are the tie case, while strict supersets let a genuinely finer cheap query replace a coarser expensive query.

A no-progress query with no active target-relevant separation is skipped.

Validation includes:

- all `15^3=3,375` three-query multi-valued partition tasks on four balanced worlds;
- all `15^2 x 2^2 = 900` two-query partition tasks with costs in `{1,2}`;
- different pure-branch partitions with the same mixed continuation;
- an explicit strict-refinement dominance control;
- equal-cost interchangeable queries; and
- no-progress query classes.

Both adaptive compressed solvers must match the original direct Bellman solver exactly in `C_A` on every exhaustive case.

See `theory/ADAPTIVE_SAFE_QUERY_COMPRESSION.md`.

## Fixed-side certificate ladder

A fixed resolver is a weighted cover of all cross-target world pairs. Strict gain can often be certified without first computing the exact numerical `C_F`:

```text
private-pair necessity
  -> integral pair packing
  -> fractional pair-cover dual
  -> exact integer budget-infeasibility proof at B=C_A
  -> exact fixed optimum, only when its value is needed
```

The layers are genuinely distinct, including a registered LP-integrality-gap control where the fractional bound stops at `C_A` but an exact integer infeasibility proof still establishes `C_F>C_A`.

See:

- `theory/FIXED_BYPASS_PAIR_COVER.md`
- `theory/PAIR_PACKING_LOWER_BOUND.md`
- `theory/FRACTIONAL_PAIR_COVER_BOUND.md`
- `theory/INTEGER_FIXED_COVER_PROOF.md`

## Exact proof compression

The fixed-side integer proof has several semantics-preserving compression layers:

```text
raw proof tree
-> two-sided residual kernel
-> exact-state DAG
-> weighted-incidence isomorphism quotient
-> color refinement
-> individualization-refinement
-> certified automorphism-orbit pruning
-> explicit isomorphism-transport DAG
-> parent-automorphism branch-orbit pruning
```

Highlights:

- a seeded proof expands to 19 tree nodes but only 14 exact-state DAG nodes;
- a six-world control compresses four label-specific residual states to two weighted-incidence isomorphism classes;
- color refinement reduces one exact permutation family from `720` to `12` candidates;
- exact automorphism stabilizers reduce several canonical searches to one orbit representative;
- every shared proof edge carries an explicit query transport that is independently verified;
- sibling proof branches in one exact parent query-automorphism orbit require only one recursive child proof.

For a proof node `v`, with `b(v)` raw affordable branches and `o(v)` orbit representatives,

\[
\boxed{s(v)=b(v)-o(v)}
\]

and

\[
\boxed{1\le b(v)/o(v)\le |\operatorname{Aut}(I_v)|}.
\]

## Finite normal-form ladder

### Unique minimal 4-world / 3-query core

For

```text
4 worlds
T=(0,0,1,1)
3 labeled binary unit-cost queries
```

all `16^3=4,096` tasks were classified exactly:

| `(C_A,C_F)` | labeled tasks |
|---|---:|
| unresolved | 1,688 |
| `(1,1)` | 1,352 |
| `(2,2)` | 864 |
| **`(2,3)`** | **192** |

All 192 strict tasks are one symmetry orbit with canonical separator signature

\[
\boxed{(3,5,9)}.
\]

### Adding a fourth query creates no new irreducible mechanism

For four worlds with four binary unit-cost queries, all `16^4=65,536` labeled tasks were enumerated. The 3,840 strict cases all have `(C_A,C_F)=(2,3)` and every one contains the unique three-query core after deleting at least one query.

The only strict canonical signatures are

```text
(0,3,5,9)   null-query extension
(3,3,5,9)   duplicate-terminal extension
(3,5,9,9)   duplicate-routing extension
```

so merely enlarging the query vocabulary from three to four creates no new irreducible gain mechanism in this scope.

### Five worlds create the first new deletion-minimal core

For

```text
5 worlds
2+3 target multiplicity
3 binary unit-cost queries
```

all `32^3=32,768` labeled tasks were classified exactly:

| `(C_A,C_F)` | labeled tasks |
|---|---:|
| unresolved | 17,928 |
| `(1,1)` | 5,768 |
| `(2,2)` | 6,336 |
| `(3,3)` | 720 |
| **`(2,3)`** | **2,016** |

Exactly 288 tasks lose strict gain after every one-world deletion. They form one symmetry orbit with unique signature

\[
\boxed{(7,28,42)}.
\]

A standard representative has

\[
T=(0,0,1,1,1)
\]

and queries

\[
(0,1,1,1,1),\quad
(0,1,0,0,1),\quad
(0,1,0,1,0).
\]

It has

\[
\boxed{C_A=2<C_F=3}
\]

and an optimal root with positive direct target information under uniform world weights,

\[
I(T;Q_{root})\approx0.0199730940\text{ bits}.
\]

Thus zero direct root information is not necessary even for deletion-minimal strict gain.

See:

- `theory/MINIMAL_STRICT_GAIN_NORMAL_FORM.md`
- `theory/FOUR_QUERY_EXTENSION_CLASSIFICATION.md`
- `theory/FIVE_WORLD_IRREDUCIBLE_NORMAL_FORM.md`

## Source-derived witnesses

For the registered MROD-style and PAYOFF-style routing abstractions:

```text
C_A = 2
C_F = C_U = U = 3
```

Under uniform represented worlds, the first routing observation has zero direct target information, while the full adaptive policy resolves the target. The best fixed information at budget 2 is 0.5 bit in both abstractions.

BALANCE supplies a negative control: under the current midpoint-reset span objective, branch labels change interval location but not the declared sufficient future-value state, so extra direction adaptivity has no gain at that step.

These are synthetic/conditional structural witnesses, not field empirical validation.

## Validation

The suite includes:

- direct-versus-incidence Bellman equivalence;
- complete 4,096-task minimal binary universe;
- complete 65,536-task four-query extension universe;
- complete 32,768-task five-world universe;
- complete 3,375-task multi-valued partition universe for pair-incidence sufficiency;
- complete 3,375-task multi-valued adaptive-compression universe;
- complete 900-task unequal-cost adaptive-compression grid;
- certificate and LP-gap controls;
- tampered proof and transport rejection;
- kernel, DAG, isomorphism, color-refinement and automorphism regressions; and
- exact normal-form iff classifiers.

CI runs on Python 3.10, 3.11, and 3.12 plus executable witness and certificate-ladder audits.

## Scope boundary

This repository does **not** claim:

- a new general theory of adaptive experimental design, Set Cover, Test Cover, graph isomorphism, color refinement, or group algorithms;
- that PAYOFF, MROD, and BALANCE are the same scientific model;
- that branch dependence alone is sufficient for adaptive gain;
- that zero direct target information is necessary or sufficient for gain;
- polynomial-time exact integer cover or graph canonicalization;
- that finite labeled-task counts are natural prevalence estimates;
- that finite synthetic controls are empirical evidence; or
- that target resolution licenses a biological report.

The current deterministic finite theory identifies which information can be safely discarded for fixed resolution, which must be retained for adaptive routing, and two exact state-local adaptive reductions—continuation equality and target-relevant refinement dominance—that preserve the Bellman optimum.

## Run

```bash
python -m pip install -e .
python -m pytest -q
python examples/audit_witnesses.py
python examples/audit_certificate_ladder.py
```
