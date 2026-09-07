# Exact adaptive two-sided Bellman kernel

The adaptive side now has safe state-local reductions on both axes of the full identity-indexed target-pair incidence representation.

## World side

At Bellman state `(A,R)`, same-target worlds are collapsed when they have identical cross-target separation profiles against every opposite-target world in `A` for every remaining query in `R`.

Every target-mixed future outcome cell contains either the whole twin class or none of it, so one representative per class preserves deterministic continuation value exactly.

## Query side

On the resulting world quotient, query `q` safely dominates `r` when

\[
S_A(q)\supseteq S_A(r)
\]

and

\[
c(q)\le c(r),
\]

where `S_A(q)` is the active identity-indexed set of cross-target pairs separated by `q`.

Only the nondominated query frontier must be evaluated.  After a dominating query is acquired, the queries it dominates are constant on every unresolved finer child and may be removed there.

## Composition theorem

Both operations are individually Bellman-value preserving.

The world quotient preserves the target-mixed child system for every remaining query.  Query refinement dominance then preserves the minimum root action value on that quotient.  After one representative query is selected, each target-mixed child is again quotiented using the smaller remaining vocabulary before recursion.

Therefore the recursive composition preserves the direct deterministic worst-path optimum:

\[
\boxed{
C_A^{\rm two-sided}=C_A^{\rm direct}.
}
\]

The order used by the implementation is

```text
current world state
-> recompute same-target world twins
-> keep one representative per twin class
-> compute target-relevant nondominated query frontier
-> acquire one frontier query
-> remove that query and its safely dominated queries
-> form target-mixed children
-> recompute world twins in every child
-> recurse
```

This is deliberately different from the fixed-side two-sided cover kernel.  The fixed kernel deletes redundant pair obligations and dominated query columns to preserve `C_F`.  The adaptive kernel preserves the Bellman target-mixed continuation system instead.

## Implementation

`adaptive_gain/adaptive_two_sided_kernel.py` exposes

- `AdaptiveTwoSidedKernelReceipt`
- `adaptive_two_sided_kernel_minimum_resolution(...)`

The receipt records:

- exact minimum worst-path cost;
- selected optimal representative root queries;
- canonical Bellman state count;
- world quotient calls and collapsed world occurrences;
- maximum world collapse at one state;
- raw query candidate occurrences;
- evaluated nondominated query occurrences;
- refinement-dominated query occurrences;
- no-progress query occurrences; and
- an internal direct-solver equality audit.

All occurrence counts are search-computation diagnostics, not empirical frequencies.

## Validation

The complete four-world arbitrary-partition universe is used again:

\[
15^3=3375
\]

three-query deterministic tasks with unit costs.

Every two-sided-kernel result is required to match the original direct Bellman solver exactly in `C_A`.

A separate control requires both sides to act in the same problem: a routing query creates a child where same-target worlds become twins, while another cheap query strictly target-relevantly refines an expensive query.

## Current representation ladder

The finite deterministic target-resolution layer can now be written as

\[
\boxed{
\text{full world/outcome model}
\to
\text{full identity-indexed target-pair incidence}
\to
\begin{cases}
\text{adaptive two-sided Bellman kernel},\\
\text{fixed weighted-cover kernel}.
\end{cases}
}
\]

The split occurs only after the full incidence representation.  The two downstream kernels answer different optimization problems and should not be conflated.

## Scope boundary

The composition theorem is for finite deterministic exact target resolution with positive additive query costs and worst-path objective.  In a noisy, weighted, information-valued, or calibration-changing problem, collapsing same-support worlds or replacing a coarser experiment by a finer deterministic partition may change likelihood mass, expected utility, or future calibration state.  Those extensions require separate criteria.
