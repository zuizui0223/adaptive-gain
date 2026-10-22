"""Source-locked, standalone meadow-day paired ST/BR visitor-role wind analysis.

Wind is observational; source role strings are not observed attacks. A positive
contrast does not identify predator avoidance or adaptive cue routing.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

SOURCE_SHA1={"watch":"fcd28cf0c9623fbfbc5619136334265a65f13dc4",
             "flowers":"c93b5496154245b9e94dc3362297ed354db3ebb6"}
KEYS=["SAMPLEDATE","PLOT_ID","WATCH"]
BEES={"social bee","solitary bee","halictine bee","semi-social bee",
      "halictine bee/semi-social bee","pollenivore bee"}
ENEMIES=("bee-parasitic","bee-predaceous","bee-predator",
         "pollinator-predaceous","predaceous onm bees",
         "kleptoparasitic bee","kloeptoparasitic bee")
OUTCOMES=["primary","bee","enemy"]

def load(source):
    root=Path(source)
    for k,v in SOURCE_SHA1.items():
        if hashlib.sha1((root/(k+".csv")).read_bytes()).hexdigest()!=v:
            raise ValueError("ORIGINAL_SOURCE_SHA1_MISMATCH:"+k)
    d=pd.read_csv(root/"watch.csv",dtype=str,keep_default_na=False)
    f=pd.read_csv(root/"flowers.csv",dtype=str,keep_default_na=False)
    if (len(d),len(f))!=(74942,23642):raise ValueError("ORIGINAL_SOURCE_ROW_COUNT_MISMATCH")
    return d,f

def presence_panel(d):
    d=d.copy()
    m=pd.to_numeric(d.MINUTE,errors="coerce")
    d["minute"]=m
    d["bad_positive"]=(d.PPI_STATUS=="1")&(~pd.to_numeric(d.NO_INT,errors="coerce").gt(0))
    meta=d.groupby(KEYS,sort=False).agg(
        min_count=("minute","nunique"),min_min=("minute","min"),min_max=("minute","max"),
        all_valid_minutes=("minute",lambda a:a.between(1,15).all()),
        wind_count=("WIND","nunique"),wind=("WIND","first"),
        wind_valid=("WIND",lambda a:a.isin(["ST","BR"]).all()),
        bad_positive=("bad_positive","any"),
        meadow=("MEADOW","first"),year=("YEAR","first"))
    mixed=d.groupby(KEYS+["MINUTE"],sort=False).PPI_STATUS.nunique()
    inconsistent=mixed.loc[mixed>1].index.droplevel("MINUTE").unique()
    good=(meta.min_count==15)&(meta.min_min==1)&(meta.min_max==15)&meta.all_valid_minutes&\
         (meta.wind_count==1)&meta.wind_valid&(~meta.bad_positive)&(~meta.index.isin(inconsistent))
    meta=meta.loc[good].copy()
    d=d.loc[d.set_index(KEYS).index.isin(meta.index)].copy()
    tp=d.VISSP_TYPE.str.lower().str.strip()
    d["bee"]=(d.PPI_STATUS=="1")&tp.isin(BEES)
    d["enemy"]=(d.PPI_STATUS=="1")&tp.apply(lambda a:any(k in a for k in ENEMIES))
    per_minute=d.groupby(KEYS+["MINUTE"],sort=False)[["bee","enemy"]].any()
    rate=per_minute.groupby(level=[0,1,2]).sum().astype(float)/15.
    panel=meta[["meadow","year","wind"]].join(rate).reset_index()
    if len(panel)!=1296 or set(panel.wind.unique())!={"ST","BR"}:
        raise ValueError("EXPECTED_1296_QUALIFIED_WATCHES")
    return panel

def flower_subset(panel,f):
    return panel.merge(f[KEYS].drop_duplicates(),on=KEYS,how="inner",validate="one_to_one")

def paired_days(panel):
    if panel.empty:return pd.DataFrame()
    g=panel.groupby(["meadow","SAMPLEDATE","wind"],sort=True)[["bee","enemy"]].mean()
    wide=g.unstack("wind")
    if ("bee","ST") not in wide or ("bee","BR") not in wide:return pd.DataFrame()
    wide=wide.dropna(subset=[("bee","ST"),("bee","BR")])
    ans=pd.DataFrame(index=wide.index)
    ans["bee_delta"]=wide["bee","BR"]-wide["bee","ST"]
    ans["enemy_delta"]=wide["enemy","BR"]-wide["enemy","ST"]
    ans["primary_delta"]=ans.enemy_delta-ans.bee_delta
    for k in ["bee","enemy"]:
        ans[k+"_ST"]=wide[k,"ST"]
        ans[k+"_BR"]=wide[k,"BR"]
    return ans.reset_index()

def holm(p):
    p=np.asarray(p,float);idx=np.argsort(p);v=np.zeros(len(p));threshold=0.
    for j,k in enumerate(idx):
        threshold=max(threshold,min(1.,(len(p)-j)*p[k]))
        v[k]=threshold
    return v.tolist()

def permute(panel,nrep=9999,seed=20261022):
    day=paired_days(panel)
    if len(day)==0:return {"status":"NO_PAIRED_DATES","days":0,"meadows":0,"outcomes":{}}
    matching=panel.merge(day[["meadow","SAMPLEDATE"]],on=["meadow","SAMPLEDATE"],how="inner",validate="many_to_one")
    rng=np.random.default_rng(seed)
    null=np.zeros((nrep,3),float)
    for _,g in matching.groupby(["meadow","SAMPLEDATE"],sort=True):
        yy=g[["enemy","bee"]].to_numpy(float)
        a=np.column_stack([yy[:,0]-yy[:,1],yy[:,1],yy[:,0]])
        b=int((g.wind=="BR").sum());n=len(g)
        if b<=0 or b>=n:raise AssertionError("BAD_PAIRED_WIND_DAY")
        draws=np.argsort(rng.random((nrep,n)),axis=1)[:,:b]
        s=a[draws].sum(axis=1)
        null+=s/b-(a.sum(axis=0)-s)/(n-b)
    null/=len(day)
    observed=day[["primary_delta","bee_delta","enemy_delta"]].mean().to_numpy(float)
    site=day.groupby("meadow")[["primary_delta","bee_delta","enemy_delta"]].sum()
    n_days=day.groupby("meadow").size().reindex(site.index).to_numpy()
    draw=rng.integers(len(site),size=(4999,len(site)))
    boot=site.to_numpy()[draw].sum(axis=1)/n_days[draw].sum(axis=1)[:,None]
    scores={};pvalues=[]
    for j,k in enumerate(OUTCOMES):
        p=(1+int(np.sum(np.abs(null[:,j])>=abs(observed[j])-1e-12)))/(nrep+1)
        pvalues.append(p)
        scores[k]={"delta":float(observed[j]),"p_two_sided":float(p),
           "site_bootstrap_95ci":[float(t) for t in np.quantile(boot[:,j],[.025,.975])]}
    for k,p in zip(OUTCOMES,holm(pvalues)):scores[k]["holm_q"]=float(p)
    return {"status":"OBSERVATIONAL_PAIR_TEST_ONLY","days":len(day),
            "meadows":int(day.meadow.nunique()),"watches":len(matching),
            "wind_watches":matching.wind.value_counts().to_dict(),
            "day_equal_rates":{k:{wind:float(day[k+"_"+wind].mean()) for wind in ["ST","BR"]}
                              for k in ["bee","enemy"]},
            "outcomes":scores}

def run(source,out,nrep=9999):
    d,f=load(source)
    p=presence_panel(d)
    variants={"main":p,"exact_flower_survey":flower_subset(p,f),
              "2014_2016":p.loc[p.year.isin(["2014","2015","2016"])]}
    answer={"source_doi":"10.6073/pasta/eec55cbc3dbfc56428629773737ab3e5",
       "original_source_sha1":SOURCE_SHA1,
       "scope":"OBSERVATIONAL_NATURAL_HISTORY_ROLE_CATEGORIES_NOT_DIRECT_SPECIES_INTERACTION",
       "n_complete_watches":len(p),"variants":{}}
    for k,v in variants.items():
        r=permute(v,nrep)
        answer["variants"][k]=r
        print("DIRECT_WIND_RESULT",k,json.dumps(r),flush=True)
    # Lock the expected source cohort, distinct from a null p-value conclusion.
    target={"main":(92,13,578),"exact_flower_survey":(57,13,313),
            "2014_2016":(73,12,511)}
    for k,(n,m,w) in target.items():
        v=answer["variants"][k]
        if (v["days"],v["meadows"],v["watches"])!=(n,m,w):
            raise ValueError("REGISTERED_SOURCE_ELIGIBILITY_CHANGED:"+k)
    answer["promotion_gate"]="NO_GO" if answer["variants"]["main"]["outcomes"]["primary"]["holm_q"]>=.05 else "CHECK_SENSITIVITY"
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    (out/"summary.json").write_text(json.dumps(answer,indent=2,ensure_ascii=False))
    print("ANDREWS_ST_BR_ROLE_ANALYSIS_COMPLETE",json.dumps({"main_days":92,"source_watches":1296,"gate":answer["promotion_gate"]}),flush=True)
    return answer

if __name__=="__main__":
    cli=argparse.ArgumentParser()
    cli.add_argument("--source-dir",required=True)
    cli.add_argument("--out",default="andrews_role_wind")
    cli.add_argument("--reps",type=int,default=9999)
    args=cli.parse_args()
    run(args.source_dir,args.out,args.reps)
