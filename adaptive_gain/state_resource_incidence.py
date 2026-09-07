"""State-resource incidence sufficient statistics for deterministic fixed resolution.

For a reachable mixed state s, let

* U_s be the set of query resources already consumed on the history to s; and
* P_s be the set of still-available queries that are productive (nonconstant)
  on the represented worlds remaining at s.

A fixed bundle B fails to resolve the target iff there exists a reachable mixed
state s with U_s subseteq B and P_s intersect B empty.  Therefore the multiset of
concrete child transitions is unnecessary for C_F: the query costs together with
the unique (U_s, P_s) rows determine the exact fixed optimum.

Combining this fixed-side statistic with the existing cost-only continuation
quotient gives a joint representation sufficient for (C_A, C_F) without retaining
resource-labelled child wiring.
"""
from __future__ import annotations

from dataclasses import dataclass

from .continuation_bisimulation import (
    build_continuation_quotient,
    continuation_quotient_costs,
)
from .core import FiniteTask, FixedResolutionReceipt, adaptive_minimum_resolution, fixed_minimum_resolution


@dataclass(frozen=True, order=True)
class StateResourceIncidenceRow:
    unavailable_queries: int
    productive_queries: int


@dataclass(frozen=True)
class StateResourceIncidenceCertificate:
    query_names: tuple[str, ...]
    query_costs: tuple[int, ...]
    rows: tuple[StateResourceIncidenceRow, ...]
    reduced_rows: tuple[StateResourceIncidenceRow, ...]
    complete: bool = True
    scope: str = "finite_deterministic_reachable_mixed_state_unavailable_productive_incidence"


@dataclass(frozen=True)
class StateResourceJointCostReceipt:
    adaptive_cost: int | None
    fixed_cost: int | None
    direct_adaptive_cost: int | None
    direct_fixed_cost: int | None
    adaptive_cost_agrees: bool
    fixed_cost_agrees: bool
    exact_costs_agree: bool
    row_count: int
    reduced_row_count: int
    scope: str = "cost_only_continuation_plus_state_resource_incidence_joint_cost_audit"


def _pure(task: FiniteTask, world_mask: int) -> bool:
    return len({
        task.worlds[i].target
        for i in range(len(task.worlds))
        if world_mask & (1 << i)
    }) <= 1


def _cells(task: FiniteTask, world_mask: int, query_index: int) -> tuple[int, ...]:
    cells: dict[object, int] = {}
    query = task.queries[query_index]
    for i, outcome in enumerate(query.outcomes):
        if world_mask & (1 << i):
            cells[outcome] = cells.get(outcome, 0) | (1 << i)
    return tuple(cells.values())


def _reduced_rows(rows: tuple[StateResourceIncidenceRow, ...]) -> tuple[StateResourceIncidenceRow, ...]:
    """Delete failure conditions implied by a stronger row.

    Row a makes row b redundant when U_a subseteq U_b and P_a subseteq P_b,
    because every bundle failing b also fails a.
    """
    keep = []
    for i, row in enumerate(rows):
        redundant = False
        for j, other in enumerate(rows):
            if i == j:
                continue
            if (
                other.unavailable_queries & ~row.unavailable_queries == 0
                and other.productive_queries & ~row.productive_queries == 0
            ):
                redundant = True
                break
        if not redundant:
            keep.append(row)
    return tuple(sorted(keep))


def build_state_resource_incidence(task: FiniteTask) -> StateResourceIncidenceCertificate:
    if not isinstance(task, FiniteTask):
        raise ValueError("task must be a FiniteTask")
    n = len(task.worlds)
    qn = len(task.queries)
    all_queries = (1 << qn) - 1
    seen: set[tuple[int, int]] = set()
    rows: set[StateResourceIncidenceRow] = set()

    def visit(world_mask: int, remaining_queries: int) -> None:
        key = (world_mask, remaining_queries)
        if key in seen:
            return
        seen.add(key)
        if _pure(task, world_mask):
            return
        productive = 0
        child_rows = []
        for q in range(qn):
            bit = 1 << q
            if not (remaining_queries & bit):
                continue
            cells = _cells(task, world_mask, q)
            if len(cells) <= 1:
                continue
            productive |= bit
            child_rows.append((q, cells))
        rows.add(StateResourceIncidenceRow(all_queries ^ remaining_queries, productive))
        for q, cells in child_rows:
            next_remaining = remaining_queries & ~(1 << q)
            for child in cells:
                if not _pure(task, child):
                    visit(child, next_remaining)

    visit((1 << n) - 1, all_queries)
    ordered = tuple(sorted(rows))
    certificate = StateResourceIncidenceCertificate(
        tuple(query.name for query in task.queries),
        tuple(query.cost for query in task.queries),
        ordered,
        _reduced_rows(ordered),
    )
    if not verify_state_resource_incidence(task, certificate):
        raise ArithmeticError("generated state-resource incidence certificate failed verification")
    return certificate


