"""Exact-balanced 22-world witness with (C_A,C_F)=(5,17).

Start from the certified 20-world/15-query depth-four ceiling witness.  Worlds
w6 and w13 have complementary signatures on those 15 queries.  Duplicate those
two signatures as w20 and w21.  Therefore every old query remains exactly
11/11 balanced.

Add q15 so that (w6,w20) differs only in q15 and q16 so that (w13,w21)
differs only in q16.  The new queries are also exactly 11/11 balanced and are
constant across every old registered private edge.  Thus all seventeen queries
have query-unique cross-target private pairs and are fixed-mandatory.

The old depth-four policy is retained.  At the old w6 leaf ask q15; at the old
(w3,w13) leaf ask q16.  Hence the task resolves in worst-case depth five.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .balanced_binary_twenty_world_depth_four import (
    twenty_world_fifteen_query_private_pairs,
)
from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class TwentyTwoWorldDepthFiveReceipt:
    world_count: int
    query_count: int
    adaptive_cost: int
    fixed_cost: int
    all_queries_exactly_balanced: bool
    all_private_pairs_query_unique: bool
    all_private_pairs_cross_target: bool
    theorem_holds: bool
    scope: str = "exact_balanced_binary_twenty_two_world_CA5_CF17"


def exact_balanced_twenty_two_world_seventeen_query_depth_five_task() -> FiniteTask:
    signatures = (
        "11111111111111100",
        "11111000100010110",
        "01111000100010110",
        "00011000100101011",
        "01011000100101011",
        "00111000100101011",
        "01111000011010010",
        "01101000011010010",
        "01101010011010010",
        "01110000011010010",
        "01110001011010010",
        "01111100011010010",
        "10000111000101101",
        "10000111100101101",
        "10000111101101101",
        "10000111101001101",
        "10000111101011101",
        "10000111010101101",
        "10000111010100101",
        "10000111010100001",
        "01111000011010000",
        "10000111100101100",
    )
    # Old targets are retained. w20 and w21 split the two refined leaves.
    targets = (0,8,9,11,9,10,1,5,4,3,2,0,13,11,6,7,4,12,14,15,16,17)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    rows = tuple(
        tuple(int(signatures[w][q]) for w in range(22))
        for q in range(17)
    )
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def twenty_two_world_seventeen_query_private_pairs() -> tuple[tuple[int, int], ...]:
    return twenty_world_fifteen_query_private_pairs() + ((6,20),(13,21))


def twenty_two_world_depth_five_policy() -> tuple:
    leaf = lambda *worlds: ("leaf", tuple(worlds))
    return (
        10,
        (
            3,
            (
                4,
                (5, leaf(0,11), (15, leaf(20), leaf(6))),
                (7, leaf(10), leaf(9)),
            ),
            (12, (6, leaf(8,16), leaf(7)), (11, leaf(14), leaf(15))),
        ),
        (
            8,
            (1, (0, leaf(1), leaf(2,4)), (2, leaf(5), (16, leaf(21), leaf(3,13)))),
            (13, (9, leaf(17), leaf(12)), (14, leaf(18), leaf(19))),
        ),
    )


def _policy_resolves(task: FiniteTask, policy: tuple) -> tuple[bool,int]:
    max_depth = 0
    def walk(node: tuple, active: tuple[int,...], depth: int) -> bool:
        nonlocal max_depth
        if node[0] == "leaf":
            max_depth = max(max_depth, depth)
            return len({task.worlds[i].target for i in active}) <= 1
        q,left_node,right_node = node
        query = task.queries[q]
        left = tuple(i for i in active if query.outcomes[i] == 1)
        right = tuple(i for i in active if query.outcomes[i] == 0)
        if not left or not right:
            return False
        return walk(left_node,left,depth+1) and walk(right_node,right,depth+1)
    return walk(policy,tuple(range(len(task.worlds))),0), max_depth


@lru_cache(maxsize=1)
def audit_exact_balanced_twenty_two_world_depth_five() -> TwentyTwoWorldDepthFiveReceipt:
    task = exact_balanced_twenty_two_world_seventeen_query_depth_five_task()
    pairs = twenty_two_world_seventeen_query_private_pairs()
    balanced = all(sum(query.outcomes)==11 and set(query.outcomes)<= {0,1} for query in task.queries)
    unique = True
    cross_target = True
    for qi,(a,b) in enumerate(pairs):
        separating = tuple(i for i,q in enumerate(task.queries) if q.outcomes[a] != q.outcomes[b])
        unique = unique and separating == (qi,)
        cross_target = cross_target and task.worlds[a].target != task.worlds[b].target
    policy_ok, policy_depth = _policy_resolves(task, twenty_two_world_depth_five_policy())
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    theorem = balanced and unique and cross_target and policy_ok and policy_depth==5 and adaptive==5 and fixed==17
    if not theorem:
        raise ArithmeticError("twenty-two-world depth-five witness audit failed")
    return TwentyTwoWorldDepthFiveReceipt(22,17,adaptive,fixed,balanced,unique,cross_target,True)
