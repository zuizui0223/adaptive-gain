"""Long-horizon retention when fluctuating selection has directional bias.

Let selection be s_t = delta * X_t with |X_t|=1, stationary mean
m=E[X_t], and geometric autocovariance

    Cov(X_t, X_{t+k}) = (1-m^2) * phi^k.

Then for S_H=sum_t s_t,

    E[S_H] = delta*m*H
    Var(S_H) = delta^2*(1-m^2)*F_H(phi)

where F_H is the partial-sum factor implemented in
``evolutionary_timescale_filter.py``.  Hence

    sqrt(E[S_H^2])/(delta*H)
      = sqrt(m^2 + (1-m^2) F_H(phi)/H^2)
      -> |m|

for fixed |phi|<1.

The covariance algebra is standard; the repository-specific role is to expose
the long-timescale filter downstream of structurally generated selection.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .evolutionary_timescale_filter import ar1_partial_sum_factor


def _validate(horizon: int, mean_sign: float, phi: float) -> tuple[int, float, float]:
    H = int(horizon)
    m = float(mean_sign)
    p = float(phi)
    if H <= 0:
        raise ValueError("horizon must be positive")
    if m < -1.0 or m > 1.0:
        raise ValueError("mean_sign must lie in [-1, 1]")
    if p < -1.0 or p > 1.0:
        raise ValueError("phi must lie in [-1, 1]")
    return H, m, p


def expected_cumulative_selection(
    horizon: int,
    selection_magnitude: float,
    mean_sign: float,
) -> float:
    """E[sum s_t] for s_t=delta*X_t."""

    H = int(horizon)
    if H <= 0:
        raise ValueError("horizon must be positive")
    delta = abs(float(selection_magnitude))
    m = float(mean_sign)
    if m < -1.0 or m > 1.0:
        raise ValueError("mean_sign must lie in [-1, 1]")
    return delta * m * H


def cumulative_selection_variance(
    horizon: int,
    selection_magnitude: float,
    mean_sign: float,
    phi: float,
) -> float:
    """Var(sum s_t) under geometric sign autocovariance."""

    H, m, p = _validate(horizon, mean_sign, phi)
    delta = abs(float(selection_magnitude))
    return (delta * delta) * (1.0 - m * m) * ar1_partial_sum_factor(H, p)


def rms_cumulative_selection(
    horizon: int,
    selection_magnitude: float,
    mean_sign: float,
    phi: float,
) -> float:
    """sqrt(E[(sum s_t)^2])."""

    mean = expected_cumulative_selection(horizon, selection_magnitude, mean_sign)
    variance = cumulative_selection_variance(
        horizon, selection_magnitude, mean_sign, phi
    )
    return sqrt(max(0.0, mean * mean + variance))


def rms_retention_fraction(
    horizon: int,
    mean_sign: float,
    phi: float,
) -> float:
    """RMS cumulative selection divided by total magnitude H*delta.

    The selection magnitude cancels, so the result depends only on horizon,
    directional bias, and temporal coherence.
    """

    H, m, p = _validate(horizon, mean_sign, phi)
    factor = ar1_partial_sum_factor(H, p)
    return sqrt(max(0.0, m * m + (1.0 - m * m) * factor / (H * H)))


def asymptotic_rms_retention_fraction(mean_sign: float) -> float:
    """Long-horizon limit |m| for any fixed finite-correlation |phi|<1."""

    m = float(mean_sign)
    if m < -1.0 or m > 1.0:
        raise ValueError("mean_sign must lie in [-1, 1]")
    return abs(m)


@dataclass(frozen=True)
class DirectionalRetentionSummary:
    horizon: int
    selection_magnitude: float
    mean_sign: float
    phi: float
    expected_cumulative_selection: float
    cumulative_variance: float
    rms_cumulative_selection: float
    rms_retention_fraction: float


def summarize_directional_retention(
    horizon: int,
    selection_magnitude: float,
    mean_sign: float,
    phi: float,
) -> DirectionalRetentionSummary:
    H, m, p = _validate(horizon, mean_sign, phi)
    delta = abs(float(selection_magnitude))
    mean = expected_cumulative_selection(H, delta, m)
    variance = cumulative_selection_variance(H, delta, m, p)
    rms = sqrt(max(0.0, mean * mean + variance))
    return DirectionalRetentionSummary(
        horizon=H,
        selection_magnitude=delta,
        mean_sign=m,
        phi=p,
        expected_cumulative_selection=mean,
        cumulative_variance=variance,
        rms_cumulative_selection=rms,
        rms_retention_fraction=rms / (delta * H) if delta > 0 else 0.0,
    )
