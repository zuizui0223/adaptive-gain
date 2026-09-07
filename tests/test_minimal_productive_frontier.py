from dataclasses import replace
from itertools import product

from adaptive_gain.core import FiniteTask, Query, World
from adaptive_gain.minimal_productive_frontier import (
    build_minimal_productive_frontier_from_pair_incidence,
    minimal_frontier_fixed_minimum_resolution,
    static_minimal_frontier_fixed_cost_audit,
    verify_minimal_productive_frontier_from_pair_incidence,
)
from adaptive_gain.productive_frontier import build_productive_frontier


def _balanced_four_world_tasks(query_count=3):
    worlds = tuple(World(f"w{i}", 0 if i < 2 else 1) for i in range(4))
    patterns = tuple(product((0, 1), repeat=4))
    for maps in product(patterns, repeat=query_count):
        yield FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, tuple(outcomes)) for j, outcomes in enumerate(maps)),
        )


def test_static_minimal_frontier_equals_state_based_frontier_on_all_4096_tasks():
    count = 0
    for task in _balanced_four_world_tasks(3):
        static = build_minimal_productive_frontier_from_pair_incidence(task)
        dynamic = build_productive_frontier(task)
        assert static.minimal_productive_sets == dynamic.minimal_productive_sets
        assert minimal_frontier_fixed_minimum_resolution(static).minimum_cost == static_minimal_frontier_fixed_cost_audit(task).fixed_cost
        count += 1
    assert count == 4096


def test_static_builder_handles_already_resolved_and_unresolved_tasks():
    resolved = FiniteTask(
        (World("a", 0), World("b", 0)),
        (Query("q", 1, (0, 1)),),
    )
    cert = build_minimal_productive_frontier_from_pair_incidence(resolved)
    assert cert.minimal_productive_sets == ()
    assert minimal_frontier_fixed_minimum_resolution(cert).minimum_cost == 0

    unresolved = FiniteTask(
        (World("a", 0), World("b", 1)),
        (Query("q", 1, (0, 0)),),
    )
    cert = build_minimal_productive_frontier_from_pair_incidence(unresolved)
    assert cert.minimal_productive_sets == (0,)
    assert minimal_frontier_fixed_minimum_resolution(cert).minimum_cost is None


def test_static_frontier_verifier_rejects_tampering():
    task = next(_balanced_four_world_tasks(3))
    cert = build_minimal_productive_frontier_from_pair_incidence(task)
    assert verify_minimal_productive_frontier_from_pair_incidence(task, cert)
    bad = replace(cert, query_costs=tuple(cost + 1 for cost in cert.query_costs))
    assert not verify_minimal_productive_frontier_from_pair_incidence(task, bad)


def test_static_audit_explicitly_reports_no_reachable_state_enumeration():
    task = next(_balanced_four_world_tasks(3))
    receipt = static_minimal_frontier_fixed_cost_audit(task)
    assert receipt.exact_cost_agrees
    assert receipt.reachable_state_enumeration_used is False
