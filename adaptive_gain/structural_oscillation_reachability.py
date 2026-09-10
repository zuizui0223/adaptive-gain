"""Structural thresholds for reaching oscillatory eco-evolutionary feedback.

This module composes two already-established layers:

1. finite unit-cost bounded-arity sensing bounds on the structural gap
   Delta_g = C_F-C_A;
2. the generalized local response threshold

       G_osc = (alpha-phi)^2 / [4(1-phi)]

   for the onset of a complex local eigenpair.

If restoring loop gain is generated linearly from structural gap,

    G = a * Delta_g,   a = (-beta*e)*lambda_cost > 0,

then the smallest integer structural gap that can enter the oscillatory region is

    g_osc,min = floor(G_osc/a) + 1.

Stable oscillation additionally requires G<G_+.

The canonical executable corollary uses

    alpha=1, phi=1/2, a=1/8.

Then G_osc=1/8, so gap >=2 is necessary for oscillation.  Existing binary
bounded-arity extremal theory proves that every binary task with <=5 worlds has
gap <=1 and every binary task with <=4 queries has gap <=1, while the sharp
(6 worlds, 5 queries, b=2) witness has C_A=3, C_F=5, gap=2.  The unit-cost
productive-frontier bound C_F<=|H_min| also implies that at least five minimal
frontier obligations are required, and the same witness attains five singleton
obligations.  Hence the first canonical binary oscillatory scope is sharp in
world count, query count, and productive-frontier edge count.

No novelty is claimed for the complex-eigenvalue threshold or integer rounding.
The repository-specific statement is the exact composition with finite sensing
extremal bounds and their constructive witness.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import floor, inf, isfinite, nextafter

from .bounded_arity_extremal_bounds import (
    maximum_bounded_arity_tree_internal_nodes,
    sharp_bounded_arity_unit_cost_witness,
)
from .core import adaptive_minimum_resolution, fixed_minimum_resolution
from .general_evolutionary_response import general_response_thresholds
from .productive_frontier import build_productive_frontier


def minimum_integer_gap_for_oscillation(
    *,
    evolutionary_persistence: float,
    community_memory: float,
    gain_per_structural_gap: float,
) -> int:
    """Smallest integer Delta_g with a*Delta_g > G_osc.

    ``nextafter`` nudges the strict threshold upward so an exact integer ratio
    ``G_osc/a`` is not accidentally admitted at equality.
    """

    a = float(gain_per_structural_gap)
    if not isfinite(a) or a <= 0.0:
        raise ValueError("gain_per_structural_gap must be finite and positive")
    threshold = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    ).oscillation_gain
    return floor(nextafter(threshold / a, inf)) + 1


def maximum_integer_gap_for_stable_response(
    *,
    evolutionary_persistence: float,
    community_memory: float,
    gain_per_structural_gap: float,
) -> int:
    """Largest nonnegative integer Delta_g with a*Delta_g < G_+.

    ``nextafter`` nudges the strict upper boundary downward so an exact integer
    ratio ``G_+/a`` remains excluded from the stable region.
    """

    a = float(gain_per_structural_gap)
    if not isfinite(a) or a <= 0.0:
        raise ValueError("gain_per_structural_gap must be finite and positive")
    upper = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    ).upper_stability_gain
    return max(0, floor(nextafter(upper / a, -inf)))


def bounded_arity_gap_ceiling_over_adaptive_depth(
    world_count: int,
    query_count: int,
    max_arity: int,
    *,
    frontier_edge_cap: int | None = None,
) -> int:
    """One-sided max Delta_g ceiling over all possible positive adaptive costs."""

    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    if frontier_edge_cap is not None and (
        type(frontier_edge_cap) is not int or frontier_edge_cap < 1
    ):
        raise ValueError("frontier_edge_cap must be a positive integer when supplied")

    best = 0
    # If h>m, then C_F<=m<h=C_A, so no positive structural gap is possible.
    max_relevant_h = min(world_count - 1, query_count)
    # Likewise if a frontier edge cap E is declared, C_F<=E means h>=E cannot
    # contribute a positive gap.
    if frontier_edge_cap is not None:
        max_relevant_h = min(max_relevant_h, frontier_edge_cap - 1)
    if max_relevant_h < 1:
        return 0

    for h in range(1, max_relevant_h + 1):
        fixed_ceiling = min(
            query_count,
            maximum_bounded_arity_tree_internal_nodes(
                world_count,
                h,
                max_arity,
            ),
        )
        if frontier_edge_cap is not None:
            fixed_ceiling = min(fixed_ceiling, frontier_edge_cap)
        best = max(best, fixed_ceiling - h)
    return max(0, best)


@dataclass(frozen=True)
class OscillationScopeReceipt:
    evolutionary_persistence: float
    community_memory: float
    gain_per_structural_gap: float
    oscillation_gain: float
    upper_stability_gain: float
    minimum_oscillatory_gap: int
    maximum_stable_gap: int
    binary_worlds_below_threshold: int
    binary_queries_below_threshold: int
    binary_frontier_edges_below_threshold: int
    witness_world_count: int
    witness_query_count: int
    witness_max_arity: int
    witness_frontier_edge_count: int
    witness_adaptive_cost: int
    witness_fixed_cost: int
    witness_gap: int
    witness_generalized_gain: float
    witness_stable: bool
    witness_oscillatory: bool
    theorem_holds: bool
    scope: str = "first_binary_structural_scope_reaching_oscillatory_feedback"


def first_binary_oscillation_scope_receipt() -> OscillationScopeReceipt:
    """Exact canonical threshold: 6 worlds, 5 queries, 5 frontier edges.

    The declared response geometry is alpha=1, phi=1/2, and gain per unit
    structural gap a=1/8.
    """

    alpha = 1.0
    phi = 0.5
    a = 0.125
    thresholds = general_response_thresholds(alpha, phi)
    required_gap = minimum_integer_gap_for_oscillation(
        evolutionary_persistence=alpha,
        community_memory=phi,
        gain_per_structural_gap=a,
    )
    max_stable_gap = maximum_integer_gap_for_stable_response(
        evolutionary_persistence=alpha,
        community_memory=phi,
        gain_per_structural_gap=a,
    )

    # World threshold: with binary queries, every task on <=5 represented worlds
    # has inherited gap ceiling at most one, even with arbitrarily many queries.
    worlds_below = 5
    for n in range(2, worlds_below + 1):
        ceiling = max(
            maximum_bounded_arity_tree_internal_nodes(n, h, 2) - h
            for h in range(1, n)
        )
        if ceiling >= required_gap:
            raise ArithmeticError("binary world threshold exclusion failed")

    # Query threshold: for any world count, m<=4 cannot realize gap two under
    # binary routing.  h>m cannot contribute a positive gap, so a world budget
    # large enough to saturate all h<=4 binary trees is sufficient.
    queries_below = 4
    generous_worlds = 16
    for m in range(1, queries_below + 1):
        ceiling = bounded_arity_gap_ceiling_over_adaptive_depth(
            generous_worlds,
            m,
            2,
        )
        if ceiling >= required_gap:
            raise ArithmeticError("binary query threshold exclusion failed")

    # Productive-frontier edge threshold: E<=4 likewise caps every binary gap at
    # one.  Use generous world/query budgets so only the edge cap is active.
    frontier_edges_below = 4
    for edge_cap in range(1, frontier_edges_below + 1):
        ceiling = bounded_arity_gap_ceiling_over_adaptive_depth(
            generous_worlds,
            generous_worlds,
            2,
            frontier_edge_cap=edge_cap,
        )
        if ceiling >= required_gap:
            raise ArithmeticError("binary frontier-edge threshold exclusion failed")

    # Constructive sharp witness at the first joint scope.
    witness = sharp_bounded_arity_unit_cost_witness(6, 5, 2)
    ca = adaptive_minimum_resolution(witness).minimum_worst_path_cost
    cf = fixed_minimum_resolution(witness).minimum_cost
    if ca is None or cf is None:
        raise ArithmeticError("binary oscillation witness was unresolved")
    gap = cf - ca
    frontier = build_productive_frontier(witness)
    frontier_edge_count = len(frontier.minimal_productive_sets)
    gain = a * gap
    stable = thresholds.lower_stability_gain < gain < thresholds.upper_stability_gain
    oscillatory = gain > thresholds.oscillation_gain

    theorem_holds = (
        required_gap == 2
        and max_stable_gap == 7
        and ca == 3
        and cf == 5
        and gap == 2
        and frontier_edge_count == 5
        and stable
        and oscillatory
    )
    if not theorem_holds:
        raise ArithmeticError("first binary oscillation scope theorem failed")

    return OscillationScopeReceipt(
        evolutionary_persistence=alpha,
        community_memory=phi,
        gain_per_structural_gap=a,
        oscillation_gain=thresholds.oscillation_gain,
        upper_stability_gain=thresholds.upper_stability_gain,
        minimum_oscillatory_gap=required_gap,
        maximum_stable_gap=max_stable_gap,
        binary_worlds_below_threshold=worlds_below,
        binary_queries_below_threshold=queries_below,
        binary_frontier_edges_below_threshold=frontier_edges_below,
        witness_world_count=6,
        witness_query_count=5,
        witness_max_arity=2,
        witness_frontier_edge_count=frontier_edge_count,
        witness_adaptive_cost=ca,
        witness_fixed_cost=cf,
        witness_gap=gap,
        witness_generalized_gain=gain,
        witness_stable=stable,
        witness_oscillatory=oscillatory,
        theorem_holds=theorem_holds,
    )
