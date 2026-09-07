"""Adaptive gain theory extracted from PAYOFF/MROD/BALANCE decision structure."""

from .automorphism import (
    ResidualAutomorphismGroupReceipt,
    residual_automorphism_group,
    verify_residual_automorphism_group,
)
from .core import (
    AdaptiveGainReceipt,
    AdaptiveNode,
    AdaptiveResolutionReceipt,
    BudgetResolutionRow,
    FiniteTask,
    FixedResolutionReceipt,
    Query,
    World,
    adaptive_gain_receipt,
    adaptive_minimum_resolution,
    adaptive_only_at_budget,
    bundle_resolves,
    fixed_minimum_resolution,
    resolution_budget_profile,
)
from .certificates import (
    BranchInvariantCertificate,
    RoutingBranch,
    RoutingCertificate,
    branch_invariant_no_routing_certificate,
    routing_certificate,
)
from .color_refinement import (
    BipartiteColorRefinementReceipt,
    RefinedCanonicalResidualCoverSignature,
    RefinedIsomorphismQuotientAdaptiveGainAudit,
    RefinedIsomorphismQuotientFixedBudgetDecision,
    refine_residual_incidence_colors,
    refined_canonical_residual_pair_cover_signature,
    refined_isomorphic_fixed_budget_cover_decision,
    refined_residual_pair_cover_isomorphism_witness,
    selected_policy_refined_isomorphism_gain_audit,
)
from .cover_kernel import (
    CoverKernelLimitError,
    KernelizedAdaptiveGainAudit,
    KernelizedFixedBudgetDecision,
    kernelized_fixed_budget_cover_decision,
    selected_policy_kernelized_gain_audit,
)
from .decomposition import PolicyCostDecomposition, optimal_policy_cost_decomposition
from .exhaustive import BinaryUniverseSummary, enumerate_binary_universe
from .fractional_packing import (
    FractionalPackedPair,
    FractionalPackingAdaptiveGainCertificate,
    FractionalPackingSearchLimitError,
    FractionalPairPackingCertificate,
    exact_fractional_pair_packing,
    selected_policy_fractional_pair_packing_gain_certificate,
)
from .individualization_refinement import (
    IndividualizationRefinementLimitError,
    IndividualizationRefinementSignature,
    individualization_refined_canonical_signature,
)
from .information import (
    RoutingInformationReceipt,
    best_fixed_information_bits,
    bundle_information_bits,
    policy_information_bits,
    routing_information_receipt,
    target_entropy_bits,
)
from .integer_cover_proof import (
    CoverProofBranch,
    CoverProofNode,
    FixedBudgetDecisionCertificate,
    IntegerCoverAdaptiveGainCertificate,
    IntegerCoverProofLimitError,
    fixed_budget_cover_decision,
    selected_policy_integer_cover_gain_certificate,
    verify_fixed_budget_decision_certificate,
)
from .isomorphism_quotient import (
    CanonicalResidualCoverSignature,
    IsomorphismQuotientAdaptiveGainAudit,
    IsomorphismQuotientFixedBudgetDecision,
    ResidualIsomorphismLimitError,
    ResidualIsomorphismWitness,
    ResidualPairCoverInstance,
    canonical_residual_pair_cover_signature,
    isomorphic_fixed_budget_cover_decision,
    residual_pair_cover_isomorphism_witness,
    selected_policy_isomorphism_quotient_gain_audit,
    verify_residual_pair_cover_isomorphism,
)
from .kernel_bounds import (
    AntichainKernelBoundReceipt,
    is_inclusion_antichain,
    minimal_separator_antichain,
    task_pair_antichain_bound,
)
from .minimal_normal_form import (
    MINIMAL_STRICT_GAIN_SIGNATURE,
    MinimalNormalFormReceipt,
    canonical_minimal_separator_signature,
    minimal_normal_form_receipt,
    minimal_strict_gain_standard_task,
    standard_raw_symmetry_orbit_size,
)
from .orbit_pruning import (
    OrbitPrunedIndividualizationSignature,
    orbit_pruned_individualization_canonical_signature,
)
from .pair_cover import (
    EssentialQueryWitness,
    PairCoverAudit,
    PairSeparatorRow,
    PrivatePairAdaptiveGainCertificate,
    PrivatePairNoBypassCertificate,
    pair_cover_audit,
    private_pair_no_bypass_certificate,
    restricted_fixed_minimum_resolution,
    selected_policy_private_pair_gain_certificate,
)
from .pair_packing import (
    PackedPair,
    PairPackingAdaptiveGainCertificate,
    PairPackingCertificate,
    PairPackingSearchLimitError,
    pair_packing_lower_bound,
    selected_policy_pair_packing_gain_certificate,
)
from .proof_dag import (
    CoverProofDagBranch,
    CoverProofDagCertificate,
    CoverProofDagNode,
    compress_fixed_budget_infeasibility_proof,
    verify_cover_proof_dag,
)

