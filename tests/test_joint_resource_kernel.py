from itertools import product

from adaptive_gain.continuation_witnesses import continuation_fixed_cost_collision
from adaptive_gain.core import FiniteTask, Query, World, adaptive_gain_receipt
from adaptive_gain.joint_resource_kernel import joint_resource_kernel


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


def test_global_query_refinement_preserves_both_costs():
    worlds = (
        World("a0", 0), World("a1", 0),
        World("b0", 1), World("b1", 1),
    )
    task = FiniteTask(
        worlds,
        (
            Query("fine", 1, (0, 1, 0, 2)),
            Query("coarse", 2, (0, 0, 0, 1)),
            Query("finish", 1, (0, 0, 1, 0)),
        ),
    )
    receipt = joint_resource_kernel(task)
    assert receipt.exact_costs_agree
    assert "coarse" in receipt.removed_query_names
    assert (receipt.original_adaptive_cost, receipt.original_fixed_cost) == (
        receipt.reduced_adaptive_cost, receipt.reduced_fixed_cost
    )


def test_query_reduction_can_create_new_world_twins_on_next_iteration():
    task = FiniteTask(
        (World("a0", 0), World("a1", 0), World("b", 1)),
        (
            # noise distinguishes the two target-0 worlds relative to b.
            Query("noise", 2, (0, 1, 1)),
            # direct separates both target-0 worlds from b and dominates noise.
            Query("direct", 1, (0, 0, 1)),
        ),
    )
    receipt = joint_resource_kernel(task)
    assert receipt.exact_costs_agree
    assert "noise" in receipt.removed_query_names
    assert len(set(receipt.removed_world_names) & {"a0", "a1"}) == 1
    assert len(receipt.reduced_task.worlds) == 2
    assert len(receipt.reduced_task.queries) == 1
    assert (receipt.original_adaptive_cost, receipt.original_fixed_cost) == (1, 1)
    assert receipt.iterations >= 2


def test_previous_strict_and_bypass_controls_keep_their_distinct_gain_status():
    strict, bypass = continuation_fixed_cost_collision()
    strict_kernel = joint_resource_kernel(strict)
    bypass_kernel = joint_resource_kernel(bypass)
    assert strict_kernel.exact_costs_agree
    assert bypass_kernel.exact_costs_agree
    assert adaptive_gain_receipt(strict_kernel.reduced_task).strict_adaptive_gain
    assert not adaptive_gain_receipt(bypass_kernel.reduced_task).strict_adaptive_gain
    assert (strict_kernel.reduced_adaptive_cost, strict_kernel.reduced_fixed_cost) == (2, 3)
    assert (bypass_kernel.reduced_adaptive_cost, bypass_kernel.reduced_fixed_cost) == (2, 2)


def test_complete_four_world_arbitrary_partition_universe_preserves_both_costs():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    partitions = _set_partitions(4)
    checked = reduced = strict = 0
    for maps in product(partitions, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        receipt = joint_resource_kernel(task)
        assert receipt.exact_costs_agree
        direct = adaptive_gain_receipt(task)
        reduced_receipt = adaptive_gain_receipt(receipt.reduced_task)
        assert reduced_receipt.adaptive_cost == direct.adaptive_cost
        assert reduced_receipt.fixed_cost == direct.fixed_cost
        assert reduced_receipt.strict_adaptive_gain == direct.strict_adaptive_gain
        reduced += int(bool(receipt.removed_world_names or receipt.removed_query_names))
        strict += int(direct.strict_adaptive_gain)
        checked += 1
    assert checked == 15 ** 3 == 3_375
    assert strict == 24
    assert reduced > 0
