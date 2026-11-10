"""Prospective SYNTHETIC 2x2 outcome-contingent query × wind assignment.

All bits are hidden from future actual bees until source cue display.
This public QA seed MUST NOT be used to randomize an actual experiment.
"""
from __future__ import annotations
import hashlib,json,random
from collections import Counter, defaultdict
from itertools import product

MODES=('contingent','precommit')
WINDS=('calm','crosswind')
WORLDS=tuple(product((0,1),repeat=3))
WIND_SEQUENCES=(('calm','crosswind','crosswind','calm'),
                ('crosswind','calm','calm','crosswind'))
PUBLIC_QA_SEED=20261111
TRIALS_PER_BLOCK=16
TRIALS_PER_BEE=64


def generate(n_colonies=24,bees_per_colony=12,seed=PUBLIC_QA_SEED):
    if (type(n_colonies) is not int or type(bees_per_colony) is not int or
        not 2<=n_colonies<=200 or not 2<=bees_per_colony<=100 or bees_per_colony%2):
        raise ValueError('NO_GO_SYNTHETIC_COLONIES_OR_BEES_UNBALANCED')
    rng=random.Random(seed)
    rows=[]
    for c in range(n_colonies):
        colony=f'QA_C{c+1:03d}'
        for b in range(bees_per_colony):
            bee=f'QA_B{b+1:03d}'
            sequence=WIND_SEQUENCES[(c+b)%2]
            for block,wind in enumerate(sequence,1):
                design=[(mode,r,u,v) for mode in MODES for (r,u,v) in WORLDS]
                rng.shuffle(design)
                for t,(mode,r,u,v) in enumerate(design,1):
                    rows.append({
                        'trial_id':f'{colony}_{bee}_T{(block-1)*16+t:03d}',
                        'colony_id':colony,'bee_id':bee,
                        'block':block,'trial_in_block':t,
                        'access_mode':mode,'assigned_wind':wind,
                        'r':r,'u':u,'v':v,
                        'correct_target':u if r==0 else v,
                        'world_concealed_from_subject':True,
                        'study_design_is_synthetic_QA_only':True})
    audit(rows,expected_colonies=n_colonies,expected_bees=bees_per_colony)
    return rows


def audit_world_balance(trials):
    target={(m,r,u,v) for m in MODES for (r,u,v) in WORLDS}
    actual=Counter((x['access_mode'],x['r'],x['u'],x['v']) for x in trials)
    if set(actual)!=target or any(n!=1 for n in actual.values()):
        raise ValueError('NO_GO_WORLD_BALANCE_WITHIN_WIND_BLOCK')
    return True


def audit(rows,expected_colonies=None,expected_bees=None):
    if not rows:raise ValueError('NO_GO_EMPTY_ALLOCATION')
    ids=[r['trial_id'] for r in rows]
    if len(set(ids))!=len(ids):raise ValueError('NO_GO_DUPLICATE_TRIAL_ID')
    bybee=defaultdict(list);bycol=defaultdict(set);bycell=Counter()
    for x in rows:
        mode=x['access_mode'];wind=x['assigned_wind']
        if mode not in MODES or wind not in WINDS:
            raise ValueError('NO_GO_INVALID_ASSIGNMENT_MODE')
        if (x['r'],x['u'],x['v']) not in WORLDS:
            raise ValueError('NO_GO_INVALID_STATE_BITS')
        if x['correct_target']!=(x['u'] if x['r']==0 else x['v']):
            raise ValueError('NO_GO_PREDEFINED_TARGET_MISMATCH')
        if x.get('world_concealed_from_subject') is not True or x.get('study_design_is_synthetic_QA_only') is not True:
            raise ValueError('NO_GO_PUBLIC_SOURCE_ALLOCATION_RELABELED_REAL')
        key=(x['colony_id'],x['bee_id'])
        bybee[key].append(x);bycol[x['colony_id']].add(x['bee_id']);bycell[(wind,mode)]+=1
    if expected_colonies is not None and len(bycol)!=expected_colonies:
        raise ValueError('NO_GO_COLONY_COUNT_CHANGED')
    if expected_bees is not None and any(len(v)!=expected_bees for v in bycol.values()):
        raise ValueError('NO_GO_BEE_COUNT_CHANGED')
    for colony,bees in bycol.items():
        sequences=Counter()
        for bee in bees:
            trials=bybee[(colony,bee)]
            if len(trials)!=TRIALS_PER_BEE:raise ValueError('NO_GO_NOT_64_TRIALS_PER_BEE')
            byblock=defaultdict(list)
            for a in trials:byblock[a['block']].append(a)
            if set(byblock)!={1,2,3,4}:raise ValueError('NO_GO_FOUR_SOURCE_BLOCKS')
            winds=[]
            for block in range(1,5):
                vals=byblock[block]
                if len(vals)!=16 or {a['trial_in_block'] for a in vals}!=set(range(1,17)):
                    raise ValueError('NO_GO_INCOMPLETE_WIND_BLOCK')
                ws={a['assigned_wind'] for a in vals}
                if len(ws)!=1:raise ValueError('NO_GO_WIND_SWITCHED_INSIDE_BLOCK')
                winds.append(next(iter(ws)))
                audit_world_balance(vals)
            if tuple(winds) not in WIND_SEQUENCES:
                raise ValueError('NO_GO_NOT_COUNTERBALANCED_BLOCKS')
            sequences[tuple(winds)]+=1
            for mode in MODES:
                for wind in WINDS:
                    vals=[a for a in trials if a['access_mode']==mode and a['assigned_wind']==wind]
                    counts=Counter((a['r'],a['u'],a['v']) for a in vals)
                    if set(counts)!=set(WORLDS) or any(v!=2 for v in counts.values()):
                        raise ValueError('NO_GO_WORLD_2_EACH_PER_BEE_CELL')
        if set(sequences)!=set(WIND_SEQUENCES) or abs(sequences[WIND_SEQUENCES[0]]-sequences[WIND_SEQUENCES[1]])>1:
            raise ValueError('NO_GO_WITHIN_COLONY_WIND_BLOCK_SEQUENCE_BIAS')
    return {
       'status':'SYNTHETIC_2x2_CONTINGENT_QUERY_WIND_ALLOCATION_VERIFIED',
       'n_trials':len(rows),'n_bees':len(bybee),'n_independent_colonies':len(bycol),
       'cell_counts':{'__'.join(k):v for k,v in sorted(bycell.items())},
       'trials_per_bee':TRIALS_PER_BEE,'eight_worlds_twice_in_every_bee_arm':True,
       'real_animal_assignments_generated':False,
       'all_world_bits_are_source_only_concealed_until_cue':True}


def receipt():
    rows=generate()
    r=audit(rows)
    b=json.dumps(rows,sort_keys=True,separators=(',',':')).encode('utf-8')
    r['public_only_synthetic_schedule_digest']=hashlib.sha256(b).hexdigest()
    r['do_not_reuse_this_seed_for_animal_recruitment']=True
    return r

if __name__=='__main__':
    import argparse
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('--out',default='stage15_design_outputs')
    root=Path(p.parse_args().out);root.mkdir(parents=True,exist_ok=True)
    r=receipt();(root/'allocation_receipt.json').write_text(json.dumps(r,indent=2))
    print('STAGE15_SYNTHETIC_BALANCED_ALLOCATION '+json.dumps(r,sort_keys=True))
