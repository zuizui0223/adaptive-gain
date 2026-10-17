"""Five-world factorial witness and deadline-conditioned exact checks."""

import pytest

from adaptive_gain.core import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    fixed_minimum_resolution,
)
from adaptive_gain.deadline_factorial import optimal_timely_resolution_mass


TARGETS = (0, 1, 1, 0, 0)
UNIFORM = (0.2,) * 5


def task_for_topology(name: str) -> FiniteTask:
    if name == "routeable":
        cues = (
            ("root", (0, 0, 1, 1, 0)),
            ("left", (0, 1, 0, 0, 0)),
            ("right", (0, 0, 0, 1, 0)),
        )
    elif name == "sequential":
        cues = (
            ("first", (1, 0, 0, 0, 0)),
            ("second", (0, 0, 0, 1, 0)),
            ("third", (1, 1, 1, 1, 0)),
        )
    else:
        raise ValueError(name)
    return FiniteTask(
        tuple(World(f"world_{i}", target) for i, target in enumerate(TARGETS)),
        tuple(Query(name, 1, outcomes) for name, outcomes in cues),
    )


def test_same_worlds_targets_query_count_and_arity_but_different_routeability():
    first, second = (task_for_topology(name) for name in ("routeable", "sequential"))
    assert first.worlds == second.worlds
    assert len(first.queries) == len(second.queries) == 3
    assert all(len(set(q.outcomes)) == 2 for task in (first, second) for q in task.queries)
    assert (adaptive_gain_receipt(first).adaptive_cost, fixed_minimum_resolution(first).minimum_cost) == (2, 3)
    assert (adaptive_gain_receipt(second).adaptive_cost, fixed_minimum_resolution(second).minimum_cost) == (3, 3)


@pytest.mark.parametrize(
    ("budget", "routeable", "sequential"),
    [(0, 0.0, 0.0), (1, 0.2, 0.2), (2, 1.0, 0.4), (3, 1.0, 1.0)],
)
def test_exact_timing_profiles_under_uniform_world_frequency(budget, routeable, sequential):
    for name, expected in (("routeable", routeable), ("sequential", sequential)):
        actual = optimal_timely_resolution_mass(task_for_topology(name), UNIFORM, budget=budget)
        assert actual == pytest.approx(expected, abs=1e-12)


def test_deadline_two_is_discriminating_while_short_and_long_deadlines_are_not():
    tasks = tuple(task_for_topology(x) for x in ("routeable", "sequential"))
    difference = [
        optimal_timely_resolution_mass(tasks[0], UNIFORM, budget=b)
        - optimal_timely_resolution_mass(tasks[1], UNIFORM, budget=b)
        for b in (1, 2, 3)
    ]
    assert difference == pytest.approx([0.0, 0.6, 0.0], abs=1e-12)
    # The fixed comparator must pre-acquire its entire universal resolving
    # bundle. It is not allowed to exploit early stopping after partial cues.
    assert all(fixed_minimum_resolution(task).minimum_cost == 3 for task in tasks)


def test_prior_shift_changes_expected_profiles_without_changing_topology():
    weights = (0.5, 0.125, 0.125, 0.125, 0.125)
    fast, slow = (task_for_topology(x) for x in ("routeable", "sequential"))
    assert [optimal_timely_resolution_mass(fast, weights, budget=b) for b in (1, 2, 3)] == pytest.approx([0.125, 1.0, 1.0])
    assert [optimal_timely_resolution_mass(slow, weights, budget=b) for b in (1, 2, 3)] == pytest.approx([0.5, 0.625, 1.0])


def test_input_guards_and_cost_budget_semantics():
    task = task_for_topology("routeable")
    for probs in ((0.25,) * 4, (0.2, 0.2, 0.2, 0.2, -0.0), (0.1,) * 5):
        with pytest.raises(ValueError):
            optimal_timely_resolution_mass(task, probs, budget=2)
    for budget in (-1, 1.0):
        with pytest.raises(ValueError):
            optimal_timely_resolution_mass(task, UNIFORM, budget=budget)
    expensive = FiniteTask(
        task.worlds,
        tuple(Query(q.name, 2, q.outcomes) for q in task.queries),
    )
    assert optimal_timely_resolution_mass(expensive, UNIFORM, budget=1) == 0.0
    assert optimal_timely_resolution_mass(expensive, UNIFORM, budget=4) == pytest.approx(1.0)
