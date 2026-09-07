from dataclasses import replace
from itertools import product

from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    build_isomorphism_transport_proof_dag,
    verify_isomorphism_transport_proof_dag,
)
from adaptive_gain.witnesses import routing_bypass_control


def _isomorphism_compression_control():
    worlds = tuple(World(f"w{i}", 0 if i < 3 else 1) for i in range(6))
    maps = (
        (0, 1, 0, 0, 1, 0),
        (1, 1, 0, 1, 1, 0),
        (0, 0, 1, 1, 1, 1),
        (1, 0, 0, 0, 1, 1),
        (0, 0, 0, 1, 0, 1),
        (0, 0, 1, 0, 1, 0),
    )
    return FiniteTask(
        worlds,
        tuple(Query(f"q{i}", 1, row) for i, row in enumerate(maps)),
    )


def test_isomorphism_transport_dag_exports_and_verifies_shared_residual_proof():
    task = _isomorphism_compression_control()
    exact = adaptive_gain_receipt(task)
    assert (exact.adaptive_cost, exact.fixed_cost) == (2, 3)
    certificate = build_isomorphism_transport_proof_dag(task, budget=2)
    assert not certificate.fixed_resolver_exists_within_budget
    assert certificate.root_node_id is not None
    assert certificate.exact_residual_instance_count > certificate.isomorphism_class_count
    assert certificate.isomorphism_merge_count > 0
    assert certificate.transported_edge_count > 0
    assert certificate.expanded_tree_nodes >= certificate.dag_node_count
    assert verify_isomorphism_transport_proof_dag(task, certificate)


def test_transport_verifier_rejects_tampered_query_bijection():
    task = _isomorphism_compression_control()
    certificate = build_isomorphism_transport_proof_dag(task, budget=2)
    node_index = None
    edge_index = None
    for i, node in enumerate(certificate.nodes):
        for j, edge in enumerate(node.edges):
            target = next(n for n in certificate.nodes if n.node_id == edge.child_node_id)
            child_qn = len(edge.child_to_representative_query)
            if child_qn >= 2 and edge.child_to_representative_query != tuple(range(child_qn)):
                node_index, edge_index = i, j
                break
        if node_index is not None:
            break
    assert node_index is not None and edge_index is not None

    node = certificate.nodes[node_index]
    edge = node.edges[edge_index]
    mapping = list(edge.child_to_representative_query)
    mapping[0], mapping[1] = mapping[1], mapping[0]
    bad_edge = replace(edge, child_to_representative_query=tuple(mapping))
    bad_edges = list(node.edges)
    bad_edges[edge_index] = bad_edge
    bad_node = replace(node, edges=tuple(bad_edges))
    bad_nodes = list(certificate.nodes)
    bad_nodes[node_index] = bad_node
    bad_certificate = replace(certificate, nodes=tuple(bad_nodes))
    assert not verify_isomorphism_transport_proof_dag(task, bad_certificate)


def test_transport_decision_constructively_refuses_false_gain_on_bypass_control():
    task = routing_bypass_control()
    certificate = build_isomorphism_transport_proof_dag(task, budget=2)
    assert certificate.fixed_resolver_exists_within_budget
    assert certificate.feasible_bundle is not None
    assert verify_isomorphism_transport_proof_dag(task, certificate)


def test_transport_dag_strict_gain_decision_matches_exact_solver_on_complete_minimal_universe():
    targets = (0, 0, 1, 1)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    patterns = tuple(product((0, 1), repeat=4))
    strict = transported_strict = false_positive = false_negative = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, outcomes) for j, outcomes in enumerate(maps)),
        )
        exact = adaptive_gain_receipt(task)
        actual = exact.strict_adaptive_gain
        predicted = False
        if exact.adaptive_cost is not None:
            decision = build_isomorphism_transport_proof_dag(
                task, budget=exact.adaptive_cost, max_permutations=6
            )
            predicted = not decision.fixed_resolver_exists_within_budget
            assert verify_isomorphism_transport_proof_dag(task, decision)
        strict += int(actual)
        transported_strict += int(predicted)
        false_positive += int(predicted and not actual)
        false_negative += int(actual and not predicted)
    assert strict == 192
    assert transported_strict == 192
    assert false_positive == 0
    assert false_negative == 0
