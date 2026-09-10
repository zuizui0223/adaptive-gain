"""Selection changes induced by transitions between finite sensing tasks.

Under the minimal structural fitness map

    s(X) = lambda * [C_F(X) - C_A(X)] - kappa(X),

a transition X -> Y obeys the exact algebraic decomposition

    Delta s
      = lambda * Delta C_F
      - lambda * Delta C_A
      - Delta kappa.

The first term is the fixed/productive-frontier channel; the second is the
adaptive-continuation channel.  This is a bookkeeping corollary of the
repository's exact C_A/C_F theory, intended to make eco-to-evo changes explicit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .core import FiniteTask
from .structural_eco_evolution import structural_selection_state


@dataclass(frozen=True)
class StructuralSelectionTransition:
    adaptive_cost_from: int
    adaptive_cost_to: int
    fixed_cost_from: int
    fixed_cost_to: int
    structural_gap_from: int
    structural_gap_to: int
    delta_adaptive_cost: int
    delta_fixed_cost: int
    delta_structural_gap: int
    fixed_frontier_channel: float
    adaptive_continuation_channel: float
    control_channel: float
    delta_log_fitness_ratio: float
    identity_holds: bool


def structural_selection_transition(
    task_from: FiniteTask,
    task_to: FiniteTask,
    *,
    lambda_cost: float = 1.0,
    control_cost_from: float = 0.0,
    control_cost_to: float = 0.0,
) -> StructuralSelectionTransition:
    """Decompose a community-state transition into exact selection channels."""

    lam = float(lambda_cost)
    if not isfinite(lam) or lam < 0:
        raise ValueError("lambda_cost must be finite and non-negative")

    before = structural_selection_state(
        task_from,
        lambda_cost=lam,
        control_cost=control_cost_from,
    )
    after = structural_selection_state(
        task_to,
        lambda_cost=lam,
        control_cost=control_cost_to,
    )

    dca = after.adaptive_cost - before.adaptive_cost
    dcf = after.fixed_cost - before.fixed_cost
    dgap = after.structural_gap - before.structural_gap
    dkappa = float(control_cost_to) - float(control_cost_from)

    fixed_channel = lam * dcf
    adaptive_channel = -lam * dca
    control_channel = -dkappa
    delta_s = after.log_fitness_ratio - before.log_fitness_ratio
    reconstructed = fixed_channel + adaptive_channel + control_channel
    identity = abs(delta_s - reconstructed) <= 1e-12
    if not identity:
        raise ArithmeticError("selection transition decomposition identity failed")

    return StructuralSelectionTransition(
        adaptive_cost_from=before.adaptive_cost,
        adaptive_cost_to=after.adaptive_cost,
        fixed_cost_from=before.fixed_cost,
        fixed_cost_to=after.fixed_cost,
        structural_gap_from=before.structural_gap,
        structural_gap_to=after.structural_gap,
        delta_adaptive_cost=dca,
        delta_fixed_cost=dcf,
        delta_structural_gap=dgap,
        fixed_frontier_channel=fixed_channel,
        adaptive_continuation_channel=adaptive_channel,
        control_channel=control_channel,
        delta_log_fitness_ratio=delta_s,
        identity_holds=identity,
    )
