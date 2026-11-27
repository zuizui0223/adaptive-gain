#!/usr/bin/env python3
"""Regional transport of compiled species reward information.

WCVP native range co-membership is not local coflowering, and the compiled
reward measurements are not local observations. Region predictions train
without ALL genera (or families) represented in the local test cohort.
No geographic holdout outcome joins; no causal wind or bee learning claims.
"""
from __future__ import annotations
import argparse,hashlib,json,math,sys,zipfile
from collections import Counter
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import rankdata,kendalltau
BASE=Path(__file__).resolve().parents[1]
for folder in ("floral_macro_stage87","floral_macro_stage116","floral_macro_stage119","floral_macro_stage120"):
    sys.path.insert(0,str(BASE/folder))
from global_native_floral_signal_tdwg3 import wcvp_regions,WCVP_SHA
from budgeted_reward import load_sources,predict,HASHES
from paired_reward_transfer import paired_data,paired_evaluate
from regional_marking_bombus import frame,W,B,E,G

REF_SHA="d2699b1fded51adab805b3657bff5434bbde19565686f2421fd348ab7dcea381"
REF_MEMBER="stage120_paired_reward.json"
COV=["source_ERA5_point_latitude","source_ERA5_1991_2020_mean_temperature_C","WorldClim_1970_2000_precip_mm_month"]
MIN_TEST=10
MIN_TEST_GENERA=5
MIN_TEST_FAMILIES=3
MIN_TRAIN=30
MIN_TRAIN_GROUPS=10
MIN_MACRO_REGIONS=30
MIN_MACRO_BLOCKS=10

def prior_check(archives,pair):
    p=archives/"github-actions-artifact-15089720778.zip"
    if hashlib.sha256(p.read_bytes()).hexdigest()!=REF_SHA:raise ValueError("Stage120 archive SHA drift")
    with zipfile.ZipFile(p) as z:d=json.loads(z.read(REF_MEMBER))
    if len(pair)!=82 or len(pair)!=d["paired_morphology_and_rewards_n"]:raise ValueError("paired cohort drift")
    for group in ("genus","family"):
        actual=paired_evaluate(pair,group)
        old=d["matched_cohort"][group]
        for reward in ("nectar","pollen"):
            for model,val in actual["outcomes"][reward]["mse"].items():
                if not math.isclose(val,old["outcomes"][reward]["mse"][model],rel_tol=0,abs_tol=1e-10):
                    raise ValueError("Stage120 original paired prediction drift")
    return True

def separate_data(z,reward):
    return z[["species","genus","family","tube","symmetry","target"]].dropna().rename(columns={"target":reward}).reset_index(drop=True)

def skill(y,pred,baseline):
    y=np.asarray(y,float);pred=np.asarray(pred,float);base=np.asarray(baseline,float)
    if len(y)<2 or not all(np.isfinite(a).all() for a in (y,pred,base)):raise ValueError("invalid source prediction arrays")
    denom=float(np.sum((y-base)**2));err=float(np.sum((y-pred)**2))
    y0=y-y.mean();p0=pred-pred.mean()
    den0=float(y0@y0);err0=float((y0-p0)@(y0-p0))
    tau=kendalltau(y,pred).statistic if np.ptp(y)>1e-12 and np.ptp(pred)>1e-12 else np.nan
    return {"mean_squared_error":err/len(y),"training_mean_baseline_mse":denom/len(y),
        "transfer_skill_vs_training_mean":1-err/denom if denom>1e-12 else None,
        "within_assemblage_pair_contrast_skill":1-err0/den0 if den0>1e-12 else None,
        "kendall_tau_b":float(tau) if np.isfinite(tau) else None,
        "test_reward_variance":den0/len(y)}

