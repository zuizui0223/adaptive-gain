#!/usr/bin/env python3
"""Compare OUBM finite rate to independently defined BM + biological nugget.

For reproducibility, use the pinned public PETS mirror (tsID582).
Does not claim an author's-archive, model-selection, or ecological-mechanism
definitive verdict. Requires numpy/scipy for numerical fitting.
"""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
from scipy.optimize import minimize
from refit_voje_2024_pets_ou import load_pets_series, observed_loglik_kalman
from adaptive_gain.ou_nugget_state_space import loglik_random_walk_with_nugget,aicc

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",default=None)
    parser.add_argument("--output",default=None)
    options=parser.parse_args()
    t,y,measurement,span,pool=load_pets_series(options.input)
    def neg(z):
        m,logS,logD=map(float,z)
        return -loglik_random_walk_with_nugget(
            t,y,measurement,m,math.exp(logD),math.exp(logS))
    init=[float(y[0]),math.log(.01467),math.log(2.53)]
    fit=minimize(neg,init,method="L-BFGS-B",
       bounds=[(float(y.min())-2,float(y.max())+2),(-15,12),(-15,12)],
       options={"maxiter":1100,"ftol":1e-13})
    logL=-float(fit.fun)
    report={"status":"PETS_MIRROR_3_PARAMETER_ALTERNATIVE",
            "n":len(y),"model":"Brownian latent movement + independent positive-time biological nugget",
            "parameters":{"initial_trait_mean":float(fit.x[0]),
                          "independent_nugget_variance":math.exp(float(fit.x[1])),
                          "brownian_diffusion_unit":math.exp(float(fit.x[2]))},
            "logL":logL,"AICc_3parameter":aicc(logL,len(y),3),
            "finite_OUBM_AICc_4parameter_reference":-153.6573645396676,
            "delta_AICc_vs_finite_OUBM":aicc(logL,len(y),3)-(-153.6573645396676),
            "optimizer_success":bool(fit.success),
            "caveats":[
                "AICc gap of about two is modest, not decisive model rejection.",
                "This model is the alpha->infinity fixed-stationary-variance boundary of OUBM.",
                "Temporal independence of each fossil-age nugget is a biological assumption.",
                "PETS source mirror is not original Dryad script or byte-verified data.",
                "This alternative does not establish reciprocal ecological feedback."
            ]}
    result=json.dumps(report,indent=2)
    print(result)
    if options.output:
        Path(options.output).write_text(result+"\n")
if __name__=="__main__":
    main()
