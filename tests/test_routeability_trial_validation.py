import pytest

from adaptive_gain.routeability_experiment_schedule import (
    build_between_subject_routeability_schedule,
)
from adaptive_gain.routeability_trial_validation import (
    ObservedRouteabilityTrial,
    validate_routeability_trial_batch,
    validate_routeability_trial_log,
)


def _planned_b2_contingent():
    trials = build_between_subject_routeability_schedule(
        individuals_per_cell=4,
        blocks_per_individual=1,
        seed=20260927,
    )
    return next(
        row for row in trials
        if row.architecture == "routeable"
        and row.access_mode == "contingent"
        and row.budget == 2
    )


def _observed(planned, **overrides):
    payload = {
        "individual_id": planned.individual_id,
        "trial_index": planned.trial_index,
        "revealed_cues": planned.revealed_cues,
        "cue_durations_seconds": tuple(1.0 for _ in planned.revealed_cues),
        "context_persisted_during_terminal": True,
        "terminal_decision": int(planned.target),
        "response_latency_seconds": 1.0,
        "apparatus_error": False,
    }
    payload.update(overrides)
    return ObservedRouteabilityTrial(**payload)


def _validate(planned, observed):
    return validate_routeability_trial_log(
        planned,
        observed,
        response_window_seconds=3.0,
        nominal_cue_duration_seconds=1.0,
        cue_duration_tolerance_seconds=0.1,
    )


def test_valid_correct_trial_scores_one():
    planned = _planned_b2_contingent()
    result = _validate(planned, _observed(planned))
    assert result.protocol_valid
    assert result.protocol_errors == ()
    assert result.biological_timeout is False
    assert result.primary_success_score == 1


def test_wrong_choice_and_timeout_are_valid_biological_zeroes():
    planned = _planned_b2_contingent()
    wrong = _validate(
        planned,
        _observed(planned, terminal_decision=1 - int(planned.target)),
    )
    assert wrong.protocol_valid
    assert wrong.biological_timeout is False
    assert wrong.primary_success_score == 0

    timeout = _validate(
        planned,
        _observed(
            planned,
            terminal_decision=None,
            response_latency_seconds=None,
        ),
    )
    assert timeout.protocol_valid
    assert timeout.biological_timeout is True
    assert timeout.primary_success_score == 0


def test_protocol_errors_are_not_silently_scored_as_biological_failures():
    planned = _planned_b2_contingent()
    apparatus = _validate(
        planned,
        _observed(planned, apparatus_error=True),
    )
    assert not apparatus.protocol_valid
    assert "apparatus_error" in apparatus.protocol_errors
    assert apparatus.primary_success_score is None

    missing_context = _validate(
        planned,
        _observed(planned, context_persisted_during_terminal=False),
    )
    assert not missing_context.protocol_valid
    assert "context_not_persistent_during_terminal" in missing_context.protocol_errors
    assert missing_context.primary_success_score is None


def test_cue_sequence_and_duration_are_machine_checked():
    planned = _planned_b2_contingent()
    wrong_sequence = _validate(
        planned,
        _observed(planned, revealed_cues=tuple(reversed(planned.revealed_cues))),
    )
    assert not wrong_sequence.protocol_valid
    assert "revealed_cue_sequence_mismatch" in wrong_sequence.protocol_errors

    bad_duration = _validate(
        planned,
        _observed(
            planned,
            cue_durations_seconds=tuple(2.0 for _ in planned.revealed_cues),
        ),
    )
    assert not bad_duration.protocol_valid
    assert "cue_duration_out_of_tolerance" in bad_duration.protocol_errors


def test_response_after_window_is_timeout_not_exclusion():
    planned = _planned_b2_contingent()
    result = _validate(
        planned,
        _observed(planned, response_latency_seconds=4.0),
    )
    assert result.protocol_valid
    assert result.biological_timeout is True
    assert result.primary_success_score == 0


def test_batch_requires_exact_planned_trial_keys():
    planned = build_between_subject_routeability_schedule(
        individuals_per_cell=4,
        blocks_per_individual=1,
        seed=1,
    )[:2]
    observed = [_observed(planned[0])]
    with pytest.raises(ValueError, match="do not match plan"):
        validate_routeability_trial_batch(
            planned,
            observed,
            response_window_seconds=3.0,
            nominal_cue_duration_seconds=1.0,
            cue_duration_tolerance_seconds=0.1,
        )
