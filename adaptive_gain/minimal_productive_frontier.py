"""Static minimal productive-frontier certificates from cross-target pair incidence.

The productive-frontier / pair-separator equivalence implies that fixed scalar
resolution never needs reachable-state enumeration once the full task table is
available.  The inclusion-minimal productive frontier is exactly the
inclusion-minimal set of cross-target pair separator masks.

This module deliberately stores only the minimal frontier needed for C_F.  It is
therefore smaller than ProductiveFrontierCertificate, whose ``productive_sets``
field records all reachable productive sets for audit/provenance purposes.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import FiniteTask, FixedResolutionReceipt, fixed_minimum_resolution
from .productive_pair_equivalence import minimal_cross_target_separator_sets


@dataclass(frozen=True)
class MinimalProductiveFrontierCertificate:
    query_names: tuple[str, ...]
    query_costs: tuple[int, ...]
    minimal_productive_sets: tuple[int, ...]
    complete: bool = True
    source: str = "cross_target_pair_incidence"
    scope: str = "static_minimal_productive_frontier_for_fixed_scalar_resolution"


@dataclass(frozen=True)
class StaticFrontierFixedCostReceipt:
    fixed_cost: int | None
    direct_fixed_cost: int | None
    exact_cost_agrees: bool
    minimal_edge_count: int
    reachable_state_enumeration_used: bool = False
    scope: str = "static_pair_incidence_minimal_frontier_fixed_cost_audit"


def build_minimal_productive_frontier_from_pair_incidence(
    task: FiniteTask,
) -> MinimalProductiveFrontierCertificate:
    if not isinstance(task, FiniteTask):
        raise ValueError("task must be a FiniteTask")
    certificate = MinimalProductiveFrontierCertificate(
        tuple(query.name for query in task.queries),
        tuple(query.cost for query in task.queries),
        minimal_cross_target_separator_sets(task),
    )
    if not verify_minimal_productive_frontier_from_pair_incidence(task, certificate):
        raise ArithmeticError("static minimal productive frontier failed verification")
    return certificate


def verify_minimal_productive_frontier_from_pair_incidence(
    task: FiniteTask,
    certificate: MinimalProductiveFrontierCertificate,
) -> bool:
    try:
        if not isinstance(task, FiniteTask):
            return False
        if not isinstance(certificate, MinimalProductiveFrontierCertificate):
            return False
        if certificate.complete is not True:
            return False
        if certificate.source != "cross_target_pair_incidence":
            return False
        if certificate.query_names != tuple(query.name for query in task.queries):
            return False
        if certificate.query_costs != tuple(query.cost for query in task.queries):
            return False
        limit = 1 << len(task.queries)
        if any(type(edge) is not int or not 0 <= edge < limit for edge in certificate.minimal_productive_sets):
            return False
        expected = minimal_cross_target_separator_sets(task)
        return certificate.minimal_productive_sets == expected
    except (AttributeError, TypeError, ValueError, ArithmeticError):
        return False


def bundle_resolves_from_minimal_productive_frontier(
    certificate: MinimalProductiveFrontierCertificate,
    bundle: tuple[str, ...],
) -> bool:
    if not isinstance(certificate, MinimalProductiveFrontierCertificate) or certificate.complete is not True:
        raise ValueError("certificate must be complete")
    lookup = {name: i for i, name in enumerate(certificate.query_names)}
    if len(set(bundle)) != len(bundle) or any(name not in lookup for name in bundle):
        raise ValueError("bundle must contain unique declared query names")
    mask = 0
    for name in bundle:
        mask |= 1 << lookup[name]
    return all(mask & edge for edge in certificate.minimal_productive_sets)


def minimal_frontier_fixed_minimum_resolution(
    certificate: MinimalProductiveFrontierCertificate,
) -> FixedResolutionReceipt:
    if not isinstance(certificate, MinimalProductiveFrontierCertificate) or certificate.complete is not True:
        raise ValueError("certificate must be complete")
    qn = len(certificate.query_names)
    if not certificate.minimal_productive_sets:
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
        if all(subset & edge for edge in certificate.minimal_productive_sets):
            bundle = tuple(
                certificate.query_names[q]
                for q in range(qn)
                if subset & (1 << q)
            )
            if best is None or cost < best:
                best, bundles = cost, [bundle]
            elif cost == best:
                bundles.append(bundle)
    return FixedResolutionReceipt(best, tuple(bundles), False)


def static_minimal_frontier_fixed_cost_audit(
    task: FiniteTask,
) -> StaticFrontierFixedCostReceipt:
    certificate = build_minimal_productive_frontier_from_pair_incidence(task)
    fixed = minimal_frontier_fixed_minimum_resolution(certificate).minimum_cost
    direct = fixed_minimum_resolution(task).minimum_cost
    if fixed != direct:
        raise ArithmeticError("static minimal frontier disagreed with direct fixed optimum")
    return StaticFrontierFixedCostReceipt(
        fixed,
        direct,
        True,
        len(certificate.minimal_productive_sets),
        False,
    )
