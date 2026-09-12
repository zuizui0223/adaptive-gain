import pytest

from adaptive_gain.aedes_gonotrophic_fixture import (
    aedes_gonotrophic_coarsened_target_task,
    aedes_gonotrophic_q1_receipt,
    aedes_gonotrophic_q1_task,
    aedes_gonotrophic_weighted_receipt,
    aedes_gonotrophic_weighted_task,
    aedes_target_coarsening_receipt,
)
from adaptive_gain.core import (
    adaptive_gain_receipt,
    adaptive_minimum_resolution,
    bundle_resolves,
    fixed_minimum_resolution,
)


def test_aedes_q1_fixture_has_exact_gap_one():
    receipt = aedes_gonotrophic_q1_receipt()
    assert receipt.adaptive_cost == 2
    assert receipt.fixed_cost == 3
    assert receipt.structural_gap == 1
    assert receipt.prospective_only is True


def test_gonotrophic_state_is_unique_optimal_adaptive_root():
    task = aedes_gonotrophic_q1_task()
    adaptive = adaptive_minimum_resolution(task)
    assert adaptive.minimum_worst_path_cost == 2
    assert adaptive.optimal_first_queries == ("gonotrophic_state",)
    assert adaptive.selected_policy is not None
    assert adaptive.selected_policy.query == "gonotrophic_state"


def test_only_all_three_queries_resolve_four_target_fixed_task():
    task = aedes_gonotrophic_q1_task()
    names = tuple(query.name for query in task.queries)
    assert bundle_resolves(task, names)
    for omitted in names:
        pair = tuple(name for name in names if name != omitted)
        assert not bundle_resolves(task, pair)
    fixed = fixed_minimum_resolution(task)
    assert fixed.minimum_cost == 3
    assert fixed.optimal_bundles == (names,)


def test_exact_solver_marks_strict_gain_without_empirical_claim():
    task = aedes_gonotrophic_q1_task()
    exact = adaptive_gain_receipt(task)
    assert exact.status == "strict_adaptive_gain"
    assert exact.adaptive_cost == 2
    assert exact.fixed_cost == 3


def test_unequal_positive_cost_formula_matches_exact_solver_on_grid():
    for state_cost in range(1, 5):
        for host_cost in range(1, 5):
            for oviposition_cost in range(1, 5):
                receipt = aedes_gonotrophic_weighted_receipt(
                    state_cost,
                    host_cost,
                    oviposition_cost,
                )
                assert receipt.adaptive_cost == state_cost + max(host_cost, oviposition_cost)
                assert receipt.fixed_cost == state_cost + host_cost + oviposition_cost
                assert receipt.structural_gap == min(host_cost, oviposition_cost)
                assert receipt.structural_gap > 0
                assert receipt.exact_formula_verified is True
                assert receipt.prospective_only is True


def test_weighted_four_target_fixture_keeps_state_as_unique_optimal_root():
    for costs in ((1, 2, 7), (9, 1, 5), (3, 8, 2), (12, 4, 4)):
        task = aedes_gonotrophic_weighted_task(*costs)
        adaptive = adaptive_minimum_resolution(task)
        assert adaptive.optimal_first_queries == ("gonotrophic_state",)


def test_unit_cost_target_coarsening_collapses_gap_to_zero():
    receipt = aedes_target_coarsening_receipt(1, 1, 1)
    assert receipt.adaptive_cost == 2
    assert receipt.fixed_cost == 2
    assert receipt.structural_gap == 0
    assert receipt.strict_gain is False
    task = aedes_gonotrophic_coarsened_target_task(1, 1, 1)
    fixed = fixed_minimum_resolution(task)
    assert fixed.optimal_bundles == (("host_acidic_cue", "oviposition_odor_cue"),)


def test_coarsened_target_formula_matches_exact_solver_on_grid():
    for state_cost in range(1, 5):
        for host_cost in range(1, 5):
            for oviposition_cost in range(1, 5):
                receipt = aedes_target_coarsening_receipt(
                    state_cost,
                    host_cost,
                    oviposition_cost,
                )
                expected_gap = max(0, min(host_cost, oviposition_cost) - state_cost)
                assert receipt.fixed_cost == host_cost + oviposition_cost
                assert receipt.adaptive_cost == min(
                    host_cost + oviposition_cost,
                    state_cost + max(host_cost, oviposition_cost),
                )
                assert receipt.structural_gap == expected_gap
                assert receipt.strict_gain is (expected_gap > 0)


def test_coarsened_targets_can_recover_gain_only_if_state_is_cheaper():
    positive = aedes_target_coarsening_receipt(1, 3, 5)
    assert positive.structural_gap == 2
    assert positive.strict_gain is True
    zero = aedes_target_coarsening_receipt(3, 3, 5)
    assert zero.structural_gap == 0
    assert zero.strict_gain is False


@pytest.mark.parametrize(
    "costs",
    [
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (-1, 1, 1),
        (1.0, 1, 1),
    ],
)
def test_weighted_fixture_rejects_nonpositive_or_noninteger_costs(costs):
    with pytest.raises(ValueError):
        aedes_gonotrophic_weighted_task(*costs)
