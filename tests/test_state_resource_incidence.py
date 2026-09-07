from itertools import product

from adaptive_gain.continuation_witnesses import continuation_fixed_cost_collision
from adaptive_gain.core import FiniteTask, Query, World, fixed_minimum_resolution
from adaptive_gain.resource_overlap import resource_role_profile_collision
from adaptive_gain.state_resource_incidence import (
    build_state_resource_incidence,
    bundle_resolves_from_state_resource_incidence,
    state_resource_fixed_minimum_resolution,
    state_resource_joint_cost_audit,
    verify_state_resource_incidence,
)


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


def test_registered_fixed_cost_collisions_are_resolved_by_state_resource_incidence():
    for tasks in (continuation_fixed_cost_collision(), resource_role_profile_collision()):
        direct = []
        derived = []
        for task in tasks:
            certificate = build_state_resource_incidence(task)
            assert verify_state_resource_incidence(task, certificate)
            direct.append(fixed_minimum_resolution(task).minimum_cost)
            derived.append(state_resource_fixed_minimum_resolution(certificate).minimum_cost)
        assert derived == direct
        assert direct[0] != direct[1]


def test_bundle_failure_criterion_matches_direct_fixed_solver_on_known_strict_task():
    strict, _ = continuation_fixed_cost_collision()
    certificate = build_state_resource_incidence(strict)
    assert not bundle_resolves_from_state_resource_incidence(certificate, ("left", "right"))
    assert not bundle_resolves_from_state_resource_incidence(certificate, ("left", "route"))
    assert not bundle_resolves_from_state_resource_incidence(certificate, ("right", "route"))
    assert bundle_resolves_from_state_resource_incidence(certificate, ("left", "right", "route"))


def test_all_four_world_three_query_set_partitions_preserve_joint_costs():
    partitions = _restricted_growth_partitions(4)
    assert len(partitions) == 15
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    checked = disagreements = reduced = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        receipt = state_resource_joint_cost_audit(task)
        disagreements += int(not receipt.exact_costs_agree)
        reduced += int(receipt.reduced_row_count < receipt.row_count)
        checked += 1
    assert checked == 15 ** 3 == 3_375
    assert disagreements == 0
    assert reduced > 0


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
            certificate = build_state_resource_incidence(task)
            assert state_resource_fixed_minimum_resolution(certificate).minimum_cost == fixed_minimum_resolution(task).minimum_cost
            checked += 1
    assert checked == 15 ** 2 * 2 ** 2 == 900


def test_tampered_incidence_certificate_is_rejected():
    strict, _ = continuation_fixed_cost_collision()
    certificate = build_state_resource_incidence(strict)
    row = certificate.rows[0]
    tampered = type(certificate)(
        certificate.query_names,
        certificate.query_costs,
        (type(row)(row.unavailable_queries, 0),) + certificate.rows[1:],
        certificate.reduced_rows,
    )
    assert not verify_state_resource_incidence(strict, tampered)
