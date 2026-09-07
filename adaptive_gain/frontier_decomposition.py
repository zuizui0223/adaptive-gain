"""Productive-frontier form of the adaptive/fixed cost decomposition.

The reachable productive-query frontier is sufficient for the fixed comparator:
``C_F`` is the minimum-weight hitting set of its inclusion-minimal edges.  For a
selected optimal adaptive policy with query union ``S``, the restricted fixed
cost ``C_U`` is the minimum-weight hitting set constrained to ``B subseteq S``.

Consequently the existing three-way decomposition can be computed without world
pairs or fixed-side child wiring:

    c(S) - C_A
      = [tau(H) - C_A]
      + [tau(H; S) - tau(H)]
      + [c(S) - tau(H; S)].

The three right-hand terms are realized adaptive gain, external shortcut
discount, and internal union redundancy respectively.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import FiniteTask
from .decomposition import optimal_policy_cost_decomposition
from .productive_frontier import (
    ProductiveFrontierCertificate,
    build_productive_frontier,
    productive_frontier_fixed_minimum_resolution,
)


@dataclass(frozen=True)
class ProductiveFrontierPolicyDecomposition:
    status: str
    adaptive_cost: int | None
    fixed_cost: int | None
    policy_union_cost: int | None
    policy_union_restricted_fixed_cost: int | None
    policy_union_queries: tuple[str, ...]
    branch_exclusive_overhead: int | None
    realized_adaptive_gain: int | None
    internal_union_redundancy: int | None
    external_shortcut_discount: int | None
    frontier_edge_count: int
    three_way_identity_holds: bool
    agrees_with_direct_decomposition: bool
    scope: str = "selected_optimal_policy_productive_frontier_hitting_set_decomposition"


def _restricted_frontier_minimum(
    certificate: ProductiveFrontierCertificate,
    allowed_queries: tuple[str, ...],
) -> int | None:
    lookup = {name: i for i, name in enumerate(certificate.query_names)}
    if len(set(allowed_queries)) != len(allowed_queries):
        raise ValueError("allowed_queries must be unique")
    if any(name not in lookup for name in allowed_queries):
        raise ValueError("allowed_queries must be declared query names")
    allowed_mask = 0
    for name in allowed_queries:
        allowed_mask |= 1 << lookup[name]
    if not certificate.productive_sets:
        return 0

    qn = len(certificate.query_names)
    best: int | None = None
    for subset in range(1 << qn):
        if subset & ~allowed_mask:
            continue
        cost = sum(
            certificate.query_costs[q]
            for q in range(qn)
            if subset & (1 << q)
        )
        if best is not None and cost >= best:
            continue
        if all(subset & edge for edge in certificate.minimal_productive_sets):
            best = cost
    return best


def productive_frontier_policy_decomposition(
    task: FiniteTask,
) -> ProductiveFrontierPolicyDecomposition:
    """Recompute the selected-policy three-way decomposition from the frontier."""
    direct = optimal_policy_cost_decomposition(task)
    frontier = build_productive_frontier(task)
    edge_count = len(frontier.minimal_productive_sets)

    if direct.status == "not_resolvable_by_declared_queries":
        return ProductiveFrontierPolicyDecomposition(
            direct.status,
            None,
            None,
            None,
            None,
            (),
            None,
            None,
            None,
            None,
            edge_count,
            True,
            True,
        )

    ca = direct.adaptive_cost
    if ca is None or direct.policy_union_cost is None:
        raise ArithmeticError("resolved decomposition lost adaptive or union cost")

    cf = productive_frontier_fixed_minimum_resolution(frontier).minimum_cost
    cu = _restricted_frontier_minimum(frontier, direct.policy_union_queries)
    if cf is None or cu is None:
        raise ArithmeticError("flattened adaptive policy union must hit every productive frontier edge")

    union_cost = direct.policy_union_cost
    if not ca <= cf <= cu <= union_cost:
        raise ArithmeticError("expected C_A <= C_F <= C_U <= union cost")

    overhead = union_cost - ca
    gain = cf - ca
    external = cu - cf
    internal = union_cost - cu
    identity = overhead == gain + external + internal
    agrees = (
        cf == direct.fixed_cost
        and cu == direct.policy_union_restricted_fixed_cost
        and overhead == direct.branch_exclusive_overhead
        and gain == direct.realized_adaptive_gain
        and external == direct.external_shortcut_discount
        and internal == direct.internal_union_redundancy
        and identity
    )
    if not agrees:
        raise ArithmeticError("productive-frontier decomposition disagreed with direct decomposition")

    return ProductiveFrontierPolicyDecomposition(
        direct.status,
        ca,
        cf,
        union_cost,
        cu,
        direct.policy_union_queries,
        overhead,
        gain,
        internal,
        external,
        edge_count,
        identity,
        agrees,
    )