def region_test(d,local,group,rewards):
    te=d[d.species.isin(local)].copy()
    tr=d[~d[group].isin(te[group])].copy()
    out={"n_test":len(te),"test_genera":int(te.genus.nunique()),"test_families":int(te.family.nunique()),
         "n_train":len(tr),"train_groups":int(tr[group].nunique())}
    if len(te)<MIN_TEST or te.genus.nunique()<MIN_TEST_GENERA or te.family.nunique()<MIN_TEST_FAMILIES:
        return {**out,"status":"insufficient_local_cohort"},[]
    if len(tr)<MIN_TRAIN or tr[group].nunique()<MIN_TRAIN_GROUPS:
        return {**out,"status":"insufficient_disjoint_training"},[]
    if set(tr[group])&set(te[group]) or set(tr.species)&set(te.species):raise ValueError("regional lineage leakage")
    results={};rows=[]
    for reward in rewards:
        train=tr.assign(target=tr[reward]);test=te.assign(target=te[reward])
        p0=predict(train,test,[]);p=predict(train,test,["tube"])
        results[reward]=skill(test.target,p,p0)
        # Only derived aggregate predictive metrics are archived; not full
        # source trait/target rows. IDs are used in-memory for support counts.
        rows.extend({"species":sp,"reward":reward} for sp in test.species)
    out.update(status="estimated_exploratory",outcomes=results)
    if len(rewards)==2:
        for metric in ("transfer_skill_vs_training_mean","within_assemblage_pair_contrast_skill","kendall_tau_b"):
            a=results["nectar"][metric];b=results["pollen"][metric]
            out[metric+"_nectar_minus_pollen"]=a-b if a is not None and b is not None else None
    return out,rows

def zrank(x):
    a=rankdata(x);s=a.std()
    return (a-a.mean())/s if s>1e-12 else np.zeros(len(a))

def macro_fit(q,y,bee,blocks):
    terms=[W]+([B] if bee else [])
    controls=COV+["n_test"]+([E] if bee else [])
    z=q.dropna(subset=[y,*terms,*controls]).copy()
    # Not a region-IID significance analysis: scores reuse taxa.
    if len(z)<MIN_MACRO_REGIONS or z[G].nunique()<MIN_MACRO_BLOCKS:return None
    arr=[np.ones(len(z))]+[zrank(z[k]) for k in terms+controls]
    if blocks:arr.append(pd.get_dummies(z[G],drop_first=True).to_numpy(float))
    X=np.column_stack(arr);yr=zrank(z[y]);rank=np.linalg.matrix_rank(X)
    if rank!=X.shape[1] or len(z)-rank<8 or yr.std()<1e-12:return None
    a=np.linalg.lstsq(X,yr,rcond=None)[0]
    return {"n":len(z),"blocks":int(z[G].nunique()),"residual_df":int(len(z)-rank),"coefficients":dict(zip(terms,map(float,a[1:1+len(terms)])))}

def macro_screen(q,y,bee):
    sub=q[q[E]>=5].copy() if bee else q.copy()
    out={"eligible_score_regions":int(sub[y].notna().sum()),"eligible_blocks":int(sub.loc[sub[y].notna(),G].nunique())}
    for block in (False,True):
        k="block_adjusted" if block else "adjusted"
        fit=macro_fit(sub,y,bee,block);out[k]=fit
        if fit is not None:
            vals=[macro_fit(sub[sub[G]!=g],y,bee,block) for g in sorted(sub[G].unique())]
            vals=[v for v in vals if v is not None]
            fit["leave_one_block_out"]={t:{"min":min(v["coefficients"][t] for v in vals),"max":max(v["coefficients"][t] for v in vals),"n":len(vals)} for t in fit["coefficients"]} if vals else None
    out["status"]="estimated_descriptive_only" if any(out[k] is not None for k in ("adjusted","block_adjusted")) else "insufficient_macro_support"
    return out

