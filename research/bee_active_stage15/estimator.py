"""Mock-only Stage15 independent-colony equal ITT estimator.

The first biological primary, actual sucrose consumed in the same original
30 s from R reveal, requires a distinct real-study registration and sources.
"""
from collections import defaultdict
from statistics import mean,stdev
from math import sqrt
from scipy.stats import t as student_t

MODES=('contingent','precommit')
WINDS=('calm','crosswind')


def estimate(assignments,validated,synthetic_only=True):
    if synthetic_only is not True:
        raise ValueError('NO_GO_REAL_EXPERIMENT_NOT_APPROVED_OR_PREREGISTERED_HERE')
    if len(validated)!=len(assignments):
        raise ValueError('NO_GO_NOT_ALL_ASSIGNED_TRIALS_ANALYZED')
    byid={r['trial_id']:r for r in assignments}
    seen=set();cells=defaultdict(list)
    for x in validated:
        tid=x.get('trial_id')
        if tid not in byid or tid in seen:
            raise ValueError('NO_GO_INVALID_OR_DUPLICATE_SOURCE_OUTCOME')
        seen.add(tid)
        item=byid[tid]
        if x['access_mode']!=item['access_mode'] or x['assigned_wind']!=item['assigned_wind']:
            raise ValueError('NO_GO_ASSIGNED_ARM_CHANGED_AFTER_MEASUREMENT')
        if x.get('sensor_status') not in ('measured','verified_no_intake'):
            raise ValueError('NO_GO_SENSOR_FAILURE_IS_NOT_NO_DRINK')
        mass=x['verified_consumed_sucrose_mg']
        if type(mass) not in (float,int) or mass<0:
            raise ValueError('NO_GO_UNVERIFIED_REAL_CONSUMPTION')
        if x.get('final_target_choice')=='no_choice' and mass!=0:
            raise ValueError('NO_GO_NO_CHOICE_IS_NOT_POSITIVE_INTAKE')
        key=(item['colony_id'],item['bee_id'],item['assigned_wind'],item['access_mode'])
        correct=1 if x['final_target_choice']==item['correct_target'] else 0
        cells[key].append({'intake':mass,'leaf_requests':x['physical_leaf_reveals'],'correct':correct,
                           'choice':x['final_target_choice']})
    if seen!=set(byid):raise ValueError('NO_GO_MISSING_ALL_ASSIGNED_ANIMALS')
    bees=defaultdict(dict)
    for (col,bee,wind,mode),vals in cells.items():
        if len(vals)!=16:
            raise ValueError('NO_GO_NOT_16_ORIGINAL_TRIALS_PER_CELL')
        bees[col,bee][wind,mode]={k:mean(x[k] for x in vals)
                              for k in ('intake','leaf_requests','correct')}
    colony=defaultdict(list)
    for (col,bee),row in sorted(bees.items()):
        if set(row)!={(w,m) for w in WINDS for m in MODES}:
            raise ValueError('NO_GO_NOT_ALL_TRUE_BEE_ARMS')
        bywind={w:row[(w,'contingent')]['intake']-row[(w,'precommit')]['intake'] for w in WINDS}
        D=mean(bywind.values())
        Q=mean(row[(w,'precommit')]['leaf_requests']-row[(w,'contingent')]['leaf_requests'] for w in WINDS)
        colony[col].append({'bee':bee,'intake_diff':D,'query_saving':Q,
               'wind_interaction':bywind['crosswind']-bywind['calm']})
    results=[]
    for col,v in sorted(colony.items()):
        results.append({'colony':col,'n_bees':len(v),
                        'intake_advantage':mean(x['intake_diff'] for x in v),
                        'query_saving':mean(x['query_saving'] for x in v),
                        'wind_interaction':mean(x['wind_interaction'] for x in v)})
    c=len(results)
    primary=mean(x['intake_advantage'] for x in results)
    savings=mean(x['query_saving'] for x in results)
    accuracy={mode:mean([v['correct'] for (col,bee,w,m),row in cells.items()
                if m==mode for v in row]) for mode in MODES}
    out={
        'status':'SYNTHETIC_PILOT_ONLY_LT_12_COLONIES' if c<12 else 'SYNTHETIC_ESTIMATOR_QA_ONLY',
        'n_independent_colonies':c,
        'n_fake_bees':len(bees),
        'n_fake_trial_assignments':len(assignments),
        'primary_contingent_minus_precommit_sucrose_mg_per_fixed_30s':primary,
        'precommit_minus_contingent_leaf_requests':savings,
        'actual_correct_target_rate_by_arm':accuracy,
        'secondary_wind_interaction_in_sucrose_mg_per_fixed_30s':mean(x['wind_interaction'] for x in results),
        'all_trial_weights_colony_then_bee_equal':True,
        'NO_REAL_ANIMAL_OUTCOMES':True,
        'source_zero_intake_kept_as_zero':True,
        'all_original_assigned_trials_retained':True}
    if c>=12:
        vals=[x['intake_advantage'] for x in results]
        sd=stdev(vals)
        if sd<1e-12:
            out['status']='SYNTHETIC_DEGENERATE_COLONY_VARIANCE'
        else:
            se=sd/sqrt(c)
            t=primary/se;crit=float(student_t.ppf(.975,c-1))
            out.update({'synthetic_t_df_NOT_REAL':c-1,
                        'synthetic_two_sided_p_NOT_REAL':float(2*student_t.sf(abs(t),c-1)),
                        'synthetic_ci95_NOT_REAL':[primary-crit*se,primary+crit*se]})
    return out

if __name__=='__main__':
    import json
    from allocation import generate
    from telemetry import mock_telemetry,validate_traces
    a=generate(24,12)
    mock=mock_telemetry(a)
    qa,verified=validate_traces(a,mock,{'calm':(.05,.15),'crosswind':(.95,1.05)})
    if verified is None:raise RuntimeError('NO_GO_MOCK_PHYSICAL_GATE')
    result=estimate(a,verified)
    print('STAGE15_MOCK_COLONY_ESTIMATOR_QA '+json.dumps(result,sort_keys=True))
