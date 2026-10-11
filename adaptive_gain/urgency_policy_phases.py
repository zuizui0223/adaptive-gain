"""Urgency-phase summaries for finite completion-cost profiles."""
from __future__ import annotations

from collections import defaultdict
import math
from typing import Sequence


def depth_mass_profile(
    path_costs: Sequence[int | float],
    world_probabilities: Sequence[float],
) -> tuple[tuple[int, float], ...]:
    """Return sorted (integer completion cost, probability mass) pairs."""
    if len(path_costs) == 0 or len(path_costs) != len(world_probabilities):
        raise ValueError("path_costs and world_probabilities must have equal nonzero length")
    probs = [float(p) for p in world_probabilities]
    if any((not math.isfinite(p) or p < 0) for p in probs):
        raise ValueError("probabilities must be finite and nonnegative")
    if not math.isclose(sum(probs), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("probabilities must sum to one")

    masses: dict[int, float] = defaultdict(float)
    for raw_cost, p in zip(path_costs, probs):
        cost = float(raw_cost)
        if not math.isfinite(cost) or cost < 0 or not cost.is_integer():
            raise ValueError("urgency polynomial requires nonnegative integer path costs")
        masses[int(cost)] += p
    return tuple(sorted(masses.items()))


def discounted_profile_value(
    profile: Sequence[tuple[int, float]],
    *,
    discount_rate: float,
) -> float:
    """Evaluate sum_d a_d exp(-mu d)."""
    if not math.isfinite(discount_rate) or discount_rate <= 0:
        raise ValueError("discount_rate must be finite and positive")
    return sum(
        float(mass) * math.exp(-discount_rate * int(depth))
        for depth, mass in profile
    )


def profile_moments(
    profile: Sequence[tuple[int, float]],
    *,
    max_order: int = 3,
) -> tuple[float, ...]:
    """Return E[T], E[T^2], ... through max_order."""
    if type(max_order) is not int or max_order < 1:
        raise ValueError("max_order must be a positive integer")
    return tuple(
        sum(float(mass) * (int(depth) ** order) for depth, mass in profile)
        for order in range(1, max_order + 1)
    )


def high_urgency_signature(
    profile: Sequence[tuple[int, float]],
) -> tuple[float, ...]:
    """Lexicographic signature: lower tuple is preferred at high urgency.

    First minimize earliest completion depth; then maximize probability mass at
    each successive depth. Missing depths between min and max are assigned zero.
    """
    if not profile:
        raise ValueError("profile must be nonempty")
    rows = sorted((int(d), float(m)) for d, m in profile)
    if any(d < 0 or m < 0 or not math.isfinite(m) for d, m in rows):
        raise ValueError("invalid profile")
    d0 = rows[0][0]
    dmax = rows[-1][0]
    mass = dict(rows)
    return (float(d0),) + tuple(-mass.get(d, 0.0) for d in range(d0, dmax + 1))


def pairwise_polynomial_coefficients(
    profile_a: Sequence[tuple[int, float]],
    profile_b: Sequence[tuple[int, float]],
) -> tuple[float, ...]:
    """Coefficients c_d for J_a(z)-J_b(z)=sum_d c_d z^d."""
    a = {int(d): float(m) for d, m in profile_a}
    b = {int(d): float(m) for d, m in profile_b}
    dmax = max(max(a, default=0), max(b, default=0))
    coeffs = tuple(a.get(d, 0.0) - b.get(d, 0.0) for d in range(dmax + 1))
    # Retain one coefficient for the identically-zero polynomial.
    last = len(coeffs) - 1
    while last > 0 and abs(coeffs[last]) <= 1e-15:
        last -= 1
    return coeffs[: last + 1]


def polynomial_value(coefficients: Sequence[float], z: float) -> float:
    """Evaluate coefficients in increasing power order using Horner's rule."""
    if not math.isfinite(z):
        raise ValueError("z must be finite")
    value = 0.0
    for coefficient in reversed(tuple(float(c) for c in coefficients)):
        value = value * z + coefficient
    return value
