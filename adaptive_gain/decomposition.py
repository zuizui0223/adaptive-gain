"""Exact cost decompositions for selected optimal adaptive resolution trees.

Let U be the cost of the UNION of query identities used anywhere in a selected
optimal adaptive policy.  Flattening that union is always a valid fixed resolving
bundle.  The original decomposition

    U - C_A = (C_F - C_A) + (U - C_F)

can be refined by inserting C_U, the cheapest fixed resolving subset restricted
to that selected policy union:

    U - C_A
    = (C_F - C_A) + (C_U - C_F) + (U - C_U).

The three right-hand discounts separate realized adaptive gain, external fixed
shortcuts, and redundancy already present inside the adaptive tree's query union.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import AdaptiveNode, FiniteTask, adaptive_minimum_resolution, fixed_minimum_resolution
from .pair_cover import private_pair_no_bypass_certificate, restricted_fixed_minimum_resolution


@dataclass(frozen=True)
class PolicyCostDecomposition:
    status: str
    adaptive_cost: int | None
    fixed_cost: int | None
    policy_union_cost: int | None
    policy_union_restricted_fixed_cost: int | None
    policy_union_queries: tuple[str, ...]
    branch_exclusive_overhead: int | None
    realized_adaptive_gain: int | None
    fixed_bypass_discount: int | None
    internal_union_redundancy: int | None
    external_shortcut_discount: int | None
    three_way_identity_holds: bool
    identity_holds: bool
    strict_gain_requires_positive_overhead: bool
    every_union_query_globally_mandatory: bool
    private_pair_no_bypass_certified: bool
    scope: str = "selected_optimal_deterministic_tree_positive_integer_query_costs"


def _policy_union_and_worst_path(task: FiniteTask, node: AdaptiveNode) -> tuple[set[str], int]:
    lookup = {q.name: q.cost for q in task.queries}

    def visit(current: AdaptiveNode, used_on_path: frozenset[str]) -> tuple[set[str], int]:
        if current.query is None:
            return set(), 0
        if current.query not in lookup:
            raise ValueError("policy contains an undeclared query")
        if current.query in used_on_path:
            raise ValueError("policy repeats a query on one path")
        union = {current.query}
        children = []
        for _, child in current.branches:
            child_union, child_cost = visit(child, used_on_path | {current.query})
            union.update(child_union)
            children.append(child_cost)
        if not children:
            raise ValueError("nonterminal policy node must have at least one branch")
        return union, lookup[current.query] + max(children)

    return visit(node, frozenset())


def optimal_policy_cost_decomposition(task: FiniteTask) -> PolicyCostDecomposition:
    """Decompose selected-tree branch overhead into gain and two bypass channels.

    Definitions:

    - C_A: minimum adaptive worst-path resolution cost;
    - C_F: global minimum fixed resolving-bundle cost;
    - U: cost of all distinct query identities used anywhere in the selected
      optimal adaptive tree;
    - C_U: minimum fixed resolving cost when restricted to that selected tree's
      query union.

    Class containment and set containment imply

        C_A <= C_F <= C_U <= U.

    Hence

        U - C_A
        = (C_F - C_A) + (C_U - C_F) + (U - C_U).

    We name the terms

        branch-exclusive overhead = U - C_A,
        realized adaptive gain     = C_F - C_A,
        external shortcut discount = C_U - C_F,
        internal union redundancy  = U - C_U.

    The older aggregate fixed-bypass discount remains U-C_F and therefore equals
    internal redundancy + external shortcut discount.
    """
    adaptive = adaptive_minimum_resolution(task)
    fixed = fixed_minimum_resolution(task)
    ca, cf = adaptive.minimum_worst_path_cost, fixed.minimum_cost
    if ca is None and cf is None:
        return PolicyCostDecomposition(
            "not_resolvable_by_declared_queries",
            None, None, None, None, (),
            None, None, None, None, None,
            True, True, True, False, False,
        )
    if ca is None or cf is None or adaptive.selected_policy is None:
        raise ArithmeticError("fixed/adaptive class containment was violated")

    union_names, policy_worst = _policy_union_and_worst_path(task, adaptive.selected_policy)
    if policy_worst != ca:
        raise ArithmeticError("selected adaptive policy does not attain reported minimum cost")
    order = {q.name: i for i, q in enumerate(task.queries)}
    names = tuple(sorted(union_names, key=order.__getitem__))
    union_cost = sum(task.queries[order[name]].cost for name in names)
    restricted = restricted_fixed_minimum_resolution(task, names)
    cu = restricted.minimum_cost
    if cu is None:
        raise ArithmeticError("selected policy union must resolve when flattened")
    if not ca <= cf <= cu <= union_cost:
        raise ArithmeticError("expected C_A <= C_F <= C_U <= policy union cost")

    overhead = union_cost - ca
    gain = cf - ca
    internal = union_cost - cu
    external = cu - cf
    bypass = union_cost - cf
    old_identity = overhead == gain + bypass
    three_way = overhead == gain + external + internal
    if not old_identity or not three_way or bypass != internal + external:
        raise ArithmeticError("policy cost decomposition identity failed")
    if gain > 0 and overhead <= 0:
        raise ArithmeticError("strict gain without branch-exclusive overhead")

    private = private_pair_no_bypass_certificate(task, names)
    if private.no_fixed_bypass_certified and cf != union_cost:
        raise ArithmeticError("private-pair certificate contradicted global fixed optimum")

    return PolicyCostDecomposition(
        "resolved_cost_decomposition",
        ca,
        cf,
        union_cost,
        cu,
        names,
        overhead,
        gain,
        bypass,
        internal,
        external,
        three_way,
        old_identity,
        gain == 0 or overhead > 0,
        private.every_union_query_globally_mandatory,
        private.no_fixed_bypass_certified,
    )
