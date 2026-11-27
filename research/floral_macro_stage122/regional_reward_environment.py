"""Stage122: exploratory environment screen on immutable Stage121 scores."""
import argparse,hashlib,zipfile,json
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import rankdata
SHA='2c4f13aed29d331488c3225a742a97327ce2d39f4bdf42c19e39bf90186c3a6a'
G='source_geographic_block';W='gust15_ERA5model_1991_2020_point';B='GBIF_Bombus_3occ_2grid_recorded_species_primary';E='GBIF_Bombus_unique_1degree_recorded_cells'
C=['source_ERA5_point_latitude','source_ERA5_1991_2020_mean_temperature_C','WorldClim_1970_2000_precip_mm_month']
METRIC='within_assemblage_pair_contrast_skill'
def load(path):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=SHA:raise ValueError('Stage121 SHA drift')
    with zipfile.ZipFile(path) as z:d=pd.read_csv(z.open('stage121_regional_reward_transfer_summary.csv'))
    if len(d)!=432 or d.TDWG_L3.nunique()!=72 or d[G].nunique()!=17 or d.duplicated(['TDWG_L3','cohort','lineage_excluded']).any():raise ValueError('cohort drift')
    return d
def zrank(v):
    r=rankdata(v);s=r.std();return (r-r.mean())/s if s>1e-12 else np.zeros(len(r))
def design(d,bee,blocks,extra,primary=True):
    terms=[W]+([B] if bee else []);ctrl=C+extra+([E] if bee else [])
    if len(d)<(30 if primary else 20) or d[G].nunique()<(10 if primary else 5):return None,terms
    x=np.column_stack([np.ones(len(d))]+[zrank(d[k]) for k in terms+ctrl]+([pd.get_dummies(d[G],drop_first=True).to_numpy(float)] if blocks else []))
    rank=np.linalg.matrix_rank(x)
    if rank!=x.shape[1] or len(d)-rank<8:return None,terms
    return x,terms
def fit(q,y,bee,blocks,extra,primary=True):
    d=q.dropna(subset=[y,W,*([B,E] if bee else []),*C,*extra])
    x,terms=design(d,bee,blocks,extra,primary)
    if x is None:return None
    v=zrank(d[y])
    if v.std()<1e-12:return None
    a=np.linalg.lstsq(x,v,rcond=None)[0]
    return {'n':len(d),'blocks':int(d[G].nunique()),'df':int(len(d)-x.shape[1]),'coef':dict(zip(terms,map(float,a[1:1+len(terms)])))}
def screen(q,y,bee,extra):
    q=q[q[E]>=5] if bee else q
    q=q.dropna(subset=[y,W,*([B,E] if bee else []),*C,*extra])
    out={'eligible_n':len(q),'eligible_blocks':int(q[G].nunique())}
    for blk in (False,True):
        res=fit(q,y,bee,blk,extra);out['block' if blk else 'adjusted']=res
        if res:
            fits=[fit(q[q[G]!=g],y,bee,blk,extra,False) for g in sorted(q[G].unique())];fits=[f for f in fits if f]
            res['lobo']={k:{'min':min(f['coef'][k] for f in fits),'max':max(f['coef'][k] for f in fits),'n':len(fits),'positive':sum(f['coef'][k]>0 for f in fits)} for k in res['coef']} if fits else None
    return out
def run(d):
    out={}
    for lineage in ['genus','family']:
        z=d[(d.lineage_excluded==lineage)&d.status.eq('estimated_exploratory')];res={}
        for reward in ['nectar','pollen']:
            q=z[z.cohort==reward+'_separate'];y=reward+'_'+METRIC
            res[reward]={m:{'wind':screen(q,y,False,c),'wind_Bombus':screen(q,y,True,c)} for m,c in [('primary',['n_test']),('support_sensitivity',['n_test','n_train']),('variance_sensitivity',['n_test',reward+'_test_reward_variance'])]}
            res[reward]['alternative_scores']={k:screen(q,reward+'_'+k,True,['n_test']) for k in ['kendall_tau_b','transfer_skill_vs_training_mean']}
        n=z[z.cohort=='nectar_separate'];p=z[z.cohort=='pollen_separate'];a=n.merge(p[['TDWG_L3','n_test','n_train','pollen_'+METRIC]],on='TDWG_L3',suffixes=('','_p'),validate='1:1');a['different_cohort_contrast']=a['nectar_'+METRIC]-a['pollen_'+METRIC+'_p']
        res['shared_regions_different_species']={'n':len(a),'blocks':int(a[G].nunique()),'positive':int((a.different_cohort_contrast>0).sum()),'median':float(a.different_cohort_contrast.median()),'wind':screen(a,'different_cohort_contrast',False,['n_test','n_test_p']),'wind_Bombus':screen(a,'different_cohort_contrast',True,['n_test','n_test_p'])}
        out[lineage]=res
    return {'source_sha256':SHA,'regional_min_n':30,'regional_min_blocks':10,'no_IID_pvalue':True,'same_region_different_species_not_paired':True,'no_37_geographic_holdout':True,'results':out}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(load(a.source));a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print('STAGE122_REGIONAL_REWARD_ENVIRONMENT',json.dumps(r,sort_keys=True))
