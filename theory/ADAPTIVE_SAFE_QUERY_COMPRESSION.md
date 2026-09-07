# Adaptive-safe target-relevant query compression

The full identity-indexed target-pair incidence is sufficient to recover the exact deterministic adaptive target-resolution cost.  This note asks a narrower question:

> Can the remaining query vocabulary be compressed **state by state** without changing the Bellman optimum?

Yes, under an exact continuation-equivalence condition.

## State-local target-relevant continuation family

Fix a current represented-world set `A` and an unmeasured query `q`.

Let

\[
\mathcal M_A(q)
\]

be the family of outcome cells of `q` restricted to `A` that contain at least two target values.  These are exactly the target-mixed children reconstructed by the full target-pair incidence.  Target-pure outcome cells are omitted because they terminate with continuation cost zero.

## Exact equivalence theorem

Suppose two remaining queries `q` and `r` satisfy

\[
\boxed{\mathcal M_A(q)=\mathcal M_A(r).}
\]

Then every target-mixed child in this common family is an outcome cell of both queries.  Hence both `q` and `r` are constant on every future mixed child reached after either query is acquired.

Therefore, once one member of the class is acquired at state `A`, the other members have zero target-resolution value in every unresolved child of that branch.

If additionally

\[
c(q)\le c(r),
\]

then replacing `r` by `q` cannot increase worst-path cost.  Thus `r` is safely removable from the Bellman candidate set at `A`.

For an equivalence class

\[
E=\{q:\mathcal M_A(q)=M\},
\]

one minimum-cost representative is sufficient.  Equal-cost members are interchangeable for the declared worst-path target-resolution objective; choosing the lowest declared index is only a deterministic tie convention.

## Why pure-branch differences do not matter

Two equivalent queries may partition target-pure worlds differently.  This does not invalidate the theorem.

Those cells already contain one target value, so their continuation cost is zero.  Only the target-mixed cells contribute to the Bellman maximum.  The compression therefore preserves the target-relevant continuation structure while discarding distinctions that are decision-irrelevant for this objective.

## No-progress classes

If

\[
\mathcal M_A(q)=\{A\},
\]

then `q` leaves the entire unresolved state in one target-mixed child and has no target-relevant pure exit.  It cannot reduce target-resolution uncertainty and may be skipped.

## What this is not

This is **not** fixed pair-obligation dominance.

Fixed cover may safely delete an obligation whose separator set contains another obligation's separator set.  That operation can lose the world-partition geometry needed by an adaptive policy.

The current representation ladder is therefore

\[
\boxed{
\text{full world/outcome model}
\to
\text{full identity-indexed target-pair incidence}
\to
\text{state-local target-relevant continuation classes}
}
\]

for the adaptive side, while the fixed side may continue to a more aggressive inclusion-minimal cover kernel.

## Implementation

`adaptive_gain/adaptive_safe_compression.py` exposes:

- `target_relevant_query_classes(...)`
- `adaptive_safe_compressed_minimum_resolution(...)`

The compressed solver groups remaining queries by exact mixed-child family, evaluates one cheapest representative per class, removes the entire class from mixed recursive children after selection, and skips no-progress classes.

The receipt reports:

- exact compressed minimum worst-path cost;
- selected representative optimal roots;
- search-state count;
- raw query candidate occurrences;
- representative query occurrences evaluated;
- equivalent query occurrences pruned;
- no-progress occurrences skipped; and
- an internal direct-solver equality audit.

## Validation

The regression suite includes:

1. every set partition of four worlds (`15` partitions) assigned to three unit-cost queries:

\[
15^3=3375
\]

complete deterministic multi-valued tasks;

2. every pair of those partitions with query costs in `{1,2}`:

\[
15^2\times 2^2=900
\]

unequal-cost tasks;

3. an explicit control where two queries have the same mixed child but different partitions of already-resolved pure worlds;

4. an equal-cost interchangeability control; and

5. a no-progress class control.

Every case is required to match the original direct Bellman solver exactly in `C_A`.

## Scope boundary

The theorem is for deterministic finite guaranteed target resolution with additive positive query costs and worst-path cost.  It does not by itself extend to expected loss, noisy likelihood observations, randomized policies, calibration-changing actions, or information-valued objectives.  In those settings, two observations with the same deterministic mixed support may have different continuation distributions or information value.
