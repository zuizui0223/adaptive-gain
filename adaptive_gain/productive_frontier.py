"""Productive-frontier hypergraph sufficient statistics for fixed resolution.

For every reachable mixed state s, let P_s be the set of physical queries that
are productive (nonconstant) on the represented worlds at s. A query already
used on the history to s is constant on the chosen outcome cell and remains
constant on every descendant, so P_s is also the set of all globally productive
queries at s.

A fixed bundle B resolves the target iff B intersects P_s for every reachable
mixed state. Therefore C_F is exactly the minimum-weight hitting set of the
reachable productive-set hypergraph. Inclusion-nonminimal productive sets are
redundant.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb

from .continuation_bisimulation import build_continuation_quotient, continuation_quotient_costs
from .core import FiniteTask, FixedResolutionReceipt, adaptive_minimum_resolution, fixed_minimum_resolution
from .state_resource_incidence import build_state_resource_incidence


@dataclass(frozen=True)
class ProductiveFrontierCertificate:
    query_names: tuple[str, ...]
    query_costs: tuple[int, ...]
    productive_sets: tuple[int, ...]
    minimal_productive_sets: tuple[int, ...]
    complete: bool = True
    scope: str = "reachable_mixed_state_productive_query_hypergraph"


@dataclass(frozen=True)
class ProductiveFrontierJointCostReceipt:
    adaptive_cost: int | None
    fixed_cost: int | None
    direct_adaptive_cost: int | None
    direct_fixed_cost: int | None
    exact_costs_agree: bool
    productive_set_count: int
    minimal_productive_set_count: int
    sperner_bound: int
    bound_holds: bool
    scope: str = "cost_only_continuation_plus_productive_frontier_joint_cost_audit"


def _minimal_sets(masks: tuple[int, ...]) -> tuple[int, ...]:
    keep = []
    for i, mask in enumerate(masks):
        if any(j != i and other & ~mask == 0 for j, other in enumerate(masks)):
            continue
        keep.append(mask)
    return tuple(sorted(keep))


def build_productive_frontier(task: FiniteTask) -> ProductiveFrontierCertificate:
    incidence = build_state_resource_incidence(task)
    productive = tuple(sorted({row.productive_queries for row in incidence.rows}))
    certificate = ProductiveFrontierCertificate(
        incidence.query_names,
        incidence.query_costs,
        productive,
        _minimal_sets(productive),
    )
    if not verify_productive_frontier(task, certificate):
        raise ArithmeticError("generated productive-frontier certificate failed verification")
    return certificate


def verify_productive_frontier(task: FiniteTask, certificate: ProductiveFrontierCertificate) -> bool:
    try:
        if not isinstance(task, FiniteTask) or not isinstance(certificate, ProductiveFrontierCertificate):
            return False
        if certificate.complete is not True:
            return False
        incidence = build_state_resource_incidence(task)
        expected = tuple(sorted({row.productive_queries for row in incidence.rows}))
        return (
            certificate.query_names == incidence.query_names
            and certificate.query_costs == incidence.query_costs
            and certificate.productive_sets == expected
            and certificate.minimal_productive_sets == _minimal_sets(expected)
        )
    except (AttributeError, TypeError, ValueError, ArithmeticError):
        return False


def bundle_resolves_from_productive_frontier(
    certificate: ProductiveFrontierCertificate,
    bundle: tuple[str, ...],
) -> bool:
    if not isinstance(certificate, ProductiveFrontierCertificate) or certificate.complete is not True:
        raise ValueError("certificate must be complete")
    lookup = {name: i for i, name in enumerate(certificate.query_names)}
    if len(set(bundle)) != len(bundle) or any(name not in lookup for name in bundle):
        raise ValueError("bundle must contain unique declared query names")
    mask = 0
    for name in bundle:
        mask |= 1 << lookup[name]
    return all(mask & productive for productive in certificate.minimal_productive_sets)


def productive_frontier_fixed_minimum_resolution(
    certificate: ProductiveFrontierCertificate,
) -> FixedResolutionReceipt:
    qn = len(certificate.query_names)
    if not certificate.productive_sets:
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


def productive_frontier_sperner_bound(query_count: int) -> int:
    if type(query_count) is not int or query_count < 0:
        raise ValueError("query_count must be a nonnegative integer")
    return comb(query_count, query_count // 2)


def productive_frontier_joint_cost_audit(task: FiniteTask) -> ProductiveFrontierJointCostReceipt:
    certificate = build_productive_frontier(task)
    continuation = build_continuation_quotient((task,))
    adaptive_cost = continuation_quotient_costs((task,), continuation)[0]
    fixed_cost = productive_frontier_fixed_minimum_resolution(certificate).minimum_cost
    direct_adaptive = adaptive_minimum_resolution(task).minimum_worst_path_cost
    direct_fixed = fixed_minimum_resolution(task).minimum_cost
    bound = productive_frontier_sperner_bound(len(task.queries))
    holds = len(certificate.minimal_productive_sets) <= bound
    return ProductiveFrontierJointCostReceipt(
        adaptive_cost,
        fixed_cost,
        direct_adaptive,
        direct_fixed,
        adaptive_cost == direct_adaptive and fixed_cost == direct_fixed,
        len(certificate.productive_sets),
        len(certificate.minimal_productive_sets),
        bound,
        holds,
    )
