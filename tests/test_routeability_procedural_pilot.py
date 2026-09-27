import pytest

from adaptive_gain.routeability_procedural_pilot import (
    FullInformationPilotTrial,
    freeze_response_window,
    pooled_full_information_nuisance_receipt,
)


def test_response_window_uses_smallest_prespecified_candidate_reaching_95_percent():
    latencies = [1.0] * 19 + [4.0]
    selected = freeze_response_window(
        latencies,
        candidate_windows=(1.0, 2.0, 3.0, 4.0),
        required_coverage=0.95,
        upper_bound=4.0,
    )
    assert selected == 1.0


def test_response_window_fails_if_prespecified_grid_is_insufficient():
    with pytest.raises(ValueError, match="no prespecified candidate response window"):
        freeze_response_window(
            [1.0, 1.0, 10.0],
            candidate_windows=(1.0, 2.0),
            required_coverage=0.95,
            upper_bound=2.0,
        )


def test_pooled_full_information_receipt_contains_no_focal_contrast():
    rows = [
        FullInformationPilotTrial("i1", "c1", True, False, 1),
        FullInformationPilotTrial("i1", "c1", False, True, 2),
        FullInformationPilotTrial("i2", "c2", True, False, 1),
        FullInformationPilotTrial("i2", "c2", True, False, 2),
    ]
    receipt = pooled_full_information_nuisance_receipt(rows)

    assert receipt["focal_architecture_contrast_opened"] is False
    assert receipt["trial_count"] == 4
    assert receipt["individual_count"] == 2
    assert receipt["colony_count"] == 2
    assert receipt["pooled_success_fraction"] == 0.75
    assert receipt["pooled_timeout_fraction"] == 0.25
    assert set(receipt["block_summary"]) == {"1", "2"}
    assert "architecture" not in receipt
    assert "access" not in receipt
    assert "H1" not in receipt
    assert "H2" not in receipt


def test_timeout_cannot_be_scored_correct():
    with pytest.raises(ValueError, match="timeout cannot also be correct"):
        pooled_full_information_nuisance_receipt(
            [FullInformationPilotTrial("i1", "c1", True, True, 1)]
        )


def test_response_window_grid_must_be_frozen_ordered_and_within_bound():
    with pytest.raises(ValueError, match="strictly increasing"):
        freeze_response_window(
            [1.0, 2.0],
            candidate_windows=(2.0, 1.0),
            upper_bound=2.0,
        )
    with pytest.raises(ValueError, match="exceeds"):
        freeze_response_window(
            [1.0, 2.0],
            candidate_windows=(1.0, 3.0),
            upper_bound=2.0,
        )
