"""Inverse diagnostics for the endogenous eco-evolutionary feedback model.

The forward local model has Jacobian

    J = [[1, Delta_s],
         [(1-phi)*eta*p_star*(1-p_star), phi]],

with trace and determinant

    T = 1 + phi,
    D = phi + (1-phi)L,

where ``L=-eta*Delta_s*p_star*(1-p_star)`` is the structural loop gain.

Therefore the local eigenvalues identify ``phi`` and ``L`` directly:

    phi = (lambda_1 + lambda_2) - 1,
    L   = (lambda_1*lambda_2 - phi)/(1-phi).

In the stable damped phase, writing the conjugate pair as

    rho * exp(+-i theta),

and observing damping time ``tau`` and period ``P`` gives

    rho   = exp(-1/tau),
    theta = 2*pi/P,
    phi   = 2*rho*cos(theta) - 1,
    L     = (rho^2 - phi)/(1-phi).

If ecological feedback strength, fitness scaling, and equilibrium phenotype
frequency are independently known, the structural gap contrast can then be
recovered from

    Delta_g = L / [(-eta)*lambda*p_star*(1-p_star)].

For unit-cost sensing tasks the exact structural gap is integer.  Comparing the
inferred gap with the nearest integer and with the repository's bounded-arity
upper bound yields a falsification-oriented diagnostic for the structural model.

The inverse algebra is elementary.  The repository-specific use is to connect
observable transient geometry back to the exact finite sensing structure.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, inf, isfinite, pi

from .feedback_structural_bounds import bounded_arity_gap_upper_bound

_TOL = 1e-10


@dataclass(frozen=True)
class FeedbackInverseEstimate:
    community_memory: float
    loop_gain: float
    trace: float
    determinant: float
    spectral_radius: float | None
    oscillation_period: float | None
    damping_time: float | None
    reconstruction: str


@dataclass(frozen=True)
class StructuralGapInference:
    loop_gain: float
    gain_per_structural_gap: float
    inferred_gap: float
    nearest_integer_gap: int
    distance_to_nearest_integer: float
    unit_cost_integer_compatible: bool


@dataclass(frozen=True)
class StructuralScopeCompatibility:
    inferred_gap: float
    structural_gap_upper_bound: int
    compatible_with_scope: bool
    nearest_integer_gap: int
    nearest_integer_compatible_with_scope: bool
    frontier_edge_cap: int | None
    scope: str = "inverse_feedback_gap_vs_bounded_arity_scope"


def _validate_inferred_phi_L(phi: float, loop_gain: float) -> tuple[float, float]:
    p = float(phi)
    L = float(loop_gain)
    if not isfinite(p) or not isfinite(L):
        raise ValueError("inferred parameters must be finite")
    if p < -_TOL or p >= 1.0 + _TOL:
        raise ValueError("inferred community memory falls outside [0,1)")
    if p < 0.0:
        p = 0.0
    if p >= 1.0:
        raise ValueError("inferred community memory must be below 1")
    return p, L


def infer_feedback_from_eigenvalues(
    eigenvalue_1: complex,
    eigenvalue_2: complex,
) -> FeedbackInverseEstimate:
    """Recover ``phi`` and ``L`` from a local eigenvalue pair.

    The sum and product must be real up to numerical tolerance because the model
    Jacobian has real coefficients.
    """

    l1 = complex(eigenvalue_1)
    l2 = complex(eigenvalue_2)
    trace_c = l1 + l2
    determinant_c = l1 * l2
    if abs(trace_c.imag) > _TOL or abs(determinant_c.imag) > _TOL:
        raise ValueError("eigenvalue pair does not define a real second-order map")
    trace = float(trace_c.real)
    determinant = float(determinant_c.real)
    phi, L = _validate_inferred_phi_L(
        trace - 1.0,
        (determinant - (trace - 1.0)) / (2.0 - trace),
    )

    rho = None
    period = None
    damping = None
    if abs(l1.imag) > _TOL or abs(l2.imag) > _TOL:
        rho = abs(l1)
        angle = abs(__import__("cmath").phase(l1))
        if angle > _TOL:
            period = 2.0 * pi / angle
        if 0.0 < rho < 1.0:
            from math import log

            damping = -1.0 / log(rho)

    return FeedbackInverseEstimate(
        community_memory=phi,
        loop_gain=L,
        trace=trace,
        determinant=determinant,
        spectral_radius=rho,
        oscillation_period=period,
        damping_time=damping,
        reconstruction="eigenvalue_pair",
    )


def infer_feedback_from_damping_and_period(
    damping_time: float,
    oscillation_period: float,
) -> FeedbackInverseEstimate:
    """Recover damped-phase ``phi`` and ``L`` from observed ``tau`` and period."""

    tau = float(damping_time)
    period = float(oscillation_period)
    if not isfinite(tau) or tau <= 0.0:
        raise ValueError("damping_time must be finite and positive")
    if not isfinite(period) or period <= 0.0:
        raise ValueError("oscillation_period must be finite and positive")

    rho = exp(-1.0 / tau)
    theta = 2.0 * pi / period
    phi = 2.0 * rho * cos(theta) - 1.0
    determinant = rho * rho
    phi, L = _validate_inferred_phi_L(
        phi,
        (determinant - phi) / (1.0 - phi),
    )

    threshold = (1.0 - phi) / 4.0
    if not threshold < L < 1.0:
        raise ValueError(
            "observed damping/period pair does not reconstruct a stable damped feedback state"
        )

    return FeedbackInverseEstimate(
        community_memory=phi,
        loop_gain=L,
        trace=1.0 + phi,
        determinant=determinant,
        spectral_radius=rho,
        oscillation_period=period,
        damping_time=tau,
        reconstruction="damping_time_and_period",
    )


def infer_structural_gap_from_loop_gain(
    loop_gain: float,
    *,
    lambda_cost: float,
    feedback_strength: float,
    equilibrium_frequency: float,
    integer_tolerance: float = 1e-6,
) -> StructuralGapInference:
    """Infer ``Delta_g`` after supplying the nonstructural loop-gain factors."""

    L = float(loop_gain)
    lam = float(lambda_cost)
    eta = float(feedback_strength)
    p = float(equilibrium_frequency)
    tol = float(integer_tolerance)
    if not isfinite(L) or L < 0.0:
        raise ValueError("loop_gain must be finite and non-negative")
    if not isfinite(lam) or lam <= 0.0:
        raise ValueError("lambda_cost must be finite and positive")
    if not isfinite(eta) or eta >= 0.0:
        raise ValueError("feedback_strength must be finite and negative")
    if not 0.0 < p < 1.0:
        raise ValueError("equilibrium_frequency must lie strictly inside (0,1)")
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("integer_tolerance must be finite and non-negative")

    scale = (-eta) * lam * p * (1.0 - p)
    inferred = L / scale
    nearest = int(round(inferred))
    distance = abs(inferred - nearest)
    return StructuralGapInference(
        loop_gain=L,
        gain_per_structural_gap=scale,
        inferred_gap=inferred,
        nearest_integer_gap=nearest,
        distance_to_nearest_integer=distance,
        unit_cost_integer_compatible=(nearest >= 0 and distance <= tol),
    )


def structural_scope_compatibility(
    inferred_gap: float,
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    *,
    frontier_edge_cap: int | None = None,
    tolerance: float = 1e-9,
) -> StructuralScopeCompatibility:
    """Compare an inferred structural gap with an inherited finite-task ceiling."""

    gap = float(inferred_gap)
    tol = float(tolerance)
    if not isfinite(gap) or gap < -tol:
        raise ValueError("inferred_gap must be finite and non-negative")
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("tolerance must be finite and non-negative")
    if gap < 0.0:
        gap = 0.0

    upper = bounded_arity_gap_upper_bound(
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        frontier_edge_cap=frontier_edge_cap,
    )
    nearest = int(round(gap))
    return StructuralScopeCompatibility(
        inferred_gap=gap,
        structural_gap_upper_bound=upper,
        compatible_with_scope=(gap <= upper + tol),
        nearest_integer_gap=nearest,
        nearest_integer_compatible_with_scope=(0 <= nearest <= upper),
        frontier_edge_cap=frontier_edge_cap,
    )


def full_damped_inverse_diagnostic(
    damping_time: float,
    oscillation_period: float,
    *,
    lambda_cost: float,
    feedback_strength: float,
    equilibrium_frequency: float,
    world_count: int,
    query_count: int,
    adaptive_cost: int,
    max_arity: int,
    frontier_edge_cap: int | None = None,
    integer_tolerance: float = 1e-6,
) -> tuple[FeedbackInverseEstimate, StructuralGapInference, StructuralScopeCompatibility]:
    """Run the full transient -> loop gain -> structural-gap -> scope audit."""

    feedback = infer_feedback_from_damping_and_period(
        damping_time,
        oscillation_period,
    )
    gap = infer_structural_gap_from_loop_gain(
        feedback.loop_gain,
        lambda_cost=lambda_cost,
        feedback_strength=feedback_strength,
        equilibrium_frequency=equilibrium_frequency,
        integer_tolerance=integer_tolerance,
    )
    scope = structural_scope_compatibility(
        gap.inferred_gap,
        world_count,
        query_count,
        adaptive_cost,
        max_arity,
        frontier_edge_cap=frontier_edge_cap,
    )
    return feedback, gap, scope
