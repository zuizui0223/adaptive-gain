"""Protocol validation for observed routeability experiment trial logs.

The validator compares an observed trial against the machine-frozen schedule.
It separates protocol validity from biological success: cue-presentation or
apparatus errors invalidate a trial according to prespecified rules, whereas
incorrect choices and timeouts remain valid biological outcomes scored zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence

from .routeability_experiment_schedule import RouteabilityTrial


@dataclass(frozen=True)
class ObservedRouteabilityTrial:
    individual_id: str
    trial_index: int
    revealed_cues: tuple[str, ...]
    cue_durations_seconds: tuple[float, ...]
    context_persisted_during_terminal: bool | None
    terminal_decision: int | None
    response_latency_seconds: float | None
    apparatus_error: bool = False


@dataclass(frozen=True)
class RouteabilityTrialValidation:
    individual_id: str
    trial_index: int
    protocol_valid: bool
    protocol_errors: tuple[str, ...]
    biological_timeout: bool | None
    terminal_response_observed: bool | None
    primary_success_score: int | None
    target: object


def validate_routeability_trial_log(
    planned: RouteabilityTrial,
    observed: ObservedRouteabilityTrial,
    *,
    response_window_seconds: float,
    nominal_cue_duration_seconds: float,
    cue_duration_tolerance_seconds: float,
) -> RouteabilityTrialValidation:
    """Validate one observed trial against its frozen planned schedule."""

    window = float(response_window_seconds)
    nominal = float(nominal_cue_duration_seconds)
    tolerance = float(cue_duration_tolerance_seconds)
    if not isfinite(window) or window <= 0:
        raise ValueError("response_window_seconds must be finite and positive")
    if not isfinite(nominal) or nominal <= 0:
        raise ValueError("nominal_cue_duration_seconds must be finite and positive")
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError("cue_duration_tolerance_seconds must be finite and non-negative")

    errors: list[str] = []
    if observed.individual_id != planned.individual_id:
        errors.append("individual_id_mismatch")
    if observed.trial_index != planned.trial_index:
        errors.append("trial_index_mismatch")
    if observed.revealed_cues != planned.revealed_cues:
        errors.append("revealed_cue_sequence_mismatch")

    if len(observed.cue_durations_seconds) != len(observed.revealed_cues):
        errors.append("cue_duration_count_mismatch")
    else:
        for duration in observed.cue_durations_seconds:
            value = float(duration)
            if not isfinite(value) or value <= 0:
                errors.append("invalid_cue_duration")
                break
            if abs(value - nominal) > tolerance:
                errors.append("cue_duration_out_of_tolerance")
                break

    requires_persistent_context = (
        "q_route" in planned.revealed_cues
        and len(planned.revealed_cues) >= 2
    )
    if requires_persistent_context and observed.context_persisted_during_terminal is not True:
        errors.append("context_not_persistent_during_terminal")

    if observed.terminal_decision not in (None, 0, 1):
        errors.append("invalid_terminal_decision")
    if observed.response_latency_seconds is not None:
        latency = float(observed.response_latency_seconds)
        if not isfinite(latency) or latency < 0:
            errors.append("invalid_response_latency")

    if observed.apparatus_error:
        errors.append("apparatus_error")

    protocol_valid = not errors
    if not protocol_valid:
        return RouteabilityTrialValidation(
            individual_id=planned.individual_id,
            trial_index=planned.trial_index,
            protocol_valid=False,
            protocol_errors=tuple(errors),
            biological_timeout=None,
            terminal_response_observed=None,
            primary_success_score=None,
            target=planned.target,
        )

    latency = observed.response_latency_seconds
    timely_response = (
        observed.terminal_decision is not None
        and latency is not None
        and float(latency) <= window
    )
    timeout = not timely_response
    if timeout:
        score = 0
    else:
        score = int(int(observed.terminal_decision) == int(planned.target))

    return RouteabilityTrialValidation(
        individual_id=planned.individual_id,
        trial_index=planned.trial_index,
        protocol_valid=True,
        protocol_errors=(),
        biological_timeout=timeout,
        terminal_response_observed=timely_response,
        primary_success_score=score,
        target=planned.target,
    )


def validate_routeability_trial_batch(
    planned_trials: Sequence[RouteabilityTrial],
    observed_trials: Sequence[ObservedRouteabilityTrial],
    *,
    response_window_seconds: float,
    nominal_cue_duration_seconds: float,
    cue_duration_tolerance_seconds: float,
) -> tuple[RouteabilityTrialValidation, ...]:
    """Validate a complete batch by exact (individual_id, trial_index) keys."""

    planned = {(row.individual_id, row.trial_index): row for row in planned_trials}
    observed = {(row.individual_id, row.trial_index): row for row in observed_trials}
    if len(planned) != len(planned_trials):
        raise ValueError("planned trial keys are not unique")
    if len(observed) != len(observed_trials):
        raise ValueError("observed trial keys are not unique")

    missing = sorted(set(planned) - set(observed))
    extra = sorted(set(observed) - set(planned))
    if missing or extra:
        raise ValueError(
            f"observed trial keys do not match plan; missing={missing!r}, extra={extra!r}"
        )

    return tuple(
        validate_routeability_trial_log(
            planned[key],
            observed[key],
            response_window_seconds=response_window_seconds,
            nominal_cue_duration_seconds=nominal_cue_duration_seconds,
            cue_duration_tolerance_seconds=cue_duration_tolerance_seconds,
        )
        for key in sorted(planned)
    )
