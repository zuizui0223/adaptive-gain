"""Observed partner/time segregation in the complete OIK-07303 raw compilation.

This is not cue routeability, animal-individual specialization, independent
floral availability, effort-standardized abundance or latent link rewiring.
Nulls preserve a visitor taxon's date counts and plant-count margins; local
nulls also preserve these margins within calendar blocks. Detection and focal
plant effort varying between dates are NOT removed by these nulls.
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, platform, time, urllib.request
from pathlib import Path
import numpy as np
import pandas as pd

SOURCE='https://zenodo.org/records/4744654/files/'
FILES={'OIK-07303_database.csv':'7a70c3e2356611b0871c163a2f9aed4a',
       'OIK-07303_original_studies.xlsx':'5db9f1b31fc27820e08aeff2b737ef13',
       'OIK-07303_network_aggregation.R':'636d0ac376b6dbb3da90692072e2856e',
       'README.pdf':'8fcef9e74f4268570246b35ffc3adb2e'}

def entropy_parts(counts):
    a=np.asarray(counts)
    if a.ndim!=2 or not np.isfinite(a).all() or (a<0).any() or (a!=np.floor(a)).any() or a.sum()<=0:
        raise ValueError('nonempty 2D nonnegative integer counts required')
    n=float(a.sum()); rows=a.sum(1); cols=a.sum(0)
    def xlogx(x):
        x=np.asarray(x,dtype=float);x=x[x>0];return float(np.sum(x*np.log(x)))
    hp=math.log(n)-xlogx(cols)/n
    hc=(xlogx(rows)-xlogx(a))/n
    return {'I':hp-hc,'Hpool':hp,'Hwithin':hc,'Dpool':math.exp(hp),'Dwithin':math.exp(hc),'ratio':math.exp(hp-hc)}

def permutation_null(counts,reps,seed,blocks=None):
    a=np.asarray(counts,dtype=np.int64);base=entropy_parts(a)
    if type(reps) is not int or reps<1:raise ValueError('positive repetitions required')
    nd,np_=a.shape
    plants=np.concatenate([np.repeat(np.arange(np_),r) for r in a])
    dates=np.repeat(np.arange(nd),a.sum(1));rng=np.random.default_rng(seed)
    if blocks is None:groups=[np.arange(len(plants))]
    else:
        blocks=np.asarray(blocks)
        if len(blocks)!=nd:raise ValueError('one block per date required')
        event_blocks=blocks[dates]
        groups=[np.flatnonzero(event_blocks==b) for b in np.unique(event_blocks)]
    # Only blocks spanning >=2 dates and >=2 plants can alter the statistic.
    groups=[g for g in groups if len(np.unique(dates[g]))>1 and len(np.unique(plants[g]))>1]
    out=np.empty(reps)
    if not groups:return np.full(reps,base['I'])
    nr=a.sum(1);nc=a.sum(0);n=len(plants)
    row_term=np.sum(nr[nr>0]*np.log(nr[nr>0]))
    col_term=np.sum(nc[nc>0]*np.log(nc[nc>0]))
    constant=(n*np.log(n)-row_term-col_term)/n
    for k in range(reps):
        shuffled=plants.copy()
        for g in groups:shuffled[g]=rng.permutation(plants[g])
        c=np.bincount(dates*np_+shuffled,minlength=nd*np_);c=c[c>0]
        out[k]=constant+np.sum(c*np.log(c))/n
    return out

def download(raw):
    raw.mkdir(parents=True,exist_ok=True);receipt=[]
    for name,md5 in FILES.items():
        path=raw/name;url=SOURCE+name+'?download=1'
        if not path.exists():
            last=None
            for attempt in range(3):
                try:
                    request=urllib.request.Request(url,headers={'User-Agent':'adaptive-gain-research/1.0'})
                    with urllib.request.urlopen(request,timeout=90) as r:path.write_bytes(r.read())
                    last=None;break
                except Exception as exc:last=exc;time.sleep(2*(attempt+1))
            if last is not None:
                if name=='OIK-07303_database.csv':raise last
                receipt.append({'file':name,'error':str(last)});continue
        b=path.read_bytes();actual=hashlib.md5(b).hexdigest()
        if actual!=md5:raise ValueError(f'checksum mismatch {name}: {actual} != {md5}')
        receipt.append({'file':name,'url':url,'bytes':len(b),'md5':actual,'sha256':hashlib.sha256(b).hexdigest()})
    (raw/'provenance.json').write_text(json.dumps(receipt,indent=2))
    return receipt

def read_source_csv(path):
    """Parse verified original bytes without lossy replacement.

    Some identifiers in the archived CSV contain non-UTF-8 bytes. Prefer strict
    UTF-8 if it works; otherwise Latin-1 maps every source byte reversibly to
    a code point. Do not mutate the archived file or silently drop rows.
    The chosen codec is reported in the quality receipt.
    """
    original = Path(path).read_bytes()
    try:
        original.decode('utf-8')
        encoding = 'utf-8'
    except UnicodeDecodeError:
        encoding = 'latin-1'
    return pd.read_csv(io.BytesIO(original), encoding=encoding), encoding


def summarize(g):
    fields=['I','Dpool','Dwithin','ratio','excess_global','excess_7d','excess_14d','excess_28d']
    ans={'panels':len(g),'visits':int(g.visits.sum()),'site_years':int(g[['site','year']].drop_duplicates().shape[0]),'visitor_labels':int(g.visitor.nunique())}
    for f in fields:
        ans[f+'_median']=float(g[f].median());ans[f+'_mean']=float(g[f].mean())
    for w in ['global','7d','14d','28d']:
        ans[w+'_positive_fraction']=float((g['excess_'+w]>1e-10).mean())
        ans[w+'_p_le_005_fraction']=float((g['p_'+w]<=.05).mean())
    ans['four_week_adjusted_factor_median']=float(np.exp(g.excess_28d).median())
    return ans

def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='macro_results');ap.add_argument('--reps',type=int,default=199)
    ap.add_argument('--min-visits',type=int,default=40);ap.add_argument('--min-days',type=int,default=4);ap.add_argument('--min-plants',type=int,default=3)
    args=ap.parse_args(argv);out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    provenance=download(out/'raw');df,source_encoding=read_source_csv(out/'raw/OIK-07303_database.csv')
    required=['study','cdate','sSite','allSites','lower','higher','freq','sgrain']
    if not set(required)<=set(df):raise ValueError(f'missing columns: {df.columns}')
    freq=pd.to_numeric(df.freq,errors='coerce');date=pd.to_datetime(df.cdate,errors='coerce')
    profile={'raw_rows':len(df),'columns':list(df),'source_text_encoding':source_encoding,
             'source_text_policy':'strict UTF-8 or reversible Latin-1, with verified original raw bytes retained','source_studies':int(df.study.nunique()),'sum_freq':float(freq.sum()),
             'zero_freq':int((freq==0).sum()),'negative_freq':int((freq<0).sum()),'noninteger_freq':int((freq.dropna()%1!=0).sum()),
             'duplicate_full_rows':int(df.duplicated().sum()),'missing_by_column':{k:int(v) for k,v in df.isna().sum().items()},
             'sgrain_counts':{str(k):int(v) for k,v in df.sgrain.value_counts(dropna=False).items()},
             'min_compiled_date':str(date.min()),'max_compiled_date':str(date.max()),'bad_date':int(date.isna().sum()),
             'sSite_units':int(df[['study','sSite']].drop_duplicates().shape[0]),'allSites_units':int(df[['study','allSites']].drop_duplicates().shape[0]),
             'duplicate_policy':'RETAIN repeated positive visit rows; no event IDs establish duplicates',
             'date_policy':'compiled cdate; three southern sources were shifted +182 days by compilers; no weather linkage performed',
             'denominator_policy':'freq is recorded interaction count, not independent survey effort; no non-detection denominator inferred'}
    valid=df[['study','sSite','lower','higher']].notna().all(axis=1)&date.notna()&freq.notna()&(freq>0)&(freq%1==0)
    if (freq<0).any() or (freq.dropna()%1!=0).any():raise ValueError('negative or noninteger visit frequencies')
    bystudy=[]
    for study,g in df.groupby('study',sort=True):
        idx=g.index
        bystudy.append({'study':study,'rows':len(g),'visits':float(freq.loc[idx].sum()),'sites':int(g.sSite.nunique()),'dates':int(g.cdate.nunique()),
                        'plants':int(g.lower.nunique()),'visitors':int(g.higher.nunique()),'grain':','.join(sorted(g.sgrain.dropna().astype(str).unique())),
                        'min_date':str(date.loc[idx].min()),'max_date':str(date.loc[idx].max())})
    pd.DataFrame(bystudy).to_csv(out/'source_inventory.csv',index=False)
    profile['valid_positive_rows']=int(valid.sum());profile['valid_positive_visits']=int(freq[valid].sum())
    daily=valid&df.sgrain.eq('day');work=df.loc[daily,required].copy();work['freq']=freq[daily].astype(np.int64);work['date']=date[daily];work['year']=work.date.dt.year
    profile['daily_rows']=len(work);profile['daily_visits']=int(work.freq.sum());profile['daily_studies']=int(work.study.nunique())
    (out/'quality_profile.json').write_text(json.dumps(profile,indent=2));print('DATA_PROFILE '+json.dumps(profile),flush=True)
    for row in bystudy:print('SOURCE '+json.dumps(row),flush=True)
    cells=work.groupby(['study','sSite','year','higher','date','lower'],observed=True,sort=True).freq.sum().reset_index()
    results=[];flow=[]
    for key,g in cells.groupby(['study','sSite','year','higher'],sort=True):
        study,site,year,visitor=key;visits=int(g.freq.sum());days=int(g.date.nunique());plants=int(g.lower.nunique())
        reasons=[]
        if visits<args.min_visits:reasons.append('visits_below_min')
        if days<args.min_days:reasons.append('dates_below_min')
        if plants<args.min_plants:reasons.append('partners_below_min')
        row={'study':study,'site':site,'year':int(year),'visitor':visitor,'visits':visits,'days':days,'plants':plants}
        flow.append(dict(row,eligible=not reasons,reasons=';'.join(reasons)))
        if reasons:continue
        mat=g.pivot(index='date',columns='lower',values='freq').fillna(0).sort_index().astype(np.int64)
        counts=mat.to_numpy();obs=entropy_parts(counts);row.update(obs)
        seed=int.from_bytes(hashlib.sha256(repr(key).encode()).digest()[:8],'little')
        ordinal=(mat.index.dayofyear.to_numpy()-1)
        for j,window in enumerate([None,7,14,28]):
            label='global' if window is None else str(window)+'d'
            blocks=None if window is None else ordinal//window
            null=permutation_null(counts,args.reps,seed+j,blocks)
            row['null_'+label]=float(null.mean());row['excess_'+label]=float(obs['I']-null.mean())
            row['p_'+label]=float((1+np.sum(null>=obs['I']-1e-12))/(args.reps+1))
        results.append(row)
    flow=pd.DataFrame(flow);res=pd.DataFrame(results)
    flow.to_csv(out/'eligibility_all_panels.csv',index=False);res.to_csv(out/'visitor_site_season_results.csv',index=False)
    if res.empty:raise ValueError('No eligible daily panels; inspect profile rather than invent results')
    study_results=[]
    for study,g in res.groupby('study',sort=True):
        entry={'study':study,**summarize(g)};study_results.append(entry);print('RESULT_STUDY '+json.dumps(entry),flush=True)
    pd.DataFrame(study_results).to_csv(out/'study_results.csv',index=False)
    full={'scope':'observed temporal resource-use segregation, not individual behavior or sensory routeability','reps':args.reps,
          'thresholds':{'visits':args.min_visits,'days':args.min_days,'partners':args.min_plants},
          'all_daily_panels':len(flow),'eligible_panels':len(res),'eligible_studies':len(study_results),**summarize(res),
          'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'provenance':provenance}
    for f in ['excess_global','excess_7d','excess_14d','excess_28d']:
        values=np.array([r[f+'_mean'] for r in study_results]);full[f+'_positive_source_means']=int((values>1e-10).sum());full[f+'_equal_source_mean']=float(values.mean())
    (out/'summary.json').write_text(json.dumps(full,indent=2));print('FINAL_SUMMARY '+json.dumps(full),flush=True)
    print('ANALYSIS_COMPLETE',flush=True)
if __name__=='__main__':main()
