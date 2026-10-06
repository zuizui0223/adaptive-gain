"""Inverse evolutionary resource thresholds for finite routing."""
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


def required_fixed_cost_for_value(
    adaptive_depth: int,
    architecture_cost: float,
    completion_value: Callable[[float], float],
    *,
    search_limit: int,
) -> int | None:
    """Minimum integer j>=h with U(h)-U(j)>K, or None within the limit."""
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


def binary_evolutionary_resource_corners(
    *,
    max_adaptive_depth: int,
    architecture_cost: float,
    completion_value: Callable[[float], float],
) -> tuple[BinaryEvolutionaryCorner, ...]:
    """Exact nondominated binary (world_count,query_count) corners by depth."""
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
    """Largest h>=0 with K < v exp(-mu h); None if even h=0 is not viable."""
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
