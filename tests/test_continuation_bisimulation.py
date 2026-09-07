from dataclasses import replace
from itertools import product
from random import Random

import pytest

from adaptive_gain.core import (
    FiniteTask, Query, World, adaptive_minimum_resolution, fixed_minimum_resolution,
)
from adaptive_gain.continuation_bisimulation import (
    ContinuationAction, ContinuationClass, ContinuationQuotientLimitError,
    build_continuation_quotient, continuation_quotient_costs,
    lift_continuation_policy, verify_continuation_quotient,
)
from adaptive_gain.continuation_witnesses import (
    continuation_fixed_cost_collision, equal_value_different_continuations,
)


def _check_policy(task, receipt):
    if receipt.minimum_worst_path_cost is None:
        assert receipt.selected_policy is None
        return
    lookup = {q.name: q for q in task.queries}
    costs = []
    for i, world in enumerate(task.worlds):
        node = receipt.selected_policy
        paid = 0
        used = set()
        while node.query is not None:
            assert world.name in node.remaining_world_names
            assert node.query not in used
            used.add(node.query)
            query = lookup[node.query]
            paid += query.cost
            node = dict(node.branches)[query.outcomes[i]]
        assert world.name in node.remaining_world_names
        assert node.resolved_target == world.target
        costs.append(paid)
    assert max(costs) == receipt.minimum_worst_path_cost


def test_recursive_same_class_does_not_preserve_fixed_cost_or_gain():
    tasks = continuation_fixed_cost_collision()
    certificate = build_continuation_quotient(tasks)
    assert verify_continuation_quotient(tasks, certificate)
    assert certificate.root_classes[0] == certificate.root_classes[1]
    assert continuation_quotient_costs(tasks, certificate) == (2, 2)
    assert tuple(fixed_minimum_resolution(t).minimum_cost for t in tasks) == (3, 2)
    assert (certificate.mixed_state_count, certificate.mixed_class_count) == (16, 3)
    for i, task in enumerate(tasks):
        lifted = lift_continuation_policy(tasks, certificate, task_index=i)
        _check_policy(task, lifted)
        assert set(lifted.optimal_first_queries) == set(adaptive_minimum_resolution(task).optimal_first_queries)


def test_equivalent_local_continuations_can_have_incomparable_pair_masks():
    task = continuation_fixed_cost_collision()[0]
    # The two route children are resolved by different queries, not by the same
    # world subset or named measurement. Both are class 1 after recursive folding.
    cert = build_continuation_quotient((task,))
    members = {(x.world_mask, x.remaining_queries): x.class_id for x in cert.memberships}
    assert members[(0b1001, 0b011)] == members[(0b0110, 0b011)]
    masks = [sum(1 << k for k, (i, j) in enumerate(((0, 2), (0, 3), (1, 2), (1, 3)))
                 if query.outcomes[i] != query.outcomes[j]) for query in task.queries]
    assert all((a | b) != a and (a | b) != b for a, b in ((masks[0], masks[1]), (masks[0], masks[2]), (masks[1], masks[2])))


def test_equal_scalar_value_is_not_claimed_to_be_bisimulation():
    tasks = equal_value_different_continuations()
    cert = build_continuation_quotient(tasks)
    assert continuation_quotient_costs(tasks, cert) == (2, 2)
    assert cert.root_classes[0] != cert.root_classes[1]


def test_resolved_cost_marker_does_not_replace_reported_target():
    tasks = (FiniteTask((World("a", "red"),), ()), FiniteTask((World("b", None),), ()))
    cert = build_continuation_quotient(tasks)
    assert cert.root_classes == (0, 0)
    assert continuation_quotient_costs(tasks, cert) == (0, 0)
    assert lift_continuation_policy(tasks, cert, task_index=0).selected_policy.resolved_target == "red"
    assert lift_continuation_policy(tasks, cert, task_index=1).selected_policy.resolved_target is None


def test_dead_mixed_state_is_not_a_resolved_state():
    dead = FiniteTask((World("a", 0), World("b", 1)), ())
    cert = build_continuation_quotient((dead,))
    assert cert.root_classes != (0,)
    assert continuation_quotient_costs((dead,), cert) == (None,)
    assert lift_continuation_policy((dead,), cert).selected_policy is None


@pytest.mark.parametrize("cap", (0, -1, True, 1.5))
def test_invalid_caps(cap):
    with pytest.raises(ValueError):
        build_continuation_quotient(continuation_fixed_cost_collision(), max_states=cap)


def test_resource_cap_returns_no_partial_equivalence():
    with pytest.raises(ContinuationQuotientLimitError):
        build_continuation_quotient(continuation_fixed_cost_collision(), max_states=1)


def test_builder_and_verifier_do_not_call_an_optimum_oracle(monkeypatch):
    import adaptive_gain.core as core
    import adaptive_gain.continuation_bisimulation as module
    def forbidden(*args, **kwargs):
        raise AssertionError("oracle/constructor partition unexpectedly used")
    monkeypatch.setattr(core, "adaptive_minimum_resolution", forbidden)
    monkeypatch.setattr(core, "fixed_minimum_resolution", forbidden)
    tasks = continuation_fixed_cost_collision()
    cert = module.build_continuation_quotient(tasks)
    monkeypatch.setattr(module, "_cells", forbidden)
    assert module.verify_continuation_quotient(tasks, cert)
    assert module.continuation_quotient_costs(tasks, cert) == (2, 2)


