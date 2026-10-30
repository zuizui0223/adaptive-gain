"""Prospective Stage14 alternative 2x2x2 recency-refresh cue-order × wind allocation.

All records are synthetic design QA only. A real experiment must use a NEW
secret allocation seed in a separate concealed register after ethics/pilot.
"""
from __future__ import annotations
import hashlib,json,random
from collections import Counter,defaultdict
from itertools import product

ORDER=('reward_first','handling_first')
WIND=('calm','crosswind')
REFRESH=('informative','sham')
SIDES=('left','right')
WIND_SEQUENCES=(('calm','crosswind','crosswind','calm'),
                ('crosswind','calm','calm','crosswind'))
BLOCKS=4
TRIALS_PER_BLOCK=16
TRIALS_PER_BEE=64
QA_SEED=20261030
TIMING={'first_on':2.,'first_off':2.75,
        'second_on':3.50,'second_off':4.25,
        'refresh_on':5.00,'refresh_off':5.75,
        'gate':6.0,'window':30.0}
REFRESH_PAYLOAD={'informative':'reward_and_handling_simultaneous',
                 'sham':'nonpredictive_luminance_matched'}

def generate(n_colonies=24,bees_per_colony=12,seed=QA_SEED):
    if not (2<=n_colonies<=100 and 2<=bees_per_colony<=50 and bees_per_colony%2==0):
        raise ValueError('NO_GO_SYNTHETIC_COUNTERBALANCED_SAMPLE_SIZE')
    rng=random.Random(seed)
    rows=[]
    for ci in range(n_colonies):
        colony=f'QA_C{ci+1:03d}'
        for bi in range(bees_per_colony):
            bee=f'QA_B{bi+1:03d}'
            seq=WIND_SEQUENCES[(ci+bi)%2]
            for block_idx,wind in enumerate(seq,1):
                arms=[(o,r,s) for o,r,s in product(ORDER,REFRESH,SIDES) for _ in range(2)]
                rng.shuffle(arms)
                assert len(arms)==TRIALS_PER_BLOCK
                for k,(order,refresh,side) in enumerate(arms,1):
                    first,second=('reward','handling') if order=='reward_first' else ('handling','reward')
                    rows.append({
                        'trial_id':f'{colony}_{bee}_T{(block_idx-1)*TRIALS_PER_BLOCK+k:03d}',
                        'colony_id':colony,'bee_id':bee,
                        'block':block_idx,'trial_in_block':k,
                        'wind':wind,'order':order,'refresh':refresh,'reward_side':side,
                        'first_type':first,'second_type':second,
                        'refresh_payload':REFRESH_PAYLOAD[refresh],
                        'first_cue_on_s':TIMING['first_on'],
                        'first_cue_off_s':TIMING['first_off'],
                        'second_cue_on_s':TIMING['second_on'],
                        'second_cue_off_s':TIMING['second_off'],
                        'refresh_on_s':TIMING['refresh_on'],
                        'refresh_off_s':TIMING['refresh_off'],
                        'both_feeders_open_at_s':TIMING['gate'],
                        'measurement_window_s':TIMING['window'],
                        'predictive_cues_visible_at_gate':False})
    audit(rows,n_colonies,bees_per_colony)
    return rows

