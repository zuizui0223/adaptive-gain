"""Reusable sufficient certificates for routing gain and local no-routing."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from typing import Hashable, Mapping

from .core import FiniteTask, _indices, _partition, _target_values, fixed_minimum_resolution

@dataclass(frozen=True)
class RoutingBranch:
    outcome: Hashable
    minimum_continuation_cost: int | None
    selected_next_query: str | None
    remaining_world_names: tuple[str, ...]

@dataclass(frozen=True)
class RoutingCertificate:
    root_query: str
    budget: int
    root_cost: int
    branches: tuple[RoutingBranch, ...]
    every_branch_resolvable: bool
    branch_dependent_next_action: bool
    no_fixed_resolution_within_budget: bool
    strict_adaptive_only_resolution_certified: bool

@dataclass(frozen=True)
class BranchInvariantCertificate:
    outcomes: tuple[Hashable, ...]
    signatures: tuple[Hashable, ...]
    branch_invariant: bool
    interpretation: str

def routing_certificate(task: FiniteTask, root_query: str, budget: int) -> RoutingCertificate:
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    lookup = {q.name: i for i, q in enumerate(task.queries)}
    if root_query not in lookup:
        raise ValueError("unknown root query")
    root_index = lookup[root_query]
    root = task.queries[root_index]
    n_worlds, n_queries = len(task.worlds), len(task.queries)
    root_mask = (1 << n_worlds) - 1
    remaining_after_root = ((1 << n_queries) - 1) ^ (1 << root_index)

    @lru_cache(None)
    def search(mask: int, remaining: int):
        targets = _target_values(task, mask)
        if len(targets) == 1:
            return 0, None
        best = None
        best_query = None
        for q_index, q in enumerate(task.queries):
            bit = 1 << q_index
            if not remaining & bit:
                continue
            groups = _partition(task, mask, q_index)
            if len(groups) <= 1:
                continue
            child_costs = []
            ok = True
            for child_mask in groups.values():
                cost, _ = search(child_mask, remaining ^ bit)
                if cost is None:
                    ok = False
                    break
                child_costs.append(cost)
            if not ok:
                continue
            cost = q.cost + max(child_costs)
            if best is None or cost < best:
                best, best_query = cost, q.name
        return best, best_query

    branches = []
    for outcome, mask in sorted(_partition(task, root_mask, root_index).items(), key=lambda item: repr(item[0])):
        cost, next_query = search(mask, remaining_after_root)
        branches.append(RoutingBranch(
            outcome,
            cost,
            next_query,
            tuple(task.worlds[i].name for i in _indices(mask, n_worlds)),
        ))
    every = root.cost <= budget and all(
        branch.minimum_continuation_cost is not None
        and root.cost + branch.minimum_continuation_cost <= budget
        for branch in branches
    )
    branch_dependent = len({branch.selected_next_query for branch in branches}) > 1
    fixed = fixed_minimum_resolution(task)
    no_fixed = fixed.minimum_cost is None or fixed.minimum_cost > budget
    return RoutingCertificate(
        root_query, budget, root.cost, tuple(branches), every, branch_dependent,
        no_fixed, every and no_fixed,
    )

def branch_invariant_no_routing_certificate(
    branch_signatures: Mapping[Hashable, Hashable],
) -> BranchInvariantCertificate:
    if not branch_signatures:
        raise ValueError("at least one branch signature is required")
    outcomes = tuple(branch_signatures)
    signatures = tuple(branch_signatures[o] for o in outcomes)
    invariant = len(set(signatures)) == 1
    return BranchInvariantCertificate(
        outcomes, signatures, invariant,
        (
            "branch-invariant declared sufficient state: no extra routing value at this step"
            if invariant
            else "branch-dependent declared future state: routing gain is possible but not guaranteed"
        ),
    )