def main():
    p=argparse.ArgumentParser()
    for k in ("source","archives","wcvp","outdir"):p.add_argument("--"+k,required=True,type=Path)
    a=p.parse_args();data,audit=load_sources(a.source,a.archives)
    pair,bad=paired_data(data);prior_check(a.archives,pair)
    if bad or len(pair)!=82 or pair.genus.nunique()!=68 or pair.family.nunique()!=28:raise ValueError("paired original cohort drift")
    n=separate_data(data["nectar"],"nectar");pollen=separate_data(data["pollen"],"pollen")
    if (len(n),len(pollen))!=(457,196):raise ValueError("separate original cohort drift")
    cohorts={"paired":(pair,("nectar","pollen")),"nectar_separate":(n,("nectar",)),"pollen_separate":(pollen,("pollen",))}
    geo=frame(a.archives).sort_values("TDWG_L3").reset_index(drop=True)
    codes=set(geo.TDWG_L3)
    allnames=set(pair.species)|set(n.species)|set(pollen.species)
    native,meta=wcvp_regions(a.wcvp,allnames)
    accepted=set().union(*native.values())
    # No outcome joins with any other geographic region. The training pool
    # consists of original compiled species values with accepted native ranges,
    # not independent measurements within any mapped region.
    ranges={code:native.get(code,set()) for code in codes}
    rows=[];metrics={}
    for label,(d,rewards) in cohorts.items():
        d=d[d.species.isin(accepted)].reset_index(drop=True)
        species_covered=set(d.species)&set().union(*ranges.values())
        counts={code:len(set(d.species)&ranges[code]) for code in codes}
        metrics[label]={"original_species":len(cohorts[label][0]),"exact_WCVP_native_species":len(d),
           "unique_species_in_72_regions":len(species_covered),"native_species_region_incidences":sum(counts.values()),
           "regions_with_any_source_species":sum(v>0 for v in counts.values()),
           "regions_with_at_least_5_species":sum(v>=5 for v in counts.values()),
           "regions_with_at_least_10_species":sum(v>=10 for v in counts.values()),
           "regional_species_count_min_median_max":[min(counts.values()),float(np.median(list(counts.values()))),max(counts.values())],
           "regional_transfer":{}}
        for group in ("genus","family"):
            eligible=[];used=set()
            for row in geo.to_dict("records"):
                code=row["TDWG_L3"]
                result,usedrows=region_test(d,ranges[code],group,rewards)
                flat={"TDWG_L3":code,"cohort":label,"lineage_excluded":group,**{k:row[k] for k in (W,B,E,G,*COV)},**{k:v for k,v in result.items() if k!="outcomes"}}
                for reward,vals in result.get("outcomes",{}).items():
                    flat.update({reward+"_"+k:v for k,v in vals.items()})
                rows.append(flat)
                if result["status"]=="estimated_exploratory":
                    eligible.append(flat);used.update(x["species"] for x in usedrows)
            st=Counter(row["status"] for row in rows if row["cohort"]==label and row["lineage_excluded"]==group)
            rec={"status_counts":dict(st),"estimated_regions":len(eligible),"unique_test_species":len(used),"estimated_geo_blocks":len({x[G] for x in eligible}),
                 "total_test_species_region_incidences":sum(x["n_test"] for x in eligible)}
            if eligible:
                q=pd.DataFrame(eligible)
                for r in rewards:
                    for k in ("transfer_skill_vs_training_mean","within_assemblage_pair_contrast_skill","kendall_tau_b"):
                        v=q[r+"_"+k].dropna()
                        rec[r+"_"+k]={"n":len(v),"median":float(v.median()) if len(v) else None,"positive_regions":int((v>0).sum()),"min_max":[float(v.min()),float(v.max())] if len(v) else None}
                if label=="paired":
                    y="within_assemblage_pair_contrast_skill_nectar_minus_pollen"
                    v=q[y].dropna()
                    rec["paired_contrast"]={"n":len(v),"median":float(v.median()) if len(v) else None,"positive_regions":int((v>0).sum())}
                    rec["paired_environment_screen"]={k:macro_screen(q,y,bee) for k,bee in [("wind",False),("wind_and_recorded_Bombus",True)]}
            metrics[label]["regional_transfer"][group]=rec
    a.outdir.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(a.outdir/"stage121_regional_reward_transfer_summary.csv",index=False)
    out={"stage120_paired_source_metrics_reproduced":True,"WCVP_original_SHA256":WCVP_SHA,
         "source_rewards_member_SHA256":HASHES,"exploration_regions":72,"geographic_blocks":17,
         "original_source_native_range_cohort_audit":meta,"cohorts":metrics,
         "min_support":{"test_species":MIN_TEST,"test_genera":MIN_TEST_GENERA,"test_families":MIN_TEST_FAMILIES,"train_species":MIN_TRAIN,"train_lineages":MIN_TRAIN_GROUPS,"macro_regions":MIN_MACRO_REGIONS,"macro_geoblocks":MIN_MACRO_BLOCKS},
         "regional_pair_contrast_is_evaluation_not_test_outcome_calibrated_prediction":True,
         "no_regional_IID_pvalues":True,"no_local_reward_measurements_or_observed_coflowering":True,
         "no_adaptive_acquisition_or_causal_wind_Bombus_claim":True,"no_37_holdout_region_outcome_join":True}
    (a.outdir/"stage121_regional_reward_transfer.json").write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("STAGE121_ORIGINAL_REGIONAL_REWARD_TRANSFER",json.dumps(out,sort_keys=True,allow_nan=False))
if __name__=="__main__":main()
