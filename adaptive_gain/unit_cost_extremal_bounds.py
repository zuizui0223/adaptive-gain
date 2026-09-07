"""Sharp fixed-world/fixed-query upper bounds for unit-cost adaptive gain.

For a productive rooted adaptive decision tree with at most ``n`` nonempty leaves
and worst-path depth ``h``, let ``I`` be its number of internal-node occurrences.
With arbitrary deterministic query arity,

    I <= M(n,h)
      = n + 1 - max(2, ceil(n / 2**(h-1))).

The selected tree's distinct query union has size at most I, and flattening that
union is a fixed resolver.  Therefore, for unit-cost tasks,

    C_F <= min(m, M(n, C_A)).

Optimizing over the possible adaptive cost gives an exact fixed-(n,m) extremum:

    max C_F/C_A
      = max(1, min(m, 1 + floor(n/2)) / 2).

The upper bound is attained by the registered depth-two k-branch routing family,
with harmless duplicate worlds / unused queries added when exact n,m counts are
larger than the core construction.

Scope: finite deterministic guaranteed target resolution, unit query costs,
arbitrary finite query arity.  Binary-only arity has a different extremal problem.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import ceil

from .core import FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution
from .extremal_routing import k_branch_routing_task


@dataclass(frozen=True)
class AdaptiveTreeUnionBoundReceipt:
    world_count: int
    adaptive_depth: int
    maximum_internal_occurrences: int
    scope: str = "arbitrary_arity_productive_tree_unit_cost_union_bound"


@dataclass(frozen=True)
class UnitCostWorldQueryRatioReceipt:
    world_count: int
    query_count: int
    sharp_ratio: Fraction
    witness_world_count: int
    witness_query_count: int
    witness_adaptive_cost: int
    witness_fixed_cost: int
    witness_ratio: Fraction
    upper_bound_attained: bool
    scope: str = "sharp_unit_cost_ratio_fixed_world_and_query_counts_arbitrary_query_arity"


def maximum_productive_tree_internal_nodes(world_count: int, depth: int) -> int:
    """Exact maximum internal-node count for a productive tree.

    Leaves are nonempty represented-world cells, hence at most ``world_count``.
    Every internal node has at least two nonempty children.  Query arity is not
    bounded above.
    """
    if type(world_count) is not int or world_count < 1:
        raise ValueError("world_count must be a positive integer")
    if type(depth) is not int or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    if world_count <= 1 or depth == 0:
        return 0
    denominator = 1 << (depth - 1)
    return world_count + 1 - max(2, ceil(world_count / denominator))


def adaptive_tree_union_bound_receipt(world_count: int, depth: int) -> AdaptiveTreeUnionBoundReceipt:
    return AdaptiveTreeUnionBoundReceipt(
        world_count,
        depth,
        maximum_productive_tree_internal_nodes(world_count, depth),
    )


def unit_cost_fixed_cost_bound(world_count: int, query_count: int, adaptive_cost: int) -> int:
    if type(query_count) is not int or query_count < 0:
        raise ValueError("query_count must be a nonnegative integer")
    if type(adaptive_cost) is not int or adaptive_cost < 0:
        raise ValueError("adaptive_cost must be a nonnegative integer")
    if adaptive_cost == 0:
        return 0
    return min(
        query_count,
        maximum_productive_tree_internal_nodes(world_count, adaptive_cost),
    )


def sharp_unit_cost_ratio(world_count: int, query_count: int) -> Fraction:
    """Exact maximum C_F/C_A at fixed n,m under unit costs and arbitrary arity."""
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    numerator = min(query_count, 1 + world_count // 2)
    return max(Fraction(1, 1), Fraction(numerator, 2))


def _pad_task(task: FiniteTask, world_count: int, query_count: int) -> FiniteTask:
    worlds = list(task.worlds)
    queries = list(task.queries)
    if world_count < len(worlds) or query_count < len(queries):
        raise ValueError("padding counts must dominate the core task")

    # Duplicate one represented world exactly.  It introduces no new target
    # distinction and therefore cannot change either optimum.
    template = worlds[0]
    while len(worlds) < world_count:
        worlds.append(World(f"pad_world_{len(worlds)}", template.target))
        for i, query in enumerate(queries):
            queries[i] = Query(query.name, query.cost, query.outcomes + (query.outcomes[0],))

    # Constant unit-cost queries are harmless extra declared resources.
    while len(queries) < query_count:
        queries.append(Query(f"pad_query_{len(queries)}", 1, tuple(0 for _ in worlds)))
    return FiniteTask(tuple(worlds), tuple(queries))


def sharp_unit_cost_ratio_witness(world_count: int, query_count: int) -> FiniteTask:
    ratio = sharp_unit_cost_ratio(world_count, query_count)
    if ratio == 1:
        # One direct unit-cost target query; all other resources are harmless.
        worlds = tuple(World(f"w{i}", i % 2) for i in range(world_count))
        direct = Query("direct", 1, tuple(world.target for world in worlds))
        queries = [direct]
        while len(queries) < query_count:
            queries.append(Query(f"pad_query_{len(queries)}", 1, tuple(0 for _ in worlds)))
        return FiniteTask(worlds, tuple(queries))

    branch_count = min(world_count // 2, query_count - 1)
    if branch_count < 2:
        raise ArithmeticError("nontrivial sharp-ratio witness lost required routing branches")
    return _pad_task(k_branch_routing_task(branch_count), world_count, query_count)


def sharp_unit_cost_ratio_receipt(world_count: int, query_count: int) -> UnitCostWorldQueryRatioReceipt:
    expected = sharp_unit_cost_ratio(world_count, query_count)
    task = sharp_unit_cost_ratio_witness(world_count, query_count)
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive in (None, 0) or fixed is None:
        raise ArithmeticError("sharp-ratio witness unexpectedly unresolved")
    actual = Fraction(fixed, adaptive)
    if actual != expected:
        raise ArithmeticError("sharp unit-cost ratio witness failed to attain theorem bound")
    return UnitCostWorldQueryRatioReceipt(
        world_count,
        query_count,
        expected,
        len(task.worlds),
        len(task.queries),
        adaptive,
        fixed,
        actual,
        True,
    )
