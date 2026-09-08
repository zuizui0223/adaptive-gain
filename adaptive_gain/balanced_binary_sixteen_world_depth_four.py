"""Exact-balanced sixteen-world witness with (C_A,C_F)=(4,12).

The twelve registered queries are globally exact 8/8.  Their Hamming-1
private-pair forest has four components of sizes (2,3,4,7).  A depth-four
policy separates every private edge; assigning one target to each terminal
leaf therefore makes every private edge cross-target.  Consequently all twelve
queries are fixed-mandatory while the policy resolves adaptively in depth four.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class SixteenWorldDepthFourReceipt:
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    component_sizes: tuple[int, ...]
    all_queries_exactly_balanced: bool
    all_private_pairs_query_unique: bool
    all_private_pairs_cross_target: bool
    theorem_holds: bool
    scope: str = "exact_balanced_binary_sixteen_world_CA4_CF12"


def exact_balanced_sixteen_world_twelve_query_depth_four_task() -> FiniteTask:
    signatures = (
        "111111111111",
        "011111111111",
        "001111010000",
        "011111010000",
        "010111010000",
        "011011101000",
        "011111101000",
        "011101101000",
        "011110101000",
        "100000000111",
        "100000100111",
        "100000010111",
        "100000011111",
        "100000011011",
        "100000000101",
        "100000100110",
    )
    # Terminal leaves of one depth-four private-edge-separating policy are:
    # (0,12), (13), (11), (1,3), (4), (2), (6), (8), (7),
    # (10), (5,15), (9), (14).
    targets = (0, 3, 5, 3, 4, 10, 6, 8, 7, 11, 9, 2, 0, 1, 12, 10)

    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    rows = tuple(
        tuple(int(signatures[world][query]) for world in range(16))
        for query in range(12)
    )
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def sixteen_world_twelve_query_private_pairs() -> tuple[tuple[int, int], ...]:
    # Pair i differs only in q_i.  The resulting forest components have sizes
    # 2, 3, 4 and 7.
    return (
        (0, 1),
        (2, 3),
        (3, 4),
        (5, 6),
        (6, 7),
        (6, 8),
        (9, 10),
        (9, 11),
        (11, 12),
        (12, 13),
        (9, 14),
        (10, 15),
    )


def sixteen_world_depth_four_policy() -> tuple:
    """One explicit policy; tuple nodes are (query,left,right)."""
    leaf = lambda *worlds: ("leaf", tuple(worlds))
    return (
        7,
        (
            0,
            (8, (9, leaf(0, 12), leaf(13)), leaf(11)),
            (1, (2, leaf(1, 3), leaf(4)), leaf(2)),
        ),
        (
            3,
            (4, (5, leaf(6), leaf(8)), leaf(7)),
            (6, (11, leaf(10), leaf(5, 15)), (10, leaf(9), leaf(14))),
        ),
    )


def _policy_resolves(task: FiniteTask, policy: tuple) -> tuple[bool, int]:
    max_depth = 0

    def walk(node: tuple, active: tuple[int, ...], depth: int) -> bool:
        nonlocal max_depth
        if node[0] == "leaf":
            max_depth = max(max_depth, depth)
            return len({task.worlds[i].target for i in active}) <= 1
        query_index, left_node, right_node = node
        query = task.queries[query_index]
        left = tuple(i for i in active if query.outcomes[i] == 1)
        right = tuple(i for i in active if query.outcomes[i] == 0)
        if not left or not right:
            return False
        return walk(left_node, left, depth + 1) and walk(right_node, right, depth + 1)

    return walk(policy, tuple(range(len(task.worlds))), 0), max_depth


@lru_cache(maxsize=1)
def audit_exact_balanced_sixteen_world_depth_four() -> SixteenWorldDepthFourReceipt:
    task = exact_balanced_sixteen_world_twelve_query_depth_four_task()
    pairs = sixteen_world_twelve_query_private_pairs()

    balanced = all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 0 for outcome in query.outcomes) == 8
        and sum(outcome == 1 for outcome in query.outcomes) == 8
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

    policy_ok, policy_depth = _policy_resolves(task, sixteen_world_depth_four_policy())
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive is None or fixed is None:
        raise ArithmeticError("sixteen-world depth-four witness is unresolved")

    theorem = (
        balanced
        and unique
        and cross_target
        and policy_ok
        and policy_depth == 4
        and adaptive == 4
        and fixed == 12
    )
    if not theorem:
        raise ArithmeticError("sixteen-world depth-four witness audit failed")

    return SixteenWorldDepthFourReceipt(
        world_count=16,
        query_count=12,
        adaptive_cost=adaptive,
        fixed_cost=fixed,
        component_sizes=(2, 3, 4, 7),
        all_queries_exactly_balanced=balanced,
        all_private_pairs_query_unique=unique,
        all_private_pairs_cross_target=cross_target,
        theorem_holds=True,
    )
