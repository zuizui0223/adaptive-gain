"""PoMS cross-site out-of-sample test of flower target × month structure.

Outcome: guild-specific counts including ZERO at a surveyed target flower.
Controls: site-held-out evaluation, observed target, month, year, habitat,
recording class, flower amount/units, weather. Critically, NEVER treat an
unsurveyed flower as a zero or infer individual sensory/fitness routeability.
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, urllib.request, warnings, zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.special import gammaln
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import PoissonRegressor
from sklearn.exceptions import ConvergenceWarning

URL="https://data-package.ceh.ac.uk/data/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip"
CSV={"1km":"data/ukpoms_1kmfitcountdata_2017-2023.csv",
     "public":"data/ukpoms_publicfitcountdata_2017-2023.csv"}
GUILDS=("bumblebees","honeybees","solitary_bees","wasps","hoverflies",
"other_flies","butterflies_moths","beetles","insects_small","insects_other")
CATEGORICAL=("target","month","year","country","recorder_type","habitat_type",
 "flower_cover","flower_context","floral_unit","cloud_cover","sunshine","wind_speed")
ALPHA=0.25
SEED=20261019

def original_source():
    req=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-original-PoMS-site-HO-v1.0"})
    with urllib.request.urlopen(req,timeout=70) as h:b=h.read()
    if not zipfile.is_zipfile(io.BytesIO(b)):raise RuntimeError("EIDC_NOT_ZIP")
    return b,zipfile.ZipFile(io.BytesIO(b))

def load(z,design):
    source=z.read(CSV[design])
    try:source.decode("utf-8");encoding="utf-8"
    except UnicodeDecodeError:encoding="latin-1"
    df=pd.read_csv(io.BytesIO(source),encoding=encoding,low_memory=False)
    target=df.target_flower_corrected.astype("string").str.strip()
    original=df.target_flower.astype("string").str.strip()
    target=target.mask(target.eq("")).fillna(original.mask(original.eq("")))
    dates=pd.to_datetime(df.date,dayfirst=True,errors="coerce")
    flowers=pd.to_numeric(df.floral_unit_count,errors="coerce")
    is_other=target.str.contains("Other - please describe",case=False,na=True)
    all_counts=df[list(GUILDS)+["all_insects_total"]].apply(pd.to_numeric,errors="coerce")
    valid=((~is_other) &target.notna()&dates.notna()&flowers.gt(0)&
        all_counts.notna().all(axis=1)&all_counts.ge(0).all(axis=1)&
        np.isclose(all_counts[list(GUILDS)].sum(axis=1),all_counts.all_insects_total))
    site=df["location_code"].astype("string") if design=="1km" else df["x1km_square"].astype("string")
    valid=valid&site.notna()
    if design=="1km":valid=valid&dates.dt.month.between(5,8)
    else:valid=valid&dates.dt.month.between(4,9)
    w=df.loc[valid,list(set(CATEGORICAL)-{"target","month","year"})].copy()
    w["site"]=site[valid].astype(str)
    w["target"]=target[valid].astype(str)
    w["month"]=dates.dt.month[valid].astype(int).astype(str)
    w["year"]=dates.dt.year[valid].astype(int).astype(str)
    w["flowers"]=flowers[valid].astype(float)
    w["target_month"]=w["target"]+" × "+w["month"]
    for col in GUILDS:w[col]=all_counts.loc[valid,col].astype(float)
    w.reset_index(drop=True,inplace=True)
    return w,{"original_rows":len(df),"valid_named_target_surveys":len(w),
             "removed":int(len(df)-len(w)),"sha256_csv":hashlib.sha256(source).hexdigest(),
             "initial_sites":int(w.site.nunique()),"initial_targets":int(w.target.nunique())}

def filter_common_support(w,design):
    # This restricts the model to repeatedly observed plant-month exposures;
    # no inference about plant-month combinations that were never surveyed.
    n_min,sites_min=(12,4) if design=="1km" else (30,10)
    def common_pairs(df):
        support=df.groupby(["target","month"]).agg(n=("site","size"),sites=("site","nunique"))
        return support.index[(support.n>=n_min)&(support.sites>=sites_min)]
    pairs=common_pairs(w)
    mask=pd.MultiIndex.from_frame(w[["target","month"]]).isin(pairs)
    x=w.loc[mask].copy()
    plant_months=x.groupby("target").month.nunique()
    x=x.loc[x.target.isin(plant_months[plant_months>=2].index)].copy()
    return x.reset_index(drop=True),{"n_min_target_month":n_min,"sites_min_target_month":sites_min,
         "eligible_target_month_cells":int(x.groupby(["target","month"]).ngroups),
         "eligible_targets":int(x.target.nunique()),"eligible_sites":int(x.site.nunique())}

def features(train,test,interaction,mode):
    columns=list(CATEGORICAL)+(["target_month"] if interaction else [])
    train_cat=train[columns].fillna("not_recorded").astype(str)
    test_cat=test[columns].fillna("not_recorded").astype(str)
    encoder=OneHotEncoder(handle_unknown="ignore",sparse_output=True,dtype=np.float64)
    aa=encoder.fit_transform(train_cat);bb=encoder.transform(test_cat)
    if mode=="floral_covariate":
        raw_train=np.log1p(train.flowers.to_numpy(float))
        raw_test=np.log1p(test.flowers.to_numpy(float))
        mean=float(raw_train.mean());sd=float(raw_train.std()) or 1.
        aa=sparse.hstack([aa,sparse.csr_matrix(((raw_train-mean)/sd).reshape(-1,1))],format="csr")
        bb=sparse.hstack([bb,sparse.csr_matrix(((raw_test-mean)/sd).reshape(-1,1))],format="csr")
    return aa,bb

def score(y,pred):
    p=np.maximum(np.asarray(pred,dtype=float),1e-8)
    y=np.asarray(y,dtype=float)
    return p-y*np.log(p)+gammaln(y+1)

def folds(df,k=5):
    group=df.site.astype(str)
    if group.nunique()<k:raise ValueError("not enough unique sites for group holdout")
    parts=list(GroupKFold(n_splits=k).split(df,np.zeros(len(df)),group))
    for train,test in parts:
        if set(group.iloc[train]) & set(group.iloc[test]):raise AssertionError("site leakage")
    return parts

def site_ci(values,seed=SEED,reps=1000):
    vals=np.asarray(values,dtype=float)
    if len(vals)<5:return [None,None]
    rng=np.random.default_rng(seed)
    bs=vals[rng.integers(len(vals),size=(reps,len(vals)))].mean(axis=1)
    return [float(v) for v in np.quantile(bs,[.025,.975])]

def fit_eval(df,parts,guild,mode):
    losses_a=np.empty(len(df));losses_b=np.empty(len(df))
    for tr,te in parts:
        train=df.iloc[tr];test=df.iloc[te]
        yy=train[guild].to_numpy(float)
        if yy.sum()<=0:raise RuntimeError("NO_POSITIVE_TRAIN_RESPONSE")
        exposure=train.flowers.to_numpy(float)
        ex_test=test.flowers.to_numpy(float)
        for interaction,out in ((False,losses_a),(True,losses_b)):
            X,Y=features(train,test,interaction,mode)
            reg=PoissonRegressor(alpha=ALPHA,max_iter=400,tol=1e-6)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore",ConvergenceWarning)
                if mode=="floral_offset":
                    # Weighted-rate representation of a Poisson count model
                    # with fixed log(exposure) offset.
                    reg.fit(X,yy/exposure,sample_weight=exposure)
                    predicted=reg.predict(Y)*ex_test
                else:
                    reg.fit(X,yy)
                    predicted=reg.predict(Y)
            out[te]=score(test[guild].to_numpy(float),predicted)
    perrow=losses_a-losses_b
    sites=pd.DataFrame({"site":df.site,"delta":perrow}).groupby("site").delta.mean()
    return {"guild":guild,"mean_baseline_nll":float(losses_a.mean()),
        "mean_interaction_nll":float(losses_b.mean()),
        "pooled_delta_positive_is_better":float(perrow.mean()),
        "site_equal_delta_positive_is_better":float(sites.mean()),
        "site_equal_ci95":site_ci(sites.to_numpy()),
        "positive_site_fraction":float((sites>0).mean()),
        "site_n":int(len(sites)),"total_observed_guild_visits":int(df[guild].sum())}

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--out",default="poms_holdout_results")
    parser.add_argument("--designs",default="1km,public")
    args=parser.parse_args();dest=Path(args.out);dest.mkdir(exist_ok=True,parents=True)
    raw,z=original_source()
    result={"analysis":"out-of-site predictive interaction comparison, NOT causal cue choice",
      "status":"EXPLORATORY_POST_MATCHED_SCHEMA","source":URL,
      "sha256_original_zip":hashlib.sha256(raw).hexdigest(),
      "model":{"alpha":ALPHA,"folds":5,"group":"site (not rows)",
        "baseline":"plant + month + year + context + weather + flower exposure",
        "interaction":"baseline + categorical plant:month",
        "primary_exposure":"log1p floral_unit_count as fitted covariate",
        "sensitivity":"floral_unit_count as fixed linear Poisson offset",
        "interpretation":"out-of-site held-out Poisson log likelihood; no unsurveyed zeros"},
      "designs":{}}
    for design in args.designs.split(","):
        w,q=load(z,design)
        w,support=filter_common_support(w,design)
        print("SITE_HO_SUPPORT",design,json.dumps({**q,**support,"final_surveys":len(w)}),flush=True)
        if len(w)<150 or w.site.nunique()<10 or w.target.nunique()<2:
            result["designs"][design]={"status":"NO_GO_WEAK_COMMON_SUPPORT","quality":q,"support":support}
            continue
        splits=folds(w)
        rr={}
        for mode in ("floral_covariate","floral_offset"):
            rows=[]
            for g in GUILDS:
                r=fit_eval(w,splits,g,mode)
                rows.append(r)
            rr[mode]=rows
            print("SITE_HO_RESULT",design,mode,json.dumps(rows),flush=True)
        result["designs"][design]={"status":"COMPLETE_EXPLORATORY","quality":q,
            "support":support,"final_surveys":len(w),"results":rr}
    (dest/"summary.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print("SITE_HO_ANALYSIS_COMPLETE",flush=True)
if __name__=="__main__":main()
