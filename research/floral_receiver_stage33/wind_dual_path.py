"""Stage33: wind has opposed information-transport and mechanical routes.

Source-free finite examples only: numbers below are hypothetical probabilities,
NOT wind-tunnel measurements, effect estimates, or a universal wind optimum.

Within ONE well-defined floral encounter opportunity:
  D = P(flower/display discovered by the focal receiver)
  L = P(successful landing | that discovery)
  T = P(legitimate pollen delivery | that landing)
  V = D * L * T
All three stage probabilities must be measured in the SAME source/cohort, or
the product cannot be interpreted as an observed field-pollination rate.

The counterfactual wind path is ordered:
  discovery effect = (D_w-D_0)*L_0*T_0
  landing effect   = D_w*(L_w-L_0)*T_0
  transfer effect  = D_w*L_w*(T_w-T_0).
The sum is an exact algebraic chain identity, not causal identification.
"""
from __future__ import annotations
from fractions import Fraction as F
import csv
from pathlib import Path

WIND_PATHS=('odour_transport','olfactory_recognition','aerodynamic_control',
            'wind_driven_flower_motion','post_landing_handling','pollen_transfer')
REQUIRED_WIND_FIELDS=(
  'source_id','year','source_type','source_doi','source_dataset',
  'receivers','setting','wind_metric','plume_transport_or_detection',
  'landing_or_flight','between_flower_or_transfer','grounded_result','not_identified'
)


def _p(name,value):
    if type(value) not in (int,F):
        raise ValueError('NO_GO_NON_EXACT_OR_UNSOURCED_'+name.upper())
    value=F(value)
    if value<0 or value>1:
        raise ValueError('NO_GO_NON_PROBABILITY_'+name.upper())
    return value


def _stage_row(state):
    if not isinstance(state,dict) or set(state)!={'discovery','landing_given_discovery','transfer_given_landing'}:
        raise ValueError('NO_GO_MISSING_STAGE_PROBABILITIES')
    d=_p('discovery',state['discovery'])
    l=_p('landing_given_discovery',state['landing_given_discovery'])
    t=_p('transfer_given_landing',state['transfer_given_landing'])
    return d,l,t


def dual_wind_decomposition(calm,wind):
    """Exact sign-separated stage decomposition under paired counterfactual states."""
    d0,l0,t0=_stage_row(calm)
    d1,l1,t1=_stage_row(wind)
    transport=(d1-d0)*l0*t0
    landing=d1*(l1-l0)*t0
    transfer=d1*l1*(t1-t0)
    overall=d1*l1*t1-d0*l0*t0
    if transport+landing+transfer!=overall:
        raise AssertionError('NO_GO_ALGEBRAIC_WIND_PATH_IDENTITY')
    if d1==0 or t0==0:
        threshold=None
    else:
        # If pollen per landing unchanged, minimum windy landing success
        # to match calm plant delivery, not an estimated biological threshold.
        threshold=d0*l0/d1
    return {
      'original_per_opportunity_transfer':d0*l0*t0,
      'windy_per_opportunity_transfer':d1*l1*t1,
      'wind_minus_calm':overall,
      'odour_or_other_detection_component':transport,
      'mechanical_landing_component':landing,
      'per_landing_pollen_transfer_component':transfer,
      'break_even_windy_landing_probability_if_transfer_unchanged':threshold,
      'wind_is_measured_condition_not_assumed_linear_predictor':True,
      'requires_same_cohort_and_sequential_denominators':True,
      'ordered_decomposition_is_not_a_statistical_mediation_test':True,
      'all_example_probabilities_hypothetical':True
    }


def wind_scenarios_source_free():
    """A constructive non-monotone example: no wind thresholds inferred."""
    calm={'discovery':F(3,10),'landing_given_discovery':F(4,5),
          'transfer_given_landing':F(3,4)}
    breeze={'discovery':F(3,5),'landing_given_discovery':F(1,2),
            'transfer_given_landing':F(3,4)}
    strong={'discovery':F(7,10),'landing_given_discovery':F(1,5),
            'transfer_given_landing':F(3,4)}
    compensated={'discovery':F(7,10),'landing_given_discovery':F(7,10),
                 'transfer_given_landing':F(3,4)}
    a=dual_wind_decomposition(calm,breeze)
    b=dual_wind_decomposition(calm,strong)
    c=dual_wind_decomposition(calm,compensated)
    if (a['wind_minus_calm'],b['wind_minus_calm'],c['wind_minus_calm']) != (
         F(9,200),-F(3,40),F(3,16)):
        raise AssertionError('NO_GO_CONSTRUCTED_WIND_SIGNS')
    if not (a['odour_or_other_detection_component']>0 and
            a['mechanical_landing_component']<0 and
            a['wind_minus_calm']>0):
        raise AssertionError('NO_GO_OPPOSED_PATHS')
    return {
        'calm':calm,
        'moderate_wind':{'rates':breeze,'decomposition':a},
        'strong_wind':{'rates':strong,'decomposition':b},
        'strong_wind_with_visual_motor_compensation':{
            'rates':compensated,'decomposition':c},
        'not_pollinator_measurements':True,
        'no_wind_speed_threshold_unless_measured':True
    }


