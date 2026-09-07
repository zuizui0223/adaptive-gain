from adaptive_gain import branch_invariant_no_routing_certificate, routing_certificate
from adaptive_gain.witnesses import mrod_routing_task

def test_branch_dependence_does_not_by_itself_certify_gain():
    receipt = branch_invariant_no_routing_certificate({"a": "state0", "b": "state1"})
    assert receipt.branch_invariant is False
    assert "possible but not guaranteed" in receipt.interpretation

def test_routing_certificate_is_budget_local():
    task = mrod_routing_task()
    low = routing_certificate(task, "context", 1)
    middle = routing_certificate(task, "context", 2)
    high = routing_certificate(task, "context", 3)
    assert not low.strict_adaptive_only_resolution_certified
    assert middle.strict_adaptive_only_resolution_certified
    assert not high.strict_adaptive_only_resolution_certified
    assert high.every_branch_resolvable
    assert not high.no_fixed_resolution_within_budget
