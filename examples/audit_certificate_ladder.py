"""Print which fixed-cost certificate layer proves each registered control.

All tasks are synthetic/structural. `exact_gain` is computed by the full fixed
bundle optimizer and is used only as the reference truth in this audit script.
"""
from adaptive_gain import (
    adaptive_gain_receipt,
    exact_fractional_pair_packing,
    optimal_policy_cost_decomposition,
    selected_policy_fractional_pair_packing_gain_certificate,
    selected_policy_integer_cover_gain_certificate,
    selected_policy_pair_packing_gain_certificate,
    selected_policy_private_pair_gain_certificate,
)
from adaptive_gain.witnesses import (
    fractional_integrality_gap_gain_control,
    fractional_only_gain_control,
    mrod_routing_task,
    partial_external_bypass_gain_control,
    partial_internal_bypass_gain_control,
    payoff_routing_task,
    routing_bypass_control,
)


def audit(label, task):
    exact = adaptive_gain_receipt(task)
    decomposition = optimal_policy_cost_decomposition(task)
    private = selected_policy_private_pair_gain_certificate(task)
    integral = selected_policy_pair_packing_gain_certificate(task)
    fractional = selected_policy_fractional_pair_packing_gain_certificate(task)
    integer_proof = selected_policy_integer_cover_gain_certificate(task)
    lp = exact_fractional_pair_packing(task)
    print(label)
    print(
        "  costs:",
        f"C_A={exact.adaptive_cost}",
        f"C_F={exact.fixed_cost}",
        f"C_U={decomposition.policy_union_restricted_fixed_cost}",
        f"U={decomposition.policy_union_cost}",
    )
    print(
        "  decomposition:",
        f"gain={decomposition.realized_adaptive_gain}",
        f"internal={decomposition.internal_union_redundancy}",
        f"external={decomposition.external_shortcut_discount}",
    )
    print(
        "  certificates:",
        f"private={private.strict_adaptive_gain_certified_without_fixed_optimization}",
        f"integral={integral.strict_adaptive_gain_certified_without_fixed_optimization}",
        f"fractional={fractional.strict_adaptive_gain_certified_without_fixed_integer_optimization}",
        f"integer-proof={integer_proof.strict_adaptive_gain_certified_without_fixed_optimum}",
        f"LP={lp.objective_exact}",
        f"ceilLP={lp.integer_fixed_cost_lower_bound}",
        f"exact_gain={exact.strict_adaptive_gain}",
    )


for label, task in (
    ("MROD source-derived routing", mrod_routing_task()),
    ("PAYOFF source-derived routing", payoff_routing_task()),
    ("partial internal bypass with residual gain", partial_internal_bypass_gain_control()),
    ("partial external bypass with residual gain", partial_external_bypass_gain_control()),
    ("fractional-only certificate control", fractional_only_gain_control()),
    ("LP integrality-gap strict-gain control", fractional_integrality_gap_gain_control()),
    ("routing bypass no-gain control", routing_bypass_control()),
):
    audit(label, task)
