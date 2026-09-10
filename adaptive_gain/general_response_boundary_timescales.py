"""Critical slowing at the lower stability boundary of the general response model.

For ``0<=alpha<=1`` and ``0<=phi<1``, the generalized gain stability interval is

    G_minus = alpha - 1
    G_plus  = (1-alpha*phi)/(1-phi).

The upper boundary is oscillatory and is handled in
``general_evolutionary_response.py``.  This module records the complementary
lower boundary.

At ``G=G_minus``, the characteristic polynomial has an eigenvalue +1 and the
second eigenvalue ``alpha+phi-1``.  For

    delta = G-G_minus > 0,

inside the stable nonoscillatory region, the dominant eigenvalue is

    lambda_+ = [alpha+phi + sqrt((2-alpha-phi)^2 - 4(1-phi)delta)] / 2.

Hence the local e-folding time diverges as

    tau ~ (2-alpha-phi) / [(1-phi)(G-G_minus)].

For the parent haploid-logit case alpha=1, this reduces to ``tau~1/G``.

The critical-slowing algebra is standard.  The relevance here is that the same
structural sensing gain can produce long-lived transients near either boundary
of the generalized eco-evolutionary stability interval.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log, sqrt

from .general_evolutionary_response import general_response_thresholds


@dataclass(frozen=True)
class LowerBoundaryTimescale:
    evolutionary_persistence: float
    community_memory: float
    generalized_gain: float
    lower_stability_gain: float
    distance_to_lower_boundary: float
    dominant_eigenvalue: float
    damping_time: float
    asymptotic_damping_time: float
    scaled_ratio: float


def lower_boundary_dominant_eigenvalue(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> float:
    """Return the real dominant eigenvalue near the lower stable boundary."""

    G = float(generalized_gain)
    if not isfinite(G):
        raise ValueError("generalized_gain must be finite")
    thresholds = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    )
    lower = thresholds.lower_stability_gain
    oscillation = thresholds.oscillation_gain
    if not lower < G <= oscillation:
        raise ValueError("requires stable nonoscillatory phase above lower boundary")

    alpha = thresholds.evolutionary_persistence
    phi = thresholds.community_memory
    delta = G - lower
    discriminant = (2.0 - alpha - phi) ** 2 - 4.0 * (1.0 - phi) * delta
    # In the declared nonoscillatory domain this is non-negative up to roundoff.
    discriminant = max(0.0, discriminant)
    return (alpha + phi + sqrt(discriminant)) / 2.0


def lower_boundary_damping_time(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> float:
    """Exact e-folding time from the dominant real eigenvalue."""

    rho = lower_boundary_dominant_eigenvalue(
        generalized_gain,
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
    )
    if not 0.0 < rho < 1.0:
        raise ValueError("dominant eigenvalue must lie inside (0,1) for damping time")
    return -1.0 / log(rho)


def lower_boundary_critical_slowing_approximation(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> float:
    """Leading asymptotic near ``G_minus=alpha-1``."""

    G = float(generalized_gain)
    thresholds = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    )
    lower = thresholds.lower_stability_gain
    # Validate phase through the exact eigenvalue helper.
    lower_boundary_dominant_eigenvalue(
        G,
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
    )
    delta = G - lower
    alpha = thresholds.evolutionary_persistence
    phi = thresholds.community_memory
    return (2.0 - alpha - phi) / ((1.0 - phi) * delta)


def summarize_lower_boundary_timescale(
    generalized_gain: float,
    *,
    evolutionary_persistence: float,
    community_memory: float,
) -> LowerBoundaryTimescale:
    thresholds = general_response_thresholds(
        evolutionary_persistence,
        community_memory,
    )
    G = float(generalized_gain)
    lower = thresholds.lower_stability_gain
    rho = lower_boundary_dominant_eigenvalue(
        G,
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
    )
    exact = lower_boundary_damping_time(
        G,
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
    )
    approx = lower_boundary_critical_slowing_approximation(
        G,
        evolutionary_persistence=evolutionary_persistence,
        community_memory=community_memory,
    )
    return LowerBoundaryTimescale(
        evolutionary_persistence=thresholds.evolutionary_persistence,
        community_memory=thresholds.community_memory,
        generalized_gain=G,
        lower_stability_gain=lower,
        distance_to_lower_boundary=G-lower,
        dominant_eigenvalue=rho,
        damping_time=exact,
        asymptotic_damping_time=approx,
        scaled_ratio=exact/approx,
    )
