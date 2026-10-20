"""PoMS cross-site out-of-sample test of flower target × month structure.

Outcome: guild-specific counts including ZERO at a surveyed target flower.
Controls: site-held-out evaluation, observed target, month, year, habitat,
recording class, flower amount/units, weather. Critically, NEVER treat an
unsurveyed flower as a zero or infer individual sensory/fitness routeability.
"""
from __future__ import annotations
import argparse, hashlib, io, json, math, urllib.request, warnings, zipfile, platform
import sklearn, scipy
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.linalg import lstsq
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
SOURCE_CSV_SHA256={
    "1km":"29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52",
    "public":"bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c"}

def original_source():
    req=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-original-PoMS-site-HO-v1.0"})
    with urllib.request.urlopen(req,timeout=70) as h:b=h.read()
    if not zipfile.is_zipfile(io.BytesIO(b)):raise RuntimeError("EIDC_NOT_ZIP")
    return b,zipfile.ZipFile(io.BytesIO(b))

def load(z,design):
    source=z.read(CSV[design])
    if hashlib.sha256(source).hexdigest()!=SOURCE_CSV_SHA256[design]:
        raise ValueError("SOURCE_CSV_CHANGED: independent review required")
    try:source.decode("utf-8");encoding="utf-8"
    except UnicodeDecodeError:encoding="latin-1"
    df=pd.read_csv(io.BytesIO(source),encoding=encoding,low_memory=False)
    if df.sample_id.isna().any() or df.sample_id.duplicated().any():
        raise ValueError("MISSING_OR_DUPLICATED_SAMPLE_ID")
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
    columns=list(CATEGORICAL)
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
    if interaction:
        joint=OneHotEncoder(handle_unknown="ignore",sparse_output=False,dtype=np.float64)
        za=joint.fit_transform(train[["target_month"]].astype(str))
        zb=joint.transform(test[["target_month"]].astype(str))
        ba=np.column_stack([np.ones(len(train)),aa.toarray()])
        bt=np.column_stack([np.ones(len(test)),bb.toarray()])
        # Remove the training baseline span: adding redundant main-effect
        # columns under ridge must not masquerade as a plant-month interaction.
        projection=lstsq(ba,za,cond=1e-10,lapack_driver="gelsd")[0]
        za=za-ba@projection;zb=zb-bt@projection
        za[np.abs(za)<1e-12]=0.;zb[np.abs(zb)<1e-12]=0.
        aa=sparse.hstack([aa,sparse.csr_matrix(za)],format="csr")
        bb=sparse.hstack([bb,sparse.csr_matrix(zb)],format="csr")
    return aa,bb

def score(y,pred):
    p=np.asarray(pred,dtype=float);y=np.asarray(y,dtype=float)
    if (p.shape!=y.shape or not np.isfinite(p).all() or (p<=0).any()
            or not np.isfinite(y).all() or (y<0).any()):
        raise ValueError("finite nonnegative counts and positive predictions required")
    p=np.maximum(p,1e-8)
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

