"""Stage14 synthetic QA for refresher-balanced order×wind colony-level contrasts.

This is not an analysis of real animals, even if synthetic p-values are
numerically small. A prospective real source/ethical gate remains required.
"""
from __future__ import annotations
from collections import defaultdict
from statistics import mean,stdev
import math,random
from scipy.stats import t as student_t
from allocation import WIND,ORDER,REFRESH,audit

STATUS={'measured','verified_no_intake'}
MIN_COLONIES_FOR_GENERAL_TEST=12

def estimate(assignments,outcomes):
    audit(assignments)
    if not isinstance(outcomes,list) or len(outcomes)!=len(assignments):
        raise ValueError('NO_GO_MISSING_ASSIGNED_OUTCOMES')
    schedule={row['trial_id']:row for row in assignments}
    measurement={}
    for source in outcomes:
        key=source.get('trial_id')
        if key in measurement or key not in schedule:
            raise ValueError('NO_GO_DUPLICATE_OR_UNKNOWN_TRIAL_OUTCOME')
        if source.get('sensor_status') not in STATUS:
            raise ValueError('NO_GO_SENSOR_FAILURE_IS_NOT_A_REAL_ZERO')
        if source.get('analysis_window_seconds')!=30.0:
            raise ValueError('NO_GO_WRONG_OUTCOME_WINDOW')
        mass=source.get('verified_consumed_sucrose_mg')
        if not isinstance(mass,(float,int)) or not math.isfinite(mass) or mass<0:
            raise ValueError('NO_GO_UNVERIFIED_OR_NEGATIVE_MASS')
        if source['sensor_status']=='verified_no_intake' and mass!=0.:
            raise ValueError('NO_GO_NO_INTAKE_NONZERO')
        measurement[key]=mass/30.0
    if set(measurement)!=set(schedule):raise ValueError('NO_GO_NOT_EVERY_ASSIGNED_TRIAL')
    per_bee=defaultdict(lambda:defaultdict(list))
    for row in assignments:
        key=(row['colony_id'],row['bee_id'])
        arm=(row['wind'],row['order'],row['refresh'])
        per_bee[key][arm].append(measurement[row['trial_id']])
    per_colony=defaultdict(list)
    for (colony,bee),cells in per_bee.items():
        if set(cells)!={(w,o,r) for w in WIND for o in ORDER for r in REFRESH} or any(len(x)!=8 for x in cells.values()):
            raise ValueError('NO_GO_ORIGINAL_BEE_8_FACTOR_CELLS')
        def cell(w,o,r):return mean(cells[(w,o,r)])
        def delta(r):
            return ((cell('crosswind','reward_first',r)-cell('crosswind','handling_first',r))
                    -(cell('calm','reward_first',r)-cell('calm','handling_first',r)))
        ref=delta('informative');sham=delta('sham')
        per_colony[colony].append({'bee':bee,'refreshed':ref,'sham':sham,'difference':ref-sham})
    colony_results=[]
    for colony,bees in sorted(per_colony.items()):
        colony_results.append({'colony':colony,'n_bees':len(bees),
          'refreshed':mean(x['refreshed'] for x in bees),
          'sham':mean(x['sham'] for x in bees),
          'difference':mean(x['difference'] for x in bees)})
    c=len(colony_results)
    actual=mean(x['refreshed'] for x in colony_results)
    report={'status':'PILOT_ONLY_FEWER_THAN_12_COLONIES' if c<MIN_COLONIES_FOR_GENERAL_TEST else 'SYNTHETIC_QA_DESIGN_ESTIMATOR',
        'only_synthetic_QA_not_animal_result':True,
        'independent_colonies':c,'individual_bees':len(per_bee),
        'assigned_trials':len(assignments),'includes_verified_zero_intake_trials':True,
        'primary_refreshed_order_x_wind_delta':actual,
        'secondary_sham_delta':mean(x['sham'] for x in colony_results),
        'secondary_refresh_difference':mean(x['difference'] for x in colony_results),
        'source_colony_DID_values':colony_results,
        'outcome_units':'verified consumed sucrose mg / 30s = mg/s',
        'primary_is_order_by_wind_only_given_simultaneous_final_informative_refresh':True,
        'factors_not_relabelled_real_cognitive_query_order':True,
        'randomization_and_intake_data_required_before_causal_claim':True}
    if c<MIN_COLONIES_FOR_GENERAL_TEST:
        report['no_population_p_value_due_to_low_colonies']=True
        return report
    vals=[x['refreshed'] for x in colony_results]
    sd=stdev(vals)
    if sd<=1e-12:
        report.update({'status':'NO_GO_ZERO_BETWEEN_COLONY_VARIANCE',
                       'no_population_p_value_due_to_degenerate_variance':True})
        return report
    se=sd/math.sqrt(c);tval=actual/se;crit=float(student_t.ppf(.975,c-1))
    report.update({'primary_t_df':c-1,'primary_t_stat':tval,
                   'primary_two_sided_p':float(2*student_t.sf(abs(tval),c-1)),
                   'primary_colony_se_mg_s':se,
                   'primary_student_t_CI95_mg_s':[actual-crit*se,actual+crit*se]})
    return report

def synthetic_outcomes(assignments,effect_refreshed=.018,effect_sham=-.004,
                       colony_heterogeneity=.003,noise_sd=.01,seed=20261031):
    """Mock outcomes only. No experimental biological values are fitted."""
    audit(assignments)
    colonies=sorted(set(x['colony_id'] for x in assignments))
    rng=random.Random(seed)
    cdelta={c:colony_heterogeneity*(i-(len(colonies)-1)/2)/max(1.,(len(colonies)-1)/2)
            for i,c in enumerate(colonies)}
    rows=[]
    for a in assignments:
        wind=int(a['wind']=='crosswind');rewardfirst=int(a['order']=='reward_first')
        ref=int(a['refresh']=='informative')
        d=(effect_refreshed+cdelta[a['colony_id']]) if ref else (effect_sham+cdelta[a['colony_id']]/2)
        y=.30+.006*rewardfirst-.025*wind+.007*ref+d*wind*rewardfirst
        y+=rng.gauss(0,noise_sd)
        y=max(0.,y)  # QA MOCK ONLY. Not a scientifically calibrated power simulation.
        rows.append({'trial_id':a['trial_id'],'sensor_status':'measured',
                     'analysis_window_seconds':30.0,
                     'verified_consumed_sucrose_mg':y*30.0})
    return rows

if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    from allocation import generate
    p=argparse.ArgumentParser();p.add_argument('--out',default='bee_stage14_design_outputs')
    root=Path(p.parse_args().out);root.mkdir(parents=True,exist_ok=True)
    a=generate(24,12)
    o=synthetic_outcomes(a,noise_sd=0.0)
    report=estimate(a,o)
    if report['status']!='SYNTHETIC_QA_DESIGN_ESTIMATOR':
        raise ValueError('NO_GO_SYNTHETIC_ESTIMATOR_NOT_VALIDATED')
    release={k:v for k,v in report.items() if k!='source_colony_DID_values'}
    release['source_colony_DID_values_NOT_REAL']=True
    release['assumed_injected_effects_mg_s']={'refreshed':.018,'sham':-.004}
    (root/'stage14_synthetic_colony_estimator_receipt.json').write_text(json.dumps(release,indent=2))
    print('STAGE14_SYNTHETIC_ESTIMATOR_QA '+json.dumps(release),flush=True)