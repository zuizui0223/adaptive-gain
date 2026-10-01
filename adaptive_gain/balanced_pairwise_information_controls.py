"""Finite controls matching routeable target-cue pairwise information profiles.

These controls strengthen the quantity/topology separation at small exact-balanced
scopes. They reuse the *same physical query matrix* as the existing balanced
routeable family and change only the target/action map.

At routing depth 2:
- target multiplicities match the routeable task;
- the multiset of canonical target-query 2x2 contingency profiles matches;
- C_A=C_F=2.

At routing depth 3:
- target multiplicities match;
- the multiset of canonical target-query 2x2 contingency profiles matches;
- C_F=3; exact C_A is audited with the repository solver.

The pairwise match is intentionally a multiset match, not a name-by-name match:
the same amount/strength profile of pairwise target information is present, but
which cue carries which profile is rearranged.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product

from .balanced_binary_extremal_family import balanced_binary_extremal_task
from .core import FiniteTask, World, adaptive_minimum_resolution, fixed_minimum_resolution


_DEPTH2_TARGET1_INDICES = (0, 1, 3, 4)
_DEPTH3_TARGET1_INDICES = (0, 1, 3, 6, 7, 10, 11, 13)


@dataclass(frozen=True)
class PairwiseMatchedControlReceipt:
    routing_depth: int
    same_query_matrix: bool
    same_target_multiplicities: bool
    same_pairwise_target_query_signature_multiset: bool
    routeable_target_multiplicities: tuple[int, int]
    control_target_multiplicities: tuple[int, int]
    control_adaptive_cost: int
    control_fixed_cost: int
    control_fixed_resolver_names: tuple[str, ...]
    theorem_holds: bool
    scope: str = "finite_exact_balanced_pairwise_target_information_matched_control"


def _target_multiplicities(task: FiniteTask) -> tuple[int, int]:
    counts = Counter(world.target for world in task.worlds)
    values = tuple(sorted(counts.values(), reverse=True))
    if len(values) != 2:
        raise ArithmeticError("expected exactly two target classes")
    return values  # type: ignore[return-value]


def _canonical_binary_pair_signature(
    left: tuple[object, ...],
    right: tuple[object, ...],
) -> tuple[int, int, int, int]:
    if len(left) != len(right):
        raise ValueError("paired variables must have equal length")
    if set(left) - {0, 1} or set(right) - {0, 1}:
        raise ValueError("pairwise signature requires binary 0/1 values")

    candidates: list[tuple[int, int, int, int]] = []
    for flip_left, flip_right in product((False, True), repeat=2):
        counts = {(a, b): 0 for a in (0, 1) for b in (0, 1)}
        for raw_left, raw_right in zip(left, right):
            a = 1 - raw_left if flip_left else raw_left
            b = 1 - raw_right if flip_right else raw_right
            counts[(a, b)] += 1
        candidates.append(
            (
                counts[(0, 0)],
                counts[(0, 1)],
                counts[(1, 0)],
                counts[(1, 1)],
            )
        )
    return min(candidates)


def target_query_signature_multiset(
    task: FiniteTask,
) -> tuple[tuple[int, int, int, int], ...]:
    target = tuple(world.target for world in task.worlds)
    return tuple(
        sorted(
            _canonical_binary_pair_signature(target, tuple(query.outcomes))
            for query in task.queries
        )
    )


def pairwise_matched_control_task(routing_depth: int) -> FiniteTask:
    if routing_depth == 2:
        target1 = set(_DEPTH2_TARGET1_INDICES)
    elif routing_depth == 3:
        target1 = set(_DEPTH3_TARGET1_INDICES)
    else:
        raise ValueError("registered pairwise-matched controls exist only at depths 2 and 3")

    routeable = balanced_binary_extremal_task(routing_depth)
    worlds = tuple(
        World(world.name, 1 if i in target1 else 0)
        for i, world in enumerate(routeable.worlds)
    )
    return FiniteTask(worlds, routeable.queries)


def pairwise_matched_control_audit(routing_depth: int) -> PairwiseMatchedControlReceipt:
    routeable = balanced_binary_extremal_task(routing_depth)
    control = pairwise_matched_control_task(routing_depth)

    same_query_matrix = routeable.queries == control.queries
    route_mult = _target_multiplicities(routeable)
    control_mult = _target_multiplicities(control)
    same_target_mult = route_mult == control_mult
    same_pairwise = (
        target_query_signature_multiset(routeable)
        == target_query_signature_multiset(control)
    )

    adaptive = adaptive_minimum_resolution(control).minimum_worst_path_cost
    fixed = fixed_minimum_resolution(control)
    if adaptive is None or fixed.minimum_cost is None:
        raise ArithmeticError("pairwise-matched control must be resolvable")

    if routing_depth == 2:
        expected_fixed_names = ("terminal_1", "terminal_2")
        expected_fixed = 2
    else:
        expected_fixed_names = ("route_bit_0", "terminal_1", "terminal_6")
        expected_fixed = 3

    bundle = frozenset(expected_fixed_names)
    registered_bundle_is_optimal = (
        fixed.minimum_cost == expected_fixed
        and any(
            frozenset(candidate) == bundle
            for candidate in fixed.optimal_bundles
        )
    )

    theorem = (
        same_query_matrix
        and same_target_mult
        and same_pairwise
        and registered_bundle_is_optimal
        and adaptive is not None
    )
    if not theorem:
        raise ArithmeticError("pairwise-matched control audit failed")

    return PairwiseMatchedControlReceipt(
        routing_depth=routing_depth,
        same_query_matrix=same_query_matrix,
        same_target_multiplicities=same_target_mult,
        same_pairwise_target_query_signature_multiset=same_pairwise,
        routeable_target_multiplicities=route_mult,
        control_target_multiplicities=control_mult,
        control_adaptive_cost=adaptive,
        control_fixed_cost=fixed.minimum_cost,
        control_fixed_resolver_names=expected_fixed_names,
        theorem_holds=theorem,
    )
