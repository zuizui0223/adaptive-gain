from itertools import product

from adaptive_gain.continuation_bisimulation import build_continuation_quotient
from adaptive_gain.continuation_witnesses import continuation_fixed_cost_collision
from adaptive_gain.core import FiniteTask, Query, World, adaptive_gain_receipt
from adaptive_gain.resource_continuation import (
    ResourceContinuationAction,
    ResourceContinuationCertificate,
    ResourceContinuationClass,
    build_resource_continuation_quotient,
    resource_continuation_cost_audit,
    verify_resource_continuation_quotient,
)


def _balanced_worlds():
    return (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )


def _set_partitions(n):
    rows = []

    def rec(prefix, next_label):
        if len(prefix) == n:
            rows.append(tuple(prefix))
            return
        for label in range(next_label + 1):
            prefix.append(label)
            rec(prefix, max(next_label, label + 1))
            prefix.pop()

    rec([0], 1)
    return tuple(rows)


def test_resource_identity_closes_the_previous_fixed_cost_collision():
    strict, bypass = continuation_fixed_cost_collision()

    # The cost-only quotient intentionally merges the two roots.
    cost_only = build_continuation_quotient((strict, bypass))
    assert cost_only.root_classes[0] == cost_only.root_classes[1]

    strict_certificate = build_resource_continuation_quotient(strict)
    bypass_certificate = build_resource_continuation_quotient(bypass)
    assert verify_resource_continuation_quotient(strict, strict_certificate)
    assert verify_resource_continuation_quotient(bypass, bypass_certificate)

    strict_audit = resource_continuation_cost_audit(strict, strict_certificate)
    bypass_audit = resource_continuation_cost_audit(bypass, bypass_certificate)
    assert (strict_audit.adaptive_cost, strict_audit.fixed_cost) == (2, 3)
    assert (bypass_audit.adaptive_cost, bypass_audit.fixed_cost) == (2, 2)
    assert strict_audit.strict_adaptive_gain
    assert not bypass_audit.strict_adaptive_gain
    assert strict_audit.exact_costs_agree
    assert bypass_audit.exact_costs_agree


def test_resource_certificate_rejects_query_token_or_cost_tampering():
    task = continuation_fixed_cost_collision()[0]
    certificate = build_resource_continuation_quotient(task)
    assert verify_resource_continuation_quotient(task, certificate)

    classes = list(certificate.classes)
    target_index = next(i for i, cls in enumerate(classes) if cls.actions)
    cls = classes[target_index]
    action = cls.actions[0]

    wrong_cost = ResourceContinuationAction(
        action.query_index, action.cost + 1, action.child_classes
    )
    classes[target_index] = ResourceContinuationClass(
        cls.class_id, cls.resolved, (wrong_cost,) + cls.actions[1:]
    )
    tampered = ResourceContinuationCertificate(
        certificate.query_names,
        certificate.query_costs,
        certificate.root_class,
        tuple(classes),
        certificate.memberships,
    )
    assert not verify_resource_continuation_quotient(task, tampered)

    classes = list(certificate.classes)
    cls = classes[target_index]
    action = cls.actions[0]
    wrong_query = ResourceContinuationAction(
        (action.query_index + 1) % len(task.queries),
        action.cost,
        action.child_classes,
    )
    altered_actions = tuple(sorted((wrong_query,) + cls.actions[1:], key=lambda row: row.query_index))
    classes[target_index] = ResourceContinuationClass(cls.class_id, cls.resolved, altered_actions)
    tampered = ResourceContinuationCertificate(
        certificate.query_names,
        certificate.query_costs,
        certificate.root_class,
        tuple(classes),
        certificate.memberships,
    )
    assert not verify_resource_continuation_quotient(task, tampered)


def test_complete_balanced_four_world_binary_universe_preserves_joint_costs():
    worlds = _balanced_worlds()
    patterns = tuple(product((0, 1), repeat=4))
    checked = strict = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        certificate = build_resource_continuation_quotient(task)
        assert verify_resource_continuation_quotient(task, certificate)
        audit = resource_continuation_cost_audit(task, certificate)
        direct = adaptive_gain_receipt(task)
        assert audit.adaptive_cost == direct.adaptive_cost
        assert audit.fixed_cost == direct.fixed_cost
        assert audit.strict_adaptive_gain == direct.strict_adaptive_gain
        assert audit.exact_costs_agree
        strict += int(audit.strict_adaptive_gain)
        checked += 1
    assert checked == 16 ** 3 == 4_096
    assert strict == 192


def test_complete_four_world_arbitrary_partition_universe_preserves_joint_costs():
    worlds = _balanced_worlds()
    partitions = _set_partitions(4)
    assert len(partitions) == 15
    checked = strict = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        certificate = build_resource_continuation_quotient(task)
        audit = resource_continuation_cost_audit(task, certificate)
        direct = adaptive_gain_receipt(task)
        assert audit.adaptive_cost == direct.adaptive_cost
        assert audit.fixed_cost == direct.fixed_cost
        assert audit.strict_adaptive_gain == direct.strict_adaptive_gain
        assert audit.exact_costs_agree
        strict += int(audit.strict_adaptive_gain)
        checked += 1
    assert checked == 15 ** 3 == 3_375
    assert strict == 24
