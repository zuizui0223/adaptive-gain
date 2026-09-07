"""Target-specific pair-cover structure for fixed-resolution bypass analysis.

For guaranteed target resolution, a fixed bundle need only separate world pairs
whose target labels differ.  This module exposes that pair-separation hypergraph,
restricted fixed optima, and a strong private-pair certificate showing that a
query is globally mandatory for every fixed resolving bundle.

The construction is a target-specific analogue of the classical Test Cover
view: each query covers the cross-target pairs it separates.  No claim of a new
general set-cover algorithm is made here.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Sequence

from .core import (
    AdaptiveNode,
    FiniteTask,
    FixedResolutionReceipt,
    adaptive_minimum_resolution,
    bundle_resolves,
)


@dataclass(frozen=True)
class PairSeparatorRow:
    world_pair: tuple[str, str]
    separator_queries: tuple[str, ...]


@dataclass(frozen=True)
class EssentialQueryWitness:
    query: str
    private_world_pair: tuple[str, str]


@dataclass(frozen=True)
class PairCoverAudit:
    cross_target_pair_count: int
    rows: tuple[PairSeparatorRow, ...]
    all_cross_target_pairs_separable: bool
    globally_essential_queries: tuple[str, ...]
    essential_witnesses: tuple[EssentialQueryWitness, ...]
    scope: str = "declared_finite_worlds_cross_target_pair_separation_hypergraph"


@dataclass(frozen=True)
class PrivatePairNoBypassCertificate:
    policy_union_queries: tuple[str, ...]
    globally_essential_union_queries: tuple[str, ...]
    missing_private_pair_queries: tuple[str, ...]
    every_union_query_globally_mandatory: bool
    union_resolves_target: bool
    no_fixed_bypass_certified: bool
    interpretation: str
    scope: str = "sufficient_private_pair_certificate_not_necessary_for_no_bypass"


@dataclass(frozen=True)
class PrivatePairAdaptiveGainCertificate:
    status: str
    adaptive_cost: int | None
    policy_union_cost: int | None
    policy_union_queries: tuple[str, ...]
    branch_exclusive_overhead: int | None
    every_union_query_globally_mandatory: bool
    globally_essential_union_queries: tuple[str, ...]
    missing_private_pair_queries: tuple[str, ...]
    strict_adaptive_gain_certified_without_fixed_optimization: bool
    interpretation: str
    scope: str = "selected_optimal_tree_private_pair_sufficient_certificate"


def _cross_target_pairs(task: FiniteTask):
    return tuple(
        (i, j)
        for i, j in combinations(range(len(task.worlds)), 2)
        if task.worlds[i].target != task.worlds[j].target
    )


def pair_cover_audit(task: FiniteTask) -> PairCoverAudit:
    """Return the exact cross-target pair-separation hypergraph.

    A query separates pair (i,j) when the declared deterministic outcomes differ.
    If one query is the ONLY declared separator of a cross-target pair, that query
    is globally mandatory for every fixed resolving bundle.  We call that pair a
    private-pair witness for the query.
    """
    pairs = _cross_target_pairs(task)
    rows = []
    private: dict[str, tuple[str, str]] = {}
    for i, j in pairs:
        separators = tuple(
            query.name
            for query in task.queries
            if query.outcomes[i] != query.outcomes[j]
        )
        pair = (task.worlds[i].name, task.worlds[j].name)
        rows.append(PairSeparatorRow(pair, separators))
        if len(separators) == 1 and separators[0] not in private:
            private[separators[0]] = pair
    order = {query.name: k for k, query in enumerate(task.queries)}
    essential = tuple(sorted(private, key=order.__getitem__))
    witnesses = tuple(EssentialQueryWitness(name, private[name]) for name in essential)
    return PairCoverAudit(
        len(pairs),
        tuple(rows),
        all(bool(row.separator_queries) for row in rows),
        essential,
        witnesses,
    )


def restricted_fixed_minimum_resolution(
    task: FiniteTask,
    allowed_queries: Sequence[str],
) -> FixedResolutionReceipt:
    """Exact fixed optimum constrained to an explicit subset of query identities."""
    names = tuple(allowed_queries)
    lookup = {query.name: query for query in task.queries}
    if len(set(names)) != len(names) or any(name not in lookup for name in names):
        raise ValueError("allowed_queries must contain unique declared query names")
    if len({world.target for world in task.worlds}) == 1:
        return FixedResolutionReceipt(0, ((),), True)

    best: int | None = None
    bundles: list[tuple[str, ...]] = []
    for subset in range(1 << len(names)):
        bundle = tuple(names[j] for j in range(len(names)) if subset & (1 << j))
        cost = sum(lookup[name].cost for name in bundle)
        if best is not None and cost > best:
            continue
        if bundle_resolves(task, bundle):
            if best is None or cost < best:
                best, bundles = cost, [bundle]
            elif cost == best:
                bundles.append(bundle)
    return FixedResolutionReceipt(best, tuple(bundles), False)


def private_pair_no_bypass_certificate(
    task: FiniteTask,
    policy_union_queries: Sequence[str],
) -> PrivatePairNoBypassCertificate:
    """Strong structural certificate that a resolving union has no fixed bypass.

    If every query in a resolving policy union has a cross-target pair for which
    it is the only separator in the ENTIRE declared vocabulary, every fixed
    resolving bundle must buy every union query.  Since the union itself resolves,
    its cost is then the global fixed optimum.

    Failure of this certificate does NOT imply a bypass exists; global essentiality
    is sufficient, not necessary, for fixed optimality of the union.
    """
    names = tuple(policy_union_queries)
    lookup = {query.name for query in task.queries}
    if len(set(names)) != len(names) or any(name not in lookup for name in names):
        raise ValueError("policy_union_queries must contain unique declared query names")
    audit = pair_cover_audit(task)
    essential = set(audit.globally_essential_queries)
    present = tuple(name for name in names if name in essential)
    missing = tuple(name for name in names if name not in essential)
    union_resolves = bundle_resolves(task, names)
    all_mandatory = bool(names) and not missing
    certified = union_resolves and all_mandatory
    return PrivatePairNoBypassCertificate(
        names,
        present,
        missing,
        all_mandatory,
        union_resolves,
        certified,
        (
            "every union query has a globally private cross-target pair; every fixed resolving bundle must buy the full union"
            if certified
            else "private-pair certificate incomplete; exact fixed optimization is still needed"
        ),
    )


def _policy_union(task: FiniteTask, node: AdaptiveNode) -> tuple[tuple[str, ...], int]:
    costs = {query.name: query.cost for query in task.queries}
    seen = set()

    def visit(current: AdaptiveNode, path: frozenset[str]) -> int:
        if current.query is None:
            return 0
        if current.query in path:
            raise ValueError("selected policy repeats a query on one path")
        if current.query not in costs:
            raise ValueError("selected policy contains an undeclared query")
        seen.add(current.query)
        child_costs = tuple(visit(child, path | {current.query}) for _, child in current.branches)
        if not child_costs:
            raise ValueError("nonterminal selected policy node requires at least one branch")
        return costs[current.query] + max(child_costs)

    worst = visit(node, frozenset())
    order = {query.name: i for i, query in enumerate(task.queries)}
    names = tuple(sorted(seen, key=order.__getitem__))
    return names, worst


def selected_policy_private_pair_gain_certificate(task: FiniteTask) -> PrivatePairAdaptiveGainCertificate:
    """Certify strict adaptive gain without solving the global fixed optimization.

    For the selected optimal adaptive tree, let U be the union cost and C_A its
    worst-path cost.  If U>C_A, the tree contains branch-exclusive query overhead.
    If every union query has a globally private cross-target pair, every fixed
    resolver must purchase the full union, so C_F=U.  Together these facts imply

        C_A < C_F = U,

    and therefore strict adaptive gain.  The certificate is sufficient only:
    strict gain can exist even when no single private pair proves one union query
    globally mandatory.
    """
    adaptive = adaptive_minimum_resolution(task)
    if adaptive.minimum_worst_path_cost is None or adaptive.selected_policy is None:
        return PrivatePairAdaptiveGainCertificate(
            "no_resolving_selected_adaptive_policy",
            adaptive.minimum_worst_path_cost,
            None,
            (),
            None,
            False,
            (),
            (),
            False,
            "no resolving adaptive policy is available for this certificate",
        )
    names, worst = _policy_union(task, adaptive.selected_policy)
    if worst != adaptive.minimum_worst_path_cost:
        raise ArithmeticError("selected policy did not attain the reported adaptive optimum")
    cost_lookup = {query.name: query.cost for query in task.queries}
    union_cost = sum(cost_lookup[name] for name in names)
    overhead = union_cost - worst
    private = private_pair_no_bypass_certificate(task, names)
    strict = overhead > 0 and private.no_fixed_bypass_certified
    return PrivatePairAdaptiveGainCertificate(
        "strict_gain_certified" if strict else "certificate_incomplete",
        worst,
        union_cost,
        names,
        overhead,
        private.every_union_query_globally_mandatory,
        private.globally_essential_union_queries,
        private.missing_private_pair_queries,
        strict,
        (
            "branch-exclusive overhead is positive and every union query is globally mandatory; fixed cost equals union cost"
            if strict
            else "private-pair conditions do not suffice to certify strict gain without global fixed optimization"
        ),
    )
