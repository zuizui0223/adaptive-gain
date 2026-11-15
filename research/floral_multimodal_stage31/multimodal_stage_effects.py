"""Stage31: quantitative contract for floral MULTIMODAL DECISION-STAGE synthesis.

All functions below are generic exact-contract calculators. There is NO
study-level meta-effect in this file. Positive effect = improvement in an
explicitly named event; handling-time effects are oriented toward saving
time only when that is the original endpoint and sampling grain permits.

One study can generate multiple dependent effects. These helpers do NOT fit
a meta-analysis or treat repeated encounters as independent replicates.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

STAGES=(
    'patch_detection',      # before seeing an individual flower
    'plant_approach',       # fly into plant/displays' vicinity
    'flower_choice',        # select a specific flower
    'landing',              # actual accepted landing and body alignment
    'within_flower_search', # proboscis entry, nectar location, movement
    'reward_assessment',    # intake and decision to stay/leave
    'pollen_transfer',      # male export, recipient deposit (separate outcomes)
    'plant_fitness'         # fertilization, fruit set, seed and siring
)
MODALITIES={
    'display_size', 'display_density', 'visible_color', 'uv_pattern',
    'nectar_guide_visible', 'nectar_guide_uv', 'scent_bouquet',
    'scent_intensity', 'scent_spatial_pattern', 'tactile_pattern',
    'floral_temperature', 'age_color_change'
}
STUDY_TYPES={
  'experimental','computational_model','review','observational',
  'meta_analysis','systematic_review_db','observational_primary_data',
  'database','computational_theory'
}
REQUIRED_SOURCE_FIELDS=(
    'source_id','year','study_type','modality','scale','stages',
    'raw_data_locator','source_url','extraction_status'
)


def validate_source_ledger(path):
    with Path(path).open(encoding='utf-8',newline='') as file:
        rd=csv.DictReader(file)
        if tuple(rd.fieldnames or ())!=REQUIRED_SOURCE_FIELDS:
            raise ValueError('NO_GO_EVIDENCE_LEDGER_FIELDS_CHANGED')
        rows=list(rd)
    if not rows or len({x['source_id'] for x in rows})!=len(rows):
        raise ValueError('NO_GO_NO_SOURCE_OR_DUPLICATE_SOURCE_IDS')
    for row in rows:
        if row['study_type'] not in STUDY_TYPES:
            raise ValueError('NO_GO_STUDY_TYPE_UNRECOGNIZED')
        if not row['source_url'].startswith('https://'):
            raise ValueError('NO_GO_SOURCE_WITHOUT_PERSISTENT_URL')
        if row['extraction_status'].strip()=='':
            raise ValueError('NO_GO_NO_EVIDENCE_STATE')
        if row['year'].isdigit() is False or not 1970<=int(row['year'])<=2026:
            raise ValueError('NO_GO_SOURCE_YEAR')
    return {'status':'SCOPING_LEDGER_VALIDATED_NOT_EFFECT_EXTRACTION',
            'total_source_rows':len(rows),
            'experimental_rows':sum(x['study_type']=='experimental' for x in rows),
            'existing_meta_rows':sum(x['study_type']=='meta_analysis' for x in rows),
            'independent_quantitative_effects_extracted':0,
            'duplicate_source_references_possible':True,
            'not_a_systematic_search':True}


def _int(name,val):
    if type(val) is not int or val<0:
        raise ValueError('NO_GO_NONCOUNT_'+name.upper())
    return val


def _binary(name, successes,trials):
    _int(name+'_successes',successes)
    _int(name+'_trials',trials)
    if trials<1 or successes>trials:
        raise ValueError('NO_GO_INVALID_BINARY_'+name.upper())


def log_odds_ratio(t_success,t_trials,c_success,c_trials):
    """Independent binary arms only. Zero cells trigger Haldane correction."""
    _binary('treated',t_success,t_trials)
    _binary('control',c_success,c_trials)
    a=float(t_success);b=float(t_trials-t_success)
    c=float(c_success);d=float(c_trials-c_success)
    corrected=any(x==0 for x in (a,b,c,d))
    if corrected:a,b,c,d=(x+0.5 for x in (a,b,c,d))
    y=math.log((a*d)/(b*c))
    v=1/a+1/b+1/c+1/d
    return {'effect_family':'log_odds_ratio',
            'estimate':y,'sampling_variance':v,
            'odds_ratio':math.exp(y),
            'continuity_correction_applied':corrected,
            'treated_successes':t_success,'treated_n':t_trials,
            'control_successes':c_success,'control_n':c_trials,
            'requires_independent_experimental_assignment':True,
            'not_valid_as_independent_if_same_bees_repeated':True}


def independent_time_log_ratio(t_n,t_mean,t_sd,c_n,c_mean,c_sd):
    """Positive handling/flight time; benefit is log(control/treatment)."""
    for nm,n in (('treated',t_n),('control',c_n)):
        if type(n) is not int or n<2:
            raise ValueError('NO_GO_TIME_N_'+nm.upper())
    for value in (t_mean,t_sd,c_mean,c_sd):
        if type(value) not in (int,float) or not math.isfinite(value):
            raise ValueError('NO_GO_TIME_NONFINITE')
    if t_mean<=0 or c_mean<=0 or t_sd<0 or c_sd<0:
        raise ValueError('NO_GO_TIME_INVALID_MOMENTS')
    benefit=math.log(c_mean/t_mean)
    variance=(t_sd*t_sd)/(t_n*t_mean*t_mean)+(c_sd*c_sd)/(c_n*c_mean*c_mean)
    return {'effect_family':'log_time_saved',
            'estimate':benefit,'sampling_variance':variance,
            'time_ratio_treat_over_control':t_mean/c_mean,
            'savings_if_positive':True,
            'independent_samples_only':True,
            'same_pollinators_need_paired_covariance':True}


def binary_factorial_interaction(cells):
    """Risk difference interaction in a 2x2 treatment design.

    Cells keyed 00, 10, 01, 11 are independent allocated GROUPS. If the
    same animal visits multiple arms, variance here is wrong; block such
    records until within-animal covariance can be recovered.
    """
    if set(cells)!={'00','10','01','11'}:
        raise ValueError('NO_GO_NOT_FULL_FACTORIAL_DESIGN')
    rates={}
    variance=0.
    for key,(y,n) in cells.items():
        _binary(key,y,n)
        p=y/n
        rates[key]=p
        variance+=p*(1-p)/n
    interaction=rates['11']-rates['10']-rates['01']+rates['00']
    return {'effect_family':'additive_interaction_risk_difference',
            'estimate':interaction,
            'sampling_variance':variance,
            'probabilities':rates,
            'requires_independent_arm_units':True,
            'NOT_same_as_positive_signal_summation':True,
            'NOT_meta_result':True}


def nested_stage_decomposition(treatment,control):
    """Conditioned success probabilities for identical stage sequences.

    Each arm must have an original denominator at discovery opportunity and
    nested numbers reaching successive stages. Identity telescopes:
    P(final event)=prod conditional stage-success probabilities.
    It does NOT estimate causality when assignment is observational.
    """
    if len(treatment)!=len(control) or len(treatment)!=len(STAGES)+1:
        raise ValueError('NO_GO_WRONG_NUMBER_OF_HIERARCHICAL_STAGES')
    for name,counts in (('treatment',treatment),('control',control)):
        for x in counts:_int(name,x)
        if counts[0]==0 or any(a<b for a,b in zip(counts,counts[1:])):
            raise ValueError('NO_GO_NONNESTED_STAGE_FLOW')
    per=[]
    for j,name in enumerate(STAGES):
        if treatment[j]==0 or control[j]==0:
            per.append({'stage':name,'stage_rate_t':None,'stage_rate_c':None,'log_ratio':None})
            continue
        pt=treatment[j+1]/treatment[j]
        pc=control[j+1]/control[j]
        per.append({'stage':name,'stage_rate_t':pt,'stage_rate_c':pc,
                    'log_ratio':math.log(pt/pc) if pt>0 and pc>0 else None})
    ptotal_t=treatment[-1]/treatment[0]
    ptotal_c=control[-1]/control[0]
    logtotal=math.log(ptotal_t/ptotal_c) if ptotal_t>0 and ptotal_c>0 else None
    if logtotal is not None:
        if not all(z['log_ratio'] is not None for z in per):
            raise ValueError('NO_GO_STAGE_DECOMPOSITION_BROKEN')
        if abs(sum(z['log_ratio'] for z in per)-logtotal)>1e-11:
            raise ValueError('NO_GO_STAGE_PRODUCT_IDENTITY')
    return {
      'stage_conditional_rates':per,
      'overall_treatment_success_rate':ptotal_t,
      'overall_control_success_rate':ptotal_c,
      'overall_log_success_ratio':logtotal,
      'exact_chain_rule_given_nested_events':True,
      'sampling_covariance_NOT_estimable_by_independent_stage_SE_sums':True,
      'selection_bias_possible_if_nonrandom_assignments':True
    }


def validate_macro_trait_state(rec):
    """Strict no-extrapolation gates: RGB has no UV or volatile chemistry."""
    needed=('taxon_id','source_id','source_url','population_id',
            'rgb_observed','uv_spectral_measured','voc_measured',
            'age_or_pollination_state_measured','guide_type')
    if any(k not in rec for k in needed):
        raise ValueError('NO_GO_MACRO_MISSING_SOURCE_FIELDS')
    if not rec['source_id'] or not rec['taxon_id'] or not rec['source_url'].startswith('https://'):
        raise ValueError('NO_GO_MACRO_UNVERIFIED_TRAIT_PROVENANCE')
    for key in ('rgb_observed','uv_spectral_measured',
                'voc_measured','age_or_pollination_state_measured'):
        if type(rec[key]) is not bool:
            raise ValueError('NO_GO_MACRO_MISSINGNESS_MUST_BE_EXPLICIT')
    if rec['guide_type'] not in ('none_measured','visible_measured','uv_measured','unknown'):
        raise ValueError('NO_GO_MACRO_GUIDE_STATE')
    if rec['guide_type']=='uv_measured' and not rec['uv_spectral_measured']:
        raise ValueError('NO_GO_RGB_INFERRED_FAKE_UV_GUIDE')
    return {'status':'MACRO_SOURCE_RECORD_ADMISSIBLE',
            'uv_unknown':not rec['uv_spectral_measured'],
            'voc_unknown':not rec['voc_measured'],
            'age_change_unknown':not rec['age_or_pollination_state_measured'],
            'do_not_require_complete_traits':True}


def empty_meta_evidence_gate():
    return {
      'status':'NO_GO_NO_SOURCE_EXTRACTED_TREATMENT_EFFECTS',
      'numbers_of_original_experimental_effects':0,
      'pre_existing_meta_and_review_data_not_counted_as_new_effects':True,
      'do_not_combine_dissimilar_binary_time_and_fitness_metrics':True,
      'floral_display_and_scent_are_not_locked_to_one_distance_class':True,
      'plant_reproduction_not_inferred_from_pollinator_visitation':True,
      'no_new_animal_or_plant_measurements':True,
    }


if __name__=='__main__':
    import json
    folder=Path(__file__).resolve().parent
    print(json.dumps({'ledger':validate_source_ledger(folder/'VERIFIED_SOURCE_GRANULARITY_LEDGER.csv'),
                      'effect_gate':empty_meta_evidence_gate()},indent=2))
