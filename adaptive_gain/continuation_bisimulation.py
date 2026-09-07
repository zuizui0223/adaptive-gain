"""Cost-labelled continuation bisimulation for finite guaranteed target resolution.

Build a structural quotient BEFORE evaluating any Bellman minima. A query is
represented by its acquisition cost and SET of recursively equivalent mixed
children. Outcome labels, pure outcomes, repeated child types and repeated action
types do not affect deterministic worst-path cost. Original state memberships are
retained so a class-level choice can be lifted to real query/outcome names.

This is an adaptive-cost quotient, not a fixed-bundle, probability, or scientific
report quotient. The complete reachable mixed-state graph is still constructed;
no polynomial-time or end-to-end speedup claim is made.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .core import AdaptiveNode, FiniteTask


class ContinuationQuotientLimitError(RuntimeError):
    """The declared structural-state cap was reached; no partial proof is returned."""


@dataclass(frozen=True, order=True)
class ContinuationAction:
    cost: int
    child_classes: tuple[int, ...]


@dataclass(frozen=True)
class ContinuationClass:
    class_id: int
    resolved: bool
    actions: tuple[ContinuationAction, ...]


@dataclass(frozen=True, order=True)
class ContinuationMembership:
    task_index: int
    world_mask: int
    remaining_queries: int
    class_id: int


@dataclass(frozen=True)
class ContinuationQuotientCertificate:
    root_classes: tuple[int, ...]
    classes: tuple[ContinuationClass, ...]
    memberships: tuple[ContinuationMembership, ...]
    complete: bool = True
    scope: str = "finite_positive_cost_deterministic_worst_path_continuation_bisimulation"

    @property
    def mixed_state_count(self) -> int:
        return sum(member.class_id != 0 for member in self.memberships)

    @property
    def mixed_class_count(self) -> int:
        return len(self.classes) - 1


@dataclass(frozen=True)
class LiftedContinuationPolicy:
    minimum_worst_path_cost: int | None
    selected_policy: AdaptiveNode | None
    optimal_first_queries: tuple[str, ...]


def _tasks(tasks: Sequence[FiniteTask]) -> tuple[FiniteTask, ...]:
    result = tuple(tasks)
    if not result or any(not isinstance(task, FiniteTask) for task in result):
        raise ValueError("tasks must be a nonempty sequence of FiniteTask objects")
    return result


def _pure(task: FiniteTask, mask: int) -> bool:
    return len({w.target for i, w in enumerate(task.worlds) if mask & (1 << i)}) == 1


def _cells(task: FiniteTask, mask: int, query: int) -> dict[object, int]:
    cells: dict[object, int] = {}
    for i, outcome in enumerate(task.queries[query].outcomes):
        if mask & (1 << i):
            cells[outcome] = cells.get(outcome, 0) | (1 << i)
    return cells


def build_continuation_quotient(
    tasks: Sequence[FiniteTask], *, max_states: int = 100_000,
) -> ContinuationQuotientCertificate:
    """Hash-cons recursive cost/action/child-type structures, without solving V.

    Class 0 is the resolved marker, including implicit pure outcome leaves.
    IDs are certificate-local, not persistent cross-run canonical identifiers.
    Multiple tasks use one interning table to permit checked cross-task matches.
    """
    tasks = _tasks(tasks)
    if type(max_states) is not int or max_states < 1:
        raise ValueError("max_states must be a positive integer")
    classes = [ContinuationClass(0, True, ())]
    intern: dict[tuple[ContinuationAction, ...], int] = {}
    memberships: dict[tuple[int, int, int], int] = {}
    discovered: set[tuple[int, int, int]] = set()

    def visit(t: int, worlds: int, remaining: int) -> int:
        key = (t, worlds, remaining)
        if key in memberships:
            return memberships[key]
        discovered.add(key)
        if len(discovered) > max_states:
            raise ContinuationQuotientLimitError("reachable structural-state cap reached")
        task = tasks[t]
        if _pure(task, worlds):
            memberships[key] = 0
            return 0
        choices: set[ContinuationAction] = set()
        for q, query in enumerate(task.queries):
            if not remaining & (1 << q):
                continue
            cells = _cells(task, worlds, q)
            if len(cells) == 1:
                continue  # A positive-cost constant query can never improve V.
            children = {
                visit(t, child, remaining & ~(1 << q))
                for child in cells.values() if not _pure(task, child)
            }
            choices.add(ContinuationAction(query.cost, tuple(sorted(children))))
        descriptor = tuple(sorted(choices))
        cid = intern.get(descriptor)
        if cid is None:
            cid = len(classes)
            intern[descriptor] = cid
            classes.append(ContinuationClass(cid, False, descriptor))
        memberships[key] = cid
        return cid

    roots = tuple(
        visit(t, (1 << len(task.worlds)) - 1, (1 << len(task.queries)) - 1)
        for t, task in enumerate(tasks)
    )
    return ContinuationQuotientCertificate(
        roots, tuple(classes),
        tuple(ContinuationMembership(*key, cid) for key, cid in sorted(memberships.items())),
    )


def verify_continuation_quotient(
    tasks: Sequence[FiniteTask], certificate: ContinuationQuotientCertificate,
) -> bool:
    """Rebuild every supported mixed transition; trust neither hashes nor values.

    A separate equality-based partition routine is used here. Missing actions,
    missing children, unreachable memberships, fake merges, cycles, cost changes,
    and invalid integer fields are rejected. No Bellman oracle is invoked.
    """
    try:
        tasks = _tasks(tasks)
        if not isinstance(certificate, ContinuationQuotientCertificate):
            return False
        if certificate.complete is not True or not certificate.classes:
            return False
        if len(certificate.root_classes) != len(tasks):
            return False
        classes = certificate.classes
        if classes[0] != ContinuationClass(0, True, ()):
            return False
        descriptors: set[tuple[ContinuationAction, ...]] = set()
        for i, cls in enumerate(classes):
            if type(cls.class_id) is not int or cls.class_id != i:
                return False
            if type(cls.resolved) is not bool or cls.resolved != (i == 0):
                return False
            if type(cls.actions) is not tuple or tuple(sorted(set(cls.actions))) != cls.actions:
                return False
            if i and cls.actions in descriptors:
                return False
            if i:
                descriptors.add(cls.actions)
            for action in cls.actions:
                if type(action.cost) is not int or action.cost <= 0:
                    return False
                children = action.child_classes
                if type(children) is not tuple or tuple(sorted(set(children))) != children:
                    return False
                if any(type(k) is not int or not 0 < k < i for k in children):
                    return False
        members: dict[tuple[int, int, int], int] = {}
        for member in certificate.memberships:
            fields = (member.task_index, member.world_mask, member.remaining_queries, member.class_id)
            if any(type(x) is not int for x in fields):
                return False
            t, mask, remaining, cid = fields
            if not 0 <= t < len(tasks) or not 0 <= cid < len(classes):
                return False
            task = tasks[t]
            if not 0 < mask < (1 << len(task.worlds)):
                return False
            if not 0 <= remaining < (1 << len(task.queries)):
                return False
            key = (t, mask, remaining)
            if key in members:
                return False
            members[key] = cid
        todo = []
        for t, task in enumerate(tasks):
            key = (t, (1 << len(task.worlds)) - 1, (1 << len(task.queries)) - 1)
            cid = certificate.root_classes[t]
            if type(cid) is not int or members.get(key) != cid:
                return False
            todo.append(key)
        seen = set()
        while todo:
            key = todo.pop()
            if key in seen:
                continue
            seen.add(key)
            t, mask, remaining = key
            task, cid = tasks[t], members[key]
            indices = tuple(i for i in range(len(task.worlds)) if mask & (1 << i))
            targets = {task.worlds[i].target for i in indices}
            if len(targets) == 1:
                if cid != 0:
                    return False
                continue
            if cid == 0:
                return False
            choices = set()
            for q, query in enumerate(task.queries):
                if not remaining & (1 << q):
                    continue
                unseen = set(indices)
                cells = []
                while unseen:
                    first = min(unseen)
                    cell = {j for j in unseen if query.outcomes[j] == query.outcomes[first]}
                    cells.append(cell)
                    unseen.difference_update(cell)
                if len(cells) == 1:
                    continue
                child_classes = set()
                for cell in cells:
                    if len({task.worlds[j].target for j in cell}) == 1:
                        continue
                    child_key = (t, sum(1 << j for j in cell), remaining & ~(1 << q))
                    if child_key not in members:
                        return False
                    child_classes.add(members[child_key])
                    todo.append(child_key)
                choices.add(ContinuationAction(query.cost, tuple(sorted(child_classes))))
            if tuple(sorted(choices)) != classes[cid].actions:
                return False
        return seen == set(members) and ({0} | set(members.values())) == set(range(len(classes)))
    except (AttributeError, TypeError, ValueError, IndexError, KeyError):
        return False


def _values(certificate: ContinuationQuotientCertificate) -> tuple[int | None, ...]:
    values: list[int | None] = [0]
    for cls in certificate.classes[1:]:
        candidates = []
        for action in cls.actions:
            children = [values[cid] for cid in action.child_classes]
            if any(value is None for value in children):
                continue
            candidates.append(action.cost + max(children, default=0))
        values.append(min(candidates) if candidates else None)
    return tuple(values)


def continuation_quotient_costs(
    tasks: Sequence[FiniteTask], certificate: ContinuationQuotientCertificate,
) -> tuple[int | None, ...]:
    """Evaluate class Bellman values only after structural verification."""
    if not verify_continuation_quotient(tasks, certificate):
        raise ValueError("invalid continuation quotient certificate")
    values = _values(certificate)
    return tuple(values[cid] for cid in certificate.root_classes)


def lift_continuation_policy(
    tasks: Sequence[FiniteTask], certificate: ContinuationQuotientCertificate,
    *, task_index: int = 0,
) -> LiftedContinuationPolicy:
    """Recover named queries and real outcome branches in one original task.

    Equal cost classes do NOT make named queries interchangeable across states.
    The local dictionary is reconstructed from original deterministic observations.
    Leaf targets are recovered from original worlds, not the generic terminal ID.
    """
    tasks = _tasks(tasks)
    if type(task_index) is not int or not 0 <= task_index < len(tasks):
        raise ValueError("task_index must select a declared task")
    if not verify_continuation_quotient(tasks, certificate):
        raise ValueError("invalid continuation quotient certificate")
    values = _values(certificate)
    root_cost = values[certificate.root_classes[task_index]]
    if root_cost is None:
        return LiftedContinuationPolicy(None, None, ())
    task = tasks[task_index]
    members = {
        (member.world_mask, member.remaining_queries): member.class_id
        for member in certificate.memberships if member.task_index == task_index
    }

    def optimal(worlds: int, remaining: int):
        choices = []
        for q, query in enumerate(task.queries):
            if not remaining & (1 << q):
                continue
            cells = _cells(task, worlds, q)
            if len(cells) == 1:
                continue
            child_costs = [
                values[members[(child, remaining & ~(1 << q))]]
                for child in cells.values() if not _pure(task, child)
            ]
            if any(cost is None for cost in child_costs):
                continue
            value = query.cost + max(child_costs, default=0)
            if value == values[members[(worlds, remaining)]]:
                choices.append(q)
        return tuple(choices)

    def lift(worlds: int, remaining: int) -> AdaptiveNode:
        support = tuple(w.name for i, w in enumerate(task.worlds) if worlds & (1 << i))
        if _pure(task, worlds):
            target = next(w.target for i, w in enumerate(task.worlds) if worlds & (1 << i))
            return AdaptiveNode(None, (), support, target)
        choices = optimal(worlds, remaining)
        if not choices:
            raise ArithmeticError("quotient choice has no valid local realization")
        q = choices[0]
        branches = tuple(
            (outcome, lift(child, remaining & ~(1 << q)))
            for outcome, child in _cells(task, worlds, q).items()
        )
        return AdaptiveNode(task.queries[q].name, branches, support, None)

    root_worlds = (1 << len(task.worlds)) - 1
    root_queries = (1 << len(task.queries)) - 1
    roots = () if _pure(task, root_worlds) else tuple(
        task.queries[q].name for q in optimal(root_worlds, root_queries)
    )
    return LiftedContinuationPolicy(root_cost, lift(root_worlds, root_queries), roots)
