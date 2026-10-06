import math

import pytest

from adaptive_gain.core import (
    FiniteTask,
    Query,
    World,
    adaptive_minimum_resolution,
)
from adaptive_gain.policy_fitness import (
    discounted_fitness_optimal_policy,
    policy_world_path_costs,
)


def _minimax_vs_fitness_witness():
    worlds = (
        World("w0_common", 0),
        World("w1_rare0", 0),
        World("w2_rare1a", 1),
        World("w3_rare1b", 1),
    )
    queries = (
        Query("q0", 1, (0, 0, 0, 1)),
        Query("q1", 1, (0, 0, 1, 0)),
        Query("q2", 1, (0, 1, 0, 1)),
        Query("q3_common_first", 1, (0, 1, 1, 1)),
    )
    return FiniteTask(worlds, queries)


def test_fitness_optimum_can_reject_the_minimax_policy():
    task = _minimax_vs_fitness_witness()
    probs = (27 / 30, 1 / 30, 1 / 30, 1 / 30)
    mu = math.log(2.0)

    minimax = adaptive_minimum_resolution(task)
    assert minimax.minimum_worst_path_cost == 2
    assert minimax.selected_policy is not None
    minimax_costs = policy_world_path_costs(
        task,
        minimax.selected_policy,
    )
    assert minimax_costs == (2.0, 2.0, 2.0, 1.0)

    minimax_value = sum(
        p * math.exp(-mu * t)
        for p, t in zip(probs, minimax_costs)
    )
    assert minimax_value == pytest.approx(31 / 120)

    fitness = discounted_fitness_optimal_policy(
        task,
        probs,
        discount_rate=mu,
    )
    assert fitness.selected_policy is not None
    assert fitness.selected_policy.query == "q3_common_first"
    assert fitness.world_path_costs in (
        (1.0, 3.0, 3.0, 2.0),
        (1.0, 3.0, 2.0, 3.0),
    )
    assert fitness.worst_path_cost == 3.0
    assert fitness.expected_discounted_completion_value == pytest.approx(7 / 15)

    assert fitness.expected_discounted_completion_value > minimax_value


def test_uniform_worlds_restore_minimax_like_pressure_in_witness():
    task = _minimax_vs_fitness_witness()
    fitness = discounted_fitness_optimal_policy(
        task,
        (0.25, 0.25, 0.25, 0.25),
        discount_rate=math.log(2.0),
    )

    assert fitness.selected_policy is not None
    assert fitness.worst_path_cost == 2.0
