"""Print representative certificate-ladder outcomes.

Heavy exhaustive/partial-bypass validations live in pytest.  This CLI is a fast
CI smoke receipt showing one task for each important ladder outcome.
"""
from adaptive_gain import (
    adaptive_gain_receipt,
    optimal_policy_cost_decomposition,
    selected_policy_fractional_pair_packing_gain_certificate,
    selected_policy_integer_cover_gain_certificate,
    selected_policy_pair_packing_gain_certificate,
    selected_policy_private_pair_gain_certificate,
)
from adaptive_gain.witnesses import (
    fractional_integrality_gap_gain_control,
    fractional_only_gain_control,
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
    lp = fractional.fractional_packing
    print(label)
    print(
        "  costs:",
        f"C_A={exact.adaptive_cost}",
        f"C_F={exact.fixed_cost}",
        f"C_U={decomposition.policy_union_restricted_fixed_cost}",
        f"U={decomposition.policy_union_cost}",
    )
    print(
        "  certificates:",
        f"private={private.strict_adaptive_gain_certified_without_fixed_optimization}",
        f"integral={integral.strict_adaptive_gain_certified_without_fixed_optimization}",
        f"fractional={fractional.strict_adaptive_gain_certified_without_fixed_integer_optimization}",
        f"integer-proof={integer_proof.strict_adaptive_gain_certified_without_fixed_optimum}",
        f"LP={None if lp is None else lp.objective_exact}",
        f"ceilLP={None if lp is None else lp.integer_fixed_cost_lower_bound}",
        f"exact_gain={exact.strict_adaptive_gain}",
    )


for label, task in (
    ("private-pair source-derived control", payoff_routing_task()),
    ("fractional-only certificate control", fractional_only_gain_control()),
    ("LP integrality-gap strict-gain control", fractional_integrality_gap_gain_control()),
    ("routing bypass no-gain control", routing_bypass_control()),
):
    audit(label, task)
