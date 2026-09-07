# adaptive-gain

A finite structural theory of **when outcome-contingent measurement choice is strictly better than a fixed measurement bundle**.

The repository was extracted from a cross-repository comparison of:

- `zuizui0223/mrod` — an early observation can route the next assay;
- `zuizui0223/payoff` — an early payoff contrast can route the next architecture distance;
- `zuizui0223/balance` — under the current threshold-span objective, branch labels move interval location but not the sufficient future-value state, giving a no-routing control.

The scientific models remain owned by those source repositories. `adaptive-gain` abstracts only the finite decision structure.

## Core theorem

Let `W` be a finite represented hidden-world set, `T:W->labels` the target, and every query have a positive integer acquisition cost plus one deterministic outcome in every represented world.

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

For integer budget `B`, the exact adaptive-only resolution window is

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

and

\[
\boxed{
U-C_A=(C_F-C_A)+(C_U-C_F)+(U-C_U).
}
\]

Interpret these as

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
\text{external shortcut}.
}
\]

Bypass is therefore a discount, not a binary veto.

---

# Representation hierarchy

The main theoretical development is now a hierarchy of **what information may be forgotten for which objective**.

## 1. Full target-pair incidence preserves both costs

For every query and every pair of worlds with different targets, record whether the query separates that pair.

The full **identity-indexed** target-pair incidence, together with target labels and query costs, determines both exact costs:

\[
\boxed{
\text{full target-pair incidence}
\Longrightarrow
(C_A,C_F).
}
\]

For one query, cross-target nonseparation edges reconstruct every target-mixed outcome cell as a connected component. Target-pure cells are already resolved, so their internal same-target partition is irrelevant to guaranteed target resolution.

Implementation: `adaptive_gain/target_pair_incidence.py`.

See `theory/TARGET_PAIR_INCIDENCE_SUFFICIENCY.md`.

## 2. Aggressive fixed compression does not preserve adaptive geometry

Fixed resolution is a weighted cover of cross-target pairs. Pair-obligation dominance can reduce this to a much smaller fixed-side kernel.

But the unique four-world and deletion-minimal five-world strict-gain cores both reduce to the same inclusion-minimal fixed signature

\[
\boxed{(1,2,4)}
\]

while having different adaptive normal forms.

Thus

\[
\boxed{
\text{same minimal fixed obstruction}
\not\Rightarrow
\text{same adaptive routing geometry}.
}
\]

The fixed-side kernel is sufficient for `C_F`, not for adaptive continuation structure.

## 3. Adaptive-only state-local kernels preserve `C_A`

The adaptive side has exact state-local reductions that are intentionally stronger than the joint-safe global reductions below.

### Query continuation equality

If two queries induce the same family of target-mixed children at one Bellman state, one cheapest representative suffices.

### Query refinement dominance

For a current world set `A`, let `S_A(q)` be the active cross-target pairs separated by query `q`. If

\[
\boxed{S_A(q)\supseteq S_A(r),\qquad c(q)\le c(r),}
\]

then `q` safely dominates `r` at that state.

### Same-target world twins

Same-target worlds with identical future separation/nonseparation relations to every opposite-target world under all remaining queries can be represented by one world in unresolved continuation states.

Combining query refinement and world twins gives the adaptive two-sided kernel.

Implementations:

- `adaptive_gain/adaptive_safe_compression.py`
- `adaptive_gain/adaptive_world_twins.py`
- `adaptive_gain/adaptive_two_sided_kernel.py`

These reductions preserve `C_A`; they are not automatically licensed as fixed-bundle reductions.

## 4. Cost-only continuation bisimulation compresses adaptive value further

`adaptive_gain/continuation_bisimulation.py` recursively represents one mixed state by the **costs** of its productive actions and the set of recursively equivalent mixed child classes.

Outcome labels, pure branches, repeated child types, query names, and repeated action types may disappear.

If two states have the same continuation type,

\[
\boxed{
\operatorname{Type}(s)=\operatorname{Type}(t)
\Longrightarrow
V_A(s)=V_A(t).
}
\]

Across the checked finite universes, `43,614` tasks had zero adaptive-cost mismatches under this quotient.

But this quotient is **not** sufficient for `C_F`.

A registered pair of four-world tasks has the same cost-only recursive root class and `C_A=2` in both cases, but

\[
C_F=3\quad\text{versus}\quad C_F=2.
\]

The lost information is whether terminal actions in separate branches are the **same physical query resource** and can therefore be reused by one fixed bundle.

See `theory/CONTINUATION_BISIMULATION.md`.

## 5. Resource-labelled continuation preserves both `C_A` and `C_F`

`adaptive_gain/resource_continuation.py` restores the missing branch-crossing resource identity.

Each productive action keeps a persistent task-local query token:

\[
q\mapsto\left(c(q),\{\text{mixed child classes}\}\right).
\]

Distinct query tokens are not collapsed merely because they have the same local cost and continuation type.

The same quotient then supports two recursions:

