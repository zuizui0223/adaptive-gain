"""Opportunity-window fitness calculations."""
from __future__ import annotations

import math
from collections.abc import Callable, Sequence


def _validate_cost_pair(c_a: float, c_f: float) -> None:
    if not math.isfinite(c_a) or not math.isfinite(c_f):
        raise ValueError("costs must be finite")
    if c_a < 0 or c_f < 0:
        raise ValueError("costs must be nonnegative")
    if c_a > c_f:
        raise ValueError("require C_A <= C_F")


def opportunity_window_mass(
    c_a: float,
    c_f: float,
    survival: Callable[[float], float],
) -> float:
    """Return P(C_A <= B < C_F) from S(c)=P(B>=c)."""
    _validate_cost_pair(c_a, c_f)
    s_a = float(survival(c_a))
    s_f = float(survival(c_f))
    if not (math.isfinite(s_a) and math.isfinite(s_f)):
        raise ValueError("survival values must be finite")
    tol = 1e-12
    if s_a < -tol or s_a > 1 + tol or s_f < -tol or s_f > 1 + tol:
        raise ValueError("survival values must lie in [0, 1]")
    if s_a + tol < s_f:
        raise ValueError("survival function must be nonincreasing")
    return max(0.0, s_a - s_f)


def exponential_window_mass(
    c_a: float,
    c_f: float,
    closure_rate: float,
) -> float:
    """Window mass for exponentially distributed opportunity duration."""
    _validate_cost_pair(c_a, c_f)
    if not math.isfinite(closure_rate) or closure_rate < 0:
        raise ValueError("closure_rate must be finite and nonnegative")
    return (
        math.exp(-closure_rate * c_a)
        - math.exp(-closure_rate * c_f)
    )


def opportunity_benefit(
    c_a: float,
    c_f: float,
    survival: Callable[[float], float],
    value: float = 1.0,
) -> float:
    if not math.isfinite(value) or value < 0:
        raise ValueError("value must be finite and nonnegative")
    return value * opportunity_window_mass(c_a, c_f, survival)


def opportunity_selection_margin(
    c_a: float,
    c_f: float,
    survival: Callable[[float], float],
    value: float = 1.0,
    maintenance_cost: float = 0.0,
) -> float:
    if not math.isfinite(maintenance_cost) or maintenance_cost < 0:
        raise ValueError("maintenance_cost must be finite and nonnegative")
    return (
        opportunity_benefit(c_a, c_f, survival, value)
        - maintenance_cost
    )




def architecture_log_fitness(
    completion_cost: float,
    survival: Callable[[float], float],
    *,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
    maintenance_log_cost: float = 0.0,
) -> float:
    """Log expected fitness for one architecture with deterministic completion cost."""
    if not math.isfinite(completion_cost) or completion_cost < 0:
        raise ValueError("completion_cost must be finite and nonnegative")
    if not math.isfinite(baseline_fitness) or baseline_fitness <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value < 0:
        raise ValueError("resolution_value must be finite and nonnegative")
    if not math.isfinite(maintenance_log_cost) or maintenance_log_cost < 0:
        raise ValueError("maintenance_log_cost must be finite and nonnegative")

    success = float(survival(completion_cost))
    if not math.isfinite(success) or not (0.0 <= success <= 1.0):
        raise ValueError("survival values must lie in [0, 1]")
    return (
        math.log(baseline_fitness + resolution_value * success)
        - maintenance_log_cost
    )


def pairwise_architecture_log_selection(
    focal_cost: float,
    comparator_cost: float,
    survival: Callable[[float], float],
    *,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
    focal_maintenance_log_cost: float = 0.0,
    comparator_maintenance_log_cost: float = 0.0,
) -> float:
    """Log-fitness advantage of a focal architecture over any comparator."""
    focal = architecture_log_fitness(
        focal_cost,
        survival,
        baseline_fitness=baseline_fitness,
        resolution_value=resolution_value,
        maintenance_log_cost=focal_maintenance_log_cost,
    )
    comparator = architecture_log_fitness(
        comparator_cost,
        survival,
        baseline_fitness=baseline_fitness,
        resolution_value=resolution_value,
        maintenance_log_cost=comparator_maintenance_log_cost,
    )
    return focal - comparator