__all__ = [
    "ResidualAutomorphismGroupReceipt", "residual_automorphism_group",
    "verify_residual_automorphism_group",
    "AdaptiveGainReceipt", "AdaptiveNode", "AdaptiveResolutionReceipt",
    "BudgetResolutionRow", "FiniteTask", "FixedResolutionReceipt", "Query", "World",
    "adaptive_gain_receipt", "adaptive_minimum_resolution", "adaptive_only_at_budget",
    "bundle_resolves", "fixed_minimum_resolution", "resolution_budget_profile",
    "BranchInvariantCertificate", "RoutingBranch", "RoutingCertificate",
    "branch_invariant_no_routing_certificate", "routing_certificate",
    "BipartiteColorRefinementReceipt", "RefinedCanonicalResidualCoverSignature",
    "RefinedIsomorphismQuotientAdaptiveGainAudit",
    "RefinedIsomorphismQuotientFixedBudgetDecision",
    "refine_residual_incidence_colors", "refined_canonical_residual_pair_cover_signature",
    "refined_isomorphic_fixed_budget_cover_decision",
    "refined_residual_pair_cover_isomorphism_witness",
    "selected_policy_refined_isomorphism_gain_audit",
    "CoverKernelLimitError", "KernelizedAdaptiveGainAudit", "KernelizedFixedBudgetDecision",
    "kernelized_fixed_budget_cover_decision", "selected_policy_kernelized_gain_audit",
    "PolicyCostDecomposition", "optimal_policy_cost_decomposition",
    "BinaryUniverseSummary", "enumerate_binary_universe",
    "FractionalPackedPair", "FractionalPackingAdaptiveGainCertificate",
    "FractionalPackingSearchLimitError", "FractionalPairPackingCertificate",
    "exact_fractional_pair_packing", "selected_policy_fractional_pair_packing_gain_certificate",
    "IndividualizationRefinementLimitError", "IndividualizationRefinementSignature",
    "individualization_refined_canonical_signature",
    "RoutingInformationReceipt", "best_fixed_information_bits", "bundle_information_bits",
    "policy_information_bits", "routing_information_receipt", "target_entropy_bits",
    "CoverProofBranch", "CoverProofNode", "FixedBudgetDecisionCertificate",
    "IntegerCoverAdaptiveGainCertificate", "IntegerCoverProofLimitError",
    "fixed_budget_cover_decision", "selected_policy_integer_cover_gain_certificate",
    "verify_fixed_budget_decision_certificate",
    "CanonicalResidualCoverSignature", "IsomorphismQuotientAdaptiveGainAudit",
    "IsomorphismQuotientFixedBudgetDecision", "ResidualIsomorphismLimitError",
    "ResidualIsomorphismWitness", "ResidualPairCoverInstance",
    "canonical_residual_pair_cover_signature", "isomorphic_fixed_budget_cover_decision",
    "residual_pair_cover_isomorphism_witness",
    "selected_policy_isomorphism_quotient_gain_audit",
    "verify_residual_pair_cover_isomorphism",
    "AntichainKernelBoundReceipt", "is_inclusion_antichain",
    "minimal_separator_antichain", "task_pair_antichain_bound",
    "MINIMAL_STRICT_GAIN_SIGNATURE", "MinimalNormalFormReceipt",
    "canonical_minimal_separator_signature", "minimal_normal_form_receipt",
    "minimal_strict_gain_standard_task", "standard_raw_symmetry_orbit_size",
    "OrbitPrunedIndividualizationSignature",
    "orbit_pruned_individualization_canonical_signature",
    "EssentialQueryWitness", "PairCoverAudit", "PairSeparatorRow",
    "PrivatePairAdaptiveGainCertificate", "PrivatePairNoBypassCertificate",
    "pair_cover_audit", "private_pair_no_bypass_certificate",
    "restricted_fixed_minimum_resolution", "selected_policy_private_pair_gain_certificate",
    "PackedPair", "PairPackingAdaptiveGainCertificate", "PairPackingCertificate",
    "PairPackingSearchLimitError", "pair_packing_lower_bound",
    "selected_policy_pair_packing_gain_certificate",
    "CoverProofDagBranch", "CoverProofDagCertificate", "CoverProofDagNode",
    "compress_fixed_budget_infeasibility_proof", "verify_cover_proof_dag",
]
