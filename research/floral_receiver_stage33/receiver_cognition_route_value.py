"""Stage33: cognition x stage x pollen-transfer analytical contracts.

NO REAL POLLINATOR PARAMETER ESTIMATES IN THIS MODULE. All numerical
examples are exact Fraction-valued thought experiments. A taxonomic group
is NOT mapped to cognitive ability, cue reliance or SVE automatically.

One can have good signal learning and low pollen delivery, or slower
learning and high delivery, without contradiction. Also, cue processing
can be costly to the receiver while beneficial to pollen transfer.
"""
from __future__ import annotations

import csv
from fractions import Fraction as F
from pathlib import Path

QUANTITIES=('encounter','cue_use','baseline_correct_route','cued_correct_route',
            'pollen_delivery_if_correct_route','pollen_delivery_if_wrong_route')
STAGE_TYPES=(
    'patch_detection','plant_approach','flower_choice','landing',
    'within_flower_search','reward_assessment','pollen_transfer','plant_fitness'
)
NO_COGNITION_RATE_STRINGS=('unknown','unmeasured','',None)


def _prob(name,value):
    if type(value) not in (int,F):
        raise ValueError('NO_GO_NONEXACT_UNVERIFIED_PARAMETER_'+name.upper())
    f=F(value)
    if not 0<=f<=1:
        raise ValueError('NO_GO_OUT_OF_RANGE_'+name.upper())
    return f


def _nonnegative(name,value):
    if type(value) not in (int,F):
        raise ValueError('NO_GO_NONEXACT_COST_'+name.upper())
    f=F(value)
    if f<0:
        raise ValueError('NO_GO_NEGATIVE_COST_'+name.upper())
    return f


def receiver_cue_value(*,encounter,cue_use,baseline_correct_route,
                       cued_correct_route,pollen_delivery_if_correct_route,
                       pollen_delivery_if_wrong_route=F(0),
                       processing_cost=F(0),reward_if_correct_route=F(1)):
    """Single signal use after encounter with externally supplied probabilities.

    cue_use is an experimentally measured/assumed frequency of executing a
    cue-dependent choice (not necessarily 'intelligence'). Difference of cue
    and no-cue correct-route probabilities is conditional on USING the cue.
    Positive plant delivery is not equivalent to positive receiver utility.
    """
    args=locals()
    x={k:_prob(k,args[k]) for k in QUANTITIES}
    cost=_nonnegative('processing_cost',processing_cost)
    reward=_nonnegative('reward_if_correct_route',reward_if_correct_route)
    before=x['baseline_correct_route']
    after=before+x['cue_use']*(x['cued_correct_route']-before)
    eta_good=x['pollen_delivery_if_correct_route']
    eta_bad=x['pollen_delivery_if_wrong_route']
    d0=eta_bad+(eta_good-eta_bad)*before
    d1=eta_bad+(eta_good-eta_bad)*after
    plant_delta=x['encounter']*(d1-d0)
    receiver_delta=x['encounter']*x['cue_use']*(
        (x['cued_correct_route']-before)*reward-cost)
    return {
      'before_route_success':before,'after_route_success':after,
      'per_encounter_plant_transfer_before':d0,
      'per_encounter_plant_transfer_after':d1,
      'plant_per_opportunity_transfer_delta':plant_delta,
      'receiver_per_opportunity_net_delta':receiver_delta,
      'route_reliability_delta':x['cued_correct_route']-before,
      'measured_animal_parameters_supplied':False,
      'not_a_real_ecological_estimate':True,
      'not_siring_or_seed_count':True
    }


def whole_route_decomposition(*,original_detection,signal_detection,
                              cue_use,baseline_correct_route,
                              cued_correct_route,pollen_delivery_if_correct_route,
                              pollen_delivery_if_wrong_route=F(0)):
    """Exact sequential decomposition: change in encounter + local cue use.

    The cross-term appears in the ordered local effect at new detection
    probability. It is conditional mechanics, NOT a fitted causal path.
    """
    original_detection=_prob('original_detection',original_detection)
    signal_detection=_prob('signal_detection',signal_detection)
    cue_use=_prob('cue_use',cue_use)
    baseline_correct_route=_prob('baseline_correct_route',baseline_correct_route)
    cued_correct_route=_prob('cued_correct_route',cued_correct_route)
    good=_prob('pollen_delivery_if_correct_route',pollen_delivery_if_correct_route)
    bad=_prob('pollen_delivery_if_wrong_route',pollen_delivery_if_wrong_route)
    b=bad+(good-bad)*baseline_correct_route
    conditional_change=cue_use*(cued_correct_route-baseline_correct_route)*(good-bad)
    remote_gain=(signal_detection-original_detection)*b
    local_gain=signal_detection*conditional_change
    exact_total=(signal_detection*(b+conditional_change)-original_detection*b)
    if remote_gain+local_gain!=exact_total:
        raise AssertionError('NO_GO_DECOMPOSITION_IDENTITY')
    return {
      'remote_detection_component':remote_gain,
      'post_detection_local_route_component':local_gain,
      'plant_transfer_total_change':exact_total,
      'decomposition_is_order_specific':True,
      'all_quantities_hypothetical':True
    }