```text
adaptive:
  choose a query separately at each state

fixed:
  replay the same selected query-token set through every branch
```

Therefore

\[
\boxed{
\text{resource-labelled continuation quotient}
\Longrightarrow
(C_A,C_F).
}
\]

Erasing the resource tokens reduces it to the cost-only quotient and recreates the registered fixed-cost collision. Thus query resource identity is demonstrably necessary for this joint comparator in some finite tasks.

See `theory/RESOURCE_LABELLED_CONTINUATION_QUOTIENT.md`.

## 6. Joint-safe global kernel before the resource quotient

Keeping every resource token is sufficient but not minimal. `adaptive_gain/joint_resource_kernel.py` applies only reductions that are globally safe for **both** objectives:

1. same-target world twins over the complete remaining query vocabulary;
2. global query refinement dominance:

\[
\boxed{S(q)\supseteq S(r),\qquad c(q)\le c(r).}
\]

The two reductions are iterated because removing a dominated query can create new world twins and vice versa.

This gives the current joint pipeline:

\[
\boxed{
\text{full task}
\to
\text{joint resource kernel}
\to
\text{resource-labelled continuation quotient}
\to
(C_A,C_F).
}
\]

The adaptive side may then use stronger state-local kernels when only `C_A` is needed.

See `theory/JOINT_RESOURCE_KERNEL.md`.

---

# Fixed-side certificates and proof compression

Strict gain can often be certified without first computing the exact numerical `C_F`:

```text
private-pair necessity
-> integral pair packing
-> fractional pair-cover dual
-> exact integer budget-infeasibility proof at B=C_A
-> exact fixed optimum only when its numerical value is needed
```

The fixed integer proof itself has an exact compression stack:

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

A proof verifier independently checks stored branches, budgets, transports, and symmetry receipts instead of trusting the generator's memoization or canonical hashes.

See the `theory/` notes on pair cover, packing, integer proof, kernelization, DAG compression, isomorphism, and symmetry pruning.

---

# Finite normal-form ladder

## Unique minimal 4-world / 3-query core

For

```text
4 worlds
T=(0,0,1,1)
3 binary unit-cost queries
```

all `16^3=4,096` tasks are classified exactly:

| `(C_A,C_F)` | tasks |
|---|---:|
| unresolved | 1,688 |
| `(1,1)` | 1,352 |
| `(2,2)` | 864 |
| **`(2,3)`** | **192** |

All 192 strict tasks are one symmetry orbit with canonical signature

\[
\boxed{(3,5,9)}.
\]

## Four queries add no new irreducible mechanism

For four balanced worlds and four binary unit-cost queries, all `16^4=65,536` tasks were enumerated. The 3,840 strict cases all have `(C_A,C_F)=(2,3)` and every one contains the unique three-query core after deleting at least one query.

## Five worlds create the first new deletion-minimal core

For

```text
5 worlds
2+3 target multiplicity
3 binary unit-cost queries
```

all `32^3=32,768` tasks are classified exactly. There are 2,016 strict tasks; exactly 288 lose strict gain after every one-world deletion and form one orbit with signature

\[
\boxed{(7,28,42)}.
\]

The standard core has

\[
\boxed{C_A=2<C_F=3}
\]

and an optimal root with positive direct target information under uniform represented-world weights,

\[
I(T;Q_{root})\approx0.0199730940\text{ bits}.
\]

So zero direct root information is not necessary even for deletion-minimal strict gain.

---

# Source-derived witnesses

For the registered MROD-style and PAYOFF-style routing abstractions:

```text
C_A = 2
C_F = C_U = U = 3
```

Under uniform represented worlds, the first routing observation has zero direct target information while the full adaptive policy resolves the target. The best fixed information at budget 2 is 0.5 bit in both abstractions.

BALANCE supplies a negative control: under the current midpoint-reset span objective, branch labels change interval location but not the declared sufficient future-value state, so extra direction adaptivity has no gain at that step.

These are synthetic/conditional structural witnesses, not field empirical validation.

---

# Validation and scope

The suite includes complete finite universes, seeded adverse controls, tampered-certificate rejection, independent verifiers, and Python 3.10/3.11/3.12 CI.

The repository does **not** claim:

- a new general theory of adaptive experimental design, Set Cover, bisimulation, or graph isomorphism;
- that PAYOFF, MROD, and BALANCE are the same scientific model;
- that branch dependence or zero direct information is sufficient/necessary for gain;
- polynomial-time exact optimization or canonicalization;
- that finite labeled-task frequencies are empirical prevalence estimates;
- that synthetic structural validation is field evidence; or
- that target resolution licenses a biological report.

The current deterministic theory instead separates the information needed for:

```text
adaptive value
fixed bundle reuse
their joint comparison
scientific report licensing
```

and keeps those claims distinct.

## Run

```bash
python -m pip install -e .
python -m pytest -q
python examples/audit_witnesses.py
python examples/audit_certificate_ladder.py
```
