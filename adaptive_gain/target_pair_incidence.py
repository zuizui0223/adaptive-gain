"""Target-pair incidence is sufficient for deterministic target-resolution cost.

A fixed resolver depends only on whether each query separates each cross-target
world pair.  Less obviously, the same *full* incidence also determines the exact
adaptive worst-path target-resolution cost.

For a current represented-world subset S and query q, build a graph whose edges
join worlds with different targets when q gives them the same outcome.  Every
outcome cell containing at least two target values is exactly one connected
component of this graph.  Outcome cells containing only one target value are
already resolved and their internal same-target partition is irrelevant to the
continuation cost.  Therefore the Bellman recursion needs only target labels,
query costs, and the full cross-target separation incidence.

This theorem concerns the full incidence, not an inclusion-minimal fixed-cover
kernel.  Pair-obligation dominance can delete rows that are redundant for fixed
cover while still discarding adaptive partition geometry.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations
from typing import Hashable

from .core import FiniteTask, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True)
class TargetPairIncidenceTask:
    world_names: tuple[str, ...]
    targets: tuple[Hashable, ...]
    query_names: tuple[str, ...]
    query_costs: tuple[int, ...]
    cross_target_pairs: tuple[tuple[int, int], ...]
    query_separation_masks: tuple[int, ...]
    scope: str = "full_cross_target_pair_separation_incidence_with_target_labels_and_query_costs"


@dataclass(frozen=True)
class PairIncidenceAdaptiveReceipt:
    minimum_worst_path_cost: int | None
    optimal_first_queries: tuple[str, ...]
    search_states: int
    scope: str = "exact_adaptive_target_resolution_from_full_pair_incidence"


@dataclass(frozen=True)
class PairIncidenceFixedReceipt:
    minimum_cost: int | None
    optimal_bundles: tuple[tuple[str, ...], ...]
    scope: str = "exact_fixed_target_resolution_from_full_pair_incidence"


@dataclass(frozen=True)
class PairIncidenceSufficiencyAudit:
    direct_adaptive_cost: int | None
    incidence_adaptive_cost: int | None
    direct_fixed_cost: int | None
    incidence_fixed_cost: int | None
    adaptive_cost_agrees: bool
    fixed_cost_agrees: bool
    exact_costs_agree: bool
    scope: str = "finite_deterministic_full_pair_incidence_sufficiency_audit"


def target_pair_incidence_task(task: FiniteTask) -> TargetPairIncidenceTask:
    pairs = tuple(
        (i, j)
        for i, j in combinations(range(len(task.worlds)), 2)
        if task.worlds[i].target != task.worlds[j].target
    )
    masks = []
    for query in task.queries:
        mask = 0
        for bit, (i, j) in enumerate(pairs):
            if query.outcomes[i] != query.outcomes[j]:
                mask |= 1 << bit
        masks.append(mask)
    return TargetPairIncidenceTask(
        tuple(world.name for world in task.worlds),
        tuple(world.target for world in task.worlds),
        tuple(query.name for query in task.queries),
        tuple(query.cost for query in task.queries),
        pairs,
        tuple(masks),
    )


def _validate_incidence(task: TargetPairIncidenceTask) -> None:
    n = len(task.world_names)
    if n == 0 or len(task.targets) != n:
        raise ValueError("incidence task needs aligned nonempty worlds and targets")
    if len(set(task.world_names)) != n:
        raise ValueError("incidence world names must be unique")
    qn = len(task.query_names)
    if len(task.query_costs) != qn or len(task.query_separation_masks) != qn:
        raise ValueError("incidence query names, costs, and masks must align")
    if len(set(task.query_names)) != qn:
        raise ValueError("incidence query names must be unique")
    if any(type(cost) is not int or cost <= 0 for cost in task.query_costs):
        raise ValueError("incidence query costs must be positive integers")
    expected_pairs = tuple(
        (i, j)
        for i, j in combinations(range(n), 2)
        if task.targets[i] != task.targets[j]
    )
    if task.cross_target_pairs != expected_pairs:
        raise ValueError("cross-target pair list must be the canonical target-derived list")
    limit = 1 << len(expected_pairs)
    if any(type(mask) is not int or mask < 0 or mask >= limit for mask in task.query_separation_masks):
        raise ValueError("query separation masks must be bitmasks over all cross-target pairs")


def _target_values(task: TargetPairIncidenceTask, world_mask: int) -> set[Hashable]:
    return {
        task.targets[i]
        for i in range(len(task.targets))
        if world_mask & (1 << i)
    }


def _mixed_outcome_components(
    task: TargetPairIncidenceTask,
    world_mask: int,
    query_index: int,
) -> tuple[int, ...]:
    """Reconstruct exactly the target-mixed outcome cells from pair incidence."""
    n = len(task.targets)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    separation = task.query_separation_masks[query_index]
    for bit, (i, j) in enumerate(task.cross_target_pairs):
        if not (world_mask & (1 << i) and world_mask & (1 << j)):
            continue
        if not (separation & (1 << bit)):
            # Different targets, same query outcome.
            union(i, j)

    components: dict[int, int] = {}
    for i in range(n):
        if world_mask & (1 << i):
            root = find(i)
            components[root] = components.get(root, 0) | (1 << i)

    mixed = []
    for component in components.values():
        if len(_target_values(task, component)) > 1:
            mixed.append(component)
    return tuple(sorted(mixed))


def pair_incidence_adaptive_minimum_resolution(
    task: TargetPairIncidenceTask,
) -> PairIncidenceAdaptiveReceipt:
    """Solve the exact adaptive Bellman recursion using pair incidence only."""
    _validate_incidence(task)
    n, qn = len(task.targets), len(task.query_names)
    root_worlds = (1 << n) - 1
    root_queries = (1 << qn) - 1
    states = 0

    @lru_cache(None)
    def search(world_mask: int, remaining_queries: int):
        nonlocal states
        states += 1
        if len(_target_values(task, world_mask)) <= 1:
            return 0, ()
        best: int | None = None
        roots: list[str] = []
        for q in range(qn):
            bit = 1 << q
            if not (remaining_queries & bit):
                continue
            mixed = _mixed_outcome_components(task, world_mask, q)
            if len(mixed) == 1 and mixed[0] == world_mask:
                # No target-relevant progress. Pure resolved cells, if any, would
                # make the mixed component a strict subset instead.
                continue
            child_costs = []
            feasible = True
            for child in mixed:
                cost, _ = search(child, remaining_queries ^ bit)
                if cost is None:
                    feasible = False
                    break
                child_costs.append(cost)
            if not feasible:
                continue
            cost = task.query_costs[q] + (max(child_costs) if child_costs else 0)
            if best is None or cost < best:
                best = cost
                roots = [task.query_names[q]]
            elif cost == best:
                roots.append(task.query_names[q])
        return best, tuple(roots)

    cost, roots = search(root_worlds, root_queries)
    return PairIncidenceAdaptiveReceipt(cost, roots, states)


def _bundle_resolves_incidence(
    task: TargetPairIncidenceTask,
    query_indices: tuple[int, ...],
) -> bool:
    if not task.cross_target_pairs:
        return True
    covered = 0
    for q in query_indices:
        covered |= task.query_separation_masks[q]
    return covered == (1 << len(task.cross_target_pairs)) - 1


def pair_incidence_fixed_minimum_resolution(
    task: TargetPairIncidenceTask,
) -> PairIncidenceFixedReceipt:
    _validate_incidence(task)
    qn = len(task.query_names)
    if not task.cross_target_pairs:
        return PairIncidenceFixedReceipt(0, ((),))
    best: int | None = None
    bundles: list[tuple[str, ...]] = []
    for subset in range(1 << qn):
        indices = tuple(q for q in range(qn) if subset & (1 << q))
        cost = sum(task.query_costs[q] for q in indices)
        if best is not None and cost > best:
            continue
        if not _bundle_resolves_incidence(task, indices):
            continue
        names = tuple(task.query_names[q] for q in indices)
        if best is None or cost < best:
            best, bundles = cost, [names]
        elif cost == best:
            bundles.append(names)
    return PairIncidenceFixedReceipt(best, tuple(bundles))


def pair_incidence_sufficiency_audit(task: FiniteTask) -> PairIncidenceSufficiencyAudit:
    incidence = target_pair_incidence_task(task)
    direct_adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    incidence_adaptive = pair_incidence_adaptive_minimum_resolution(incidence).minimum_worst_path_cost
    direct_fixed = fixed_minimum_resolution(task).minimum_cost
    incidence_fixed = pair_incidence_fixed_minimum_resolution(incidence).minimum_cost
    return PairIncidenceSufficiencyAudit(
        direct_adaptive,
        incidence_adaptive,
        direct_fixed,
        incidence_fixed,
        direct_adaptive == incidence_adaptive,
        direct_fixed == incidence_fixed,
        direct_adaptive == incidence_adaptive and direct_fixed == incidence_fixed,
    )
