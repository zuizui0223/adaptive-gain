from adaptive_gain.aedes_gonotrophic_fixture import (
    aedes_gonotrophic_q1_receipt,
    aedes_gonotrophic_q1_task,
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


def test_only_all_three_queries_resolve_fixed_task():
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
