from adaptive_gain.balanced_binary_cap_saturation_depth import (
    audit_exact_balanced_cap_saturation_depth,
    exact_balanced_cap_saturation_adaptive_depth,
    exact_balanced_cap_saturation_task,
)
from adaptive_gain.balanced_binary_fixed_cost_cap import (
    exact_balanced_binary_fixed_cost_cap_private_pairs,
)


def test_cap_saturation_depth_formula():
    assert exact_balanced_cap_saturation_adaptive_depth(8) == 3
    assert exact_balanced_cap_saturation_adaptive_depth(10) == 4
    assert exact_balanced_cap_saturation_adaptive_depth(12) == 5
    assert exact_balanced_cap_saturation_adaptive_depth(14) == 6


def test_cap_saturation_registered_private_edges_are_cross_target():
    for world_count in (8, 10, 12):
        task = exact_balanced_cap_saturation_task(world_count)
        pairs = exact_balanced_binary_fixed_cost_cap_private_pairs(world_count)
        assert len(task.queries) == world_count - 3
        assert all(task.worlds[a].target != task.worlds[b].target for a, b in pairs)


def test_cap_saturation_direct_exact_solver_audits():
    for world_count, pair in ((8, (3, 5)), (10, (4, 7)), (12, (5, 9))):
        receipt = audit_exact_balanced_cap_saturation_depth(world_count)
        assert (receipt.adaptive_cost, receipt.fixed_cost) == pair
        assert receipt.theorem_holds
