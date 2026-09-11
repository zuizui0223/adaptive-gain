from __future__ import annotations

from itertools import product

import pytest

from adaptive_gain.local_routing_mutation import (
    RoutingPruningState,
    canonical_q2_k3_bridge_audit,
    exhaustive_minimum_local_prunings_for_gain,
    initial_full_program_state,
    minimum_local_prunings_for_gain,
    optimal_branch_specific_state,
    prune_one_occurrence,
    routing_pruning_accessibility_receipt,
)


def test_state_cost_and_gain_are_exact() -> None:
    state = RoutingPruningState(3, (3, 2, 1))
    assert state.fixed_task_cost == 4
    assert state.worst_path_cost == 4
    assert state.realized_structural_gain == 0
    assert state.optimal_task_gap == 2
    assert state.pruned_occurrences == 3

    state2 = RoutingPruningState(3, (2, 2, 1))
    assert state2.worst_path_cost == 3
    assert state2.realized_structural_gain == 1


def test_initial_and_optimal_states_match_extremal_family_endpoints() -> None:
    for k in range(2, 7):
        initial = initial_full_program_state(k)
        optimal = optimal_branch_specific_state(k)
        assert initial.branch_lengths == (k,) * k
        assert initial.worst_path_cost == k + 1
        assert initial.realized_structural_gain == 0
        assert optimal.branch_lengths == (1,) * k
        assert optimal.worst_path_cost == 2
        assert optimal.realized_structural_gain == k - 1


def test_one_pruning_changes_only_one_branch_and_preserves_valid_state() -> None:
    state = initial_full_program_state(4)
    nxt = prune_one_occurrence(state, 2)
    assert nxt.branch_lengths == (4, 4, 3, 4)
    assert nxt.pruned_occurrences == 1
    assert nxt.realized_structural_gain == 0


def test_exact_kr_mutation_distance_matches_independent_bfs() -> None:
    for k in range(2, 6):
        for required_gain in range(0, k):
            formula = minimum_local_prunings_for_gain(k, required_gain)
            exhaustive = exhaustive_minimum_local_prunings_for_gain(k, required_gain)
            assert formula == k * required_gain
            assert exhaustive == formula


def test_first_k_minus_one_edits_are_necessarily_neutral() -> None:
    for k in range(2, 6):
        # Every state reachable with at most k-1 deletions leaves at least one
        # branch at full length k, so worst-case cost has not improved.
        for lengths in product(range(1, k + 1), repeat=k):
            state = RoutingPruningState(k, tuple(lengths))
            if state.pruned_occurrences <= k - 1:
                assert state.realized_structural_gain == 0

        # k edits suffice: prune once in every branch.
        state = RoutingPruningState(k, (k - 1,) * k)
        assert state.pruned_occurrences == k
        assert state.realized_structural_gain == 1


def test_receipt_combines_static_exact_costs_with_local_accessibility() -> None:
    receipt = routing_pruning_accessibility_receipt(5, 3)
    assert receipt.world_count == 10
    assert receipt.query_count == 6
    assert receipt.task_adaptive_optimum == 2
    assert receipt.task_fixed_optimum == 6
    assert receipt.task_optimal_gap == 4
    assert receipt.minimum_local_prunings == 15
    assert receipt.target_max_branch_length == 2
    assert receipt.neutral_prefix_before_first_gain == 4
    assert receipt.theorem_holds is True


def test_canonical_q2_k3_bridge_hits_exact_pareto_frontier_and_six_edits() -> None:
    receipt = canonical_q2_k3_bridge_audit()
    assert receipt.branch_count == 3
    assert receipt.required_gain == 2
    assert receipt.world_count == 6
    assert receipt.query_count == 4
    assert receipt.task_adaptive_optimum == 2
    assert receipt.task_fixed_optimum == 4
    assert receipt.task_optimal_gap == 2
    assert receipt.minimum_local_prunings == 6
    assert receipt.neutral_prefix_before_first_gain == 2


def test_validation_rejects_out_of_scope_states_and_mutations() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        RoutingPruningState(1, (1,))
    with pytest.raises(ValueError, match="one entry per branch"):
        RoutingPruningState(3, (3, 3))
    with pytest.raises(ValueError, match=r"\[1,k\]"):
        RoutingPruningState(3, (3, 0, 2))
    with pytest.raises(ValueError, match="\[0,k-1\]"):
        minimum_local_prunings_for_gain(3, 3)
    with pytest.raises(ValueError, match="out of range"):
        prune_one_occurrence(initial_full_program_state(3), 3)
    with pytest.raises(ValueError, match="no irrelevant"):
        prune_one_occurrence(optimal_branch_specific_state(3), 0)
    with pytest.raises(ValueError, match="restricted"):
        exhaustive_minimum_local_prunings_for_gain(7, 1)
