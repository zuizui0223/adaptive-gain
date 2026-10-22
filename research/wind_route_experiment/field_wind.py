"""Source-locked Balfour/Ratnieks: decompose wind association of inflorescence/flower visits.

Original study already reported a positive *proportional* switching association.
The analysis separately checks inflorescence numerator and flower denominator.
Fields are observational and individuals have no separate ID; dates are clusters.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

SWITCH_FILE='Balfouretal_Inflorescence_Switch_Rate_DataDryad.csv'
FORAGE_FILE='Balfouretal_Foraging_Rate_DataDryad.csv'
SHA256={
  SWITCH_FILE:'f47ba91ebca47433a3bc709d23771fd0c3b380100b5e3a9109b47458df5da53d',
  FORAGE_FILE:'ffe3d3e8612f673478b677284a5b05703c1000e8e040153144865ad3662b941d'}
SEED=20261022

def load_balfour(path):
    path=Path(path);raw=path.read_bytes();actual=hashlib.sha256(raw).hexdigest()
    if actual!=SHA256.get(path.name):raise ValueError('ORIGINAL_FIELD_CSV_DIGEST_OR_NAME_CHANGED')
    df=pd.read_csv(path)
    if df.isna().any().any():raise ValueError('SOURCE_CSV_UNEXPECTED_MISSINGNESS')
    for c in ('Date','Bee_species','Flower_species','Location'):
        if c not in df:raise ValueError('SOURCE_HEADER_CHANGED_'+c)
        df[c]=df[c].astype(str).str.strip()
    if path.name==SWITCH_FILE:
        if len(df)!=210 or not (df['Inflorences']>=1).all() or not (df['Flowers']>=1).all() or not (df['Inflorences']<=df['Flowers']).all():
            raise ValueError('INFLORESCENCE_COUNTS_INCOHERENT')
    elif path.name==FORAGE_FILE:
        if len(df)!=329 or not (df['Flowers']>0).all():raise ValueError('FLOWER_COUNTS_INCOHERENT')
        # Source spelling typo is harmonized only for this known genus.
        df['Bee_species']=df['Bee_species'].str.replace('^zApis mellifera$','Apis mellifera',regex=True)
    return df,{'original_sha256_verified':True,'sha256':actual,'rows':len(df),
               'dates':int(df.Date.nunique()),'bee_classes':int(df.Bee_species.nunique()),
               'flower_categories':int(df.Flower_species.nunique()),
               'locations':int(df.Location.nunique())}

def baseline_matrix(df,temp_field):
    categorical=['Date','Bee_species','Flower_species','Location']
    dummy=pd.get_dummies(df[categorical],drop_first=True,dtype=float)
    z=np.column_stack([np.ones(len(df)),dummy.to_numpy(float),pd.to_numeric(df[temp_field]).to_numpy(float)])
    return z

def fit_ols_with_controls(wind,y,controls):
    z=np.asarray(controls,float)
    if z.ndim!=2 or len(z)!=len(y):raise ValueError('INVALID_CONTROL_MATRIX')
    x=np.column_stack([np.ones(len(y)),np.asarray(wind,float),z])
    return float(np.linalg.lstsq(x,np.asarray(y,float),rcond=None)[0][1])

def date_shuffle_reference(wind,dates,rng,reps=4999):
    dates=np.asarray(dates);wind=np.asarray(wind,float)
    m=np.repeat(wind[None,:],reps,axis=0)
    for label in pd.unique(dates):
        ix=np.flatnonzero(dates==label)
        if len(ix)<=1:continue
        order=np.argsort(rng.random((reps,len(ix))),axis=1)
        m[:,ix]=wind[ix][order]
    return m

def bootstrap_date(wind,yy,z,dates,reps=4999,seed=SEED):
    wind=np.asarray(wind,float);y=np.asarray(yy,float);dates=np.asarray(dates)
    y=y.reshape(-1,1) if y.ndim==1 else y
    X=np.column_stack([wind,z])
    keys=list(pd.unique(dates));N=len(keys)
    xx=[];xy=[]
    for date in keys:
        w=(dates==date);xx.append(X[w].T@X[w]);xy.append(X[w].T@y[w])
    xx=np.stack(xx);xy=np.stack(xy)
    rng=np.random.default_rng(seed)
    betas=np.empty((reps,y.shape[1]))
    for j in range(reps):
        draw=rng.integers(N,size=N)
        weight=np.bincount(draw,minlength=N)
        gram=np.tensordot(weight,xx,axes=(0,0));rhs=np.tensordot(weight,xy,axes=(0,0))
        betas[j]=np.linalg.lstsq(gram,rhs,rcond=1e-12)[0][0]
    return np.quantile(betas,[.025,.975],axis=0).T

def field_regressions(df,outcomes,temp_col='Temp',reps=4999,seed=SEED):
    z=baseline_matrix(df,temp_col)
    x=df.Wind.to_numpy(float)
    ys=np.column_stack([np.asarray(val,float) for val in outcomes.values()])
    keys=list(outcomes)
    # Frisch-Waugh-Lovell: residualize outcomes and permuted wind with exact
    # original baseline before computing any post-analysis perm p-values.
    U,S,V=np.linalg.svd(z,full_matrices=False)
    rank=int((S>S[0]*1e-10).sum())
    Q=U[:,:rank]
    Y=ys-Q@(Q.T@ys)
    xp=x-Q@(Q.T@x)
    denom=xp@xp
    if denom<1e-10:raise ValueError('NO_WITHIN_CONTEXT_WIND_VARIATION')
    slopes=(xp@Y)/denom
    nullwind=date_shuffle_reference(x,df.Date.to_numpy(),np.random.default_rng(seed+1),reps=reps)
    WX=nullwind-(nullwind@Q)@Q.T
    null=(WX@Y)/(WX*WX).sum(axis=1)[:,None]
    ci=bootstrap_date(x,ys,z,df.Date.to_numpy(),reps=reps,seed=seed+2)
    summary={}
    for j,name in enumerate(keys):
        p=(1+int((np.abs(null[:,j])>=abs(slopes[j])-1e-12).sum()))/(reps+1)
        summary[name]={
          'n_observations':int(len(df)),'n_dates':int(df.Date.nunique()),
          'wind_slope_log_per_ms':float(slopes[j]),
          'multiplicative_per_1ms':float(np.exp(slopes[j])),
          'date_bootstrap_slope95':[float(v) for v in ci[j]],
          'date_bootstrap_multiplicative95':[float(np.exp(v)) for v in ci[j]],
          'within_date_wind_shuffle_p_two_sided_exploratory':float(p),
          'sign_from_regression':'positive' if slopes[j]>0 else 'negative',
          'uncertainty':'date cluster bootstrap and conditional label shuffle; natural wind unassigned'}
    return summary

def analyze(root,out):
    root=Path(root);out=Path(out);out.mkdir(exist_ok=True,parents=True)
    s,q1=load_balfour(root/SWITCH_FILE)
    f,q2=load_balfour(root/FORAGE_FILE)
    if s.Date.nunique()<10 or f.Date.nunique()<10:raise ValueError('WEAK_TEMPORAL_REPLICATION')
    I=s.Inflorences.to_numpy(float);F=s.Flowers.to_numpy(float)
    outcomes={'log_inflorescences_visited':np.log(I),
              'log_flowers_visited':np.log(F),
              'log_inflorescence_per_flower':np.log(I/F)}
    a=field_regressions(s,outcomes)
    eq=a['log_inflorescence_per_flower']['wind_slope_log_per_ms']-(a['log_inflorescences_visited']['wind_slope_log_per_ms']-a['log_flowers_visited']['wind_slope_log_per_ms'])
    if abs(eq)>1e-10:raise AssertionError('RATIO_COMPONENT_ARITHMETIC_FAILED')
    b=field_regressions(f,{'log_flowers_per_minute':np.log(f.Flowers.to_numpy(float))},temp_col='Temperature')
    switch=(I-1)/(F-1)
    sensitivity={
       'n_raw_switches':len(s),'n_switch_proxy_undefined_Feq1':int(np.sum(F<=1)),
       'mean_I_div_F':float(np.mean(I/F)),'mean_switch_proxy_Iminus1_div_Fminus1':float(np.mean(switch[F>1]))}
    report={'source_doi':'10.5061/dryad.4qrfj6qpf','source_zip_sha256':'79d9ed20ccaa0370d31cd454eb6b293efbf2d18525443a3ae16ae3154a43fa38',
            'original_tables':{SWITCH_FILE:q1,FORAGE_FILE:q2},
            'primary_rows':len(s),'primary_dates':int(s.Date.nunique()),
            'primary_definition':'log(I/F)=log(I)-log(F). I=inflorescences observed, F=flowers observed, one-minute window.',
            'decomposition_algebra_error':float(eq),'switch':a,'foraging_independent_subset':b,
            'sensitivity':sensitivity,
            'limitations':['Observational natural wind; only foraging-active bees observed.',
               'No independent bee ID, cluster inference by observed Date only.',
               'No individual plant identities; inflorescences not equivalent to different plants.',
               'Ratio change may reflect flower denominator rather than inter-plant route choice.',
               'Original paper already reported proportional movement and lower foraging speed.',
               'Original paper methods and figure definitions of switch rate are not perfectly consistent.',
               'Source dates/groups differ across 210 switch and 329 foraging observations; not an independent replication.',
               'Repeated sessions within location/date and flower selection may confound natural wind effects.']}
    (out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    for key,result in a.items():print('BALFOUR_DECOMPOSITION',key,json.dumps(result),flush=True)
    print('BALFOUR_FORAGING_RATE',json.dumps(b),flush=True)
    print('BALFOUR_SOURCE_ANALYSIS_COMPLETE',report['primary_rows'],report['primary_dates'],flush=True)
    return report

if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--source-dir',default='.')
    cli.add_argument('--out',default='field_results');args=cli.parse_args()
    analyze(args.source_dir,args.out)