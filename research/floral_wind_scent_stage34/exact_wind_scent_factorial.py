"""Stage34: source-free exact wind x floral scent interaction decomposition.

A 2x2 *intervention* would assign odor ON/OFF and wind LOW/HIGH
separately while holding display, color, morphology and reward comparable.
THIS IS NOT AN OBSERVED FOUR-ARM STUDY. Existing Crall 2020 wind-at-scent
stations and Haverkamp 2016 scent ON/OFF do not form a valid pooled 2x2.

Both stage and endpoint-specific interactions are calculable but different:
- relative plume/detection benefit
- arrival x landing x pollen success benefit
Positive wind-by-scent for detection does NOT imply a positive net wind effect
on a scented flower or an experimentally measured plant fitness interaction.
"""
from __future__ import annotations
from fractions import Fraction as F
import json
from pathlib import Path

CORNERS=('calm_scent_off','wind_scent_off','calm_scent_on','wind_scent_on')
STAGES=('discovery','landing_given_discovery','pollen_given_landing')


def _prob(k,v):
    if type(v) not in (int,F):
        raise ValueError('NO_GO_NO_SOURCE_EXACT_PROBABILITY_'+k.upper())
    val=F(v)
    if val<0 or val>1:
        raise ValueError('NO_GO_OUT_OF_RANGE_'+k.upper())
    return val


def _state(x):
    if not isinstance(x,dict) or set(x)!=set(STAGES):
        raise ValueError('NO_GO_INCOMPLETE_STAGE_DECOMPOSITION')
    return {k:_prob(k,x[k]) for k in STAGES}


def full_factorial(cells):
    """All differences are exact, based on caller-specified conditional rates."""
    if not isinstance(cells,dict) or set(cells)!=set(CORNERS):
        raise ValueError('NO_GO_MISSING_WIND_OR_SCENT_CELL')
    x={k:_state(v) for k,v in cells.items()}
    v={k:x[k]['discovery']*x[k]['landing_given_discovery']*
       x[k]['pollen_given_landing'] for k in CORNERS}
    a,b,c,d=(CORNERS)
    wind_discovery_without=x[b]['discovery']-x[a]['discovery']
    wind_discovery_with=x[d]['discovery']-x[c]['discovery']
    discovery_interaction=wind_discovery_with-wind_discovery_without
    wind_net_without=v[b]-v[a]
    wind_net_with=v[d]-v[c]
    net_interaction=wind_net_with-wind_net_without
    landing_interaction=(x[d]['landing_given_discovery']-x[c]['landing_given_discovery'])-(
        x[b]['landing_given_discovery']-x[a]['landing_given_discovery'])
    return {
        'status':'EXACT_ASSUMED_2X2_INTERACTION_NOT_EMPIRICAL',
        'wind_effect_on_discovery_if_scent_off':wind_discovery_without,
        'wind_effect_on_discovery_if_scent_on':wind_discovery_with,
        'wind_x_scent_detection_interaction':discovery_interaction,
        'wind_x_scent_landing_interaction_conditional':landing_interaction,
        'per_original_opportunity_pollen_transfer':v,
        'wind_effect_on_pollen_transfer_if_scent_off':wind_net_without,
        'wind_effect_on_pollen_transfer_if_scent_on':wind_net_with,
        'wind_x_scent_pollen_interaction':net_interaction,
        'wind_on_scented_flower_absolute_benefit':wind_net_with>0,
        'positive_relative_scent_wind_detection_advantage':discovery_interaction>0,
        'no_species_wide_fragrance_wind_conclusion':True,
        'no_original_four_arm_data_supplied':True,
        'no_inferred_causal_mediation':True,
        'nested_stages_assumed_same_cohort_not_observed':True
    }


def constructed_counterexample():
    """Wind makes odor-bearing flower *less harmed*, not necessarily helped."""
    off_calm={'discovery':F(3,10),'landing_given_discovery':F(4,5),
              'pollen_given_landing':F(3,4)}
    off_wind={'discovery':F(3,10),'landing_given_discovery':F(1,2),
              'pollen_given_landing':F(3,4)}
    on_calm={'discovery':F(2,5),'landing_given_discovery':F(4,5),
             'pollen_given_landing':F(3,4)}
    on_wind={'discovery':F(3,5),'landing_given_discovery':F(1,2),
             'pollen_given_landing':F(3,4)}
    result=full_factorial(dict(zip(CORNERS,(off_calm,off_wind,on_calm,on_wind))))
    assert result['wind_x_scent_detection_interaction']==F(1,5)
    assert result['wind_x_scent_pollen_interaction']==F(21,400)
    assert result['wind_effect_on_pollen_transfer_if_scent_on']==-F(3,200)
    assert result['wind_effect_on_pollen_transfer_if_scent_off']==-F(27,400)
    assert not result['wind_on_scented_flower_absolute_benefit']
    return result


def preexisting_source_design_gate():
    return {
      'status':'NO_GO_NO_ORIGINAL_2X2_WIND_BY_SCENT_EXPERIMENT_EXTRACTED',
      'wind_plus_odor_source':'Crall et al 2020 doi:10.1098/rsbl.2020.0103',
      'wind_plus_odor_design':'within scented-bait station variation; missing independent scent-off factorial control',
      'scent_on_off_source':'Haverkamp et al 2016 doi:10.7554/eLife.15039',
      'scent_on_off_design':'wild-type-like scented vs nonemitting flowers; NOT a fully crossed calm-vs-windy factorial',
      'scent_on_off_prior_result':'similar moth visitation/approach; scent-bearing flowers had higher seed production',
      'required_design':'randomize odor on/off with matched display, controls and two or more wind regimes in one original experiment',
      'required_measurements':'matched independent trials of odor flux/blend, airflow/plume, original detection opportunities, landing given detection, pollen deposition, original plant seed/siring outcomes',
      'no_valid_pooled_cross_paper_interaction':True,
      'zero_empirical_2x2_effects_extracted':True,
      'not_a_meta_analytical_result':True
    }


if __name__=='__main__':
    def stringify(v):
        if isinstance(v,F):return str(v)
        if isinstance(v,dict):return {k:stringify(x) for k,x in v.items()}
        return v
    print(json.dumps(stringify({
        'source_gate':preexisting_source_design_gate(),
        'assumed_counterexample':constructed_counterexample()
    }),indent=2,sort_keys=True))
