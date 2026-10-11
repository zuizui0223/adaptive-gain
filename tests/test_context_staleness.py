"""Regression tests for a declared context-staleness ecological comparator."""
import math

import pytest

from adaptive_gain.context_staleness import (
    completion_comparator,
    coupled_never_advantage,
    coupled_volatility_net_gain,
    critical_staleness,
    log_selection_a_vs_p,
    stale_context_probability,
)


def test_flip_probability_is_markov_two_state_transition():
    # Independent closed-form solution of the two-state CTMC.
    for nu in (0, 0.01, 0.1, 1, 5):
        for lag in (0, 0.1, 1, 2):
            q = stale_context_probability(nu, lag)
            assert q == pytest.approx((1 - math.exp(-2 * nu * lag)) / 2)
            assert 0 <= q <= 0.5


def test_preindexed_can_dominate_routing():
    # A=2, P=1. A can outperform a universal fixed comparator U while
    # losing to a context-preindexed competitor P with a reliable memory.
    c = completion_comparator(
        context_flip_probability=0,
        opportunity_hazard=0.3,
        routing_time=1,
        terminal_time=1,
    )
    assert c.adaptive == pytest.approx(math.exp(-0.6))
    assert c.preindexed == pytest.approx(math.exp(-0.3))
    assert c.advantage < 0
    assert log_selection_a_vs_p(c, baseline_fitness=1.0) < 0


def test_staleness_and_opportunity_cost_exact_crossing():
    args = dict(opportunity_hazard=0.3, routing_time=1.0,
                terminal_time=2.0, stale_relative_success=0.2)
    threshold = critical_staleness(**args)
    assert threshold == pytest.approx((1 - math.exp(-0.3)) / 0.8)
    assert threshold is not None
    for q, selected in ((threshold - 0.01, False),
                        (threshold + 0.01, True)):
        comp = completion_comparator(context_flip_probability=q, **args)
        assert (comp.advantage > 0) == selected
    assert completion_comparator(
        context_flip_probability=threshold, **args
    ).advantage == pytest.approx(0)


def test_critical_staleness_includes_maintenance_in_reward_units():
    args = dict(opportunity_hazard=0.2, routing_time=1,
                terminal_time=2, reward_value=2,
                stale_relative_success=0.1, additive_control_cost=0.03)
    q = critical_staleness(**args)
    assert q is not None
    comp = completion_comparator(
        context_flip_probability=q,
        opportunity_hazard=args["opportunity_hazard"],
        routing_time=args["routing_time"],
        terminal_time=args["terminal_time"],
        stale_relative_success=args["stale_relative_success"],
    )
    assert (args["reward_value"] * comp.advantage
            - args["additive_control_cost"]) == pytest.approx(0)
    assert critical_staleness(opportunity_hazard=100,
                              routing_time=1) is None
    assert critical_staleness(opportunity_hazard=0.3, routing_time=1,
                              stale_relative_success=1) is None


def test_log_fitness_uses_a_distinct_cost_currency():
    comp = completion_comparator(context_flip_probability=0.4,
        opportunity_hazard=0.2, routing_time=1, terminal_time=1)
    raw_log = log_selection_a_vs_p(
        comp, baseline_fitness=2, reward_value=1.5)
    direct = math.log((2 + 1.5 * comp.adaptive) /
                      (2 + 1.5 * comp.preindexed))
    assert raw_log == pytest.approx(direct)
    assert log_selection_a_vs_p(comp, baseline_fitness=2,
        reward_value=1.5,
        log_maintenance_difference=raw_log) == pytest.approx(0)


def test_intermediate_volatility_selection_window_needs_coupled_hazard():
    args = dict(memory_lag=2.0, hazard_per_turnover=0.3,
                routing_time=1.0, terminal_time=1.0,
                stale_relative_success=0.1, reward_value=1.0)
    assert not coupled_never_advantage(
        memory_lag=args["memory_lag"],
        hazard_per_turnover=args["hazard_per_turnover"],
        routing_time=args["routing_time"],
        stale_relative_success=args["stale_relative_success"],
    )
    k = 0.05
    values = [coupled_volatility_net_gain(
        turnover_rate=nu, additive_control_cost=k, **args
    ) for nu in (0.0, 0.5, 30.0)]
    assert values[0] < 0 < values[1]
    assert values[2] < 0


def test_coupled_hazard_no_positive_performance_grid():
    assert coupled_never_advantage(
        memory_lag=0.2, hazard_per_turnover=0.7,
        routing_time=1, stale_relative_success=0.5)
    for rate in (0, 0.001, 0.01, 0.1, 0.25, 1, 5, 20):
        net = coupled_volatility_net_gain(
            turnover_rate=rate, memory_lag=0.2,
            hazard_per_turnover=0.7, routing_time=1,
            terminal_time=2, stale_relative_success=0.5)
        assert net <= 1e-15


def test_high_turnover_reversal_requires_hazard_turnover_coupling():
    kwargs = dict(opportunity_hazard=0.3, routing_time=1,
                  terminal_time=1, stale_relative_success=0.1)
    gains = [completion_comparator(
        context_flip_probability=stale_context_probability(nu, 2),
        **kwargs).advantage for nu in (0.1, 0.5, 1, 2, 10)]
    assert gains == sorted(gains)
    assert gains[-1] > 0


def test_critical_q_independent_of_terminal_time_without_k():
    args = dict(opportunity_hazard=0.4, routing_time=0.5,
                stale_relative_success=0.2,
                additive_control_cost=0)
    thresholds = [critical_staleness(terminal_time=a, **args)
                  for a in (0, 1, 10, 100)]
    assert thresholds == pytest.approx([thresholds[0]] * 4)


def test_invalid_inputs_cannot_silently_generate_fitness():
    with pytest.raises(ValueError):
        stale_context_probability(-1, 2)
    with pytest.raises(ValueError):
        completion_comparator(context_flip_probability=0.2,
            opportunity_hazard=0.5, routing_time=1, terminal_time=1,
            stale_relative_success=1.2)
    with pytest.raises(ValueError):
        log_selection_a_vs_p(completion_comparator(
            context_flip_probability=0, opportunity_hazard=0,
            routing_time=0, terminal_time=0), baseline_fitness=0)
    with pytest.raises(ValueError):
        coupled_volatility_net_gain(turnover_rate=float("nan"),
            memory_lag=1, hazard_per_turnover=0.3,
            routing_time=1, terminal_time=1)
