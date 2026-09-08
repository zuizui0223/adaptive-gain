"""Constructive exact-balanced binary frontier at adaptive depth four.

This module records two explicit finite tasks found after closing the adaptive
Depth-3 envelope:

* n=12, m=8 with (C_A, C_F) = (4, 8),
* n=14, m=10 with (C_A, C_F) = (4, 10).

Every query is globally exact 50/50.  For each query q_i the registered task
contains a cross-target world pair that differs in q_i and in no other query,
so every query is fixed-mandatory.  Explicit depth-four policies give the
matching adaptive upper bound; the universal binary depth-three flattening
bound C_F<=7 gives the adaptive lower bound C_A>=4.

These are constructive lower bounds for the still-open sharp depth-four
function D_4(n)=max{C_F : C_A<=4} under exact balance.  No sharp claim for
D_4(12) or D_4(14) is made here.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class DepthFourWitnessReceipt:
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    ratio_numerator: int
    ratio_denominator: int
    all_queries_exactly_balanced: bool
    all_registered_private_pairs_query_unique: bool
    all_registered_private_pairs_cross_target: bool
    theorem_holds: bool


@dataclass(frozen=True)
class DepthFourConstructiveFrontierReceipt:
    twelve_world: DepthFourWitnessReceipt
    fourteen_world: DepthFourWitnessReceipt
    depth_three_flattening_cap: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_depth_four_constructive_frontier"


def _task_from_signatures(
    signatures: tuple[str, ...],
    targets: tuple[int, ...],
) -> FiniteTask:
    if len(signatures) != len(targets):
        raise ValueError("signature and target counts differ")
    query_count = len(signatures[0])
    if any(len(signature) != query_count for signature in signatures):
        raise ValueError("all signatures must have equal length")
    if any(set(signature) - {"0", "1"} for signature in signatures):
        raise ValueError("signatures must be binary strings")

    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    rows = tuple(
        tuple(int(signatures[world_index][query_index]) for world_index in range(len(signatures)))
        for query_index in range(query_count)
    )
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def exact_balanced_twelve_world_eight_query_depth_four_task() -> FiniteTask:
    """Exact-balanced witness with (C_A,C_F)=(4,8)."""
    signatures = (
        "00010111",
        "00101000",
        "00101001",
        "00111000",
        "01010111",
        "01011111",
        "10101000",
        "10101010",
        "11000110",
        "11010001",
        "11010101",
        "11100110",
    )
    # Targets are the terminal cells of the explicit policy
    # q0 -> q1/q2 -> q3/q4/q5/q6 -> q7.
    targets = (3, 0, 1, 2, 4, 5, 9, 10, 7, 6, 8, 10)
    return _task_from_signatures(signatures, targets)


def twelve_world_eight_query_private_pairs() -> tuple[tuple[int, int], ...]:
    # Pair i differs only in q_i.
    return (
        (1, 6),
        (0, 4),
        (8, 11),
        (1, 3),
        (4, 5),
        (9, 10),
        (6, 7),
        (1, 2),
    )


def exact_balanced_fourteen_world_ten_query_depth_four_task() -> FiniteTask:
    """Exact-balanced witness with (C_A,C_F)=(4,10)."""
    signatures = (
        "0001011101",
        "0010100010",
        "0010100110",
        "0011100010",
        "0101011101",
        "0101111101",
        "1010100010",
        "1010101010",
        "1100011001",
        "1101000100",
        "1101010100",
        "1110011001",
        "0101011111",
        "1010100011",
    )
    # Terminal classes of the explicit depth-four policy documented in
    # theory/EXACT_BALANCED_BINARY_DEPTH_FOUR_FRONTIER.md.
    targets = (2, 0, 1, 2, 3, 5, 6, 8, 10, 9, 10, 11, 4, 7)
    return _task_from_signatures(signatures, targets)


def fourteen_world_ten_query_private_pairs() -> tuple[tuple[int, int], ...]:
    # Pair i differs only in q_i.
    return (
        (1, 6),
        (0, 4),
        (8, 11),
        (1, 3),
        (4, 5),
        (9, 10),
        (6, 7),
        (1, 2),
        (4, 12),
        (6, 13),
    )


def _audit_witness(task: FiniteTask, private_pairs: tuple[tuple[int, int], ...]) -> DepthFourWitnessReceipt:
    if len(private_pairs) != len(task.queries):
        raise ArithmeticError("one registered private pair is required per query")

    half = len(task.worlds) // 2
    balanced = all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 0 for outcome in query.outcomes) == half
        and sum(outcome == 1 for outcome in query.outcomes) == half
        for query in task.queries
    )

    unique = True
    cross_target = True
    for query_index, (left, right) in enumerate(private_pairs):
        separating = tuple(
            index
            for index, query in enumerate(task.queries)
            if query.outcomes[left] != query.outcomes[right]
        )
        unique = unique and separating == (query_index,)
        cross_target = cross_target and task.worlds[left].target != task.worlds[right].target

    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive is None or fixed is None:
        raise ArithmeticError("registered depth-four witness is unresolved")

    expected_fixed = len(task.queries)
    theorem = (
        balanced
        and unique
        and cross_target
        and adaptive == 4
        and fixed == expected_fixed
        and fixed > 7
    )
    if not theorem:
        raise ArithmeticError("exact-balanced depth-four witness audit failed")

    return DepthFourWitnessReceipt(
        world_count=len(task.worlds),
        query_count=len(task.queries),
        adaptive_cost=adaptive,
        fixed_cost=fixed,
        ratio_numerator=fixed,
        ratio_denominator=adaptive,
        all_queries_exactly_balanced=balanced,
        all_registered_private_pairs_query_unique=unique,
        all_registered_private_pairs_cross_target=cross_target,
        theorem_holds=True,
    )


@lru_cache(maxsize=1)
def audit_exact_balanced_depth_four_constructive_frontier() -> DepthFourConstructiveFrontierReceipt:
    twelve = _audit_witness(
        exact_balanced_twelve_world_eight_query_depth_four_task(),
        twelve_world_eight_query_private_pairs(),
    )
    fourteen = _audit_witness(
        exact_balanced_fourteen_world_ten_query_depth_four_task(),
        fourteen_world_ten_query_private_pairs(),
    )
    theorem = (
        twelve.theorem_holds
        and fourteen.theorem_holds
        and (twelve.adaptive_cost, twelve.fixed_cost) == (4, 8)
        and (fourteen.adaptive_cost, fourteen.fixed_cost) == (4, 10)
    )
    if not theorem:
        raise ArithmeticError("depth-four constructive frontier audit failed")
    return DepthFourConstructiveFrontierReceipt(
        twelve_world=twelve,
        fourteen_world=fourteen,
        depth_three_flattening_cap=7,
        theorem_holds=True,
    )
