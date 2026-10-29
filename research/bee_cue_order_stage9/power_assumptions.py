"""Stage 9 prospective independent-colony factorial interaction power.

All numerical values are ILLUSTRATIVE ASSUMPTIONS, not fitted or estimated
from bees. Use a two-tailed Student t test of *independent colony contrast
means*. Thousands of trials within each colony are REPEATED measurements;
never calculate power as if n = total trial count were independent colonies.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from scipy.stats import t as student_t, nct

BASE_SD_COLONY_INTERACTION=0.025  # assumed mg sucrose / s
BASE_SD_BEE_INTERACTION=0.030     # assumed mg sucrose / s
BASE_SD_TRIAL=0.080               # assumed mg sucrose / s
BEE_PER_COLONY=12
TRIAL_PER_CELL_PER_BEE=16
COLONY_SCENARIOS=(8,12,16,24,32,48)
EFFECT_SCENARIOS=(0.010,0.020,0.030)
COLONY_VARIANCE_SCENARIOS=(0.025,0.040)
ALPHA=0.05

def sd_of_colony_contrast(sigma_colony, sigma_bee, sigma_trial,
                          bees=BEE_PER_COLONY,cell_trials=TRIAL_PER_CELL_PER_BEE):
    """Exact independent Gaussian balanced 2x2 colony-DID SD assumption."""
    if not (0<=sigma_colony<1 and 0<=sigma_bee<1 and 0<sigma_trial<1):
        raise ValueError("NO_GO_ILLEGAL_ASSUMED_VARIANCE")
    if bees<2 or cell_trials<1:
        raise ValueError("NO_GO_INSUFFICIENT_BEES_OR_TRIALS")
    variance=(sigma_colony*sigma_colony +
              (sigma_bee*sigma_bee)/bees +
              4*sigma_trial*sigma_trial/(bees*cell_trials))
    return math.sqrt(variance)

def noncentral_t_power(n_colonies,delta_mg_per_sec,sd_delta,
                       alpha=ALPHA):
    """Two-sided independent-colony paired interaction contrast t power."""
    if n_colonies<3 or not isinstance(n_colonies,int):
        raise ValueError("NO_GO_INSUFFICIENT_SOURCE_COLONIES")
    if not (sd_delta>0 and math.isfinite(sd_delta)):
        raise ValueError("NO_GO_BAD_COLONY_INTERACTION_SD")
    if not (0<alpha<.5) or not math.isfinite(delta_mg_per_sec):
        raise ValueError("NO_GO_BAD_POWER_ENDPOINT")
    df=n_colonies-1
    critical=float(student_t.ppf(1-alpha/2,df))
    ncp=delta_mg_per_sec*math.sqrt(n_colonies)/sd_delta
    return float(nct.sf(critical,df,ncp)+nct.cdf(-critical,df,ncp))

def power_table():
    results=[]
    for sigma_colony in COLONY_VARIANCE_SCENARIOS:
        sd=sd_of_colony_contrast(
            sigma_colony,BASE_SD_BEE_INTERACTION,BASE_SD_TRIAL)
        for true_delta in EFFECT_SCENARIOS:
            for colonies in COLONY_SCENARIOS:
                p=noncentral_t_power(colonies,true_delta,sd)
                results.append({
                    "n_independent_colonies":colonies,
                    "bees_per_colony":BEE_PER_COLONY,
                    "trials_per_bee_per_factorial_cell":TRIAL_PER_CELL_PER_BEE,
                    "total_randomized_trials":4*colonies*BEE_PER_COLONY*
                                              TRIAL_PER_CELL_PER_BEE,
                    "hypothesized_true_order_x_wind_delta_mg_s":true_delta,
                    "assumed_colony_interaction_sd_mg_s":sigma_colony,
                    "assumed_bee_interaction_sd_mg_s":BASE_SD_BEE_INTERACTION,
                    "assumed_single_trial_residual_sd_mg_s":BASE_SD_TRIAL,
                    "derived_colony_contrast_sd_mg_s":sd,
                    "two_sided_alpha":ALPHA,
                    "power_independent_colony_student_t":p,
                    "standard_error_if_sd_known_mg_s":sd/math.sqrt(colonies)
                })
    min_requirement=[]
    for sigma_colony in COLONY_VARIANCE_SCENARIOS:
        for delta in EFFECT_SCENARIOS:
            matching=[r for r in results if
                      r["assumed_colony_interaction_sd_mg_s"]==sigma_colony and
                      r["hypothesized_true_order_x_wind_delta_mg_s"]==delta and
                      r["power_independent_colony_student_t"]>=0.8]
            min_requirement.append({
                "delta_mg_s":delta,"sigma_colony_mg_s":sigma_colony,
                "minimum_tested_independent_colonies_for_at_least_80pct_power":
                    min((x["n_independent_colonies"] for x in matching),default=None),
                "caveat":"Not a prior study empirical effect or observed colony variance"
            })
    return {
        "status":"ASSUMED_MODEL_ONLY_NO_LIVE_BEE_DATA",
        "model":"two-sided noncentral Student t, independent original colony 2x2 DID means",
        "variance_formula":"sigma_colony_Delta^2 + sigma_bee_Delta^2/B + 4*sigma_trial^2/(B*T)",
        "effect_units":"mg actual consumed sucrose per 30-second observation / 30 s = mg/s",
        "colony_counts_tested":list(COLONY_SCENARIOS),
        "effect_sizes_assumed":list(EFFECT_SCENARIOS),
        "colony_heterogeneity_scenarios":list(COLONY_VARIANCE_SCENARIOS),
        "fully_randomized_ITT_not_success_conditioned":True,
        "sample_size_targets_not_actual_recruited_animals":True,
        "gaussian_balanced_heteroscedasticity_and_zero_intake_NOT_MODELED":True,
        "data_based_sample_size_changes_forbidden_after_unblinding":True,
        "all_power_cases":results,
        "minimum_within_tested_grid":min_requirement
    }

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="bee_stage9_design_output")
    a=ap.parse_args(argv)
    out=Path(a.out)
    out.mkdir(parents=True,exist_ok=True)
    data=power_table()
    (out/"bee_stage9_assumption_only_power.json").write_text(
        json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False))
    display=[r for r in data["all_power_cases"]
             if r["hypothesized_true_order_x_wind_delta_mg_s"]==.02]
    print("STAGE9_ASSUMPTION_ONLY_POWER_FOR_DELTA_0p02 "+
          json.dumps(display,ensure_ascii=False,allow_nan=False),flush=True)
    print("STAGE9_POWER_PLANNING_COMPLETED_WITHOUT_BEE_OBSERVATIONS",flush=True)

if __name__=="__main__":main()
