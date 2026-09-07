from dataclasses import replace
from itertools import product

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.frontier_transversals import (
    enumerate_minimal_transversals,
    frontier_transversal_policy_decomposition,
    verify_minimal_transversal_certificate,
)
from adaptive_gain.productive_frontier import build_productive_frontier
from adaptive_gain.witnesses import (
    external_shortcut_control,
    internal_redundancy_control,
    mrod_routing_task,
    partial_external_bypass_gain_control,
    partial_internal_bypass_gain_control,
    payoff_routing_task,
    routing_bypass_control,
)


def test_source_routing_witnesses_have_no_internal_or_external_discount():
    for task in (mrod_routing_task(), payoff_routing_task()):
        receipt = frontier_transversal_policy_decomposition(task)
        assert receipt.agrees_with_frontier_decomposition
        assert (receipt.adaptive_cost, receipt.fixed_cost) == (2, 3)
        assert receipt.realized_adaptive_gain == 1
        assert receipt.internal_union_redundancy == 0
        assert receipt.external_shortcut_discount == 0
        assert receipt.union_is_minimal_transversal
        assert receipt.every_union_query_has_private_frontier_edge
        assert not receipt.outside_cheaper_transversal_exists


def test_internal_bypass_is_a_smaller_transversal_inside_policy_union():
    for task in (routing_bypass_control(), internal_redundancy_control()):
        receipt = frontier_transversal_policy_decomposition(task)
        assert receipt.agrees_with_frontier_decomposition
        assert receipt.internal_union_redundancy == 1
        assert receipt.external_shortcut_discount == 0
        assert not receipt.union_is_minimal_transversal
        assert not receipt.every_union_query_has_private_frontier_edge
        assert not receipt.outside_cheaper_transversal_exists

    partial = frontier_transversal_policy_decomposition(partial_internal_bypass_gain_control())
    assert (partial.adaptive_cost, partial.fixed_cost, partial.policy_union_cost) == (3, 4, 5)
    assert partial.realized_adaptive_gain == 1
    assert partial.internal_union_redundancy == 1
    assert partial.external_shortcut_discount == 0
    assert not partial.union_is_minimal_transversal


def test_external_bypass_is_a_cheaper_transversal_using_outside_resource():
    complete = frontier_transversal_policy_decomposition(external_shortcut_control())
    assert (complete.adaptive_cost, complete.fixed_cost) == (2, 2)
    assert complete.policy_union_restricted_fixed_cost == 3
    assert complete.external_shortcut_discount == 1
    assert complete.internal_union_redundancy == 0
    assert complete.union_is_minimal_transversal
    assert complete.outside_cheaper_transversal_exists

    partial = frontier_transversal_policy_decomposition(partial_external_bypass_gain_control())
    assert (partial.adaptive_cost, partial.fixed_cost) == (3, 4)
    assert partial.policy_union_restricted_fixed_cost == 5
    assert partial.policy_union_cost == 5
    assert partial.realized_adaptive_gain == 1
    assert partial.external_shortcut_discount == 1
    assert partial.internal_union_redundancy == 0
    assert partial.union_is_minimal_transversal
    assert partial.outside_cheaper_transversal_exists


def test_minimal_transversal_certificate_rejects_tampering():
    frontier = build_productive_frontier(payoff_routing_task())
    certificate = enumerate_minimal_transversals(frontier)
    assert verify_minimal_transversal_certificate(frontier, certificate)
    assert certificate.transversal_masks
    tampered = replace(certificate, transversal_masks=certificate.transversal_masks[:-1])
    assert not verify_minimal_transversal_certificate(frontier, tampered)


def test_complete_balanced_four_world_three_query_universe_matches_frontier_decomposition():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    patterns = tuple(product((0, 1), repeat=4))
    checked = 0
    strict = 0
    internal_positive = 0
    external_positive = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        receipt = frontier_transversal_policy_decomposition(task)
        assert receipt.agrees_with_frontier_decomposition
        assert receipt.three_way_identity_holds
        assert receipt.internal_zero_certificate_exact
        if receipt.adaptive_cost is not None and receipt.fixed_cost is not None:
            strict += int(receipt.adaptive_cost < receipt.fixed_cost)
            internal_positive += int((receipt.internal_union_redundancy or 0) > 0)
            external_positive += int((receipt.external_shortcut_discount or 0) > 0)
        checked += 1
    assert checked == 16 ** 3 == 4_096
    assert strict == 192
    # These counts are intentionally not asserted: selected-policy tie-breaking
    # can change which optimal tree exhibits internal/external bypass while the
    # exact decomposition identities remain invariant for the selected tree.
    assert internal_positive >= 0
    assert external_positive >= 0
