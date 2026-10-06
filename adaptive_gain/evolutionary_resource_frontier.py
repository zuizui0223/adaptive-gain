"""Inverse robust statewise-value thresholds for finite routing.

These functions invert U(C_A)-U(C_F)>K, where C_A is a worst-path guarantee.
They therefore characterize distribution-free robust viability, not the minimum
structure required for positive expected selection under a particular world
frequency distribution.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

from .bounded_arity_extremal_bounds import (
    maximum_bounded_arity_tree_internal_nodes,
)


@dataclass(frozen=True)
class EvolutionaryDepthRequirement:
    adaptive_depth: int
    required_fixed_cost: int | None
    required_gap: int | None
    structurally_feasible: bool


@dataclass(frozen=True)
class BinaryEvolutionaryCorner:
    adaptive_depth: int
    required_fixed_cost: int
    required_gap: int
    minimum_world_count: int
    minimum_query_count: int


@dataclass(frozen=True)
class BoundedArityEvolutionaryCorner:
    adaptive_depth: int
    max_arity: int
    required_fixed_cost: int
    required_gap: int
    minimum_world_count: int
    minimum_query_count: int


def required_fixed_cost_for_value(
    adaptive_depth: int,
    architecture_cost: float,
    completion_value: Callable[[float], float],
    *,
    search_limit: int,
) -> int | None:
    """Minimum j>=h making the robust worst-state value U(h)-U(j) exceed K."""
    if type(adaptive_depth) is not int or adaptive_depth < 0:
        raise ValueError("adaptive_depth must be a nonnegative integer")
    if not math.isfinite(architecture_cost) or architecture_cost < 0:
        raise ValueError("architecture_cost must be finite and nonnegative")
    if type(search_limit) is not int or search_limit < adaptive_depth:
        raise ValueError("search_limit must be an integer at least adaptive_depth")

    u_h = float(completion_value(float(adaptive_depth)))
    if not math.isfinite(u_h):
        raise ValueError("completion_value must be finite")

    previous = u_h
    for fixed_cost in range(adaptive_depth, search_limit + 1):
        value = float(completion_value(float(fixed_cost)))
        if not math.isfinite(value):
            raise ValueError("completion_value must be finite")
        if value > previous + 1e-12:
            raise ValueError("completion_value must be nonincreasing")
        previous = value
        if u_h - value > architecture_cost + 1e-15:
            return fixed_cost
    return None



def minimum_world_count_for_fixed_burden(
    required_fixed_cost: int,
    adaptive_depth: int,
    max_arity: int,
) -> int | None:
    """Minimum n with F_b(n,h)>=required_fixed_cost, or None if impossible at h."""
    if type(required_fixed_cost) is not int or required_fixed_cost < 0:
        raise ValueError("required_fixed_cost must be a nonnegative integer")
    if type(adaptive_depth) is not int or adaptive_depth < 1:
        raise ValueError("adaptive_depth must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    if required_fixed_cost < adaptive_depth:
        raise ValueError("required_fixed_cost cannot be below adaptive_depth")

    absolute_ceiling = full_b_ary_internal_nodes(max_arity, adaptive_depth)
    if required_fixed_cost > absolute_ceiling:
        return None

    maximum_worlds = max_arity ** adaptive_depth
    for world_count in range(adaptive_depth + 1, maximum_worlds + 1):
        if maximum_bounded_arity_tree_internal_nodes(
            world_count,
            adaptive_depth,
            max_arity,
        ) >= required_fixed_cost:
            return world_count
    raise ArithmeticError("failed to find world count below full-tree leaf ceiling")


def bounded_arity_evolutionary_depth_corners(
    *,
    max_adaptive_depth: int,
    max_arity: int,
    architecture_cost: float,
    completion_value: Callable[[float], float],
) -> tuple[BoundedArityEvolutionaryCorner, ...]:
    """Exact minimum (n,m) for robust positive value at each adaptive depth."""
    if type(max_adaptive_depth) is not int or max_adaptive_depth < 1:
        raise ValueError("max_adaptive_depth must be a positive integer")
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")

    rows: list[BoundedArityEvolutionaryCorner] = []
    for depth in range(1, max_adaptive_depth + 1):
        absolute_ceiling = full_b_ary_internal_nodes(max_arity, depth)
        required = required_fixed_cost_for_value(
            depth,
            architecture_cost,
            completion_value,
            search_limit=absolute_ceiling,
        )
        if required is None:
            continue
        n_min = minimum_world_count_for_fixed_burden(
            required,
            depth,
            max_arity,
        )
        if n_min is None:
            continue
        rows.append(
            BoundedArityEvolutionaryCorner(
                adaptive_depth=depth,
                max_arity=max_arity,
                required_fixed_cost=required,
                required_gap=required-depth,
                minimum_world_count=n_min,
                minimum_query_count=required,
            )
        )
    return tuple(rows)


def binary_evolutionary_resource_corners(
    *,
    max_adaptive_depth: int,
    architecture_cost: float,
    completion_value: Callable[[float], float],
) -> tuple[BinaryEvolutionaryCorner, ...]:
    """Exact binary resource corners for positive robust statewise value."""
    if type(max_adaptive_depth) is not int or max_adaptive_depth < 1:
        raise ValueError("max_adaptive_depth must be a positive integer")

    candidates: list[BinaryEvolutionaryCorner] = []
    for depth in range(1, max_adaptive_depth + 1):
        structural_ceiling = (1 << depth) - 1
        required = required_fixed_cost_for_value(
            depth,
            architecture_cost,
            completion_value,
            search_limit=structural_ceiling,
        )
        if required is None:
            continue
        candidates.append(
            BinaryEvolutionaryCorner(
                depth,
                required,
                required - depth,
                required + 1,
                required,
            )
        )

    nondominated = []
    for row in candidates:
        dominated = any(
            other.minimum_world_count <= row.minimum_world_count
            and other.minimum_query_count <= row.minimum_query_count
            and (
                other.minimum_world_count < row.minimum_world_count
                or other.minimum_query_count < row.minimum_query_count
            )
            for other in candidates
        )
        if not dominated:
            nondominated.append(row)
    return tuple(nondominated)


def exponential_required_gap(
    adaptive_depth: int,
    architecture_cost: float,
    *,
    closure_rate: float,
    resolution_value: float = 1.0,
) -> int | None:
    """Closed-form q_h for U(c)=v exp(-mu c), or None if depth is unviable."""
    if type(adaptive_depth) is not int or adaptive_depth < 0:
        raise ValueError("adaptive_depth must be a nonnegative integer")
    if not math.isfinite(architecture_cost) or architecture_cost < 0:
        raise ValueError("architecture_cost must be finite and nonnegative")
    if not math.isfinite(closure_rate) or closure_rate <= 0:
        raise ValueError("closure_rate must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value <= 0:
        raise ValueError("resolution_value must be finite and positive")

    available = resolution_value * math.exp(-closure_rate * adaptive_depth)
    if architecture_cost >= available - 1e-15:
        return None
    ratio = architecture_cost / available
    threshold = -math.log1p(-ratio) / closure_rate
    return math.floor(threshold + 1e-15) + 1


def exponential_max_viable_adaptive_depth(
    architecture_cost: float,
    *,
    closure_rate: float,
    resolution_value: float = 1.0,
) -> int | None:
    """Largest h whose guaranteed completion value can exceed K before fixed contrast."""
    if not math.isfinite(architecture_cost) or architecture_cost < 0:
        raise ValueError("architecture_cost must be finite and nonnegative")
    if not math.isfinite(closure_rate) or closure_rate <= 0:
        raise ValueError("closure_rate must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value <= 0:
        raise ValueError("resolution_value must be finite and positive")
    if architecture_cost == 0:
        return None  # no finite upper depth ceiling
    if architecture_cost >= resolution_value:
        return -1

    bound = math.log(resolution_value / architecture_cost) / closure_rate
    return math.ceil(bound - 1e-15) - 1



def full_b_ary_internal_nodes(max_arity: int, adaptive_depth: int) -> int:
    """Maximum internal-node count of a full b-ary tree of depth h."""
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    if type(adaptive_depth) is not int or adaptive_depth < 0:
        raise ValueError("adaptive_depth must be a nonnegative integer")
    if adaptive_depth == 0:
        return 0
    return (max_arity ** adaptive_depth - 1) // (max_arity - 1)


def exponential_arity_limited_cost_ceiling(
    max_arity: int,
    *,
    closure_rate: float,
    resolution_value: float = 1.0,
) -> tuple[float, tuple[int, ...]]:
    """Exact arity-limited robust K_crit^(b) for U(c)=v exp(-mu c), plus depths.

    The search stops exactly once the upper bound v*exp(-mu*h) for all future
    depths is no larger than the best value already seen.
    """
    if type(max_arity) is not int or max_arity < 2:
        raise ValueError("max_arity must be an integer at least 2")
    if not math.isfinite(closure_rate) or closure_rate <= 0:
        raise ValueError("closure_rate must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value <= 0:
        raise ValueError("resolution_value must be finite and positive")

    best = -1.0
    maximizing: list[int] = []
    h = 2
    while True:
        fixed = full_b_ary_internal_nodes(max_arity, h)
        value = resolution_value * (
            math.exp(-closure_rate * h)
            - math.exp(-closure_rate * fixed)
        )
        if value > best + 1e-15:
            best = value
            maximizing = [h]
        elif math.isclose(value, best, rel_tol=0.0, abs_tol=1e-15):
            maximizing.append(h)

        next_upper = resolution_value * math.exp(
            -closure_rate * (h + 1)
        )
        if next_upper <= best + 1e-15:
            break
        h += 1

    return best, tuple(maximizing)


def exponential_unrestricted_information_cost_ceiling(
    *,
    closure_rate: float,
    resolution_value: float = 1.0,
) -> float:
    """Supremal robust K_crit with no finite n,m,b restriction."""
    if not math.isfinite(closure_rate) or closure_rate <= 0:
        raise ValueError("closure_rate must be finite and positive")
    if not math.isfinite(resolution_value) or resolution_value <= 0:
        raise ValueError("resolution_value must be finite and positive")
    return resolution_value * math.exp(-2.0 * closure_rate)
