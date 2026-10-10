import math

import pytest

from adaptive_gain.bounded_arity_extremal_bounds import (
    bounded_arity_unit_cost_witness_at_depth,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution
from adaptive_gain.opportunity_extremal_envelope import (
    sharp_exponential_opportunity_envelope,
    sharp_completion_value_envelope,
    sharp_log_selection_envelope,
    sharp_opportunity_advantage_envelope,
    sharp_maintenance_log_cost_ceiling,
    robust_positive_advantage_possible_in_scope,
)


def exp_survival(mu):
    return lambda c: math.exp(-mu * c)


def test_binary_n10_m9_urgency_changes_sharp_depth():
    low = sharp_exponential_opportunity_envelope(
        10, 9, 2, closure_rate=0.10
    )
    middle = sharp_exponential_opportunity_envelope(
        10, 9, 2, closure_rate=0.30
    )
    high = sharp_exponential_opportunity_envelope(
        10, 9, 2, closure_rate=1.00
    )

    assert low.maximizing_adaptive_costs == (4,)
    assert middle.maximizing_adaptive_costs == (3,)
    assert high.maximizing_adaptive_costs == (2,)


def test_binary_n10_m9_exact_rows_match_structural_frontier():
    receipt = sharp_exponential_opportunity_envelope(
        10, 9, 2, closure_rate=0.3
    )
    rows = {row.adaptive_cost: row for row in receipt.rows}

    assert (rows[2].adaptive_cost, rows[2].sharp_fixed_cost) == (2, 3)
    assert (rows[3].adaptive_cost, rows[3].sharp_fixed_cost) == (3, 7)
    assert (rows[4].adaptive_cost, rows[4].sharp_fixed_cost) == (4, 9)


def test_envelope_is_attained_by_explicit_arbitrary_depth_witnesses():
    mu = 0.3
    receipt = sharp_exponential_opportunity_envelope(
        8, 6, 3, closure_rate=mu
    )

    for row in receipt.rows:
        task = bounded_arity_unit_cost_witness_at_depth(
            8, 6, 3, row.adaptive_cost
        )
        ca = adaptive_minimum_resolution(task).minimum_worst_path_cost
        cf = fixed_minimum_resolution(task).minimum_cost

        assert ca == row.adaptive_cost
        assert cf == row.sharp_fixed_cost

        direct = math.exp(-mu * ca) - math.exp(-mu * cf)
        assert direct == pytest.approx(row.opportunity_advantage)


def test_log_selection_envelope_uses_same_sharp_depth_without_maintenance():
    performance = sharp_opportunity_advantage_envelope(
        10,
        9,
        2,
        exp_survival(0.3),
        resolution_value=1e-6,
    )
    selection = sharp_log_selection_envelope(
        10,
        9,
        2,
        exp_survival(0.3),
        baseline_fitness=1.0,
        resolution_value=1e-6,
        maintenance_log_cost=0.0,
    )

    assert selection.maximizing_adaptive_costs == performance.maximizing_adaptive_costs


def test_nonincreasing_survival_is_required():
    with pytest.raises(ValueError):
        sharp_opportunity_advantage_envelope(
            5,
            4,
            2,
            lambda c: min(1.0, 0.2 + 0.1 * c),
        )



def test_maintenance_cost_ceiling_is_exact_robust_existence_threshold():
    survival = exp_survival(0.3)
    ceiling = sharp_maintenance_log_cost_ceiling(
        10,
        9,
        2,
        survival,
        baseline_fitness=1.0,
        resolution_value=1.0,
    )
    assert ceiling > 0.0

    assert robust_positive_advantage_possible_in_scope(
        10,
        9,
        2,
        survival,
        baseline_fitness=1.0,
        resolution_value=1.0,
        maintenance_log_cost=0.99 * ceiling,
    )
    assert not robust_positive_advantage_possible_in_scope(
        10,
        9,
        2,
        survival,
        baseline_fitness=1.0,
        resolution_value=1.0,
        maintenance_log_cost=ceiling,
    )
    assert not robust_positive_advantage_possible_in_scope(
        10,
        9,
        2,
        survival,
        baseline_fitness=1.0,
        resolution_value=1.0,
        maintenance_log_cost=1.01 * ceiling,
    )


def test_exponential_maintenance_ceiling_is_small_at_urgency_extremes():
    low = sharp_maintenance_log_cost_ceiling(
        10, 9, 2, exp_survival(1e-5)
    )
    middle = sharp_maintenance_log_cost_ceiling(
        10, 9, 2, exp_survival(0.3)
    )
    high = sharp_maintenance_log_cost_ceiling(
        10, 9, 2, exp_survival(10.0)
    )

    assert low < middle
    assert high < middle



def test_unbounded_structural_ratio_still_has_finite_log_fitness_ceiling():
    w0 = 2.0
    value = 3.0
    receipt = sharp_log_selection_envelope(
        20,
        20,
        2,
        exp_survival(0.2),
        baseline_fitness=w0,
        resolution_value=value,
        maintenance_log_cost=0.0,
    )
    universal_ceiling = math.log(1.0 + value / w0)
    assert receipt.sharp_log_selection <= universal_ceiling + 1e-12



def test_general_monotone_value_envelope_contains_opportunity_special_case():
    mu = 0.3
    general = sharp_completion_value_envelope(
        10,
        9,
        2,
        lambda c: math.exp(-mu * c),
    )
    special = sharp_exponential_opportunity_envelope(
        10,
        9,
        2,
        closure_rate=mu,
    )
    assert general.sharp_opportunity_advantage == pytest.approx(
        special.sharp_opportunity_advantage
    )
    assert general.maximizing_adaptive_costs == special.maximizing_adaptive_costs


def test_linear_completion_value_recovers_maximum_additive_gap():
    lam = 0.4
    receipt = sharp_completion_value_envelope(
        10,
        9,
        2,
        lambda c: -lam * c,
    )
    rows = {row.adaptive_cost: row for row in receipt.rows}
    expected = lam * max(row.structural_gap for row in receipt.rows)
    assert receipt.sharp_opportunity_advantage == pytest.approx(expected)
    assert receipt.maximizing_adaptive_costs == (4,)
    assert rows[4].structural_gap == 5


def test_general_completion_value_must_be_nonincreasing():
    with pytest.raises(ValueError):
        sharp_completion_value_envelope(
            5,
            4,
            2,
            lambda c: c,
        )



def test_structural_ratio_can_increase_while_ecological_value_falls():
    mu = 0.3

    def ratio(depth):
        return (2 ** depth) / (depth + 1)

    def opportunity_value(depth):
        ca = depth + 1
        cf = 2 ** depth
        return math.exp(-mu * ca) - math.exp(-mu * cf)

    assert ratio(5) > ratio(4)
    assert opportunity_value(5) < opportunity_value(4)
