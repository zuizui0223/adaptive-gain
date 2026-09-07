"""Minimal-transversal structure behind internal and external fixed bypass.

For a productive-frontier hypergraph H, inclusion-minimal hitting sets
(transversals) are sufficient to recover every positive-cost fixed optimum.
For one selected optimal adaptive policy with query union S,

    C_F = min_{T in Tr(H)} c(T)
    C_U = min_{T in Tr(H), T subseteq S} c(T).

Thus internal redundancy and external shortcut discount have exact structural
interpretations in the transversal family.  Enumeration here is deliberately
small-state and fail-closed behind a subset cap; it is a structural verifier, not
an assertion of scalable hypergraph dualization.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import AdaptiveNode, FiniteTask, adaptive_minimum_resolution
from .frontier_decomposition import productive_frontier_policy_decomposition
from .productive_frontier import ProductiveFrontierCertificate, build_productive_frontier


class FrontierTransversalLimitError(RuntimeError):
    """Exact subset enumeration exceeded the declared cap."""


@dataclass(frozen=True)
class MinimalTransversalCertificate:
    query_names: tuple[str, ...]
    query_costs: tuple[int, ...]
    frontier_edges: tuple[int, ...]
    transversal_masks: tuple[int, ...]
    subsets_examined: int
    complete: bool = True
    scope: str = "exact_inclusion_minimal_transversals_of_productive_frontier"


@dataclass(frozen=True)
class FrontierTransversalPolicyDecomposition:
    status: str
    adaptive_cost: int | None
    fixed_cost: int | None
    policy_union_restricted_fixed_cost: int | None
    policy_union_cost: int | None
    policy_union_queries: tuple[str, ...]
    minimal_transversal_count: int
    global_optimal_transversals: tuple[tuple[str, ...], ...]
    restricted_optimal_transversals: tuple[tuple[str, ...], ...]
    branch_exclusive_overhead: int | None
    realized_adaptive_gain: int | None
    external_shortcut_discount: int | None
    internal_union_redundancy: int | None
    union_is_minimal_transversal: bool
    every_union_query_has_private_frontier_edge: bool
    internal_zero_certificate_exact: bool
    outside_cheaper_transversal_exists: bool
    three_way_identity_holds: bool
    agrees_with_frontier_decomposition: bool
    scope: str = "selected_policy_minimal_transversal_bypass_decomposition"


def _hits_all(mask: int, edges: tuple[int, ...]) -> bool:
    return all(mask & edge for edge in edges)


def _enumerate_minimal_transversals_unverified(
    certificate: ProductiveFrontierCertificate,
    *,
    max_subsets: int,
) -> MinimalTransversalCertificate:
    if not isinstance(certificate, ProductiveFrontierCertificate) or certificate.complete is not True:
        raise ValueError("certificate must be a complete ProductiveFrontierCertificate")
    if type(max_subsets) is not int or max_subsets < 1:
        raise ValueError("max_subsets must be a positive integer")
    qn = len(certificate.query_names)
    total = 1 << qn
    if total > max_subsets:
        raise FrontierTransversalLimitError(
            f"exact transversal enumeration needs {total} subsets, exceeding cap {max_subsets}"
        )
    edges = certificate.minimal_productive_sets
    if any(type(edge) is not int or edge < 0 or edge >= total for edge in edges):
        raise ValueError("frontier edge mask is outside the declared query universe")

    minimal: list[int] = []
    examined = 0
    # Cardinality order ensures any already-retained subset is a genuine smaller
    # transversal and makes inclusion-minimality checking cheap and exact.
    order = sorted(range(total), key=lambda mask: (mask.bit_count(), mask))
    for mask in order:
        examined += 1
        if any(previous & ~mask == 0 for previous in minimal):
            continue
        if _hits_all(mask, edges):
            minimal.append(mask)
    return MinimalTransversalCertificate(
        certificate.query_names,
        certificate.query_costs,
        edges,
        tuple(sorted(minimal)),
        examined,
        True,
    )


def enumerate_minimal_transversals(
    certificate: ProductiveFrontierCertificate,
    *,
    max_subsets: int = 1_000_000,
) -> MinimalTransversalCertificate:
    result = _enumerate_minimal_transversals_unverified(certificate, max_subsets=max_subsets)
    if not verify_minimal_transversal_certificate(certificate, result, max_subsets=max_subsets):
        raise ArithmeticError("generated minimal-transversal certificate failed verification")
    return result


def verify_minimal_transversal_certificate(
    frontier: ProductiveFrontierCertificate,
    certificate: MinimalTransversalCertificate,
    *,
    max_subsets: int = 1_000_000,
) -> bool:
    """Independently re-enumerate the bounded subset family and compare exactly."""
    try:
        if not isinstance(certificate, MinimalTransversalCertificate) or certificate.complete is not True:
            return False
        rebuilt = _enumerate_minimal_transversals_unverified(frontier, max_subsets=max_subsets)
        return rebuilt == certificate
    except (AttributeError, TypeError, ValueError, ArithmeticError, FrontierTransversalLimitError):
        return False


def _policy_union(task: FiniteTask, node: AdaptiveNode | None) -> tuple[tuple[str, ...], int]:
    if node is None:
        return (), 0
    costs = {query.name: query.cost for query in task.queries}
    order = {query.name: i for i, query in enumerate(task.queries)}

    def visit(current: AdaptiveNode, used: frozenset[str]) -> set[str]:
        if current.query is None:
            return set()
        if current.query not in costs:
            raise ValueError("policy contains an undeclared query")
        if current.query in used:
            raise ValueError("policy repeats a query on one path")
        union = {current.query}
        for _, child in current.branches:
            union.update(visit(child, used | {current.query}))
        return union

    names_set = visit(node, frozenset())
    names = tuple(sorted(names_set, key=order.__getitem__))
    return names, sum(costs[name] for name in names)


def _cost(mask: int, query_costs: tuple[int, ...]) -> int:
    return sum(cost for q, cost in enumerate(query_costs) if mask & (1 << q))


def _names(mask: int, query_names: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(name for q, name in enumerate(query_names) if mask & (1 << q))


def frontier_transversal_policy_decomposition(
    task: FiniteTask,
    *,
    max_subsets: int = 1_000_000,
) -> FrontierTransversalPolicyDecomposition:
    """Recover the selected-policy decomposition from minimal frontier transversals."""
    adaptive = adaptive_minimum_resolution(task)
    frontier = build_productive_frontier(task)
    trans = enumerate_minimal_transversals(frontier, max_subsets=max_subsets)
    reference = productive_frontier_policy_decomposition(task)

    ca = adaptive.minimum_worst_path_cost
    if ca is None:
        return FrontierTransversalPolicyDecomposition(
            "not_resolvable_by_declared_queries",
            None, None, None, None, (),
            len(trans.transversal_masks), (), (),
            None, None, None, None,
            False, False, True, False, True,
            reference.status == "not_resolvable_by_declared_queries",
        )

    union_names, union_cost = _policy_union(task, adaptive.selected_policy)
    lookup = {name: i for i, name in enumerate(frontier.query_names)}
    union_mask = 0
    for name in union_names:
        union_mask |= 1 << lookup[name]

    masks = trans.transversal_masks
    if not masks:
        raise ArithmeticError("resolved task must have at least one frontier transversal")
    costs = {mask: _cost(mask, frontier.query_costs) for mask in masks}
    cf = min(costs.values())
    global_opt = tuple(mask for mask in masks if costs[mask] == cf)
    inside = tuple(mask for mask in masks if mask & ~union_mask == 0)
    if not inside:
        raise ArithmeticError("flattened selected adaptive policy union must contain a frontier transversal")
    cu = min(costs[mask] for mask in inside)
    restricted_opt = tuple(mask for mask in inside if costs[mask] == cu)

    overhead = union_cost - ca
    gain = cf - ca
    external = cu - cf
    internal = union_cost - cu
    identity = overhead == gain + external + internal

    union_minimal = union_mask in masks
    private = all(
        any((edge & union_mask) == (1 << q) for edge in frontier.minimal_productive_sets)
        for q in range(len(frontier.query_names))
        if union_mask & (1 << q)
    )
    # For a hitting set S, inclusion-minimality is equivalent to every member
    # having a private edge relative to S.  With positive costs this is also
    # equivalent to zero internal cost redundancy.
    internal_zero_exact = (
        union_minimal == private == (internal == 0)
    )
    outside_cheaper = any(
        costs[mask] < cu and mask & ~union_mask
        for mask in masks
    )
    if outside_cheaper != (external > 0):
        raise ArithmeticError("external shortcut witness disagreed with scalar discount")

    agrees = (
        reference.adaptive_cost == ca
        and reference.fixed_cost == cf
        and reference.policy_union_restricted_fixed_cost == cu
        and reference.policy_union_cost == union_cost
        and reference.branch_exclusive_overhead == overhead
        and reference.realized_adaptive_gain == gain
        and reference.external_shortcut_discount == external
        and reference.internal_union_redundancy == internal
        and reference.three_way_identity_holds == identity
    )
    if not identity or not internal_zero_exact or not agrees:
        raise ArithmeticError("minimal-transversal decomposition failed exact consistency checks")

    return FrontierTransversalPolicyDecomposition(
        reference.status,
        ca,
        cf,
        cu,
        union_cost,
        union_names,
        len(masks),
        tuple(_names(mask, frontier.query_names) for mask in global_opt),
        tuple(_names(mask, frontier.query_names) for mask in restricted_opt),
        overhead,
        gain,
        external,
        internal,
        union_minimal,
        private,
        internal_zero_exact,
        outside_cheaper,
        identity,
        agrees,
    )