def fit_eval(df,parts,guild,mode,alpha=ALPHA,feature_cache=None):
    if mode not in ("floral_covariate","floral_offset") or alpha<=0:
        raise ValueError("invalid exposure mode or nonpositive penalty")
    all_test=np.concatenate([np.asarray(te,dtype=int) for tr,te in parts])
    if len(all_test)!=len(df) or not np.array_equal(np.sort(all_test),np.arange(len(df))):
        raise ValueError("test folds must cover every row exactly once")
    for tr,te in parts:
        if set(df.iloc[tr].site)&set(df.iloc[te].site):
            raise ValueError("site leakage")
    losses_a=np.empty(len(df));losses_b=np.empty(len(df))
    predictions_a=np.empty(len(df));predictions_b=np.empty(len(df))
    fold_id=np.full(len(df),-1,dtype=int);iterations=[];unknown=0
    for fi,(tr,te) in enumerate(parts):
        fold_id[te]=fi
        train=df.iloc[tr];test=df.iloc[te]
        unknown+=int((~test.target_month.isin(train.target_month)).sum())
        yy=train[guild].to_numpy(float)
        if yy.sum()<=0:raise RuntimeError("NO_POSITIVE_TRAIN_RESPONSE")
        exposure=train.flowers.to_numpy(float)
        ex_test=test.flowers.to_numpy(float)
        for interaction,out in ((False,losses_a),(True,losses_b)):
            X,Y=features(train,test,interaction,mode) if feature_cache is None else feature_cache[(fi,interaction)]
            # Weighted-rate deviance is normalized by sum(exposure), not n.
            # alpha/mean(exposure) preserves the declared count-scale penalty
            # and predictions under a global change in exposure units.
            fit_alpha=alpha/float(exposure.mean()) if mode=="floral_offset" else alpha
            reg=PoissonRegressor(alpha=fit_alpha,max_iter=2000,tol=1e-9)
            with warnings.catch_warnings():
                warnings.simplefilter("error",ConvergenceWarning)
                if mode=="floral_offset":
                    # Weighted-rate representation of a Poisson count model
                    # with fixed log(exposure) offset.
                    reg.fit(X,yy/exposure,sample_weight=exposure)
                    predicted=reg.predict(Y)*ex_test
                else:
                    reg.fit(X,yy)
                    predicted=reg.predict(Y)
            if interaction:predictions_b[te]=predicted
            else:predictions_a[te]=predicted
            iterations.append(int(reg.n_iter_))
            out[te]=score(test[guild].to_numpy(float),predicted)
    perrow=losses_a-losses_b
    audit=pd.DataFrame({"site":df.site,"fold":fold_id,"baseline_nll":losses_a,
                        "interaction_nll":losses_b,"delta":perrow})
    grouped=audit.groupby("site",sort=True).agg(
        delta=("delta","mean"),baseline=("baseline_nll","mean"),
        interaction=("interaction_nll","mean"),fold=("fold","first"),n=("delta","size"))
    sites=grouped.delta
    fold_deltas=grouped.groupby("fold").delta.mean()
    serialized=[]
    for sid,r in grouped.iterrows():
        serialized.append({"site_hash":hashlib.sha256(str(sid).encode()).hexdigest()[:16],
                           "fold":int(r['fold']),"surveys":int(r['n']),
                           "baseline_nll":float(r['baseline']),
                           "interaction_nll":float(r['interaction']),"delta":float(r['delta'])})
    return {"guild":guild,"alpha_count_scale":alpha,
        "mean_baseline_nll":float(losses_a.mean()),
        "site_equal_baseline_nll":float(grouped.baseline.mean()),
        "site_equal_relative_improvement":float(sites.mean()/grouped.baseline.mean()),
        "fold_site_equal_deltas":[float(x) for x in fold_deltas],
        "positive_folds":int((fold_deltas>0).sum()),
        "unknown_target_month_test_rows":unknown,
        "maximum_solver_iterations":max(iterations),"fit_count":len(iterations),
        "site_scores":serialized,
        "mean_interaction_nll":float(losses_b.mean()),
        "pooled_delta_positive_is_better":float(perrow.mean()),
        "site_equal_delta_positive_is_better":float(sites.mean()),
        "site_equal_ci95":site_ci(sites.to_numpy()),
        "positive_site_fraction":float((sites>0).mean()),
        "site_n":int(len(sites)),"total_observed_guild_visits":int(df[guild].sum())}

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--out",default="poms_holdout_results")
    parser.add_argument("--designs",default="1km,public")
    parser.add_argument("--alpha",type=float,default=ALPHA)
    args=parser.parse_args();dest=Path(args.out);dest.mkdir(exist_ok=True,parents=True)
    raw,z=original_source()
    result={"analysis":"out-of-site predictive interaction comparison, NOT causal cue choice",
      "status":"EXPLORATORY_POST_MATCHED_SCHEMA","source":URL,
      "sha256_original_zip":hashlib.sha256(raw).hexdigest(),
      "versions":{"python":platform.python_version(),"numpy":np.__version__,
                  "pandas":pd.__version__,"scipy":scipy.__version__,"sklearn":sklearn.__version__},
      "uncertainty":"exploratory bootstrap of fixed out-of-fold site scores; not full refit or spatial/block uncertainty; unadjusted across 10 guilds",
      "model":{"alpha":args.alpha,"folds":5,"group":"site (not rows)",
        "baseline":"plant + month + year + context + weather + flower exposure",
        "interaction":"baseline + training-only baseline-orthogonal plant:month block",
        "primary_exposure":"log1p floral_unit_count as fitted covariate",
        "sensitivity":"floral_unit_count as fixed linear Poisson offset",
        "penalty_scale":"count-scale alpha; weighted-rate alpha is alpha/mean(training exposure)",
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
            cache={(fi,inter):features(w.iloc[tr],w.iloc[te],inter,mode)
                   for fi,(tr,te) in enumerate(splits) for inter in (False,True)}
            rows=[]
            for g in GUILDS:
                r=fit_eval(w,splits,g,mode,alpha=args.alpha,feature_cache=cache)
                pd.DataFrame(r.pop("site_scores")).to_csv(dest/f"{design}_{mode}_{g}_site_scores.csv",index=False)
                rows.append(r)
            rr[mode]=rows
            print("SITE_HO_RESULT",design,mode,json.dumps(rows),flush=True)
        result["designs"][design]={"status":"COMPLETE_EXPLORATORY","quality":q,
            "support":support,"final_surveys":len(w),"results":rr}
    (dest/"summary.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print("SITE_HO_ANALYSIS_COMPLETE",flush=True)
if __name__=="__main__":main()
