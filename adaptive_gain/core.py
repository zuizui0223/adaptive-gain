"""Exact finite deterministic adaptive-vs-fixed target-resolution theory."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from typing import Hashable, Sequence

@dataclass(frozen=True)
class World:
    name: str
    target: Hashable

@dataclass(frozen=True)
class Query:
    name: str
    cost: int
    outcomes: tuple[Hashable, ...]

@dataclass(frozen=True)
class FiniteTask:
    worlds: tuple[World, ...]
    queries: tuple[Query, ...]
    def __post_init__(self) -> None:
        if not self.worlds:
            raise ValueError("task requires at least one world")
        if len({w.name for w in self.worlds}) != len(self.worlds):
            raise ValueError("world names must be unique")
        if any(not isinstance(w.name, str) or not w.name.strip() for w in self.worlds):
            raise ValueError("world names must be non-empty strings")
        if len({q.name for q in self.queries}) != len(self.queries):
            raise ValueError("query names must be unique")
        for q in self.queries:
            if not isinstance(q.name, str) or not q.name.strip():
                raise ValueError("query names must be non-empty strings")
            if type(q.cost) is not int or q.cost <= 0:
                raise ValueError("query costs must be positive integers")
            if len(q.outcomes) != len(self.worlds):
                raise ValueError("each query needs one outcome per world")
        if len(self.queries) > 20:
            raise ValueError("exact finite solver permits at most 20 queries")

@dataclass(frozen=True)
class FixedResolutionReceipt:
    minimum_cost: int | None
    optimal_bundles: tuple[tuple[str, ...], ...]
    target_already_identified: bool

@dataclass(frozen=True)
class AdaptiveNode:
    query: str | None
    branches: tuple[tuple[Hashable, "AdaptiveNode"], ...]
    remaining_world_names: tuple[str, ...]
    resolved_target: Hashable | None

@dataclass(frozen=True)
class AdaptiveResolutionReceipt:
    minimum_worst_path_cost: int | None
    selected_policy: AdaptiveNode | None
    optimal_first_queries: tuple[str, ...]
    target_already_identified: bool
    search_states: int

@dataclass(frozen=True)
class AdaptiveGainReceipt:
    adaptive_cost: int | None
    fixed_cost: int | None
    strict_adaptive_gain: bool
    adaptive_only_budget_lower: int | None
    adaptive_only_budget_upper: int | None
    status: str

def _indices(mask: int, n: int) -> tuple[int, ...]:
    return tuple(i for i in range(n) if mask & (1 << i))

def _target_values(task: FiniteTask, mask: int) -> set[Hashable]:
    return {task.worlds[i].target for i in _indices(mask, len(task.worlds))}

def _partition(task: FiniteTask, mask: int, query_index: int) -> dict[Hashable, int]:
    groups: dict[Hashable, int] = {}
    q = task.queries[query_index]
    for i in _indices(mask, len(task.worlds)):
        outcome = q.outcomes[i]
        groups[outcome] = groups.get(outcome, 0) | (1 << i)
    return groups

def bundle_resolves(task: FiniteTask, bundle: Sequence[str]) -> bool:
    names = tuple(bundle)
    lookup = {q.name: j for j, q in enumerate(task.queries)}
    if len(set(names)) != len(names) or any(name not in lookup for name in names):
        raise ValueError("bundle must contain unique declared query names")
    chosen = tuple(lookup[name] for name in names)
    for i, j in combinations(range(len(task.worlds)), 2):
        if task.worlds[i].target == task.worlds[j].target:
            continue
        if not any(task.queries[q].outcomes[i] != task.queries[q].outcomes[j] for q in chosen):
            return False
    return True

def fixed_minimum_resolution(task: FiniteTask) -> FixedResolutionReceipt:
    root_targets = {w.target for w in task.worlds}
    if len(root_targets) == 1:
        return FixedResolutionReceipt(0, ((),), True)
    n = len(task.queries)
    best: int | None = None
    bundles: list[tuple[str, ...]] = []
    for subset in range(1 << n):
        cost = sum(task.queries[j].cost for j in range(n) if subset & (1 << j))
        if best is not None and cost > best:
            continue
        names = tuple(task.queries[j].name for j in range(n) if subset & (1 << j))
        if bundle_resolves(task, names):
            if best is None or cost < best:
                best, bundles = cost, [names]
            elif cost == best:
                bundles.append(names)
    return FixedResolutionReceipt(best, tuple(bundles), False)

def adaptive_minimum_resolution(task: FiniteTask) -> AdaptiveResolutionReceipt:
    n_worlds, n_queries = len(task.worlds), len(task.queries)
    root_mask = (1 << n_worlds) - 1
    states = 0
    @lru_cache(None)
    def search(mask: int, remaining: int):
        nonlocal states
        states += 1
        targets = _target_values(task, mask)
        support = tuple(task.worlds[i].name for i in _indices(mask, n_worlds))
        if len(targets) == 1:
            value = next(iter(targets))
            return 0, AdaptiveNode(None, (), support, value), ()
        best_cost: int | None = None
        best_node: AdaptiveNode | None = None
        roots: list[str] = []
        for q_index, q in enumerate(task.queries):
            bit = 1 << q_index
            if not (remaining & bit):
                continue
            groups = _partition(task, mask, q_index)
            if len(groups) <= 1:
                continue
            child_rows = []
            feasible = True
            for outcome, child_mask in sorted(groups.items(), key=lambda item: repr(item[0])):
                child_cost, child_node, _ = search(child_mask, remaining ^ bit)
                if child_cost is None:
                    feasible = False
                    break
                child_rows.append((outcome, child_cost, child_node))
            if not feasible:
                continue
            cost = q.cost + max(row[1] for row in child_rows)
            node = AdaptiveNode(
                q.name,
                tuple((outcome, child) for outcome, _, child in child_rows),
                support,
                None,
            )
            if best_cost is None or cost < best_cost:
                best_cost, best_node, roots = cost, node, [q.name]
            elif cost == best_cost:
                roots.append(q.name)
        return best_cost, best_node, tuple(roots)
    cost, node, roots = search(root_mask, (1 << n_queries) - 1)
    return AdaptiveResolutionReceipt(
        cost, node, roots, len({w.target for w in task.worlds}) == 1, states
    )

def adaptive_gain_receipt(task: FiniteTask) -> AdaptiveGainReceipt:
    adaptive = adaptive_minimum_resolution(task)
    fixed = fixed_minimum_resolution(task)
    ca, cf = adaptive.minimum_worst_path_cost, fixed.minimum_cost
    if ca is None and cf is None:
        return AdaptiveGainReceipt(None, None, False, None, None, "not_resolvable_by_declared_queries")
    if ca is None and cf is not None:
        raise ArithmeticError("adaptive class lost a feasible fixed bundle")
    if ca is not None and cf is None:
        raise ArithmeticError("adaptive tree exists while full fixed vocabulary does not resolve")
    assert ca is not None and cf is not None
    if ca > cf:
        raise ArithmeticError("adaptive class cannot be more expensive than the best fixed bundle")
    strict = ca < cf
    return AdaptiveGainReceipt(
        ca, cf, strict,
        ca if strict else None,
        cf - 1 if strict else None,
        "strict_adaptive_gain" if strict else "no_strict_adaptive_gain",
    )

def adaptive_only_at_budget(task: FiniteTask, budget: int) -> bool:
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    receipt = adaptive_gain_receipt(task)
    if not receipt.strict_adaptive_gain:
        return False
    return receipt.adaptive_only_budget_lower <= budget <= receipt.adaptive_only_budget_upper

@dataclass(frozen=True)
class BudgetResolutionRow:
    budget: int
    adaptive_guaranteed: bool
    fixed_guaranteed: bool
    adaptive_only: bool

def resolution_budget_profile(task: FiniteTask, max_budget: int) -> tuple[BudgetResolutionRow, ...]:
    if type(max_budget) is not int or max_budget < 0:
        raise ValueError("max_budget must be a nonnegative integer")
    receipt = adaptive_gain_receipt(task)
    ca, cf = receipt.adaptive_cost, receipt.fixed_cost
    rows = []
    for budget in range(max_budget + 1):
        adaptive = ca is not None and ca <= budget
        fixed = cf is not None and cf <= budget
        rows.append(BudgetResolutionRow(budget, adaptive, fixed, adaptive and not fixed))
    return tuple(rows)
