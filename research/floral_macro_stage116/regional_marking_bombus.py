"""Stage116 source-conditional regional marking x wind x recorded Bombus."""
import pandas as pd, numpy as np, zipfile, hashlib, json
from pathlib import Path
from scipy.stats import rankdata
SOURCES={15069908329:('8c9e02040c5a3e68331b636b0c61886410bb15242e3770c065657e65d9b7a6d2','stage114_original72_contactfree_mainland_ERA5point_3cue_reporting_frame_ONLY.csv'),14419407872:('2fe7510fe8c08189d63151fe255a00baafb96c7acc87d3d0fedc970966ca1a43','stage87D_original_GBIF_Bombus_TDWG3_recorded_richness.csv')}
W='gust15_ERA5model_1991_2020_point'; B='GBIF_Bombus_3occ_2grid_recorded_species_primary'; E='GBIF_Bombus_unique_1degree_recorded_cells'; R='GBIF_Bombus_original_positive_occurrence_records'; G='source_geographic_block'; Y='near_visual_NHM_word_positive_per_colour_described'; Y2='near_visual_NHM_word_positive_per_native'; C=['NHM_colour_field_description_coverage','WFO_original_flora_description_coverage','source_ERA5_point_latitude','source_ERA5_1991_2020_mean_temperature_C','WorldClim_1970_2000_precip_mm_month']
def load(root,id):
    sha,m=SOURCES[id];p=root/f'github-actions-artifact-{id}.zip'
    if hashlib.sha256(p.read_bytes()).hexdigest()!=sha:raise ValueError("source SHA changed")
    with zipfile.ZipFile(p) as z:return pd.read_csv(z.open(m))
def frame(root):
    a=load(root,15069908329);b=load(root,14419407872)
    if len(a)!=72 or a[G].nunique()!=17 or len(b)!=165:raise ValueError("source scope drift")
    d=a.merge(b,on='TDWG_L3',how='left',validate='1:1')
    if len(d)!=72 or d[R].notna().sum()!=43 or (d[E]>=5).sum()!=37:raise ValueError("recorded Bombus scope drift")
    return d

def fit(d,y,w=W,b=B,eff=E,blocks=False,interaction=True,extra=()):
    cs=C+[eff]+list(extra);fields=[y,w,b]+cs;d=d.dropna(subset=fields).copy()
    if len(d)<8:return None
    def zr(x):
        v=rankdata(x);s=v.std();return (v-v.mean())/s if s>0 else np.zeros(len(v))
    x=zr(d[w]);z=zr(d[b]);vals=[np.ones(len(d)),x,z];names=['intercept','wind','Bombus']
    if interaction:vals.append(x*z);names.append('wind_x_Bombus')
    for c in cs:
        v=zr(d[c])
        if v.std()>0:vals.append(v);names.append(c)
    if blocks:
        for k in sorted(d[G].unique())[1:]:vals.append((d[G]==k).to_numpy(float));names.append(k)
    X=np.column_stack(vals);v=zr(d[y]);rank=np.linalg.matrix_rank(X);df=len(v)-rank
    if rank!=X.shape[1] or df<5 or np.std(v)==0:return None
    co=np.linalg.lstsq(X,v,rcond=None)[0]
    return {'n':len(d),'blocks':d[G].nunique(),'rank':int(rank),'residual_df':int(df),'coefficients':{k:float(co[names.index(k)]) for k in ['wind','Bombus']+(['wind_x_Bombus'] if interaction else [])}}

def model_set(d,y,w=W,b=B,eff=E,extra=()):
    out={}
    for blocks in (False,True):
        for inter in (False,True):
            key=('block' if blocks else 'adjusted')+('_interaction' if inter else '_additive');result=fit(d,y,w,b,eff,blocks,inter,extra)
            if result is not None:
                vals=[fit(d[d[G]!=g],y,w,b,eff,blocks,inter,extra) for g in sorted(d[G].unique())];vals=[v for v in vals if v is not None]
                result['LOBO']={k:{'min':min(v['coefficients'][k] for v in vals),'max':max(v['coefficients'][k] for v in vals),'positive':sum(v['coefficients'][k]>0 for v in vals),'n':len(vals)} for k in result['coefficients']} if vals else None
            out[key]=result
    return out

def within_block_product(d,y):
    """Separate centered-within-block product from cross-level products.
    A global rank product with block FE is NOT a purely within-block interaction.
    """
    d=d.dropna(subset=[y,W,B,*C,E]).copy()
    def zr(x):
        v=rankdata(x);s=v.std();return (v-v.mean())/s if s>0 else np.zeros(len(v))
    d['x']=zr(d[W]);d['z']=zr(d[B]);d['y']=zr(d[y])
    d['wx']=d.x-d.groupby(G).x.transform('mean')
    d['wz']=d.z-d.groupby(G).z.transform('mean')
    d['bx']=d.x-d.wx;d['bz']=d.z-d.wz
    X0=np.column_stack([np.ones(len(d)),d.wx,d.wz]+[zr(d[k]) for k in C+[E]]+[pd.get_dummies(d[G],drop_first=True).to_numpy(float)])
    outputs={}
    for kind,names,terms in [('within_only',['within_wind_x_within_Bombus'],[d.wx*d.wz]),('within_cross',['within_wind_x_within_Bombus','within_wind_x_between_Bombus','between_wind_x_within_Bombus'],[d.wx*d.wz,d.wx*d.bz,d.bx*d.wz])]:
        X=np.column_stack([X0]+terms);rank=np.linalg.matrix_rank(X);df=len(d)-rank
        if rank!=X.shape[1] or df<5:outputs[kind]=None;continue
        coef=np.linalg.lstsq(X,d.y,rcond=None)[0][-len(terms):]
        outputs[kind]={'n':len(d),'residual_df':int(df),'coefficients':dict(zip(names,map(float,coef)))}
    return outputs

def run(root):
    d=frame(root);results={}
    for cut in [1,5,10]:
        q=d[d[E]>=cut].copy();results[str(cut)]={'regions':len(q),'blocks':q[G].nunique(),'primary':model_set(q,Y),'native_denominator':model_set(q,Y2),'within_centered_product':within_block_product(q,Y)}
    q=d[d[E]>=5]
    results['sensitivity']={k:model_set(q,Y,w=w,b=b,eff=e) for k,w,b,e in [('gust10','gust10_secondary',B,E),('gust20','gust20_secondary',B,E),('record_effort',W,B,R),('strict_species',W,'GBIF_Bombus_strict_binomial_recorded_species',E),('uncertainty10km',W,'GBIF_Bombus_2grid_coord_uncertainty_le10km_sensitivity_species',E)]}
    return {'n_exploration':72,'n_with_positive_Bombus_records':43,'n_missing_not_absent':29,'NO_holdout_floral_outcomes':True,'NO_taxonomic_adjustment_in_this_regional_screen':True,'NO_causal_or_true_Bombus_suitability_claim':True,'results':results}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--archives',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=run(a.archives)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print("STAGE116_SOURCE_REGIONAL",json.dumps(d,sort_keys=True))
