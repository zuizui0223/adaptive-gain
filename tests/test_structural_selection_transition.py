import pytest

from adaptive_gain.structural_selection_transition import structural_selection_transition
from adaptive_gain.resource_overlap import resource_role_profile_collision
from adaptive_gain.witnesses import direct_resolution_control, payoff_routing_task


def test_resource_collision_selection_change_is_pure_fixed_frontier_channel():
    no_gain, strict = resource_role_profile_collision()
    tr = structural_selection_transition(
        no_gain,
        strict,
        lambda_cost=2.0,
        control_cost_from=0.5,
        control_cost_to=0.5,
    )

    assert tr.identity_holds
    assert tr.adaptive_cost_from == 2
    assert tr.adaptive_cost_to == 2
    assert tr.fixed_cost_from == 2
    assert tr.fixed_cost_to == 3
    assert tr.delta_adaptive_cost == 0
    assert tr.delta_fixed_cost == 1
    assert tr.delta_structural_gap == 1
    assert tr.fixed_frontier_channel == pytest.approx(2.0)
    assert tr.adaptive_continuation_channel == pytest.approx(0.0)
    assert tr.control_channel == pytest.approx(0.0)
    assert tr.delta_log_fitness_ratio == pytest.approx(2.0)


def test_reverse_collision_reverses_only_fixed_frontier_channel():
    no_gain, strict = resource_role_profile_collision()
    tr = structural_selection_transition(
        strict,
        no_gain,
        lambda_cost=1.5,
        control_cost_from=0.25,
        control_cost_to=0.25,
    )
    assert tr.delta_adaptive_cost == 0
    assert tr.delta_fixed_cost == -1
    assert tr.fixed_frontier_channel == pytest.approx(-1.5)
    assert tr.adaptive_continuation_channel == pytest.approx(0.0)
    assert tr.delta_log_fitness_ratio == pytest.approx(-1.5)


def test_both_structural_channels_can_change():
    # direct control: C_A=C_F=1
    # payoff routing: C_A=2, C_F=3
    tr = structural_selection_transition(
        direct_resolution_control(),
        payoff_routing_task(),
        lambda_cost=1.2,
        control_cost_from=0.0,
        control_cost_to=0.0,
    )
    assert tr.delta_adaptive_cost == 1
    assert tr.delta_fixed_cost == 2
    assert tr.delta_structural_gap == 1
    assert tr.fixed_frontier_channel == pytest.approx(2.4)
    assert tr.adaptive_continuation_channel == pytest.approx(-1.2)
    assert tr.delta_log_fitness_ratio == pytest.approx(1.2)


def test_control_cost_change_is_separate_channel():
    task = payoff_routing_task()
    tr = structural_selection_transition(
        task,
        task,
        lambda_cost=3.0,
        control_cost_from=0.2,
        control_cost_to=0.9,
    )
    assert tr.delta_adaptive_cost == 0
    assert tr.delta_fixed_cost == 0
    assert tr.fixed_frontier_channel == pytest.approx(0.0)
    assert tr.adaptive_continuation_channel == pytest.approx(0.0)
    assert tr.control_channel == pytest.approx(-0.7)
    assert tr.delta_log_fitness_ratio == pytest.approx(-0.7)
