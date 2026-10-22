"""From original CSV, independently reconstruct beta=route composition/within speed.

No import or calls to production calculation routines. The original analytic
study is the observation of bees, never independent film-row inference.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np
import pandas as pd

SHA='2361dccb523b97f1e5e542fc492d302a5e7c290cdde72eb2dfb2ce021153d6f7'


def original(path):
    body=Path(path).read_bytes()
    assert hashlib.sha256(body).hexdigest()==SHA
    d=pd.read_csv(path)
    assert len(d)==548 and d['Bee ID'].nunique()==58
    d['route']=np.where(d['Median altitude (mm)']>d['Canopy height (mm)'],1,0)
    return d


def independent_height(d,h,direction=None,exclude_bee=None):
    tab=d.loc[d['Canopy height (mm)']==h]
    if direction is not None:tab=tab.loc[tab['Flight Direction Label']==direction]
    if exclude_bee is not None:tab=tab.loc[tab['Bee ID']!=exclude_bee]
    ids=[]
    for bid in sorted(tab['Bee ID'].unique()):
        sub=tab.loc[tab['Bee ID']==bid]
        if set(sub['Wind Presence'].unique())=={'No','Yes'}:
            ids.append(bid)
    if not ids:raise ValueError('no paired bees')
    t=tab[tab['Bee ID'].isin(ids)]
    p={};v={};mu={}
    for w in ('No','Yes'):
        subset=t.loc[t['Wind Presence']==w]
        den={bid:len(subset.loc[subset['Bee ID']==bid]) for bid in ids}
        numerator={route:0. for route in (0,1)}
        weighted_speed={route:0. for route in (0,1)}
        for _,row in subset.iterrows():
            bid=row['Bee ID']; r=row['route']
            weight=1/(len(ids)*den[bid])
            numerator[r]+=weight
            weighted_speed[r]+=weight*row['Median ground speed (m/s)']
        if min(numerator.values())<=0:raise ValueError('empty observed route cell')
        p[w]=numerator
        v[w]={r:weighted_speed[r]/numerator[r] for r in (0,1)}
        mu[w]=sum(weighted_speed.values())
    pa=p['Yes'][1];pb=p['No'][1]
    v1=v['Yes'];v0=v['No']
    c=(pa-pb)*((v1[1]+v0[1])/2-(v1[0]+v0[0])/2)
    wr=((pa+pb)/2)*(v1[1]-v0[1])+(1-(pa+pb)/2)*(v1[0]-v0[0])
    delta=mu['Yes']-mu['No']
    assert abs(delta-c-wr)<1e-12
    return {'n_bees':len(ids),'bee_ids':[int(x) for x in ids],
           'delta':float(delta),'composition':float(c),'within_route':float(wr),
           'p_above_no':float(pb),'p_above_yes':float(pa)}


def report(source,summary,out):
    d=original(source)
    expected=json.loads(Path(summary).read_text())['outcomes']
    actual={}
    diffs=[]
    for name,heights,direction in (
         ('main_height_98_127',[98,127],None),
         ('all_height_69_127',[69,98,127],None),
         ('Up-tunnel',[98,127],'Up-tunnel'),
         ('Down-tunnel',[98,127],'Down-tunnel')):
        pieces=[independent_height(d,h,direction) for h in heights]
        obs={k:float(np.mean([p[k] for p in pieces]))
             for k in ['delta','composition','within_route']}
        expected_obs=(expected['by_flight_direction_98_127'][name]['observed']
                      if direction else expected[name]['observed'])
        err={k:abs(obs[k]-expected_obs[k]) for k in obs}
        diffs.extend(err.values())
        actual[name]={'observed':obs,'parts':{str(h):p for h,p in zip(heights,pieces)},'error':err}
    if max(diffs)>=1e-12:raise AssertionError('PRODUCTION_VS_INDEPENDENT_DISAGREE')
    # Individual deletion check: sample unit is bee, not one of its repeated flights.
    deletion=[]
    for h in (98,127):
        baseline=independent_height(d,h)
        for bid in baseline['bee_ids']:
            child=independent_height(d,h,exclude_bee=bid)
            other=independent_height(d,127 if h==98 else 98)
            deletion.append({'height':int(h),'bee_hash':hashlib.sha256(str(bid).encode()).hexdigest()[:12],
               'delta':(child['delta']+other['delta'])/2,
               'composition':(child['composition']+other['composition'])/2,
               'within_route':(child['within_route']+other['within_route'])/2})
    outcome={'source_sha256':SHA,'status':'INDEPENDENT_ARITHMETIC_VALIDATED',
        'maximum_difference':max(diffs),'reconstructions':actual,
        'delete_one_bee':{'n':len(deletion),'delta_range':[min(x['delta'] for x in deletion),max(x['delta'] for x in deletion)],
        'composition_range':[min(x['composition'] for x in deletion),max(x['composition'] for x in deletion)],
        'within_route_range':[min(x['within_route'] for x in deletion),max(x['within_route'] for x in deletion)]}}
    Path(out).write_text(json.dumps(outcome,indent=2))
    print('INDEPENDENT_CHECK',json.dumps({'max_error':max(diffs),'deletions':len(deletion),'range':outcome['delete_one_bee']}),flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--source',required=True);a.add_argument('--summary',required=True);a.add_argument('--out',required=True)
    q=a.parse_args();report(q.source,q.summary,q.out)