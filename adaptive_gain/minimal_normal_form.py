"""Canonical normal form for the minimal 4-world / 3-binary-query universe.

In the balanced two-target setting with two worlds per target, three labeled
unit-cost binary queries are the smallest vocabulary that can show strict
worst-path adaptive cost gain. Exhaustive classification shows that every strict
case is one symmetry orbit. This module exposes the symmetry-invariant signature
and one canonical representative; the exhaustive iff check lives in tests.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product

from .core import FiniteTask, Query, World, adaptive_gain_receipt


MINIMAL_STRICT_GAIN_SIGNATURE = (3, 5, 9)


@dataclass(frozen=True)
class MinimalNormalFormReceipt:
    canonical_separator_signature: tuple[int, int, int]
    matches_unique_strict_gain_normal_form: bool
    adaptive_cost: int | None
    fixed_cost: int | None
    exact_strict_gain: bool
    classification_agrees_with_exact_solver: bool
    scope: str = "four_world_two_plus_two_target_three_binary_unit_cost_queries"


def _validate_minimal_scope(task: FiniteTask) -> None:
    if len(task.worlds) != 4 or len(task.queries) != 3:
        raise ValueError("minimal normal form requires exactly four worlds and three queries")
    multiplicities: dict[object, int] = {}
    for world in task.worlds:
        multiplicities[world.target] = multiplicities.get(world.target, 0) + 1
    if sorted(multiplicities.values()) != [2, 2]:
        raise ValueError("target multiplicities must be exactly 2+2")
    if any(query.cost != 1 for query in task.queries):
        raise ValueError("minimal normal form requires unit query costs")
    for query in task.queries:
        if len(set(query.outcomes)) > 2:
            raise ValueError("minimal normal form requires binary-or-constant query outcomes")


def _world_symmetries(task: FiniteTask):
    """Permutations preserving the target equivalence relation, including block swap."""
    targets = tuple(world.target for world in task.worlds)
    return tuple(
        p
        for p in permutations(range(4))
        if all(
            (targets[i] == targets[j]) == (targets[p[i]] == targets[p[j]])
            for i in range(4)
            for j in range(4)
        )
    )


def _separator_mask(outcomes) -> int:
    # Canonical positions 0,1 share one target; 2,3 share the other.
    cross_pairs = ((0, 2), (0, 3), (1, 2), (1, 3))
    mask = 0
    for bit, (i, j) in enumerate(cross_pairs):
        if outcomes[i] != outcomes[j]:
            mask |= 1 << bit
    return mask


def canonical_minimal_separator_signature(task: FiniteTask) -> tuple[int, int, int]:
    """Quotient world symmetries, query order and binary outcome relabeling.

    Query outcome flips need no explicit enumeration because pair-separation
    masks depend only on equality versus inequality of outcomes.
    """
    _validate_minimal_scope(task)
    representatives = []
    for permutation in _world_symmetries(task):
        masks = []
        for query in task.queries:
            transformed = tuple(query.outcomes[permutation[i]] for i in range(4))
            masks.append(_separator_mask(transformed))
        representatives.append(tuple(sorted(masks)))
    return min(representatives)


def minimal_strict_gain_standard_task() -> FiniteTask:
    """One canonical representative of the unique minimal strict-gain orbit."""
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    return FiniteTask(
        worlds,
        (
            Query("q_left", 1, (0, 0, 1, 0)),
            Query("q_route", 1, (0, 1, 1, 0)),
            Query("q_right", 1, (0, 1, 1, 1)),
        ),
    )


def minimal_normal_form_receipt(task: FiniteTask) -> MinimalNormalFormReceipt:
    signature = canonical_minimal_separator_signature(task)
    predicted = signature == MINIMAL_STRICT_GAIN_SIGNATURE
    exact = adaptive_gain_receipt(task)
    return MinimalNormalFormReceipt(
        signature,
        predicted,
        exact.adaptive_cost,
        exact.fixed_cost,
        exact.strict_adaptive_gain,
        predicted == exact.strict_adaptive_gain,
    )


def standard_raw_symmetry_orbit_size() -> int:
    """Count labeled binary query maps in the standard form's declared symmetry orbit."""
    task = minimal_strict_gain_standard_task()
    raw = set()
    for world_permutation in _world_symmetries(task):
        transformed = tuple(
            tuple(query.outcomes[world_permutation[i]] for i in range(4))
            for query in task.queries
        )
        for query_permutation in permutations(range(3)):
            ordered = tuple(transformed[i] for i in query_permutation)
            for flips in product((0, 1), repeat=3):
                flipped = tuple(
                    tuple((1 - value) if flips[q] else value for value in ordered[q])
                    for q in range(3)
                )
                raw.add(flipped)
    return len(raw)
