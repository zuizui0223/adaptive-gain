from fractions import Fraction

from adaptive_gain.balanced_quantity_topology_contrast import (
    balanced_quantity_matched_control_task,
    balanced_quantity_topology_contrast_audit,
)
from adaptive_gain.balanced_binary_extremal_family import (
    balanced_binary_extremal_task,
)


def test_quantity_matched_control_is_exact_no_gain_at_small_depths():
    for depth in (2, 3):
        receipt = balanced_quantity_topology_contrast_audit(depth, direct_check=True)
        k = 1 << depth

        assert receipt.theorem_holds
        assert receipt.same_world_names
        assert receipt.same_query_outcome_matrix
        assert receipt.same_query_marginals
        assert receipt.same_target_multiplicities
        assert receipt.routeable_target_multiplicities == (k + 2, k)
        assert receipt.control_target_multiplicities == (k + 2, k)
        assert receipt.same_target_entropy
        assert receipt.same_full_vocabulary_target_information

        assert receipt.control_adaptive_cost == 2
        assert receipt.control_fixed_cost == 2
        assert receipt.control_exact_no_gain

        assert receipt.direct_routeable_adaptive_cost is not None
        assert receipt.direct_routeable_fixed_cost is not None
        assert receipt.direct_routeable_adaptive_cost <= depth + 1
        assert receipt.direct_routeable_fixed_cost >= k


def test_control_changes_targets_only():
    depth = 3
    routeable = balanced_binary_extremal_task(depth)
    control = balanced_quantity_matched_control_task(depth)

    assert tuple(w.name for w in routeable.worlds) == tuple(w.name for w in control.worlds)
    assert routeable.queries == control.queries
    assert tuple(w.target for w in routeable.worlds) != tuple(
        w.target for w in control.worlds
    )


def test_control_target_is_equality_of_first_two_routing_bits():
    control = balanced_quantity_matched_control_task(3)
    route0, route1 = control.queries[:2]

    for i, world in enumerate(control.worlds):
        expected = 0 if route0.outcomes[i] == route1.outcomes[i] else 1
        assert world.target == expected


def test_matched_ratio_gap_is_unbounded_analytically():
    depths = (2, 3, 4, 6, 8)
    receipts = [
        balanced_quantity_topology_contrast_audit(depth, direct_check=False)
        for depth in depths
    ]

    assert [r.routeable_ratio_lower_bound for r in receipts] == [
        Fraction(4, 3),
        Fraction(2, 1),
        Fraction(16, 5),
        Fraction(64, 7),
        Fraction(256, 9),
    ]
    assert [r.matched_ratio_gap_lower_bound for r in receipts] == [
        Fraction(1, 3),
        Fraction(1, 1),
        Fraction(11, 5),
        Fraction(57, 7),
        Fraction(247, 9),
    ]
    assert [r.matched_ratio_gap_lower_bound for r in receipts] == sorted(
        r.matched_ratio_gap_lower_bound for r in receipts
    )


def test_matched_quantities_hold_analytically_beyond_solver_cap():
    receipt = balanced_quantity_topology_contrast_audit(8, direct_check=False)
    assert receipt.world_count == 514
    assert receipt.query_count == 264
    assert receipt.same_query_outcome_matrix
    assert receipt.same_query_marginals
    assert receipt.same_target_multiplicities
    assert receipt.same_target_entropy
    assert receipt.same_full_vocabulary_target_information
    assert receipt.control_adaptive_cost == 2
    assert receipt.control_fixed_cost == 2
