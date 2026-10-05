import math

import pytest

from adaptive_gain.opportunity_fitness import (
    exponential_max_window_mass,
    exponential_optimal_closure_rate,
    exponential_window_mass,
    opportunity_selection_margin,
    opportunity_window_mass,
    pathwise_advantage_over_fixed,
)


def exp_survival(rate):
    return lambda c: math.exp(-rate * c)


def test_window_mass_is_survival_difference():
    rate = 0.4
    got = opportunity_window_mass(2.0, 3.0, exp_survival(rate))
    expected = math.exp(-0.8) - math.exp(-1.2)
    assert got == pytest.approx(expected)


def test_payoff_style_witness_has_exact_interior_optimum():
    c_a, c_f = 2.0, 3.0
    rate_star = exponential_optimal_closure_rate(c_a, c_f)
    assert rate_star == pytest.approx(math.log(1.5))
    assert exponential_window_mass(c_a, c_f, rate_star) == pytest.approx(4.0 / 27.0)
    assert exponential_max_window_mass(c_a, c_f) == pytest.approx(4.0 / 27.0)


def test_gap_two_witness_peak():
    c_a, c_f = 2.0, 4.0
    rate_star = exponential_optimal_closure_rate(c_a, c_f)
    assert rate_star == pytest.approx(math.log(2.0) / 2.0)
    assert exponential_window_mass(c_a, c_f, rate_star) == pytest.approx(0.25)


def test_window_is_hump_shaped_around_unique_optimum():
    c_a, c_f = 2.0, 3.0
    rate_star = exponential_optimal_closure_rate(c_a, c_f)
    peak = exponential_window_mass(c_a, c_f, rate_star)
    assert exponential_window_mass(c_a, c_f, rate_star / 3.0) < peak
    assert exponential_window_mass(c_a, c_f, rate_star * 3.0) < peak
    assert exponential_window_mass(c_a, c_f, 0.0) == pytest.approx(0.0)


def test_equal_gap_does_not_imply_equal_fitness_value():
    rate = 0.5
    early = exponential_window_mass(1.0, 2.0, rate)
    late = exponential_window_mass(3.0, 4.0, rate)
    assert early > late


def test_maintenance_cost_subtracts_from_opportunity_benefit():
    rate = 0.4
    surv = exp_survival(rate)
    raw = opportunity_window_mass(2.0, 3.0, surv)
    margin = opportunity_selection_margin(
        2.0,
        3.0,
        surv,
        value=2.0,
        maintenance_cost=0.1,
    )
    assert margin == pytest.approx(2.0 * raw - 0.1)


def test_pathwise_advantage_exceeds_worst_path_window_lower_bound():
    rate = 0.4
    surv = exp_survival(rate)
    adaptive_costs = [1.0, 2.0, 2.0]
    probs = [0.2, 0.3, 0.5]
    c_a = max(adaptive_costs)
    c_f = 3.0

    pathwise = pathwise_advantage_over_fixed(
        adaptive_costs,
        probs,
        c_f,
        surv,
        value=1.0,
    )
    lower_bound = opportunity_window_mass(c_a, c_f, surv)

    assert pathwise > lower_bound


def test_invalid_cost_order_is_rejected():
    with pytest.raises(ValueError):
        exponential_window_mass(3.0, 2.0, 0.5)


def test_optimal_rate_requires_strict_positive_window():
    with pytest.raises(ValueError):
        exponential_optimal_closure_rate(0.0, 2.0)
    with pytest.raises(ValueError):
        exponential_optimal_closure_rate(2.0, 2.0)
