"""Identifiability of the generalized scalar eco-evolutionary response model.

The generalized local Jacobian is

    J = [[alpha, beta*Delta_s],
         [(1-phi)*e, phi]],

with generalized loop gain

    G = -beta*Delta_s*e.

Its characteristic invariants are

    T = alpha + phi,
    D = alpha*phi + (1-phi)*G.

A local scalar time series (including the phenotype coordinate when both local
modes are visible) identifies only ``T`` and ``D`` through the second-order
recurrence

    x[t+2] = T*x[t+1] - D*x[t].

Unless either intrinsic evolutionary persistence ``alpha`` or community memory
``phi`` is known independently, the three biological quantities ``alpha``,
``phi`` and ``G`` are therefore not jointly identifiable.

For each feasible candidate memory ``phi`` the same observed pair ``(T,D)`` is
explained by

    alpha(phi) = T - phi,
    G(phi) = [D - phi*(T-phi)]/(1-phi).

This module makes that equivalence class explicit.  In the special parent model
``alpha=1`` the ridge collapses and the earlier inverse formulas are recovered.

The algebra is elementary.  The repository-specific use is to state exactly
which parts of the structural adaptive-gain mechanism can and cannot be inferred
from evolutionary transient geometry once the haploid-logit response assumption
is removed.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf, isfinite, sqrt

_TOL = 1e-12


@dataclass(frozen=True)
class GeneralResponseCandidate:
    intrinsic_persistence: float
    community_memory: float
    loop_gain: float
    trace: float
    determinant: float


@dataclass(frozen=True)
class FeasibleMemoryInterval:
    lower: float
    upper: float
    upper_open: bool


@dataclass(frozen=True)
class GeneralResponseGainEnvelope:
    trace: float
    determinant: float
    memory_interval: FeasibleMemoryInterval
    gain_lower_bound: float
    gain_upper_bound: float
    gain_upper_unbounded: bool
    stationary_memory: float | None
    stable_observation: bool
    scope: str = "general_scalar_response_trace_determinant_identifiability"


def _finite(value: float, *, name: str) -> float:
    out = float(value)
    if not isfinite(out):
        raise ValueError(f"{name} must be finite")
    return out


def generalized_trace_determinant(
    intrinsic_persistence: float,
    community_memory: float,
    loop_gain: float,
) -> tuple[float, float]:
    """Return ``(T,D)`` for the generalized local Jacobian."""

    alpha = _finite(intrinsic_persistence, name="intrinsic_persistence")
    phi = _finite(community_memory, name="community_memory")
    G = _finite(loop_gain, name="loop_gain")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("intrinsic_persistence must lie in [0,1]")
    if not 0.0 <= phi < 1.0:
        raise ValueError("community_memory must lie in [0,1)")
    return alpha + phi, alpha * phi + (1.0 - phi) * G


def generalized_ar2_coefficients(
    intrinsic_persistence: float,
    community_memory: float,
    loop_gain: float,
) -> tuple[float, float]:
    """Return ``(a1,a2)`` for ``x[t+2]=a1*x[t+1]+a2*x[t]``."""

    trace, determinant = generalized_trace_determinant(
        intrinsic_persistence,
        community_memory,
        loop_gain,
    )
    return trace, -determinant


def is_schur_stable_trace_determinant(trace: float, determinant: float) -> bool:
    """Exact second-order Jury stability check from observable invariants."""

    T = _finite(trace, name="trace")
    D = _finite(determinant, name="determinant")
    return (1.0 - T + D > 0.0) and (1.0 + T + D > 0.0) and (1.0 - D > 0.0)


def feasible_memory_interval(trace: float) -> FeasibleMemoryInterval:
    """Memory values compatible with ``alpha in [0,1]`` and ``phi in [0,1)``.

    Since ``T=alpha+phi``, a generalized biological decomposition exists only
    for ``0<=T<2``.
    """

    T = _finite(trace, name="trace")
    if T < 0.0 or T >= 2.0:
        raise ValueError("trace must lie in [0,2) for alpha in [0,1], phi in [0,1)")
    lower = max(0.0, T - 1.0)
    if T < 1.0:
        return FeasibleMemoryInterval(lower=lower, upper=T, upper_open=False)
    return FeasibleMemoryInterval(lower=lower, upper=1.0, upper_open=True)


def _candidate_from_memory_unchecked(trace: float, determinant: float, phi: float) -> GeneralResponseCandidate:
    alpha = trace - phi
    G = (determinant - alpha * phi) / (1.0 - phi)
    return GeneralResponseCandidate(
        intrinsic_persistence=alpha,
        community_memory=phi,
        loop_gain=G,
        trace=trace,
        determinant=determinant,
    )


def candidate_from_memory(
    trace: float,
    determinant: float,
    community_memory: float,
) -> GeneralResponseCandidate:
    """Recover ``alpha`` and ``G`` after ``phi`` is independently supplied."""

    T = _finite(trace, name="trace")
    D = _finite(determinant, name="determinant")
    phi = _finite(community_memory, name="community_memory")
    interval = feasible_memory_interval(T)
    if phi < interval.lower - _TOL:
        raise ValueError("community_memory is incompatible with observed trace")
    if interval.upper_open:
        if phi >= interval.upper:
            raise ValueError("community_memory is incompatible with observed trace")
    elif phi > interval.upper + _TOL:
        raise ValueError("community_memory is incompatible with observed trace")
    if phi < 0.0:
        phi = 0.0
    if not interval.upper_open and phi > interval.upper:
        phi = interval.upper
    candidate = _candidate_from_memory_unchecked(T, D, phi)
    if candidate.intrinsic_persistence < -_TOL or candidate.intrinsic_persistence > 1.0 + _TOL:
        raise ValueError("implied intrinsic persistence falls outside [0,1]")
    return candidate


def candidate_from_intrinsic_persistence(
    trace: float,
    determinant: float,
    intrinsic_persistence: float,
) -> GeneralResponseCandidate:
    """Recover ``phi`` and ``G`` after ``alpha`` is independently supplied."""

    T = _finite(trace, name="trace")
    D = _finite(determinant, name="determinant")
    alpha = _finite(intrinsic_persistence, name="intrinsic_persistence")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("intrinsic_persistence must lie in [0,1]")
    phi = T - alpha
    if phi < -_TOL or phi >= 1.0:
        raise ValueError("intrinsic_persistence is incompatible with observed trace")
    if phi < 0.0:
        phi = 0.0
    return candidate_from_memory(T, D, phi)


def compatible_gain_at_memory(trace: float, determinant: float, community_memory: float) -> float:
    """Convenience wrapper for the loop gain along the identifiability ridge."""

    return candidate_from_memory(trace, determinant, community_memory).loop_gain


def gain_identifiability_envelope(
    trace: float,
    determinant: float,
    *,
    require_stable: bool = True,
) -> GeneralResponseGainEnvelope:
    """Return the exact gain range compatible with observed ``(T,D)``.

    The result optimizes

        G(phi) = [D - T*phi + phi^2]/(1-phi)

    over all ``phi`` compatible with ``alpha in [0,1]``.  For a stable observed
    recurrence with ``T>=1``, Jury gives ``1-T+D>0`` and therefore
    ``G(phi)->+infinity`` as ``phi->1-``.  In that common case transient geometry
    alone provides no finite upper bound on generalized loop gain.
    """

    T = _finite(trace, name="trace")
    D = _finite(determinant, name="determinant")
    interval = feasible_memory_interval(T)
    stable = is_schur_stable_trace_determinant(T, D)
    if require_stable and not stable:
        raise ValueError("trace/determinant pair is not Schur stable")

    candidates: list[tuple[float, float]] = []

    lo_candidate = _candidate_from_memory_unchecked(T, D, interval.lower)
    candidates.append((interval.lower, lo_candidate.loop_gain))

    if not interval.upper_open:
        hi_candidate = _candidate_from_memory_unchecked(T, D, interval.upper)
        candidates.append((interval.upper, hi_candidate.loop_gain))

    jury1 = 1.0 - T + D
    stationary_phi: float | None = None
    if jury1 >= 0.0:
        root = 1.0 - sqrt(max(0.0, jury1))
        inside_lower = root >= interval.lower - _TOL
        inside_upper = root < interval.upper - _TOL if interval.upper_open else root <= interval.upper + _TOL
        if inside_lower and inside_upper and 0.0 <= root < 1.0:
            stationary_phi = max(interval.lower, root)
            if not interval.upper_open:
                stationary_phi = min(interval.upper, stationary_phi)
            stationary = _candidate_from_memory_unchecked(T, D, stationary_phi)
            candidates.append((stationary_phi, stationary.loop_gain))

    lower = min(value for _, value in candidates)

    upper_unbounded = False
    if interval.upper_open:
        if jury1 > 0.0:
            upper = inf
            upper_unbounded = True
        elif jury1 < 0.0:
            # This branch is excluded for stable observations but retained for
            # completeness when require_stable=False.
            upper = max(value for _, value in candidates)
        else:
            # When the numerator also vanishes at phi=1, the finite open-end
            # limit is T-2.
            upper = max(max(value for _, value in candidates), T - 2.0)
    else:
        upper = max(value for _, value in candidates)

    return GeneralResponseGainEnvelope(
        trace=T,
        determinant=D,
        memory_interval=interval,
        gain_lower_bound=lower,
        gain_upper_bound=upper,
        gain_upper_unbounded=upper_unbounded,
        stationary_memory=stationary_phi,
        stable_observation=stable,
    )


def parent_haploid_inverse(trace: float, determinant: float) -> GeneralResponseCandidate:
    """Recover the parent inverse by imposing its exact ``alpha=1`` assumption."""

    return candidate_from_intrinsic_persistence(trace, determinant, 1.0)
