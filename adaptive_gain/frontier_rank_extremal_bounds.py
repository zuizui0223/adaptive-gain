"""Sharp unit-cost ratio under a cap on productive-frontier rank.

Let H_min be the inclusion-minimal productive frontier and define its rank as

    rank(H_min) = max(|E| : E in H_min).

For any positive rank cap r >= 1, imposing rank(H_min) <= r does not reduce the
sharp adaptive/fixed ratio at fixed world count n, query count m, or maximum
query arity b.  The sharp bounded-arity witness already has a frontier made only
of singleton edges, hence rank one, while attaining the unrestricted bounded-
arity optimum.

Therefore

    R_{b, rank<=r}(n,m) = R_b(n,m)       for every r >= 1.

This is an exact negative extremal result: upper-bounding frontier edge size is
not a useful way to control the worst fixed/adaptive ratio.  Singleton frontier
obligations can already make individual physical queries fixed-mandatory.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .bounded_arity_extremal_bounds import (
    sharp_bounded_arity_unit_cost_ratio,
    sharp_bounded_arity_unit_cost_witness,
)
from .core import adaptive_minimum_resolution, fixed_minimum_resolution
from .productive_frontier import build_productive_frontier


@dataclass(frozen=True)
class FrontierRankCappedRatioReceipt:
    world_count: int
    query_count: int
    max_arity: int
    frontier_rank_cap: int
    sharp_ratio: Fraction
    witness_adaptive_cost: int | None
    witness_fixed_cost: int | None
    witness_ratio: Fraction | None
    witness_frontier_rank: int
    witness_frontier_edge_count: int
    rank_cap_holds: bool
    direct_check_agrees: bool
    scope: str = "sharp_unit_cost_ratio_with_productive_frontier_rank_cap"


def _validate(
    world_count: int,
    query_count: int,
    max_arity: int,
    frontier_rank_cap: int,
) -> None:
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    if type(frontier_rank_cap) is not int or frontier_rank_cap < 1:
        raise ValueError("frontier_rank_cap must be a positive integer")


def productive_frontier_rank(minimal_productive_sets: tuple[int, ...]) -> int:
    """Maximum edge size, with rank zero only for an empty frontier."""
    return max((edge.bit_count() for edge in minimal_productive_sets), default=0)


def sharp_frontier_rank_capped_unit_cost_ratio(
    world_count: int,
    query_count: int,
    max_arity: int,
    frontier_rank_cap: int,
) -> Fraction:
    """Exact ratio under rank(H_min) <= frontier_rank_cap, for cap >= 1."""
    _validate(world_count, query_count, max_arity, frontier_rank_cap)
    return sharp_bounded_arity_unit_cost_ratio(
        world_count, query_count, max_arity
    )


def sharp_frontier_rank_capped_unit_cost_ratio_receipt(
    world_count: int,
    query_count: int,
    max_arity: int,
    frontier_rank_cap: int,
) -> FrontierRankCappedRatioReceipt:
    _validate(world_count, query_count, max_arity, frontier_rank_cap)
    expected = sharp_frontier_rank_capped_unit_cost_ratio(
        world_count, query_count, max_arity, frontier_rank_cap
    )
    task = sharp_bounded_arity_unit_cost_witness(
        world_count, query_count, max_arity
    )
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    frontier = build_productive_frontier(task)
    rank = productive_frontier_rank(frontier.minimal_productive_sets)
    if adaptive in (None, 0) or fixed is None:
        raise ArithmeticError("rank-capped extremal witness unexpectedly unresolved")
    actual = Fraction(fixed, adaptive)
    if actual != expected or rank > frontier_rank_cap:
        raise ArithmeticError("rank-capped extremal witness failed theorem audit")
    # Every nontrivial sharp bounded-arity construction used here has singleton
    # private-edge obligations, hence the stronger rank-one property.
    if rank != 1:
        raise ArithmeticError("sharp bounded-arity witness lost rank-one frontier")
    return FrontierRankCappedRatioReceipt(
        world_count,
        query_count,
        max_arity,
        frontier_rank_cap,
        expected,
        adaptive,
        fixed,
        actual,
        rank,
        len(frontier.minimal_productive_sets),
        rank <= frontier_rank_cap,
        actual == expected,
    )