def inspect_wind_source_ledger(filename):
    with Path(filename).open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames or ())!=REQUIRED_WIND_FIELDS:
            raise ValueError('NO_GO_WIND_LEDGER_SCHEMA')
        rows=list(reader)
    if len({r['source_id'] for r in rows})!=len(rows) or not rows:
        raise ValueError('NO_GO_SOURCE_DUPLICATED')
    if len(rows)<8:
        raise ValueError('NO_GO_WIND_EVIDENCE_INSUFFICIENT_FOR_SCOPING')
    for r in rows:
        if not r['source_dataset'].startswith(('https://','not_verified')):
            raise ValueError('NO_GO_WIND_SOURCE_NOT_TRACEABLE')
        if not r['source_doi'].startswith('10.'):
            raise ValueError('NO_GO_WIND_PRIMARY_DOI_NOT_IDENTIFIED')
        if not r['not_identified']:
            raise ValueError('NO_GO_WIND_CAUSAL_STOP_NOT_RECORDED')
    if not any('orchid_bee' in r['receivers'] for r in rows):
        raise ValueError('NO_GO_MISSING_POSITIVE_SCENT_ARRIVAL_STUDY')
    if not any('Bombus' in r['receivers'] for r in rows):
        raise ValueError('NO_GO_MISSING_BUMBLEBEE_LANDING_STUDY')
    if not any('bees_flies_butterflies' in r['receivers'] for r in rows):
        raise ValueError('NO_GO_MISSING_WIND_GUILD_REASSEMBLY')
    return {
       'status':'WIND_SOURCE_STUDIES_SCOPED_NO_UNIFIED_ESTIMATE',
       'distinct_reference_rows':len(rows),
       'all_effect_sizes_from_original_raw_studies_extracted':False,
       'no_claim_of_same_cohort_between_scent_and_landing_studies':True,
       'original_dataset_candidates':[
          '10.5281/zenodo.3675327','10.5281/zenodo.60234',
          '10.5061/dryad.4qrfj6qpf','10.17632/mww9m8r3dk.1'],
       'wind_cannot_be_reduced_to_one_ordinal_strength_score':True
    }


def measurement_contract(row):
    """No pretending a single weather-station mean identifies plume or landing."""
    keys=('original_session_id','plant_individual_id','receiver_id','original_source_url',
          'mean_wind_m_s','wind_direction_deg','gust_sd_m_s','flower_sway_displacement_cm',
          'plume_encounter_observed','discovery_observed','landing_observed',
          'pollen_transfer_observed')
    if type(row)is not dict or set(row)!=set(keys):
        raise ValueError('NO_GO_WIND_MISSING_MERGE_KEYS_OR_MEASURES')
    for k in ('original_session_id','plant_individual_id','receiver_id','original_source_url'):
        if not isinstance(row[k],str) or not row[k]:
            raise ValueError('NO_GO_SOURCE_GRAIN_UNIDENTIFIED')
    if not row['original_source_url'].startswith('https://'):
        raise ValueError('NO_GO_SOURCE_URL_INVALID')
    for key in ('mean_wind_m_s','wind_direction_deg','gust_sd_m_s',
                'flower_sway_displacement_cm'):
        if row[key] is not None and type(row[key]) not in (int,float,F):
            raise ValueError('NO_GO_WIND_NONNUMERIC_MEASUREMENT')
    if row['mean_wind_m_s'] is not None and row['mean_wind_m_s']<0:
        raise ValueError('NO_GO_NEGATIVE_WIND_SPEED')
    for k in ('plume_encounter_observed','discovery_observed',
              'landing_observed','pollen_transfer_observed'):
        if type(row[k]) is not bool and row[k] is not None:
            raise ValueError('NO_GO_UNCERTAIN_EVENT_NOT_NULL')
    # Downstream missingness must be explicit, not set to False because the
    # pollinator never discovered/landed on the source.
    if row['discovery_observed'] is False and (
        row['landing_observed'] is not None or row['pollen_transfer_observed'] is not None):
        raise ValueError('NO_GO_POST_DISCOVERY_EVENT_NOT_OBSERVED')
    if row['landing_observed'] is False and row['pollen_transfer_observed'] is not None:
        raise ValueError('NO_GO_POLLEN_DELIVERY_UNOBSERVABLE_AFTER_FAILED_LANDING')
    return {
        'status':'OBSERVATION_CONTRACT_VALID_NOT_CAUSAL',
        'plume_measured':row['plume_encounter_observed'] is not None,
        'flower_sway_measured':row['flower_sway_displacement_cm'] is not None,
        'all_events_directly_observed':all(row[k] is not None for k in (
            'plume_encounter_observed','discovery_observed',
            'landing_observed','pollen_transfer_observed')),
        'not_assuming_conditional_independence_of_outcomes':True
    }


if __name__=='__main__':
    import json
    def render(v):
        if isinstance(v,F):return str(v)
        if isinstance(v,dict):return {k:render(x) for k,x in v.items()}
        if isinstance(v,list):return [render(x) for x in v]
        return v
    here=Path(__file__).resolve().parent
    print(json.dumps(render({
      'scoping':inspect_wind_source_ledger(here/'WIND_DUAL_PATH_EVIDENCE_LEDGER.csv'),
      'example':wind_scenarios_source_free()}),indent=2,sort_keys=True))
