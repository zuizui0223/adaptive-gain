"""Sharp unit-cost ratio under a cap on productive-frontier edge count.

For a finite deterministic task let H be its inclusion-minimal productive
frontier.  Under unit costs C_F is the transversal number tau(H), so

    C_F <= |H|.

Combining this with the sharp bounded-arity tree-union theorem gives, for
n represented worlds, m declared queries, query arity at most b, and
|H| <= E,

    max C_F/C_A
      = max_h min(m, E, F_b(n,h)) / h.

Sharpness uses the bounded-arity private-pair forest construction.  Truncating
it to I=min(m,E,F_b(n,h)) internal queries makes the productive frontier exactly
I singleton edges, so every retained query is fixed-mandatory.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .bounded_arity_extremal_bounds import (
    maximum_bounded_arity_tree_internal_nodes,
    sharp_bounded_arity_unit_cost_witness,
)
from .core import FiniteTask, Query, adaptive_minimum_resolution, fixed_minimum_resolution
from .productive_frontier import build_productive_frontier


@dataclass(frozen=True)
class FrontierEdgeCappedRatioReceipt:
    world_count: int
    query_count: int
    max_arity: int
    frontier_edge_cap: int
    sharp_ratio: Fraction
    witness_adaptive_cost: int | None
    witness_fixed_cost: int | None
    witness_ratio: Fraction | None
    witness_frontier_edge_count: int
    edge_cap_holds: bool
    direct_check_agrees: bool
    scope: str = "sharp_unit_cost_ratio_with_productive_frontier_edge_cap"


def sharp_frontier_edge_capped_unit_cost_ratio(
    world_count: int,
    query_count: int,
    max_arity: int,
    frontier_edge_cap: int,
) -> Fraction:
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    if type(frontier_edge_cap) is not int or frontier_edge_cap < 1:
        raise ValueError("frontier_edge_cap must be a positive integer")
    return max(
        Fraction(
            min(
                query_count,
                frontier_edge_cap,
                maximum_bounded_arity_tree_internal_nodes(
                    world_count, depth, max_arity
                ),
            ),
            depth,
        )
        for depth in range(1, world_count)
    )


def sharp_frontier_edge_capped_unit_cost_witness(
    world_count: int,
    query_count: int,
    max_arity: int,
    frontier_edge_cap: int,
) -> FiniteTask:
    if query_count > 20:
        raise ValueError("FiniteTask witness is limited by the exact solver's 20-query cap")
    effective_query_count = min(query_count, frontier_edge_cap)
    core = sharp_bounded_arity_unit_cost_witness(
        world_count, effective_query_count, max_arity
    )
    queries = list(core.queries)
    while len(queries) < query_count:
        queries.append(
            Query(
                f"frontier_pad_query_{len(queries)}",
                1,
                tuple(0 for _ in core.worlds),
            )
        )
    task = FiniteTask(core.worlds, tuple(queries))
    frontier = build_productive_frontier(task)
    if len(frontier.minimal_productive_sets) > frontier_edge_cap:
        raise ArithmeticError("edge-capped extremal witness exceeded its frontier cap")
    return task


def sharp_frontier_edge_capped_unit_cost_ratio_receipt(
    world_count: int,
    query_count: int,
    max_arity: int,
    frontier_edge_cap: int,
) -> FrontierEdgeCappedRatioReceipt:
    expected = sharp_frontier_edge_capped_unit_cost_ratio(
        world_count, query_count, max_arity, frontier_edge_cap
    )
    task = sharp_frontier_edge_capped_unit_cost_witness(
        world_count, query_count, max_arity, frontier_edge_cap
    )
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    frontier = build_productive_frontier(task)
    if adaptive in (None, 0) or fixed is None:
        raise ArithmeticError("edge-capped extremal witness unexpectedly unresolved")
    actual = Fraction(fixed, adaptive)
    edge_count = len(frontier.minimal_productive_sets)
    if actual != expected or edge_count > frontier_edge_cap:
        raise ArithmeticError("edge-capped extremal witness failed theorem audit")
    return FrontierEdgeCappedRatioReceipt(
        world_count,
        query_count,
        max_arity,
        frontier_edge_cap,
        expected,
        adaptive,
        fixed,
        actual,
        edge_count,
        edge_count <= frontier_edge_cap,
        actual == expected,
    )
