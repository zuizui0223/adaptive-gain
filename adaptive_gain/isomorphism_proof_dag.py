"""Independently checkable isomorphism-transport DAGs for fixed-cover infeasibility.

The existing exact integer proof tree is recursive, while the residual isomorphism
solver only memoizes the decision internally.  This module exports the stronger
object: one representative residual pair-cover proof node per exact weighted-
incidence isomorphism class, with every shared edge carrying an explicit local
query bijection from the source child instance to the representative node.

The verifier does not trust canonical signatures.  It reconstructs each child
instance from its parent edge and verifies the supplied transport bijection
against the representative weighted incidence directly.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .color_refinement import (
    refined_canonical_residual_pair_cover_signature,
    refined_residual_pair_cover_isomorphism_witness,
)
from .core import FiniteTask, bundle_resolves
from .isomorphism_quotient import (
    ResidualIsomorphismLimitError,
    ResidualIsomorphismWitness,
    ResidualPairCoverInstance,
    verify_residual_pair_cover_isomorphism,
)


class IsomorphismProofDagLimitError(RuntimeError):
    """Exact transported proof DAG generation exceeded a declared cap."""


@dataclass(frozen=True)
class IsomorphismTransportEdge:
    selected_query_index: int
    child_node_id: int
    child_to_representative_query: tuple[int, ...]


@dataclass(frozen=True)
class IsomorphismProofDagNode:
    node_id: int
    instance: ResidualPairCoverInstance
    status: str
    chosen_obligation_index: int
    affordable_separator_queries: tuple[int, ...]
    edges: tuple[IsomorphismTransportEdge, ...]


@dataclass(frozen=True)
class IsomorphismTransportProofDagCertificate:
    budget: int
    fixed_resolver_exists_within_budget: bool
    feasible_bundle: tuple[str, ...] | None
    root_node_id: int | None
    nodes: tuple[IsomorphismProofDagNode, ...]
    exact_residual_instance_count: int
    isomorphism_class_count: int
    isomorphism_merge_count: int
    transported_edge_count: int
    expanded_tree_nodes: int
    dag_node_count: int
    compression_ratio: float | None
    canonicalization_calls: int
    canonical_permutations_examined: int
    complete_search: bool
    scope: str = "exact_fixed_cover_budget_decision_with_explicit_isomorphism_transport_proof_dag"


def _root_instance(task: FiniteTask, budget: int) -> ResidualPairCoverInstance:
    rows = []
    for i, j in combinations(range(len(task.worlds)), 2):
        if task.worlds[i].target == task.worlds[j].target:
            continue
        mask = 0
        for q, query in enumerate(task.queries):
            if query.outcomes[i] != query.outcomes[j]:
                mask |= 1 << q
        rows.append(mask)
    return ResidualPairCoverInstance(
        tuple(query.cost for query in task.queries),
        tuple(sorted(rows)),
        budget,
    )


def _instance_key(instance: ResidualPairCoverInstance) -> tuple:
    return (
        instance.remaining_budget,
        instance.query_costs,
        tuple(sorted(instance.separator_rows)),
    )


def _affordable_separators(
    instance: ResidualPairCoverInstance, row_index: int
) -> tuple[int, ...]:
    row = instance.separator_rows[row_index]
    return tuple(
        q
        for q, cost in enumerate(instance.query_costs)
        if row & (1 << q) and cost <= instance.remaining_budget
    )


def _choose_obligation(instance: ResidualPairCoverInstance) -> tuple[int, tuple[int, ...]]:
    if not instance.separator_rows:
        raise ValueError("resolved residual instance has no uncovered obligation")
    candidates = tuple(
        (len(_affordable_separators(instance, p)), p, _affordable_separators(instance, p))
        for p in range(len(instance.separator_rows))
    )
    _, p, affordable = min(candidates)
    return p, affordable


def _child_instance(
    instance: ResidualPairCoverInstance,
    selected_query_index: int,
) -> ResidualPairCoverInstance:
    qn = len(instance.query_costs)
    if not 0 <= selected_query_index < qn:
        raise ValueError("selected query index is outside the residual query vocabulary")
    cost = instance.query_costs[selected_query_index]
    if cost > instance.remaining_budget:
        raise ValueError("selected query is not affordable")

    remaining_queries = tuple(q for q in range(qn) if q != selected_query_index)
    old_to_new = {old: new for new, old in enumerate(remaining_queries)}
    rows = []
    for row in instance.separator_rows:
        if row & (1 << selected_query_index):
            continue
        mask = 0
        for old in remaining_queries:
            if row & (1 << old):
                mask |= 1 << old_to_new[old]
        rows.append(mask)
    return ResidualPairCoverInstance(
        tuple(instance.query_costs[q] for q in remaining_queries),
        tuple(sorted(rows)),
        instance.remaining_budget - cost,
    )


def build_isomorphism_transport_proof_dag(
    task: FiniteTask,
    *,
    budget: int,
    max_nodes: int = 200_000,
    max_permutations: int = 100_000,
) -> IsomorphismTransportProofDagCertificate:
    """Decide bounded fixed cover and export an explicit transported DAG if infeasible."""
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    if type(max_nodes) is not int or max_nodes < 1:
        raise ValueError("max_nodes must be a positive integer")

    root = _root_instance(task, budget)
    root_labels = tuple(query.name for query in task.queries)
    if not root.separator_rows:
        return IsomorphismTransportProofDagCertificate(
            budget, True, (), None, (), 1, 0, 0, 0, 0, 0, None, 0, 0, True
        )

    nodes: dict[int, IsomorphismProofDagNode] = {}
    signature_to_node: dict[tuple, int] = {}
    exact_instances: set[tuple] = set()
    canonical_calls = 0
    permutations_examined = 0
    next_node_id = 0

    @dataclass(frozen=True)
    class SearchResult:
        feasible: bool
        bundle: tuple[str, ...] | None
        node_id: int | None
        source_to_node_query: tuple[int, ...] | None

    def search(
        instance: ResidualPairCoverInstance,
        labels: tuple[str, ...],
    ) -> SearchResult:
        nonlocal canonical_calls, permutations_examined, next_node_id
        exact_instances.add(_instance_key(instance))
        if not instance.separator_rows:
            return SearchResult(True, (), None, None)

        canonical = refined_canonical_residual_pair_cover_signature(
            instance,
            max_permutations=max_permutations,
        )
        canonical_calls += 1
        permutations_examined += canonical.permutations_examined
        signature = canonical.signature
        existing_id = signature_to_node.get(signature)
        if existing_id is not None:
            representative = nodes[existing_id].instance
            witness = refined_residual_pair_cover_isomorphism_witness(
                instance,
                representative,
                max_permutations=max_permutations,
            )
            if witness is None or not verify_residual_pair_cover_isomorphism(witness):
                raise ArithmeticError("canonical cache hit lacked a valid explicit transport")
            return SearchResult(False, None, existing_id, witness.left_to_right_query)

        if len(nodes) >= max_nodes:
            raise IsomorphismProofDagLimitError("transport proof DAG node cap reached")

        chosen, affordable = _choose_obligation(instance)
        if not affordable:
            node_id = next_node_id
            next_node_id += 1
            node = IsomorphismProofDagNode(
                node_id,
                instance,
                "no_affordable_separator",
                chosen,
                (),
                (),
            )
            nodes[node_id] = node
            signature_to_node[signature] = node_id
            return SearchResult(
                False,
                None,
                node_id,
                tuple(range(len(instance.query_costs))),
            )

        edge_specs = []
        for q in affordable:
            child = _child_instance(instance, q)
            child_labels = tuple(label for i, label in enumerate(labels) if i != q)
            result = search(child, child_labels)
            if result.feasible:
                assert result.bundle is not None
                return SearchResult(
                    True,
                    (labels[q],) + result.bundle,
                    None,
                    None,
                )
            assert result.node_id is not None and result.source_to_node_query is not None
            edge_specs.append(
                IsomorphismTransportEdge(
                    q,
                    result.node_id,
                    result.source_to_node_query,
                )
            )

        node_id = next_node_id
        next_node_id += 1
        node = IsomorphismProofDagNode(
            node_id,
            instance,
            "all_affordable_separators_infeasible",
            chosen,
            affordable,
            tuple(edge_specs),
        )
        nodes[node_id] = node
        signature_to_node[signature] = node_id
        return SearchResult(
            False,
            None,
            node_id,
            tuple(range(len(instance.query_costs))),
        )

    result = search(root, root_labels)
    if result.feasible:
        assert result.bundle is not None
        lookup = {query.name: query.cost for query in task.queries}
        if len(set(result.bundle)) != len(result.bundle):
            raise ArithmeticError("transport DAG solver repeated a query")
        if sum(lookup[name] for name in result.bundle) > budget:
            raise ArithmeticError("transport DAG solver returned an over-budget bundle")
        if not bundle_resolves(task, result.bundle):
            raise ArithmeticError("transport DAG solver returned a non-resolving bundle")
        certificate = IsomorphismTransportProofDagCertificate(
            budget, True, result.bundle, None, (),
            len(exact_instances), 0, 0, 0, 0, 0, None,
            canonical_calls, permutations_examined, True,
        )
        if not verify_isomorphism_transport_proof_dag(task, certificate):
            raise ArithmeticError("generated feasible transport decision failed verification")
        return certificate

    assert result.node_id is not None
    if result.source_to_node_query != tuple(range(len(root.query_costs))):
        # The root is the first visited state, so it must be its own representative.
        raise ArithmeticError("root transport proof unexpectedly reused another representative")
    ordered = tuple(nodes[node_id] for node_id in sorted(nodes))
    node_map = {node.node_id: node for node in ordered}

    transport_edges = 0
    for node in ordered:
        for edge in node.edges:
            child = _child_instance(node.instance, edge.selected_query_index)
            target = node_map[edge.child_node_id].instance
            if _instance_key(child) != _instance_key(target):
                transport_edges += 1

    expansion_cache: dict[int, int] = {}
    def expanded_count(node_id: int) -> int:
        if node_id in expansion_cache:
            return expansion_cache[node_id]
        node = node_map[node_id]
        value = 1 + sum(expanded_count(edge.child_node_id) for edge in node.edges)
        expansion_cache[node_id] = value
        return value

    expanded = expanded_count(result.node_id)
    dag_count = len(ordered)
    certificate = IsomorphismTransportProofDagCertificate(
        budget,
        False,
        None,
        result.node_id,
        ordered,
        len(exact_instances),
        dag_count,
        len(exact_instances) - dag_count,
        transport_edges,
        expanded,
        dag_count,
        expanded / dag_count if dag_count else None,
        canonical_calls,
        permutations_examined,
        True,
    )
    if not verify_isomorphism_transport_proof_dag(task, certificate):
        raise ArithmeticError("generated isomorphism transport proof DAG failed verification")
    return certificate


def verify_isomorphism_transport_proof_dag(
    task: FiniteTask,
    certificate: IsomorphismTransportProofDagCertificate,
) -> bool:
    """Verify all structural branches and every explicit isomorphism transport edge."""
    if not certificate.complete_search or certificate.budget < 0:
        return False
    if certificate.fixed_resolver_exists_within_budget:
        if certificate.root_node_id is not None or certificate.nodes:
            return False
        bundle = certificate.feasible_bundle
        if bundle is None:
            return False
        lookup = {query.name: query.cost for query in task.queries}
        if len(set(bundle)) != len(bundle) or any(name not in lookup for name in bundle):
            return False
        if sum(lookup[name] for name in bundle) > certificate.budget:
            return False
        return bundle_resolves(task, bundle)

    if certificate.feasible_bundle is not None or certificate.root_node_id is None:
        return False
    node_map = {node.node_id: node for node in certificate.nodes}
    if len(node_map) != len(certificate.nodes) or certificate.root_node_id not in node_map:
        return False
    if certificate.dag_node_count != len(node_map) or certificate.isomorphism_class_count != len(node_map):
        return False
    root = _root_instance(task, certificate.budget)
    if _instance_key(node_map[certificate.root_node_id].instance) != _instance_key(root):
        return False

    visiting: set[int] = set()
    verified: set[int] = set()
    reconstructed_exact: set[tuple] = {_instance_key(root)}
    transported_edges = 0

    def check(node_id: int) -> bool:
        nonlocal transported_edges
        if node_id in verified:
            return True
        if node_id in visiting or node_id not in node_map:
            return False
        visiting.add(node_id)
        node = node_map[node_id]
        instance = node.instance
        if not instance.separator_rows:
            return False
        if not 0 <= node.chosen_obligation_index < len(instance.separator_rows):
            return False
        affordable = _affordable_separators(instance, node.chosen_obligation_index)

        if node.status == "no_affordable_separator":
            ok = not affordable and not node.affordable_separator_queries and not node.edges
        elif node.status == "all_affordable_separators_infeasible":
            if node.affordable_separator_queries != affordable:
                return False
            if tuple(edge.selected_query_index for edge in node.edges) != affordable:
                return False
            ok = True
            for edge in node.edges:
                if edge.child_node_id not in node_map:
                    return False
                try:
                    child = _child_instance(instance, edge.selected_query_index)
                except ValueError:
                    return False
                reconstructed_exact.add(_instance_key(child))
                target = node_map[edge.child_node_id].instance
                witness = ResidualIsomorphismWitness(
                    child,
                    target,
                    edge.child_to_representative_query,
                )
                if not verify_residual_pair_cover_isomorphism(witness):
                    return False
                if _instance_key(child) != _instance_key(target):
                    transported_edges += 1
                if target.remaining_budget >= instance.remaining_budget:
                    return False
                if not check(edge.child_node_id):
                    ok = False
                    break
        else:
            return False

        visiting.remove(node_id)
        if ok:
            verified.add(node_id)
        return ok

    if not check(certificate.root_node_id):
        return False
    if verified != set(node_map):
        return False
    if certificate.exact_residual_instance_count != len(reconstructed_exact):
        return False
    if certificate.isomorphism_merge_count != (
        certificate.exact_residual_instance_count - certificate.isomorphism_class_count
    ):
        return False
    if certificate.transported_edge_count != transported_edges:
        return False

    expansion_cache: dict[int, int] = {}
    def expanded_count(node_id: int) -> int:
        if node_id in expansion_cache:
            return expansion_cache[node_id]
        value = 1 + sum(
            expanded_count(edge.child_node_id)
            for edge in node_map[node_id].edges
        )
        expansion_cache[node_id] = value
        return value

    expanded = expanded_count(certificate.root_node_id)
    if certificate.expanded_tree_nodes != expanded:
        return False
    if certificate.compression_ratio is None:
        return False
    if abs(certificate.compression_ratio - expanded / len(node_map)) > 1e-12:
        return False
    return True
