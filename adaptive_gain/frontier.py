"""Public entrypoint for productive-frontier fixed and bypass structure."""

from .frontier_decomposition import (
    ProductiveFrontierPolicyDecomposition,
    productive_frontier_policy_decomposition,
)
from .frontier_transversals import (
    FrontierTransversalLimitError,
    FrontierTransversalPolicyDecomposition,
    MinimalTransversalCertificate,
    enumerate_minimal_transversals,
    frontier_transversal_policy_decomposition,
    verify_minimal_transversal_certificate,
)
from .minimal_productive_frontier import (
    MinimalProductiveFrontierCertificate,
    StaticFrontierFixedCostReceipt,
    build_minimal_productive_frontier_from_pair_incidence,
    bundle_resolves_from_minimal_productive_frontier,
    minimal_frontier_fixed_minimum_resolution,
    static_minimal_frontier_fixed_cost_audit,
    verify_minimal_productive_frontier_from_pair_incidence,
)
from .productive_frontier import (
    ProductiveFrontierCertificate,
    ProductiveFrontierJointCostReceipt,
    build_productive_frontier,
    bundle_resolves_from_productive_frontier,
    productive_frontier_fixed_minimum_resolution,
    productive_frontier_joint_cost_audit,
    productive_frontier_sperner_bound,
    verify_productive_frontier,
)

__all__ = [
    "ProductiveFrontierPolicyDecomposition",
    "productive_frontier_policy_decomposition",
    "FrontierTransversalLimitError",
    "FrontierTransversalPolicyDecomposition",
    "MinimalTransversalCertificate",
    "enumerate_minimal_transversals",
    "frontier_transversal_policy_decomposition",
    "verify_minimal_transversal_certificate",
    "MinimalProductiveFrontierCertificate",
    "StaticFrontierFixedCostReceipt",
    "build_minimal_productive_frontier_from_pair_incidence",
    "bundle_resolves_from_minimal_productive_frontier",
    "minimal_frontier_fixed_minimum_resolution",
    "static_minimal_frontier_fixed_cost_audit",
    "verify_minimal_productive_frontier_from_pair_incidence",
    "ProductiveFrontierCertificate",
    "ProductiveFrontierJointCostReceipt",
    "build_productive_frontier",
    "bundle_resolves_from_productive_frontier",
    "productive_frontier_fixed_minimum_resolution",
    "productive_frontier_joint_cost_audit",
    "productive_frontier_sperner_bound",
    "verify_productive_frontier",
]