def opportunity_log_selection(
    c_a: float,
    c_f: float,
    survival: Callable[[float], float],
    *,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
    maintenance_log_cost: float = 0.0,
) -> float:
    """Exact log-fitness ratio for stochastic opportunity closure."""
    _validate_cost_pair(c_a, c_f)
    if not math.isfinite(baseline_fitness) or baseline_fitness <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value < 0:
        raise ValueError("resolution_value must be finite and nonnegative")
    if not math.isfinite(maintenance_log_cost) or maintenance_log_cost < 0:
        raise ValueError("maintenance_log_cost must be finite and nonnegative")

    s_a = float(survival(c_a))
    s_f = float(survival(c_f))
    if not (math.isfinite(s_a) and math.isfinite(s_f)):
        raise ValueError("survival values must be finite")
    if not (0.0 <= s_a <= 1.0 and 0.0 <= s_f <= 1.0):
        raise ValueError("survival values must lie in [0, 1]")
    if s_a < s_f:
        raise ValueError("survival function must be nonincreasing")

    return pairwise_architecture_log_selection(
        c_a,
        c_f,
        survival,
        baseline_fitness=baseline_fitness,
        resolution_value=resolution_value,
        focal_maintenance_log_cost=maintenance_log_cost,
        comparator_maintenance_log_cost=0.0,
    )


def hard_budget_log_selection(
    c_a: float,
    c_f: float,
    budget: float,
    *,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
    maintenance_log_cost: float = 0.0,
) -> float:
    """Degenerate-opportunity special case with a deterministic hard budget."""
    if not math.isfinite(budget) or budget < 0:
        raise ValueError("budget must be finite and nonnegative")
    survival = lambda c: 1.0 if budget >= c else 0.0
    return opportunity_log_selection(
        c_a,
        c_f,
        survival,
        baseline_fitness=baseline_fitness,
        resolution_value=resolution_value,
        maintenance_log_cost=maintenance_log_cost,
    )

def exponential_optimal_closure_rate(c_a: float, c_f: float) -> float:
    """Unique closure rate maximizing exponential opportunity-window mass."""
    _validate_cost_pair(c_a, c_f)
    if not (0 < c_a < c_f):
        raise ValueError("require 0 < C_A < C_F")
    return math.log(c_f / c_a) / (c_f - c_a)


def exponential_max_window_mass(c_a: float, c_f: float) -> float:
    _validate_cost_pair(c_a, c_f)
    if not (0 < c_a < c_f):
        raise ValueError("require 0 < C_A < C_F")
    gap = c_f - c_a
    return (gap / c_f) * (c_a / c_f) ** (c_a / gap)


