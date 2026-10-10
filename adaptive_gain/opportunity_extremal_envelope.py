"""Sharp opportunity-weighted adaptive advantage under finite structural budgets."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

from .bounded_arity_extremal_bounds import bounded_arity_fixed_cost_bound


@dataclass(frozen=True)
class OpportunityEnvelopeRow:
    adaptive_cost: int
    sharp_fixed_cost: int
    structural_gap: int
    opportunity_advantage: float


@dataclass(frozen=True)
class OpportunityEnvelopeReceipt:
    world_count: int
    query_count: int
    max_arity: int
    sharp_opportunity_advantage: float
    maximizing_adaptive_costs: tuple[int, ...]
    rows: tuple[OpportunityEnvelopeRow, ...]
    scope: str = "sharp_guarantee_level_opportunity_advantage"


@dataclass(frozen=True)
class LogSelectionEnvelopeReceipt:
    world_count: int
    query_count: int
    max_arity: int
    sharp_log_selection: float
    maximizing_adaptive_costs: tuple[int, ...]
    maintenance_log_cost: float
    scope: str = "sharp_guarantee_level_log_selection"


def _validate_counts(world_count: int, query_count: int, max_arity: int) -> None:
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")


def _survival_values(
    world_count: int,
    query_count: int,
    survival: Callable[[float], float],
) -> dict[int, float]:
    maximum_cost = max(world_count - 1, query_count)
    values: dict[int, float] = {}
    previous = None
    for cost in range(maximum_cost + 1):
        value = float(survival(float(cost)))
        if not math.isfinite(value) or not (0.0 <= value <= 1.0):
            raise ValueError("survival values must be finite and lie in [0, 1]")
        if previous is not None and value > previous + 1e-12:
            raise ValueError("survival must be nonincreasing on the relevant costs")
        values[cost] = value
        previous = value
    return values



def sharp_completion_value_envelope(
    world_count: int,
    query_count: int,
    max_arity: int,
    completion_value: Callable[[float], float],
) -> OpportunityEnvelopeReceipt:
    """Exact maximum robust statewise margin U(C_A)-U(C_F)."""
    _validate_counts(world_count, query_count, max_arity)

    maximum_cost = max(world_count - 1, query_count)
    values: dict[int, float] = {}
    previous = None
    for cost in range(maximum_cost + 1):
        value = float(completion_value(float(cost)))
        if not math.isfinite(value):
            raise ValueError("completion_value must be finite on relevant costs")
        if previous is not None and value > previous + 1e-12:
            raise ValueError("completion_value must be nonincreasing")
        values[cost] = value
        previous = value

    rows: list[OpportunityEnvelopeRow] = []
    max_depth = min(world_count - 1, query_count)
    for depth in range(1, max_depth + 1):
        fixed = bounded_arity_fixed_cost_bound(
            world_count,
            query_count,
            depth,
            max_arity,
        )
        advantage = values[depth] - values[fixed]
        rows.append(
            OpportunityEnvelopeRow(
                depth,
                fixed,
                fixed - depth,
                advantage,
            )
        )

    optimum = max(row.opportunity_advantage for row in rows)
    maximizing = tuple(
        row.adaptive_cost
        for row in rows
        if math.isclose(
            row.opportunity_advantage,
            optimum,
            rel_tol=0.0,
            abs_tol=1e-12,
        )
    )
    return OpportunityEnvelopeReceipt(
        world_count,
        query_count,
        max_arity,
        optimum,
        maximizing,
        tuple(rows),
        scope="sharp_monotone_completion_value_advantage",
    )


def sharp_opportunity_advantage_envelope(
    world_count: int,
    query_count: int,
    max_arity: int,
    survival: Callable[[float], float],
    *,
    resolution_value: float = 1.0,
) -> OpportunityEnvelopeReceipt:
    """Exact maximum v[S(C_A)-S(C_F)] over the declared structural scope."""
    _validate_counts(world_count, query_count, max_arity)
    if not math.isfinite(resolution_value) or resolution_value < 0:
        raise ValueError("resolution_value must be finite and nonnegative")

    _survival_values(world_count, query_count, survival)
    base = sharp_completion_value_envelope(
        world_count,
        query_count,
        max_arity,
        lambda c: resolution_value * float(survival(c)),
    )
    return OpportunityEnvelopeReceipt(
        base.world_count,
        base.query_count,
        base.max_arity,
        base.sharp_opportunity_advantage,
        base.maximizing_adaptive_costs,
        base.rows,
        scope="sharp_guarantee_level_opportunity_advantage",
    )


def sharp_log_selection_envelope(
    world_count: int,
    query_count: int,
    max_arity: int,
    survival: Callable[[float], float],
    *,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
    maintenance_log_cost: float = 0.0,
) -> LogSelectionEnvelopeReceipt:
    """Exact maximum robust guarantee-level log-value advantage in the scope."""
    _validate_counts(world_count, query_count, max_arity)
    if not math.isfinite(baseline_fitness) or baseline_fitness <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value < 0:
        raise ValueError("resolution_value must be finite and nonnegative")
    if not math.isfinite(maintenance_log_cost) or maintenance_log_cost < 0:
        raise ValueError("maintenance_log_cost must be finite and nonnegative")

    s = _survival_values(world_count, query_count, survival)
    rows = []
    max_depth = min(world_count - 1, query_count)
    for depth in range(1, max_depth + 1):
        fixed = bounded_arity_fixed_cost_bound(
            world_count,
            query_count,
            depth,
            max_arity,
        )
        value = (
            math.log(
                (baseline_fitness + resolution_value * s[depth])
                / (baseline_fitness + resolution_value * s[fixed])
            )
            - maintenance_log_cost
        )
        rows.append((depth, value))

    optimum = max(value for _, value in rows)
    maximizing = tuple(
        depth
        for depth, value in rows
        if math.isclose(value, optimum, rel_tol=0.0, abs_tol=1e-12)
    )
    return LogSelectionEnvelopeReceipt(
        world_count,
        query_count,
        max_arity,
        optimum,
        maximizing,
        maintenance_log_cost,
    )


def sharp_exponential_opportunity_envelope(
    world_count: int,
    query_count: int,
    max_arity: int,
    *,
    closure_rate: float,
    resolution_value: float = 1.0,
) -> OpportunityEnvelopeReceipt:
    """Convenience wrapper for S(c)=exp(-mu*c)."""
    if not math.isfinite(closure_rate) or closure_rate <= 0:
        raise ValueError("closure_rate must be finite and positive")
    return sharp_opportunity_advantage_envelope(
        world_count,
        query_count,
        max_arity,
        lambda c: math.exp(-closure_rate * c),
        resolution_value=resolution_value,
    )



def sharp_maintenance_log_cost_ceiling(
    world_count: int,
    query_count: int,
    max_arity: int,
    survival: Callable[[float], float],
    *,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
) -> float:
    """Largest log maintenance cost supportable with positive value in every world."""
    receipt = sharp_log_selection_envelope(
        world_count,
        query_count,
        max_arity,
        survival,
        baseline_fitness=baseline_fitness,
        resolution_value=resolution_value,
        maintenance_log_cost=0.0,
    )
    return receipt.sharp_log_selection


def robust_positive_advantage_possible_in_scope(
    world_count: int,
    query_count: int,
    max_arity: int,
    survival: Callable[[float], float],
    *,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
    maintenance_log_cost: float = 0.0,
) -> bool:
    """Whether some task can keep the adaptive net advantage positive in every world.

    This is a distribution-free robust criterion derived from worst-path
    completion. It is not a necessary condition for positive expected selection
    under a particular nonuniform world distribution.
    """
    if not math.isfinite(maintenance_log_cost) or maintenance_log_cost < 0:
        raise ValueError("maintenance_log_cost must be finite and nonnegative")
    ceiling = sharp_maintenance_log_cost_ceiling(
        world_count,
        query_count,
        max_arity,
        survival,
        baseline_fitness=baseline_fitness,
        resolution_value=resolution_value,
    )
    return maintenance_log_cost < ceiling - 1e-15
