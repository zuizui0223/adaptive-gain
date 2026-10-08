"""Brownian latent random walk plus independent biological nugget.

A descriptive alternative to the moving-optimum OU at fossil sampling
times.  For t>0: Y_i = mu + B(t_i) + eps_i + measurement_error_i.
B is Brownian with variance rate D; eps_i are independent N(0,S).
At the initial time t=0 the trait is deterministic and only measurement
error contributes (matching the exact high-alpha OUBM limit).

This is a complete *three-parameter observation likelihood*, not evidence
that a biological process is actually temporally white or that the optimal
trait state does not exist.
"""
from __future__ import annotations
from math import isfinite, log, pi

def loglik_random_walk_with_nugget(
    times, observations, sampling_variances,
    ancestral_mean:float, optimum_diffusion:float, biological_nugget:float
)->float:
    t = list(map(float,times))
    y = list(map(float,observations))
    v = list(map(float,sampling_variances))
    n = len(t)
    if n < 2 or len(y)!=n or len(v)!=n:
        raise ValueError("times, observations and sample variances must align (n>=2)")
    if not all(isfinite(z) for z in t+y+v+
        [ancestral_mean,optimum_diffusion,biological_nugget]):
        raise ValueError("all quantities must be finite")
    if abs(t[0])>1e-12 or any(t[i]<=t[i-1] for i in range(1,n)):
        raise ValueError("times must start at 0 and increase strictly")
    if any(s<=0 for s in v) or optimum_diffusion<0 or biological_nugget<0:
        raise ValueError("sampling variances positive; diffusion and nugget nonnegative")
    state=float(ancestral_mean)
    variance=0.0
    ll=0.0
    for i in range(n):
        if i:
            variance+=optimum_diffusion*(t[i]-t[i-1])
        extra=biological_nugget if i else 0.0
        s=variance+v[i]+extra
        delta=y[i]-state
        ll-=0.5*(log(2*pi*s)+delta*delta/s)
        if i:
            gain=variance/s
            state+=gain*delta
            variance*=1-gain
    return ll

def aicc(loglik:float,n:int,k:int)->float:
    if n<=k+1 or k<0 or not isfinite(loglik):
        raise ValueError("AICc requires n > k+1 and finite log-likelihood")
    return -2*loglik+2*k+2*k*(k+1)/(n-k-1)
