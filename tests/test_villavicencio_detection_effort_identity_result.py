import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = (
    ROOT
    / "validation"
    / "villavicencio_detection_effort_identity_result_v1.json"
)


def _result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_detection_identity_direction_is_strong_in_all_six_transitions():
    data = _result()
    assert data["status"] == (
        "observed_gain_loss_direction_strongly_aligned_with_detection_map"
    )
    assert (
        data["all_six_transitions"][
            "auc_detection_q_difference_gain_over_loss"
        ]
        > 0.85
    )
    assert all(
        value > 0.7
        for value in data[
            "per_transition_auc_detection_q_difference"
        ].values()
    )


def test_identified_subset_keeps_strong_detection_direction_alignment():
    data = _result()["identified_five_transition_subset"]
    assert data["changed_rows"] == 357
    assert data["observed_gain"] == 151
    assert data["observed_loss"] == 206
    assert data["auc_detection_q_difference_gain_over_loss"] > 0.83


def test_detection_identity_result_is_not_promoted_as_ecological_prediction():
    data = _result()
    assert "not an independent ecological prediction model" in data[
        "analysis_status"
    ]
    assert "biological fraction of observed turnover" in data[
        "not_established"
    ]
    ceiling = data["claim_ceiling"].lower()
    assert "rewiring-identification boundary" in ceiling
    assert "corrected ecological rewiring" in ceiling
