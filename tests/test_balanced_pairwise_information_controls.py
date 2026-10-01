from adaptive_gain.balanced_pairwise_information_controls import (
    pairwise_matched_control_audit,
    pairwise_matched_control_task,
    target_query_signature_multiset,
)
from adaptive_gain.balanced_binary_extremal_family import (
    balanced_binary_extremal_task,
)


def test_depth_two_pairwise_matched_control_is_no_gain():
    receipt = pairwise_matched_control_audit(2)
    assert receipt.theorem_holds
    assert receipt.same_query_matrix
    assert receipt.same_target_multiplicities
    assert receipt.same_pairwise_target_query_signature_multiset
    assert receipt.routeable_target_multiplicities == (6, 4)
    assert receipt.control_target_multiplicities == (6, 4)
    assert receipt.control_adaptive_cost == 2
    assert receipt.control_fixed_cost == 2
    assert receipt.control_fixed_resolver_names == ("terminal_1", "terminal_2")


def test_depth_three_pairwise_matched_control_has_fixed_cost_three():
    receipt = pairwise_matched_control_audit(3)
    assert receipt.theorem_holds
    assert receipt.same_query_matrix
    assert receipt.same_target_multiplicities
    assert receipt.same_pairwise_target_query_signature_multiset
    assert receipt.routeable_target_multiplicities == (10, 8)
    assert receipt.control_target_multiplicities == (10, 8)
    assert receipt.control_fixed_cost == 3
    assert receipt.control_fixed_resolver_names == (
        "route_bit_0",
        "terminal_1",
        "terminal_6",
    )
    assert receipt.control_adaptive_cost <= 3


def test_pairwise_match_is_multiset_not_named_identity():
    routeable = balanced_binary_extremal_task(2)
    control = pairwise_matched_control_task(2)

    assert target_query_signature_multiset(routeable) == target_query_signature_multiset(
        control
    )

    routeable_by_name = {
        q.name: sig
        for q, sig in zip(routeable.queries, target_query_signature_multiset_by_order(routeable))
    }
    control_by_name = {
        q.name: sig
        for q, sig in zip(control.queries, target_query_signature_multiset_by_order(control))
    }
    assert routeable_by_name != control_by_name


def target_query_signature_multiset_by_order(task):
    target = tuple(world.target for world in task.worlds)
    from adaptive_gain.balanced_pairwise_information_controls import (
        _canonical_binary_pair_signature,
    )

    return tuple(
        _canonical_binary_pair_signature(target, tuple(query.outcomes))
        for query in task.queries
    )
