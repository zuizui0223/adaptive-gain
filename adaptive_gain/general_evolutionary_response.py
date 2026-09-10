"""General local evolutionary response for structural eco-evolutionary feedback.

The original endogenous-feedback model uses the haploid logit update

    z[t+1] = z[t] + s(q[t]),

which fixes the local evolutionary self-derivative and selection response to one.
This module replaces that special update by a generic differentiable local map

    x[t+1] = F(x[t], s(q[t]))

around an interior equilibrium where ``s(q*)=0``.

Define

    alpha = dF/dx              intrinsic evolutionary persistence,
    beta  = dF/ds              local response to selection,
    ds    = ds/dq              state-selection slope,
    e     = d q_target / dx    ecological feedback slope,
    phi   = community memory.

The local Jacobian is

    J = [[alpha, beta*ds],
         [(1-phi)*e, phi]].

Define generalized closed-loop gain

    G = -beta * ds * e.

Then

    trace = alpha + phi,
    determinant = alpha*phi + (1-phi)*G.

For the main biological domain ``0<=alpha<=1`` and ``0<=phi<1``, the exact Jury
stability interval is

    alpha - 1 < G < (1-alpha*phi)/(1-phi).

The eigenvalues are complex exactly when

    G > (alpha-phi)^2 / [4(1-phi)].

The original haploid-logit model is recovered by ``alpha=beta=1`` and
``e=eta*p*(1-p)``, making ``G=L`` and recovering the parent bounds
``0<L<1`` and ``L>(1-phi)/4``.

The generic local-linear algebra is standard.  The repository-specific link is
that ``ds`` may be generated from the exact adaptive/fixed structural gap via
``ds=lambda_cost*Delta_g``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, inf, isfinite, log, pi, sqrt

_TOL = 1e-12


@dataclass(frozen=True)
class GeneralResponseThresholds:
    evolutionary_persistence: float
    community_memory: float
    lower_stability_gain: float
    upper_stability_gain: float
    oscillation_gain: float
    upper_boundary_period: float


@dataclass(frozen=True)
class GeneralResponseSummary:
    evolutionary_persistence: float
    selection_responsiveness: float
    selection_contrast: float
    ecological_feedback_slope: float
    community_memory: float
    loop_gain: float
    trace: float
    determinant: float
    discriminant: float
    eigenvalues: tuple[complex, complex]
    locally_stable: bool
    oscillatory: bool
    regime: str


def _validate_alpha_phi(alpha: float, phi: float) -> tuple[float, float]:
    a = float(alpha)
    p = float(phi)
    if not isfinite(a) or not 0.0 <= a <= 1.0:
        raise ValueError("evolutionary_persistence must lie in [0,1]")
    if not isfinite(p) or not 0.0 <= p < 1.0:
        raise ValueError("community_memory must lie in [0,1)")
    return a, p


def generalized_loop_gain(
    *,
    selection_responsiveness: float,
    selection_contrast: float,
    ecological_feedback_slope: float,
) -> float:
    """Return G=-beta*Delta_s*e."""

    beta = float(selection_responsiveness)
    ds = float(selection_contrast)
    e = float(ecological_feedback_slope)
    if not isfinite(beta) or beta < 0.0:
        raise ValueError("selection_responsiveness must be finite and non-negative")
    if not isfinite(ds) or ds < 0.0:
        raise ValueError("selection_contrast must be finite and non-negative")
    if not isfinite(e):
        raise ValueError("ecological_feedback_slope must be finite")
    return -beta * ds * e


def general_response_thresholds(
    evolutionary_persistence: float,
    community_memory: float,
) -> GeneralResponseThresholds:
    """Exact local gain thresholds for 0<=alpha<=1 and 0<=phi<1."""

    alpha, phi = _validate_alpha_phi(evolutionary_persistence, community_memory)
    lower = alpha - 1.0
    upper = (1.0 - alpha * phi) / (1.0 - phi)
    oscillation = (alpha - phi) ** 2 / (4.0 * (1.0 - phi))
    theta = acos((alpha + phi) / 2.0)
    period = 2.0 * pi / theta
    return GeneralResponseThresholds(
        evolutionary_persistence=alpha,
        community_memory=phi,
        lower_stability_gain=lower,
        upper_stability_gain=upper,
        oscillation_gain=oscillation,
        upper_boundary_period=period,
    )


def general_response_jacobian(
    *,
    evolutionary_persistence: float,
    selection_responsiveness: float,
    selection_contrast: float,
    ecological_feedback_slope: float,
    community_memory: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Return the exact local 2x2 Jacobian."""

    alpha, phi = _validate_alpha_phi(evolutionary_persistence, community_memory)
    beta = float(selection_responsiveness)
    ds = float(selection_contrast)
    e = float(ecological_feedback_slope)
    # Reuse loop-gain validation for beta/ds/e.
    generalized_loop_gain(
        selection_responsiveness=beta,
        selection_contrast=ds,
        ecological_feedback_slope=e,
    )
    return (
        (alpha, beta * ds),
        ((1.0 - phi) * e, phi),
    )


