"""Long-horizon retention when fluctuating selection has directional bias.

Let selection be s_t = delta * X_t with |X_t|=1, stationary mean
m=E[X_t], and geometric autocovariance

    Cov(X_t, X_{t+k}) = (1-m^2) * phi^k.

Then for S_H=sum_t s_t,

    E[S_H] = delta*m*H
    Var(S_H) = delta^2*(1-m^2)*F_H(phi)

where F_H is the partial-sum factor implemented in
``evolutionary_timescale_filter.py``. Hence

    sqrt(E[S_H^2])/(delta*H)
      = sqrt(m^2 + (1-m^2) F_H(phi)/H^2)
      -> |m|

for fixed |phi|<1.

When interpreted as a stationary two-state Markov sign process, the transition
probabilities

    a = P(+ | -)
    b = P(- | +)

imply

    m   = (a-b)/(a+b)
    phi = 1-a-b.

Conversely, for |m|<1,

    a = (1+m)(1-phi)/2
    b = (1-m)(1-phi)/2.

Not every pair (m,phi) is Markov-feasible; equivalently

    phi >= -(1-|m|)/(1+|m|).

The covariance algebra is standard; the repository-specific role is to expose
the long-timescale filter downstream of structurally generated selection and to
map it back to community-state switching dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf, sqrt

from .evolutionary_timescale_filter import ar1_partial_sum_factor


_TOL = 1e-12


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


def two_state_markov_transition_probabilities(
    mean_sign: float,
    phi: float,
) -> tuple[float, float]:
    """Return P(+|-), P(-|+) for the stationary two-state Markov interpretation.

    Raises when ``(mean_sign, phi)`` cannot be realized by a stationary two-state
    Markov chain with sign values -1 and +1. Degenerate |m|=1 is treated as a
    one-support-state process and returns zero for both off-diagonal transitions.
    """

    m = float(mean_sign)
    p = float(phi)
    if m < -1.0 or m > 1.0:
        raise ValueError("mean_sign must lie in [-1, 1]")
    if p < -1.0 or p > 1.0:
        raise ValueError("phi must lie in [-1, 1]")
    if abs(m) == 1.0:
        return 0.0, 0.0
    plus_from_minus = 0.5 * (1.0 + m) * (1.0 - p)
    minus_from_plus = 0.5 * (1.0 - m) * (1.0 - p)
    if plus_from_minus > 1.0 + _TOL or minus_from_plus > 1.0 + _TOL:
        minimum_phi = -(1.0 - abs(m)) / (1.0 + abs(m))
        raise ValueError(
            "mean_sign and phi are not jointly feasible for a stationary two-state "
            f"Markov sign process; require phi >= {minimum_phi:.12g}"
        )
    return (
        min(1.0, max(0.0, plus_from_minus)),
        min(1.0, max(0.0, minus_from_plus)),
    )


def two_state_markov_feasible(mean_sign: float, phi: float) -> bool:
    """Whether ``(m,phi)`` has a stationary two-state Markov realization."""

    try:
        two_state_markov_transition_probabilities(mean_sign, phi)
    except ValueError:
        return False
    return True


def community_switching_to_mean_and_coherence(
    plus_from_minus: float,
    minus_from_plus: float,
) -> tuple[float, float]:
    """Map two community-state switching probabilities to ``(m, phi)``.

    ``plus_from_minus`` is ``a=P(X_{t+1}=+ | X_t=-)`` and
    ``minus_from_plus`` is ``b=P(X_{t+1}=- | X_t=+)``. The chain must be
    ergodic in the two-state sense ``a+b>0``; the fully absorbing ``a=b=0``
    case has no unique stationary occupancy.
    """

    a = float(plus_from_minus)
    b = float(minus_from_plus)
    if a < 0.0 or a > 1.0 or b < 0.0 or b > 1.0:
        raise ValueError("switching probabilities must lie in [0, 1]")
    total = a + b
    if total <= _TOL:
        raise ValueError("a+b must be positive for a unique stationary two-state occupancy")
    mean_sign = (a - b) / total
    phi = 1.0 - total
    return mean_sign, phi


def stationary_plus_occupancy(
    plus_from_minus: float,
    minus_from_plus: float,
) -> float:
    """Stationary probability of the selection-positive community state."""

    a = float(plus_from_minus)
    b = float(minus_from_plus)
    m, _ = community_switching_to_mean_and_coherence(a, b)
    return 0.5 * (1.0 + m)


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


def directional_signal_to_noise(
    horizon: int,
    mean_sign: float,
    phi: float,
) -> float:
    """Absolute cumulative mean divided by its standard deviation."""

    H, m, p = _validate(horizon, mean_sign, phi)
    numerator = abs(m) * H
    variance_factor = (1.0 - m * m) * ar1_partial_sum_factor(H, p)
    if variance_factor <= 0.0:
        return inf if numerator > 0.0 else 0.0
    return numerator / sqrt(variance_factor)


def asymptotic_directional_crossover_horizon(
    mean_sign: float,
    phi: float,
) -> float:
    """Asymptotic generations needed for directional mean ~= fluctuation SD.

    For 0<|m|<1 and -1<phi<1,

        H_x ~= ((1-m^2)/m^2) * ((1+phi)/(1-phi)).
    """

    m = float(mean_sign)
    p = float(phi)
    if m < -1.0 or m > 1.0:
        raise ValueError("mean_sign must lie in [-1, 1]")
    if not (-1.0 < p < 1.0):
        raise ValueError("crossover approximation requires -1 < phi < 1")
    if m == 0.0:
        return inf
    if abs(m) == 1.0:
        return 0.0
    return ((1.0 - m * m) / (m * m)) * ((1.0 + p) / (1.0 - p))


def community_directional_crossover_horizon(
    plus_from_minus: float,
    minus_from_plus: float,
) -> float:
    """Directional trend-emergence horizon written directly in community rates.

    For ``a=P(+|-)`` and ``b=P(-|+)`` with ``a,b>0``, ``a!=b``, and
    ``a+b<2``, substitution into the ``(m,phi)`` formula gives

        H_x ~= 4ab(2-a-b) / ((a-b)^2 (a+b)).

    Balanced occupancy ``a=b`` gives infinite crossover because the stationary
    directional bias is zero. Degenerate one-way chains have zero sign variance
    in stationarity and return zero.
    """

    a = float(plus_from_minus)
    b = float(minus_from_plus)
    m, phi = community_switching_to_mean_and_coherence(a, b)
    if m == 0.0:
        return inf
    if abs(m) == 1.0:
        return 0.0
    if not (-1.0 < phi < 1.0):
        # This includes deterministic alternation a=b=1, already caught by m=0.
        raise ValueError("finite crossover approximation requires -1 < phi < 1")
    direct = asymptotic_directional_crossover_horizon(m, phi)
    closed = 4.0 * a * b * (2.0 - a - b) / (((a - b) ** 2) * (a + b))
    if abs(direct - closed) > 1e-9 * max(1.0, abs(direct)):
        raise ArithmeticError("community crossover substitution identity failed")
    return direct


@dataclass(frozen=True)
class CommunitySwitchingSummary:
    plus_from_minus: float
    minus_from_plus: float
    stationary_plus_occupancy: float
    mean_sign: float
    phi: float
    asymptotic_retained_fraction: float
    crossover_horizon: float


def summarize_community_switching(
    plus_from_minus: float,
    minus_from_plus: float,
) -> CommunitySwitchingSummary:
    """Summarize evolutionary timescale controls from two community transitions."""

    a = float(plus_from_minus)
    b = float(minus_from_plus)
    m, phi = community_switching_to_mean_and_coherence(a, b)
    return CommunitySwitchingSummary(
        plus_from_minus=a,
        minus_from_plus=b,
        stationary_plus_occupancy=0.5 * (1.0 + m),
        mean_sign=m,
        phi=phi,
        asymptotic_retained_fraction=abs(m),
        crossover_horizon=community_directional_crossover_horizon(a, b),
    )


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
    directional_signal_to_noise: float


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
        directional_signal_to_noise=directional_signal_to_noise(H, m, p),
    )
