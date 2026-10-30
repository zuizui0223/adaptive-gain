"""Original survey-key data contract; observational unit is survey, not bee row."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd

HASHES={'forage.csv':'c5bb7b67780b8749014cb645fa43fc35bc1ffe8a4b1c8edcb5637d07a5146f61','nectar.csv':'3908be05bbc4e5585d1ad93cbebf08fa6a67ea7e975278c8386e19b4c7da9d6a','weather.csv':'c7b09eaef978b4bc8bbd6bf093c2872130c8a6038ec206a4f36fa365896a9641'}
def norm(x): return ' '.join(str(x).strip().lower().split())
def prepare(df):
    out=df.copy();out.columns=[c.strip() for c in out.columns]
    if len(set(out.columns))!=len(out.columns): raise ValueError('NORMALIZED_COLUMN_COLLISION')
    out['survey']=out.survey.astype(str).str.strip()
    out['date']=pd.to_datetime(out.date.astype(str).str.strip(),format='%d/%m/%Y',errors='raise')
    return out

def numeric(df,cols):
    out=df[cols].apply(pd.to_numeric,errors='raise')
    if not np.isfinite(out.to_numpy(dtype=float)).all(): raise ValueError('MISSING_NONFINITE_REQUIRED_NUMERIC')
    return out

def energy_j(volume_ul,brix):
    if not np.isfinite(volume_ul) or not np.isfinite(brix) or volume_ul<0 or not 0<=brix<=100:
        raise ValueError('INVALID_NECTAR_UNITS')
    gravity=1+brix/(258.6-(brix/258.2)*227.1)
    return volume_ul/1000*(brix/100)*gravity*16480

def build(forage,nectar,weather):
    f,n,w=map(prepare,(forage,nectar,weather))
    excluded=[];rows=[]
    q={'forage_rows':len(f),'forage_surveys':int(f.survey.nunique()),'nectar_rows':len(n),'weather_rows':len(w),
       'weather_surveys':int(w.survey.nunique()),'excluded':excluded,
       'source_join':'aggregate each source to survey before one-to-one matching; nectar.site is forage.location'}
    for key,g in f.groupby('survey',sort=True):
        def drop(reason,details=None): excluded.append({'survey':key,'forage_rows':len(g),'reason':reason,'details':details})
        if any(g[c].map(norm).nunique()!=1 for c in ('date','site','location','plant')):
            drop('forage_metadata_not_unique');continue
        ng=n[n.survey==key];wg=w[w.survey==key]
        if ng.empty:drop('no_nectar_source');continue
        if wg.empty:drop('no_weather_source');continue
        date=g.date.iloc[0];city=str(g.site.iloc[0]).strip();loc=str(g.location.iloc[0]).strip();plant=str(g.plant.iloc[0]).strip()
        if any(not (ng[c].map(norm)==norm(value)).all() for c,value in [('date',date),('site',loc),('plant',plant)]):
            drop('nectar_metadata_mismatch',{c:ng[c].astype(str).unique().tolist() for c in ('date','site','plant')});continue
        if any(not (wg[c].map(norm)==norm(value)).all() for c,value in [('date',date),('site',city),('location',loc)]):
            drop('weather_metadata_mismatch',{c:wg[c].astype(str).unique().tolist() for c in ('date','site','location')});continue
        rawcols=['tube volume','tube length','length','number of flowers sampled']
        if ng[rawcols].isna().any().any():drop('nectar_not_directly_sampled');continue
        fn=numeric(g,['flowers probed','time flying (s)','approx flower density (flowers / m2)'])
        nn=numeric(ng,['volume/flower','concentration'])
        wn=numeric(wg,['temperature','blue_sky','beaufort'])
        if (fn['flowers probed']<0).any() or (fn['flowers probed']%1!=0).any(): raise ValueError('INVALID_PROBED_COUNTS')
        if not fn['time flying (s)'].between(0,60).all():raise ValueError('FLYING_TIME_OUTSIDE_60S')
        if not wn.beaufort.between(0,12).all() or not wn.blue_sky.between(0,100).all():raise ValueError('WEATHER_UNITS_INVALID')
        if not nn.concentration.between(0,100).all() or (nn['volume/flower']<0).any():raise ValueError('NECTAR_UNITS_INVALID')
        v=float(nn['volume/flower'].mean());c=float(nn.concentration.mean())
        row={'survey':key,'date':date.strftime('%Y-%m-%d'),'site':city,'location':loc,'plant':plant,
             'n_observations':len(g),'n_nectar_samples':len(ng),'n_weather_readings':len(wg),
             'probes':float(fn['flowers probed'].mean()),'flying_seconds':float(fn['time flying (s)'].mean()),
             'flower_density':float(fn['approx flower density (flowers / m2)'].mean()),
             'volume_ul':v,'brix':c,'energy_j':energy_j(v,c),
             'temperature':float(wn.temperature.mean()),'blue_sky':float(wn.blue_sky.mean()),'wind':float(wn.beaufort.mean())}
        rows.append(row)
    d=pd.DataFrame(rows)
    if not d.empty:
        if d.survey.duplicated().any():raise ValueError('JOIN_MULTIPLICATION')
        q.update(eligible_surveys=len(d),eligible_foraging_observations=int(d.n_observations.sum()),cities=sorted(d.site.unique().tolist()),
                 city_days=int((d.site+'|'+d.date).nunique()),plants=int(d.plant.nunique()),
                 plant_support=[{'plant':k,'surveys':len(g),'wind_levels':int(g.wind.nunique()),'dates':int(g.date.nunique())} for k,g in d.groupby('plant')],
                 wind_counts={str(k):int(v) for k,v in d.wind.value_counts().sort_index().items()})
    return d,q

def run(root):
    root=Path(root);tables=[]
    for name,sha in HASHES.items():
        raw=(root/name).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('ORIGINAL_HASH_CHANGED:'+name)
        tables.append(pd.read_csv(root/name))
    d,q=build(*tables)
    d.to_csv(root/'survey_cohort.csv',index=False)
    (root/'cohort_receipt.json').write_text(json.dumps(q,indent=2,ensure_ascii=False))
    print('STAGE11_COHORT_QA '+json.dumps(q,ensure_ascii=False),flush=True)
    return d,q
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',default='stage11_original')
    run(p.parse_args().out)
