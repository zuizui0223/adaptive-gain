"""Exact-balanced ten-state routeability stress test.

This module instantiates routing depth d=2 from the quantity/topology theorem as
a practical experimental design.

Both architecture groups share the exact same ten physical cue vectors across
six binary cue channels. Every cue is exactly 5/5 balanced. Only the target /
reward map differs.

Routeable architecture:
    exact costs (C_A,C_F) = (3,4)

Matched control:
    exact costs (C_A,C_F) = (2,2)

At common budget B=3:
    routeable contingent ceiling = 1.0
    routeable best fixed three-cue ceiling = 0.8
    control contingent ceiling = 1.0
    control best fixed three-cue ceiling = 1.0

Therefore the exact uniform-state architecture x access ceiling interaction is
0.20.

The 0.20 value is an information/decision ceiling under the deterministic
stimulus table. It is not a behavioral effect-size assumption.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from .balanced_binary_extremal_family import balanced_binary_extremal_task
from .balanced_quantity_topology_contrast import balanced_quantity_matched_control_task
from .core import (
    FiniteTask,
    adaptive_minimum_resolution,
    fixed_minimum_resolution,
)


@dataclass(frozen=True)
class ExactBalancedStressTestReceipt:
    world_count: int
    query_count: int
    all_queries_exactly_balanced: bool
    same_query_matrix: bool
    same_target_multiplicities: bool
    routeable_adaptive_cost: int
    routeable_fixed_cost: int
    control_adaptive_cost: int
    control_fixed_cost: int
    common_budget: int
    routeable_contingent_accuracy_ceiling: float
    routeable_best_fixed_accuracy_ceiling: float
    control_contingent_accuracy_ceiling: float
    control_best_fixed_accuracy_ceiling: float
    architecture_access_interaction_ceiling: float
    routeable_best_fixed_bundles: tuple[tuple[str, ...], ...]
    control_best_fixed_bundles: tuple[tuple[str, ...], ...]
    theorem_holds: bool
    scope: str = "exact_balanced_ten_state_routeability_stress_test"


def exact_balanced_routeable_stress_task() -> FiniteTask:
    return balanced_binary_extremal_task(2)


def exact_balanced_control_stress_task() -> FiniteTask:
    return balanced_quantity_matched_control_task(2)


def uniform_target_accuracy_for_bundle(
    task: FiniteTask,
    query_names: tuple[str, ...],
) -> float:
    lookup = {query.name: query for query in task.queries}
    grouped: dict[tuple[object, ...], list[object]] = defaultdict(list)
    for i, world in enumerate(task.worlds):
        pattern = tuple(lookup[name].outcomes[i] for name in query_names)
        grouped[pattern].append(world.target)

    correct = 0
    for targets in grouped.values():
        counts: dict[object, int] = {}
        for target in targets:
            counts[target] = counts.get(target, 0) + 1
        correct += max(counts.values())
    return correct / len(task.worlds)


def best_fixed_bundle_accuracy(
    task: FiniteTask,
    budget: int,
) -> tuple[float, tuple[tuple[str, ...], ...]]:
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    names = tuple(query.name for query in task.queries)
    if budget > len(names):
        budget = len(names)

    best = -1.0
    bundles: list[tuple[str, ...]] = []
    for bundle in combinations(names, budget):
        accuracy = uniform_target_accuracy_for_bundle(task, bundle)
        if accuracy > best:
            best = accuracy
            bundles = [bundle]
        elif accuracy == best:
            bundles.append(bundle)
    return best, tuple(bundles)


def routed_depth_two_accuracy(task: FiniteTask) -> float:
    """Uniform accuracy of r0 -> r1 -> branch-specific terminal."""
    lookup = {query.name: query for query in task.queries}
    r0 = lookup["route_bit_0"]
    r1 = lookup["route_bit_1"]

    grouped: dict[tuple[object, object, object], list[object]] = defaultdict(list)
    for i, world in enumerate(task.worlds):
        branch = int(r0.outcomes[i]) + 2 * int(r1.outcomes[i])
        terminal = lookup[f"terminal_{branch}"]
        pattern = (r0.outcomes[i], r1.outcomes[i], terminal.outcomes[i])
        grouped[pattern].append(world.target)

    correct = 0
    for targets in grouped.values():
        counts: dict[object, int] = {}
        for target in targets:
            counts[target] = counts.get(target, 0) + 1
        correct += max(counts.values())
    return correct / len(task.worlds)


def exact_balanced_stress_test_audit() -> ExactBalancedStressTestReceipt:
    routeable = exact_balanced_routeable_stress_task()
    control = exact_balanced_control_stress_task()

    route_a = adaptive_minimum_resolution(routeable).minimum_worst_path_cost
    route_f = fixed_minimum_resolution(routeable).minimum_cost
    control_a = adaptive_minimum_resolution(control).minimum_worst_path_cost
    control_f = fixed_minimum_resolution(control).minimum_cost

    if None in (route_a, route_f, control_a, control_f):
        raise ArithmeticError("stress-test tasks must be exactly resolvable")

    budget = 3
    route_cont = routed_depth_two_accuracy(routeable)
    control_cont = routed_depth_two_accuracy(control)
    route_fixed, route_bundles = best_fixed_bundle_accuracy(routeable, budget)
    control_fixed, control_bundles = best_fixed_bundle_accuracy(control, budget)

    interaction = (route_cont - route_fixed) - (control_cont - control_fixed)

    balanced = all(
        sum(outcome == 0 for outcome in query.outcomes)
        == sum(outcome == 1 for outcome in query.outcomes)
        for query in routeable.queries
    )
    same_matrix = routeable.queries == control.queries
    route_targets = sorted(
        [sum(world.target == target for world in routeable.worlds)
         for target in {world.target for world in routeable.worlds}],
        reverse=True,
    )
    control_targets = sorted(
        [sum(world.target == target for world in control.worlds)
         for target in {world.target for world in control.worlds}],
        reverse=True,
    )

    theorem = (
        len(routeable.worlds) == 10
        and len(routeable.queries) == 6
        and balanced
        and same_matrix
        and route_targets == control_targets == [6, 4]
        and route_a == 3
        and route_f == 4
        and control_a == 2
        and control_f == 2
        and route_cont == 1.0
        and route_fixed == 0.8
        and control_cont == 1.0
        and control_fixed == 1.0
        and interaction == 0.2
    )
    if not theorem:
        raise ArithmeticError("exact-balanced stress-test audit failed")

    return ExactBalancedStressTestReceipt(
        world_count=10,
        query_count=6,
        all_queries_exactly_balanced=balanced,
        same_query_matrix=same_matrix,
        same_target_multiplicities=route_targets == control_targets,
        routeable_adaptive_cost=route_a,
        routeable_fixed_cost=route_f,
        control_adaptive_cost=control_a,
        control_fixed_cost=control_f,
        common_budget=budget,
        routeable_contingent_accuracy_ceiling=route_cont,
        routeable_best_fixed_accuracy_ceiling=route_fixed,
        control_contingent_accuracy_ceiling=control_cont,
        control_best_fixed_accuracy_ceiling=control_fixed,
        architecture_access_interaction_ceiling=interaction,
        routeable_best_fixed_bundles=route_bundles,
        control_best_fixed_bundles=control_bundles,
        theorem_holds=theorem,
    )
