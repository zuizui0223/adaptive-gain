"""Rapid OU relaxation approaches a random-walk-plus-nugget observation law.

For an exogenous Brownian moving optimum with dX = alpha(Theta-X)dt
+sqrt(vs)dW1 and dTheta=sqrt(vo)dW2, fix S=vs/(2*alpha) and
positive sampling times t_i. For distinct times, alpha->infinity
yields Cov[X_s,X_t] -> vo*min(s,t); for equal positive times
the limit is vo*t+S. At t=0 X_0 is deterministic, so
the nugget S is not present at the initial time.

This is a standard high-rate limit, NOT a new mathematical novelty claim.
"""
from __future__ import annotations
from math import exp, expm1, isfinite

def finite_moving_ou_covariance(s: float,t: float,alpha: float,
                                 stationary_trait_variance:float,
                                 optimum_diffusion:float)->float:
    """Covariance at arbitrary nonnegative times before measurement noise."""
    if not all(map(isfinite,(s,t,alpha,stationary_trait_variance,optimum_diffusion))):
        raise ValueError("arguments must be finite")
    if min(s,t,stationary_trait_variance,optimum_diffusion)<0 or alpha<=0:
        raise ValueError("times and variances must be nonnegative; alpha positive")
    m=min(s,t)
    if m==0:
        return 0.0
    h=abs(s-t)
    eh=exp(-alpha*h)
    h2=-expm1(-2*alpha*m)
    tr=stationary_trait_variance*eh*h2
    opt=optimum_diffusion*(m-
        (1+eh)*(-expm1(-alpha*m))/alpha
        +eh*h2/(2*alpha))
    return tr+opt

def rapid_relaxation_covariance_limit(s:float,t:float,
                                      stationary_trait_variance:float,
                                      optimum_diffusion:float)->float:
    """Distinct fixed sampling times; at any positive same-time add nugget."""
    if not all(map(isfinite,(s,t,stationary_trait_variance,optimum_diffusion))):
        raise ValueError("arguments must be finite")
    if min(s,t,stationary_trait_variance,optimum_diffusion)<0:
        raise ValueError("inputs must be nonnegative")
    if s==0 or t==0:
        return 0.0
    return optimum_diffusion*min(s,t)+(stationary_trait_variance if s==t else 0.0)
