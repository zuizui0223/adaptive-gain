"""Sharp structural-opportunity bounds inherited from adaptive-gain extremal theory.

For a nontrivial finite unit-cost task define the adaptive-only budget-window
width

    W = C_F - C_A,

and normalize it by the adaptive effort needed to exploit that window:

    Omega = W / C_A = C_F / C_A - 1.

Because the repository already has exact sharp formulas for max C_F/C_A at
fixed world count n, query count m, query arity b, and optional productive-
frontier constraints, the corresponding normalized window bounds follow by
subtracting one.

This module deliberately keeps the statement structural and fitness-free.  A
biological application may later map an adaptive-only sensing window to a
fitness benefit under a natural-history-specific deadline, energetic ceiling,
handling-time limit, or opportunity window.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .bounded_arity_extremal_bounds import sharp_bounded_arity_unit_cost_ratio
from .core import FiniteTask, adaptive_minimum_resolution, fixed_minimum_resolution
from .frontier_edge_extremal_bounds import sharp_frontier_edge_capped_unit_cost_ratio
from .frontier_rank_extremal_bounds import sharp_frontier_rank_capped_unit_cost_ratio


@dataclass(frozen=True)
class StructuralOpportunityReceipt:
    adaptive_cost: int
    fixed_cost: int
    adaptive_only_budget_count: int
    normalized_opportunity: Fraction
    strict_gain: bool
    scope: str = "finite_deterministic_unit_cost_structural_opportunity"


def task_structural_opportunity(task: FiniteTask) -> StructuralOpportunityReceipt:
    """Return W=C_F-C_A and Omega=W/C_A for a nontrivial resolvable task.

    The task must use unit query costs because the extremal comparisons in this
    module are unit-cost theorems.  The task-level identity itself is algebraic,
    but enforcing unit costs keeps receipts directly comparable with the sharp
    fixed-(n,m,b) results.
    """

    if any(query.cost != 1 for query in task.queries):
        raise ValueError("structural opportunity receipt requires unit query costs")
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive is None or fixed is None:
        raise ValueError("task must be resolvable by the declared query vocabulary")
    if adaptive <= 0:
        raise ValueError("task must be nontrivial with positive adaptive cost")
    if fixed < adaptive:
        raise ArithmeticError("fixed cost cannot be below adaptive cost")
    width = fixed - adaptive
    return StructuralOpportunityReceipt(
        adaptive_cost=adaptive,
        fixed_cost=fixed,
        adaptive_only_budget_count=width,
        normalized_opportunity=Fraction(width, adaptive),
        strict_gain=width > 0,
    )


def sharp_normalized_opportunity(
    world_count: int,
    query_count: int,
    max_arity: int,
) -> Fraction:
    """Exact max of (C_F-C_A)/C_A at fixed (n,m,b)."""

    return sharp_bounded_arity_unit_cost_ratio(
        world_count, query_count, max_arity
    ) - 1


def sharp_edge_capped_normalized_opportunity(
    world_count: int,
    query_count: int,
    max_arity: int,
    frontier_edge_cap: int,
) -> Fraction:
    """Exact max normalized opportunity under |H_min| <= E."""

    return sharp_frontier_edge_capped_unit_cost_ratio(
        world_count,
        query_count,
        max_arity,
        frontier_edge_cap,
    ) - 1


def sharp_rank_capped_normalized_opportunity(
    world_count: int,
    query_count: int,
    max_arity: int,
    frontier_rank_cap: int,
) -> Fraction:
    """Exact max normalized opportunity under rank(H_min) <= r, r>=1.

    The inherited extremal theorem says the rank cap is vacuous: rank-one
    singleton obligations already attain the unrestricted bounded-arity maximum.
    """

    return sharp_frontier_rank_capped_unit_cost_ratio(
        world_count,
        query_count,
        max_arity,
        frontier_rank_cap,
    ) - 1


def opportunity_bound_holds(
    task: FiniteTask,
    *,
    max_arity: int | None = None,
) -> bool:
    """Check a task against the inherited sharp fixed-(n,m,b) bound."""

    receipt = task_structural_opportunity(task)
    if max_arity is None:
        max_arity = max((len(set(query.outcomes)) for query in task.queries), default=2)
        max_arity = max(2, max_arity)
    if any(len(set(query.outcomes)) > max_arity for query in task.queries):
        raise ValueError("declared max_arity is below an observed query arity")
    bound = sharp_normalized_opportunity(
        len(task.worlds), len(task.queries), max_arity
    )
    return receipt.normalized_opportunity <= bound