def source_species_atlas(path):
    with Path(path).open(encoding='utf-8',newline='') as handle:
        r=csv.DictReader(handle)
        rows=list(r)
    expected={
       'Bombus ignitus','Osmia orientalis','Eristalis cerealis','Eristalis tenax',
       'Idea leuconoe','Argyreus hyperbius','Pieris rapae','Lycaena phlaeas'}
    if {x['taxon'] for x in rows}!=expected or len(rows)!=8:
        raise ValueError('NO_GO_UNVERIFIED_EIGHT_TAXON_COMPARISON')
    if len({x['taxon'] for x in rows})!=len(rows):
        raise ValueError('NO_GO_DUPLICATE_TAXON')
    for row in rows:
        if row['source_doi']!='10.1111/1440-1703.12249':
            raise ValueError('NO_GO_MISMATCHED_COMPARISON_SOURCE')
        if row['color_reward_learning_observed']!='yes':
            raise ValueError('NO_GO_FALSE_NO_LEARNING_TAXON')
        if row['rate_numeric_extracted']!='no' or row['raw_trial_count_verified']!='no':
            raise ValueError('NO_GO_INVENTED_LEARNING_NUMBERS')
        if row['nectar_guide_response_same_animals']!='no' or row['pollen_transfer_same_animals']!='no':
            raise ValueError('NO_GO_UNSOURCED_BEHAVIOR_TO_PLANT_FITNESS_JOIN')
    return {
        'status':'QUALITATIVE_COLOR_LEARNING_COMPARISON_ONLY',
        'eight_species':len(rows),
        'reported_learning_present_for_all_eight':True,
        'higher_rate_Bombus_ignitus_in_this_task':True,
        'slow_learning_is_not_random_behavior':True,
        'cross_task_efficiency_or_fitness_measured':False,
        'numeric_learning_rate_effects_extracted':0,
        'not_a_global_cognitive_ranking':True,
        'newly_observed_pollinators':0
    }


def compare_joint_evidence(evidence):
    """Strictly separate within-context cognition-plant data from cross-study.

    Only same original animal/plant/sample records can estimate a joint
    cognition -> route -> pollen-transfer pathway. Matched species names or
    guild names in two meta sources are NOT same observational subjects.
    """
    required={'learning_trial_source','cue_response_source','pollen_transfer_source',
              'original_animal_id_present','original_plant_id_present',
              'same_experiment_join_keys_verified',
              'repeated_measure_covariance_known',
              'independent_colony_or_plant_replication_verified'}
    if type(evidence) is not dict or set(evidence)!=required:
        raise ValueError('NO_GO_INCOMPLETE_JOINT_EVIDENCE_CONTRACT')
    for key in required:
        if key not in ('learning_trial_source','cue_response_source','pollen_transfer_source') and type(evidence[key]) is not bool:
            raise ValueError('NO_GO_UNVERIFIED_JOINT_FLAG')
    if not all(isinstance(evidence[k],str) and evidence[k] for k in
               ('learning_trial_source','cue_response_source','pollen_transfer_source')):
        return {'status':'NO_GO_SOURCE_IDS_MISSING','causal_mediation_allowed':False}
    if all(evidence[k] for k in (
          'original_animal_id_present','original_plant_id_present',
          'same_experiment_join_keys_verified','repeated_measure_covariance_known',
          'independent_colony_or_plant_replication_verified'
    )):
        return {
          'status':'STRUCTURAL_ORIGINAL_JOIN_ELIGIBLE_FOR_MODELING_ONLY',
          'causal_mediation_allowed':False,
          'why':'Identified source keys do not alone ensure unconfounded mediation; interventions or causal design still needed.'
        }
    return {'status':'NO_GO_CROSS_STUDY_COGNITION_TO_FITNESS_MEDIATION',
            'causal_mediation_allowed':False,
            'source_matching_by_taxon_or_guild_insufficient':True}


