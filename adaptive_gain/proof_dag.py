"""Compress verified integer fixed-cover proof trees into checkable state DAGs.

The bounded fixed-cover continuation problem depends only on the residual state

    (uncovered cross-target pairs, available queries, remaining budget).

Different branch histories that reach the same residual state therefore have the
same continuation feasibility. A verified recursive infeasibility proof can be
quotiented by exact residual-state equality and exported as a DAG whose shared
nodes are independently rechecked from the task.
"""
from __future__ import annotations

from dataclasses import dataclass

from .core import FiniteTask
from .integer_cover_proof import (
    FixedBudgetDecisionCertificate,
    _cover_masks,
    _rows,
    verify_fixed_budget_decision_certificate,
)


@dataclass(frozen=True)
class CoverProofDagBranch:
    query: str
    child_node_id: int


@dataclass(frozen=True)
class CoverProofDagNode:
    node_id: int
    status: str
    remaining_budget: int
    uncovered_world_pair: tuple[str, str]
    affordable_separator_queries: tuple[str, ...]
    branches: tuple[CoverProofDagBranch, ...]


@dataclass(frozen=True)
class CoverProofDagCertificate:
    budget: int
    root_node_id: int
    nodes: tuple[CoverProofDagNode, ...]
    expanded_tree_nodes: int
    dag_node_count: int
    shared_state_savings: int
    compression_ratio: float
    source_tree_verified: bool
    scope: str = "exact_residual_state_quotient_of_verified_fixed_cover_infeasibility_tree"


def _expanded_dag_occurrences(root_id: int, node_map: dict[int, CoverProofDagNode]) -> int:
    """Count recursive tree occurrences represented by one DAG-root occurrence."""
    cache: dict[int, int] = {}

    def count(node_id: int) -> int:
        if node_id in cache:
            return cache[node_id]
        node = node_map[node_id]
        value = 1 + sum(count(branch.child_node_id) for branch in node.branches)
        cache[node_id] = value
        return value

    return count(root_id)


def compress_fixed_budget_infeasibility_proof(
    task: FiniteTask,
    certificate: FixedBudgetDecisionCertificate,
) -> CoverProofDagCertificate:
    """Quotient a verified recursive infeasibility proof by residual-state equality."""
    if certificate.fixed_resolver_exists_within_budget:
        raise ValueError("DAG compression requires an infeasibility certificate")
    if not verify_fixed_budget_decision_certificate(task, certificate):
        raise ValueError("source fixed-budget certificate failed independent verification")
    root = certificate.infeasibility_proof
    if root is None:
        raise ValueError("infeasibility certificate has no proof tree")

    rows = _rows(task)
    covers = _cover_masks(task, rows)
    query_count = len(task.queries)
    name_to_q = {query.name: q for q, query in enumerate(task.queries)}
    pair_to_p = {
        (task.worlds[i].name, task.worlds[j].name): p
        for p, (i, j, _) in enumerate(rows)
    }

    state_to_id: dict[tuple[int, int, int], int] = {}
    nodes: dict[int, CoverProofDagNode] = {}

    def visit(node, uncovered: int, available: int, remaining: int) -> int:
        state = (uncovered, available, remaining)
        if state in state_to_id:
            return state_to_id[state]
        node_id = len(state_to_id)
        state_to_id[state] = node_id

        if node.uncovered_world_pair not in pair_to_p:
            raise ArithmeticError("verified source proof contained an unknown pair")
        dag_branches = []
        for branch in node.branches:
            q = name_to_q[branch.query]
            child_id = visit(
                branch.child,
                uncovered & ~covers[q],
                available & ~(1 << q),
                remaining - task.queries[q].cost,
            )
            dag_branches.append(CoverProofDagBranch(branch.query, child_id))
        nodes[node_id] = CoverProofDagNode(
            node_id,
            node.status,
            node.remaining_budget,
            node.uncovered_world_pair,
            node.affordable_separator_queries,
            tuple(dag_branches),
        )
        return node_id

    root_id = visit(
        root,
        (1 << len(rows)) - 1,
        (1 << query_count) - 1,
        certificate.budget,
    )
    ordered = tuple(nodes[i] for i in range(len(nodes)))
    dag_count = len(ordered)
    if dag_count == 0:
        raise ArithmeticError("empty proof DAG")

    # Count the full recursive tree represented by the DAG *after* quotienting.
    # Counting visits during construction would undercount shared subtrees because
    # construction intentionally stops descending when a state is seen again.
    expanded = _expanded_dag_occurrences(root_id, nodes)
    if expanded < dag_count:
        raise ArithmeticError("invalid proof DAG compression counts")
    result = CoverProofDagCertificate(
        certificate.budget,
        root_id,
        ordered,
        expanded,
        dag_count,
        expanded - dag_count,
        expanded / dag_count,
        True,
    )
    if not verify_cover_proof_dag(task, result):
        raise ArithmeticError("generated proof DAG failed independent verification")
    return result


