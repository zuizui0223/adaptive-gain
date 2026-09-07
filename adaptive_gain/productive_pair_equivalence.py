"""Equivalence of productive frontiers and minimal cross-target separator rows.

For a cross-target world pair (i,j), let S_ij be the set of queries on which the
pair differs.  Applying every query outside S_ij and following the common outcomes
of i,j reaches a mixed state whose productive query set is exactly S_ij.

Conversely every reachable mixed state contains a cross-target pair, and that
pair's separator set is contained in the state's productive set.  Therefore the
inclusion-minimal reachable productive sets are exactly the inclusion-minimal
cross-target separator sets.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import FiniteTask
from .productive_frontier import build_productive_frontier
from .target_pair_incidence import target_pair_incidence_task


@dataclass(frozen=True)
class ProductivePairEquivalenceReceipt:
    cross_target_pair_count: int
    distinct_pair_separator_set_count: int
    minimal_pair_separator_sets: tuple[int, ...]
    minimal_reachable_productive_sets: tuple[int, ...]
    frontiers_equal: bool
    scope: str = "minimal_reachable_productive_sets_equal_minimal_cross_target_separator_sets"


def _minimal_sets(masks: tuple[int, ...]) -> tuple[int, ...]:
    unique = tuple(sorted(set(masks)))
    return tuple(
        mask for i, mask in enumerate(unique)
        if not any(j != i and other & ~mask == 0 for j, other in enumerate(unique))
    )


def cross_target_pair_separator_sets(task: FiniteTask) -> tuple[int, ...]:
    incidence = target_pair_incidence_task(task)
    rows = []
    for pair_bit in range(len(incidence.cross_target_pairs)):
        query_mask = 0
        for q, separation in enumerate(incidence.query_separation_masks):
            if separation & (1 << pair_bit):
                query_mask |= 1 << q
        rows.append(query_mask)
    return tuple(rows)


def minimal_cross_target_separator_sets(task: FiniteTask) -> tuple[int, ...]:
    return _minimal_sets(cross_target_pair_separator_sets(task))


def productive_pair_equivalence_audit(task: FiniteTask) -> ProductivePairEquivalenceReceipt:
    rows = cross_target_pair_separator_sets(task)
    pair_minimal = _minimal_sets(rows)
    productive = build_productive_frontier(task).minimal_productive_sets
    return ProductivePairEquivalenceReceipt(
        len(rows),
        len(set(rows)),
        pair_minimal,
        productive,
        pair_minimal == productive,
    )