@pytest.mark.parametrize("change", ("incomplete", "missing_state", "fake_terminal", "missing_action", "cycle", "cost", "duplicate", "bool_root"))
def test_certificate_tampering_is_rejected(change):
    tasks = continuation_fixed_cost_collision()
    cert = build_continuation_quotient(tasks)
    root_id = cert.root_classes[0]
    classes = list(cert.classes)
    if change == "incomplete":
        bad = replace(cert, complete=False)
    elif change == "missing_state":
        bad = replace(cert, memberships=cert.memberships[1:])
    elif change == "duplicate":
        bad = replace(cert, memberships=cert.memberships + (cert.memberships[0],))
    elif change == "bool_root":
        bad = replace(cert, root_classes=(True, cert.root_classes[1]))
    else:
        root = classes[root_id]
        if change == "fake_terminal":
            classes[root_id] = replace(root, resolved=True)
        elif change == "missing_action":
            classes[root_id] = replace(root, actions=root.actions[:1])
        elif change == "cycle":
            classes[root_id] = replace(root, actions=(ContinuationAction(1, (root_id,)),))
        else:
            classes[root_id] = replace(root, actions=(ContinuationAction(2, (1,)),))
        bad = replace(cert, classes=tuple(classes))
    assert not verify_continuation_quotient(tasks, bad)
    with pytest.raises(ValueError):
        continuation_quotient_costs(tasks, bad)


def test_cost_recalibration_requires_reverification():
    tasks = continuation_fixed_cost_collision()
    cert = build_continuation_quotient(tasks)
    changed = replace(tasks[0], queries=(replace(tasks[0].queries[0], cost=5),) + tasks[0].queries[1:])
    assert not verify_continuation_quotient((changed, tasks[1]), cert)


def test_complete_4096_binary_universe_matches_direct_solver():
    worlds = tuple(World(f"w{i}", i // 2) for i in range(4))
    patterns = tuple(product((0, 1), repeat=4))
    tasks = tuple(FiniteTask(worlds, tuple(Query(f"q{j}", 1, col) for j, col in enumerate(cols)))
                  for cols in product(patterns, repeat=3))
    cert = build_continuation_quotient(tasks)
    assert verify_continuation_quotient(tasks, cert)
    assert (cert.mixed_state_count, cert.mixed_class_count) == (20992, 12)
    assert continuation_quotient_costs(tasks, cert) == tuple(
        adaptive_minimum_resolution(task).minimum_worst_path_cost for task in tasks)


def test_seeded_weighted_multitarget_multiway_relabelled_tasks():
    rng = Random(20260907)
    for _ in range(250):
        n, m = rng.randint(2, 6), rng.randint(0, 5)
        worlds = tuple(World(f"w{i}", rng.randrange(3)) for i in range(n))
        task = FiniteTask(worlds, tuple(Query(f"q{j}", rng.randint(1, 5), tuple(rng.randrange(3) for _ in range(n))) for j in range(m)))
        order = list(range(n)); rng.shuffle(order)
        qorder = list(range(m)); rng.shuffle(qorder)
        renamed = FiniteTask(tuple(World(f"renamed_{i}", worlds[old].target) for i, old in enumerate(order)),
            tuple(Query(f"sensor_{j}", task.queries[old].cost,
                tuple(f"label_{task.queries[old].outcomes[i]}" for i in order)) for j, old in enumerate(qorder)))
        cert = build_continuation_quotient((task, renamed))
        assert cert.root_classes[0] == cert.root_classes[1]
        expected = adaptive_minimum_resolution(task).minimum_worst_path_cost
        assert continuation_quotient_costs((task, renamed), cert) == (expected, expected)
        for i, candidate in enumerate((task, renamed)):
            _check_policy(candidate, lift_continuation_policy((task, renamed), cert, task_index=i))


def _partitions(n):
    def extend(prefix):
        if len(prefix) == n:
            yield prefix
        else:
            for value in range(max(prefix, default=-1) + 2):
                yield from extend(prefix + (value,))
    return tuple(extend(()))


@pytest.mark.parametrize("targets,patterns,states,classes", (
    ((0, 0, 1, 1, 1), tuple(product((0, 1), repeat=5)), 238880, 43),
    ((0, 0, 1, 1), _partitions(4), 13275, 16),
    ((0, 0, 1, 2), _partitions(4), 15075, 17),
))
def test_five_world_and_multiway_complete_universes(targets, patterns, states, classes):
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    tasks = tuple(FiniteTask(worlds, tuple(Query(f"q{j}", 1, col) for j, col in enumerate(cols)))
                  for cols in product(patterns, repeat=3))
    cert = build_continuation_quotient(tasks, max_states=1_000_000)
    assert (cert.mixed_state_count, cert.mixed_class_count) == (states, classes)
    assert continuation_quotient_costs(tasks, cert) == tuple(
        adaptive_minimum_resolution(task).minimum_worst_path_cost for task in tasks)


def test_fixed_comparator_boundary_has_direct_pair_certificates():
    strict, bypass = continuation_fixed_cost_collision()
    pairs = ((0, 3), (1, 2), (0, 2))
    # One private cross-target pair for each of the three strict-task queries.
    for q, (i, j) in enumerate(pairs):
        separators = [r for r, query in enumerate(strict.queries) if query.outcomes[i] != query.outcomes[j]]
        assert separators == [q]
    # The second task instead has a two-query resolving bundle.
    for i in (0, 1):
        for j in (2, 3):
            assert any(bypass.queries[q].outcomes[i] != bypass.queries[q].outcomes[j] for q in (1, 2))
