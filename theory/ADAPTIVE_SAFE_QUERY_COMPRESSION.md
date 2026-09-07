# Adaptive-safe target-relevant query compression

The full identity-indexed target-pair incidence is sufficient to recover the exact deterministic adaptive target-resolution cost.  This note asks a narrower question:

> Can the remaining query vocabulary be compressed **state by state** without changing the Bellman optimum?

Yes.  Two exact rules are now available: continuation equality and the stronger **target-relevant refinement dominance**.

## State-local target-relevant structure

Fix a current represented-world set `A` and an unmeasured query `q`.

Let

\[
\mathcal M_A(q)
\]

be the family of outcome cells of `q` restricted to `A` that contain at least two target values.  These are exactly the target-mixed children reconstructed by the full target-pair incidence.  Target-pure outcome cells are omitted because they terminate with continuation cost zero.

Equivalently, let

\[
S_A(q)
\]

be the set of identity-indexed cross-target pairs inside `A` that `q` separates.

Because target-mixed outcome cells are the connected components of cross-target **nonseparation** edges, a larger separation set yields a target-relevantly finer unresolved partition.

## Theorem 1: continuation equality

If

\[
\boxed{\mathcal M_A(q)=\mathcal M_A(r)},
\]

then every unresolved child in the common family is an outcome cell of both queries.  Hence both queries are constant on every future target-mixed child reached after either one is acquired.

If also

\[
c(q)\le c(r),
\]

then `r` is safely removable at state `A`.  One cheapest representative of the equivalence class is sufficient.  Equal-cost members are interchangeable; using the lowest declared index is only a deterministic tie convention.

## Theorem 2: target-relevant refinement dominance

The equality condition is stronger than necessary.

Suppose

\[
\boxed{S_A(q)\supseteq S_A(r)}
\]

and

\[
\boxed{c(q)\le c(r)}.
\]

Then every target-mixed outcome cell of `q` is contained in one target-mixed outcome cell of `r`.  In other words, `q` is at least as fine as `r` on the part of the state that can still require continuation.

After observing `q`, query `r` is constant on every unresolved `q`-child.  Therefore any policy rooted at `r` can be simulated after using `q` by starting its continuation separately on the finer `q`-children, never paying more at the root and never needing `r` later.

Thus

\[
\boxed{
S_A(q)\supseteq S_A(r),\ c(q)\le c(r)
\Longrightarrow
q\text{ safely dominates }r\text{ at }A.
}
\]

This strictly generalizes continuation equality.  Equal separation masks are the tie case; strict supersets allow one query to replace a genuinely coarser query.

For equal cost and equal separation mask, the implementation keeps the lowest declared query index so the dominance relation is deterministic and acyclic.

## Why pure-branch differences do not matter

Two continuation-equivalent queries may partition target-pure worlds differently.  This does not invalidate either theorem.

Those cells already contain one target value, so their continuation cost is zero.  Only target-mixed cells contribute to the Bellman maximum.  The compression therefore preserves the target-relevant continuation structure while discarding distinctions that are decision-irrelevant for this objective.

## No-progress queries

If

\[
\mathcal M_A(q)=\{A\},
\]

then `q` leaves the entire unresolved state in one target-mixed child and has no target-relevant pure exit.  It cannot reduce target-resolution uncertainty and may be skipped.

Equivalently, its active cross-target separation mask on `A` is empty.

## What this is not

This is **not** the fixed-side pair-obligation dominance rule.

Fixed cover may safely delete an obligation whose separator set contains another obligation's separator set.  That operation changes the identity-indexed pair system and can lose world-partition geometry needed by an adaptive policy.

The adaptive rule instead compares **query columns on the full active cross-target incidence** and removes a query only when another query is target-relevantly at least as informative at no greater cost.

The current representation ladder is therefore

\[
\boxed{
\text{full world/outcome model}
\to
\text{full identity-indexed target-pair incidence}
\to
\begin{cases}
\text{state-local adaptive refinement frontier},\\
\text{more aggressive fixed-cover kernel}.
\end{cases}
}
\]

## Implementation

`adaptive_gain/adaptive_safe_compression.py` exposes two layers.

Equality layer:

- `target_relevant_query_classes(...)`
- `adaptive_safe_compressed_minimum_resolution(...)`

Refinement-dominance layer:

- `target_relevant_refinement_dominance(...)`
- `adaptive_refinement_compressed_minimum_resolution(...)`

The refinement solver evaluates only nondominated query roots.  When query `q` is selected, every query that `q` safely dominates at the current state is removed from each unresolved child, because it is constant there.

Both receipts include an internal equality audit against the original direct Bellman solver.

## Validation

The regression suite includes:

1. every set partition of four worlds (`15` partitions) assigned to three unit-cost queries:

\[
15^3=3375
\]

complete deterministic multi-valued tasks;

2. every pair of those partitions with query costs in `{1,2}`:

\[
15^2\times2^2=900
\]

unequal-cost tasks;

3. a control where two queries have the same target-mixed child but different partitions of already-resolved pure worlds;

4. an explicit **strict refinement** control where the cheaper query separates a proper superset of the cross-target pairs separated by the expensive query;

5. equal-cost interchangeability; and

6. no-progress query classes.

Both compressed solvers are required to match the original direct Bellman solver exactly in `C_A` on every exhaustive case.

## Scope boundary

The theorems are for deterministic finite guaranteed target resolution with additive positive query costs and worst-path cost.  They do not by themselves extend to expected loss, noisy likelihood observations, randomized policies, calibration-changing actions, or information-valued objectives.  In those settings, a finer deterministic support partition need not dominate a coarser observation with a different likelihood or information structure.
