from adaptive_gain import adaptive_gain_receipt, resolution_budget_profile, routing_certificate
from adaptive_gain.witnesses import (
    balance_no_routing_certificates,
    direct_resolution_control,
    mrod_routing_task,
    payoff_routing_task,
)

def test_mrod_style_witness_is_two_adaptive_three_fixed():
    task = mrod_routing_task()
    receipt = adaptive_gain_receipt(task)
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
    cert = routing_certificate(task, "context", 2)
    assert cert.strict_adaptive_only_resolution_certified
    assert cert.branch_dependent_next_action
    assert {b.selected_next_query for b in cert.branches} == {"assay0", "assay1"}

def test_payoff_style_witness_is_two_adaptive_three_fixed():
    task = payoff_routing_task()
    receipt = adaptive_gain_receipt(task)
    assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
    cert = routing_certificate(task, "intrinsic_r_0.5", 2)
    assert cert.strict_adaptive_only_resolution_certified
    assert {b.selected_next_query for b in cert.branches} == {
        "interaction_d_0.1",
        "interaction_d_0.2",
    }

def test_positive_witnesses_have_same_adaptive_only_budget_window():
    for task in (mrod_routing_task(), payoff_routing_task()):
        rows = resolution_budget_profile(task, 3)
        assert [row.budget for row in rows if row.adaptive_only] == [2]

def test_balance_span_witness_is_branch_invariant():
    forward, reverse = balance_no_routing_certificates()
    assert forward.branch_invariant
    assert reverse.branch_invariant

def test_direct_control_window_is_empty():
    receipt = adaptive_gain_receipt(direct_resolution_control())
    assert receipt.strict_adaptive_gain is False
