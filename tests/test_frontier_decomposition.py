from itertools import product

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.frontier_decomposition import productive_frontier_policy_decomposition
from adaptive_gain.witnesses import (
    partial_external_bypass_gain_control,
    partial_internal_bypass_gain_control,
    routing_bypass_control,
)


def test_frontier_decomposition_separates_internal_and_external_bypass_controls():
    internal = productive_frontier_policy_decomposition(partial_internal_bypass_gain_control())
    assert internal.agrees_with_direct_decomposition
    assert (internal.adaptive_cost, internal.fixed_cost) == (3, 4)
    assert internal.realized_adaptive_gain == 1
    assert internal.internal_union_redundancy == 1
    assert internal.external_shortcut_discount == 0
    assert internal.three_way_identity_holds

    external = productive_frontier_policy_decomposition(partial_external_bypass_gain_control())
    assert external.agrees_with_direct_decomposition
    assert (external.adaptive_cost, external.fixed_cost) == (3, 4)
    assert external.realized_adaptive_gain == 1
    assert external.internal_union_redundancy == 0
    assert external.external_shortcut_discount == 1
    assert external.three_way_identity_holds

    bypass = productive_frontier_policy_decomposition(routing_bypass_control())
    assert bypass.agrees_with_direct_decomposition
    assert (bypass.adaptive_cost, bypass.fixed_cost) == (2, 2)
    assert bypass.realized_adaptive_gain == 0
    assert bypass.internal_union_redundancy == 1
    assert bypass.external_shortcut_discount == 0


def test_complete_minimal_binary_universe_matches_direct_decomposition():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    patterns = tuple(product((0, 1), repeat=4))
    checked = unresolved = strict = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        receipt = productive_frontier_policy_decomposition(task)
        assert receipt.agrees_with_direct_decomposition
        assert receipt.three_way_identity_holds
        if receipt.adaptive_cost is None:
            unresolved += 1
        elif receipt.fixed_cost is not None and receipt.adaptive_cost < receipt.fixed_cost:
            strict += 1
        checked += 1
    assert checked == 16 ** 3 == 4_096
    assert unresolved == 1_688
    assert strict == 192
