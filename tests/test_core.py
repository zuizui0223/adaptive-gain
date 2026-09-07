from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    adaptive_minimum_resolution,
    adaptive_only_at_budget,
    bundle_resolves,
    fixed_minimum_resolution,
    resolution_budget_profile,
)

def test_direct_control_has_no_strict_gain():
    task = FiniteTask(
        (World("a", 0), World("b", 1)),
        (Query("direct", 1, ("x", "y")),),
    )
    assert bundle_resolves(task, ("direct",))
    assert fixed_minimum_resolution(task).minimum_cost == 1
    assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 1
    receipt = adaptive_gain_receipt(task)
    assert receipt.strict_adaptive_gain is False
    assert receipt.adaptive_only_budget_lower is None

def test_budget_window_is_exact_integer_interval():
    from adaptive_gain.witnesses import mrod_routing_task
    task = mrod_routing_task()
    receipt = adaptive_gain_receipt(task)
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
    assert adaptive_only_at_budget(task, 2)
    assert not adaptive_only_at_budget(task, 1)
    assert not adaptive_only_at_budget(task, 3)
    rows = resolution_budget_profile(task, 3)
    assert [(r.adaptive_guaranteed, r.fixed_guaranteed, r.adaptive_only) for r in rows] == [
        (False, False, False),
        (False, False, False),
        (True, False, True),
        (True, True, False),
    ]

def test_already_identified_target_costs_zero():
    task = FiniteTask(
        (World("a", "same"), World("b", "same")),
        (Query("noise", 2, ("x", "y")),),
    )
    assert fixed_minimum_resolution(task).minimum_cost == 0
    assert adaptive_minimum_resolution(task).minimum_worst_path_cost == 0

def test_invalid_query_outcome_length_is_rejected():
    try:
        FiniteTask(
            (World("a", 0), World("b", 1)),
            (Query("bad", 1, ("x",)),),
        )
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
