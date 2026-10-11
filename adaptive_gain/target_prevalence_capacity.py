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


@dataclass(frozen=True)
class FiniteTargetPrevalenceCapacity:
    world_count: int
    query_count: int
    max_arity: int
    target_one_probability: float
    binary_supr: float
    two_target_pure_root_supr: float | None
    expected_value_supremum: float
    maximizing_root_pattern: str
    scope: str = "sharp_finite_expected_value_fixed_target_prevalence"


def finite_target_prevalence_expected_capacity(
    world_count: int,
    query_count: int,
    target_one_probability: float,
    *,
    max_arity: int,
    completion_value,
) -> FiniteTargetPrevalenceCapacity:
    """Exact expected-value supremum at fixed two-target marginal and (n,m,b).

    World probabilities may vary, must be strictly positive, and must retain
    the supplied target marginal. Unit-cost deterministic exact resolution.
    """
    if type(world_count) is not int or world_count < 2:
        raise ValueError("world_count must be an integer at least 2")
    if type(query_count) is not int or query_count < 1:
        raise ValueError("query_count must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    p = float(target_one_probability)
    if not math.isfinite(p) or not 0.0 < p < 1.0:
        raise ValueError("target_one_probability must lie strictly between 0 and 1")

    m = min(query_count, world_count - 1)
    values = {
        j: float(completion_value(float(j)))
        for j in range(1, m + 1)
    }
    if any(not math.isfinite(v) for v in values.values()):
        raise ValueError("completion values must be finite")
    if any(values[j] < values[j + 1] for j in range(1, m)):
        raise ValueError("completion_value must be nonincreasing")

    if m == 1:
        return FiniteTargetPrevalenceCapacity(
            world_count, query_count, max_arity, p, 0.0, None, 0.0, "no_gain"
        )

    q = max(p, 1.0 - p)
    binary = q * values[1] + (1.0 - q) * values[2] - values[m]
    ternary = None
    if max_arity >= 3 and world_count >= 4:
        m3 = min(query_count, world_count - 2)
        if m3 >= 2:
            ternary = values[1] - values[m3]

    if ternary is not None and ternary > binary:
        best = ternary
        pattern = "two_target_pure_root_outcomes_plus_rare_mixed"
    else:
        best = binary
        pattern = "one_target_pure_root_outcome_plus_rare_mixed"

    return FiniteTargetPrevalenceCapacity(
        world_count, query_count, max_arity, p,
        binary, ternary, best, pattern,
    )


def finite_minimum_expected_cue_arity_with_target_prevalence(
    world_count: int,
    query_count: int,
    target_one_probability: float,
    architecture_cost: float,
    *,
    completion_value,
) -> int | None:
    """Minimum arity 2 or 3 that allows strict positive expected net value."""
    if not math.isfinite(architecture_cost) or architecture_cost < 0:
        raise ValueError("architecture_cost must be finite and nonnegative")
    binary = finite_target_prevalence_expected_capacity(
        world_count, query_count, target_one_probability,
        max_arity=2, completion_value=completion_value,
    )
    if architecture_cost < binary.expected_value_supremum:
        return 2
    ternary = finite_target_prevalence_expected_capacity(
        world_count, query_count, target_one_probability,
        max_arity=3, completion_value=completion_value,
    )
    if architecture_cost < ternary.expected_value_supremum:
        return 3
    return None



@dataclass(frozen=True)
class FiniteTernaryOnlyPrevalenceInterval:
    """Exact range of target prevalence where ternary, but not binary, can pay K.

    World frequencies remain freely redistributable within each of two fixed
    target classes. This is an existence result over finite unit-cost tasks,
    not an inference about a measured sensory system.
    """

    world_count: int
    query_count: int
    architecture_cost: float
    binary_ceiling_at_balance: float
    two_pure_root_ceiling: float | None
    target_one_probability_interval: tuple[float, float] | None
    majority_target_probability_max: float | None
    scope: str = "finite_target_prevalence_ternary_only_existence"


def finite_ternary_only_prevalence_interval(
    world_count: int,
    query_count: int,
    architecture_cost: float,
    *,
    completion_value,
) -> FiniteTernaryOnlyPrevalenceInterval:
    """Invert TP2 for the exact prevalence interval requiring >=3 cue outcomes.

    A returned closed interval [p_lo,p_hi] means that throughout that
    interval binary tasks cannot generate strictly positive net expected value
    after K, while some ternary task can. Outside the interval, binary tasks
    can pay K, whenever the interval exists.

    Returns None for the interval if no ternary-only region exists.
    """
    if not math.isfinite(architecture_cost) or architecture_cost < 0:
        raise ValueError("architecture_cost must be finite and nonnegative")

    binary = finite_target_prevalence_expected_capacity(
        world_count,
        query_count,
        0.5,
        max_arity=2,
        completion_value=completion_value,
    )
    ternary = finite_target_prevalence_expected_capacity(
        world_count,
        query_count,
        0.5,
        max_arity=3,
        completion_value=completion_value,
    )

    baseline = binary.binary_supr
    pure = ternary.two_target_pure_root_supr
    if (
        pure is None
        or architecture_cost < baseline
        or architecture_cost >= pure
    ):
        return FiniteTernaryOnlyPrevalenceInterval(
            world_count, query_count, architecture_cost,
            baseline, pure, None, None,
        )

    M = min(query_count, world_count - 1)
    u1 = float(completion_value(1.0))
    u2 = float(completion_value(2.0))
    uM = float(completion_value(float(M)))
    if u1 <= u2:
        # The ternary pure-root ceiling cannot strictly exceed the binary
        # ceiling if the first two completion values are equal.
        return FiniteTernaryOnlyPrevalenceInterval(
            world_count, query_count, architecture_cost,
            baseline, pure, None, None,
        )

    q_max = (architecture_cost - u2 + uM) / (u1 - u2)
    # In a genuine ternary-only regime, this lies in [1/2,1).
    if q_max < 0.5 - 1e-12 or q_max >= 1.0:
        raise ArithmeticError("unexpected ternary-only prevalence boundary")
    q_max = max(q_max, 0.5)

    return FiniteTernaryOnlyPrevalenceInterval(
        world_count, query_count, architecture_cost,
        baseline, pure,
        (1.0 - q_max, q_max),
        q_max,
    )



@dataclass(frozen=True)
class FiniteTernaryCapacityPremiumInterval:
    """Class-level expected-value capacity advantage after ternary overhead.

    NOT a within-task genotype comparison: the binary and ternary ceilings
    optimize over different admissible task designs with common (n,m,p,U).
    """
    world_count: int
    query_count: int
    extra_ternary_cost: float
    maximal_capacity_premium_at_balance: float
    ternary_minus_binary_positive_interval: tuple[float, float] | None
    majority_prevalence_threshold: float | None
    scope: str = "finite_task_class_capacity_comparison_not_pairwise_selection"


def finite_ternary_capacity_premium_prevalence_interval(
    world_count: int,
    query_count: int,
    extra_ternary_cost: float,
    *,
    completion_value,
) -> FiniteTernaryCapacityPremiumInterval:
    """Where the ternary-class sharp ceiling exceeds the binary ceiling + overhead.

    The interval, if present, is OPEN at both prevalence boundaries: equal
    net class capacities do not give strict advantage. This is a comparison
    of attainable class optima, not selection between two policies evaluated
    on one shared realized cue task.
    """
    if not math.isfinite(extra_ternary_cost) or extra_ternary_cost < 0:
        raise ValueError("extra_ternary_cost must be finite and nonnegative")
    binary = finite_target_prevalence_expected_capacity(
        world_count, query_count, 0.5,
        max_arity=2, completion_value=completion_value
    )
    ternary = finite_target_prevalence_expected_capacity(
        world_count, query_count, 0.5,
        max_arity=3, completion_value=completion_value
    )
    ternary_pure = ternary.two_target_pure_root_supr
    maximal_premium = max(
        0.0,
        (ternary_pure - binary.binary_supr)
        if ternary_pure is not None else 0.0,
    )
    if ternary_pure is None or extra_ternary_cost >= maximal_premium:
        return FiniteTernaryCapacityPremiumInterval(
            world_count, query_count, extra_ternary_cost,
            maximal_premium, None, None
        )

    M = min(world_count - 1, query_count)
    u1 = float(completion_value(1.0))
    u2 = float(completion_value(2.0))
    uM = float(completion_value(float(M)))
    if u1 <= u2:
        return FiniteTernaryCapacityPremiumInterval(
            world_count, query_count, extra_ternary_cost,
            maximal_premium, None, None
        )
    q_limit = (
        ternary_pure - extra_ternary_cost - u2 + uM
    ) / (u1 - u2)
    if not (0.5 < q_limit <= 1.0 + 1e-12):
        raise ArithmeticError("ternary capacity premium boundary outside (1/2,1]")
    # If the query budget binds both classes (M3=M) and overhead is zero,
    # q_limit=1: ternary capacity is strictly higher for every p in (0,1).
    q_limit = min(q_limit, 1.0)

    return FiniteTernaryCapacityPremiumInterval(
        world_count, query_count, extra_ternary_cost,
        maximal_premium,
        (1.0 - q_limit, q_limit),
        q_limit
    )
