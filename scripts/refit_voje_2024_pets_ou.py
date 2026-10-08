#!/usr/bin/env python3
"""Independent, reproducible PETS-mirror OUBM refit for Voje et al. (2024).

Uses no evoTS or paleoTS fitting code. The two-state Gaussian state-space
Kalman likelihood is analytically equivalent to evoTS logL.joint.OU.BM with
opt.anc=TRUE. Uses the 266 observations labelled tsID 582 in the public
PETS mirror; it is NOT a byte-verified Dryad-author-archive refit.

Requires: numpy, scipy. Example:
  python scripts/refit_voje_pets_ou.py
  python scripts/refit_voje_pets_ou.py --input timeseries.txt
"""
import argparse
import csv
import io
import json
import math
from pathlib import Path
from urllib.request import urlopen

import numpy as np
from scipy.optimize import minimize
from scipy.linalg import cholesky, solve_triangular

SOURCE_SHA = "718d603c49ae640e34a5c36c93bcd8ba36d1e389"
DATA_URL = (
    "https://raw.githubusercontent.com/VildeBruhn/rate_time/"
    + SOURCE_SHA + "/empirical_data/timeseries.txt"
)
SERIES_ID = 582

def load_pets_series(path=None):
    if path:
        text = Path(path).read_text(encoding="utf-8")
    else:
        with urlopen(DATA_URL, timeout=35) as response:
            text = response.read().decode("utf-8")
    obs = [row for row in csv.DictReader(io.StringIO(text), delimiter="\t")
           if int(row["tsID"]) == SERIES_ID]
    obs.sort(key=lambda row: float(row["age_MY"]))
    if len(obs) != 266:
        raise RuntimeError(f"Expected 266 C. andinus PETS rows; got {len(obs)}")
    time_raw = np.array([float(x["age_MY"]) for x in obs])
    interval = float(time_raw[-1]-time_raw[0])
    tt = (time_raw-time_raw[0])/interval
    y = np.array([float(x["trait_mean"]) for x in obs])
    vv = np.array([float(x["trait_var"]) for x in obs])
    nn = np.array([float(x["N"]) for x in obs])
    if not np.all(np.diff(tt) > 0):
        raise ValueError("The independent Kalman likelihood expects unique increasing times")
    if abs(interval-0.30941525) > 1e-9 or abs(y[0]-2.644626001)>1e-8:
        raise ValueError("PETS source fingerprint changed: inspect provenance before fitting")
    pooled = float(np.sum((nn-1)*vv)/np.sum(nn-1))
    # PETS trait_mean is already around 2.645 ln(micrometres). Applying
    # ln.paleoTS again would create a second, incorrect logarithm.
    return tt, y, pooled/nn, interval, pooled

def q_integrals(alpha, dt):
    w = alpha*dt
    e = math.exp(-w)
    if w < 0.01:
        f1 = 1-w+(2/3)*w*w-(1/3)*w*w*w
        f2 = w/2-w*w/6+w*w*w/24-w**4/120
        g = w*w/3-w**3/4+7*w**4/60
    else:
        h = -math.expm1(-w)
        h2 = -math.expm1(-2*w)
        f1 = h2/(2*w)
        f2 = 1-h/w
        g = 1-2*h/w+h2/(2*w)
    return e, dt*f1, dt*f2, dt*g

def observed_loglik_kalman(x, times, obs, measurement_variance):
    anc, log_vs, log_alpha, log_vo = x
    vs, alpha, vo = map(math.exp, (log_vs, log_alpha, log_vo))
    # Broad optimizer guardrails, no biological claim about their bounds.
    if (not all(map(math.isfinite, (anc,vs,alpha,vo))) or
        min(vs,alpha,vo)<1e-14 or alpha>1e11):
        return -1e100
    mx = my = anc
    p00 = p01 = p11 = 0.0
    ll = 0.0
    for i in range(len(obs)):
        if i:
            dt = float(times[i]-times[i-1])
            e, i1, i2, i3 = q_integrals(alpha, dt)
            h = 1-e
            mx_next=e*mx+h*my
            p00_next=e*e*p00+2*e*h*p01+h*h*p11+vs*i1+vo*i3
            p01_next=e*p01+h*p11+vo*i2
            p11_next=p11+vo*dt
            mx,p00,p01,p11=mx_next,p00_next,p01_next,p11_next
        s = p00+float(measurement_variance[i])
        if s<=0 or not math.isfinite(s):
            return -1e100
        error = float(obs[i])-mx
        ll -= 0.5*(math.log(2*math.pi)+math.log(s)+error*error/s)
        k0,k1=p00/s,p01/s
        mx+=k0*error
        my+=k1*error
        p11-=k1*p01
        p01-=k0*p01
        p00-=k0*p00
    return ll if math.isfinite(ll) else -1e100

