"""Resource-overlap diagnostics for joint adaptive/fixed representations.

The cost-only continuation quotient forgets physical query identity. Keeping only
query-orbit capacities is still insufficient for the fixed comparator. A stronger
projection records, for every physical resource, the set of abstract continuation
roles it can realize across reachable mixed states. That projection is also not
sufficient in general: two four-world/four-query tasks can have the same multiset
of per-resource role profiles while their fixed costs differ.

This module makes those losses executable. It also exposes a stronger
state-resource co-location signature that retains which local roles coexist in the
same concrete reachable state. Co-location distinguishes the registered collision
but is NOT claimed to be generally sufficient. The exact sufficient joint
representation remains ``resource_continuation.py``, which keeps resource-labelled
transition structure.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import permutations, product
from math import factorial
from typing import Sequence

from .continuation_bisimulation import (
    ContinuationQuotientCertificate,
    build_continuation_quotient,
)
from .core import FiniteTask, Query, World, adaptive_gain_receipt
from .resource_orbit_quotient import task_automorphism_group


class ResourceCoLocationLimitError(RuntimeError):
    """Exact cost-preserving query-column canonicalization exceeded its cap."""


@dataclass(frozen=True)
class ResourceOverlapTaskSignature:
    continuation_root_type: tuple
    resource_orbit_capacity_profile: tuple[tuple[int, int], ...]
    resource_role_profile_multiset: tuple[tuple, ...]
    state_resource_colocation_signature: tuple
    scope: str = "finite_deterministic_resource_overlap_projection"


@dataclass(frozen=True)
class ResourceOverlapCollisionAudit:
    orbit_capacity_costs: tuple[tuple[int | None, int | None], ...]
    orbit_capacity_signatures_equal: bool
    role_profile_costs: tuple[tuple[int | None, int | None], ...]
    role_profile_signatures_equal: bool
    role_profile_colocation_signatures_equal: bool
    interpretation: str
    scope: str = "explicit_resource_overlap_information_loss_hierarchy"


@dataclass(frozen=True)
class ResourceRoleOverlapUniverseSummary:
    query_count: int
    task_count: int
    signature_count: int
    ambiguous_signature_count: int
    ambiguous_task_count: int
    ambiguous_cost_pair_counts: tuple[tuple[tuple[int | None, int | None], int], ...]
    scope: str = "balanced_four_world_binary_unit_cost_resource_role_overlap_exhaustive_scan"


def orbit_capacity_collision() -> tuple[FiniteTask, FiniteTask]:
    """Same continuation type + resource-orbit capacities; fixed costs 3 vs 2."""
    worlds = tuple(World(f"w{i}", 0 if i < 2 else 1) for i in range(5))
    strict = FiniteTask(
        worlds,
        (
            Query("q0", 1, (0, 0, 0, 0, 1)),
            Query("q1", 1, (0, 1, 0, 0, 0)),
            Query("q2", 1, (0, 1, 1, 1, 0)),
        ),
    )
    bypass = FiniteTask(
        worlds,
        (
            Query("q0", 1, (0, 1, 0, 0, 0)),
            Query("q1", 1, (0, 1, 0, 0, 1)),
            Query("q2", 1, (0, 1, 1, 1, 0)),
        ),
    )
    return strict, bypass


def resource_role_profile_collision() -> tuple[FiniteTask, FiniteTask]:
    """Same continuation + per-resource abstract role profiles; fixed 2 vs 3."""
    worlds = tuple(World(f"w{i}", i // 2) for i in range(4))
    no_gain = FiniteTask(
        worlds,
        (
            Query("left", 1, (0, 0, 0, 1)),
            Query("right", 1, (0, 1, 0, 0)),
            Query("bypass", 1, (0, 1, 0, 1)),
            Query("route", 1, (0, 1, 1, 0)),
        ),
    )
    strict = FiniteTask(
        worlds,
        (
            Query("left", 1, (0, 0, 0, 1)),
            Query("right", 1, (0, 1, 0, 0)),
            Query("route_a", 1, (0, 1, 1, 0)),
            Query("route_b", 1, (0, 1, 1, 0)),
        ),
    )
    return no_gain, strict


def _class_types(certificate: ContinuationQuotientCertificate) -> tuple[tuple, ...]:
    result: list[tuple] = [("R",)]
    for cls in certificate.classes[1:]:
        action_rows = [
            (
                "A",
                action.cost,
                tuple(result[child] for child in action.child_classes),
            )
            for action in cls.actions
        ]
        result.append(("M", tuple(sorted(action_rows, key=repr))))
    return tuple(result)


def _cells(task: FiniteTask, world_mask: int, query_index: int) -> tuple[int, ...]:
    groups: dict[object, int] = {}
    query = task.queries[query_index]
    for i, outcome in enumerate(query.outcomes):
        if world_mask & (1 << i):
            groups[outcome] = groups.get(outcome, 0) | (1 << i)
    return tuple(groups.values())


def _pure(task: FiniteTask, world_mask: int) -> bool:
    return len(
        {
            task.worlds[i].target
            for i in range(len(task.worlds))
            if world_mask & (1 << i)
        }
    ) <= 1


def _query_orbit_capacity_profile(task: FiniteTask) -> tuple[tuple[int, int], ...]:
    receipt = task_automorphism_group(task)
    unseen = set(range(len(task.queries)))
    rows = []
    while unseen:
        q = min(unseen)
        orbit = {auto.query_mapping[q] for auto in receipt.automorphisms}
        rows.append((task.queries[q].cost, len(orbit)))
        unseen.difference_update(orbit)
    return tuple(sorted(rows))


def _resource_role_profiles(
    task: FiniteTask,
    certificate: ContinuationQuotientCertificate,
    task_index: int,
    class_types: tuple[tuple, ...],
) -> tuple[tuple, ...]:
    lookup = {
        (member.world_mask, member.remaining_queries): member.class_id
        for member in certificate.memberships
        if member.task_index == task_index
    }
    profiles: list[set[tuple]] = [set() for _ in task.queries]
    for member in certificate.memberships:
        if member.task_index != task_index or member.class_id == 0:
            continue
        parent_type = class_types[member.class_id]
        for q, query in enumerate(task.queries):
            bit = 1 << q
            if not (member.remaining_queries & bit):
                continue
            cells = _cells(task, member.world_mask, q)
            if len(cells) <= 1:
                continue
            children = set()
            for child in cells:
                if _pure(task, child):
                    continue
                child_id = lookup[(child, member.remaining_queries & ~bit)]
                children.add(class_types[child_id])
            action_type = ("A", query.cost, tuple(sorted(children, key=repr)))
            profiles[q].add((parent_type, action_type))
    return tuple(
        sorted(
            (tuple(sorted(profile, key=repr)) for profile in profiles),
            key=repr,
        )
    )


def _cost_preserving_orders(task: FiniteTask, max_permutations: int):
    groups: dict[int, list[int]] = {}
    for q, query in enumerate(task.queries):
        groups.setdefault(query.cost, []).append(q)
    ordered_groups = tuple(tuple(groups[cost]) for cost in sorted(groups))
    count = 1
    for group in ordered_groups:
        count *= factorial(len(group))
    if count > max_permutations:
        raise ResourceCoLocationLimitError(
            f"state-resource co-location canonicalization needs {count} query permutations, "
            f"exceeding cap {max_permutations}"
        )
    families = tuple(tuple(permutations(group)) for group in ordered_groups)
    for selected in product(*families):
        order = []
        for family in selected:
            order.extend(family)
        yield tuple(order)


def _state_resource_colocation_signature(
    task: FiniteTask,
    certificate: ContinuationQuotientCertificate,
    task_index: int,
    class_types: tuple[tuple, ...],
    *,
    max_permutations: int,
) -> tuple:
    lookup = {
        (member.world_mask, member.remaining_queries): member.class_id
        for member in certificate.memberships
        if member.task_index == task_index
    }
    rows = []
    for member in certificate.memberships:
        if member.task_index != task_index or member.class_id == 0:
            continue
        cells_by_query = []
        for q, query in enumerate(task.queries):
            bit = 1 << q
            if not (member.remaining_queries & bit):
                cells_by_query.append(("U",))
                continue
            cells = _cells(task, member.world_mask, q)
            if len(cells) <= 1:
                cells_by_query.append(("C", query.cost))
                continue
            children = set()
            for child in cells:
                if _pure(task, child):
                    continue
                child_id = lookup[(child, member.remaining_queries & ~bit)]
                children.add(class_types[child_id])
            cells_by_query.append(
                ("P", query.cost, tuple(sorted(children, key=repr)))
            )
        rows.append((class_types[member.class_id], tuple(cells_by_query)))

    best = None
    best_key = None
    for order in _cost_preserving_orders(task, max_permutations):
        transformed_rows = [
            (parent, tuple(cells[q] for q in order))
            for parent, cells in rows
        ]
        candidate = tuple(sorted(transformed_rows, key=repr))
        key = repr(candidate)
        if best_key is None or key < best_key:
            best, best_key = candidate, key
    return best if best is not None else ()


def resource_overlap_signatures(
    tasks: Sequence[FiniteTask], *, max_permutations: int = 100_000,
) -> tuple[ResourceOverlapTaskSignature, ...]:
    tasks = tuple(tasks)
    if not tasks:
        raise ValueError("tasks must be nonempty")
    certificate = build_continuation_quotient(tasks)
    class_types = _class_types(certificate)
    rows = []
    for t, task in enumerate(tasks):
        rows.append(
            ResourceOverlapTaskSignature(
                class_types[certificate.root_classes[t]],
                _query_orbit_capacity_profile(task),
                _resource_role_profiles(task, certificate, t, class_types),
                _state_resource_colocation_signature(
                    task,
                    certificate,
                    t,
                    class_types,
                    max_permutations=max_permutations,
                ),
            )
        )
    return tuple(rows)


def resource_overlap_collision_audit() -> ResourceOverlapCollisionAudit:
    capacity_tasks = orbit_capacity_collision()
    capacity_signatures = resource_overlap_signatures(capacity_tasks)
    capacity_costs = tuple(
        (receipt.adaptive_cost, receipt.fixed_cost)
        for receipt in map(adaptive_gain_receipt, capacity_tasks)
    )
    capacity_equal = (
        capacity_signatures[0].continuation_root_type
        == capacity_signatures[1].continuation_root_type
        and capacity_signatures[0].resource_orbit_capacity_profile
        == capacity_signatures[1].resource_orbit_capacity_profile
    )

    role_tasks = resource_role_profile_collision()
    role_signatures = resource_overlap_signatures(role_tasks)
    role_costs = tuple(
        (receipt.adaptive_cost, receipt.fixed_cost)
        for receipt in map(adaptive_gain_receipt, role_tasks)
    )
    role_equal = (
        role_signatures[0].continuation_root_type
        == role_signatures[1].continuation_root_type
        and role_signatures[0].resource_role_profile_multiset
        == role_signatures[1].resource_role_profile_multiset
    )
    coloc_equal = (
        role_signatures[0].state_resource_colocation_signature
        == role_signatures[1].state_resource_colocation_signature
    )
    return ResourceOverlapCollisionAudit(
        capacity_costs,
        capacity_equal,
        role_costs,
        role_equal,
        coloc_equal,
        (
            "orbit capacity and then first-order per-resource role profiles both admit explicit fixed-cost collisions; "
            "the registered four-query role collision is separated only after retaining concrete state-resource co-location"
        ),
    )


def enumerate_balanced_resource_role_overlap_universe(
    query_count: int,
) -> ResourceRoleOverlapUniverseSummary:
    """Exact compact scan for 4 balanced worlds and binary unit-cost queries.

    The global interning table gives one shared structural continuation vocabulary
    across the complete labeled universe. The signature keeps the root class and
    the multiset of each resource's abstract local role set. This is a scope-
    specific classifier used to locate the first resource-role ambiguity; it is
    not a general canonicalizer.
    """
    if query_count not in (3, 4):
        raise ValueError("registered exhaustive scope supports query_count 3 or 4")
    targets = (0, 0, 1, 1)
    patterns = tuple(product((0, 1), repeat=4))
    intern: dict[tuple, int] = {}
    class_values: dict[int, int | None] = {0: 0}
    next_id = 1
    signature_costs: dict[tuple, Counter] = {}

    def pure(mask: int) -> bool:
        return len({targets[i] for i in range(4) if mask & (1 << i)}) <= 1

    for maps in product(patterns, repeat=query_count):
        memberships: dict[tuple[int, int], int] = {}
        profiles: list[set[tuple]] = [set() for _ in range(query_count)]

        def groups(world_mask: int, q: int) -> tuple[int, ...]:
            zero = one = 0
            for i in range(4):
                if not (world_mask & (1 << i)):
                    continue
                if maps[q][i]:
                    one |= 1 << i
                else:
                    zero |= 1 << i
            return tuple(mask for mask in (zero, one) if mask)

        def visit(world_mask: int, remaining: int) -> int:
            nonlocal next_id
            key = (world_mask, remaining)
            if key in memberships:
                return memberships[key]
            if pure(world_mask):
                memberships[key] = 0
                return 0
            actions = set()
            local_actions = []
            for q in range(query_count):
                bit = 1 << q
                if not (remaining & bit):
                    continue
                cells = groups(world_mask, q)
                if len(cells) <= 1:
                    continue
                children = set()
                for child in cells:
                    if not pure(child):
                        children.add(visit(child, remaining & ~bit))
                action = (1, tuple(sorted(children)))
                actions.add(action)
                local_actions.append((q, action))
            descriptor = tuple(sorted(actions))
            cid = intern.get(descriptor)
            if cid is None:
                cid = next_id
                next_id += 1
                intern[descriptor] = cid
                candidates = []
                for cost, children in descriptor:
                    values = [class_values[child] for child in children]
                    if any(value is None for value in values):
                        continue
                    candidates.append(cost + max(values, default=0))
                class_values[cid] = min(candidates) if candidates else None
            memberships[key] = cid
            for q, action in local_actions:
                profiles[q].add((cid, action))
            return cid

        root = visit(0b1111, (1 << query_count) - 1)
        profile_multiset = tuple(
            sorted(
                (tuple(sorted(profile)) for profile in profiles),
                key=repr,
            )
        )
        signature = (root, profile_multiset)

        fixed = None
        for bundle in range(1 << query_count):
            cost = bundle.bit_count()
            if fixed is not None and cost >= fixed:
                continue
            resolves = True
            for i, j in ((0, 2), (0, 3), (1, 2), (1, 3)):
                if not any(
                    bundle & (1 << q) and maps[q][i] != maps[q][j]
                    for q in range(query_count)
                ):
                    resolves = False
                    break
            if resolves:
                fixed = cost
        pair = (class_values[root], fixed)
        signature_costs.setdefault(signature, Counter())[pair] += 1

    ambiguous = [counts for counts in signature_costs.values() if len(counts) > 1]
    merged = Counter()
    for counts in ambiguous:
        merged.update(counts)
    return ResourceRoleOverlapUniverseSummary(
        query_count,
        16 ** query_count,
        len(signature_costs),
        len(ambiguous),
        sum(merged.values()),
        tuple(sorted(merged.items(), key=repr)),
    )