def verify_state_resource_incidence(
    task: FiniteTask,
    certificate: StateResourceIncidenceCertificate,
) -> bool:
    """Independently reconstruct every reachable mixed-state (U,P) row."""
    try:
        if not isinstance(task, FiniteTask) or not isinstance(certificate, StateResourceIncidenceCertificate):
            return False
        if certificate.complete is not True:
            return False
        if certificate.query_names != tuple(query.name for query in task.queries):
            return False
        if certificate.query_costs != tuple(query.cost for query in task.queries):
            return False
        qn = len(task.queries)
        limit = 1 << qn
        for row in certificate.rows:
            if (
                type(row.unavailable_queries) is not int
                or type(row.productive_queries) is not int
                or not 0 <= row.unavailable_queries < limit
                or not 0 <= row.productive_queries < limit
                or row.unavailable_queries & row.productive_queries
            ):
                return False
        n = len(task.worlds)
        all_queries = limit - 1
        seen: set[tuple[int, int]] = set()
        rebuilt: set[StateResourceIncidenceRow] = set()

        def target_pure(mask: int) -> bool:
            values = {
                task.worlds[i].target
                for i in range(n)
                if mask & (1 << i)
            }
            return len(values) <= 1

        def partition(mask: int, q: int) -> tuple[int, ...]:
            indices = [i for i in range(n) if mask & (1 << i)]
            groups = []
            unused = set(indices)
            while unused:
                first = min(unused)
                cell = {
                    i for i in unused
                    if task.queries[q].outcomes[i] == task.queries[q].outcomes[first]
                }
                groups.append(sum(1 << i for i in cell))
                unused.difference_update(cell)
            return tuple(groups)

        def walk(mask: int, remaining: int) -> None:
            key = (mask, remaining)
            if key in seen:
                return
            seen.add(key)
            if target_pure(mask):
                return
            productive = 0
            children = []
            for q in range(qn):
                bit = 1 << q
                if not (remaining & bit):
                    continue
                cells = partition(mask, q)
                if len(cells) <= 1:
                    continue
                productive |= bit
                children.append((q, cells))
            rebuilt.add(StateResourceIncidenceRow(all_queries ^ remaining, productive))
            for q, cells in children:
                next_remaining = remaining & ~(1 << q)
                for child in cells:
                    if not target_pure(child):
                        walk(child, next_remaining)

        walk((1 << n) - 1, all_queries)
        ordered = tuple(sorted(rebuilt))
        return (
            certificate.rows == ordered
            and certificate.reduced_rows == _reduced_rows(ordered)
        )
    except (AttributeError, TypeError, ValueError, IndexError, KeyError):
        return False


def _bundle_mask(certificate: StateResourceIncidenceCertificate, bundle: tuple[str, ...]) -> int:
    lookup = {name: i for i, name in enumerate(certificate.query_names)}
    if len(set(bundle)) != len(bundle) or any(name not in lookup for name in bundle):
        raise ValueError("bundle must contain unique declared query names")
    mask = 0
    for name in bundle:
        mask |= 1 << lookup[name]
    return mask


def bundle_resolves_from_state_resource_incidence(
    certificate: StateResourceIncidenceCertificate,
    bundle: tuple[str, ...],
) -> bool:
    if not isinstance(certificate, StateResourceIncidenceCertificate) or certificate.complete is not True:
        raise ValueError("certificate must be a complete StateResourceIncidenceCertificate")
    bundle_mask = _bundle_mask(certificate, bundle)
    for row in certificate.reduced_rows:
        if (
            row.unavailable_queries & ~bundle_mask == 0
            and row.productive_queries & bundle_mask == 0
        ):
            return False
    return True


def state_resource_fixed_minimum_resolution(
    certificate: StateResourceIncidenceCertificate,
) -> FixedResolutionReceipt:
    qn = len(certificate.query_names)
    if not certificate.rows:
        return FixedResolutionReceipt(0, ((),), True)
    best: int | None = None
    bundles: list[tuple[str, ...]] = []
    for subset in range(1 << qn):
        cost = sum(
            certificate.query_costs[q]
            for q in range(qn)
            if subset & (1 << q)
        )
        if best is not None and cost > best:
            continue
        bundle = tuple(
            certificate.query_names[q]
            for q in range(qn)
            if subset & (1 << q)
        )
        if bundle_resolves_from_state_resource_incidence(certificate, bundle):
            if best is None or cost < best:
                best, bundles = cost, [bundle]
            elif cost == best:
                bundles.append(bundle)
    return FixedResolutionReceipt(best, tuple(bundles), False)


def state_resource_joint_cost_audit(task: FiniteTask) -> StateResourceJointCostReceipt:
    incidence = build_state_resource_incidence(task)
    continuation = build_continuation_quotient((task,))
    adaptive_cost = continuation_quotient_costs((task,), continuation)[0]
    fixed_cost = state_resource_fixed_minimum_resolution(incidence).minimum_cost
    direct_adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    direct_fixed = fixed_minimum_resolution(task).minimum_cost
    return StateResourceJointCostReceipt(
        adaptive_cost,
        fixed_cost,
        direct_adaptive,
        direct_fixed,
        adaptive_cost == direct_adaptive,
        fixed_cost == direct_fixed,
        adaptive_cost == direct_adaptive and fixed_cost == direct_fixed,
        len(incidence.rows),
        len(incidence.reduced_rows),
    )
