"""Capacity-aware task-automorphism quotient for joint adaptive/fixed states.

A resource automorphism may rename worlds and physical queries simultaneously,
but it does not make several physical query tokens into one token.  This module
therefore quotients STATE LABELS, not resource multiplicity.

A state carries:

* the current represented-world subset;
* the remaining physical-query subset; and, for fixed replay,
* the still-selected fixed-bundle subset.

Every exact task automorphism transports all of those masks together.  Canonical
orbit representatives can be shared without losing the number of distinct
resources remaining in a query orbit.  This is the finite exact version of
"resource orbit + capacity" for small deterministic tasks.

The automorphism enumeration is factorial and fail-closed behind a hard cap.  It
is intended as a structural verifier/control, not a scalable general graph
canonicalizer.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import permutations, product
from math import factorial

from .core import FiniteTask, adaptive_minimum_resolution, fixed_minimum_resolution


class ResourceOrbitLimitError(RuntimeError):
    """Exact task-automorphism enumeration exceeded the declared cap."""


@dataclass(frozen=True, order=True)
class TaskAutomorphism:
    world_mapping: tuple[int, ...]
    query_mapping: tuple[int, ...]


@dataclass(frozen=True)
class TaskAutomorphismReceipt:
    automorphisms: tuple[TaskAutomorphism, ...]
    world_target_class_sizes: tuple[int, ...]
    query_cost_class_sizes: tuple[int, ...]
    candidate_pairs_examined: int
    complete_enumeration: bool
    scope: str = "exact_target_and_cost_preserving_task_automorphism_up_to_query_outcome_relabeling"

    @property
    def automorphism_count(self) -> int:
        return len(self.automorphisms)


@dataclass(frozen=True)
class ResourceOrbitCostReceipt:
    automorphism_count: int
    adaptive_cost: int | None
    fixed_cost: int | None
    direct_adaptive_cost: int | None
    direct_fixed_cost: int | None
    adaptive_state_occurrences: int
    adaptive_orbit_states: int
    fixed_state_occurrences: int
    fixed_orbit_states: int
    adaptive_cost_agrees: bool
    fixed_cost_agrees: bool
    exact_costs_agree: bool
    scope: str = "capacity_aware_resource_orbit_joint_cost_audit"


def _partition_signature(outcomes: tuple[object, ...], order: tuple[int, ...]) -> tuple[tuple[bool, ...], ...]:
    """Outcome-label-free equality matrix after a world permutation."""
    return tuple(
        tuple(outcomes[order[i]] == outcomes[order[j]] for j in range(len(order)))
        for i in range(len(order))
    )


def _groups(values: tuple[object, ...]) -> tuple[tuple[int, ...], ...]:
    buckets: dict[object, list[int]] = {}
    for i, value in enumerate(values):
        buckets.setdefault(value, []).append(i)
    return tuple(tuple(indices) for _, indices in sorted(buckets.items(), key=lambda item: min(item[1])))


def _permutation_family(groups: tuple[tuple[int, ...], ...], n: int):
    families = tuple(tuple(permutations(group)) for group in groups)
    for selected in product(*families):
        mapping = list(range(n))
        for group, image in zip(groups, selected):
            for old, new in zip(group, image):
                mapping[old] = new
        yield tuple(mapping)


def _inverse(mapping: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(mapping)
    for old, new in enumerate(mapping):
        inverse[new] = old
    return tuple(inverse)


def _mapped_query_partition(task: FiniteTask, q: int, world_mapping: tuple[int, ...]) -> tuple[tuple[bool, ...], ...]:
    # world_mapping is old -> new.  In the new coordinate order, position j came
    # from inverse[j] in the original task.
    inverse = _inverse(world_mapping)
    return _partition_signature(task.queries[q].outcomes, inverse)


def task_automorphism_group(
    task: FiniteTask, *, max_candidates: int = 200_000,
) -> TaskAutomorphismReceipt:
    """Enumerate exact target/cost-preserving task automorphisms for a small task."""
    if not isinstance(task, FiniteTask):
        raise ValueError("task must be a FiniteTask")
    if type(max_candidates) is not int or max_candidates < 1:
        raise ValueError("max_candidates must be a positive integer")

    world_groups = _groups(tuple(world.target for world in task.worlds))
    query_groups = _groups(tuple(query.cost for query in task.queries))
    world_candidates = 1
    for group in world_groups:
        world_candidates *= factorial(len(group))
    query_candidates = 1
    for group in query_groups:
        query_candidates *= factorial(len(group))
    total = world_candidates * query_candidates
    if total > max_candidates:
        raise ResourceOrbitLimitError(
            f"exact task automorphism enumeration needs {total} candidate world/query mappings, "
            f"exceeding cap {max_candidates}"
        )

    original_partitions = tuple(
        _partition_signature(query.outcomes, tuple(range(len(task.worlds))))
        for query in task.queries
    )
    automorphisms = []
    examined = 0
    for world_mapping in _permutation_family(world_groups, len(task.worlds)):
        transformed = tuple(
            _mapped_query_partition(task, q, world_mapping)
            for q in range(len(task.queries))
        )
        for query_mapping in _permutation_family(query_groups, len(task.queries)):
            examined += 1
            if all(
                transformed[q] == original_partitions[query_mapping[q]]
                for q in range(len(task.queries))
            ):
                automorphisms.append(TaskAutomorphism(world_mapping, query_mapping))
    identity = TaskAutomorphism(
        tuple(range(len(task.worlds))), tuple(range(len(task.queries)))
    )
    if identity not in automorphisms:
        raise ArithmeticError("identity task automorphism was lost")
    receipt = TaskAutomorphismReceipt(
        tuple(sorted(automorphisms)),
        tuple(len(group) for group in world_groups),
        tuple(len(group) for group in query_groups),
        examined,
        True,
    )
    if not verify_task_automorphism_group(task, receipt):
        raise ArithmeticError("task automorphism receipt failed independent verification")
    return receipt


def verify_task_automorphism_group(task: FiniteTask, receipt: TaskAutomorphismReceipt) -> bool:
    """Re-enumerate the bounded family and verify exact completeness."""
    try:
        if not isinstance(task, FiniteTask) or not receipt.complete_enumeration:
            return False
        rebuilt = task_automorphism_group.__wrapped__(task)  # type: ignore[attr-defined]
        return rebuilt == receipt
    except (AttributeError, TypeError, ValueError, ArithmeticError, ResourceOrbitLimitError):
        return False


# Install an internal non-verifying builder so the public builder can verify
# without recursive self-calls.  Keeping it here avoids duplicating the exact
# enumeration logic in a second module.
def _task_automorphism_group_unverified(task: FiniteTask, *, max_candidates: int = 200_000):
    world_groups = _groups(tuple(world.target for world in task.worlds))
    query_groups = _groups(tuple(query.cost for query in task.queries))
    total = 1
    for group in world_groups:
        total *= factorial(len(group))
    for group in query_groups:
        total *= factorial(len(group))
    if total > max_candidates:
        raise ResourceOrbitLimitError("task automorphism candidate cap reached")
    original = tuple(
        _partition_signature(query.outcomes, tuple(range(len(task.worlds))))
        for query in task.queries
    )
    autos = []
    examined = 0
    for wm in _permutation_family(world_groups, len(task.worlds)):
        transformed = tuple(_mapped_query_partition(task, q, wm) for q in range(len(task.queries)))
        for qm in _permutation_family(query_groups, len(task.queries)):
            examined += 1
            if all(transformed[q] == original[qm[q]] for q in range(len(task.queries))):
                autos.append(TaskAutomorphism(wm, qm))
    return TaskAutomorphismReceipt(
        tuple(sorted(autos)),
        tuple(len(group) for group in world_groups),
        tuple(len(group) for group in query_groups),
        examined,
        True,
    )

# Python functions do not normally expose __wrapped__; use it as a private hook
# for the independent verifier without changing the public API.
task_automorphism_group.__wrapped__ = _task_automorphism_group_unverified  # type: ignore[attr-defined]


def _map_mask(mask: int, mapping: tuple[int, ...]) -> int:
    result = 0
    for old, new in enumerate(mapping):
        if mask & (1 << old):
            result |= 1 << new
    return result


def canonical_resource_state(
    world_mask: int,
    remaining_query_mask: int,
    receipt: TaskAutomorphismReceipt,
) -> tuple[int, int]:
    return min(
        (
            _map_mask(world_mask, auto.world_mapping),
            _map_mask(remaining_query_mask, auto.query_mapping),
        )
        for auto in receipt.automorphisms
    )


def canonical_fixed_replay_state(
    world_mask: int,
    remaining_query_mask: int,
    bundle_mask: int,
    receipt: TaskAutomorphismReceipt,
) -> tuple[int, int, int]:
    return min(
        (
            _map_mask(world_mask, auto.world_mapping),
            _map_mask(remaining_query_mask, auto.query_mapping),
            _map_mask(bundle_mask, auto.query_mapping),
        )
        for auto in receipt.automorphisms
    )


def _pure(task: FiniteTask, mask: int) -> bool:
    return len({w.target for i, w in enumerate(task.worlds) if mask & (1 << i)}) <= 1


def _cells(task: FiniteTask, mask: int, q: int) -> tuple[int, ...]:
    cells: dict[object, int] = {}
    for i, outcome in enumerate(task.queries[q].outcomes):
        if mask & (1 << i):
            cells[outcome] = cells.get(outcome, 0) | (1 << i)
    return tuple(cells.values())


def resource_orbit_cost_audit(task: FiniteTask, *, max_candidates: int = 200_000) -> ResourceOrbitCostReceipt:
    """Compute both costs while memoizing exact automorphism orbits of resource states."""
    group = task_automorphism_group(task, max_candidates=max_candidates)
    n, qn = len(task.worlds), len(task.queries)
    root_worlds = (1 << n) - 1
    root_queries = (1 << qn) - 1
    adaptive_occurrences = 0
    adaptive_cache: dict[tuple[int, int], int | None] = {}

    def adaptive(worlds: int, remaining: int) -> int | None:
        nonlocal adaptive_occurrences
        adaptive_occurrences += 1
        key = canonical_resource_state(worlds, remaining, group)
        if key in adaptive_cache:
            return adaptive_cache[key]
        worlds, remaining = key
        if _pure(task, worlds):
            adaptive_cache[key] = 0
            return 0
        best = None
        for q, query in enumerate(task.queries):
            bit = 1 << q
            if not remaining & bit:
                continue
            cells = _cells(task, worlds, q)
            if len(cells) <= 1:
                continue
            child_values = []
            feasible = True
            for child in cells:
                if _pure(task, child):
                    continue
                value = adaptive(child, remaining & ~bit)
                if value is None:
                    feasible = False
                    break
                child_values.append(value)
            if feasible:
                value = query.cost + max(child_values, default=0)
                best = value if best is None or value < best else best
        adaptive_cache[key] = best
        return best

    adaptive_cost = adaptive(root_worlds, root_queries)

    fixed_occurrences = 0
    fixed_cache: dict[tuple[int, int, int], bool] = {}

    def fixed_resolves(worlds: int, remaining: int, bundle: int) -> bool:
        nonlocal fixed_occurrences
        fixed_occurrences += 1
        key = canonical_fixed_replay_state(worlds, remaining, bundle, group)
        if key in fixed_cache:
            return fixed_cache[key]
        worlds, remaining, bundle = key
        if _pure(task, worlds):
            fixed_cache[key] = True
            return True
        available_bundle = bundle & remaining
        if not available_bundle:
            fixed_cache[key] = False
            return False
        bit = available_bundle & -available_bundle
        q = bit.bit_length() - 1
        cells = _cells(task, worlds, q)
        next_remaining = remaining & ~bit
        next_bundle = bundle & ~bit
        if len(cells) <= 1:
            result = fixed_resolves(worlds, next_remaining, next_bundle)
        else:
            result = all(
                _pure(task, child)
                or fixed_resolves(child, next_remaining, next_bundle)
                for child in cells
            )
        fixed_cache[key] = result
        return result

    fixed_cost = None
    for bundle in range(1 << qn):
        cost = sum(task.queries[q].cost for q in range(qn) if bundle & (1 << q))
        if fixed_cost is not None and cost >= fixed_cost:
            continue
        if fixed_resolves(root_worlds, root_queries, bundle):
            fixed_cost = cost

    direct_adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    direct_fixed = fixed_minimum_resolution(task).minimum_cost
    return ResourceOrbitCostReceipt(
        group.automorphism_count,
        adaptive_cost,
        fixed_cost,
        direct_adaptive,
        direct_fixed,
        adaptive_occurrences,
        len(adaptive_cache),
        fixed_occurrences,
        len(fixed_cache),
        adaptive_cost == direct_adaptive,
        fixed_cost == direct_fixed,
        adaptive_cost == direct_adaptive and fixed_cost == direct_fixed,
    )
