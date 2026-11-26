#!/usr/bin/env python3
"""Stage119: same-budget conditional acquisition on original compiled floral rewards.
Predictions are for across-species compiled production, not actual standing crop,
bee decisions, sensory acquisition cost, or fitness. Outer genus/family holdout
is predictive, not phylogenetic inference. No geography holdout data used.
"""
from __future__ import annotations
import argparse,hashlib,json,math,re,sys
from collections import Counter
from itertools import combinations
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage118"))
from reward_source_admission import members,tables,load_archive,canon
HASHES={"morphology":"e42b1d0a8a0b6f332e6843c4a16bd5af9c3afa6f0270cd9b9a867df7ad7c3bd3",
"nectar":"6f25de3ca8057581b823d15ad31acf23291071c9be95c17bd65bced2b0245441",
"pollen":"bce3e448e44c175ad95409ac01a6bff955f331a2e0cd895157b32256bb2f0556"}
HUES={"white":"white|whitish|cream|ivory","yellow":"yellow|yellowish|golden","purple":"purple|purplish|violet|violaceous|lilac|lavender|mauve","blue":"blue|bluish|azure|cyan","pink":"pink|pinkish|rose|rosy|salmon","red":"red|reddish|scarlet|crimson|maroon|carmine","orange":"orange|orangish|copper","green":"green|greenish","brown":"brown|brownish","black":"black|blackish","gray":"grey|gray|greyish|grayish"}
STATES=("radial","bilateral")
CANDIDATES=("tube","shape","hue")
def species(x):
    return canon(str(x or "").replace("_"," "))
def cat(x):
    s=str(x or "").strip().casefold()
    return None if s in {"","na","n/a","nan","none","unknown","?","-"} else s
def number(x):
    try:v=float(x)
    except (ValueError,TypeError):return np.nan
    return v if math.isfinite(v) else np.nan
def unique(x):
    vals=set(x.dropna())
    return next(iter(vals)) if len(vals)==1 else None
def read_table(raw,typ):
    ts=tables(raw,typ)
    if len(ts)!=1:raise ValueError("unexpected source sheet count "+typ)
    _,rows,_=ts[0]
    header=[str(v or "").strip() for v in rows[3]]
    req={"morphology":["Species","Genus","Family","Tube_length","Floral_shape_class","Symmetry","Orientation"],
         "nectar":["Species","Genus","Family","Nectar (µg/day)"],
         "pollen":["Species","Genus","Family","log No. pollen grains"]}[typ]
    if any(header.count(k)!=1 for k in req):raise ValueError(f"original source header drift {typ}: {header}")
    selected=req+["Source"] if "Source" in header else req
    idx=[header.index(k) for k in selected]
    d=pd.DataFrame([{k:r[j] if j<len(r) else None for k,j in zip(selected,idx)} for r in rows[4:]])
    d["species"]=d.Species.map(species);d["genus"]=d.Genus.map(cat);d["family"]=d.Family.map(cat)
    valid=d.species.notna()&d.genus.notna()&d.family.notna()&(d.species.str.split().str[0]==d.genus)
    audit={"source_data_rows":len(d),"strict_species_rows":int(valid.sum()),"strict_species":int(d.loc[valid,"species"].nunique()),"excluded_name_or_taxonomy_rows":int((~valid).sum())}
    d=d[valid].copy()
    if typ=="morphology":
        d["tube_raw"]=d.Tube_length.map(number)
        d.loc[d.tube_raw<0,"tube_raw"]=np.nan
        d["shape"]=d.Floral_shape_class.map(cat)
        d["symmetry"]=d.Symmetry.map(cat).replace({"actinomorphic":"radial","zygomorphic":"bilateral","radial symmetry":"radial","bilateral symmetry":"bilateral"})
        d.loc[~d.symmetry.isin(STATES),"symmetry"]=None
        d["orientation"]=d.Orientation.map(cat)
        audit["source_symmetry_states"]=dict(Counter(str(x) for x in d.Symmetry))
        audit["source_shape_states"]=dict(Counter(str(x) for x in d.Floral_shape_class))
        out=d.groupby("species",sort=True).agg(genus=("genus",unique),family=("family",unique),tube_raw=("tube_raw","mean"),shape=("shape",unique),symmetry=("symmetry",unique),orientation=("orientation",unique),morphology_records=("species","size"))
        out["tube"]=np.log1p(out.tube_raw)
    else:
        column="Nectar (µg/day)" if typ=="nectar" else "log No. pollen grains"
        d["value"]=d[column].map(number)
        # Nectar is sugar mass: nonpositive values cannot enter log model.
        # Pollen is already logged by the original authors: no second log.
        audit["numeric_missing"]=int(d.value.isna().sum())
        audit["numeric_nonpositive"]=int((d.value<=0).sum())
        d=d[d.value.notna() & ((d.value>0) if typ=="nectar" else np.isfinite(d.value))]
        out=d.groupby("species",sort=True).agg(genus=("genus",unique),family=("family",unique),reward_raw=("value","mean"),reward_records=("value","size"))
        out["target"]=np.log10(out.reward_raw) if typ=="nectar" else out.reward_raw
    out=out.dropna(subset=["genus","family"]).reset_index()
    audit["admitted_unique_species"]=len(out)
    audit["multiple_source_rows_species"]=int((out.iloc[:,out.columns.get_loc("morphology_records" if typ=="morphology" else "reward_records")]>1).sum())
    return out,audit