def dense_loglik(x,times,y,mvar):
    """Independent covariance implementation matching evoTS source formula."""
    anc, log_vs, log_alpha, log_vo = x
    vs,alpha,vo=map(math.exp,(log_vs,log_alpha,log_vo))
    ta=np.minimum.outer(times,times)
    hd=np.abs(np.subtract.outer(times,times))
    eh=np.exp(-alpha*hd)
    em=np.exp(-alpha*ta)
    e2=np.exp(-alpha*(hd+2*ta))
    cov=vs*(eh-e2)/(2*alpha)+vo*(ta-(1+eh)*(1-em)/alpha+(eh-e2)/(2*alpha))
    cov.flat[::len(times)+1] += mvar
    L=cholesky(cov,lower=True,check_finite=True)
    residual=solve_triangular(L,y-anc,lower=True,check_finite=True)
    logdet=2*float(np.log(np.diag(L)).sum())
    return float(-0.5*(len(y)*math.log(2*math.pi)+logdet+np.dot(residual,residual)))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",help="Local PETS timeseries.txt, otherwise pinned GitHub raw")
    ap.add_argument("--output",help="Optional JSON receipt destination")
    args=ap.parse_args()
    t,y,mvar,interval,pool=load_pets_series(args.input)
    def objective(x):
        return -observed_loglik_kalman(x,t,y,mvar)
    starts=[20,200,2000,10000,20000,80000]
    best=None
    for alpha_start in starts:
        init=np.array([y[0],math.log(500.0),math.log(alpha_start),math.log(2.5)])
        res=minimize(objective,init,method="L-BFGS-B",
          bounds=[(float(y.min())-2,float(y.max())+2),
                  (-15,20),(-15,27),(-15,20)],
          options={"maxiter":650,"ftol":1e-12})
        if best is None or res.fun<best.fun:
            best=res
    anc, log_vs, log_alpha, log_vo=map(float,best.x)
    alpha=math.exp(log_alpha)
    ll=-float(best.fun)
    dense=dense_loglik(best.x,t,y,mvar)
    if abs(ll-dense)>1e-6:
        raise AssertionError(f"Kalman and dense Gaussian likelihood differ: {ll} vs {dense}")
    aicc=-2*ll+2*4+2*4*5/(len(y)-4-1)
    h=math.log(2)/alpha*interval*1e6
    report={
       "status":"INDEPENDENT_PETS_MIRROR_FIT_NOT_DRYAD_BYTE_VERIFIED",
       "source_repo":"VildeBruhn/rate_time",
       "source_commit":SOURCE_SHA,
       "source_file":"empirical_data/timeseries.txt",
       "series_id":SERIES_ID,
       "n":len(y),"interval_my":interval,"first_trait_mean":float(y[0]),
       "variance_pooling":"weighted by within-population sample df N-1",
       "pooled_within_sample_variance":pool,
       "source_trait_unit":"already log micrometres; do not apply second log",
       "opt_anc":True,"scale":"time 0..1",
       "params":{"anc":anc,"vstep_trait":math.exp(log_vs),
                 "alpha_unit_interval":alpha,"vstep_optimum":math.exp(log_vo)},
       "logL_kalman":ll,"logL_dense":dense,"dense_error":abs(ll-dense),
       "AICc":aicc,"half_life_years":h,
       "reported_AICc":-153.573,"reported_half_life_years":12,
       "delta_AICc":aicc-(-153.573),
       "optimizer_success":bool(best.success),"optimizer_message":str(best.message),
       "caveats":[
          "PETS is an independent publicly mirrored dataset, not a Dryad byte-identical reconstruction.",
          "Authors' archive R script, variance handling and exact parameter/time mapping remain unverified.",
          "AICc proximity and half-life agreement do not demonstrate empirical causal feedback.",
          "The exact reciprocal gauge still requires independently meaningful biological latent-state semantics."
       ]
    }
    result=json.dumps(report,indent=2,ensure_ascii=False)
    print(result)
    if args.output:
        Path(args.output).write_text(result+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