def audit(rows,expected_colonies=None,expected_bees_per_colony=None):
    if not rows:raise ValueError('NO_GO_EMPTY_SYNTHETIC_ALLOCATION')
    by_bee=defaultdict(list);by_colony=defaultdict(set);seen=set();arm_total=Counter()
    expected_arms={(w,o,r) for w,o,r in product(WIND,ORDER,REFRESH)}
    expected_block={(o,r,s) for o,r,s in product(ORDER,REFRESH,SIDES)}
    for row in rows:
        tid=row['trial_id']
        if tid in seen:raise ValueError('NO_GO_DUPLICATE_TRIAL_IDS')
        seen.add(tid)
        wind,order,refresh,side=(row[k] for k in ('wind','order','refresh','reward_side'))
        if wind not in WIND or order not in ORDER or refresh not in REFRESH or side not in SIDES:
            raise ValueError('NO_GO_INVALID_FACTOR')
        first,second=('reward','handling') if order=='reward_first' else ('handling','reward')
        if row['first_type']!=first or row['second_type']!=second:
            raise ValueError('NO_GO_CUE_ORDER')
        if row['refresh_payload']!=REFRESH_PAYLOAD[refresh]:
            raise ValueError('NO_GO_REFRESH_HARDWARE_PAYLOAD')
        for attr,source in (
          ('first_cue_on_s','first_on'),('first_cue_off_s','first_off'),
          ('second_cue_on_s','second_on'),('second_cue_off_s','second_off'),
          ('refresh_on_s','refresh_on'),('refresh_off_s','refresh_off')):
            if row[attr]!=TIMING[source]:raise ValueError('NO_GO_CUE_TIMING')
        if row['both_feeders_open_at_s']!=TIMING['gate'] or row['measurement_window_s']!=TIMING['window'] or row['predictive_cues_visible_at_gate'] is not False:
            raise ValueError('NO_GO_GATE_OR_VISUAL_INFORMATION_TIMING')
        key=(row['colony_id'],row['bee_id'])
        by_bee[key].append(row);by_colony[row['colony_id']].add(row['bee_id'])
        arm_total[(wind,order,refresh)]+=1
    if expected_colonies is not None and len(by_colony)!=expected_colonies:
        raise ValueError('NO_GO_WRONG_COLONY_COUNT')
    if expected_bees_per_colony is not None and any(len(v)!=expected_bees_per_colony for v in by_colony.values()):
        raise ValueError('NO_GO_WRONG_BEE_COUNT')
    for key,bee_rows in by_bee.items():
        if len(bee_rows)!=TRIALS_PER_BEE:raise ValueError('NO_GO_MISSING_BEE_TRIAL')
        block_map=defaultdict(list)
        for row in bee_rows:block_map[row['block']].append(row)
        if set(block_map)!={1,2,3,4}:raise ValueError('NO_GO_MISSING_BEE_BLOCK')
        actual_block_seq=[]
        for b in range(1,5):
            sub=block_map[b]
            if len(sub)!=TRIALS_PER_BLOCK or {r['trial_in_block'] for r in sub}!=set(range(1,17)):
                raise ValueError('NO_GO_INCOMPLETE_BEE_BLOCK')
            wind={r['wind'] for r in sub}
            if len(wind)!=1:raise ValueError('NO_GO_MIDBLOCK_WIND_SWITCH')
            actual_block_seq.append(next(iter(wind)))
            per_factor=Counter((r['order'],r['refresh'],r['reward_side']) for r in sub)
            if set(per_factor)!=expected_block or any(n!=2 for n in per_factor.values()):
                raise ValueError('NO_GO_REFRESH_SIDE_ORDER_BALANCE')
        if tuple(actual_block_seq) not in WIND_SEQUENCES:raise ValueError('NO_GO_BEE_WIND_SEQUENCE')
        per_arm=Counter((r['wind'],r['order'],r['refresh']) for r in bee_rows)
        if set(per_arm)!=expected_arms or any(n!=8 for n in per_arm.values()):
            raise ValueError('NO_GO_EIGHT_PER_BEE_CELL')
    return {
      'status':'SYNTHETIC_2x2x2_ALLOCATION_VERIFIED',
      'synthetic_QA_only':True,'actual_animal_assignments_must_be_private_and_new':True,
      'colony_count':len(by_colony),'bee_count':len(by_bee),'trials':len(rows),
      'trials_per_bee':64,'source_arms':8,
      'per_bee_trials_per_order_wind_refresh':8,
      'arm_totals':{'__'.join(k):v for k,v in sorted(arm_total.items())},
      'cue_clock':TIMING,'two_types_equal_initial_dose_s':.75,
      'both_types_last_exposure_time_matched_when_refresh_informative':True,
      'no_predictive_graphics_visible_at_release':True,'not_a_real_study':True}

def receipt(n_colonies=24,bees_per_colony=12):
    rows=generate(n_colonies,bees_per_colony)
    report=audit(rows,n_colonies,bees_per_colony)
    canonical=json.dumps(rows,sort_keys=True,separators=(',',':'))
    report['synthetic_QA_allocation_sha256']=hashlib.sha256(canonical.encode()).hexdigest()
    report['no_real_trial_IDs_published_or_observed']=True
    return report

if __name__=='__main__':
    import argparse
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('--out',default='bee_stage14_design_outputs')
    root=Path(p.parse_args().out);root.mkdir(parents=True,exist_ok=True)
    report=receipt()
    (root/'stage14_synthetic_allocation_receipt.json').write_text(json.dumps(report,indent=2))
    print('STAGE14_ALLOCATION_QA '+json.dumps(report),flush=True)