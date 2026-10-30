"""Constructive non-identification of internal adaptive query from Stage14 order effect.

The agent NEVER selects which cue to observe. A wind-dependent passive
first/second cue weight yields a nonzero order×wind effect despite a
simultaneous latest external refresh. Pure math; not bee source data.
"""
from __future__ import annotations
import math,json,argparse
from pathlib import Path

def passive_choice(first_weight,second_weight,refresh_weight,reward_first):
    values=(first_weight,second_weight,refresh_weight)
    if not all(isinstance(x,(float,int)) and math.isfinite(x) and x>=0 for x in values):
        raise ValueError('NO_GO_NEGATIVE_OR_NONFINITE_PASSIVE_WEIGHTS')
    reward=(first_weight if reward_first else second_weight)+refresh_weight
    handling=(second_weight if reward_first else first_weight)+refresh_weight
    score=reward-handling
    return 1/(1+math.exp(-score))

def order_by_wind(first_calm,second_calm,first_wind,second_wind,last_refresh,high,low):
    if not all(isinstance(v,(int,float)) and math.isfinite(v) for v in (high,low)) or high<=low or low<0:
        raise ValueError('NO_GO_REWARD_ORDER_OR_UNIT')
    output={}
    for wind,first,second in (('calm',first_calm,second_calm),
                              ('crosswind',first_wind,second_wind)):
        p_r=passive_choice(first,second,last_refresh,True)
        p_h=passive_choice(first,second,last_refresh,False)
        output[wind]={
          'P_high_given_reward_first':p_r,
          'P_high_given_handling_first':p_h,
          'order_effect_high_choice':p_r-p_h,
          'order_effect_consumed_mg_s':(high-low)*(p_r-p_h)}
    d=output['crosswind']['order_effect_consumed_mg_s']-output['calm']['order_effect_consumed_mg_s']
    return {'delta_mg_s':d,'by_wind':output,
            'high_reward_outcome_mg_s':high,'low_reward_outcome_mg_s':low,
            'latest_refresh_weight_shared_both_cues':last_refresh}

def witness():
    params={'first_calm':1.,'second_calm':1.,'first_wind':2.,
            'second_wind':1.,'last_refresh':1.,'high':.34,'low':.30}
    result=order_by_wind(**params)
    return {
      'status':'CONSTRUCTIVE_NONIDENTIFICATION_OF_INTERNAL_ACTIVE_QUERY_POLICY',
      'parameters_all_illustrative_not_biological_data':params,
      'passive_fixed_forced_cues_only':True,
      'bee_selects_which_cue_to_sample':False,
      'latest_external_reward_handling_refresh_identical':True,
      'calm_order_effect_high_reward_choice':result['by_wind']['calm']['order_effect_high_choice'],
      'crosswind_order_effect_high_reward_choice':result['by_wind']['crosswind']['order_effect_high_choice'],
      'order_by_wind_intake_contrast_mg_s':result['delta_mg_s'],
      'analytical_expression':'(high-low)*(tanh((first_wind-second_wind)/2)-tanh((first_calm-second_calm)/2))',
      'mathematical_not_organism_level_causal_claim':True,
      'conclusion':'A nonzero randomized presentation order × wind intake effect with equal latest cue time does not uniquely identify adaptive self-directed information acquisition, because passive wind-dependent primacy can generate the same effect.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='bee_stage14_design_outputs')
    root=Path(p.parse_args().out);root.mkdir(parents=True,exist_ok=True)
    receipt=witness()
    (root/'stage14_passive_primacy_counterexample.json').write_text(json.dumps(receipt,indent=2))
    print('STAGE14_PASSIVE_PRIMACY_COUNTEREXAMPLE '+json.dumps(receipt),flush=True)