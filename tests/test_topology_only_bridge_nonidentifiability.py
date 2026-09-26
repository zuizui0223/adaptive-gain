from __future__ import annotations

from collections import Counter

from adaptive_gain import adaptive_gain_receipt
from adaptive_gain.witnesses import payoff_routing_task, routing_bypass_control


def _coarse_task_signature(task):
    target_counts = tuple(sorted(Counter(world.target for world in task.worlds).values()))
    query_costs = tuple(sorted(query.cost for query in task.queries))
    query_arities = tuple(sorted(len(set(query.outcomes)) for query in task.queries))
    return (
        len(task.worlds),
        len(task.queries),
        target_counts,
        query_costs,
        query_arities,
    )


def test_same_coarse_finite_task_signature_can_have_different_structural_gap() -> None:
    strict = payoff_routing_task()
    no_gain = routing_bypass_control()

    assert _coarse_task_signature(strict) == _coarse_task_signature(no_gain) == (
        4,
        3,
        (2, 2),
        (1, 1, 1),
        (2, 2, 2),
    )

    strict_receipt = adaptive_gain_receipt(strict)
    no_gain_receipt = adaptive_gain_receipt(no_gain)

    assert (strict_receipt.adaptive_cost, strict_receipt.fixed_cost) == (2, 3)
    assert (no_gain_receipt.adaptive_cost, no_gain_receipt.fixed_cost) == (2, 2)

    strict_gap = strict_receipt.fixed_cost - strict_receipt.adaptive_cost
    no_gain_gap = no_gain_receipt.fixed_cost - no_gain_receipt.adaptive_cost
    assert strict_gap == 1
    assert no_gain_gap == 0
    assert strict_gap != no_gain_gap
