from adaptive_gain import (
    adaptive_gain_receipt,
    adaptive_minimum_resolution,
    best_fixed_information_bits,
    routing_certificate,
    routing_information_receipt,
)
from adaptive_gain.witnesses import (
    balance_no_routing_certificates,
    mrod_routing_task,
    payoff_routing_task,
)

for label, task, root in (
    ("MROD-style", mrod_routing_task(), "context"),
    ("PAYOFF-style", payoff_routing_task(), "intrinsic_r_0.5"),
):
    gain = adaptive_gain_receipt(task)
    policy = adaptive_minimum_resolution(task).selected_policy
    info = routing_information_receipt(task, policy)
    route = routing_certificate(task, root, 2)
    print(label)
    print("  costs:", gain.adaptive_cost, gain.fixed_cost)
    print("  adaptive-only budget:", gain.adaptive_only_budget_lower)
    print("  root direct target info:", info.root_direct_target_information_bits)
    print("  policy target info:", info.total_policy_target_information_bits)
    print("  best fixed info at B=2:", best_fixed_information_bits(task, 2))
    print("  branch next actions:", [b.selected_next_query for b in route.branches])

print("BALANCE-style branch invariance:")
for certificate in balance_no_routing_certificates():
    print(" ", certificate.branch_invariant, certificate.interpretation)
