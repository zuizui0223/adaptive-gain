"""Pareto structure of world versus query complexity at required gap q.

For deterministic unit-cost sensing with maximum query arity b>=2, let

    Delta_g = C_F - C_A >= q.

Two different lower envelopes matter.

1. Query/frontier minimum.
   If C_A=h, flattening a b-ary adaptive tree gives

       C_F <= T_b(h) = (b**h-1)/(b-1).

   Therefore the smallest adaptive depth compatible with gap q is

       h_b*(q) = min{h>=1 : T_b(h)-h >= q},

   and the minimum possible fixed/query/frontier count is

       m_min = E_min = h_b*(q)+q.

2. World minimum.
   Allowing larger arity does not reduce the smallest represented-world count.
   The unrestricted-arity productive-tree bound implies

       max Delta_g at n worlds = n-1-ceil(log2 n),

   and the binary private-pair witness attains it. Hence

       n_min(q) = q + h_2*(q) + 1.

The two minima need not be simultaneously attainable.  For each adaptive depth h
between h_b*(q) and h_2*(q), define

    I = h+q,
    n_b(q,h) = min{n : F_b(n,h) >= I}.

Then (n_b(q,h), I, I) gives the minimum world/query/frontier coordinates at that
depth. Removing dominated points gives the exact world-vs-query Pareto frontier.

Example: q=3,b=4 has frontier

    (worlds,queries,frontier_edges,depth) = (8,5,5,2), (7,6,6,3).

Thus richer observations can reduce query/frontier burden but cannot beat the
global world-count lower bound; for some gaps the two optima are incompatible.

No novelty is claimed for elementary b-ary tree counting.  The repository-specific
use is the exact composition with the adaptive/fixed structural gap and productive
frontier.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, log2

from .bounded_arity_extremal_bounds import (
    _height,
    _internal_count,
    _maximum_tree,
    _prune_to_internal_count,
    _tree_task,
    maximum_bounded_arity_tree_internal_nodes,
)
from .core import adaptive_minimum_resolution, fixed_minimum_resolution
from .productive_frontier import build_productive_frontier


def full_bary_internal_capacity(adaptive_depth: int, max_arity: int) -> int:
    if type(adaptive_depth) is not int or adaptive_depth < 1:
        raise ValueError("adaptive_depth must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    b = max_arity
    h = adaptive_depth
    return (b**h - 1) // (b - 1)


def minimum_adaptive_depth_for_gap(required_gap: int, max_arity: int) -> int:
    if type(required_gap) is not int or required_gap < 1:
        raise ValueError("required_gap must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    h = 1
    while full_bary_internal_capacity(h, max_arity) - h < required_gap:
        h += 1
    return h


def minimum_query_count_for_gap(required_gap: int, max_arity: int) -> int:
    return required_gap + minimum_adaptive_depth_for_gap(required_gap, max_arity)


def minimum_productive_frontier_edges_for_gap(required_gap: int, max_arity: int) -> int:
    return minimum_query_count_for_gap(required_gap, max_arity)


def minimum_world_count_for_gap(required_gap: int) -> int:
    """Arity-independent minimum represented-world count for gap q."""
    h_binary = minimum_adaptive_depth_for_gap(required_gap, 2)
    return required_gap + h_binary + 1


def unrestricted_world_gap_ceiling(world_count: int) -> int:
    """Exact maximum additive gap at n worlds when query arity is unrestricted."""
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    n = world_count
    return n - 1 - ceil(log2(n))


def minimum_worlds_for_internal_count_at_depth(
    internal_count: int,
    adaptive_depth: int,
    max_arity: int,
) -> int:
    """Smallest leaf/world budget whose F_b capacity reaches I at depth h."""
    if type(internal_count) is not int or internal_count < 1:
        raise ValueError("internal_count must be a positive integer")
    if type(adaptive_depth) is not int or adaptive_depth < 1:
        raise ValueError("adaptive_depth must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")

    # Any tree with I internal nodes and arity at most b has at most
    # 1+(b-1)I leaves, so this is a finite constructive search interval.
    upper = 1 + (max_arity - 1) * internal_count
    for n in range(2, upper + 1):
        if maximum_bounded_arity_tree_internal_nodes(n, adaptive_depth, max_arity) >= internal_count:
            return n
    raise ArithmeticError("bounded-arity world search failed inside constructive upper bound")


@dataclass(frozen=True)
class ArityGapParetoPoint:
    required_structural_gap: int
    max_arity: int
    adaptive_depth: int
    world_count: int
    query_count: int
    productive_frontier_edge_count: int



def arity_gap_pareto_frontier(required_gap: int, max_arity: int) -> tuple[ArityGapParetoPoint, ...]:
    """Exact nondominated (worlds,queries/frontier) points for gap q.

    Depths larger than the binary minimum cannot reduce world count below the
    arity-independent world optimum and only increase query/frontier count, so
    only h_b*(q) through h_2*(q) need be considered.
    """
    q = required_gap
    if type(q) is not int or q < 1:
        raise ValueError("required_gap must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")

    h_min = minimum_adaptive_depth_for_gap(q, max_arity)
    h_binary = minimum_adaptive_depth_for_gap(q, 2)
    points: list[ArityGapParetoPoint] = []
    best_worlds_so_far: int | None = None

    for h in range(h_min, h_binary + 1):
        fixed = h + q
        n = minimum_worlds_for_internal_count_at_depth(fixed, h, max_arity)
        # Query count increases with h.  A new depth is Pareto-relevant exactly
        # when it strictly decreases the minimum world count.
        if best_worlds_so_far is None or n < best_worlds_so_far:
            points.append(
                ArityGapParetoPoint(
                    required_structural_gap=q,
                    max_arity=max_arity,
                    adaptive_depth=h,
                    world_count=n,
                    query_count=fixed,
                    productive_frontier_edge_count=fixed,
                )
            )
            best_worlds_so_far = n

    return tuple(points)


@dataclass(frozen=True)
class ArityGapWitnessAudit:
    point: ArityGapParetoPoint
    direct_check_performed: bool
    observed_adaptive_cost: int | None
    observed_fixed_cost: int | None
    observed_frontier_edge_count: int | None
    theorem_holds: bool



def audit_arity_gap_pareto_point(
    point: ArityGapParetoPoint,
    *,
    direct_check: bool = True,
) -> ArityGapWitnessAudit:
    """Construct the private-pair witness for a Pareto point and audit it."""
    I = point.query_count
    n = point.world_count
    h = point.adaptive_depth
    b = point.max_arity

    tree = _maximum_tree(n, h, b)
    tree = _prune_to_internal_count(tree, I)
    if _internal_count(tree) != I or _height(tree) != h:
        raise ArithmeticError("Pareto witness tree lost declared size or depth")

    observed_ca = observed_cf = observed_edges = None
    perform = bool(direct_check and I <= 20)
    if perform:
        task, private_count = _tree_task(tree, n, I)
        if private_count != I:
            raise ArithmeticError("Pareto witness lost private-pair obligations")
        observed_ca = adaptive_minimum_resolution(task).minimum_worst_path_cost
        observed_cf = fixed_minimum_resolution(task).minimum_cost
        observed_edges = len(build_productive_frontier(task).minimal_productive_sets)

    direct_agrees = (
        not perform
        or (
            observed_ca == h
            and observed_cf == I
            and observed_cf - observed_ca == point.required_structural_gap
            and observed_edges == I
        )
    )
    theorem_holds = direct_agrees
    if not theorem_holds:
        raise ArithmeticError("bounded-arity Pareto witness audit failed")
    return ArityGapWitnessAudit(
        point=point,
        direct_check_performed=perform,
        observed_adaptive_cost=observed_ca,
        observed_fixed_cost=observed_cf,
        observed_frontier_edge_count=observed_edges,
        theorem_holds=theorem_holds,
    )