def original_design_context_audit(path):
    """Check reported Table 1 confounders; NEVER estimate cognition from them."""
    with Path(path).open(encoding='utf-8',newline='') as handle:
        rd=csv.DictReader(handle)
        rows=list(rd)
    taxa={x['taxon'] for x in rows}
    expected={'Bombus ignitus','Osmia orientalis','Eristalis cerealis',
              'Eristalis tenax','Idea leuconoe','Argyreus hyperbius',
              'Pieris rapae','Lycaena phlaeas'}
    if len(rows)!=8 or taxa!=expected:
        raise ValueError('NO_GO_ORIGINAL_DESIGN_TAXON_MISMATCH')
    flying_bee_or_fly={x for x in expected if x.startswith(
        ('Bombus','Osmia','Eristalis'))}
    butterflies=expected-flying_bee_or_fly
    for row in rows:
        if row['source_locator']!='https://doi.org/10.1111/1440-1703.12249':
            raise ValueError('NO_GO_INCORRECT_ORIGINAL_TABLE1_SOURCE')
        if row['design_is_identical_across_species']!='no':
            raise ValueError('NO_GO_UNSUPPORTED_UNIFORM_PROTOCOL')
        category='fly_or_bee' if row['taxon'] in flying_bee_or_fly else 'butterfly'
        expect_scent='yes' if category=='fly_or_bee' else 'no'
        expect_sugar='40' if category=='fly_or_bee' else '10'
        if row['honey_odor_near_array']!=expect_scent or row['sucrose_concentration_percent']!=expect_sugar:
            raise ValueError('NO_GO_DIFFERENT_EXPERIMENTAL_TREATMENT_SCOPE')
        if not row['arena_dimensions_m'] or not row['training_color_1'] or not row['training_color_2']:
            raise ValueError('NO_GO_UNRECORDED_ARENA_OR_COLOR')
    by_taxon={x['taxon']:x for x in rows}
    if by_taxon['Bombus ignitus']['original_colony_replication']!='one_bumblebee_colony_reported':
        raise ValueError('NO_GO_BOMBUS_ORIGINAL_COLONY_SCOPE')
    return {
      'status':'PUBLISHED_ORIGINAL_TABLE1_CONFONDERS_DOCUMENTED',
      'taxa_checked':8,
      'honey_odor_added_to_bees_and_hoverflies_only':True,
      'sucrose_bees_and_hoverflies_percent':40,
      'sucrose_butterflies_percent':10,
      'different_training_color_pairs_across_species':True,
      'different_flower_sizes_and_arenas_across_species':True,
      'Bombus_ignitus_one_colony_reported':True,
      'cannot_identify_order_or_sociality_effect_separately_from_these_design_factors_in_one_study':True,
      'no_new_phenotypic_or_learning_rate_effect':True
    }


def source_free_counterexamples():
    """Constructive counterexamples; NOT measurements from Bombus or hoverflies."""
    high_use=receiver_cue_value(
        encounter=F(1),cue_use=F(9,10),
        baseline_correct_route=F(11,20),cued_correct_route=F(19,20),
        pollen_delivery_if_correct_route=F(1,4))
    low_use=receiver_cue_value(
        encounter=F(1),cue_use=F(2,5),
        baseline_correct_route=F(1,2),cued_correct_route=F(4,5),
        pollen_delivery_if_correct_route=F(9,10))
    opposed=receiver_cue_value(
        encounter=F(1),cue_use=F(4,5),
        baseline_correct_route=F(1,2),cued_correct_route=F(4,5),
        pollen_delivery_if_correct_route=F(4,5),
        processing_cost=F(2,5),reward_if_correct_route=F(1))
    if high_use['plant_per_opportunity_transfer_delta']!=F(9,100):
        raise AssertionError('NO_GO_HIGH_USE_CONSTRUCTION')
    if low_use['plant_per_opportunity_transfer_delta']!=F(27,250):
        raise AssertionError('NO_GO_LOW_USE_CONSTRUCTION')
    if opposed['receiver_per_opportunity_net_delta']>=0 or opposed['plant_per_opportunity_transfer_delta']<=0:
        raise AssertionError('NO_GO_CONFLICT_COUNTEREXAMPLE')
    return {
        'high_cue_use_low_transfer_plant_gain':high_use['plant_per_opportunity_transfer_delta'],
        'lower_cue_use_high_transfer_plant_gain':low_use['plant_per_opportunity_transfer_delta'],
        'lower_cue_use_can_have_larger_plant_gain_in_this_constructed_world':True,
        'receiver_negative_plant_positive_counterexample':True,
        'all_parameters_assumed_source_free':True,
        'never_label_as_real_guild_performance':True
    }


if __name__=='__main__':
    import json
    path=Path(__file__).with_name('KANDORI_2021_EIGHT_TAXA_TASK_ATLAS.csv')
    def plain(v):
        if isinstance(v,F):return str(v)
        if isinstance(v,dict):return {k:plain(a) for k,a in v.items()}
        return v
    print(json.dumps(plain({'qualitative_evidence':source_species_atlas(path),
                           'original_table1_design':original_design_context_audit(Path(__file__).with_name('KANDORI_2021_PUBLISHED_DESIGN_CONTEXT_TABLE1.csv')),
                           'mathematical_examples':source_free_counterexamples()}),
                     indent=2,sort_keys=True))
