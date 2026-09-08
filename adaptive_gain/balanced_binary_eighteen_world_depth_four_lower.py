"""Exact-balanced eighteen-world witness with (C_A,C_F)=(4,13).

The thirteen queries are globally exact 9/9.  Each query owns a Hamming-1
cross-target private pair, so every query is fixed-mandatory.  The registered
private-pair forest has five components of sizes (3,3,4,4,4), and an explicit
depth-four policy separates all thirteen private edges.

Because a binary adaptive policy of depth at most three flattens to at most
seven distinct queries, C_F=13 forces C_A>=4.  Hence the explicit policy is
sharp for this task and the exact cost pair is (4,13).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .core import FiniteTask, Query, World


@dataclass(frozen=True)
class EighteenWorldDepthFourLowerReceipt:
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    component_sizes: tuple[int, ...]
    all_queries_exactly_balanced: bool
    all_private_pairs_query_unique: bool
    all_private_pairs_cross_target: bool
    policy_resolves: bool
    policy_depth: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_eighteen_world_CA4_CF13"


def exact_balanced_eighteen_world_thirteen_query_depth_four_task() -> FiniteTask:
    """Return the registered exact-balanced witness with (C_A,C_F)=(4,13)."""
    one_sides = (
        (0, 6, 7, 8, 9, 10, 11, 12, 13),
        (0, 2, 3, 4, 5, 6, 7, 8, 9),
        (0, 1, 2, 4, 5, 6, 7, 8, 9),
        (0, 1, 2, 3, 4, 6, 7, 8, 9),
        (0, 1, 2, 3, 4, 5, 6, 8, 9),
        (0, 1, 2, 6, 7, 10, 11, 12, 13),
        (0, 1, 2, 3, 4, 5, 6, 7, 9),
        (0, 1, 2, 3, 4, 5, 11, 12, 13),
        (0, 1, 2, 6, 7, 8, 9, 10, 12),
        (0, 1, 2, 3, 4, 5, 10, 11, 12),
        (0, 1, 2, 3, 4, 5, 14, 16, 17),
        (0, 1, 2, 6, 7, 8, 9, 15, 16),
        (0, 1, 2, 3, 4, 5, 14, 15, 16),
    )
    targets = (0, 1, 2, 3, 2, 4, 0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 14)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    rows = tuple(
        tuple(1 if world in side else 0 for world in range(18))
        for side in one_sides
    )
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def eighteen_world_thirteen_query_private_pairs() -> tuple[tuple[int, int], ...]:
    """Private pair i differs only in q_i."""
    return (
        (0, 2),
        (1, 2),
        (3, 4),
        (4, 5),
        (7, 6),
        (6, 9),
        (8, 9),
        (10, 12),
        (12, 11),
        (11, 13),
        (15, 16),
        (16, 14),
        (14, 17),
    )


def eighteen_world_depth_four_policy() -> tuple:
    """One explicit policy; internal nodes are (query, one-branch, zero-branch)."""
    leaf = ("leaf",)
    return (
        0,
        (
            1,
            (5, (4, leaf, leaf), (6, leaf, leaf)),
            (8, (7, leaf, leaf), (9, leaf, leaf)),
        ),
        (
            1,
            (2, (3, leaf, leaf), leaf),
            (11, (10, leaf, leaf), (12, leaf, leaf)),
        ),
    )


def _policy_resolves(task: FiniteTask, policy: tuple) -> tuple[bool, int]:
    max_depth = 0

    def walk(node: tuple, active: tuple[int, ...], depth: int) -> bool:
        nonlocal max_depth
        if node[0] == "leaf":
            max_depth = max(max_depth, depth)
            return len({task.worlds[i].target for i in active}) <= 1
        query_index, one_node, zero_node = node
        query = task.queries[query_index]
        one = tuple(i for i in active if query.outcomes[i] == 1)
        zero = tuple(i for i in active if query.outcomes[i] == 0)
        if not one or not zero:
            return False
        return walk(one_node, one, depth + 1) and walk(zero_node, zero, depth + 1)

    return walk(policy, tuple(range(len(task.worlds))), 0), max_depth


@lru_cache(maxsize=1)
def audit_exact_balanced_eighteen_world_depth_four_lower() -> EighteenWorldDepthFourLowerReceipt:
    task = exact_balanced_eighteen_world_thirteen_query_depth_four_task()
    pairs = eighteen_world_thirteen_query_private_pairs()

    balanced = all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 0 for outcome in query.outcomes) == 9
        and sum(outcome == 1 for outcome in query.outcomes) == 9
        for query in task.queries
    )

    unique = True
    cross_target = True
    for query_index, (left, right) in enumerate(pairs):
        separating = tuple(
            index
            for index, query in enumerate(task.queries)
            if query.outcomes[left] != query.outcomes[right]
        )
        unique = unique and separating == (query_index,)
        cross_target = cross_target and task.worlds[left].target != task.worlds[right].target

    policy_ok, policy_depth = _policy_resolves(task, eighteen_world_depth_four_policy())

    # All 13 queries are fixed-mandatory by their cross-target private pairs,
    # and there are exactly 13 declared queries, so C_F=13.  The policy gives
    # C_A<=4.  A binary depth-three tree contains at most seven internal query
    # occurrences, so C_F=13 rules out C_A<=3.  Hence C_A=4.
    theorem = (
        len(task.worlds) == 18
        and len(task.queries) == 13
        and balanced
        and unique
        and cross_target
        and policy_ok
        and policy_depth == 4
    )
    if not theorem:
        raise ArithmeticError("eighteen-world depth-four lower witness audit failed")

    return EighteenWorldDepthFourLowerReceipt(
        world_count=18,
        query_count=13,
        adaptive_cost=4,
        fixed_cost=13,
        component_sizes=(3, 3, 4, 4, 4),
        all_queries_exactly_balanced=True,
        all_private_pairs_query_unique=True,
        all_private_pairs_cross_target=True,
        policy_resolves=True,
        policy_depth=4,
        theorem_holds=True,
    )
