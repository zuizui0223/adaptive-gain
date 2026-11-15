"""Stage27: matched-bee, source-verified estimand-contamination audit.

This is a reanalysis of an existing 2026 *Bombus terrestris* author CSV,
not a new experiment. The source was peer-produced; its Git blob is pinned
by the Stage26 checker before any statistic is calculated. Never call
Random_Free_Cue Info_Requested=1 a voluntary paid query: it marks cue access.

Primary estimand: the Easy->Impossible gradient in the strict Regular
PAID animal-initiated platform landing, contrasted with the nonsensical
pooled Info_Requested gradient across regular and automatic free-cue trials.

Bee IDs are cluster/bootstrap units. Colonies, unavailable in this CSV,
are NOT independently replicated by this procedure.
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
sys.path.insert(0,str(PREVIOUS))
from audit_author_request_semantics import (  # noqa: E402
    audit_csv_bytes, AUTHOR_REPO, AUTHOR_COMMIT, SOURCE_PATH, SOURCE_BLOB_SHA1
)

DIFF=('Easy','Hard','Impossible')
TYPE=('Regular','Random_Free_Cue')
UINT=2**32


class XorShift32:
    """Portable, prespecified bootstrap RNG; not cryptographic randomness."""
    def __init__(self,seed=20261115):
        if type(seed) is not int or not 0<seed<UINT:
            raise ValueError('NO_GO_INVALID_BOOTSTRAP_SEED')
        self.state=seed
    def index(self,n):
        if type(n) is not int or n<1:
            raise ValueError('NO_GO_INVALID_CLUSTER_COUNT')
        x=self.state
        x ^= (x<<13)&0xffffffff
        x ^= x>>17
        x ^= (x<<5)&0xffffffff
        self.state=x&0xffffffff
        return (self.state*n)>>32


def _quantile(values,prob):
    if not values:
        raise ValueError('NO_GO_EMPTY_BOOTSTRAP')
    a=sorted(values)
    loc=(len(a)-1)*prob
    i=int(math.floor(loc))
    frac=loc-i
    return (1-frac)*a[i]+frac*a[min(i+1,len(a)-1)]


def _new():
    return {'n':0,'flag':0,'landing':0}


def _aggregate(table):
    total_n=sum(v['n'] for v in table.values())
    if total_n==0:
        raise ValueError('NO_GO_NO_SOURCE_TRIALS')
    return {k:sum(v[k] for v in table.values()) for k in ('n','flag','landing')}


def _bees_and_groups(data):
    reader=csv.DictReader(io.StringIO(data.decode('utf-8-sig')))
    bee=defaultdict(lambda:defaultdict(_new))
    global_counts=defaultdict(_new)
    periods=defaultdict(_new)
    for row in reader:
        b=row['Bee_ID']
        d=row['Difficulty']
        typ=row['Trial_Type']
        if d not in DIFF or typ not in TYPE:
            raise ValueError('NO_GO_UNEXPECTED_DIFFICULTY_OR_TRIAL_TYPE')
        n=int(row['Trial_Number'])
        flag=int(row['Info_Requested'])
        landed=int(row['Actually_Landed_On_Platform'])
        period='Early' if n<=50 else 'Late'
        for t in (typ,'Pooled'):
            key=(d,t)
            for dst in (bee[b][key],global_counts[key],periods[(period,*key)]):
                dst['n']+=1
                dst['flag']+=flag
                dst['landing']+=landed
    return bee,global_counts,periods


def _rate(count,what):
    if count['n']==0:
        raise ValueError('NO_GO_MISSING_PER_BEE_DIFFICULTY_TREATMENT')
    return count[what]/count['n']


def _subject_effects(bee):
    records=[]
    for b in sorted(bee):
        m=bee[b]
        reg_grad=(_rate(m[('Impossible','Regular')],'landing')-
                  _rate(m[('Easy','Regular')],'landing'))
        naive_grad=(_rate(m[('Impossible','Pooled')],'flag')-
                    _rate(m[('Easy','Pooled')],'flag'))
        free_grad=(_rate(m[('Impossible','Random_Free_Cue')],'landing')-
                   _rate(m[('Easy','Random_Free_Cue')],'landing'))
        records.append({'bee':b,'regular_gradient':reg_grad,
                        'naive_pooled_flag_gradient':naive_grad,
                        'contamination_difference':reg_grad-naive_grad,
                        'landing_interaction':reg_grad-free_grad})
    if not records:
        raise ValueError('NO_GO_NO_ORIGINAL_BEES')
    return records


def _mean(xs):
    return sum(xs)/len(xs)


def _sd(xs):
    mu=_mean(xs)
    return math.sqrt(sum((x-mu)**2 for x in xs)/(len(xs)-1)) if len(xs)>1 else None


def _bee_summary(records):
    keys=('regular_gradient','naive_pooled_flag_gradient',
          'contamination_difference','landing_interaction')
    out={}
    for k in keys:
        arr=[r[k] for r in records]
        out[k]={'equal_bee_mean':_mean(arr),
                'bee_to_bee_sd':_sd(arr),
                'n_positive':sum(x>0 for x in arr),
                'n_negative':sum(x<0 for x in arr),
                'n_zero':sum(x==0 for x in arr)}
    return out


def _bootstrap(records,reps,seed):
    if type(reps) is not int or reps<1 or reps>100000:
        raise ValueError('NO_GO_UNSAFE_BOOTSTRAP_COUNT')
    rng=XorShift32(seed)
    keys=('regular_gradient','naive_pooled_flag_gradient',
          'contamination_difference','landing_interaction')
    values=[[r[k] for r in records] for k in keys]
    n=len(records)
    boot={k:[] for k in keys}
    boot['naive_over_regular_ratio']=[]
    for _ in range(reps):
        sums=[0.]*len(keys)
        for __ in range(n):
            j=rng.index(n)
            for v in range(len(keys)):
                sums[v]+=values[v][j]
        for v,key in enumerate(keys):
            boot[key].append(sums[v]/n)
        boot['naive_over_regular_ratio'].append(
            sums[1]/sums[0] if sums[0]>0 else float('nan'))
    intervals={}
    for key,vals in boot.items():
        if not all(math.isfinite(x) for x in vals):
            raise ValueError('NO_GO_BOOTSTRAP_NONFINITE_RATIO')
        intervals[key]=[_quantile(vals,.025),_quantile(vals,.975)]
    return {'unit':'Bee_ID not trial','n_original_bee_ids':n,
            'resamples':reps,'rng':'xorshift32','seed':seed,
            'percentile95':intervals,
            'bee_independence_unverified_due_to_missing_colony_ids':True,
            'not_colony_robust_confidence_intervals':True}


def _time_strata(periods):
    out={}
    for period in ('Early','Late'):
        rows={}
        for d in DIFF:
            r=periods[(period,d,'Regular')]
            p=periods[(period,d,'Pooled')]
            rows[d]={'regular':{'n':r['n'],'landing_rate':_rate(r,'landing')},
                     'pooled_flag':{'n':p['n'],'flag_rate':_rate(p,'flag')}}
        regular=rows['Impossible']['regular']['landing_rate']-rows['Easy']['regular']['landing_rate']
        naive=rows['Impossible']['pooled_flag']['flag_rate']-rows['Easy']['pooled_flag']['flag_rate']
        out[period]={'difficulty':rows,
                     'regular_gradient':regular,
                     'naive_pooled_flag_gradient':naive,
                     'contamination_difference':regular-naive}
    return out


def summarize(source,verify_source=True,reps=10000,seed=20261115):
    stage26=audit_csv_bytes(source,verify_source=verify_source)
    bee,counts,periods=_bees_and_groups(source)
    records=_subject_effects(bee)
    groups={}
    for d in DIFF:
        r=counts[(d,'Regular')]
        f=counts[(d,'Random_Free_Cue')]
        p=counts[(d,'Pooled')]
        groups[d]={
          'regular_paid':{'n':r['n'],'actual_requests':r['landing'],
                          'rate':_rate(r,'landing')},
          'random_free_cue':{'n':f['n'],'automatic_cue_flags':f['flag'],
                             'landing':f['landing'],
                             'landing_rate':_rate(f,'landing')},
          'naive_pooled_info_flag':{'n':p['n'],'flagged':p['flag'],
                                    'rate':_rate(p,'flag')}
        }
    regular=(groups['Impossible']['regular_paid']['rate']-
             groups['Easy']['regular_paid']['rate'])
    naive=(groups['Impossible']['naive_pooled_info_flag']['rate']-
           groups['Easy']['naive_pooled_info_flag']['rate'])
    reg_total=sum(groups[d]['regular_paid']['actual_requests'] for d in DIFF)
    flagged=sum(groups[d]['naive_pooled_info_flag']['flagged'] for d in DIFF)
    free_total=sum(groups[d]['random_free_cue']['automatic_cue_flags'] for d in DIFF)
    if flagged-reg_total!=free_total or any(
       groups[d]['random_free_cue']['automatic_cue_flags']!=
       groups[d]['random_free_cue']['n'] for d in DIFF
    ):
        raise ValueError('NO_GO_FREE_CUE_EXPOSURE_NOT_SEPARATED')
    result={
      'status':'PINNED_AUTHOR_SOURCE_ESTIMAND_CONTAMINATION_AUDITED'
               if verify_source else 'SOURCE_FREE_SYNTHETIC_QA_ONLY',
      'author_repository':AUTHOR_REPO,'author_commit':AUTHOR_COMMIT,
      'author_csv':SOURCE_PATH,'source_git_blob_sha1':SOURCE_BLOB_SHA1,
      'source_verified_in_this_run':verify_source,
      'n_trials':stage26['source_trial_rows'],
      'n_bee_ids':len(bee),
      'difficulty_source_counts':groups,
      'naively_counted_information_flags':flagged,
      'actual_paid_voluntary_request_landings_regular_only':reg_total,
      'automatic_free_cue_trials_in_naive_flag':free_total,
      'contaminated_fraction_of_naive_flags':free_total/flagged,
      'pooled_flag_is_not_paid_request':True,
      'trial_weighted':{
        'regular_paid_easy_to_impossible_gradient':regular,
        'naive_pooled_flag_easy_to_impossible_gradient':naive,
        'gradient_difference':regular-naive,
        'gradient_retained_fraction':naive/regular if regular else None,
        'gradient_relative_attenuation':(regular-naive)/regular if regular else None
      },
      'equal_bee_level':_bee_summary(records),
      'individual_bee_cluster_bootstrap':_bootstrap(records,reps,seed),
      'early_late_trial_number_robustness':_time_strata(periods),
      'leave_one_bee_out':{},
      'measurement_semantics':{
        'true_paid_animal_action':'Trial_Type==Regular AND Actually_Landed_On_Platform==1',
        'free_cue_info_flag':'automatic cue provision, NOT voluntary paid query',
        'free_cue_platform_landing':'observed landing, but NOT proof of paid information acquisition',
        'comparison_estimand':'difficulty gradient in different observables: legitimate regular paid request vs incorrect pooled information-exposure flag',
        'not_an_optimal_policy_payoff_comparison':True
      },
      'scientific_limits':{
        'original_animals_newly_collected':0,
        'original_colony_ids_in_public_source':False,
        'independent_colony_inference':False,
        'source_randomization_audited_from_assignment_log':False,
        'causal_effect_estimated':False,
        'stage24_8d_sensory_recognition_measured':False,
        'stage25_empirical_parameter_box_identified':False,
        'absolute_fitness_improvement_estimated':False,
        'all_data_existing_public_author_trials':True,
        'raw_csv_redistributed':False,
      }
    }
    for key in ('regular_gradient','naive_pooled_flag_gradient',
                'contamination_difference','landing_interaction'):
        arr=[r[key] for r in records]
        out=[(sum(arr)-x)/(len(arr)-1) for x in arr] if len(arr)>1 else []
        result['leave_one_bee_out'][key]={
           'min_equal_bee_mean':min(out) if out else None,
           'max_equal_bee_mean':max(out) if out else None}
    if verify_source:
        if len(bee)!=192 or stage26['source_trial_rows']!=19200 or (
           flagged,reg_total,free_total)!=(9526,5686,3840):
            raise ValueError('NO_GO_SOURCE_RECEIPT_CHANGED')
        if abs(regular-(2229/3112-591/6140))>1e-12 or abs(naive-(2957/3840-2131/7680))>1e-12:
            raise ValueError('NO_GO_MISMATCHED_SOURCE_GRADIENTS')
        if any(result['early_late_trial_number_robustness'][p]['contamination_difference']<=0
              for p in ('Early','Late')):
            raise ValueError('NO_GO_TRIAL_ORDER_SENSITIVITY_SIGN_REVERSED')
    return result


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--input',default=None)
    p.add_argument('--out',default='stage27_source_locked_receipts')
    p.add_argument('--bootstrap-reps',type=int,default=10000)
    a=p.parse_args(argv)
    if a.input is None:
        result={'status':'NO_GO_NO_PINNED_AUTHOR_SOURCE',
                'no_new_animals':True,'claim_limit':'CANNOT_COMPUTE_REAL_SOURCE_WITHOUT_EXACT_BYTES'}
    else:
        result=summarize(Path(a.input).read_bytes(),reps=a.bootstrap_reps)
    dest=Path(a.out);dest.mkdir(parents=True,exist_ok=True)
    (dest/'stage27_estimand_contamination.json').write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps({
       'status':result['status'],
       'source_rows':result.get('n_trials',0),
       'regular_paid_requests':result.get('actual_paid_voluntary_request_landings_regular_only',0),
       'pooled_info_flags':result.get('naively_counted_information_flags',0),
       'no_new_animals':True
    },sort_keys=True))


if __name__=='__main__':
    main()
