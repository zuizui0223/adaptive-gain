"""Budget-gated evolutionary selection from the exact adaptive-gain window.

The deterministic repository proves C_A <= C_F.  For a hard ecological sensing
budget B, the contingent architecture can resolve the target exactly when
C_A <= B, while the fixed architecture can do so exactly when C_F <= B.
Therefore the difference in binary resolution success is

    1{C_A <= B < C_F}.

This module converts that exact budget window into a minimal fitness model
without assuming that each unit of sensing cost has a linear fitness value.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log
from typing import Iterable, Sequence

from .core import FiniteTask, adaptive_gain_receipt
from .structural_eco_evolution import frequency_path


@dataclass(frozen=True)
class BudgetResolutionState:
    adaptive_cost: int
    fixed_cost: int
    budget: float
    adaptive_resolves: bool
    fixed_resolves: bool
    adaptive_only_window: bool


@dataclass(frozen=True)
class BudgetFitnessState:
    resolution: BudgetResolutionState
    baseline_fitness: float
    resolution_benefit: float
    contingent_maintenance_log_cost: float
    adaptive_fitness: float
    fixed_fitness: float
    log_fitness_ratio: float


def _validate_budget(budget: float) -> float:
    B = float(budget)
    if not isfinite(B) or B < 0:
        raise ValueError("budget must be finite and non-negative")
    return B


def budget_resolution_state(task: FiniteTask, budget: float) -> BudgetResolutionState:
    """Evaluate exact deterministic resolution feasibility under budget B."""

    B = _validate_budget(budget)
    receipt = adaptive_gain_receipt(task)
    if receipt.adaptive_cost is None or receipt.fixed_cost is None:
        raise ValueError("task must be resolvable by the declared query vocabulary")
    ca = int(receipt.adaptive_cost)
    cf = int(receipt.fixed_cost)
    adaptive_ok = ca <= B
    fixed_ok = cf <= B
    adaptive_only = adaptive_ok and not fixed_ok
    if fixed_ok and not adaptive_ok:
        raise ArithmeticError("C_A <= C_F invariant violated")
    return BudgetResolutionState(
        adaptive_cost=ca,
        fixed_cost=cf,
        budget=B,
        adaptive_resolves=adaptive_ok,
        fixed_resolves=fixed_ok,
        adaptive_only_window=adaptive_only,
    )


def budget_fitness_state(
    task: FiniteTask,
    budget: float,
    *,
    baseline_fitness: float = 1.0,
    resolution_benefit: float = 1.0,
    contingent_maintenance_log_cost: float = 0.0,
) -> BudgetFitnessState:
    """Map deterministic resolution success to a simple positive fitness model.

    Fitness before contingent maintenance cost is

        baseline_fitness + resolution_benefit * 1{architecture resolves}.

    The adaptive architecture additionally pays a multiplicative maintenance
    factor exp(-kappa), so

        W_A = exp(-kappa) * (w0 + v * 1{C_A <= B})
        W_F =               (w0 + v * 1{C_F <= B}).

    This is deliberately minimal and keeps all fitnesses strictly positive.
    """

    w0 = float(baseline_fitness)
    v = float(resolution_benefit)
    kappa = float(contingent_maintenance_log_cost)
    if not isfinite(w0) or w0 <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    if not isfinite(v) or v < 0:
        raise ValueError("resolution_benefit must be finite and non-negative")
    if not isfinite(kappa) or kappa < 0:
        raise ValueError("contingent_maintenance_log_cost must be finite and non-negative")

    resolution = budget_resolution_state(task, budget)
    wa = exp(-kappa) * (w0 + v * float(resolution.adaptive_resolves))
    wf = w0 + v * float(resolution.fixed_resolves)
    return BudgetFitnessState(
        resolution=resolution,
        baseline_fitness=w0,
        resolution_benefit=v,
        contingent_maintenance_log_cost=kappa,
        adaptive_fitness=wa,
        fixed_fitness=wf,
        log_fitness_ratio=log(wa / wf),
    )


def maximum_maintenance_cost_for_adaptive_advantage(
    *, baseline_fitness: float = 1.0, resolution_benefit: float = 1.0
) -> float:
    """Critical kappa inside an adaptive-only budget window.

    If C_A <= B < C_F, adaptive sensing is favoured exactly when

        kappa < log((w0 + v) / w0).
    """

    w0 = float(baseline_fitness)
    v = float(resolution_benefit)
    if not isfinite(w0) or w0 <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    if not isfinite(v) or v < 0:
        raise ValueError("resolution_benefit must be finite and non-negative")
    return log((w0 + v) / w0)


def budget_selection_path(
    tasks: Sequence[FiniteTask],
    budgets: Sequence[float] | float,
    *,
    baseline_fitness: float = 1.0,
    resolution_benefit: float = 1.0,
    contingent_maintenance_log_cost: float = 0.0,
) -> tuple[float, ...]:
    """Return generation-specific log-fitness ratios under hard sensing budgets."""

    if not tasks:
        raise ValueError("tasks must be non-empty")
    if isinstance(budgets, (int, float)):
        Bs = tuple(float(budgets) for _ in tasks)
    else:
        Bs = tuple(float(x) for x in budgets)
        if len(Bs) != len(tasks):
            raise ValueError("budgets sequence must match tasks length")
    return tuple(
        budget_fitness_state(
            task,
            B,
            baseline_fitness=baseline_fitness,
            resolution_benefit=resolution_benefit,
            contingent_maintenance_log_cost=contingent_maintenance_log_cost,
        ).log_fitness_ratio
        for task, B in zip(tasks, Bs)
    )


def budget_frequency_path(
    initial_frequency: float,
    tasks: Sequence[FiniteTask],
    budgets: Sequence[float] | float,
    *,
    baseline_fitness: float = 1.0,
    resolution_benefit: float = 1.0,
    contingent_maintenance_log_cost: float = 0.0,
) -> tuple[float, ...]:
    """Exact haploid frequency path driven by budget-gated structural selection."""

    selection = budget_selection_path(
        tasks,
        budgets,
        baseline_fitness=baseline_fitness,
        resolution_benefit=resolution_benefit,
        contingent_maintenance_log_cost=contingent_maintenance_log_cost,
    )
    return frequency_path(initial_frequency, selection)
