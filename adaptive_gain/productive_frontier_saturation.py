"""Minimal-world saturation witness for the q=4 productive-frontier Sperner bound."""
from __future__ import annotations

from dataclasses import dataclass
from math import comb

from .core import FiniteTask, Query, World, adaptive_gain_receipt
from .productive_pair_equivalence import minimal_cross_target_separator_sets
from .productive_frontier import productive_frontier_sperner_bound


@dataclass(frozen=True)
class FourQueryProductiveFrontierSaturationReceipt:
    query_count: int
    world_count: int
    target_class_sizes: tuple[int, ...]
    cross_target_pair_count: int
    minimal_productive_sets: tuple[int, ...]
    frontier_size: int
    sperner_bound: int
    adaptive_cost: int
    fixed_cost: int
    strict_adaptive_gain: bool
    lower_bound_world_count: int
    world_count_minimal_for_saturation: bool
    scope: str = "q4_binary_unit_cost_minimal_world_sperner_saturating_productive_frontier"


def minimum_worlds_for_cross_target_pairs(required_pairs: int) -> int:
    """Smallest n whose bipartition can contain at least required_pairs pairs."""
    if type(required_pairs) is not int or required_pairs < 0:
        raise ValueError("required_pairs must be a nonnegative integer")
    n = 0
    while (n // 2) * (n - n // 2) < required_pairs:
        n += 1
    return n


def four_query_sperner_saturation_task() -> FiniteTask:
    """Five worlds whose six cross-target pairs realize all q=4 rank-2 edges."""
    bit_patterns = (0b0000, 0b0011, 0b0101, 0b0110, 0b1001)
    targets = (0, 0, 0, 1, 1)
    worlds = tuple(
        World(f"x{pattern:04b}", target)
        for pattern, target in zip(bit_patterns, targets)
    )
    queries = tuple(
        Query(
            f"q{q}",
            1,
            tuple((pattern >> q) & 1 for pattern in bit_patterns),
        )
        for q in range(4)
    )
    return FiniteTask(worlds, queries)


def four_query_productive_frontier_saturation_receipt() -> FourQueryProductiveFrontierSaturationReceipt:
    task = four_query_sperner_saturation_task()
    frontier = minimal_cross_target_separator_sets(task)
    expected = tuple(sorted((1 << i) | (1 << j) for i in range(4) for j in range(i + 1, 4)))
    if frontier != expected:
        raise ArithmeticError("registered q4 saturation task lost the complete rank-2 frontier")
    pair_count = 3 * 2
    bound = productive_frontier_sperner_bound(4)
    lower = minimum_worlds_for_cross_target_pairs(bound)
    gain = adaptive_gain_receipt(task)
    if gain.adaptive_cost is None or gain.fixed_cost is None:
        raise ArithmeticError("registered q4 saturation task became unresolved")
    return FourQueryProductiveFrontierSaturationReceipt(
        4,
        len(task.worlds),
        (3, 2),
        pair_count,
        frontier,
        len(frontier),
        bound,
        gain.adaptive_cost,
        gain.fixed_cost,
        gain.strict_adaptive_gain,
        lower,
        len(task.worlds) == lower,
    )
