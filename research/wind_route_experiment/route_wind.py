"""Original Dryad bee flight wind experiment: route choice and motion are separate outcomes.

Replicate units are BEES. Direction-matched per-bee contrasts prevent individual
repeated flights being treated as independent. The wind condition was assigned
within bees, while obstacle field height was randomized among bees. A route
proxy based on median altitude is not a trajectory or real plant choice.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

SOURCE_SHA256='2361dccb523b97f1e5e542fc492d302a5e7c290cdde72eb2dfb2ce021153d6f7'
SOURCE_SIZE=22602
SEED=20261022
WINDS=['No','Yes']
REQUIRED=['Bee ID','Canopy height (mm)','Wind Presence','Flight Direction Label',
          'Median altitude (mm)','Altitudinal range (mm)',
          'Median ground speed (m/s)','Lateral excursion (mm)']
NUMERIC=REQUIRED[4:]

def load_original(path, enforce_size=True):
    raw=Path(path).read_bytes()
    sha=hashlib.sha256(raw).hexdigest()
    if sha!=SOURCE_SHA256 or (enforce_size and len(raw)!=SOURCE_SIZE):
        raise ValueError('PUBLIC_ORIGINAL_FILE_SHA256_OR_SIZE_MISMATCH')
    d=pd.read_csv(path)
    if set(REQUIRED)!=set(d.columns):raise ValueError('ORIGINAL_FLIGHT_COLUMN_CHANGE')
    if d[REQUIRED].isna().any().any():raise ValueError('MISSING_ORIGINAL_FLIGHT_MEASUREMENT')
    if not d['Wind Presence'].isin(WINDS).all():raise ValueError('UNKNOWN_WIND_CONDITION')
    if not d['Flight Direction Label'].isin(['Up-tunnel','Down-tunnel']).all():
        raise ValueError('UNKNOWN_FLIGHT_DIRECTION')
    if (d[NUMERIC]<0).any().any():raise ValueError('NEGATIVE_MOTION_MEASUREMENT')
    if d.groupby('Bee ID')['Canopy height (mm)'].nunique().gt(1).any():
        raise ValueError('OBSTACLE_HEIGHT_CHANGED_WITHIN_BEE')
    return d,{'sha256':sha,'sha256_verified':True,'bytes':len(raw),
               'n_flights':len(d),'n_bees':int(d['Bee ID'].nunique()),
               'wind_flights':{str(k):int(v) for k,v in d['Wind Presence'].value_counts().items()},
               'height_flights':{str(k):int(v) for k,v in d['Canopy height (mm)'].value_counts().items()}}

def matched_bee_deltas(d, col, min_canopy=None, wind_dir=None):
    """Mean within each bee & flight direction, then equal direction weights."""
    w=d.copy()
    if min_canopy is not None:
        w=w.loc[w['Canopy height (mm)']>=min_canopy]
    if wind_dir is not None:
        w=w.loc[w['Flight Direction Label']==wind_dir]
    if len(w)==0:return pd.DataFrame(columns=['bee_id','height','delta','n_matched_directions'])
    cols=['Bee ID','Canopy height (mm)','Flight Direction Label']
    grouped=w.groupby(cols+['Wind Presence'],sort=True,observed=True)[col].mean().unstack('Wind Presence')
    if not set(WINDS)<=set(grouped.columns):return pd.DataFrame(columns=['bee_id','height','delta','n_matched_directions'])
    paired=grouped.dropna(subset=WINDS).copy()
    if paired.empty:return pd.DataFrame(columns=['bee_id','height','delta','n_matched_directions'])
    paired['difference']=paired['Yes']-paired['No']
    bead=paired.groupby(['Bee ID','Canopy height (mm)']).agg(
        delta=('difference','mean'),n_matched_directions=('difference','size')).reset_index()
    return bead.rename(columns={'Bee ID':'bee_id','Canopy height (mm)':'height'})

def route_differences(d,min_canopy=69,wind_dir=None):
    w=d.copy()
    if 'route_above_proxy' not in w:
        w['route_above_proxy']=(w['Median altitude (mm)']>w['Canopy height (mm)']).astype(float)
    return matched_bee_deltas(w,'route_above_proxy',min_canopy=min_canopy,wind_dir=wind_dir)

def bootstrap_ci(values,reps=4999,seed=SEED):
    x=np.asarray(values,dtype=float)
    if not len(x) or not np.isfinite(x).all():raise ValueError('INVALID_BEE_CONTRAST')
    rng=np.random.default_rng(seed)
    draw=x[rng.integers(len(x),size=(reps,len(x)))].mean(axis=1)
    return [float(v) for v in np.quantile(draw,[.025,.975])]

def sign_flip_p(values,reps=9999,seed=SEED):
    x=np.asarray(values,dtype=float)
    if not len(x) or not np.isfinite(x).all():raise ValueError('INVALID_BEE_CONTRAST')
    observed=float(np.mean(x))
    if np.all(x==0):return 1.
    rng=np.random.default_rng(seed)
    signs=rng.choice([-1.,1.],size=(reps,len(x)))
    null=(signs*x).mean(axis=1)
    return float((1+int((np.abs(null)>=abs(observed)-1e-12).sum()))/(reps+1))

def summarize(d,field,min_canopy=None,wind_dir=None):
    x=(route_differences(d,min_canopy,wind_dir) if field=='route_above_proxy'
         else matched_bee_deltas(d,field,min_canopy,wind_dir))
    n=len(x)
    if n<5:return {'status':'NO_GO_FEWER_THAN_FIVE_PAIRED_BEES','n_bees':n}
    vals=x['delta'].to_numpy()
    return {'status':'PAIRED_DESCRIPTIVE','n_bees':n,
            'n_directions_matched':int(x.n_matched_directions.sum()),
            'mean_wind_minus_still':float(vals.mean()),
            'site_equal_bee_bootstrap_ci95':bootstrap_ci(vals),
            'bee_signflip_p_two_sided_exploratory':sign_flip_p(vals),
            'positive_bees':int((vals>0).sum()),'negative_bees':int((vals<0).sum()),
            'zero_bees':int((vals==0).sum()),
            'by_obstacle_height':{str(h):{
                'n_bees':int(len(g)),'mean_delta':float(g.delta.mean())}
                for h,g in x.groupby('height')}}

def run(source,outdir):
    d,qc=load_original(source)
    d['route_above_proxy']=(d['Median altitude (mm)']>d['Canopy height (mm)']).astype(float)
    main={
       'route_69to127':summarize(d,'route_above_proxy',min_canopy=69),
       'route_40to127':summarize(d,'route_above_proxy',min_canopy=40),
       'route_98to127':summarize(d,'route_above_proxy',min_canopy=98),
       'route_127_only':summarize(d.loc[d['Canopy height (mm)']==127],'route_above_proxy',min_canopy=127),
       'median_ground_speed':summarize(d,'Median ground speed (m/s)'),
       'lateral_excursion':summarize(d,'Lateral excursion (mm)'),
       'median_altitude':summarize(d,'Median altitude (mm)')}
    for k,dirn in [('up_headwind','Up-tunnel'),('down_tailwind','Down-tunnel')]:
        main[f'ground_speed_{k}']=summarize(d,'Median ground speed (m/s)',wind_dir=dirn)
        main[f'lateral_excursion_{k}']=summarize(d,'Lateral excursion (mm)',wind_dir=dirn)
        main[f'route_{k}_69to127']=summarize(d,'route_above_proxy',min_canopy=69,wind_dir=dirn)
    route=d[d['Canopy height (mm)']>=69]
    tally=route.groupby(['Canopy height (mm)','Wind Presence'])['route_above_proxy'].agg(['sum','size','mean'])
    receipt={'study':'Burnett Badger Combes 2022','doi':'10.25338/B8Z34Q',
      'experiment':'fanned wind versus still air; height randomly assigned among bees, condition order randomly initiated',
      'scope':'Flight path proxy versus speed and lateral excursion; not natural biological alternative/cue access',
      'source_qc':qc,
      'counts_by_height_wind':[{'height_mm':int(h),'wind':str(w),'n':int(x['size']),
          'n_above':int(x['sum']),'fraction_above':float(x['mean'])}
          for (h,w),x in tally.iterrows()],
      'results':main,'limitations':[
          'Above proxy is median altitude exceeding obstacle height, not entire trajectory',
          'Wind direct manipulation at 0.54m/s in laboratory, not field wind and no species interaction',
          'Within bee wind order could affect fatigue, bee held obstacle height fixed',
          'Bee-signflip p exploratory, imperfect randomization-based null; repeated flights not independent',
          'Direction-specific windy tail/head contrast also depends on tunnel direction',
          'A non-significant route difference does not demonstrate equivalence/no effect',
          'Original publication already reported wind affecting performance not altitude']}
    path=Path(outdir);path.mkdir(parents=True,exist_ok=True)
    (path/'summary.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False))
    for name,r in main.items():
        print('WIND_ROUTE_RESULT',name,json.dumps(r,ensure_ascii=False),flush=True)
    print('WIND_ROUTE_SOURCE_COMPLETE',len(d),qc['n_bees'],flush=True)
    return receipt

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--source',required=True);a.add_argument('--out',default='results')
    args=a.parse_args()
    run(args.source,args.out)