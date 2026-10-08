"""Dimensionless common-innovation correlation sensitivity for the exact OUBM gauge.

For v_trait > 0, v_optimum > 0 and 0 < q <= 1:
  a=q*alpha, d=(1-q)*alpha
  Q11 = v_trait
  Q12 = -(1-q)*v_trait/q
  Q22 = ((1-q)**2 * v_trait + v_optimum) / q**2

Hence the instantaneous innovation correlation is
  rho(q) = -(1-q) / sqrt((1-q)**2 + v_optimum/v_trait).

An independently justified bound |rho| <= cap < 1 yields
  1-q <= cap * sqrt(v_optimum / (v_trait*(1-cap**2))).
If the right hand side is <1, this bounds H_direct/H_OU = 1/q.
If it is >=1, this *particular* correlation cap gives no finite
upper bound on the direct half-life.

This is a sensitivity calculation *within the constructed two-state
reciprocal family*, not a universal evolutionary or causal result.
Importantly, a latent state's physical interpretation must be anchored.
"""
from __future__ import annotations
from math import inf, isfinite, sqrt

def _positive(name: str, value: float) -> float:
    x = float(value)
    if not isfinite(x) or x <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return x

def innovation_correlation(
    response_fraction: float, v_trait: float, v_optimum: float
) -> float:
    """Q12/sqrt(Q11*Q22), with an anchored Y in the exact reciprocal gauge."""
    q = float(response_fraction)
    vx = _positive("v_trait", v_trait)
    vo = _positive("v_optimum", v_optimum)
    if not isfinite(q) or not 0.0 < q <= 1.0:
        raise ValueError("response_fraction must be in (0,1]")
    w = 1.0-q
    return -w/sqrt(w*w+vo/vx)

def critical_innovation_correlation(v_trait: float,v_optimum: float)->float:
    """Limiting |rho| as q->0, below which a finite upper half-life exists."""
    vx = _positive("v_trait",v_trait)
    vo = _positive("v_optimum",v_optimum)
    return sqrt(vx/(vx+vo))

def minimum_response_fraction_from_correlation_cap(
    v_trait: float, v_optimum: float, correlation_cap: float
) -> float:
    """Sharp infimum of q under |rho|<=cap in this reciprocal family."""
    vx=_positive("v_trait",v_trait)
    vo=_positive("v_optimum",v_optimum)
    cap=float(correlation_cap)
    if not isfinite(cap) or not 0.0 <= cap < 1.0:
        raise ValueError("correlation_cap must be in [0,1)")
    if cap >= sqrt(vx/(vx+vo)):
        return 0.0
    delta=cap*sqrt(vo/(vx*(1.0-cap*cap)))
    return max(0.0,1.0-delta)

def direct_half_life_multiplier_from_correlation_cap(
    v_trait: float, v_optimum: float, correlation_cap: float
)->float:
    """Sharp upper H_direct/H_OU within the reciprocal gauge, possibly inf."""
    q_min=minimum_response_fraction_from_correlation_cap(
        v_trait,v_optimum,correlation_cap
    )
    return inf if q_min==0.0 else 1.0/q_min