def verify_cover_proof_dag(task: FiniteTask, certificate: CoverProofDagCertificate) -> bool:
    """Reconstruct and verify every residual-state transition in a proof DAG."""
    if certificate.budget < 0 or not certificate.source_tree_verified:
        return False
    node_map = {node.node_id: node for node in certificate.nodes}
    if len(node_map) != len(certificate.nodes):
        return False
    if certificate.root_node_id not in node_map:
        return False
    if certificate.dag_node_count != len(node_map) or certificate.dag_node_count <= 0:
        return False

    rows = _rows(task)
    covers = _cover_masks(task, rows)
    query_count = len(task.queries)
    costs = tuple(query.cost for query in task.queries)
    name_to_q = {query.name: q for q, query in enumerate(task.queries)}
    pair_to_p = {
        (task.worlds[i].name, task.worlds[j].name): p
        for p, (i, j, _) in enumerate(rows)
    }
    expected_state: dict[int, tuple[int, int, int]] = {}
    visiting: set[int] = set()
    verified: set[int] = set()

    def check(node_id: int, uncovered: int, available: int, remaining: int) -> bool:
        expected = (uncovered, available, remaining)
        if node_id in expected_state:
            return expected_state[node_id] == expected and node_id in verified
        if node_id not in node_map or node_id in visiting:
            return False
        expected_state[node_id] = expected
        visiting.add(node_id)
        node = node_map[node_id]
        if node.remaining_budget != remaining or node.uncovered_world_pair not in pair_to_p:
            return False
        p = pair_to_p[node.uncovered_world_pair]
        if not (uncovered & (1 << p)):
            return False
        separator_mask = rows[p][2] & available
        candidates = tuple(
            q for q in range(query_count)
            if separator_mask & (1 << q) and costs[q] <= remaining
        )
        names = tuple(task.queries[q].name for q in candidates)

        if node.status == "unseparable_pair":
            ok = rows[p][2] == 0 and not node.branches and not node.affordable_separator_queries
        elif node.status == "no_affordable_separator":
            ok = not candidates and not node.branches and not node.affordable_separator_queries
        elif node.status == "all_affordable_separators_infeasible":
            if node.affordable_separator_queries != names:
                return False
            if tuple(branch.query for branch in node.branches) != names:
                return False
            ok = True
            for branch in node.branches:
                q = name_to_q.get(branch.query)
                if q is None or costs[q] > remaining or branch.child_node_id not in node_map:
                    return False
                if not check(
                    branch.child_node_id,
                    uncovered & ~covers[q],
                    available & ~(1 << q),
                    remaining - costs[q],
                ):
                    ok = False
                    break
        else:
            return False
        visiting.remove(node_id)
        if ok:
            verified.add(node_id)
        return ok

    root_ok = check(
        certificate.root_node_id,
        (1 << len(rows)) - 1,
        (1 << query_count) - 1,
        certificate.budget,
    )
    if not root_ok or verified != set(node_map):
        return False

    expanded = _expanded_dag_occurrences(certificate.root_node_id, node_map)
    if expanded != certificate.expanded_tree_nodes:
        return False
    if certificate.shared_state_savings != expanded - certificate.dag_node_count:
        return False
    if abs(certificate.compression_ratio - expanded / certificate.dag_node_count) > 1e-12:
        return False
    return True
