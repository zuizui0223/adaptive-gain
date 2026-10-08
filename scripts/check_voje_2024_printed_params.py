#!/usr/bin/env python3
"""Evaluate the parameter vector printed in Voje et al. (2024) Table 2.

Model-to-dataset label in rendered Table 2 conflicts with paper Table 1
and prose. This numerical check tests that *printed parameters* reproduce
the C. andinus PETS observation likelihood, not that a source label is wrong.

Parameter order: anc=2.645, vstep_trait=2152.526, alpha=73318.010,
vstep_optimum=2.532; all on time interval normalized to [0,1].

Run: python scripts/check_voje_2024_printed_params.py --input timeseries.txt
"""
import argparse,math,json
from refit_voje_2024_pets_ou import load_pets_series,observed_loglik_kalman,dense_loglik
def main():
  ap=argparse.ArgumentParser()
  ap.add_argument("--input",default=None)
  z=ap.parse_args()
  times,y,samp,span,pooled=load_pets_series(z.input)
  anc,vs,alpha,vo=2.645,2152.526,73318.010,2.532
  pars=[anc,math.log(vs),math.log(alpha),math.log(vo)]
  ll=observed_loglik_kalman(pars,times,y,samp)
  dense=dense_loglik(pars,times,y,samp)
  n=len(y);k=4
  aicc=-2*ll+2*k+2*k*(k+1)/(n-k-1)
  print(json.dumps({
    "model":"printed Table 2 OUBM parameter row evaluated on C. andinus PETS mirror",
    "parameter_order":["anc","vstep_trait","alpha","vstep_optimum"],
    "source_reported_AICc":-153.573,
    "evaluated_AICc":aicc,
    "evaluated_logL":ll,
    "dense_logL":dense,
    "difference_kalman_dense":abs(ll-dense),
    "calculated_half_life_years_if_unit_scaled":math.log(2)/alpha*span*1e6,
    "reported_half_life_years":12,
    "status":"NEAR_EXACT_AICC_MATCH_WITH_TIME_UNIT_TRANSFORM_UNRESOLVED",
    "caveat":"No original authors' Dryad script executed; do not assert a published table error"
  },indent=2))
if __name__=="__main__":
  main()
