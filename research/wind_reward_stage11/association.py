"""Frozen survey-level wind x independently sampled floral-reward association.

No calculated energetic profit is used as response. CR1 city-date clusters.
The protocol was committed before the first biological model was evaluated.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t

def within_plant(d):
    z=d.copy()
    if 'survey' in z and z.survey.duplicated().any(): raise ValueError('SURVEY_DUPLICATION')
    z['q']=np.log1p(z.energy_j)
    z['w']=z.wind-z.groupby('plant').wind.transform('mean')
    q=z.q-z.groupby('plant').q.transform('mean')
    sd=float(np.std(q.to_numpy(),ddof=1))
    if not np.isfinite(sd) or sd<=1e-12: raise ValueError('NO_WITHIN_PLANT_REWARD_VARIATION')
    z['r']=q/sd
    return z,sd

def design(d,city=True):
    parts=[np.ones((len(d),1))];names=['Intercept']
    for c in (['plant','site'] if city else ['plant']):
        levels=sorted(d[c].astype(str).unique())
        for level in levels[1:]:
            parts.append((d[c].astype(str)==level).to_numpy(dtype=float)[:,None]);names.append(c+':'+level)
    doy=pd.to_datetime(d.date).dt.dayofyear.to_numpy()
    columns={'w':d.w.to_numpy(),'r':d.r.to_numpy(),'w:r':(d.w*d.r).to_numpy(),
             'temperature':d.temperature.to_numpy(),'blue_sky_fraction':d.blue_sky.to_numpy()/100,
             'season_sin':np.sin(2*np.pi*doy/365.25),'season_cos':np.cos(2*np.pi*doy/365.25),
             'log1p_density':np.log1p(d.flower_density.to_numpy())}
    for name,value in columns.items():parts.append(np.asarray(value,dtype=float)[:,None]);names.append(name)
    X=np.hstack(parts)
    if not np.isfinite(X).all(): raise ValueError('NONFINITE_FROZEN_DESIGN')
    return X,names

def clustered_ols(X,y,g):
    X=np.asarray(X,dtype=float);y=np.asarray(y,dtype=float);g=np.asarray(g)
    n,p=X.shape;groups=np.unique(g);G=len(groups)
    if len(y)!=n or len(g)!=n or not np.isfinite(X).all() or not np.isfinite(y).all():raise ValueError('INVALID_OLS_INPUT')
    rank=int(np.linalg.matrix_rank(X))
    if rank!=p:raise ValueError(f'DESIGN_RANK_DEFICIENT:{rank}/{p}')
    if n<=p or G<2:raise ValueError('INSUFFICIENT_CLUSTER_OR_RESIDUAL_DF')
    Q,R=np.linalg.qr(X,mode='reduced')
    beta=np.linalg.solve(R,Q.T@y)
    residual=y-X@beta
    invR=np.linalg.solve(R,np.eye(p));bread=invR@invR.T
    scores=np.vstack([X[g==k].T@residual[g==k] for k in groups])
    correction=G/(G-1)*(n-1)/(n-p)
    cov=correction*bread@(scores.T@scores)@bread
    cov=(cov+cov.T)/2
    if not np.isfinite(cov).all():raise ValueError('NONFINITE_CLUSTER_COVARIANCE')
    return {'beta':beta,'cov':cov,'n':n,'p':p,'rank':rank,'residual_df':n-p,'clusters':G,'t_df':G-1,
            'cr1_correction':float(correction),'residual':residual,'condition_number':float(np.linalg.cond(X))}

def contrast(fit,c):
    c=np.asarray(c,dtype=float);b=float(c@fit['beta']);v=float(c@fit['cov']@c)
    if v < -1e-10:raise ValueError('NEGATIVE_CONTRAST_VARIANCE')
    se=float(np.sqrt(max(0,v)))
    if se<=0:raise ValueError('DEGENERATE_CONTRAST_VARIANCE')
    critical=float(t.ppf(.975,fit['t_df']));stat=b/se
    return {'coefficient':b,'cluster_se':se,'ci95':[b-critical*se,b+critical*se],
            't':stat,'t_df':fit['t_df'],'p_two_sided':float(2*t.sf(abs(stat),fit['t_df']))}

def evaluate(d,city=True,min_residual=40):
    X,names=design(d,city=city);groups=(d.site.astype(str)+'|'+d.date.astype(str)).to_numpy()
    fit=clustered_ols(X,np.log1p(d.probes.to_numpy()),groups)
    if fit['residual_df']<min_residual:raise ValueError('RESIDUAL_DF_BELOW_FROZEN_GATE')
    eye=np.eye(len(names));c=eye[names.index('w:r')];effect=contrast(fit,c)
    slopes={str(r):contrast(fit,eye[names.index('w')]+r*c) for r in (-1,0,1)}
    return {'status':'ESTIMATED','surveys':fit['n'],'columns':fit['p'],'rank':fit['rank'],
            'residual_df':fit['residual_df'],'city_date_clusters':fit['clusters'],'condition_number':fit['condition_number'],
            'primary_interaction':effect,'conditional_wind_slopes':slopes,
            'coefficient_names':names,'coefficients':fit['beta'].tolist(),
            'response':'log(1+survey_mean_observed_probes_per_60s)',
            'wind_units':'within-plant centered ordinal Beaufort, not metres per second',
            'reward_units':'within-plant log1p(sampled_J_per_flower), per pooled within-plant SD'}

def run(root):
    root=Path(root);out=root/'association_results.json'
    d=pd.read_csv(root/'survey_cohort.csv')
    result={'status':'PENDING','model_protocol':'PROTOCOL_WIND_REWARD_20261030.md',
            'not_causal':True,'nectar_is_sampled_potential_not_actual_intake':True}
    try:
        if d.survey.duplicated().any():raise ValueError('DUPLICATE_SURVEY')
        G=(d.site.astype(str)+'|'+d.date.astype(str)).nunique()
        if len(d)<80 or G<30 or d.site.nunique()!=2:raise ValueError('FROZEN_SAMPLE_SUPPORT_NOT_MET')
        z,scale=within_plant(d)
        result['within_plant_log_reward_sd']=scale
        result['primary']=evaluate(z)
        result['by_city_descriptive']={}
        for city,g in z.groupby('site',sort=True):
            try:res=evaluate(g,city=False,min_residual=15)
            except ValueError as e:res={'status':'NOT_ESTIMABLE','reason':str(e),'surveys':len(g)}
            result['by_city_descriptive'][city]=res
        result['status']='SOURCE_VERIFIED_SINGLE_PRIMARY_MODEL_COMPLETE'
    except ValueError as e:
        result.update(status='NO_GO_FROZEN_MODEL',reason=str(e))
        raise
    finally:
        out.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
        print('STAGE11_ASSOCIATION_RESULT '+json.dumps(result,ensure_ascii=False,allow_nan=False),flush=True)
    return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',default='stage11_original')
    run(p.parse_args().out)
