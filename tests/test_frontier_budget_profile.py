from itertools import product

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.frontier_budget_profile import frontier_budget_profile_audit
from adaptive_gain.witnesses import mrod_routing_task, payoff_routing_task


def test_source_witness_profiles_and_fixed_bundles_are_recovered():
    for task in (mrod_routing_task(), payoff_routing_task()):
        audit = frontier_budget_profile_audit(task, 4)
        assert audit.exact_agrees
        assert (audit.adaptive_cost, audit.fixed_cost) == (2, 3)
        assert [row.adaptive_only for row in audit.profile] == [False, False, True, False, False]
        assert audit.frontier_optimal_fixed_bundles == audit.direct_optimal_fixed_bundles
        assert not audit.static_frontier_used_reachable_state_enumeration


def test_complete_balanced_four_world_three_query_universe_recovers_profiles_and_all_fixed_optima():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    patterns = tuple(product((0, 1), repeat=4))
    checked = strict = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        audit = frontier_budget_profile_audit(task, 3)
        assert audit.exact_agrees
        assert audit.profile_agrees
        assert audit.optimal_fixed_bundles_agree
        if audit.adaptive_cost is not None and audit.fixed_cost is not None:
            strict += int(audit.adaptive_cost < audit.fixed_cost)
        checked += 1
    assert checked == 16 ** 3 == 4_096
    assert strict == 192