def hue(row):
    text=" ".join(str(row.get(k) or "") for k in ("flower colour","petal colour","corolla colour")).lower()
    found=[k for k,v in HUES.items() if re.search(r"(?<![a-z])(?:"+v+r")(?![a-z])",text)]
    return found[0] if len(found)==1 else "multiple_hue_words" if len(found)>1 else None

def load_sources(path,archives):
    raw=members(path)
    if any(hashlib.sha256(raw[k]).hexdigest()!=HASHES[k] for k in HASHES):
        raise ValueError("Stage118 pinned original author member SHA changed")
    tables_out={};audit={}
    for k,v in raw.items():tables_out[k],audit[k]=read_table(v,k)
    n=load_archive(archives,"nhm")
    n["species"]=n.taxon.map(species);n["hue"]=n.apply(hue,axis=1)
    h=n.dropna(subset=["species"]).groupby("species").hue.agg(unique).reset_index()
    m=tables_out["morphology"].merge(h,on="species",how="left",validate="1:1")
    e=load_archive(archives,"visits");v=load_archive(archives,"voc")
    E=set(e.Original_plant_accepted_name_literal.map(species).dropna())
    V=set(v.source_species_canonical_binomial_if_valid.map(species).dropna())
    P=set(e.loc[e.Stage67_direct_petal_spectra_name_match.eq(1),"Original_plant_accepted_name_literal"].map(species).dropna())
    result={}
    for reward in ("nectar","pollen"):
        rr=tables_out[reward]
        z=m.merge(rr,on="species",suffixes=("","_reward"),validate="1:1")
        bad=(z.genus!=z.genus_reward)|(z.family!=z.family_reward)
        audit[reward]["exact_morphology_overlap"]=len(z)
        audit[reward]["taxonomy_conflicts"]=int(bad.sum())
        z=z[~bad].copy()
        audit[reward]["morphology_tube_symmetry_complete"]=int(z[["tube","symmetry"]].notna().all(axis=1).sum())
        S=set(rr.species);audit[reward]["existing_source_overlap"]={"NHM":len(S&set(h.species)),"EuPP":len(S&E),"VOC":len(S&V),"EuPP_VOC":len(S&E&V),"EuPP_petal_spectrum":len(S&P),"EuPP_petal_VOC":len(S&E&P&V)}
        result[reward]=z.reset_index(drop=True)
    audit["both_rewards_species"]=len(set(tables_out["nectar"].species)&set(tables_out["pollen"].species))
    return result,audit

def predict(train,test,features):
    if not features:return np.repeat(float(train.target.mean()),len(test))
    num=[f for f in features if f=="tube"]
    catcols=[f for f in features if f!="tube"]
    trans=ColumnTransformer([("numeric",StandardScaler(),num),("categorical",OneHotEncoder(handle_unknown="ignore",sparse_output=False),catcols)],remainder="drop")
    model=make_pipeline(trans,Ridge(alpha=5.0));model.fit(train[list(features)],train.target)
    return model.predict(test[list(features)])

def routed(train,test,cues):
    out=np.empty(len(test))
    for state in STATES:
        tr=train[train.symmetry==state];mask=(test.symmetry==state).to_numpy();te=test.loc[mask]
        if len(te)==0:continue
        if len(tr)==0:out[mask]=float(train.target.mean())
        elif len(tr)<8:out[mask]=float(tr.target.mean())
        else:out[mask]=predict(tr,te,[cues[state]])
    return out

def inner_select(train,group,candidates):
    # Both policies get the same first cue, same branch-specific estimator,
    # same training folds and exactly one more cue. Choose only in train CV.
    k=min(3,train[group].nunique())
    if k<2:raise ValueError("insufficient inner groups")
    loss={c:{s:0.0 for s in STATES} for c in candidates}
    pairs=list(combinations(("symmetry",)+tuple(candidates),2))
    pair_loss={p:0.0 for p in pairs}
    for i,j in GroupKFold(k).split(train,groups=train[group]):
        tr=train.iloc[i];te=train.iloc[j]
        for c in candidates:
            pred=routed(tr,te,{s:c for s in STATES});err=(pred-te.target.to_numpy())**2
            for s in STATES:loss[c][s]+=float(err[(te.symmetry==s).to_numpy()].sum())
        for p in pairs:
            pred=predict(tr,te,p);pair_loss[p]+=float(np.sum((pred-te.target.to_numpy())**2))
    fixed=min(candidates,key=lambda c:(sum(loss[c].values()),c))
    adaptive={s:min(candidates,key=lambda c:(loss[c][s],c)) for s in STATES}
    best_pair=min(pairs,key=lambda p:(pair_loss[p],p))
    return fixed,adaptive,best_pair

