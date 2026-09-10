"""Map generalized local feedback geometry to bounded-arity information scopes.

The generalized response supplies a strict integer structural-gap requirement
q_osc for entering the complex-eigenpair region and a largest integer gap that
remains below the upper stability boundary.  For a declared query-arity cap b,
this module composes those dynamic thresholds with the exact structural Pareto
frontier from ``arity_gap_pareto``.

Binary sensing is the special case in which the Pareto frontier collapses to one
componentwise first corner.  For b>2 the first stable oscillatory information
scope can contain multiple nondominated world/query/frontier tradeoffs.
"""

from __future__ import annotations

from dataclasses import dataclass

from .arity_gap_pareto import ArityGapParetoPoint, arity_gap_pareto_frontier
from .structural_oscillation_reachability import (
    maximum_integer_gap_for_stable_response,
    minimum_integer_gap_for_oscillation,
)


@dataclass(frozen=True)
class ArityOscillationParetoReceipt:
    evolutionary_persistence: float
    community_memory: float
    gain_per_structural_gap: float
    max_arity: int
    minimum_oscillatory_gap: int
    maximum_stable_gap: int
    stable_integer_oscillation_possible: bool
    pareto_frontier: tuple[ArityGapParetoPoint, ...]
    scope: str = "bounded_arity_pareto_scope_for_stable_oscillatory_feedback"


def stable_oscillation_pareto_scope(
    *,
    evolutionary_persistence: float,
    community_memory: float,
    gain_per_structural_gap: float,
    max_arity: int,
) -> ArityOscillationParetoReceipt:
    """Return the first bounded-arity information Pareto set for stable oscillation.

    The dynamic layer first determines the smallest integer gap strictly above
    ``G_osc`` and the largest integer gap strictly below ``G_+``.  If the former
    exceeds the latter, the unit-cost integer gap ladder skips the stable
    oscillatory region and the returned Pareto set is empty.
    """

    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")

    q = minimum_integer_gap_for_oscillation(
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
        gain_per_structural_gap=gain_per_structural_gap,
    )
    stable_max = maximum_integer_gap_for_stable_response(
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
        gain_per_structural_gap=gain_per_structural_gap,
    )
    possible = q <= stable_max
    frontier = arity_gap_pareto_frontier(q, max_arity) if possible else ()

    return ArityOscillationParetoReceipt(
        evolutionary_persistence=float(evolutionary_persistence),
        community_memory=float(community_memory),
        gain_per_structural_gap=float(gain_per_structural_gap),
        max_arity=max_arity,
        minimum_oscillatory_gap=q,
        maximum_stable_gap=stable_max,
        stable_integer_oscillation_possible=possible,
        pareto_frontier=frontier,
    )
