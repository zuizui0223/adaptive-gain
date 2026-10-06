import math

import pytest

from adaptive_gain.bounded_arity_extremal_bounds import (
    bounded_arity_unit_cost_witness_at_depth,
)
from adaptive_gain.core import adaptive_minimum_resolution, fixed_minimum_resolution
from adaptive_gain.opportunity_extremal_envelope import (
    sharp_exponential_opportunity_envelope,
    sharp_log_selection_envelope,
    sharp_opportunity_advantage_envelope,
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