def pathwise_expected_success(
    path_costs: Sequence[float],
    state_probabilities: Sequence[float],
    survival: Callable[[float], float],
) -> float:
    if len(path_costs) == 0 or len(path_costs) != len(state_probabilities):
        raise ValueError("inputs must have equal nonzero length")
    probs = [float(p) for p in state_probabilities]
    costs = [float(c) for c in path_costs]
    if any((not math.isfinite(c) or c < 0) for c in costs):
        raise ValueError("path costs must be finite and nonnegative")
    if any((not math.isfinite(p) or p < 0) for p in probs):
        raise ValueError("probabilities must be finite and nonnegative")
    if not math.isclose(sum(probs), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("state probabilities must sum to one")

    total = 0.0
    for p, c in zip(probs, costs):
        s = float(survival(c))
        if not math.isfinite(s) or not (0.0 <= s <= 1.0):
            raise ValueError("survival values must lie in [0, 1]")
        total += p * s
    return total


def pathwise_advantage_over_fixed(
    adaptive_path_costs: Sequence[float],
    state_probabilities: Sequence[float],
    fixed_cost: float,
    survival: Callable[[float], float],
    value: float = 1.0,
) -> float:
    if not math.isfinite(fixed_cost) or fixed_cost < 0:
        raise ValueError("fixed_cost must be finite and nonnegative")
    if not math.isfinite(value) or value < 0:
        raise ValueError("value must be finite and nonnegative")
    adaptive_success = pathwise_expected_success(
        adaptive_path_costs, state_probabilities, survival
    )
    fixed_success = float(survival(fixed_cost))
    if not math.isfinite(fixed_success) or not (0.0 <= fixed_success <= 1.0):
        raise ValueError("survival values must lie in [0, 1]")
    return value * (adaptive_success - fixed_success)



def empirical_timely_success_probability(
    completion_times: Sequence[float],
    opportunity_limits: Sequence[float],
) -> float:
    """Independent empirical plug-in estimate of P(T <= B).

    completion_times may contain math.inf to encode trials that never
    complete correctly. opportunity_limits must be finite and nonnegative.
    """
    if len(completion_times) == 0 or len(opportunity_limits) == 0:
        raise ValueError("empirical samples must be nonempty")

    times = [float(t) for t in completion_times]
    limits = [float(b) for b in opportunity_limits]

    if any(math.isnan(t) or t < 0 for t in times):
        raise ValueError("completion times must be nonnegative or infinity")
    if any((not math.isfinite(b) or b < 0) for b in limits):
        raise ValueError("opportunity limits must be finite and nonnegative")

    successful_pairs = sum(t <= b for t in times for b in limits)
    return successful_pairs / (len(times) * len(limits))


def empirical_performance_advantage(
    focal_completion_times: Sequence[float],
    comparator_completion_times: Sequence[float],
    opportunity_limits: Sequence[float],
    *,
    resolution_value: float = 1.0,
) -> float:
    """Plug-in performance advantage v[P(T_i<=B)-P(T_j<=B)]."""
    if not math.isfinite(resolution_value) or resolution_value < 0:
        raise ValueError("resolution_value must be finite and nonnegative")
    focal = empirical_timely_success_probability(
        focal_completion_times, opportunity_limits
    )
    comparator = empirical_timely_success_probability(
        comparator_completion_times, opportunity_limits
    )
    return resolution_value * (focal - comparator)


def empirical_pairwise_log_selection(
    focal_completion_times: Sequence[float],
    comparator_completion_times: Sequence[float],
    opportunity_limits: Sequence[float],
    *,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
    focal_maintenance_log_cost: float = 0.0,
    comparator_maintenance_log_cost: float = 0.0,
) -> float:
    """Plug-in log-fitness comparison from empirical T and B samples."""
    if not math.isfinite(baseline_fitness) or baseline_fitness <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value < 0:
        raise ValueError("resolution_value must be finite and nonnegative")
    if (
        not math.isfinite(focal_maintenance_log_cost)
        or focal_maintenance_log_cost < 0
        or not math.isfinite(comparator_maintenance_log_cost)
        or comparator_maintenance_log_cost < 0
    ):
        raise ValueError("maintenance log costs must be finite and nonnegative")

    q_focal = empirical_timely_success_probability(
        focal_completion_times, opportunity_limits
    )
    q_comparator = empirical_timely_success_probability(
        comparator_completion_times, opportunity_limits
    )
    return (
        math.log(
            (baseline_fitness + resolution_value * q_focal)
            / (baseline_fitness + resolution_value * q_comparator)
        )
        - (focal_maintenance_log_cost - comparator_maintenance_log_cost)
    )



def opportunity_log_recovery_exponential(
    saving: float,
    *,
    baseline_completion_cost: float,
    closure_rate: float,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
) -> float:
    """Log-performance recovery from reducing completion cost."""
    if not math.isfinite(saving) or saving < 0:
        raise ValueError("saving must be finite and nonnegative")
    if (
        not math.isfinite(baseline_completion_cost)
        or baseline_completion_cost <= 0
        or saving >= baseline_completion_cost
    ):
        raise ValueError("require 0 <= saving < baseline_completion_cost")
    if not math.isfinite(closure_rate) or closure_rate <= 0:
        raise ValueError("closure_rate must be finite and positive")
    if not math.isfinite(baseline_fitness) or baseline_fitness <= 0:
        raise ValueError("baseline_fitness must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value <= 0:
        raise ValueError("resolution_value must be finite and positive")

    base_term = resolution_value * math.exp(
        -closure_rate * baseline_completion_cost
    )
    routed_term = base_term * math.exp(closure_rate * saving)
    return math.log(
        (baseline_fitness + routed_term)
        / (baseline_fitness + base_term)
    )


def opportunity_architecture_thresholds_exponential(
    max_saving: float,
    *,
    baseline_completion_cost: float,
    closure_rate: float,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
) -> tuple[float, float]:
    """Return local and global linear architecture-cost thresholds."""
    if not math.isfinite(max_saving) or max_saving <= 0:
        raise ValueError("max_saving must be finite and positive")
    if max_saving >= baseline_completion_cost:
        raise ValueError("max_saving must be below baseline completion cost")

    a = resolution_value * math.exp(
        -closure_rate * baseline_completion_cost
    )
    p0 = a / (baseline_fitness + a)
    local = closure_rate * p0
    recovery = opportunity_log_recovery_exponential(
        max_saving,
        baseline_completion_cost=baseline_completion_cost,
        closure_rate=closure_rate,
        baseline_fitness=baseline_fitness,
        resolution_value=resolution_value,
    )
    global_threshold = recovery / max_saving
    return local, global_threshold


def opportunity_architecture_value_exponential(
    saving: float,
    *,
    baseline_completion_cost: float,
    closure_rate: float,
    architecture_cost_per_saving: float,
    baseline_fitness: float = 1.0,
    resolution_value: float = 1.0,
) -> float:
    """Net log-fitness value with linear architecture cost."""
    if (
        not math.isfinite(architecture_cost_per_saving)
        or architecture_cost_per_saving < 0
    ):
        raise ValueError(
            "architecture_cost_per_saving must be finite and nonnegative"
        )
    return opportunity_log_recovery_exponential(
        saving,
        baseline_completion_cost=baseline_completion_cost,
        closure_rate=closure_rate,
        baseline_fitness=baseline_fitness,
        resolution_value=resolution_value,
    ) - architecture_cost_per_saving * saving
