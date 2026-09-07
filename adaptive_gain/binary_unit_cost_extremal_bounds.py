"""Sharp fixed-(world,query) adaptive-gain ratio for binary unit-cost queries.

Let ``n>=2`` and ``m>=1``.  Put ``K=min(m,n-1)`` and
``d=floor(log2(K+1))``.  For finite deterministic guaranteed target resolution
with binary query outcomes and unit costs,

    max C_F/C_A
      = max(1, (2**d - 1)/d, K/(d+1)).

Upper bound: a binary adaptive tree of worst-path depth h has at most 2**h-1
internal-node occurrences, at most n-1 by leaf counting, and cannot use more than
m declared resources.  Flattening its distinct query union is fixed-resolving.

Attainment: place N worlds in an ordered path with alternating targets and declare
all N-1 threshold queries.  Every threshold is the unique separator of one
adjacent opposite-target pair, so C_F=N-1.  Adaptive balanced binary search must
isolate the exact position because every non-singleton interval contains both
targets, giving C_A=ceil(log2 N).  Padding with duplicate worlds and constant
queries realizes exact larger n,m counts.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import ceil, floor, log2

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class BinaryUnitCostWorldQueryRatioReceipt:
    world_count: int
    query_count: int
    effective_resource_cap: int
    logarithmic_index: int
    sharp_ratio: Fraction
    first_candidate: Fraction
    second_candidate: Fraction
    witness_adaptive_cost: int
    witness_fixed_cost: int
    witness_ratio: Fraction
    upper_bound_attained: bool
    scope: str = "sharp_binary_unit_cost_ratio_fixed_world_and_query_counts"


def binary_tree_fixed_cost_bound(world_count: int, query_count: int, adaptive_cost: int) -> int:
    if type(world_count) is not int or world_count < 1:
        raise ValueError("world_count must be a positive integer")
    if type(query_count) is not int or query_count < 0:
        raise ValueError("query_count must be a nonnegative integer")
    if type(adaptive_cost) is not int or adaptive_cost < 0:
        raise ValueError("adaptive_cost must be a nonnegative integer")
    if adaptive_cost == 0:
        return 0
    return min(query_count, max(0, world_count - 1), (1 << adaptive_cost) - 1)


def _floor_log2_positive(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive")
    return value.bit_length() - 1


def sharp_binary_unit_cost_ratio(world_count: int, query_count: int) -> Fraction:
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    cap = min(query_count, world_count - 1)
    if cap <= 2:
        return Fraction(1, 1)
    d = _floor_log2_positive(cap + 1)
    first = Fraction((1 << d) - 1, d)
    second = Fraction(cap, d + 1)
    return max(Fraction(1, 1), first, second)


def threshold_path_task(world_count: int) -> FiniteTask:
    """Alternating targets on a path, with one binary threshold per boundary."""
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    worlds = tuple(World(f"w{i}", i & 1) for i in range(world_count))
    queries = []
    for boundary in range(world_count - 1):
        outcomes = tuple(int(i > boundary) for i in range(world_count))
        queries.append(Query(f"threshold_{boundary}", 1, outcomes))
    return FiniteTask(worlds, tuple(queries))


def _pad_binary_task(task: FiniteTask, world_count: int, query_count: int) -> FiniteTask:
    worlds = list(task.worlds)
    queries = list(task.queries)
    if world_count < len(worlds) or query_count < len(queries):
        raise ValueError("padding counts must dominate the core task")
    while len(worlds) < world_count:
        worlds.append(World(f"pad_world_{len(worlds)}", worlds[0].target))
        for i, query in enumerate(queries):
            queries[i] = Query(query.name, query.cost, query.outcomes + (query.outcomes[0],))
    while len(queries) < query_count:
        queries.append(Query(f"pad_query_{len(queries)}", 1, tuple(0 for _ in worlds)))
    return FiniteTask(tuple(worlds), tuple(queries))


def _direct_ratio_one_task(world_count: int, query_count: int) -> FiniteTask:
    worlds = tuple(World(f"w{i}", i & 1) for i in range(world_count))
    queries = [Query("direct", 1, tuple(world.target for world in worlds))]
    while len(queries) < query_count:
        queries.append(Query(f"pad_query_{len(queries)}", 1, tuple(0 for _ in worlds)))
    return FiniteTask(worlds, tuple(queries))


def sharp_binary_unit_cost_ratio_witness(world_count: int, query_count: int) -> FiniteTask:
    ratio = sharp_binary_unit_cost_ratio(world_count, query_count)
    if ratio == 1:
        return _direct_ratio_one_task(world_count, query_count)

    cap = min(query_count, world_count - 1)
    d = _floor_log2_positive(cap + 1)
    first = Fraction((1 << d) - 1, d)
    second = Fraction(cap, d + 1)
    if first >= second:
        core_worlds = 1 << d
    else:
        core_worlds = cap + 1
    return _pad_binary_task(threshold_path_task(core_worlds), world_count, query_count)


def sharp_binary_unit_cost_ratio_receipt(
    world_count: int,
    query_count: int,
) -> BinaryUnitCostWorldQueryRatioReceipt:
    expected = sharp_binary_unit_cost_ratio(world_count, query_count)
    cap = min(query_count, world_count - 1)
    d = _floor_log2_positive(cap + 1)
    first = Fraction((1 << d) - 1, d) if d else Fraction(1, 1)
    second = Fraction(cap, d + 1)
    task = sharp_binary_unit_cost_ratio_witness(world_count, query_count)
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive in (None, 0) or fixed is None:
        raise ArithmeticError("binary sharp-ratio witness unexpectedly unresolved")
    actual = Fraction(fixed, adaptive)
    if actual != expected:
        raise ArithmeticError("binary sharp-ratio witness failed to attain theorem bound")
    return BinaryUnitCostWorldQueryRatioReceipt(
        world_count,
        query_count,
        cap,
        d,
        expected,
        first,
        second,
        adaptive,
        fixed,
        actual,
        True,
    )
