# Adaptive-safe target-relevant world twin quotient

The deterministic adaptive state can be compressed on the **world side** as well as the query side.

## State-local twin relation

Fix a current represented-world set `A` and remaining query vocabulary `R`.

Two worlds `u,v in A` are target-relevant twins when:

1. they have the same target value, and
2. for every remaining query `q in R` and every currently represented world `w` with a different target,

\[
\boxed{
\mathbf 1[q(u)\ne q(w)]
=
\mathbf 1[q(v)\ne q(w)].
}
\]

This definition uses only the full identity-indexed cross-target pair incidence.

## Mixed-cell lemma

Let `q` be any remaining query. If a target-mixed `q` outcome cell contains `u`, then it also contains every target-relevant twin `v` of `u`.

Proof: because the cell is target-mixed, choose `w` in the cell with target different from `T(u)`. Then `q(u)=q(w)`, so the cross-target separation bit for `(u,w)` is zero. Twin equality forces the bit for `(v,w)` to be zero as well, hence

\[
q(v)=q(w)=q(u).
\]

Thus `v` is in the same outcome cell. The converse is symmetric.

Therefore every unresolved child is a union of whole twin classes.

If one query puts twins in different outcome cells, neither cell can be target-mixed; those branches are target-pure and terminate immediately.

## Quotient theorem

One representative per target-relevant twin class is sufficient for deterministic worst-path target resolution.

Collapsing a twin class does not change any target-mixed child reachable under any remaining query. Target-pure branch multiplicity is irrelevant because those branches have continuation cost zero.

Hence the adaptive Bellman recursion is preserved exactly.

For the fixed side, twin worlds generate duplicate cross-target pair obligations: for every opposite-target world, the separator row for one twin is identical to the row for the other. Therefore removing duplicate twins also preserves `C_F`.

So at the root,

\[
\boxed{
(C_A,C_F)_{m original}
=
(C_A,C_F)_{m twin\ quotient}.
}
\]

## Why the quotient is dynamic

Twinhood can become coarser later in a policy.

A routed-away opposite-target world can be the only world that distinguished two same-target worlds' future cross-target incidence. Once that opposite world exits through a target-pure branch, the two surviving worlds can become twins inside the remaining mixed child.

Likewise, consuming queries can remove distinctions from the remaining-query signature.

Therefore `adaptive_world_twin_compressed_minimum_resolution(...)` recomputes twin classes at every Bellman state rather than applying only one root quotient.

## Implementation

`adaptive_gain/adaptive_world_twins.py` exposes:

- `TargetRelevantWorldTwinClass`
- `target_relevant_world_twin_classes(...)`
- `target_relevant_world_twin_representative_mask(...)`
- `static_target_relevant_world_twin_quotient(...)`
- `adaptive_world_twin_compressed_minimum_resolution(...)`

The dynamic receipt reports the canonical state count, number of quotient calls, total world occurrences collapsed across reached states, maximum collapse at one state, and an internal equality audit against the direct adaptive solver.

`world_occurrences_collapsed` is a search-computation count, not a count of unique biological worlds.

## Validation

The regression suite requires exact agreement with the direct Bellman solver for all

\[
15^3=3375
\]

triples of arbitrary set partitions of four balanced worlds.

Additional controls verify:

- same-target worlds may have distinct outcomes on a query and still be twins when those distinctions occur only in target-pure cells;
- a static root quotient preserves both `C_A` and `C_F`; and
- worlds that are not twins at the root can become twins only after an opposite-target world routes away.

## Relationship to query compression

The adaptive-safe representation now has reductions on both axes of the full target-pair incidence matrix:

```text
world rows:
  same-target future-incidence twins -> one representative

query columns:
  target-relevant refinement dominance -> nondominated frontier
```

These are distinct from the more aggressive fixed-cover kernel, which may delete pair obligations that are redundant for `C_F` but still encode adaptive routing geometry.

## Scope boundary

This theorem is for finite deterministic guaranteed target resolution with positive additive query costs and worst-path objective. It does not automatically extend to weighted empirical frequencies, noisy likelihoods, expected loss, information-valued objectives, or calibration actions. In those settings, two duplicated support states may carry different probability mass or downstream utility even when their deterministic target-relevant incidence matches.
