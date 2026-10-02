from adaptive_gain import (
    adaptive_minimum_resolution,
    best_fixed_information_bits,
    bundle_information_bits,
    conditional_bundle_information_bits,
    fixed_information_minimum_cost,
    fixed_minimum_resolution,
    outcome_resolved_query_information,
    routing_information_receipt,
    target_entropy_given_history_bits,
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


def test_fixed_resolution_is_exactly_the_minimum_full_information_bundle():
    task = mrod_routing_task()
    structural = fixed_minimum_resolution(task).minimum_cost
    informational = fixed_information_minimum_cost(task)
    assert structural == 3
    assert informational == structural

    # The equivalence is structural and therefore survives any strictly
    # positive full-support reweighting of the represented worlds.
    weights = tuple(range(1, len(task.worlds) + 1))
    assert fixed_information_minimum_cost(task, weights) == structural


def test_mrod_history_switches_which_assay_contains_target_information():
    task = mrod_routing_task()

    root = outcome_resolved_query_information(task, "context")
    assert abs(root.current_target_entropy_bits - 1.0) < 1e-12
    assert abs(root.conditional_mutual_information_bits) < 1e-12
    assert len(root.outcomes) == 2
    assert all(abs(row.residual_target_entropy_bits - 1.0) < 1e-12 for row in root.outcomes)

    assert abs(target_entropy_given_history_bits(task, (("context", "0"),)) - 1.0) < 1e-12
    assert abs(target_entropy_given_history_bits(task, (("context", "1"),)) - 1.0) < 1e-12

    assert abs(
        conditional_bundle_information_bits(task, ("assay0",), (("context", "0"),)) - 1.0
    ) < 1e-12
    assert abs(
        conditional_bundle_information_bits(task, ("assay1",), (("context", "0"),))
    ) < 1e-12

    assert abs(
        conditional_bundle_information_bits(task, ("assay0",), (("context", "1"),))
    ) < 1e-12
    assert abs(
        conditional_bundle_information_bits(task, ("assay1",), (("context", "1"),)) - 1.0
    ) < 1e-12
