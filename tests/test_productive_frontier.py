from itertools import product

from adaptive_gain.continuation_witnesses import continuation_fixed_cost_collision
from adaptive_gain.core import FiniteTask, Query, World, fixed_minimum_resolution
from adaptive_gain.productive_frontier import (
    build_productive_frontier,
    bundle_resolves_from_productive_frontier,
    productive_frontier_fixed_minimum_resolution,
    productive_frontier_joint_cost_audit,
    productive_frontier_sperner_bound,
    verify_productive_frontier,
)
from adaptive_gain.resource_overlap import resource_role_profile_collision


def _restricted_growth_partitions(n: int):
    rows = []
    def rec(prefix, maximum):
        if len(prefix) == n:
            rows.append(tuple(prefix))
            return
        for value in range(maximum + 2):
            rec(prefix + (value,), max(maximum, value))
    rec((0,), 0)
    return tuple(rows)


def test_registered_fixed_cost_collisions_are_separated_by_productive_frontier():
    for tasks in (continuation_fixed_cost_collision(), resource_role_profile_collision()):
        direct = []
        derived = []
        for task in tasks:
            certificate = build_productive_frontier(task)
            assert verify_productive_frontier(task, certificate)
            direct.append(fixed_minimum_resolution(task).minimum_cost)
            derived.append(productive_frontier_fixed_minimum_resolution(certificate).minimum_cost)
        assert derived == direct
        assert direct[0] != direct[1]


def test_strict_collision_requires_hitting_every_productive_edge():
    strict, _ = continuation_fixed_cost_collision()
    certificate = build_productive_frontier(strict)
    assert set(certificate.minimal_productive_sets) == {1, 2, 4}
    assert not bundle_resolves_from_productive_frontier(certificate, ("left", "right"))
    assert not bundle_resolves_from_productive_frontier(certificate, ("left", "route"))
    assert not bundle_resolves_from_productive_frontier(certificate, ("right", "route"))
    assert bundle_resolves_from_productive_frontier(certificate, ("left", "right", "route"))


def test_all_four_world_three_query_partitions_preserve_joint_costs_and_sperner_bound():
    partitions = _restricted_growth_partitions(4)
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    checked = disagreements = max_frontier = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        receipt = productive_frontier_joint_cost_audit(task)
        disagreements += int(not receipt.exact_costs_agree)
        assert receipt.bound_holds
        max_frontier = max(max_frontier, receipt.minimal_productive_set_count)
        checked += 1
    assert checked == 15 ** 3 == 3_375
    assert disagreements == 0
    assert max_frontier == productive_frontier_sperner_bound(3) == 3


def test_unequal_cost_grid_preserves_fixed_cost():
    partitions = _restricted_growth_partitions(4)
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    checked = 0
    for maps in product(partitions, repeat=2):
        for costs in product((1, 2), repeat=2):
            task = FiniteTask(
                worlds,
                tuple(Query(f"q{i}", costs[i], maps[i]) for i in range(2)),
            )
            certificate = build_productive_frontier(task)
            assert productive_frontier_fixed_minimum_resolution(certificate).minimum_cost == fixed_minimum_resolution(task).minimum_cost
            checked += 1
    assert checked == 15 ** 2 * 2 ** 2 == 900


def test_sperner_bounds_small_query_counts():
    assert [productive_frontier_sperner_bound(q) for q in range(7)] == [1, 1, 2, 3, 6, 10, 20]
