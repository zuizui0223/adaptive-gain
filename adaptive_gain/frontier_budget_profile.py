"""Reconstruct deterministic guarantee budget profiles from compact sufficient objects.

For exact guaranteed target resolution, the adaptive and fixed feasibility curves
are step functions at C_A and C_F.  Hence any representation preserving those
two minima preserves the entire binary guarantee budget profile.

This module obtains C_A from the cost-only continuation quotient and C_F (plus
all optimal fixed bundles) from the static minimal productive frontier built
directly from cross-target pair incidence.
"""
from __future__ import annotations

from dataclasses import dataclass

from .continuation_bisimulation import build_continuation_quotient, continuation_quotient_costs
from .core import BudgetResolutionRow, FiniteTask, fixed_minimum_resolution, resolution_budget_profile
from .minimal_productive_frontier import (
    build_minimal_productive_frontier_from_pair_incidence,
    minimal_frontier_fixed_minimum_resolution,
)


@dataclass(frozen=True)
class FrontierBudgetProfileAudit:
    adaptive_cost: int | None
    fixed_cost: int | None
    profile: tuple[BudgetResolutionRow, ...]
    direct_profile: tuple[BudgetResolutionRow, ...]
    frontier_optimal_fixed_bundles: tuple[tuple[str, ...], ...]
    direct_optimal_fixed_bundles: tuple[tuple[str, ...], ...]
    profile_agrees: bool
    optimal_fixed_bundles_agree: bool
    exact_agrees: bool
    static_frontier_used_reachable_state_enumeration: bool = False
    scope: str = "deterministic_guarantee_budget_profile_from_continuation_and_static_frontier"


def frontier_resolution_budget_profile(
    task: FiniteTask,
    max_budget: int,
) -> tuple[BudgetResolutionRow, ...]:
    if not isinstance(task, FiniteTask):
        raise ValueError("task must be a FiniteTask")
    if type(max_budget) is not int or max_budget < 0:
        raise ValueError("max_budget must be a nonnegative integer")

    continuation = build_continuation_quotient((task,))
    ca = continuation_quotient_costs((task,), continuation)[0]
    frontier = build_minimal_productive_frontier_from_pair_incidence(task)
    fixed = minimal_frontier_fixed_minimum_resolution(frontier)
    cf = fixed.minimum_cost
    if (ca is None) != (cf is None):
        raise ArithmeticError("adaptive/fixed feasibility classes disagreed")

    rows = []
    for budget in range(max_budget + 1):
        adaptive = ca is not None and ca <= budget
        fixed_ok = cf is not None and cf <= budget
        rows.append(BudgetResolutionRow(budget, adaptive, fixed_ok, adaptive and not fixed_ok))
    return tuple(rows)


def frontier_budget_profile_audit(
    task: FiniteTask,
    max_budget: int,
) -> FrontierBudgetProfileAudit:
    profile = frontier_resolution_budget_profile(task, max_budget)
    direct_profile = resolution_budget_profile(task, max_budget)

    continuation = build_continuation_quotient((task,))
    ca = continuation_quotient_costs((task,), continuation)[0]
    frontier = build_minimal_productive_frontier_from_pair_incidence(task)
    frontier_fixed = minimal_frontier_fixed_minimum_resolution(frontier)
    direct_fixed = fixed_minimum_resolution(task)
    cf = frontier_fixed.minimum_cost

    profile_agrees = profile == direct_profile
    bundles_agree = frontier_fixed.optimal_bundles == direct_fixed.optimal_bundles
    exact = profile_agrees and bundles_agree and cf == direct_fixed.minimum_cost
    if not exact:
        raise ArithmeticError("compact frontier budget-profile audit disagreed with direct solver")

    return FrontierBudgetProfileAudit(
        ca,
        cf,
        profile,
        direct_profile,
        frontier_fixed.optimal_bundles,
        direct_fixed.optimal_bundles,
        profile_agrees,
        bundles_agree,
        exact,
    )
