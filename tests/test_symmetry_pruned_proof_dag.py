from dataclasses import replace
from itertools import product

from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    build_isomorphism_transport_proof_dag,
    build_symmetry_pruned_proof_dag,
    verify_symmetry_pruned_proof_dag,
)
from adaptive_gain.witnesses import routing_bypass_control


def _cycle_branch_symmetry_control():
    # Cross-target separator rows are 0011, 0110, 1001, 1100: a 4-cycle.
    # At budget 1 the first obligation has two affordable separators in the
    # same exact query-automorphism orbit. Both children are infeasible.
    worlds = (
        World("a", 0), World("b", 0), World("c", 1), World("d", 1)
    )
    queries = (
        Query("q0", 1, (0, 1, 1, 0)),
        Query("q1", 1, (0, 1, 1, 1)),
        Query("q2", 1, (0, 1, 0, 1)),
        Query("q3", 1, (0, 1, 0, 0)),
    )
    return FiniteTask(worlds, queries)


def test_parent_automorphism_orbit_prunes_two_branches_to_one_representative():
    task = _cycle_branch_symmetry_control()
    raw = build_isomorphism_transport_proof_dag(task, budget=1)
    assert not raw.fixed_resolver_exists_within_budget
    raw_root = next(node for node in raw.nodes if node.node_id == raw.root_node_id)
    assert len(raw_root.affordable_separator_queries) == 2
    assert len(raw_root.edges) == 2

    certificate = build_symmetry_pruned_proof_dag(task, budget=1)
    assert not certificate.fixed_resolver_exists_within_budget
    root = next(node for node in certificate.nodes if node.node_id == certificate.root_node_id)
    assert root.automorphism_receipt is not None
    assert root.automorphism_receipt.automorphism_count == 8
    assert root.affordable_separator_queries == (0, 1)
    assert len(root.branch_orbits) == 1
    assert root.branch_orbits[0].member_queries == (0, 1)
    assert certificate.raw_affordable_branch_count >= 2
    assert certificate.representative_branch_count < certificate.raw_affordable_branch_count
    assert certificate.symmetric_branch_savings >= 1
    assert certificate.explicit_skipped_branch_transports >= 1
    assert verify_symmetry_pruned_proof_dag(task, certificate)


def test_symmetry_verifier_rejects_tampered_skipped_branch_transport():
    task = _cycle_branch_symmetry_control()
    certificate = build_symmetry_pruned_proof_dag(task, budget=1)
    node_i = orbit_i = member_i = None
    for i, node in enumerate(certificate.nodes):
        for j, orbit in enumerate(node.branch_orbits):
            for k, member in enumerate(orbit.members):
                if member.query_index != orbit.representative_query_index:
                    node_i, orbit_i, member_i = i, j, k
                    break
            if node_i is not None:
                break
        if node_i is not None:
            break
    assert node_i is not None

    node = certificate.nodes[node_i]
    orbit = node.branch_orbits[orbit_i]
    member = orbit.members[member_i]
    assert len(member.child_to_orbit_representative_query) >= 2
    bad_member = replace(
        member,
        child_to_orbit_representative_query=(0,) * len(member.child_to_orbit_representative_query),
    )
    bad_members = list(orbit.members)
    bad_members[member_i] = bad_member
    bad_orbit = replace(orbit, members=tuple(bad_members))
    bad_orbits = list(node.branch_orbits)
    bad_orbits[orbit_i] = bad_orbit
    bad_node = replace(node, branch_orbits=tuple(bad_orbits))
    bad_nodes = list(certificate.nodes)
    bad_nodes[node_i] = bad_node
    bad_certificate = replace(certificate, nodes=tuple(bad_nodes))
    assert not verify_symmetry_pruned_proof_dag(task, bad_certificate)


def test_symmetry_pruned_decision_constructively_refuses_false_gain():
    task = routing_bypass_control()
    certificate = build_symmetry_pruned_proof_dag(task, budget=2)
    assert certificate.fixed_resolver_exists_within_budget
    assert certificate.feasible_bundle is not None
    assert verify_symmetry_pruned_proof_dag(task, certificate)


def test_symmetry_pruned_strict_gain_matches_exact_solver_on_complete_minimal_universe():
    targets = (0, 0, 1, 1)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    patterns = tuple(product((0, 1), repeat=4))
    strict = predicted_strict = false_positive = false_negative = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, outcomes) for j, outcomes in enumerate(maps)),
        )
        exact = adaptive_gain_receipt(task)
        actual = exact.strict_adaptive_gain
        predicted = False
        if exact.adaptive_cost is not None:
            certificate = build_symmetry_pruned_proof_dag(
                task,
                budget=exact.adaptive_cost,
                max_permutations=6,
            )
            predicted = not certificate.fixed_resolver_exists_within_budget
            assert verify_symmetry_pruned_proof_dag(task, certificate)
        strict += int(actual)
        predicted_strict += int(predicted)
        false_positive += int(predicted and not actual)
        false_negative += int(actual and not predicted)
    assert strict == 192
    assert predicted_strict == 192
    assert false_positive == 0
    assert false_negative == 0
