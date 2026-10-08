"""Identified-set consequences for OU adaptation half-life.

In the evoTS moving-optimum model the fitted pull rate ``alpha`` is interpreted
as a direct adaptation rate, with half-life log(2)/alpha.  The exact reciprocal
congruence construction instead decomposes the same observed relaxation rate as

    alpha = a + d,

where ``a=q*alpha`` is the direct response of the observed trait to the latent
state and ``d=(1-q)*alpha`` is the reverse response of the latent state to the
trait.  The complete observed trait likelihood is unchanged for every
``0<q<1`` when the corresponding latent innovation covariance is allowed.

Consequently the mechanistic trait-response half-life is

    log(2)/a = (log(2)/alpha)/q,

so the fitted OU half-life is only the lower endpoint of the congruent set and
there is no finite upper bound without an extra causal/noise restriction.
"""

from __future__ import annotations

from math import log


def ou_half_life(alpha: float) -> float:
    """Conventional OU half-life log(2)/alpha."""

    rate = float(alpha)
    if rate <= 0.0:
        raise ValueError("alpha must be positive")
    return log(2.0) / rate


def direct_trait_half_life(alpha: float, response_fraction: float) -> float:
    """Direct trait-response half-life inside the reciprocal congruence family."""

    rate = float(alpha)
    q = float(response_fraction)
    if rate <= 0.0:
        raise ValueError("alpha must be positive")
    if not 0.0 < q < 1.0:
        raise ValueError("response_fraction must lie strictly between 0 and 1")
    return log(2.0) / (q * rate)


def direct_half_life_from_reported(
    reported_half_life: float, response_fraction: float
) -> float:
    """Map a reported one-way OU half-life to a congruent direct-response value."""

    half = float(reported_half_life)
    q = float(response_fraction)
    if half <= 0.0:
        raise ValueError("reported_half_life must be positive")
    if not 0.0 < q < 1.0:
        raise ValueError("response_fraction must lie strictly between 0 and 1")
    return half / q


def reported_half_life_is_lower_bound_with_shared_innovation() -> bool:
    """Exact symbolic ordering for 0<q<1: H_direct = H_reported/q > H_reported."""

    return True
