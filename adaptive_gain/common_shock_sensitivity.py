"""Sensitivity bounds for mechanistic OU half-life under hidden common shocks.

For the exact reciprocal evoTS congruence family,

    a = q*alpha,
    d = (1-q)*alpha,

and the process covariance between the observed trait and latent state is

    Q12 = -(d/a) * v_trait = -((1-q)/q) * v_trait.

If external knowledge supplies an upper bound ``|Q12| <= C``, then

    q >= v_trait / (v_trait + C)

and the direct trait-response half-life obeys

    H_OU <= H_direct <= H_OU * (1 + C/v_trait).

Thus the usual one-way OU half-life is recovered at C=0, while an unrestricted
common shock gives no finite upper bound.
"""

from __future__ import annotations


def minimum_response_fraction_from_common_shock_bound(
    v_trait: float, common_shock_bound: float
) -> float:
    """Smallest q compatible with ``|Q12| <= common_shock_bound``."""

    vx = float(v_trait)
    bound = float(common_shock_bound)
    if vx <= 0.0:
        raise ValueError("v_trait must be positive")
    if bound < 0.0:
        raise ValueError("common_shock_bound must be non-negative")
    return vx / (vx + bound)


def half_life_multiplier_upper_bound(
    v_trait: float, common_shock_bound: float
) -> float:
    """Maximum H_direct/H_OU implied by an absolute common-shock bound."""

    q_min = minimum_response_fraction_from_common_shock_bound(
        v_trait, common_shock_bound
    )
    return 1.0 / q_min


def direct_half_life_upper_bound(
    reported_half_life: float,
    v_trait: float,
    common_shock_bound: float,
) -> float:
    """Finite upper endpoint for direct half-life under ``|Q12| <= C``."""

    half = float(reported_half_life)
    if half <= 0.0:
        raise ValueError("reported_half_life must be positive")
    return half * half_life_multiplier_upper_bound(v_trait, common_shock_bound)
