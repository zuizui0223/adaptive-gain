"""Fail-closed validity gate for repeated ecological interaction responses.

This module does not estimate ecological effects. It classifies whether an
observed interaction-response surface is suitable for:

1. response feasibility only;
2. descriptive observed-link turnover;
3. detection-defensible ecological state analysis; or
4. a routeability bridge, which additionally requires an independent
   decision-structure exposure.

The gate is deliberately conservative. A predictor can generalize out of
sample while still predicting detection rather than latent ecological state.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ResponseValidity(str, Enum):
    NOT_ESTIMABLE = "not_estimable"
    FEASIBILITY_ONLY = "feasibility_only"
    OBSERVED_LINK_TURNOVER_ONLY = "observed_link_turnover_only"
    DETECTION_DEFENSIBLE_STATE = "detection_defensible_state"


@dataclass(frozen=True)
class NetworkResponseEvidence:
    response_reconstructable: bool
    response_nondegenerate: bool
    effort_semantics_resolved: bool
    binary_detection_audited: bool
    binary_detection_material: bool
    binary_state_detection_defensible: bool
    true_absence_independently_supported: bool
    effort_standardized_response_available: bool
    repeated_detection_model_available: bool
    repeated_detection_identifiable: bool
    state_effect_reproducible: bool
    observation_model_robust: bool
    independent_decision_layer: bool = False


@dataclass(frozen=True)
class NetworkResponseAssessment:
    response_validity: ResponseValidity
    routeability_bridge_eligible: bool
    reasons: tuple[str, ...]
    claim_ceiling: str


def assess_network_response_validity(
    evidence: NetworkResponseEvidence,
) -> NetworkResponseAssessment:
    """Classify a repeated interaction response using fail-closed rules."""

    reasons: list[str] = []

    if not evidence.response_reconstructable or not evidence.response_nondegenerate:
        reasons.append(
            "The declared interaction response is not reproducibly estimable."
        )
        return NetworkResponseAssessment(
            response_validity=ResponseValidity.NOT_ESTIMABLE,
            routeability_bridge_eligible=False,
            reasons=tuple(reasons),
            claim_ceiling=(
                "Do not interpret predictor effects because the response "
                "surface itself is not estimable."
            ),
        )

    if not evidence.effort_semantics_resolved:
        reasons.append(
            "Observation-effort semantics are unresolved."
        )
        return NetworkResponseAssessment(
            response_validity=ResponseValidity.FEASIBILITY_ONLY,
            routeability_bridge_eligible=False,
            reasons=tuple(reasons),
            claim_ceiling=(
                "Use the data only for response feasibility until observation "
                "effort is defined and audited."
            ),
        )

    if (
        not evidence.binary_detection_audited
        and not evidence.true_absence_independently_supported
    ):
        reasons.append(
            "Binary interaction detection has not been audited and true "
            "absence is not independently known."
        )
        return NetworkResponseAssessment(
            response_validity=(
                ResponseValidity.OBSERVED_LINK_TURNOVER_ONLY
            ),
            routeability_bridge_eligible=False,
            reasons=tuple(reasons),
            claim_ceiling=(
                "Describe zero/non-zero changes as observed-link turnover "
                "until imperfect detection is audited or true absence is "
                "independently supported."
            ),
        )

    if (
        evidence.binary_detection_audited
        and not evidence.binary_detection_material
        and not evidence.binary_state_detection_defensible
        and not evidence.true_absence_independently_supported
    ):
        reasons.append(
            "Detection was audited, but binary zero/non-zero states were not "
            "validated as defensible latent ecological states."
        )
        return NetworkResponseAssessment(
            response_validity=(
                ResponseValidity.OBSERVED_LINK_TURNOVER_ONLY
            ),
            routeability_bridge_eligible=False,
            reasons=tuple(reasons),
            claim_ceiling=(
                "Detection diagnostics may support descriptive robustness, "
                "but binary turnover cannot be promoted to latent ecological "
                "state change without an explicit state-validity argument."
            ),
        )

    detection_problem = (
        evidence.binary_detection_material
        and not evidence.true_absence_independently_supported
    )

    if detection_problem:
        reasons.append(
            "Binary zero/non-zero interaction states are materially "
            "detection-sensitive and true absence is not independently known."
        )

        detection_defensible = (
            evidence.effort_standardized_response_available
            and evidence.repeated_detection_model_available
            and evidence.repeated_detection_identifiable
            and evidence.state_effect_reproducible
            and evidence.observation_model_robust
        )

        if not detection_defensible:
            if not evidence.effort_standardized_response_available:
                reasons.append(
                    "No effort-standardized response is available."
                )
            if not evidence.repeated_detection_model_available:
                reasons.append(
                    "No repeated-detection state model is available."
                )
            elif not evidence.repeated_detection_identifiable:
                reasons.append(
                    "The repeated-detection model is not sufficiently "
                    "identified for the declared state contrast."
                )
            if not evidence.state_effect_reproducible:
                reasons.append(
                    "The ecological state-side effect is not reproducible "
                    "under the frozen rule."
                )
            if not evidence.observation_model_robust:
                reasons.append(
                    "Latent-state conclusions are sensitive to the observation "
                    "model."
                )

            return NetworkResponseAssessment(
                response_validity=(
                    ResponseValidity.OBSERVED_LINK_TURNOVER_ONLY
                ),
                routeability_bridge_eligible=False,
                reasons=tuple(reasons),
                claim_ceiling=(
                    "Describe zero/non-zero changes as observed-link turnover "
                    "or detection-sensitive interaction observations, not as "
                    "identified ecological rewiring."
                ),
            )

    # Either detection was not material, true absence was independently
    # supported, or all detection-defensibility conditions were satisfied.
    reasons.append(
        "The declared ecological state response passes the response-side "
        "detection gate."
    )

    if not evidence.independent_decision_layer:
        reasons.append(
            "No independent decision-structure exposure is available."
        )
        return NetworkResponseAssessment(
            response_validity=ResponseValidity.DETECTION_DEFENSIBLE_STATE,
            routeability_bridge_eligible=False,
            reasons=tuple(reasons),
            claim_ceiling=(
                "Ecological state analysis may proceed, but routeability "
                "cannot be tested without an independent decision layer."
            ),
        )

    reasons.append(
        "An independent decision-structure exposure is available."
    )
    return NetworkResponseAssessment(
        response_validity=ResponseValidity.DETECTION_DEFENSIBLE_STATE,
        routeability_bridge_eligible=True,
        reasons=tuple(reasons),
        claim_ceiling=(
            "A routeability bridge is empirically eligible, subject to the "
            "predeclared ecological analysis and causal-design limits."
        ),
    )
