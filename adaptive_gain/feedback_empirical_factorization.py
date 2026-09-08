"""Empirical factorization ladder for the inverse feedback model.

The inverse transient identifies the closed-loop invariant

    L = (-eta) * Delta_s * p_star * (1-p_star),

where ``eta<0`` is ecological feedback slope and ``Delta_s>0`` is the
state-specific log-fitness selection contrast.

This module keeps the empirical ladder explicit:

1. transient geometry -> L and phi (handled in ``feedback_inverse_diagnostics``);
2. independently measured eta and p_star -> Delta_s;
3. direct fitness measurements can test that inferred Delta_s;
4. only after a structural gap Delta_g is independently specified or inferred
   does the continuous lift ``Delta_s=lambda*Delta_g`` identify lambda.

The algebra is elementary.  The purpose is to prevent the structural gap from
being inferred before the nonstructural factors have been independently
constrained.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class SelectionContrastInference:
    loop_gain: float
    feedback_strength: float
    equilibrium_frequency: float
    evolutionary_response: float
    inferred_selection_contrast: float


@dataclass(frozen=True)
class FeedbackStrengthInference:
    loop_gain: float
    selection_contrast: float
    equilibrium_frequency: float
    evolutionary_response: float
    inferred_feedback_strength: float


@dataclass(frozen=True)
class FitnessScalingInference:
    selection_contrast: float
    structural_gap: float
    inferred_lambda_cost: float


def evolutionary_response(equilibrium_frequency: float) -> float:
    """Return p*(1-p*), the local logit-to-frequency response factor."""

    p = float(equilibrium_frequency)
    if not isfinite(p) or not 0.0 < p < 1.0:
        raise ValueError("equilibrium_frequency must lie strictly inside (0,1)")
    return p * (1.0 - p)


def infer_selection_contrast_from_loop_gain(
    loop_gain: float,
    *,
    feedback_strength: float,
    equilibrium_frequency: float,
) -> SelectionContrastInference:
    """Infer Delta_s from L after eta and p* are independently measured.

    Uses

        Delta_s = L / [(-eta) p*(1-p)].

    The restoring model requires eta<0 and Delta_s>=0.
    """

    L = float(loop_gain)
    eta = float(feedback_strength)
    if not isfinite(L) or L < 0.0:
        raise ValueError("loop_gain must be finite and non-negative")
    if not isfinite(eta) or eta >= 0.0:
        raise ValueError("feedback_strength must be finite and negative")
    response = evolutionary_response(equilibrium_frequency)
    contrast = L / ((-eta) * response)
    return SelectionContrastInference(
        loop_gain=L,
        feedback_strength=eta,
        equilibrium_frequency=float(equilibrium_frequency),
        evolutionary_response=response,
        inferred_selection_contrast=contrast,
    )


def infer_feedback_strength_from_loop_gain(
    loop_gain: float,
    *,
    selection_contrast: float,
    equilibrium_frequency: float,
) -> FeedbackStrengthInference:
    """Infer eta from L after Delta_s and p* are independently measured.

    Uses

        eta = -L / [Delta_s p*(1-p)].
    """

    L = float(loop_gain)
    contrast = float(selection_contrast)
    if not isfinite(L) or L < 0.0:
        raise ValueError("loop_gain must be finite and non-negative")
    if not isfinite(contrast) or contrast <= 0.0:
        raise ValueError("selection_contrast must be finite and positive")
    response = evolutionary_response(equilibrium_frequency)
    eta = -L / (contrast * response)
    return FeedbackStrengthInference(
        loop_gain=L,
        selection_contrast=contrast,
        equilibrium_frequency=float(equilibrium_frequency),
        evolutionary_response=response,
        inferred_feedback_strength=eta,
    )


def infer_lambda_from_selection_and_structural_gap(
    selection_contrast: float,
    structural_gap: float,
) -> FitnessScalingInference:
    """Calibrate lambda in Delta_s=lambda*Delta_g after Delta_g is specified.

    This is deliberately downstream of the direct selection-contrast check.
    A positive structural gap is required; gap zero cannot explain a positive
    selection contrast under the continuous structural lift.
    """

    contrast = float(selection_contrast)
    gap = float(structural_gap)
    if not isfinite(contrast) or contrast < 0.0:
        raise ValueError("selection_contrast must be finite and non-negative")
    if not isfinite(gap) or gap <= 0.0:
        raise ValueError("structural_gap must be finite and positive")
    lam = contrast / gap
    return FitnessScalingInference(
        selection_contrast=contrast,
        structural_gap=gap,
        inferred_lambda_cost=lam,
    )


def reconstructed_loop_gain(
    *,
    feedback_strength: float,
    selection_contrast: float,
    equilibrium_frequency: float,
) -> float:
    """Forward cross-check L=(-eta)*Delta_s*p*(1-p)."""

    eta = float(feedback_strength)
    contrast = float(selection_contrast)
    if not isfinite(eta) or eta >= 0.0:
        raise ValueError("feedback_strength must be finite and negative")
    if not isfinite(contrast) or contrast < 0.0:
        raise ValueError("selection_contrast must be finite and non-negative")
    response = evolutionary_response(equilibrium_frequency)
    return (-eta) * contrast * response
