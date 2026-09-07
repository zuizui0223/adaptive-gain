import pytest

from adaptive_gain import (
    FiniteTask,
    FractionalPackingSearchLimitError,
    Query,
    World,
    adaptive_gain_receipt,
    exact_fractional_pair_packing,
    pair_packing_lower_bound,
    selected_policy_fractional_pair_packing_gain_certificate,
    selected_policy_pair_packing_gain_certificate,
)
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def _fractional_only_certificate_control():
    # C_A=2, C_F=3. Integral unit-pair packing reaches only 2, but the exact
    # fractional dual optimum is 5/2, whose integer ceiling certifies C_F>=3.
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1), World("w4", 1),
    )
    maps = (
        (1, 0, 1, 0, 1),
        (0, 1, 1, 0, 0),
        (0, 1, 1, 1, 1),
        (1, 1, 0, 1, 0),
    )
    return FiniteTask(worlds, tuple(Query(f"q{i}", 1, row) for i, row in enumerate(maps)))


def _lp_integrality_gap_control():
    # C_A=2, C_F=3, but the fractional pair-cover optimum is exactly 2.
    # The integer fixed optimum therefore needs a genuinely combinatorial cut;
    # neither integral nor fractional packing proves the strict gain.
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1), World("w4", 1),
    )
    maps = (
        (1, 0, 0, 0, 0),
        (1, 0, 0, 1, 1),
        (1, 0, 1, 0, 1),
        (0, 1, 0, 0, 1),
    )
    return FiniteTask(worlds, tuple(Query(f"q{i}", 1, row) for i, row in enumerate(maps)))


def test_fractional_dual_certifies_strict_gain_when_integral_pair_packing_cannot():
    task = _fractional_only_certificate_control()
    actual = adaptive_gain_receipt(task)
    assert (actual.adaptive_cost, actual.fixed_cost) == (2, 3)
    integral = selected_policy_pair_packing_gain_certificate(task)
    assert not integral.strict_adaptive_gain_certified_without_fixed_optimization
    assert integral.pair_packing is not None
    assert integral.pair_packing.achieved_lower_bound == 2

    fractional = selected_policy_fractional_pair_packing_gain_certificate(task)
    assert fractional.fractional_fixed_lower_bound_exact == "5/2"
    assert fractional.integer_fixed_cost_lower_bound == 3
    assert fractional.strict_adaptive_gain_certified_without_fixed_integer_optimization


def test_fractional_pair_cover_has_an_integrality_gap_and_is_not_complete_for_strict_gain():
    task = _lp_integrality_gap_control()
    actual = adaptive_gain_receipt(task)
    assert (actual.adaptive_cost, actual.fixed_cost) == (2, 3)
    packing = exact_fractional_pair_packing(task)
    assert packing.objective_exact == "2"
    assert packing.integer_fixed_cost_lower_bound == 2
    certificate = selected_policy_fractional_pair_packing_gain_certificate(task)
    assert not certificate.strict_adaptive_gain_certified_without_fixed_integer_optimization


def test_fractional_solver_recovers_payoff_private_pair_lower_bound_exactly():
    task = payoff_routing_task()
    packing = exact_fractional_pair_packing(task)
    assert packing.objective_exact == "3"
    assert packing.integer_fixed_cost_lower_bound == 3
    assert selected_policy_fractional_pair_packing_gain_certificate(
        task
    ).strict_adaptive_gain_certified_without_fixed_integer_optimization


def test_fractional_solver_does_not_false_certify_no_gain_control():
    task = routing_bypass_control()
    packing = exact_fractional_pair_packing(task)
    assert packing.objective_exact == "2"
    assert packing.integer_fixed_cost_lower_bound == 2
    assert not selected_policy_fractional_pair_packing_gain_certificate(
        task
    ).strict_adaptive_gain_certified_without_fixed_integer_optimization


def test_exact_fractional_solver_fails_closed_when_basis_cap_is_too_small():
    with pytest.raises(FractionalPackingSearchLimitError):
        exact_fractional_pair_packing(
            _fractional_only_certificate_control(), max_basis_candidates=10
        )


def test_fractional_bound_is_never_weaker_than_integral_pair_packing_on_registered_control():
    task = _fractional_only_certificate_control()
    integral = pair_packing_lower_bound(task)
    fractional = exact_fractional_pair_packing(task)
    assert fractional.objective_float >= integral.achieved_lower_bound
