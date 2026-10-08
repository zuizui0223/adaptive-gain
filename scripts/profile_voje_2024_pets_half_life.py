#!/usr/bin/env python3
"""Independent profile of Voje 2024 OUBM observation-model half-life.

Not a source-author archive reconstruction. Uses pinned PETS mirror (tsID582),
with same pooled variance convention as refit_voje_2024_pets_ou.py.
Profiles each fixed half-life against (anc, S=vs/(2 alpha), vo).

Requires numpy scipy and network or --input pinned PETS timeseries.txt.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import math
import numpy as np
from scipy.optimize import minimize
from refit_voje_2024_pets_ou import (
    load_pets_series,observed_loglik_kalman
)

HALF_LIVES_YR=[.01,.1,.5,1,2,3,5,8,10,12,15,20,24,30,36,48,60,80,100,150]
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",default=None)
    parser.add_argument("--output",default=None)
    args=parser.parse_args()
    t,y,mvar,span,pool=load_pets_series(args.input)
    observations=[]
    for h in HALF_LIVES_YR:
        alpha=math.log(2)*span*1e6/h
        def nll(z):
            anc, logS, logVo=map(float,z)
            return -observed_loglik_kalman(
              [anc,math.log(2*alpha)+logS,math.log(alpha),logVo],t,y,mvar)
        solutions=[]
        for init in [
            [2.652,math.log(.01477),math.log(2.52)],
            [2.645,math.log(.02),math.log(1.5)]
        ]:
            res=minimize(nll,init,method="L-BFGS-B",
              bounds=[(float(y.min())-2,float(y.max())+2),(-14,12),(-14,12)],
              options={"maxiter":1200,"ftol":1e-12})
            solutions.append(res)
        best=min(solutions,key=lambda z:z.fun)
        observations.append({
           "half_life_years":h, "alpha_unit":alpha,
           "logL":float(-best.fun),
           "ancestral_mean":float(best.x[0]),
           "stationary_trait_variance":float(math.exp(best.x[1])),
           "moving_optimum_diffusion":float(math.exp(best.x[2])),
           "optimizer_success":bool(best.success)
        })
    mx=max(r["logL"] for r in observations)
    for r in observations:
        r["delta_logL_from_profile_grid_max"]=r["logL"]-mx
    report={
      "source":"PETS mirror tsID582; independent Gaussian Kalman likelihood",
      "n":len(y),"span_years":span*1e6,
      "method":"Fix half-life, optimize mean/S/vo; interval profile grid only",
      "calibration":"Likelihood differences are not confidence intervals; boundary LR asymptotics not established",
      "points":observations,
      "interpretation":"Fast-alpha saturation (random-walk latent process plus positive-time nugget); does not itself prove a reciprocal ecological mechanism"
    }
    output=json.dumps(report,indent=2)
    print(output)
    if args.output:
        Path(args.output).write_text(output+"\n",encoding="utf-8")
if __name__=="__main__":
    main()
