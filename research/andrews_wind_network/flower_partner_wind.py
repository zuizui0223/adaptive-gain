"""SA026: blooming-flower-matched ST/BR plant–visitor link incidence.

This is observational, not an experiment or a proof of animal choice or
wind-driven predation. Original source SHA-1 is verified. Source presence
in flowering-plant data is mandatory before a visit/no-visit response exists.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
import numpy as np
import pandas as pd

EXPECTED_SHA1={
    'watch.csv':'fcd28cf0c9623fbfbc5619136334265a65f13dc4',
    'flowers.csv':'c93b5496154245b9e94dc3362297ed354db3ebb6',
}
KEY=['SAMPLEDATE','PLOT_ID','WATCH']
BEE_ROLES={'social bee','solitary bee','halictine bee','semi-social bee',
           'halictine bee/semi-social bee','pollenivore bee'}
METRICS=['H_all','H_bee','signed_all','signed_bee']


def validate_source(folder):
    source=Path(folder)
    for fn,sha in EXPECTED_SHA1.items():
        found=hashlib.sha1((source/fn).read_bytes()).hexdigest()
        if found!=sha:raise ValueError('SA026_ORIGINAL_SHA1_MISMATCH_'+fn)
    watch=pd.read_csv(source/'watch.csv',dtype=str,keep_default_na=False,encoding='latin-1')
    flowers=pd.read_csv(source/'flowers.csv',dtype=str,keep_default_na=False,encoding='latin-1')
    if (len(watch),len(flowers))!=(74942,23642):
        raise ValueError('SA026_ORIGINAL_ROW_COUNT_MISMATCH')
    return watch,flowers


def eligible_watches(w):
    """Use the exact earlier source QC gate, not an optimized new subset."""
    x=w.copy()
    x['minute_num']=pd.to_numeric(x.MINUTE,errors='coerce')
    x['bad_positive']=(x.PPI_STATUS=='1')&~pd.to_numeric(x.NO_INT,errors='coerce').gt(0)
    meta=x.groupby(KEY,sort=False).agg(
        minute_n=('minute_num','nunique'),minute_min=('minute_num','min'),minute_max=('minute_num','max'),
        minute_valid=('minute_num',lambda s:s.between(1,15).all()),
        wind_n=('WIND','nunique'),wind=('WIND','first'),
        wind_valid=('WIND',lambda s:s.isin(['ST','BR']).all()),
        bad=('bad_positive','any'),meadow=('MEADOW','first'),year=('YEAR','first'))
    mixed=x.groupby(KEY+['MINUTE'],sort=False).PPI_STATUS.nunique()
    conflict=mixed[mixed>1].index.droplevel('MINUTE').unique()
    good=(meta.minute_n==15)&(meta.minute_min==1)&(meta.minute_max==15)&meta.minute_valid&\
         (meta.wind_n==1)&meta.wind_valid&~meta.bad&~meta.index.isin(conflict)
    meta=meta.loc[good].reset_index()
    if len(meta)!=1296:raise ValueError('COMPLETE_1296_WATCH_GATE_CHANGED')
    pos=x[(x.PPI_STATUS=='1') & (~x.bad_positive) & (x.PLTSP_CODE.str.strip()!='')].copy()
    pos=pos.merge(meta[KEY],on=KEY,how='inner',validate='many_to_one')
    pos['plant']=pos.PLTSP_CODE.str.strip()
    pos['is_bee']=pos.VISSP_TYPE.str.lower().str.strip().isin(BEE_ROLES)
    return meta,pos


def bloom_rows(f,require_positive_flower_amount=False):
    z=f[(f.FLW_STATUS=='FLW')&(f.PLTSP_CODE.str.strip()!='')].copy()
    z['plant']=z.PLTSP_CODE.str.strip()
    if require_positive_flower_amount:
        z=z.loc[pd.to_numeric(z.NO_STALK,errors='coerce').gt(0)&
                pd.to_numeric(z.NO_FLWS,errors='coerce').gt(0)].copy()
    if z.duplicated(KEY+['plant']).any():
        raise ValueError('DUPLICATED_WATCH_FLOWERING_PLANT')
    return z[KEY+['plant']]


def admissible_masks(bloom,n_br):
    """All assignments of wind to WHOLE watches retaining bloom overlap."""
    b=np.asarray(bloom,bool)
    if b.ndim!=2 or b.shape[1]<1:raise ValueError('INVALID_BLOOM_PANEL')
    n=b.shape[0]
    out=[]
    for ix in combinations(range(n),int(n_br)):
        mask=np.zeros(n,bool);mask[list(ix)]=True
        if not mask.any() or mask.all():continue
        if np.all(np.any(b[mask],axis=0)) and np.all(np.any(b[~mask],axis=0)):
            out.append(mask)
    return np.asarray(out,bool).reshape((-1,n))


def day_stats(bloom,visit_all,visit_bee,wind_br):
    b=np.asarray(bloom,bool);m=np.asarray(wind_br,bool)
    if b.ndim!=2 or b.shape!=np.asarray(visit_all).shape or b.shape!=np.asarray(visit_bee).shape:
        raise ValueError('MISMATCHED_OPPORTUNITY_AND_VISIT_MATRIX')
    if np.any(np.asarray(visit_all,bool)&~b) or np.any(np.asarray(visit_bee,bool)&~b):
        raise ValueError('UNSURVEYED_FLOWERS_MUST_NOT_BE_IMPUTED_VISITS')
    if not m.any() or m.all() or np.any(b[m].sum(axis=0)==0) or np.any(b[~m].sum(axis=0)==0):
        raise ValueError('NO_SAME_PLANT_BLOOM_EXPOSURE_IN_BOTH_WIND_CLASSES')
    output=[]; signed=[]
    for visits in [visit_all,visit_bee]:
        v=np.asarray(visits,bool)
        d=v[m].sum(axis=0)/b[m].sum(axis=0)-v[~m].sum(axis=0)/b[~m].sum(axis=0)
        output.append(float(np.mean((d-d.mean())**2)))
        signed.append(float(d.mean()))
    return np.asarray(output+signed,float)


def holm(pvals):
    x=np.asarray(pvals,float);idx=np.argsort(x)
    adjusted=np.zeros(len(x));prefix=0.
    for j,k in enumerate(idx):
        prefix=max(prefix,min(1.,(len(x)-j)*x[k]))
        adjusted[k]=prefix
    return adjusted.tolist()


def construct_days(meta,pos,f,require_positive_amount=False):
    flor=bloom_rows(f,require_positive_amount)
    matched=meta.merge(flor,on=KEY,how='inner',validate='one_to_many')
    # Only fixed plant taxa observed flowering in both original wind states.
    group=matched.groupby(['meadow','SAMPLEDATE','plant']).wind.nunique()
    shared=group[group==2].reset_index()[['meadow','SAMPLEDATE','plant']]
    shared=shared.merge(matched,on=['meadow','SAMPLEDATE','plant'],how='inner')
    positive=pos.groupby(KEY+['plant']).agg(all=('is_bee','size'),bee=('is_bee','sum')).reset_index()
    days=[];candidate=[]
    for (meadow,date),fl in shared.groupby(['meadow','SAMPLEDATE'],sort=True):
        plants=sorted(fl.plant.unique())
        if len(plants)<2:continue
        w=meta.loc[(meta.meadow==meadow)&(meta.SAMPLEDATE==date)].sort_values(KEY).reset_index(drop=True)
        n=len(w);P=len(plants)
        wind=w.wind.eq('BR').to_numpy(bool)
        if len(w.drop_duplicates(subset=KEY))!=n:raise ValueError('DUPLICATE_WATCH')
        b=np.zeros((n,P),bool)
        index={tuple(row):i for i,row in enumerate(w[KEY].itertuples(index=False,name=None))}
        cols={k:j for j,k in enumerate(plants)}
        for row in fl[KEY+['plant']].itertuples(index=False,name=None):
            b[index[tuple(row[:3])],cols[row[3]]]=True
        valid=admissible_masks(b,int(wind.sum()))
        if len(valid)<2:continue
        if not np.any(np.all(valid==wind,axis=1)):raise ValueError('OBSERVED_ASSIGNMENT_NOT_ADMISSIBLE')
        y=np.zeros_like(b);yb=np.zeros_like(b)
        p=positive.loc[positive.set_index(KEY).index.isin(w.set_index(KEY).index)]
        for row in p[KEY+['plant','all','bee']].itertuples(index=False,name=None):
            kk=tuple(row[:3]);pp=row[3]
            if kk in index and pp in cols and b[index[kk],cols[pp]]:
                y[index[kk],cols[pp]]=row[4]>0
                yb[index[kk],cols[pp]]=row[5]>0
        days.append({'meadow':str(meadow),'date':str(date),'wind':wind,'bloom':b,
                     'all':y,'bee':yb,'names':plants,'n_assignments':len(valid)})
        candidate.append({'meadow':str(meadow),'date':str(date),'plants':len(plants),
                          'n_watches':n,'n_wind_ST':int((~wind).sum()),'n_wind_BR':int(wind.sum()),
                          'n_admissible_label_assignments':len(valid),
                          'observed_all_opportunities':int(b.sum()),
                          'all_positive_bloom_links':int(y.sum()),'bee_positive_bloom_links':int(yb.sum())})
    return days,pd.DataFrame(candidate),{
       'source_floral_match_watches':int(matched[KEY].drop_duplicates().shape[0]),
       'source_floral_opportunity_rows':len(matched),
       'shared_bloom_plant_date_codes_before_gates':int(group.eq(2).sum()),
       'flower_amount_policy':'positive NO_STALK and NO_FLWS required' if require_positive_amount else 'recorded FLW status only'
    }


def evaluate_panel(days,reps=9999,seed=20261022,boot_reps=4999,equal_days=False):
    if not days:raise ValueError('NO_ELIGIBLE_PAIRED_BLOOM_DAYS')
    pre=[];out=[]
    for d in days:
        valid=admissible_masks(d['bloom'],int(np.asarray(d['wind'],bool).sum()))
        values=np.vstack([day_stats(d['bloom'],d['all'],d['bee'],m) for m in valid])
        observed=day_stats(d['bloom'],d['all'],d['bee'],d['wind'])
        center=values.mean(axis=0)
        pre.append({'meadow':d['meadow'],'date':d.get('date','synthetic'),
                    'value':observed,'center':center,'null':values-center,'excess':observed-center,
                    'n_masks':len(valid),'n_plants':int(d['bloom'].shape[1])})
    groups=sorted({x['meadow'] for x in pre})
    rng=np.random.default_rng(seed)
    # Keep all watch contrasts for one meadow together; overrepresentation of
    # dates by some meadows must not create fake independent replication.
    site_effect=np.zeros((len(groups),len(METRICS)))
    site_null=np.zeros((len(groups),reps,len(METRICS)))
    days_per_site=[]
    for i,site in enumerate(groups):
        one=[p for p in pre if p['meadow']==site]
        site_effect[i]=np.mean([p['excess'] for p in one],axis=0)
        for p in one:
            k=len(p['null'])
            inds=rng.integers(k,size=reps)
            site_null[i]+=p['null'][inds]/len(one)
        days_per_site.append(len(one))
    if equal_days:
        weights=np.asarray(days_per_site,float)/sum(days_per_site)
    else:
        weights=np.full(len(groups),1/len(groups))
    observed=np.average(site_effect,axis=0,weights=weights)
    null=np.einsum('i,irj->rj',weights,site_null)
    boots=None
    if not equal_days:
        indices=rng.integers(len(groups),size=(boot_reps,len(groups)))
        boots=site_effect[indices].mean(axis=1)
    # One-sided H and centered two-sided signed reference.
    ps=[];metrics={}
    for j,name in enumerate(METRICS):
        if j<2:
            p=(1+int(np.sum(null[:,j]>=observed[j]-1e-12)))/(reps+1)
        else:
            p=(1+int(np.sum(np.abs(null[:,j])>=abs(observed[j])-1e-12)))/(reps+1)
        ps.append(p)
        metrics[name]={'excess_above_exact_assignment_mean':float(observed[j]),
                       'permutation_p':float(p),
                       'null_centered_sd':float(null[:,j].std(ddof=1)),
                       'site_bootstrap_95ci':([float(x) for x in np.quantile(boots[:,j],[.025,.975])]
                          if boots is not None else None)}
    for j,q in enumerate(holm(ps[:2])):metrics[METRICS[j]]['holm_q_family2']=q
    # Raw per-day observed effects and exact finite allocation expectations.
    raw_mean=np.average(np.array([np.mean([p['value'] for p in pre if p['meadow']==m],axis=0)
                        for m in groups]),axis=0,weights=weights)
    null_mean=np.average(np.array([np.mean([p['center'] for p in pre if p['meadow']==m],axis=0)
                        for m in groups]),axis=0,weights=weights)
    for j,name in enumerate(METRICS):
        metrics[name]['raw_observed']=float(raw_mean[j])
        metrics[name]['exact_assignment_expected']=float(null_mean[j])
    return {'n_meadows':len(groups),'n_days':len(days),'n_plant_day_pairs':sum(int(d['bloom'].shape[1]) for d in days),
            'n_plant_watch_observation_opportunities':sum(int(d['bloom'].sum()) for d in days),
            'n_watches':sum(len(d['wind']) for d in days),
            'n_dates_exact_label_null_invariant_H_all':int(sum(np.ptp(p['null'][:,0])<1e-12 for p in pre)),
            'n_dates_exact_label_null_invariant_H_bee':int(sum(np.ptp(p['null'][:,1])<1e-12 for p in pre)),
            'min_max_admissible_assignments':[min(p['n_masks'] for p in pre),max(p['n_masks'] for p in pre)],
            'weighting':'day-equal' if equal_days else 'meadow-equal',
            'metrics':metrics,'site_scores':[{'meadow_hash':hashlib.sha256(s.encode()).hexdigest()[:14],
               'n_days':days_per_site[i],**{k:float(site_effect[i,j]) for j,k in enumerate(METRICS)}}
                 for i,s in enumerate(groups)],
            'eligibility_comment':'Every compared flowering plant was recorded in both ST and BR and every null assignment retains that support.'}


def run(folder,out,reps=9999):
    w,f=validate_source(folder)
    meta,pos=eligible_watches(w)
    all_days,candidates,qa=construct_days(meta,pos,f)
    if (len(all_days),len(set(d['meadow'] for d in all_days)),sum(len(d['names']) for d in all_days))!=(35,11,162):
        raise ValueError('SOURCE_PREANALYSIS_SUPPORT_CHANGED')
    variants={'main':evaluate_panel(all_days,reps),
              'day_equal_weight':evaluate_panel(all_days,reps,seed=20261023,equal_days=True)}
    balanced=[d for d in all_days if int(d['wind'].sum())>=2 and int((~d['wind']).sum())>=2]
    variants['min2_watches_per_wind']=(evaluate_panel(balanced,reps,seed=20261024) if balanced else {'status':'NO_DATA'})
    flower_strict,strict_qc,strict_info=construct_days(meta,pos,f,require_positive_amount=True)
    if len(flower_strict)<20 or len(set(d['meadow'] for d in flower_strict))<8:
        variants['numeric_flower_amounts']={'status':'NO_GO_INSUFFICIENT_SUPPORT','n_days':len(flower_strict),
                      'n_meadows':len(set(d['meadow'] for d in flower_strict))}
    else:
        variants['numeric_flower_amounts']=evaluate_panel(flower_strict,reps,seed=20261025)
    report={'status':'EXPLORATORY_OBSERVATIONAL_NOT_CAUSAL','doi':'10.6073/pasta/eec55cbc3dbfc56428629773737ab3e5',
        'checksum_source_sha1':EXPECTED_SHA1,'source_watch_rows':len(w),'source_flower_rows':len(f),
        'eligible_complete_15min_watches':len(meta),'qc':qa,'strict_flower_amount_qc':strict_info,
        'variants':variants,'limit':'wind label not randomized; multiple sampled plots; known bloom presence is not complete available choice; no individual predator cues or fitness'}
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    candidates.to_csv(out/'source_support_ledger.csv',index=False)
    strict_qc.to_csv(out/'strict_source_support_ledger.csv',index=False)
    print('PLANT_PARTNER_WIND_ANALYSIS_COMPLETE',json.dumps({'main':variants['main']['metrics'],
          'support':{k:variants['main'][k] for k in ['n_days','n_meadows','n_plant_day_pairs','n_plant_watch_observation_opportunities','n_dates_exact_label_null_invariant_H_all']},
          'balanced':{'n_days':len(balanced)},'strict':{'n_days':len(flower_strict)}}),flush=True)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-dir',required=True);p.add_argument('--out',required=True);p.add_argument('--reps',type=int,default=9999)
    a=p.parse_args();run(a.source_dir,a.out,a.reps)