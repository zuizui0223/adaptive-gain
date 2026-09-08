"""Adaptive depth forced by a saturated exact-balanced fixed-cost bundle.

For even n=2h>=8, suppose the declared exact-balanced binary query family has
exactly n-3 queries and all n-3 are fixed-mandatory.  Choosing one private
cross-target pair per query gives a forest with n vertices and n-3 edges, hence
three components.

Exact balance forces the component sizes to be (h-1, 2, h-1), and every edge
of each (h-1)-component must be a leaf edge, so both large components are stars.
Thus the private-pair normal form is star--edge--star.

With no external queries available, separating all registered private edges
requires adaptive depth exactly h-1.  The middle-edge query can be asked first;
then the two star sides are handled in parallel with h-2 leaf queries.  The
matching lower bound follows because any queries asked before the middle split
only add to one of the two remaining star spines.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .balanced_binary_fixed_cost_cap import (
    exact_balanced_binary_fixed_cost_cap_private_pairs,
    exact_balanced_binary_fixed_cost_cap_witness,
)
from .core import FiniteTask, World, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class CapSaturationDepthReceipt:
    world_count: int
    fixed_cost: int
    adaptive_cost: int
    expected_fixed_cost: int
    expected_adaptive_cost: int
    ratio_numerator: int
    ratio_denominator: int
    theorem_holds: bool
    scope: str = "exact_balanced_binary_cap_saturation_adaptive_depth"


def exact_balanced_cap_saturation_adaptive_depth(world_count: int) -> int:
    """Sharp depth of a saturated n-3-query bundle, for even n>=8."""
    if type(world_count) is not int or world_count < 8 or world_count % 2:
        raise ValueError("world_count must be an even integer at least 8")
    return world_count // 2 - 1


def exact_balanced_cap_saturation_task(world_count: int) -> FiniteTask:
    """Explicit star--edge--star task attaining (C_A,C_F)=(n/2-1,n-3)."""
    depth = exact_balanced_cap_saturation_adaptive_depth(world_count)
    base = exact_balanced_binary_fixed_cost_cap_witness(world_count)
    half = world_count // 2
    left = tuple(range(0, half - 1))
    middle = (half - 1, half)
    right = tuple(range(half + 1, world_count))

    targets: list[int | None] = [None] * world_count
    target = 0

    # q_middle separates the two large sides.  On each side, identify the
    # middle endpoint with that star's center; every star leaf gets its own
    # target.  This makes every registered forest edge cross-target while the
    # q_middle-first policy resolves in 1+(half-2)=half-1 queries.
    targets[left[0]] = target
    targets[middle[0]] = target
    target += 1
    for leaf in left[1:]:
        targets[leaf] = target
        target += 1

    targets[right[0]] = target
    targets[middle[1]] = target
    target += 1
    for leaf in right[1:]:
        targets[leaf] = target
        target += 1

    if any(value is None for value in targets):
        raise ArithmeticError("cap-saturation target assignment is incomplete")
    worlds = tuple(World(base.worlds[i].name, int(targets[i])) for i in range(world_count))
    task = FiniteTask(worlds, base.queries)

    pairs = exact_balanced_binary_fixed_cost_cap_private_pairs(world_count)
    if any(task.worlds[a].target == task.worlds[b].target for a, b in pairs):
        raise ArithmeticError("registered private edge lost cross-target status")
    if len(task.queries) != world_count - 3 or depth != half - 1:
        raise ArithmeticError("cap-saturation construction count mismatch")
    return task


@lru_cache(maxsize=None)
def audit_exact_balanced_cap_saturation_depth(world_count: int) -> CapSaturationDepthReceipt:
    task = exact_balanced_cap_saturation_task(world_count)
    adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(task).minimum_cost
    if adaptive is None or fixed is None:
        raise ArithmeticError("cap-saturation task is unresolved")
    expected_adaptive = exact_balanced_cap_saturation_adaptive_depth(world_count)
    expected_fixed = world_count - 3
    theorem = adaptive == expected_adaptive and fixed == expected_fixed
    if not theorem:
        raise ArithmeticError("cap-saturation adaptive-depth audit failed")
    return CapSaturationDepthReceipt(
        world_count=world_count,
        fixed_cost=fixed,
        adaptive_cost=adaptive,
        expected_fixed_cost=expected_fixed,
        expected_adaptive_cost=expected_adaptive,
        ratio_numerator=fixed,
        ratio_denominator=adaptive,
        theorem_holds=True,
    )
