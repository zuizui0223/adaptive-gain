"""Adaptive gain theory extracted from PAYOFF/MROD/BALANCE decision structure."""

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
from .decomposition import PolicyCostDecomposition, optimal_policy_cost_decomposition
from .exhaustive import BinaryUniverseSummary, enumerate_binary_universe
from .information import (
    RoutingInformationReceipt,
    best_fixed_information_bits,
    bundle_information_bits,
    policy_information_bits,
    routing_information_receipt,
    target_entropy_bits,
)

__all__ = [
    "AdaptiveGainReceipt",
    "AdaptiveNode",
    "AdaptiveResolutionReceipt",
    "BudgetResolutionRow",
    "FiniteTask",
    "FixedResolutionReceipt",
    "Query",
    "World",
    "adaptive_gain_receipt",
    "adaptive_minimum_resolution",
    "adaptive_only_at_budget",
    "bundle_resolves",
    "fixed_minimum_resolution",
    "resolution_budget_profile",
    "BranchInvariantCertificate",
    "RoutingBranch",
    "RoutingCertificate",
    "branch_invariant_no_routing_certificate",
    "routing_certificate",
    "PolicyCostDecomposition",
    "optimal_policy_cost_decomposition",
    "BinaryUniverseSummary",
    "enumerate_binary_universe",
    "RoutingInformationReceipt",
    "best_fixed_information_bits",
    "bundle_information_bits",
    "policy_information_bits",
    "routing_information_receipt",
    "target_entropy_bits",
]
