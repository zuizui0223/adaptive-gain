"""Exact noncausal Oaxaca-Kitagawa decomposition of filmed wind-tunnel speed.

The source records experimentally switched wind *within bees*, but observed
flight route is post-treatment; decomposition is descriptive, not mediation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ORIGINAL_SHA256="2361dccb523b97f1e5e542fc492d302a5e7c290cdde72eb2dfb2ce021153d6f7"
SEED=20261022


def components(p,v):
    """Symmetric exact composition and within-state mean shift, route 0/1."""
    p=np.asarray(p,float);v=np.asarray(v,float)
    if p.shape!=(2,2) or v.shape!=(2,2) or not (np.isfinite(p).all() and np.isfinite(v).all()):
        raise ValueError('BAD_ROUTE_STATE_MATRIX')
    if not np.allclose(p.sum(axis=1),1.,atol=1e-10):
        raise ValueError('ROUTE_PROBABILITY_NOT_NORMALIZED')
    d=float((p[1]*v[1]).sum()-(p[0]*v[0]).sum())
    c=float(((p[1]-p[0])*(v[0]+v[1])*.5).sum())
    w=float(((p[1]+p[0])*(v[1]-v[0])*.5).sum())
    if abs(d-c-w)>2e-12:raise AssertionError('EXACT_ROUTE_DECOMPOSITION_IDENTITY')
    return {'delta':d,'composition':c,'within_route':w}


def height_components(arr):
    """arr[bee,wind(0/1),route(0/1), count/speed-sum] of positive recordings."""
    x=np.asarray(arr,float)
    if x.ndim!=4 or x.shape[1:]!=(2,2,2) or x.shape[0]<1:
        raise ValueError('BAD_BEE_PANEL_SHAPE')
    c=x[:,:,:,0];s=x[:,:,:,1]
    if (c<0).any() or (s<0).any() or not np.isfinite(x).all():
        raise ValueError('NONFINITE_OR_NEGATIVE_SOURCE')
    denom=c.sum(axis=2,keepdims=True)
    if (denom<=0).any():raise ValueError('UNPAIRED_BEE_WIND_COHORT')
    p=np.mean(c/denom,axis=0)
    mass=np.mean(s/denom,axis=0)
    if (p<=0).any():raise ValueError('EMPTY_WIND_ROUTE_CELL')
    v=mass/p
    res=components(p,v)
    res.update({'route_above_wind_minus_still':float(p[1,1]-p[0,1]), 'n_bees':int(len(x)),
        'p':p.tolist(),'v':v.tolist(),
        'speed_by_wind':mass.sum(axis=1).tolist(),
        'n_films_by_wind_route':c.sum(axis=0).astype(int).tolist()})
    return res


def bootstrap_components(panels,heights,nrep=9999,seed=SEED):
    """Stratified by randomized obstacle height, entire bees resampled."""
    if len(heights)<1 or any(h not in panels for h in heights) or nrep<1:
        raise ValueError('INVALID_BOOTSTRAP_DESIGN')
    rng=np.random.default_rng(seed)
    estimates={int(h):height_components(panels[h]) for h in heights}
    obs={key:float(np.mean([estimates[h][key] for h in estimates]))
         for key in ['delta','composition','within_route','route_above_wind_minus_still']}
    if abs(obs['delta']-obs['composition']-obs['within_route'])>2e-12:
        raise AssertionError('STRATUM_MEAN_IDENTITY')
    draws=[]
    invalid=[]
    for h in heights:
        arr=np.asarray(panels[h],float)
        c=arr[:,:,:,0];s=arr[:,:,:,1]
        denom=c.sum(axis=2,keepdims=True)
        if (denom<=0).any():raise ValueError('UNPAIRED_BEE_WIND_COHORT')
        probs=c/denom; masses=s/denom
        idx=rng.integers(len(arr),size=(nrep,len(arr)))
        p=probs[idx].mean(axis=1)
        mass=masses[idx].mean(axis=1)
        good=(p>0).all(axis=(1,2))
        v=np.zeros_like(mass)
        np.divide(mass,p,out=v,where=p>0)
        d=(mass[:,1,:]-mass[:,0,:]).sum(axis=1)
        cr=(((p[:,1,:]-p[:,0,:])*(v[:,1,:]+v[:,0,:]))/2).sum(axis=1)
        wr=(((p[:,1,:]+p[:,0,:])*(v[:,1,:]-v[:,0,:]))/2).sum(axis=1)
        route_delta=p[:,1,1]-p[:,0,1]
        arr3=np.column_stack([d,cr,wr,route_delta]);arr3[~good,:]=np.nan
        draws.append(arr3);invalid.append(int((~good).sum()))
    combined=np.mean(np.stack(draws,axis=0),axis=0)
    good=np.isfinite(combined).all(axis=1)
    if not good.any():raise ValueError('NO_VALID_BEE_BOOTSTRAPS')
    if np.max(np.abs(combined[good,0]-combined[good,1]-combined[good,2]))>1e-12:
        raise AssertionError('BOOTSTRAP_IDENTITY_FAILED')
    labels=['delta','composition','within_route','route_above_wind_minus_still']
    ci={key:[float(t) for t in np.quantile(combined[good,i],[.025,.975])]
        for i,key in enumerate(labels)}
    return {'heights_mm':list(map(int,heights)),
      'height_specific':estimates,'observed':obs,'bootstrap_ci95':ci,
      'bootstrap_reps':int(nrep),'valid_reps':int(good.sum()),
      'invalid_by_height':{str(h):n for h,n in zip(heights,invalid)},
      'bootstrap_sign_counts':{key:{'negative':int((combined[good,i]<0).sum()),
                                 'positive':int((combined[good,i]>0).sum())}
        for i,key in enumerate(labels)},
      'claim_ceiling':'Exact descriptive partition, not a causal route-mediated wind effect; route is selected after wind.'}


def load_source(path):
    path=Path(path);body=path.read_bytes();digest=hashlib.sha256(body).hexdigest()
    if digest!=ORIGINAL_SHA256:raise ValueError('UNVERIFIED_DRYAD_ORIGINAL')
    d=pd.read_csv(path)
    expected={'Bee ID','Canopy height (mm)','Wind Presence','Flight Direction Label',
      'Median altitude (mm)','Median ground speed (m/s)','Lateral excursion (mm)'}
    if len(d)!=548 or d['Bee ID'].nunique()!=58 or expected-set(d):
        raise ValueError('ORIGINAL_SOURCE_GRAIN_CHANGE')
    if d[list(expected)].isna().any().any() or not d['Wind Presence'].isin(['Yes','No']).all():
        raise ValueError('MISSING_OR_NONBINARY_EXPERIMENTAL_WIND')
    if d.groupby('Bee ID')['Canopy height (mm)'].nunique().max()!=1:
        raise ValueError('RANDOMIZED_BETWEEN_BEE_HEIGHT_NOT_FIXED')
    d=d.copy();d['wind']=(d['Wind Presence']=='Yes').astype(int)
    d['route']=(d['Median altitude (mm)']>d['Canopy height (mm)']).astype(int)
    return d,{'sha256':digest,'source_bytes':len(body),'n_flights':int(len(d)),
       'n_individual_bees':int(d['Bee ID'].nunique()),
       'canopy_levels':{str(k):int(v) for k,v in d['Canopy height (mm)'].value_counts().sort_index().items()}}


def prepare_bee_panels(d,heights,flight_direction=None):
    """Construct an exact 2-wind × 2-route × counts/speed-sum array per bee."""
    df=d[d['Canopy height (mm)'].isin(heights)].copy()
    if flight_direction is not None:
        df=df.loc[df['Flight Direction Label']==flight_direction]
    ans={}
    for h in heights:
        sub=df.loc[df['Canopy height (mm)']==h]
        blocks=[]
        for bid,g in sub.groupby('Bee ID',sort=True):
            if g.wind.nunique()!=2:continue
            arr=np.zeros((2,2,2),float)
            for wind in [0,1]:
                for route in [0,1]:
                    sel=g.loc[(g.wind==wind)&(g.route==route)]
                    arr[wind,route,0]=len(sel)
                    arr[wind,route,1]=sel['Median ground speed (m/s)'].sum()
            blocks.append(arr)
        if blocks:ans[int(h)]=np.stack(blocks,axis=0)
    return ans


def run(source,out,reps=9999):
    df,qc=load_source(source)
    panels=prepare_bee_panels(df,[69,98,127])
    main=bootstrap_components(panels,[98,127],reps,seed=SEED)
    sensitivity=bootstrap_components(panels,[69,98,127],reps,seed=SEED+7)
    directions={}
    for direction in ('Up-tunnel','Down-tunnel'):
        pan=prepare_bee_panels(df,[98,127],flight_direction=direction)
        directions[direction]=bootstrap_components(pan,[98,127],reps,seed=SEED+len(direction))
    result={'study':'Burnett Badger Combes 2022','doi':'10.25338/B8Z34Q',
     'source_qc':qc,'source_data_used':'unmodified original',
     'outcomes':{'main_height_98_127':main,'all_height_69_127':sensitivity,
                 'by_flight_direction_98_127':directions},
     'reanalysis_tag':'post-support exploratory route-composition versus within-route-speed decomposition',
     'not_estimated':'Causal mediation, wind effect on ecological accessibility, bee resource choice or fitness'}
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print('MAIN_ROUTE_SPEED_DECOMPOSITION',json.dumps(main,ensure_ascii=False))
    print('SOURCE_QC',json.dumps(qc,ensure_ascii=False))
    return result

if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--source',required=True);cli.add_argument('--out',required=True);cli.add_argument('--reps',type=int,default=9999)
    a=cli.parse_args();run(a.source,a.out,a.reps)