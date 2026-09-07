from dataclasses import replace

from adaptive_gain.proof_size_bounds import (
    branch_orbit_proof_size_audit,
    verify_symmetry_pruned_proof_size_metrics,
)
from adaptive_gain.symmetry_pruned_proof_dag import build_symmetry_pruned_proof_dag
from adaptive_gain.symmetry_witnesses import cycle_branch_symmetry_control


def test_cycle_control_has_exact_two_to_one_local_branch_orbit_compression():
    task = cycle_branch_symmetry_control()
    certificate = build_symmetry_pruned_proof_dag(task, budget=1)
    receipt = branch_orbit_proof_size_audit(certificate)
    assert receipt.raw_branch_count == 2
    assert receipt.orbit_representative_count == 1
    assert receipt.symmetric_branch_savings == 1
    assert receipt.automorphism_receipt_count == 1
    assert receipt.metrics_match_certificate
    assert receipt.all_local_group_bounds_hold

    branch_nodes = [row for row in receipt.node_audits if row.raw_branch_count]
    assert len(branch_nodes) == 1
    row = branch_nodes[0]
    assert row.raw_branch_count == 2
    assert row.orbit_representative_count == 1
    assert row.local_compression_factor == 2.0
    assert row.automorphism_count == 8
    assert row.local_group_bound_holds
    assert verify_symmetry_pruned_proof_size_metrics(certificate)


def test_proof_size_audit_detects_tampered_automorphism_receipt_count_metadata():
    certificate = build_symmetry_pruned_proof_dag(
        cycle_branch_symmetry_control(), budget=1
    )
    bad = replace(
        certificate,
        automorphism_receipts_built=certificate.automorphism_receipts_built + 1,
    )
    receipt = branch_orbit_proof_size_audit(bad)
    assert not receipt.metrics_match_certificate
    assert not verify_symmetry_pruned_proof_size_metrics(bad)
