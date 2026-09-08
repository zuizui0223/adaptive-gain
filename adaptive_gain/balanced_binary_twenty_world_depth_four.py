"""Exact-balanced twenty-world witness with (C_A,C_F)=(4,15).

The fifteen registered queries are globally exact 10/10. Their Hamming-1
private-pair forest has five components of sizes (1,2,3,6,8). A complete
binary depth-four policy uses all fifteen query labels exactly once and
separates every registered private edge. Therefore all fifteen queries are
fixed-mandatory while the task resolves adaptively in depth four.

Appending complementary all-zero/all-one world pairs preserves exact balance,
the same depth-four policy, and all original private pairs. Hence the same
(C_A,C_F)=(4,15) pair is attained for every even world count n>=20.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class TwentyWorldDepthFourReceipt:
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    component_sizes: tuple[int, ...]
    complete_tree_internal_nodes: int
    complete_tree_distinct_query_labels: int
    all_queries_exactly_balanced: bool
    all_private_pairs_query_unique: bool
    all_private_pairs_cross_target: bool
    theorem_holds: bool
    scope: str = "exact_balanced_binary_twenty_world_CA4_CF15"


def _task_from_signatures(signatures: tuple[str, ...], targets: tuple[int, ...]) -> FiniteTask:
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    query_count = len(signatures[0])
    rows = tuple(
        tuple(int(signatures[w][q]) for w in range(len(signatures)))
        for q in range(query_count)
    )
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def exact_balanced_twenty_world_fifteen_query_depth_four_task() -> FiniteTask:
    signatures = (
        "111111111111111",
        "111110001000101",
        "011110001000101",
        "000110001001010",
        "010110001001010",
        "001110001001010",
        "011110000110100",
        "011010000110100",
        "011010100110100",
        "011100000110100",
        "011100010110100",
        "011111000110100",
        "100001110001011",
        "100001111001011",
        "100001111011011",
        "100001111010011",
        "100001111010111",
        "100001110101011",
        "100001110101001",
        "100001110101000",
    )
    targets = (0, 8, 9, 11, 9, 10, 1, 5, 4, 3, 2, 0, 13, 11, 6, 7, 4, 12, 14, 15)
    return _task_from_signatures(signatures, targets)


def twenty_world_fifteen_query_private_pairs() -> tuple[tuple[int, int], ...]:
    return (
        (1, 2),
        (3, 4),
        (3, 5),
        (6, 7),
        (6, 9),
        (6, 11),
        (7, 8),
        (9, 10),
        (12, 13),
        (12, 17),
        (13, 14),
        (14, 15),
        (15, 16),
        (17, 18),
        (18, 19),
    )


def twenty_world_depth_four_policy() -> tuple:
    leaf = lambda *worlds: ("leaf", tuple(worlds))
    return (
        10,
        (
            3,
            (
                4,
                (5, leaf(0, 11), leaf(6)),
                (7, leaf(10), leaf(9)),
            ),
            (12, (6, leaf(8, 16), leaf(7)), (11, leaf(14), leaf(15))),
        ),
        (
            8,
            (1, (0, leaf(1), leaf(2, 4)), (2, leaf(5), leaf(3, 13))),
            (13, (9, leaf(17), leaf(12)), (14, leaf(18), leaf(19))),
        ),
    )


def _policy_resolves(task: FiniteTask, policy: tuple) -> tuple[bool, int, tuple[int, ...]]:
    labels: list[int] = []
    max_depth = 0

    def walk(node: tuple, active: tuple[int, ...], depth: int) -> bool:
        nonlocal max_depth
        if node[0] == "leaf":
            max_depth = max(max_depth, depth)
            return len({task.worlds[i].target for i in active}) <= 1
        query_index, left_node, right_node = node
        labels.append(query_index)
        query = task.queries[query_index]
        left = tuple(i for i in active if query.outcomes[i] == 1)
        right = tuple(i for i in active if query.outcomes[i] == 0)
        if not left or not right:
            return False
        return walk(left_node, left, depth + 1) and walk(right_node, right, depth + 1)

    ok = walk(policy, tuple(range(len(task.worlds))), 0)
    return ok, max_depth, tuple(labels)


def exact_balanced_depth_four_ceiling_witness(world_count: int) -> FiniteTask:
    """Pad the n=20 witness to every even n>=20."""
    if type(world_count) is not int or world_count < 20 or world_count % 2:
        raise ValueError("world_count must be an even integer at least 20")
    task = exact_balanced_twenty_world_fifteen_query_depth_four_task()
    while len(task.worlds) < world_count:
        worlds = list(task.worlds)
        zero_index = len(worlds)
        one_index = zero_index + 1
        # all-zero routes to the w19 terminal (target 15); all-one routes to
        # the (w0,w11) terminal (target 0).
        worlds.extend((World(f"pad_zero_{zero_index}", 15), World(f"pad_one_{one_index}", 0)))
        queries = tuple(
            Query(query.name, query.cost, query.outcomes + (0, 1))
            for query in task.queries
        )
        task = FiniteTask(tuple(worlds), queries)
    return task


@lru_cache(maxsize=1)
def audit_exact_balanced_twenty_world_depth_four() -> TwentyWorldDepthFourReceipt:
    task = exact_balanced_twenty_world_fifteen_query_depth_four_task()
    pairs = twenty_world_fifteen_query_private_pairs()
    balanced = all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 0 for outcome in query.outcomes) == 10
        and sum(outcome == 1 for outcome in query.outcomes) == 10
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

    policy_ok, policy_depth, labels = _policy_resolves(task, twenty_world_depth_four_policy())
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive is None or fixed is None:
        raise ArithmeticError("twenty-world depth-four witness is unresolved")
    theorem = (
        balanced
        and unique
        and cross_target
        and policy_ok
        and policy_depth == 4
        and len(labels) == 15
        and len(set(labels)) == 15
        and adaptive == 4
        and fixed == 15
    )
    if not theorem:
        raise ArithmeticError("twenty-world depth-four witness audit failed")
    return TwentyWorldDepthFourReceipt(
        world_count=20,
        query_count=15,
        adaptive_cost=adaptive,
        fixed_cost=fixed,
        component_sizes=(1, 2, 3, 6, 8),
        complete_tree_internal_nodes=len(labels),
        complete_tree_distinct_query_labels=len(set(labels)),
        all_queries_exactly_balanced=balanced,
        all_private_pairs_query_unique=unique,
        all_private_pairs_cross_target=cross_target,
        theorem_holds=True,
    )
