import pytest

from adaptive_gain.routeability_material_pretest import (
    qualify_material_pretest,
)


def _spec():
    return {
        "material_set_id": "materials-v1",
        "cue_roles": {
            "q_route": {"description": "context"},
            "q_left": {"description": "terminal A"},
            "q_right": {"description": "terminal B"},
        },
    }


def _rows(final_correct=(16, 17, 18), *, n=24):
    rows = []
    for cue, correct_count in zip(
        ("q_route", "q_left", "q_right"),
        final_correct,
    ):
        prefix_n = n - 20
        for index in range(1, prefix_n + 1):
            rows.append(
                {
                    "material_set_id": "materials-v1",
                    "individual_id": f"{cue}-bee-{index}",
                    "cue_identity": cue,
                    "sequence_index": index,
                    "correct": 1,
                    "architecture_neutral": True,
                    "confirmatory_roster_member": False,
                }
            )
        for offset in range(20):
            rows.append(
                {
                    "material_set_id": "materials-v1",
                    "individual_id": f"{cue}-bee-final-{offset}",
                    "cue_identity": cue,
                    "sequence_index": prefix_n + offset + 1,
                    "correct": int(offset < correct_count),
                    "architecture_neutral": True,
                    "confirmatory_roster_member": False,
                }
            )
    return rows


def _qualify(rows):
    return qualify_material_pretest(
        rows,
        material_spec=_spec(),
        trial_log_sha256="a" * 64,
        material_spec_sha256="b" * 64,
    )


def test_material_pretest_passes_frozen_accuracy_and_salience_rule():
    receipt = _qualify(_rows((16, 17, 18)))
    assert receipt["qualified"] is True
    assert receipt["status"] == "PASS_material_set_qualified"
    assert receipt["cue_results"]["q_route"]["final20_accuracy"] == 0.80
    assert receipt["cue_results"]["q_left"]["final20_accuracy"] == 0.85
    assert receipt["cue_results"]["q_right"]["final20_accuracy"] == 0.90
    assert receipt["final20_accuracy_spread"] == pytest.approx(0.10)


def test_material_pretest_fails_when_one_cue_is_below_80_percent():
    receipt = _qualify(_rows((15, 17, 18)))
    assert receipt["qualified"] is False
    assert receipt["all_cues_meet_accuracy"] is False
    assert receipt["status"] == "FAIL_material_set_not_qualified"


def test_material_pretest_fails_when_salience_spread_exceeds_point_one():
    receipt = _qualify(_rows((16, 16, 19)))
    assert receipt["qualified"] is False
    assert receipt["all_cues_meet_accuracy"] is True
    assert receipt["salience_balance_pass"] is False


def test_material_pretest_rejects_confirmatory_roster_member():
    rows = _rows()
    rows[0]["confirmatory_roster_member"] = True
    with pytest.raises(ValueError, match="confirmatory-roster"):
        _qualify(rows)


def test_material_pretest_rejects_non_neutral_pretest():
    rows = _rows()
    rows[0]["architecture_neutral"] = False
    with pytest.raises(ValueError, match="architecture-neutral"):
        _qualify(rows)


def test_material_pretest_requires_all_three_roles_and_twenty_choices():
    bad_spec = _spec()
    bad_spec["cue_roles"].pop("q_right")
    with pytest.raises(ValueError, match="exactly"):
        qualify_material_pretest(
            _rows(),
            material_spec=bad_spec,
            trial_log_sha256="a" * 64,
            material_spec_sha256="b" * 64,
        )

    short = [
        row
        for row in _rows()
        if not (
            row["cue_identity"] == "q_route"
            and row["sequence_index"] > 19
        )
    ]
    with pytest.raises(ValueError, match="at least 20"):
        _qualify(short)
