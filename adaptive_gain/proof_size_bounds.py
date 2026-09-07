"""Exact local and global size accounting for symmetry-pruned fixed-cover proofs."""
from __future__ import annotations

from dataclasses import dataclass

from .symmetry_pruned_proof_dag import SymmetryPrunedProofDagCertificate


@dataclass(frozen=True)
class BranchOrbitNodeAudit:
    node_id: int
    raw_branch_count: int
    orbit_representative_count: int
    symmetric_branch_savings: int
    local_compression_factor: float | None
    automorphism_count: int | None
    local_group_bound_holds: bool


@dataclass(frozen=True)
class BranchOrbitProofSizeReceipt:
    node_audits: tuple[BranchOrbitNodeAudit, ...]
    raw_branch_count: int
    orbit_representative_count: int
    symmetric_branch_savings: int
    automorphism_receipt_count: int
    metrics_match_certificate: bool
    all_local_group_bounds_hold: bool
    scope: str = "exact_branch_orbit_size_accounting_for_symmetry_pruned_fixed_cover_proof_DAG"


def branch_orbit_proof_size_audit(
    certificate: SymmetryPrunedProofDagCertificate,
) -> BranchOrbitProofSizeReceipt:
    """Recompute branch-orbit proof-size metrics from the stored proof object.

    If a proof node has b affordable branches partitioned into o exact query-
    automorphism orbits, the stored recursive proof needs only o representative
    children. The local saving is b-o. For b>0,

        b/o <= |Aut(I)|,

    because every orbit intersection has size at most the parent automorphism
    group order, so their average size cannot exceed that order.
    """
    audits = []
    raw_total = orbit_total = auto_receipts = 0
    all_bounds = True

    for node in certificate.nodes:
        b = len(node.affordable_separator_queries)
        o = len(node.branch_orbits)
        if node.automorphism_receipt is None:
            group_order = None
            local_ok = (b == 0 and o == 0)
        else:
            auto_receipts += 1
            group_order = node.automorphism_receipt.automorphism_count
            local_ok = (
                b > 0
                and o > 0
                and o <= b
                and b <= o * group_order
            )
        factor = (b / o) if o else None
        audits.append(
            BranchOrbitNodeAudit(
                node.node_id,
                b,
                o,
                b - o,
                factor,
                group_order,
                local_ok,
            )
        )
        raw_total += b
        orbit_total += o
        all_bounds = all_bounds and local_ok

    savings = raw_total - orbit_total
    metrics_match = (
        raw_total == certificate.raw_affordable_branch_count
        and orbit_total == certificate.representative_branch_count
        and savings == certificate.symmetric_branch_savings
        and auto_receipts == certificate.automorphism_receipts_built
    )
    return BranchOrbitProofSizeReceipt(
        tuple(audits),
        raw_total,
        orbit_total,
        savings,
        auto_receipts,
        metrics_match,
        all_bounds,
    )


def verify_symmetry_pruned_proof_size_metrics(
    certificate: SymmetryPrunedProofDagCertificate,
) -> bool:
    receipt = branch_orbit_proof_size_audit(certificate)
    return receipt.metrics_match_certificate and receipt.all_local_group_bounds_hold
