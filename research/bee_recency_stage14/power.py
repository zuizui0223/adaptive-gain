"""Uncalibrated assumed independent-colony Student-t power. No observed bees."""
from __future__ import annotations
import math,json,argparse
from pathlib import Path
from scipy.stats import t,nct

BEE_PER_COLONY=12
CELL_TRIALS=8
ALPHA=.05

def _power(colonies,delta,sd):
    df=colonies-1
    cut=float(t.ppf(1-ALPHA/2,df))
    ncp=delta*math.sqrt(colonies)/sd
    return float(nct.sf(cut,df,ncp)+nct.cdf(-cut,df,ncp))

def comparison(colonies=24,true_delta=.020,sigma_colony=.025,
               sigma_bee=.030,sigma_trial=.080,bees=BEE_PER_COLONY):
    if not isinstance(colonies,int) or colonies<3 or not isinstance(bees,int) or bees<2:
        raise ValueError('NO_GO_ASSUMED_INDEPENDENT_COLONIES_OR_BEES')
    if not 0<=sigma_colony<1 or not 0<=sigma_bee<1 or not 0<sigma_trial<1:
        raise ValueError('NO_GO_ASSUMED_VARIANCE')
    if not 0<=true_delta<1:raise ValueError('NO_GO_ASSUMED_EFFECT')
    def contrast_sd(nt):
        return math.sqrt(sigma_colony**2+sigma_bee**2/bees+
                         4*sigma_trial**2/(bees*nt))
    sdnew=contrast_sd(CELL_TRIALS)
    sdprior=contrast_sd(16)
    return {
      'n_independent_colonies':colonies,'bees_per_colony':bees,
      'refreshed_arm_trials_per_order_wind_cell_per_bee':CELL_TRIALS,
      'no_refresh_arm_trials_per_order_wind_cell_per_bee':CELL_TRIALS,
      'total_qa_trials':colonies*bees*64,
      'assumed_delta_mg_s':true_delta,'assumed_sigma_colony':sigma_colony,
      'assumed_sigma_bee':sigma_bee,'assumed_sigma_trial':sigma_trial,
      'assumed_colony_DID_sd_new_mg_s':sdnew,
      'new_power_if_assumptions_true':_power(colonies,true_delta,sdnew),
      'original_stage9_power_if_assumptions_true':_power(colonies,true_delta,sdprior),
      'all_sds_are_assumptions_not_data':True,
      'zero_mass_and_non_gaussian_animal_outcomes_not_modelled':True,
      'not_an_actual_experiment_or_power_estimate':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='bee_stage14_design_outputs')
    root=Path(p.parse_args().out);root.mkdir(parents=True,exist_ok=True)
    records=[comparison(c,true_delta=.02,sigma_colony=s)
             for c in (12,16,24,32,48) for s in (.025,.04)]
    result={'status':'POWER_ASSUMPTIONS_ONLY','cases':records}
    (root/'stage14_assumed_power_receipt.json').write_text(json.dumps(result,indent=2))
    print('STAGE14_ASSUMED_POWER_QA '+json.dumps(result),flush=True)