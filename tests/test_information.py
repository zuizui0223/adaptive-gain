from adaptive_gain import (
    adaptive_minimum_resolution,
    best_fixed_information_bits,
    bundle_information_bits,
    routing_information_receipt,
)
from adaptive_gain.witnesses import mrod_routing_task, payoff_routing_task

def test_mrod_root_has_zero_direct_information_but_routes_one_bit_policy():
    task = mrod_routing_task()
    policy = adaptive_minimum_resolution(task).selected_policy
    receipt = routing_information_receipt(task, policy)
    assert receipt.root_query == "context"
    assert abs(receipt.root_direct_target_information_bits) < 1e-12
    assert abs(receipt.total_policy_target_information_bits - 1.0) < 1e-12
    assert abs(receipt.continuation_target_information_bits - 1.0) < 1e-12
    assert abs(receipt.next_action_entropy_bits - 1.0) < 1e-12
    assert receipt.zero_direct_information_routing_witness
    assert abs(best_fixed_information_bits(task, 2) - 0.5) < 1e-12

def test_payoff_abstract_root_is_also_zero_direct_phase_information():
    task = payoff_routing_task()
    policy = adaptive_minimum_resolution(task).selected_policy
    receipt = routing_information_receipt(task, policy)
    assert receipt.root_query == "intrinsic_r_0.5"
    assert abs(receipt.root_direct_target_information_bits) < 1e-12
    assert abs(receipt.total_policy_target_information_bits - 1.0) < 1e-12
    assert abs(receipt.next_action_entropy_bits - 1.0) < 1e-12
    assert abs(best_fixed_information_bits(task, 2) - 0.5) < 1e-12

def test_empty_bundle_information_is_zero():
    assert bundle_information_bits(mrod_routing_task(), ()) == 0.0
