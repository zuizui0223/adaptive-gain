from __future__ import annotations

from adaptive_gain.continuation_bisimulation import (
    build_continuation_quotient,
    continuation_quotient_costs,
)
from adaptive_gain.continuation_witnesses import continuation_fixed_cost_collision
from adaptive_gain.productive_frontier import (
    build_productive_frontier,
    productive_frontier_fixed_minimum_resolution,
)


def test_same_adaptive_continuation_but_different_frontier_changes_gap() -> None:
    strict, bypass = continuation_fixed_cost_collision()
    tasks = (strict, bypass)

    continuation = build_continuation_quotient(tasks)
    assert continuation.root_classes[0] == continuation.root_classes[1]
    assert continuation_quotient_costs(tasks, continuation) == (2, 2)

    strict_frontier = build_productive_frontier(strict)
    bypass_frontier = build_productive_frontier(bypass)

    strict_fixed = productive_frontier_fixed_minimum_resolution(strict_frontier).minimum_cost
    bypass_fixed = productive_frontier_fixed_minimum_resolution(bypass_frontier).minimum_cost

    assert strict_fixed == 3
    assert bypass_fixed == 2
    assert strict_frontier.minimal_productive_sets != bypass_frontier.minimal_productive_sets

    strict_gap = strict_fixed - 2
    bypass_gap = bypass_fixed - 2
    assert (strict_gap, bypass_gap) == (1, 0)


def test_joint_kernel_components_recover_exact_scalar_costs() -> None:
    strict, bypass = continuation_fixed_cost_collision()
    tasks = (strict, bypass)
    continuation = build_continuation_quotient(tasks)
    adaptive_costs = continuation_quotient_costs(tasks, continuation)

    recovered = []
    for task, adaptive_cost in zip(tasks, adaptive_costs, strict=True):
        frontier = build_productive_frontier(task)
        fixed_cost = productive_frontier_fixed_minimum_resolution(frontier).minimum_cost
        recovered.append((adaptive_cost, fixed_cost, fixed_cost - adaptive_cost))

    assert recovered == [(2, 3, 1), (2, 2, 0)]
