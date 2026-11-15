"""Stage28: published bee-cue outcome source QA and conditional payoff sensitivity.

Existing PUBLIC author data only; NO newly observed bees.
The trial table has no target-side randomization key or final selected side,
so the unexpectedly low "Impossible, Regular, no cue" correctness cannot be
interpreted as animal maladaptation or an estimate of 8-world source value.

Payoff formula is an ANALYTICAL PROXY: 5 uL 15% versus 5 uL 30% sucrose
gives 1/2 relative concentration for correct responses. No negative quinine
utility, reward-satiety dynamics, fitness mapping or source request causal
effect is identified. We display the unknown disutility penalty K explicitly.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

PREVIOUS=Path(__file__).resolve().parents[1] / 'bee_original_audit_stage26'
STAGE27=Path(__file__).resolve().parents[1] / 'bee_estimand_stage27'
sys.path.insert(0,str(PREVIOUS))
sys.path.insert(0,str(STAGE27))
from audit_author_request_semantics import (  # noqa: E402
    audit_csv_bytes, AUTHOR_REPO, AUTHOR_COMMIT, SOURCE_PATH, SOURCE_BLOB_SHA1,
)
from estimand_contamination import XorShift32, _quantile  # noqa: E402

DIFFICULTY=('Easy','Hard','Impossible')
OUTCOMES=('Regular_No_Cue','Regular_Paid_Cue',
          'Free_Cue_No_Landing','Free_Cue_Landing')
IMP_NOCUE=('Impossible','Regular_No_Cue')
IMP_FREENOLAND=('Impossible','Free_Cue_No_Landing')


def _blank():
    return {'n':0,'correct':0}


def _classify(row):
    typ=row['Trial_Type']
    landing=row['Actually_Landed_On_Platform']
    request=row['Info_Requested']
    if typ=='Regular':
        if landing!=request:
            raise ValueError('NO_GO_REGULAR_SELF_REQUEST_INCONSISTENT')
        return 'Regular_Paid_Cue' if landing=='1' else 'Regular_No_Cue'
    if typ=='Random_Free_Cue':
        if request!='1':
            raise ValueError('NO_GO_AUTOMATIC_EXPOSURE_FLAG_MISSING')
        return 'Free_Cue_Landing' if landing=='1' else 'Free_Cue_No_Landing'
    raise ValueError('NO_GO_INVALID_TREATMENT')


def _correct(row):
    flag=row['Info_Requested']
    field='Is_Post_Request_Correct' if flag=='1' else 'Is_Post_Non_Request_Correct'
    v=row[field]
    if v not in ('0','1','0.0','1.0'):
        raise ValueError('NO_GO_MISSING_OR_INVALID_CORRECTNESS')
    return int(float(v))


def _outcomes(data):
    reader=csv.DictReader(io.StringIO(data.decode('utf-8-sig')))
    names=set(reader.fieldnames or ())
    missing_randomization=('Correct_Target_Side','Chosen_Target_Side','Colony_ID')
    if any(x in names for x in missing_randomization):
        raise ValueError('NO_GO_UNEXPECTED_SOURCE_SCHEMA_REVISION')
    bees=defaultdict(lambda:defaultdict(_blank))
    count=defaultdict(_blank)
    time=defaultdict(_blank)
    for row in reader:
        d=row['Difficulty']
        if d not in DIFFICULTY:
            raise ValueError('NO_GO_UNKNOWN_DIFFICULTY')
        cat=_classify(row)
        y=_correct(row)
        bee=row['Bee_ID']
        try:
            trial_number=int(row['Trial_Number'])
        except ValueError as exc:
            raise ValueError('NO_GO_INVALID_TRIAL_NUMBER') from exc
        phase='Early' if trial_number<=50 else 'Late'
        for cell in (bees[bee][(d,cat)], count[(d,cat)],time[(phase,d,cat)]):
            cell['n']+=1
            cell['correct']+=y
    return bees,count,time


def _prob(cell):
    if cell['n']<1:
        raise ValueError('NO_GO_EMPTY_REQUIRED_STRATUM')
    return cell['correct']/cell['n']


def _source_classes(count):
    output={}
    for d in DIFFICULTY:
        output[d]={}
        for cat in OUTCOMES:
            o=count[(d,cat)]
            if not o['n']:
                raise ValueError('NO_GO_MISSING_PUBLIC_OUTCOME_CLASS')
            output[d][cat]={
                'trials':o['n'],'correct':o['correct'],
                'accuracy':_prob(o),
            }
    return output


def _per_bee_nocue(bees):
    out=[]
    for bee, info in sorted(bees.items()):
        cell=info.get(IMP_NOCUE)
        if not cell or cell['n']<1:
            raise ValueError('NO_GO_BEE_WITHOUT_IMPOSSIBLE_NO_CUE')
        out.append({'bee':bee,'no_cue_impossible_n':cell['n'],
                    'no_cue_impossible_accuracy':_prob(cell)})
    return {
        'n_bees':len(out),
        'n_below_50pct':sum(x['no_cue_impossible_accuracy']<0.5 for x in out),
        'n_equal_50pct':sum(x['no_cue_impossible_accuracy']==0.5 for x in out),
        'n_above_50pct':sum(x['no_cue_impossible_accuracy']>0.5 for x in out),
        'equal_bee_mean_accuracy':sum(x['no_cue_impossible_accuracy'] for x in out)/len(out),
        'n_bee_trials_min':min(x['no_cue_impossible_n'] for x in out),
        'n_bee_trials_max':max(x['no_cue_impossible_n'] for x in out),
        'requires_target_side_and_choice_side_to_test_chance_null':True,
    }


def _bootstrap(bees,reps,seed):
    if type(reps) is not int or not 1<=reps<=100000:
        raise ValueError('NO_GO_INVALID_BOOTSTRAP_REPS')
    if not bees:
        raise ValueError('NO_GO_NO_BEES')
    bs=[bees[k] for k in sorted(bees)]
    rng=XorShift32(seed)
    wanted=[IMP_NOCUE,IMP_FREENOLAND,
            ('Hard','Regular_No_Cue'),('Hard','Regular_Paid_Cue'),
            ('Impossible','Regular_Paid_Cue')]
    sample={k:[] for k in wanted}
    sample['difference_free_without_landing_minus_regular_no_cue']=[]
    for _ in range(reps):
        totals={k:[0,0] for k in wanted}
        for j in range(len(bs)):
            person=bs[rng.index(len(bs))]
            for k in wanted:
                obs=person.get(k)
                if obs:
                    totals[k][0]+=obs['n']
                    totals[k][1]+=obs['correct']
        rates={}
        for k in wanted:
            if totals[k][0]==0:
                raise ValueError('NO_GO_BOOTSTRAP_EMPTY_SOURCE_CLASS')
            rates[k]=totals[k][1]/totals[k][0]
            sample[k].append(rates[k])
        sample['difference_free_without_landing_minus_regular_no_cue'].append(
            rates[IMP_FREENOLAND]-rates[IMP_NOCUE])
    return {
        'sampling_unit':'Bee_ID (not independent colony)',
        'repetitions':reps,'seed':seed,
        'percentile95':{
          (f'{key[0]}|{key[1]}' if isinstance(key,tuple) else key):
          [_quantile(v,.025),_quantile(v,.975)]
          for key,v in sample.items()
        },
        'independent_colony_variance_unavailable':True,
        'not_95pct_colony_population_inference':True
    }


def _reward_sensitivity(group):
    out={}
    for d in DIFFICULTY:
        p_paid=group[d]['Regular_Paid_Cue']['accuracy']
        p_nocue=group[d]['Regular_No_Cue']['accuracy']
        # For an observed stratum, relative correct reward mass is 0.5 vs 1.
        # A wrong choice receives an unknown negative quinine penalty K.
        # Difference = (0.5*P_paid - P_no) + K*(P_paid - P_no).
        base=0.5*p_paid-p_nocue
        slope=p_paid-p_nocue
        threshold=-base/slope if slope>0 else None
        out[d]={
            'paid_correct_probability':p_paid,'no_cue_correct_probability':p_nocue,
            'correct_reward_proxy_paid_at_K0':0.5*p_paid,
            'correct_reward_proxy_no_cue_at_K0':p_nocue,
            'paid_minus_no_cue_correct_reward_proxy_at_K0':base,
            'unknown_wrong_choice_penalty_slope':slope,
            'conditional_break_even_K':threshold,
            'positive_K_needed_for_paid_proxy_preference':
              max(threshold,0) if threshold is not None else None,
            'CAUTION':'Observational action-stratum difference, not causal counterfactual; sucrose concentration ratio is not physiological fitness utility.'
        }
    p_paid=group['Impossible']['Regular_Paid_Cue']['accuracy']
    imagined_no_cue_chance=0.5
    base=0.5*p_paid-imagined_no_cue_chance
    slope=p_paid-imagined_no_cue_chance
    out['Impossible_if_unobserved_no_cue_chance_is_0point5']={
      'NOT_OBSERVED_COUNTERFACTUAL':True,
      'hypothetical_no_cue_accuracy':imagined_no_cue_chance,
      'paid_accuracy_taken_from_selected_source':p_paid,
      'paid_minus_no_cue_correct_reward_proxy_K0':base,
      'conditional_break_even_K':-base/slope if slope>0 else None,
    }
    return out


def analyze_csv(source,verify_source=True,reps=10000,seed=20261115):
    prev=audit_csv_bytes(source,verify_source=verify_source)
    bees,counts,times=_outcomes(source)
    group=_source_classes(counts)
    per_bee=_per_bee_nocue(bees)
    time={}
    for phase in ('Early','Late'):
        time[phase]={}
        for key in (IMP_NOCUE,IMP_FREENOLAND):
            o=times[(phase,*key)]
            time[phase]['|'.join(key)]={'trials':o['n'],
                                         'correct':o['correct'],'accuracy':_prob(o)}
    boot=_bootstrap(bees,reps,seed)
    reward=_reward_sensitivity(group)
    r={
      'status':'PINNED_AUTHOR_SOURCE_OUTCOME_AND_NEGATIVE_CONTROL_AUDIT'
                if verify_source else 'FAKE_SOURCE_FREE_TEST_ONLY',
      'author_repository':AUTHOR_REPO,'author_commit':AUTHOR_COMMIT,
      'source_path':SOURCE_PATH,'git_blob_sha1':SOURCE_BLOB_SHA1,
      'n_author_trial_rows':prev['source_trial_rows'],
      'n_unique_bee_ids':len(bees),
      'source_specific_accuracy':group,
      'impossible_no_cue_negative_control':{
         'trials':group['Impossible']['Regular_No_Cue']['trials'],
         'correct':group['Impossible']['Regular_No_Cue']['correct'],
         'accuracy':group['Impossible']['Regular_No_Cue']['accuracy'],
         'proposed_ideal_random_side_chance_accuracy':0.5,
         'status':'SOURCE_SIDE_RANDOMIZATION_UNIDENTIFIABLE',
         'hard_stop_on_biological_below_chance_inference':True,
         'original_target_side_not_in_csv':True,
         'original_choice_side_not_in_csv':True,
         'pre_trial_target_side_randomization_log_missing':True,
         'no_p_value_or_independent_colony_test_claimed':True
      },
      'per_bee_negative_control':per_bee,
      'bee_unit_bootstrap':boot,
      'early_late_source_check':time,
      'hypothetical_reward_proxy_not_fitness':reward,
      'required_next_source':'Trial-level correct target side, actual final choice side, prior/cue timing and source randomization log',
      'real_animal_new_collection':0,
      'anomalous_rate_reason_unidentified':True,
      'no_causal_paid_query_reward_gain_claim':True,
      'stage24_8world_model_empirically_validated':False,
      'raw_author_trial_data_not_redistributed':True
    }
    if verify_source:
        if r['n_author_trial_rows']!=19200 or r['n_unique_bee_ids']!=192:
            raise ValueError('NO_GO_PUBLIC_SOURCE_CARDINALITY')
        if (group['Impossible']['Regular_No_Cue']['correct'],
            group['Impossible']['Regular_No_Cue']['trials'])!=(183,883):
            raise ValueError('NO_GO_IMPOSSIBLE_UNCUED_SOURCE_RESULT_CHANGED')
        if (group['Impossible']['Free_Cue_No_Landing']['correct'],
            group['Impossible']['Free_Cue_No_Landing']['trials'])!=(532,575):
            raise ValueError('NO_GO_FREE_NO_LANDING_SOURCE_RESULT_CHANGED')
        if per_bee['n_below_50pct']!=170:
            raise ValueError('NO_GO_NEGATIVE_CONTROL_BEE_COUNT_CHANGED')
        if not (0.1 < reward['Impossible']['paid_minus_no_cue_correct_reward_proxy_at_K0'] <0.3):
            raise ValueError('NO_GO_PAYOFF_PROXY_CONSTRUCTION_CHANGED')
        for phase in ('Early','Late'):
            if time[phase]['Impossible|Regular_No_Cue']['accuracy']>=0.5:
                raise ValueError('NO_GO_TIME_STRATUM_CHANCE_ANOMALY_REVERSED')
    return r


def main(argv=None):
    a=argparse.ArgumentParser()
    a.add_argument('--input')
    a.add_argument('--out',default='stage28_source_outcome_receipt')
    a.add_argument('--bootstrap-reps',type=int,default=10000)
    opts=a.parse_args(argv)
    if opts.input is None:
        result={'status':'NO_GO_NO_PINNED_AUTHOR_SOURCE','new_bees':0,
                'no_biological_inference':True}
    else:
        result=analyze_csv(Path(opts.input).read_bytes(),reps=opts.bootstrap_reps)
    d=Path(opts.out);d.mkdir(parents=True,exist_ok=True)
    (d/'stage28_chance_baseline_outcomes.json').write_text(
      json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',
      encoding='utf-8')
    print(json.dumps({
        'status':result['status'],
        'rows':result.get('n_author_trial_rows',0),
        'bees':result.get('n_unique_bee_ids',0),
        'no_biological_inference':True
    },sort_keys=True))


if __name__=='__main__':
    main()