def evaluate(d,group,candidates):
    d=d.reset_index(drop=True)
    if len(d)<60 or d[group].nunique()<10 or min(d.symmetry.value_counts().reindex(STATES,fill_value=0))<12:
        return {"status":"insufficient_support","n":len(d),"groups":int(d[group].nunique()),"states":{str(k):int(v) for k,v in d.symmetry.value_counts().items()}}
    names=["no_cue","symmetry_only","fixed_routed","adaptive_routed","fixed_any_pair"]
    preds={k:np.empty(len(d)) for k in names};folds=[]
    for fold,(i,j) in enumerate(GroupKFold(5).split(d,groups=d[group])):
        tr=d.iloc[i];te=d.iloc[j]
        assert not set(tr[group])&set(te[group])
        f,a,p=inner_select(tr,group,candidates)
        vals={"no_cue":predict(tr,te,[]),"symmetry_only":predict(tr,te,["symmetry"]),
              "fixed_routed":routed(tr,te,{s:f for s in STATES}),
              "adaptive_routed":routed(tr,te,a),"fixed_any_pair":predict(tr,te,p)}
        for k,v in vals.items():preds[k][j]=v
        foldloss={k:float(np.mean((v-te.target.to_numpy())**2)) for k,v in vals.items()}
        folds.append({"fold":fold,"n_test":len(te),"heldout_groups":int(te[group].nunique()),"fixed_second":f,"adaptive_second":a,"fixed_any_pair":list(p),"MSE":foldloss})
    err={k:(v-d.target.to_numpy())**2 for k,v in preds.items()}
    mse={k:float(np.mean(v)) for k,v in err.items()}
    # Equal-fold and species-weighted summary. Cluster bootstrap of fixed
    # out-of-fold paired losses is a descriptive sensitivity, not a CI for
    # the entire re-trained algorithm or independent study replication.
    rng=np.random.default_rng(20261126);groups=d[group].unique()
    delta=err["fixed_routed"]-err["adaptive_routed"]
    stat=d.assign(delta=delta).groupby(group).delta.agg(["sum","count"])
    idx=rng.integers(0,len(stat),size=(1999,len(stat)))
    sim=stat["sum"].to_numpy()[idx].sum(axis=1)/stat["count"].to_numpy()[idx].sum(axis=1)
    return {"status":"estimated_exploratory","n":len(d),"groups":len(groups),"states":{str(k):int(v) for k,v in d.symmetry.value_counts().items()},"mse":mse,"rmse":{k:math.sqrt(v) for k,v in mse.items()},
        "adaptive_relative_mse_gain_vs_routed_fixed":1-mse["adaptive_routed"]/mse["fixed_routed"],
        "adaptive_relative_mse_gain_vs_any_fixed_pair":1-mse["adaptive_routed"]/mse["fixed_any_pair"],
        "paired_fixed_minus_adaptive_mse":float(delta.mean()),"descriptive_group_resample_delta_95":list(map(float,np.quantile(sim,[.025,.975]))),
        "positive_outer_folds":sum(f["MSE"]["fixed_routed"]>f["MSE"]["adaptive_routed"] for f in folds),"folds":folds}
def main():
    p=argparse.ArgumentParser();p.add_argument("--source",required=True,type=Path);p.add_argument("--archives",required=True,type=Path);p.add_argument("--out",required=True,type=Path);a=p.parse_args()
    data,audit=load_sources(a.source,a.archives)
    out={"source_member_sha256":HASHES,"source_audit":audit,"primary_budget":"symmetry then one of tube/shape; identical two-group cost proxy, no actual acquisition costs","comparators":"branch-matched fixed second feature and best inner-CV unrestricted fixed pair","models":"fixed alpha 5 Ridge, group CV 5 outer / 3 inner; fold-local transforms and policy choice","no_causal_receiver_or_fitness_claim":True,"no_geographic_holdout":True,"results":{}}
    for reward,z in data.items():
        out["results"][reward]={}
        # Separate identical-cohort comparisons; missingness never substitutes
        # for a cue. No best-panel claim based on the heldout results.
        for name,candidates in [("morphology_primary",("tube","shape")),("hue_extension",("tube","shape","hue")),("tube_hue_secondary",("tube","hue"))]:
            d=z.dropna(subset=["target","symmetry","genus","family",*candidates])
            out["results"][reward][name]={g:evaluate(d,g,candidates) for g in ("genus","family")}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STAGE119_REWARD_PREDICTIVE_BUDGET",json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
