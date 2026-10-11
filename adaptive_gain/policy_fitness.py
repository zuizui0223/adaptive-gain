"""Distribution-sensitive fitness optimization over finite adaptive policies."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import math
from typing import Hashable, Sequence

from .core import AdaptiveNode, FiniteTask, _indices, _partition, _target_values


@dataclass(frozen=True)
class DiscountedPolicyReceipt:
    discount_rate: float
    expected_discounted_completion_value: float
    selected_policy: AdaptiveNode | None
    world_path_costs: tuple[float, ...] | None
    worst_path_cost: float | None
    mean_path_cost: float | None


def policy_world_path_costs(
    task: FiniteTask,
    policy: AdaptiveNode,
) -> tuple[float, ...]:
    """Return realized query cost for each declared world under one policy."""
    query_cost = {q.name: q.cost for q in task.queries}
    query_lookup = {q.name: i for i, q in enumerate(task.queries)}
    costs: dict[str, float] = {}

    def walk(node: AdaptiveNode, accrued: float) -> None:
        if node.query is None:
            for world_name in node.remaining_world_names:
                costs[world_name] = accrued
            return

        if node.query not in query_lookup:
            raise ValueError(f"policy uses unknown query {node.query!r}")
        new_cost = accrued + query_cost[node.query]
        for _, child in node.branches:
            walk(child, new_cost)

    walk(policy, 0.0)

    if set(costs) != {w.name for w in task.worlds}:
        raise ValueError("policy did not assign a completion cost to every world")
    return tuple(costs[w.name] for w in task.worlds)


def discounted_fitness_optimal_policy(
    task: FiniteTask,
    world_probabilities: Sequence[float],
    *,
    discount_rate: float,
) -> DiscountedPolicyReceipt:
    """Optimize E[exp(-mu*T)] over guaranteed-resolving adaptive policies.

    This objective is a minimal model for a monotonically declining ecological
    value of decision time. It deliberately differs from the core minimax
    objective used to define C_A.
    """
    n_worlds = len(task.worlds)
    n_queries = len(task.queries)

    probs = tuple(float(p) for p in world_probabilities)
    if len(probs) != n_worlds:
        raise ValueError("one probability is required for each world")
    if any((not math.isfinite(p) or p < 0) for p in probs):
        raise ValueError("world probabilities must be finite and nonnegative")
    if not math.isclose(sum(probs), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("world probabilities must sum to one")
    if not math.isfinite(discount_rate) or discount_rate <= 0:
        raise ValueError("discount_rate must be finite and positive")

    root_mask = (1 << n_worlds) - 1

    @lru_cache(None)
    def search(mask: int, remaining: int):
        targets = _target_values(task, mask)
        support = tuple(
            task.worlds[i].name
            for i in _indices(mask, n_worlds)
        )
        if len(targets) == 1:
            weight = sum(
                probs[i]
                for i in _indices(mask, n_worlds)
            )
            return (
                weight,
                AdaptiveNode(
                    None,
                    (),
                    support,
                    next(iter(targets)),
                ),
            )

        best_value = None
        best_node = None

        for q_index, q in enumerate(task.queries):
            bit = 1 << q_index
            if not (remaining & bit):
                continue
            groups = _partition(task, mask, q_index)
            if len(groups) <= 1:
                continue

            children = []
            total_child_value = 0.0
            feasible = True
            for outcome, child_mask in sorted(
                groups.items(),
                key=lambda item: repr(item[0]),
            ):
                child_value, child_node = search(
                    child_mask,
                    remaining ^ bit,
                )
                if child_node is None:
                    feasible = False
                    break
                total_child_value += child_value
                children.append((outcome, child_node))

            if not feasible:
                continue

            value = math.exp(-discount_rate * q.cost) * total_child_value
            if best_value is None or value > best_value + 1e-15:
                best_value = value
                best_node = AdaptiveNode(
                    q.name,
                    tuple(children),
                    support,
                    None,
                )

        if best_value is None:
            return 0.0, None
        return best_value, best_node

    value, policy = search(root_mask, (1 << n_queries) - 1)
    if policy is None:
        return DiscountedPolicyReceipt(
            discount_rate,
            0.0,
            None,
            None,
            None,
            None,
        )

    path_costs = policy_world_path_costs(task, policy)
    mean_cost = sum(p * c for p, c in zip(probs, path_costs))
    return DiscountedPolicyReceipt(
        discount_rate,
        value,
        policy,
        path_costs,
        max(path_costs),
        mean_cost,
    )