def _eigenvalues(trace: float, determinant: float) -> tuple[complex, complex]:
    discriminant = trace * trace - 4.0 * determinant
    root = complex(discriminant) ** 0.5
    return ((trace + root) / 2.0, (trace - root) / 2.0)


def summarize_general_response(
    *,
    evolutionary_persistence: float,
    selection_responsiveness: float,
    selection_contrast: float,
    ecological_feedback_slope: float,
    community_memory: float,
) -> GeneralResponseSummary:
    """Return local invariants and exact Jury/oscillation classification."""

    alpha, phi = _validate_alpha_phi(evolutionary_persistence, community_memory)
    beta = float(selection_responsiveness)
    ds = float(selection_contrast)
    e = float(ecological_feedback_slope)
    G = generalized_loop_gain(
        selection_responsiveness=beta,
        selection_contrast=ds,
        ecological_feedback_slope=e,
    )
    trace = alpha + phi
    determinant = alpha * phi + (1.0 - phi) * G
    discriminant = trace * trace - 4.0 * determinant
    eig = _eigenvalues(trace, determinant)

    # Jury conditions for lambda^2 - T lambda + D.
    jury1 = 1.0 - trace + determinant
    jury2 = 1.0 + trace + determinant
    jury3 = 1.0 - determinant
    stable = jury1 > _TOL and jury2 > _TOL and jury3 > _TOL
    oscillatory = discriminant < -_TOL

    thresholds = general_response_thresholds(alpha, phi)
    if G <= thresholds.lower_stability_gain + _TOL:
        regime = "lower_boundary_or_nonrestoring_instability"
    elif G >= thresholds.upper_stability_gain - _TOL:
        regime = "upper_oscillatory_instability"
    elif oscillatory:
        regime = "stable_damped_oscillation"
    else:
        regime = "stable_nonoscillatory"

    return GeneralResponseSummary(
        evolutionary_persistence=alpha,
        selection_responsiveness=beta,
        selection_contrast=ds,
        ecological_feedback_slope=e,
        community_memory=phi,
        loop_gain=G,
        trace=trace,
        determinant=determinant,
        discriminant=discriminant,
        eigenvalues=eig,
        locally_stable=stable,
        oscillatory=oscillatory,
        regime=regime,
    )


def generalized_structural_loop_gain(
    structural_gap_contrast: float,
    *,
    lambda_cost: float,
    selection_responsiveness: float,
    ecological_feedback_slope: float,
) -> float:
    """Map exact structural gap contrast into the generalized loop gain.

    Uses Delta_s=lambda_cost*Delta_g, hence

        G = -beta * lambda_cost * Delta_g * e.
    """

    gap = float(structural_gap_contrast)
    lam = float(lambda_cost)
    if not isfinite(gap) or gap < 0.0:
        raise ValueError("structural_gap_contrast must be finite and non-negative")
    if not isfinite(lam) or lam < 0.0:
        raise ValueError("lambda_cost must be finite and non-negative")
    return generalized_loop_gain(
        selection_responsiveness=selection_responsiveness,
        selection_contrast=lam * gap,
        ecological_feedback_slope=ecological_feedback_slope,
    )


def damped_spectral_radius(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> float:
    """Complex-pair modulus in the stable damped region."""

    G = float(generalized_gain)
    thresholds = general_response_thresholds(
        evolutionary_persistence, community_memory
    )
    if not thresholds.oscillation_gain < G < thresholds.upper_stability_gain:
        raise ValueError("requires stable damped generalized-response phase")
    alpha = thresholds.evolutionary_persistence
    phi = thresholds.community_memory
    determinant = alpha * phi + (1.0 - phi) * G
    return sqrt(determinant)


def damped_damping_time(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> float:
    """Local e-folding time in the generalized stable damped phase."""

    rho = damped_spectral_radius(
        generalized_gain,
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
    )
    if rho >= 1.0 - _TOL:
        return inf
    return -1.0 / log(rho)


def upper_boundary_critical_slowing_approximation(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> float:
    """Leading damping-time asymptotic near the upper unit-circle boundary.

    Since D=1-(1-phi)(G_upper-G),

        tau ~ 2 / [(1-phi)(G_upper-G)].
    """

    G = float(generalized_gain)
    thresholds = general_response_thresholds(
        evolutionary_persistence, community_memory
    )
    if not thresholds.oscillation_gain < G < thresholds.upper_stability_gain:
        raise ValueError("requires stable damped generalized-response phase")
    distance = thresholds.upper_stability_gain - G
    return 2.0 / ((1.0 - thresholds.community_memory) * distance)
