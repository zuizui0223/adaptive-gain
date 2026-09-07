from dataclasses import replace

import pytest

from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    compress_fixed_budget_infeasibility_proof,
    fixed_budget_cover_decision,
    verify_cover_proof_dag,
)
from adaptive_gain.witnesses import (
    fractional_integrality_gap_gain_control,
    routing_bypass_control,
)


def _dag_compression_control():
    # Seeded strict-gain benchmark with genuine state reconvergence.
    # At B=3 the recursive proof has 19 node occurrences but only 14 distinct
    # residual states, so exact state quotienting removes five repeated subproofs.
    worlds = tuple(World(f"w{i}", 0 if i < 4 else 1) for i in range(8))
    maps = (
        (0, 1, 0, 0, 0, 0, 0, 0),
        (0, 0, 1, 1, 0, 1, 1, 1),
        (0, 0, 1, 0, 1, 1, 0, 0),
        (1, 0, 1, 0, 1, 0, 1, 0),
        (1, 0, 0, 0, 1, 0, 1, 1),
        (1, 1, 0, 1, 1, 1, 1, 0),
        (1, 0, 1, 0, 1, 1, 1, 1),
        (0, 1, 1, 0, 1, 0, 1, 0),
    )
    return FiniteTask(
        worlds,
        tuple(Query(f"q{i}", 1, row) for i, row in enumerate(maps)),
    )


def test_verified_tree_compresses_to_exact_shared_state_dag():
    task = _dag_compression_control()
    exact = adaptive_gain_receipt(task)
    assert (exact.adaptive_cost, exact.fixed_cost) == (3, 4)
    tree = fixed_budget_cover_decision(task, budget=3)
    assert not tree.fixed_resolver_exists_within_budget
    assert tree.states_visited == 14

    dag = compress_fixed_budget_infeasibility_proof(task, tree)
    assert verify_cover_proof_dag(task, dag)
    assert dag.expanded_tree_nodes == 19
    assert dag.dag_node_count == 14
    assert dag.shared_state_savings == 5
    assert abs(dag.compression_ratio - 19 / 14) < 1e-12


def test_dag_verifier_rejects_wrong_shared_child_reference():
    task = _dag_compression_control()
    tree = fixed_budget_cover_decision(task, budget=3)
    dag = compress_fixed_budget_infeasibility_proof(task, tree)
    root = next(node for node in dag.nodes if node.node_id == dag.root_node_id)
    assert root.branches
    bad_branch = replace(root.branches[0], child_node_id=dag.root_node_id)
    bad_root = replace(root, branches=(bad_branch,) + root.branches[1:])
    bad_nodes = tuple(bad_root if n.node_id == root.node_id else n for n in dag.nodes)
    bad = replace(dag, nodes=bad_nodes)
    assert not verify_cover_proof_dag(task, bad)


def test_dag_compression_preserves_lp_integrality_gap_integer_proof():
    task = fractional_integrality_gap_gain_control()
    tree = fixed_budget_cover_decision(task, budget=2)
    assert not tree.fixed_resolver_exists_within_budget
    dag = compress_fixed_budget_infeasibility_proof(task, tree)
    assert verify_cover_proof_dag(task, dag)
    assert dag.dag_node_count <= dag.expanded_tree_nodes


def test_feasible_fixed_decision_is_not_misrepresented_as_infeasibility_dag():
    task = routing_bypass_control()
    tree = fixed_budget_cover_decision(task, budget=2)
    assert tree.fixed_resolver_exists_within_budget
    with pytest.raises(ValueError):
        compress_fixed_budget_infeasibility_proof(task, tree)
