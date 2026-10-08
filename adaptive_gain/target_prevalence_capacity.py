"""Expected adaptive-value ceilings with fixed binary-target prevalence.

These are supremal value bounds over finite deterministic unit-cost tasks and
positive world frequencies subject to a fixed binary-target marginal.
Comparison is to one universal fixed resolving bundle.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class TargetPrevalenceCapacity:
    target_one_probability: float
    max_arity: int
    binary_ceiling: float
    ternary_or_higher_ceiling: float
    selected_arity_ceiling: float
    scope: str = "scalable_expected_value_binary_target_fixed_prevalence"


def target_prevalence_expected_capacity(
    target_one_probability: float,
    *,
    value_at_one: float,
    value_at_two: float,
    limiting_value: float,
    max_arity: int,
) -> TargetPrevalenceCapacity:
    """Sharp expected-value supremum with a fixed two-class target marginal.

    b=2: max(p,1-p)*U(1) + min(p,1-p)*U(2) - U_infinity.
    b>=3: U(1)-U_infinity.

    Finite and nonincreasing U with a finite asymptotic limit is assumed.
    The result does not hold for a fixed distribution over individual worlds.
    """
    p = float(target_one_probability)
    u1, u2, uinf = (
        float(value_at_one),
        float(value_at_two),
        float(limiting_value),
    )
    if not math.isfinite(p) or not 0.0 < p < 1.0:
        raise ValueError("target_one_probability must be strictly between zero and one")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least two")
    if any(not math.isfinite(x) for x in (u1, u2, uinf)):
        raise ValueError("completion values must be finite")
    if not (u1 >= u2 >= uinf):
        raise ValueError("require U(1) >= U(2) >= U_infinity")

    a = max(p, 1.0 - p)
    binary = a * u1 + (1.0 - a) * u2 - uinf
    ternary = u1 - uinf
    return TargetPrevalenceCapacity(
        target_one_probability=p,
        max_arity=max_arity,
        binary_ceiling=binary,
        ternary_or_higher_ceiling=ternary,
        selected_arity_ceiling=binary if max_arity == 2 else ternary,
    )


def exponential_target_prevalence_expected_capacity(
    target_one_probability: float,
    *,
    closure_rate: float,
    resolution_value: float = 1.0,
    max_arity: int,
) -> TargetPrevalenceCapacity:
    """Expected-capacity special case U(c)=v*exp(-mu*c)."""
    if not math.isfinite(closure_rate) or closure_rate <= 0.0:
        raise ValueError("closure_rate must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value <= 0.0:
        raise ValueError("resolution_value must be finite and positive")
    return target_prevalence_expected_capacity(
        target_one_probability,
        value_at_one=resolution_value * math.exp(-closure_rate),
        value_at_two=resolution_value * math.exp(-2.0 * closure_rate),
        limiting_value=0.0,
        max_arity=max_arity,
    )


def minimum_expected_cue_arity_with_target_prevalence(
    architecture_cost: float,
    target_one_probability: float,
    *,
    value_at_one: float,
    value_at_two: float,
    limiting_value: float,
) -> int | None:
    """Return 2, 3, or None for strict positive expected net value.

    This is an existence threshold over arbitrarily large finite tasks and
    freely selected strictly positive within-target world frequencies.
    """
    if not math.isfinite(architecture_cost) or architecture_cost < 0:
        raise ValueError("architecture_cost must be finite and nonnegative")
    receipt = target_prevalence_expected_capacity(
        target_one_probability,
        value_at_one=value_at_one,
        value_at_two=value_at_two,
        limiting_value=limiting_value,
        max_arity=2,
    )
    if architecture_cost < receipt.binary_ceiling:
        return 2
    if architecture_cost < receipt.ternary_or_higher_ceiling:
        return 3
    return None


def exponential_minimum_expected_arity_with_target_prevalence(
    architecture_cost: float,
    target_one_probability: float,
    *,
    closure_rate: float,
    resolution_value: float = 1.0,
) -> int | None:
    """Minimum arity for U(c)=v*exp(-mu*c) and fixed binary-target prevalence."""
    receipt = exponential_target_prevalence_expected_capacity(
        target_one_probability,
        closure_rate=closure_rate,
        resolution_value=resolution_value,
        max_arity=2,
    )
    return minimum_expected_cue_arity_with_target_prevalence(
        architecture_cost,
        target_one_probability,
        value_at_one=resolution_value * math.exp(-closure_rate),
        value_at_two=resolution_value * math.exp(-2.0 * closure_rate),
        limiting_value=0.0,
    )
