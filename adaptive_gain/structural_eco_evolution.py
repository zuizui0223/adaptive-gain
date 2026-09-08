"""Structural eco-evolution bridge built from the repository's exact costs.

A community state is represented, at the sensing layer, by a ``FiniteTask``.
Two heritable sensory architectures are compared:

* A: outcome-contingent sensing, paying the adaptive worst-path cost C_A;
* F: a fixed sensing architecture, paying the fixed resolving cost C_F.

If one unit of saved sensing cost contributes ``lambda_cost`` log-fitness units
and contingent control has log-fitness cost ``control_cost``, then

    s(X) = log(W_A/W_F) = lambda_cost * (C_F - C_A) - control_cost.

Under haploid viability selection with no mutation or frequency dependence,
log odds evolve exactly by addition of these state-dependent coefficients:

    logit(p_{t+1}) = logit(p_t) + s(X_t).

This makes the repository's deterministic structural gap a direct input to a
minimal fluctuating-selection model.  The population-genetic recurrence itself
is standard; the new bridge is the identification of s(X) with the exact
adaptive-vs-fixed structural cost gap and its existing decomposition.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log
from typing import Iterable, Sequence

from .core import FiniteTask, adaptive_gain_receipt
from .decomposition import optimal_policy_cost_decomposition


@dataclass(frozen=True)
class StructuralSelectionState:
    adaptive_cost: int
    fixed_cost: int
    structural_gap: int
    lambda_cost: float
    control_cost: float
    log_fitness_ratio: float


@dataclass(frozen=True)
class StructuralSelectionDecomposition:
    adaptive_cost: int
    fixed_cost: int
    policy_union_cost: int
    restricted_fixed_cost: int
    branch_exclusive_opportunity: int
    external_shortcut_discount: int
    internal_union_redundancy: int
    structural_gap: int
    scaled_branch_opportunity: float
    scaled_external_discount: float
    scaled_internal_redundancy: float
    control_cost: float
    log_fitness_ratio: float
    identity_holds: bool


def _validate_selection_parameters(lambda_cost: float, control_cost: float) -> tuple[float, float]:
    lam = float(lambda_cost)
    kappa = float(control_cost)
    if not isfinite(lam) or lam < 0:
        raise ValueError("lambda_cost must be finite and non-negative")
    if not isfinite(kappa) or kappa < 0:
        raise ValueError("control_cost must be finite and non-negative")
    return lam, kappa


def structural_selection_state(
    task: FiniteTask,
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
) -> StructuralSelectionState:
    """Map one finite ecological sensing task to a log-fitness selection state."""

    lam, kappa = _validate_selection_parameters(lambda_cost, control_cost)
    receipt = adaptive_gain_receipt(task)
    if receipt.adaptive_cost is None or receipt.fixed_cost is None:
        raise ValueError("task must be resolvable by the declared query vocabulary")
    gap = receipt.fixed_cost - receipt.adaptive_cost
    s = lam * gap - kappa
    return StructuralSelectionState(
        adaptive_cost=receipt.adaptive_cost,
        fixed_cost=receipt.fixed_cost,
        structural_gap=gap,
        lambda_cost=lam,
        control_cost=kappa,
        log_fitness_ratio=s,
    )


def structural_selection_decomposition(
    task: FiniteTask,
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
) -> StructuralSelectionDecomposition:
    """Lift the repository's U/C_A/C_F/C_U identity to log-fitness units.

    Since

        C_F - C_A = (U - C_A) - (C_U - C_F) - (U - C_U),

    selection for contingent sensing can be read as branch-exclusive opportunity
    minus external shortcut discount minus internal union redundancy, followed by
    the constitutive control cost.
    """

    lam, kappa = _validate_selection_parameters(lambda_cost, control_cost)
    dec = optimal_policy_cost_decomposition(task)
    required = (
        dec.adaptive_cost,
        dec.fixed_cost,
        dec.policy_union_cost,
        dec.policy_union_restricted_fixed_cost,
        dec.branch_exclusive_overhead,
        dec.external_shortcut_discount,
        dec.internal_union_redundancy,
        dec.realized_adaptive_gain,
    )
    if any(value is None for value in required):
        raise ValueError("task must have a resolved selected adaptive policy")

    ca = int(dec.adaptive_cost)
    cf = int(dec.fixed_cost)
    U = int(dec.policy_union_cost)
    cu = int(dec.policy_union_restricted_fixed_cost)
    overhead = int(dec.branch_exclusive_overhead)
    external = int(dec.external_shortcut_discount)
    internal = int(dec.internal_union_redundancy)
    gap = int(dec.realized_adaptive_gain)
    identity = gap == overhead - external - internal == cf - ca
    if not identity:
        raise ArithmeticError("structural selection decomposition identity failed")

    scaled_overhead = lam * overhead
    scaled_external = lam * external
    scaled_internal = lam * internal
    s = scaled_overhead - scaled_external - scaled_internal - kappa
    if abs(s - (lam * gap - kappa)) > 1e-12:
        raise ArithmeticError("scaled structural selection identity failed")

    return StructuralSelectionDecomposition(
        adaptive_cost=ca,
        fixed_cost=cf,
        policy_union_cost=U,
        restricted_fixed_cost=cu,
        branch_exclusive_opportunity=overhead,
        external_shortcut_discount=external,
        internal_union_redundancy=internal,
        structural_gap=gap,
        scaled_branch_opportunity=scaled_overhead,
        scaled_external_discount=scaled_external,
        scaled_internal_redundancy=scaled_internal,
        control_cost=kappa,
        log_fitness_ratio=s,
        identity_holds=identity,
    )


def structural_selection_path(
    tasks: Sequence[FiniteTask],
    *,
    lambda_cost: float = 1.0,
    control_cost: float = 0.0,
) -> tuple[float, ...]:
    """Return state-dependent log-fitness ratios for a community-state sequence."""

    if not tasks:
        raise ValueError("tasks must be non-empty")
    return tuple(
        structural_selection_state(
            task,
            lambda_cost=lambda_cost,
            control_cost=control_cost,
        ).log_fitness_ratio
        for task in tasks
    )


def logit(p: float) -> float:
    p = float(p)
    if not (0.0 < p < 1.0):
        raise ValueError("frequency must lie strictly between 0 and 1")
    return log(p / (1.0 - p))


def logistic(x: float) -> float:
    x = float(x)
    if x >= 0:
        z = exp(-x)
        return 1.0 / (1.0 + z)
    z = exp(x)
    return z / (1.0 + z)


def update_frequency_by_log_fitness_ratio(p: float, s: float) -> float:
    """Exact one-generation haploid viability-selection update."""

    p = float(p)
    s = float(s)
    if not (0.0 <= p <= 1.0):
        raise ValueError("frequency must lie in [0, 1]")
    if not isfinite(s):
        raise ValueError("log fitness ratio must be finite")
    if p in (0.0, 1.0):
        return p
    return logistic(logit(p) + s)


def frequency_path(initial_frequency: float, selection: Iterable[float]) -> tuple[float, ...]:
    """Return frequencies including the initial state and all subsequent generations."""

    p = float(initial_frequency)
    if not (0.0 <= p <= 1.0):
        raise ValueError("initial_frequency must lie in [0, 1]")
    out = [p]
    for s in selection:
        p = update_frequency_by_log_fitness_ratio(p, float(s))
        out.append(p)
    return tuple(out)


def cumulative_log_odds_change(selection: Iterable[float]) -> float:
    """Exact total log-odds displacement under the minimal selection model."""

    return sum(float(s) for s in selection)


def evolutionary_selection_activity(selection: Iterable[float]) -> float:
    """Total absolute log-odds pressure experienced across generations."""

    return sum(abs(float(s)) for s in selection)


def evolutionary_selection_retention(selection: Iterable[float]) -> float:
    """Absolute retained log-odds displacement after temporal cancellation."""

    return abs(cumulative_log_odds_change(selection))


def evolutionary_selection_retention_ratio(selection: Iterable[float]) -> float:
    """Retained log-odds change divided by total absolute selection activity."""

    values = tuple(float(s) for s in selection)
    if not values:
        raise ValueError("selection must be non-empty")
    activity = evolutionary_selection_activity(values)
    if activity == 0.0:
        return 0.0
    return evolutionary_selection_retention(values) / activity


def symmetric_switching_control_cost(
    gap_high: float,
    gap_low: float,
    *,
    lambda_cost: float = 1.0,
) -> float:
    """Control cost making high/low structural states exert equal opposite selection."""

    lam = float(lambda_cost)
    if lam < 0 or not isfinite(lam):
        raise ValueError("lambda_cost must be finite and non-negative")
    high = float(gap_high)
    low = float(gap_low)
    if high < low:
        raise ValueError("gap_high must be at least gap_low")
    return lam * (high + low) / 2.0
