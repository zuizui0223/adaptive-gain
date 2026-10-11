"""Expected-value decomposition above the robust routeability base."""
from __future__ import annotations

import math
from typing import Callable, Sequence


def robust_plus_early_premium(
    path_costs: Sequence[float],
    world_probabilities: Sequence[float],
    fixed_cost: float,
    completion_value: Callable[[float], float],
) -> tuple[float, float, float]:
    """Return (robust_base, early_premium, expected_advantage)."""
    if len(path_costs) == 0 or len(path_costs) != len(world_probabilities):
        raise ValueError("path_costs and probabilities must have equal nonzero length")
    costs = [float(c) for c in path_costs]
    probs = [float(p) for p in world_probabilities]
    if any((not math.isfinite(c) or c < 0) for c in costs):
        raise ValueError("path costs must be finite and nonnegative")
    if any((not math.isfinite(p) or p < 0) for p in probs):
        raise ValueError("probabilities must be finite and nonnegative")
    if not math.isclose(sum(probs), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("probabilities must sum to one")
    if not math.isfinite(fixed_cost) or fixed_cost < 0:
        raise ValueError("fixed_cost must be finite and nonnegative")

    h = max(costs)
    u_h = float(completion_value(h))
    u_f = float(completion_value(fixed_cost))
    values = [float(completion_value(c)) for c in costs]
    if any(not math.isfinite(v) for v in values + [u_h, u_f]):
        raise ValueError("completion values must be finite")

    # Verify monotonicity only on the finite set of realized costs plus fixed.
    ordered = sorted(set(costs + [fixed_cost, h]))
    previous = None
    for c in ordered:
        value = float(completion_value(c))
        if previous is not None and value > previous + 1e-12:
            raise ValueError("completion_value must be nonincreasing")
        previous = value

    robust = u_h - u_f
    premium = sum(
        p * (value - u_h)
        for p, value in zip(probs, values)
    )
    expected = robust + premium
    return robust, premium, expected


def four_world_rescue_probability_threshold(
    *,
    discount_rate: float,
    architecture_cost: float = 0.0,
) -> float | None:
    """Exact p threshold for paths (1,3,3,2) versus fixed cost 2.

    Returns None when no p<1 can overcome the declared additive architecture
    cost.
    """
    if not math.isfinite(discount_rate) or discount_rate <= 0:
        raise ValueError("discount_rate must be finite and positive")
    if not math.isfinite(architecture_cost) or architecture_cost < 0:
        raise ValueError("architecture_cost must be finite and nonnegative")

    x = math.exp(-discount_rate)
    maximum = x - x * x
    if architecture_cost >= maximum - 1e-15:
        return None

    base = 2.0 * x / (2.0 * x + 3.0)
    cost_term = (
        3.0 * architecture_cost
        / (x * (1.0 - x) * (2.0 * x + 3.0))
    )
    return base + cost_term
