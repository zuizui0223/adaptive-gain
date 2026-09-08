"""Inverse diagnostics for the endogenous eco-evolutionary feedback model.

The local forward map has invariants

    T = 1 + phi,
    D = phi + (1-phi)L,

where ``L=-eta*Delta_s*p_star*(1-p_star)``.  The same invariants can be recovered
from a local eigenvalue pair, a stable damped transient, or the phenotype-logit
AR(2) recurrence

    x[t+2] = T*x[t+1] - D*x[t].

If nonstructural factors are independently known, the recovered loop gain can be
factorized into the structural gap

    Delta_g = L / [(-eta)*lambda*p_star*(1-p_star)],

which can then be checked against unit-cost integrality and the repository's
finite structural bounds.

The inverse algebra and AR(2) reduction are standard.  The repository-specific
use is to connect observable transient geometry back to exact finite sensing
structure.
"""

from __future__ import annotations

from cmath import phase
from dataclasses import dataclass
from math import cos, exp, isfinite, log, pi

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


def _estimate_from_trace_determinant(
    trace: float,
    determinant: float,
    *,
    reconstruction: str,
) -> FeedbackInverseEstimate:
    T = float(trace)
    D = float(determinant)
    if not isfinite(T) or not isfinite(D):
        raise ValueError("trace and determinant must be finite")
    denominator = 2.0 - T
    if abs(denominator) <= _TOL:
        raise ValueError("trace implies community memory too close to one for inversion")
    phi = T - 1.0
    phi, L = _validate_inferred_phi_L(phi, (D - phi) / denominator)
    return FeedbackInverseEstimate(
        community_memory=phi,
        loop_gain=L,
        trace=T,
        determinant=D,
        spectral_radius=None,
        oscillation_period=None,
        damping_time=None,
        reconstruction=reconstruction,
    )


def infer_feedback_from_eigenvalues(
    eigenvalue_1: complex,
    eigenvalue_2: complex,
) -> FeedbackInverseEstimate:
    """Recover ``phi`` and ``L`` from a local eigenvalue pair."""

    l1 = complex(eigenvalue_1)
    l2 = complex(eigenvalue_2)
    if not all(isfinite(v) for v in (l1.real, l1.imag, l2.real, l2.imag)):
        raise ValueError("eigenvalues must be finite")
    trace_c = l1 + l2
    determinant_c = l1 * l2
    if abs(trace_c.imag) > _TOL or abs(determinant_c.imag) > _TOL:
        raise ValueError("eigenvalue pair does not define a real second-order map")

    estimate = _estimate_from_trace_determinant(
        float(trace_c.real),
        float(determinant_c.real),
        reconstruction="eigenvalue_pair",
    )

    rho = None
    period = None
    damping = None
    if abs(l1.imag) > _TOL or abs(l2.imag) > _TOL:
        rho = abs(l1)
        angle = abs(phase(l1))
        if angle > _TOL:
            period = 2.0 * pi / angle
        if 0.0 < rho < 1.0:
            damping = -1.0 / log(rho)

    return FeedbackInverseEstimate(
        community_memory=estimate.community_memory,
        loop_gain=estimate.loop_gain,
        trace=estimate.trace,
        determinant=estimate.determinant,
        spectral_radius=rho,
        oscillation_period=period,
        damping_time=damping,
        reconstruction="eigenvalue_pair",
    )


def infer_feedback_from_ar2_coefficients(
    lag1_coefficient: float,
    lag2_coefficient: float,
) -> FeedbackInverseEstimate:
    """Recover feedback parameters from ``x[t+2]=a1*x[t+1]+a2*x[t]``."""

    a1 = float(lag1_coefficient)
    a2 = float(lag2_coefficient)
    if not isfinite(a1) or not isfinite(a2):
        raise ValueError("AR(2) coefficients must be finite")
    return _estimate_from_trace_determinant(
        a1,
        -a2,
        reconstruction="phenotype_logit_ar2",
    )


def infer_feedback_from_damping_and_period(
    damping_time: float,
    oscillation_period: float,
) -> FeedbackInverseEstimate:
    """Recover damped-phase ``phi`` and ``L`` from local ``tau`` and period.

    A discrete-time nonreal eigenvalue has principal angle ``0<theta<pi``, so
    its unaliased local period must satisfy ``P>2`` generations.  Shorter values
    are rejected rather than folded through the cosine into a spurious inverse.
    """

    tau = float(damping_time)
    period = float(oscillation_period)
    if not isfinite(tau) or tau <= 0.0:
        raise ValueError("damping_time must be finite and positive")
    if not isfinite(period) or period <= 2.0:
        raise ValueError("oscillation_period must be finite and greater than 2 generations")

    rho = exp(-1.0 / tau)
    theta = 2.0 * pi / period
    phi = 2.0 * rho * cos(theta) - 1.0
    determinant = rho * rho
    estimate = _estimate_from_trace_determinant(
        1.0 + phi,
        determinant,
        reconstruction="damping_time_and_period",
    )
    phi = estimate.community_memory
    L = estimate.loop_gain

    threshold = (1.0 - phi) / 4.0
    if not threshold < L < 1.0:
        raise ValueError(
            "observed damping/period pair does not reconstruct a stable damped feedback state"
        )

    return FeedbackInverseEstimate(
        community_memory=phi,
        loop_gain=L,
        trace=estimate.trace,
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
    """Compare an inferred gap with the inherited finite-task gap ceiling."""

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
    """Run transient -> loop gain -> structural gap -> finite-scope audit."""

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
