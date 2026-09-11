from __future__ import annotations

from itertools import product

import pytest

from adaptive_gain.local_routing_mutation import RoutingPruningState
from adaptive_gain.local_routing_mutation_radius import (
    balanced_strict_improvement_path,
    minimum_one_step_edit_radius_for_gain,
    minimum_radius_for_first_strict_gain,
    one_step_gain_reachable,
    routing_mutation_radius_receipt,
    strict_improvement_path_exists,
)


def _one_step_states_from_full(k: int, rho: int):
    # Enumerate deletion-count vectors d_i in [0,k-1] with L1 radius <=rho.
    for deletions in product(range(k), repeat=k):
        if sum(deletions) <= rho:
            yield RoutingPruningState(k, tuple(k - d for d in deletions))


def test_direct_gain_radius_matches_exhaustive_one_step_enumeration() -> None:
    for k in range(2, 6):
        for r in range(1, k):
            exact = minimum_one_step_edit_radius_for_gain(k, r)
            assert exact == k * r
            for rho in range(1, exact + 2):
                observed = any(
                    state.realized_structural_gain >= r
                    for state in _one_step_states_from_full(k, rho)
                )
                assert one_step_gain_reachable(k, r, rho) is observed
                assert observed is (rho >= exact)


def test_first_strict_gain_radius_is_branch_count() -> None:
    for k in range(2, 8):
        assert minimum_radius_for_first_strict_gain(k) == k
        assert strict_improvement_path_exists(k, 1, k - 1) is False
        assert strict_improvement_path_exists(k, 1, k) is True


def test_balanced_radius_k_path_gains_one_per_event() -> None:
    for k in range(2, 7):
        for r in range(1, k):
            path = balanced_strict_improvement_path(k, r, k)
            assert len(path) == r + 1
            assert [state.realized_structural_gain for state in path] == list(range(r + 1))
            for before, after in zip(path, path[1:]):
                elementary_edits = sum(
                    a - b
                    for a, b in zip(
                        before.branch_lengths,
                        after.branch_lengths,
                        strict=True,
                    )
                )
                assert elementary_edits == k
                assert after.realized_structural_gain == before.realized_structural_gain + 1


def test_radius_receipt_separates_first_gain_and_direct_target_thresholds() -> None:
    receipt = routing_mutation_radius_receipt(3, 2)
    assert receipt.first_strict_gain_radius == 3
    assert receipt.direct_target_radius == 6
    assert receipt.unit_edit_strictly_trapped is True
    assert receipt.balanced_strict_path_radius == 3
    assert receipt.balanced_strict_path_steps == 2


def test_required_gap_minimal_star_radius_scaling() -> None:
    for q in range(1, 7):
        k = q + 1
        receipt = routing_mutation_radius_receipt(k, q)
        assert receipt.first_strict_gain_radius == q + 1
        assert receipt.direct_target_radius == q * (q + 1)
        assert receipt.balanced_strict_path_steps == q


def test_radius_validation() -> None:
    with pytest.raises(ValueError, match="positive integer"):
        one_step_gain_reachable(3, 1, 0)
    with pytest.raises(ValueError, match="too small"):
        balanced_strict_improvement_path(3, 1, 2)
