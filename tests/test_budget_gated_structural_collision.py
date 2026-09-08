from math import log

import pytest

from adaptive_gain.budget_gated_selection import (
    budget_fitness_state,
    budget_frequency_path,
    budget_selection_path,
)
from adaptive_gain.resource_overlap import resource_role_profile_collision
from adaptive_gain.structural_eco_evolution import (
    evolutionary_selection_activity,
    evolutionary_selection_retention,
    evolutionary_selection_retention_ratio,
)


def test_same_continuation_and_role_profiles_reverse_hard_budget_selection():
    no_gain, strict = resource_role_profile_collision()
    half_log2 = 0.5 * log(2.0)

    low = budget_fitness_state(
        no_gain,
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=half_log2,
    )
    high = budget_fitness_state(
        strict,
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=half_log2,
    )

    assert low.resolution.adaptive_cost == 2
    assert low.resolution.fixed_cost == 2
    assert low.resolution.adaptive_resolves
    assert low.resolution.fixed_resolves
    assert not low.resolution.adaptive_only_window
    assert low.log_fitness_ratio == pytest.approx(-half_log2)

    assert high.resolution.adaptive_cost == 2
    assert high.resolution.fixed_cost == 3
    assert high.resolution.adaptive_resolves
    assert not high.resolution.fixed_resolves
    assert high.resolution.adaptive_only_window
    assert high.log_fitness_ratio == pytest.approx(half_log2)


def test_higher_order_collision_can_produce_exact_burst_stasis_cycles_without_linear_cost_value():
    no_gain, strict = resource_role_profile_collision()
    half_log2 = 0.5 * log(2.0)

    selection = budget_selection_path(
        (strict, no_gain, strict, no_gain),
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=half_log2,
    )

    assert selection == pytest.approx(
        (half_log2, -half_log2, half_log2, -half_log2)
    )
    assert evolutionary_selection_activity(selection) == pytest.approx(4 * half_log2)
    assert evolutionary_selection_retention(selection) == pytest.approx(0.0)
    assert evolutionary_selection_retention_ratio(selection) == pytest.approx(0.0)

    path = budget_frequency_path(
        0.42,
        (strict, no_gain, strict, no_gain),
        2,
        baseline_fitness=1.0,
        resolution_benefit=1.0,
        contingent_maintenance_log_cost=half_log2,
    )
    assert path[1] != pytest.approx(path[0])
    assert path[2] == pytest.approx(path[0])
    assert path[4] == pytest.approx(path[0])
