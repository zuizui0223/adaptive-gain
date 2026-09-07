"""Resource-labelled continuation quotient for joint adaptive/fixed resolution.

The cost-only continuation quotient is sufficient for deterministic worst-path
adaptive cost, but it can merge states/tasks whose fixed bundle costs differ
because it forgets whether branch-specific actions are the same physical query.

This module keeps each declared query as a task-local resource token.  A mixed
state is represented recursively by the productive transitions of those tokens:

    query token -> (declared cost, set of mixed child classes)

Pure children are terminal and repeated child classes are irrelevant to
worst-path guaranteed resolution.  Constant queries are omitted because they do
not refine the current state.  Unlike the cost-only quotient, query identity is
never collapsed.

The resulting quotient preserves both:

* C_A: minimum worst-path adaptive acquisition cost; and
* C_F: minimum cost of a fixed query bundle that resolves every branch.

For C_F, a selected bundle is replayed through the quotient using the same
resource tokens in every branch.  Thus cross-branch query reuse is retained.
This is a finite deterministic exact-resolution result, not a claim about noisy,
probabilistic, continuous, or calibration-changing experiments.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .core import FiniteTask, adaptive_minimum_resolution, fixed_minimum_resolution


class ResourceContinuationLimitError(RuntimeError):
    """The declared reachable-state cap was exceeded; no partial proof is returned."""


@dataclass(frozen=True, order=True)
class ResourceContinuationAction:
    query_index: int
    cost: int
    child_classes: tuple[int, ...]


@dataclass(frozen=True)
class ResourceContinuationClass:
    class_id: int
    resolved: bool
    actions: tuple[ResourceContinuationAction, ...]


@dataclass(frozen=True, order=True)
class ResourceContinuationMembership:
    world_mask: int
    remaining_queries: int
    class_id: int


@dataclass(frozen=True)
class ResourceContinuationCertificate:
    query_names: tuple[str, ...]
    query_costs: tuple[int, ...]
    root_class: int
    classes: tuple[ResourceContinuationClass, ...]
    memberships: tuple[ResourceContinuationMembership, ...]
    complete: bool = True
    scope: str = "task_local_query_identity_preserving_finite_deterministic_continuation_quotient"

    @property
    def mixed_state_count(self) -> int:
        return sum(member.class_id != 0 for member in self.memberships)

    @property
    def mixed_class_count(self) -> int:
        return len(self.classes) - 1


@dataclass(frozen=True)
class ResourceContinuationCostReceipt:
    adaptive_cost: int | None
    fixed_cost: int | None
    strict_adaptive_gain: bool
    direct_adaptive_cost: int | None
    direct_fixed_cost: int | None
    adaptive_cost_agrees: bool
    fixed_cost_agrees: bool
    exact_costs_agree: bool
    scope: str = "resource_labelled_quotient_joint_adaptive_fixed_cost_audit"


def _pure(task: FiniteTask, mask: int) -> bool:
    return len({w.target for i, w in enumerate(task.worlds) if mask & (1 << i)}) <= 1


def _cells(task: FiniteTask, mask: int, query_index: int) -> dict[object, int]:
    cells: dict[object, int] = {}
    query = task.queries[query_index]
    for i, outcome in enumerate(query.outcomes):
        if mask & (1 << i):
            cells[outcome] = cells.get(outcome, 0) | (1 << i)
    return cells


def build_resource_continuation_quotient(
    task: FiniteTask, *, max_states: int = 100_000,
) -> ResourceContinuationCertificate:
    """Build an exact task-local quotient while preserving physical query identity."""
    if not isinstance(task, FiniteTask):
        raise ValueError("task must be a FiniteTask")
    if type(max_states) is not int or max_states < 1:
        raise ValueError("max_states must be a positive integer")

    classes = [ResourceContinuationClass(0, True, ())]
    intern: dict[tuple[ResourceContinuationAction, ...], int] = {}
    memberships: dict[tuple[int, int], int] = {}
    discovered: set[tuple[int, int]] = set()

    def visit(worlds: int, remaining: int) -> int:
        key = (worlds, remaining)
        if key in memberships:
            return memberships[key]
        discovered.add(key)
        if len(discovered) > max_states:
            raise ResourceContinuationLimitError("reachable resource-state cap reached")
        if _pure(task, worlds):
            memberships[key] = 0
            return 0

        actions = []
        for q, query in enumerate(task.queries):
            bit = 1 << q
            if not remaining & bit:
                continue
            cells = _cells(task, worlds, q)
            if len(cells) == 1:
                continue
            children = {
                visit(child, remaining & ~bit)
                for child in cells.values()
                if not _pure(task, child)
            }
            actions.append(
                ResourceContinuationAction(q, query.cost, tuple(sorted(children)))
            )
        descriptor = tuple(actions)
        cid = intern.get(descriptor)
        if cid is None:
            cid = len(classes)
            intern[descriptor] = cid
            classes.append(ResourceContinuationClass(cid, False, descriptor))
        memberships[key] = cid
        return cid

    root_worlds = (1 << len(task.worlds)) - 1
    root_queries = (1 << len(task.queries)) - 1
    root_class = visit(root_worlds, root_queries)
    return ResourceContinuationCertificate(
        tuple(query.name for query in task.queries),
        tuple(query.cost for query in task.queries),
        root_class,
        tuple(classes),
        tuple(
            ResourceContinuationMembership(worlds, remaining, cid)
            for (worlds, remaining), cid in sorted(memberships.items())
        ),
    )


def verify_resource_continuation_quotient(
    task: FiniteTask, certificate: ResourceContinuationCertificate,
) -> bool:
    """Independently reconstruct every transition and query-resource token."""
    try:
        if not isinstance(task, FiniteTask):
            return False
        if not isinstance(certificate, ResourceContinuationCertificate):
            return False
        if certificate.complete is not True or not certificate.classes:
            return False
        if certificate.query_names != tuple(query.name for query in task.queries):
            return False
        if certificate.query_costs != tuple(query.cost for query in task.queries):
            return False

        classes = certificate.classes
        if classes[0] != ResourceContinuationClass(0, True, ()):
            return False
        descriptors: set[tuple[ResourceContinuationAction, ...]] = set()
        for i, cls in enumerate(classes):
            if type(cls.class_id) is not int or cls.class_id != i:
                return False
            if type(cls.resolved) is not bool or cls.resolved != (i == 0):
                return False
            if type(cls.actions) is not tuple:
                return False
            if tuple(sorted(cls.actions, key=lambda action: action.query_index)) != cls.actions:
                return False
            if len({action.query_index for action in cls.actions}) != len(cls.actions):
                return False
            if i and cls.actions in descriptors:
                return False
            if i:
                descriptors.add(cls.actions)
            for action in cls.actions:
                q = action.query_index
                if type(q) is not int or not 0 <= q < len(task.queries):
                    return False
                if type(action.cost) is not int or action.cost != task.queries[q].cost:
                    return False
                children = action.child_classes
                if type(children) is not tuple or tuple(sorted(set(children))) != children:
                    return False
                if any(type(cid) is not int or not 0 < cid < i for cid in children):
                    return False

        members: dict[tuple[int, int], int] = {}
        for member in certificate.memberships:
            fields = (member.world_mask, member.remaining_queries, member.class_id)
            if any(type(value) is not int for value in fields):
                return False
            worlds, remaining, cid = fields
            if not 0 < worlds < (1 << len(task.worlds)):
                return False
            if not 0 <= remaining < (1 << len(task.queries)):
                return False
            if not 0 <= cid < len(classes):
                return False
            key = (worlds, remaining)
            if key in members:
                return False
            members[key] = cid

        root = ((1 << len(task.worlds)) - 1, (1 << len(task.queries)) - 1)
        if type(certificate.root_class) is not int:
            return False
        if members.get(root) != certificate.root_class:
            return False

        todo = [root]
        seen: set[tuple[int, int]] = set()
        while todo:
            key = todo.pop()
            if key in seen:
                continue
            seen.add(key)
            worlds, remaining = key
            cid = members[key]
            if _pure(task, worlds):
                if cid != 0:
                    return False
                continue
            if cid == 0:
                return False

            reconstructed = []
            for q, query in enumerate(task.queries):
                bit = 1 << q
                if not remaining & bit:
                    continue
                cells = _cells(task, worlds, q)
                if len(cells) == 1:
                    continue
                child_classes = set()
                for child in cells.values():
                    if _pure(task, child):
                        continue
                    child_key = (child, remaining & ~bit)
                    if child_key not in members:
                        return False
                    child_classes.add(members[child_key])
                    todo.append(child_key)
                reconstructed.append(
                    ResourceContinuationAction(
                        q, query.cost, tuple(sorted(child_classes))
                    )
                )
            if tuple(reconstructed) != classes[cid].actions:
                return False
        return seen == set(members) and ({0} | set(members.values())) == set(range(len(classes)))
    except (AttributeError, TypeError, ValueError, IndexError, KeyError):
        return False


def _adaptive_values(
    certificate: ResourceContinuationCertificate,
) -> tuple[int | None, ...]:
    values: list[int | None] = [0]
    for cls in certificate.classes[1:]:
        candidates = []
        for action in cls.actions:
            child_values = [values[cid] for cid in action.child_classes]
            if any(value is None for value in child_values):
                continue
            candidates.append(action.cost + max(child_values, default=0))
        values.append(min(candidates) if candidates else None)
    return tuple(values)


def resource_continuation_adaptive_cost(
    task: FiniteTask, certificate: ResourceContinuationCertificate,
) -> int | None:
    if not verify_resource_continuation_quotient(task, certificate):
        raise ValueError("invalid resource continuation certificate")
    return _adaptive_values(certificate)[certificate.root_class]


def _bundle_resolves_class(
    certificate: ResourceContinuationCertificate,
    class_id: int,
    bundle_mask: int,
    cache: dict[tuple[int, int], bool],
) -> bool:
    key = (class_id, bundle_mask)
    if key in cache:
        return cache[key]
    if class_id == 0:
        cache[key] = True
        return True
    if bundle_mask == 0:
        cache[key] = False
        return False

    bit = bundle_mask & -bundle_mask
    q = bit.bit_length() - 1
    rest = bundle_mask & ~bit
    action = next(
        (row for row in certificate.classes[class_id].actions if row.query_index == q),
        None,
    )
    if action is None:
        # The resource is either already absent in this concrete state or is
        # constant on it.  In either case it contributes no further partition.
        result = _bundle_resolves_class(certificate, class_id, rest, cache)
    else:
        result = all(
            _bundle_resolves_class(certificate, child, rest, cache)
            for child in action.child_classes
        )
    cache[key] = result
    return result


def resource_continuation_fixed_cost(
    task: FiniteTask, certificate: ResourceContinuationCertificate,
) -> int | None:
    """Compute C_F on the quotient while reusing the same query tokens in all branches."""
    if not verify_resource_continuation_quotient(task, certificate):
        raise ValueError("invalid resource continuation certificate")
    qn = len(task.queries)
    best: int | None = None
    cache: dict[tuple[int, int], bool] = {}
    for bundle in range(1 << qn):
        cost = sum(task.queries[q].cost for q in range(qn) if bundle & (1 << q))
        if best is not None and cost >= best:
            continue
        if _bundle_resolves_class(certificate, certificate.root_class, bundle, cache):
            best = cost
    return best


def resource_continuation_cost_audit(
    task: FiniteTask,
    certificate: ResourceContinuationCertificate | None = None,
) -> ResourceContinuationCostReceipt:
    if certificate is None:
        certificate = build_resource_continuation_quotient(task)
    adaptive = resource_continuation_adaptive_cost(task, certificate)
    fixed = resource_continuation_fixed_cost(task, certificate)
    direct_adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    direct_fixed = fixed_minimum_resolution(task).minimum_cost
    return ResourceContinuationCostReceipt(
        adaptive,
        fixed,
        adaptive is not None and fixed is not None and adaptive < fixed,
        direct_adaptive,
        direct_fixed,
        adaptive == direct_adaptive,
        fixed == direct_fixed,
        adaptive == direct_adaptive and fixed == direct_fixed,
    )
