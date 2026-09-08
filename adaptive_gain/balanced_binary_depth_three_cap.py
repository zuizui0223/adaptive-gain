"""Sharp fixed-cost envelope at adaptive depth at most three.

For exactly-balanced binary unit-cost tasks on an even number n>=6 of
represented worlds, let

    D_3(n) = max C_F over tasks with C_A <= 3.

Then

    D_3(6)  = 3,
    D_3(8)  = 5,
    D_3(10) = 6,
    D_3(n)  = 7 for every even n>=12.

Equivalently, for even n>=6,

    D_3(n) = min(7, n-3)

except for the unique defect n=10, where D_3(10)=6.

The upper bound combines the binary depth-three flattening cap 7, the sharp
global exact-balanced fixed-cost cap n-3, and the registered ten-world
compatibility obstruction.  Sharp witnesses are explicit at n=6,8,10,12 and
the twelve-world (3,7) witness pads by complementary world pairs to every
larger even n.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .balanced_binary_eight_world_profile import exact_balanced_eight_world_three_query_task
from .balanced_binary_small_scope import exact_balanced_eight_world_five_query_task
from .balanced_binary_ten_world_profile import (
    audit_ten_world_no_depth_three_fixed_seven,
    exact_balanced_ten_world_six_query_task,
)
from .balanced_binary_twelve_world_profile import exact_balanced_depth_three_seven_query_witness
from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class ExactBalancedDepthThreeCapReceipt:
    world_count: int
    sharp_fixed_cost_cap: int
    witness_adaptive_cost: int
    witness_fixed_cost: int
    universal_tree_cap: int
    universal_global_balance_cap: int
    ten_world_exception_used: bool
    theorem_holds: bool
    scope: str = "exact_balanced_binary_sharp_fixed_cost_given_CA_at_most_3"


def sharp_exact_balanced_depth_three_fixed_cost_cap(world_count: int) -> int:
    if type(world_count) is not int or world_count < 6 or world_count % 2:
        raise ValueError("world_count must be an even integer at least 6")
    if world_count == 10:
        return 6
    return min(7, world_count - 3)


def exact_balanced_six_world_three_query_task() -> FiniteTask:
    """Exactly-balanced six-world witness with (C_A,C_F)=(2,3)."""
    targets = (0, 1, 1, 1, 0, 0)
    rows = (
        (0, 0, 0, 1, 1, 1),
        (1, 1, 0, 1, 0, 0),
        (1, 0, 1, 0, 1, 0),
    )
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    queries = tuple(Query(f"q{i}", 1, row) for i, row in enumerate(rows))
    return FiniteTask(worlds, queries)


def exact_balanced_depth_three_cap_witness(world_count: int) -> FiniteTask:
    if type(world_count) is not int or world_count < 6 or world_count % 2:
        raise ValueError("world_count must be an even integer at least 6")
    if world_count == 6:
        return exact_balanced_six_world_three_query_task()
    if world_count == 8:
        return exact_balanced_eight_world_five_query_task()
    if world_count == 10:
        return exact_balanced_ten_world_six_query_task()
    return exact_balanced_depth_three_seven_query_witness(world_count)


def _all_queries_exactly_balanced(task: FiniteTask) -> bool:
    half = len(task.worlds) // 2
    return all(
        set(query.outcomes) <= {0, 1}
        and sum(outcome == 0 for outcome in query.outcomes) == half
        and sum(outcome == 1 for outcome in query.outcomes) == half
        for query in task.queries
    )


@lru_cache(maxsize=None)
def audit_exact_balanced_depth_three_fixed_cost_cap(
    world_count: int,
) -> ExactBalancedDepthThreeCapReceipt:
    cap = sharp_exact_balanced_depth_three_fixed_cost_cap(world_count)
    witness = exact_balanced_depth_three_cap_witness(world_count)
    adaptive = adaptive_minimum_resolution(witness).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(witness).minimum_cost
    if adaptive is None or fixed is None:
        raise ArithmeticError("registered depth-three cap witness is unresolved")

    global_cap = world_count - 3
    tree_cap = 7
    exception = world_count == 10
    obstruction_ok = True
    if exception:
        obstruction = audit_ten_world_no_depth_three_fixed_seven()
        obstruction_ok = obstruction.theorem_holds and not obstruction.depth_three_fixed_seven_possible

    theorem = (
        adaptive <= 3
        and fixed == cap
        and _all_queries_exactly_balanced(witness)
        and cap <= tree_cap
        and cap <= global_cap
        and obstruction_ok
    )
    if not theorem:
        raise ArithmeticError("exact-balanced depth-three cap audit failed")

    return ExactBalancedDepthThreeCapReceipt(
        world_count=world_count,
        sharp_fixed_cost_cap=cap,
        witness_adaptive_cost=adaptive,
        witness_fixed_cost=fixed,
        universal_tree_cap=tree_cap,
        universal_global_balance_cap=global_cap,
        ten_world_exception_used=exception,
        theorem_holds=True,
    )
