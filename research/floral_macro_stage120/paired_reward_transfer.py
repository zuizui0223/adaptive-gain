#!/usr/bin/env python3
"""Stage120: distinguish reward target from sample composition and publication.
All data are compiled species-level production, not realized rewards or
observed information use. Same species/lineages/folds for paired comparison.
Source-label holdout is a conservative provenance sensitivity, not a guarantee
that two labels denote independent experiments. Never use geographic holdout.
"""
import argparse,hashlib,json,math,sys
from collections import Counter
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.model_selection import GroupKFold
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage119"))
from budgeted_reward import load_sources,read_table,members,tables,HASHES,species,cat,number,predict,routed,STATES

MODELS=("no_cue","symmetry","tube","symmetry_tube_joint","symmetry_tube_routed")
def model_predictions(tr,te):
    return {"no_cue":predict(tr,te,[]),"symmetry":predict(tr,te,["symmetry"]),
            "tube":predict(tr,te,["tube"]),"symmetry_tube_joint":predict(tr,te,["symmetry","tube"]),
            "symmetry_tube_routed":routed(tr,te,{s:"tube" for s in STATES})}
def summary(errors):
    mse={k:float(np.mean(v)) for k,v in errors.items()}
    return {"mse":mse,"skill_vs_no_cue":{k:1-v/mse["no_cue"] for k,v in mse.items() if k!="no_cue"}}
def paired_data(data):
    # Identical species, identical morphology, exact cross-target taxonomic match.
    n=data["nectar"];p=data["pollen"]
    fields=["species","genus","family","tube","symmetry","target"]
    n=n[fields].dropna().rename(columns={"target":"nectar"})
    p=p[fields].dropna().rename(columns={"target":"pollen"})
    z=n.merge(p,on="species",suffixes=("","_p"),validate="1:1")
    good=z.genus.eq(z.genus_p)&z.family.eq(z.family_p)&z.symmetry.eq(z.symmetry_p)&np.isclose(z.tube,z.tube_p,atol=1e-12,rtol=0)
    return z[good][["species","genus","family","tube","symmetry","nectar","pollen"]].reset_index(drop=True),int((~good).sum())

def paired_evaluate(d,group):
    n=len(d);g=d[group].nunique()
    # This is a prespecified descriptive matched-cohort check, not a new
    # confirmation. Do not force sparse two-state models.
    if n<30 or g<10 or min(d.symmetry.value_counts().reindex(STATES,fill_value=0))<5:
        return {"status":"insufficient_paired_support","n":n,"groups":int(g),"states":{str(k):int(v) for k,v in d.symmetry.value_counts().items()}}
    err={r:{k:np.empty(n) for k in MODELS} for r in ("nectar","pollen")}
    folds=[];predrows=[]
    for f,(i,j) in enumerate(GroupKFold(5).split(d,groups=d[group])):
        assert not set(d.iloc[i][group])&set(d.iloc[j][group])
        one={"fold":f,"n_test":len(j)}
        for r in err:
            tr=d.iloc[i].assign(target=d.iloc[i][r]);te=d.iloc[j].assign(target=d.iloc[j][r])
            pred=model_predictions(tr,te)
            for k,v in pred.items():err[r][k][j]=(v-te.target.to_numpy())**2
            one[r]=summary({k:err[r][k][j] for k in MODELS})
        folds.append(one)
    result={r:summary(x) for r,x in err.items()}
    # Ratio of pooled heldout losses, not difference of differently scaled MSE.
    # Descriptive group bootstrap on fixed OOF errors with same draws for both rewards.
    ids=d[group].unique();rng=np.random.default_rng(20261126)
    vals={}
    for r in err:
        tab=pd.DataFrame({"group":d[group],**err[r]}).groupby("group").sum().reindex(ids)
        vals[r]=tab
    ix=rng.integers(0,len(ids),size=(1999,len(ids)))
    contrasts={}
    for model in MODELS[1:]:
        skill={}
        for r in err:
            sums=vals[r][model].to_numpy()[ix].sum(axis=1)
            denom=vals[r]["no_cue"].to_numpy()[ix].sum(axis=1)
            skill[r]=1-sums/denom
        delta=skill["nectar"]-skill["pollen"]
        contrasts[model]={"observed_nectar_minus_pollen_skill":result["nectar"]["skill_vs_no_cue"][model]-result["pollen"]["skill_vs_no_cue"][model],
                          "descriptive_paired_group_resampling_95":list(map(float,np.quantile(delta,[.025,.975])))}
    return {"status":"estimated_exploratory","n":n,"groups":int(g),"states":{str(k):int(v) for k,v in d.symmetry.value_counts().items()},"outcomes":result,"paired_skill_contrasts":contrasts,"folds":folds}

def nectar_rows(raw):
    _,rows,_=tables(raw,"nectar")[0]
    h=[str(x or "").strip() for x in rows[3]]
    fields=["Species","Genus","Family","Nectar (µg/day)","Source"]
    if any(h.count(k)!=1 for k in fields):raise ValueError("nectar source header changed")
    ix=[h.index(k) for k in fields]
    d=pd.DataFrame([{k:r[j] if j<len(r) else None for k,j in zip(fields,ix)} for r in rows[4:]])
    d["species"]=d.Species.map(species);d["genus"]=d.Genus.map(cat);d["family"]=d.Family.map(cat)
    d["value"]=d["Nectar (µg/day)"].map(number);d["source"]=d.Source.map(cat)
    ok=d.species.notna()&d.genus.notna()&d.family.notna()&d.species.str.split().str[0].eq(d.genus)
    return d[ok].copy()
def zero_audit(raw):
    d=nectar_rows(raw);valid=d[d.value.notna()].copy()
    z=valid.assign(zero=valid.value.eq(0),negative=valid.value.lt(0),positive=valid.value.gt(0)).groupby("species").agg(zero=("zero","sum"),negative=("negative","sum"),positive=("positive","sum"))
    bysource=valid.assign(zero=valid.value.eq(0),negative=valid.value.lt(0)).groupby("source",dropna=False).agg(rows=("value","size"),zero=("zero","sum"),negative=("negative","sum")).sort_values("zero",ascending=False)
    return {"rows":len(d),"zero_rows":int((valid.value==0).sum()),"negative_rows":int((valid.value<0).sum()),"species_with_zero":int((z.zero>0).sum()),"species_with_zero_and_positive":int(((z.zero>0)&(z.positive>0)).sum()),"species_all_zero_or_negative":int((z.positive==0).sum()),"source_label_rows":int(d.source.notna().sum()),"distinct_source_labels":int(d.source.nunique()),"source_zero_counts":bysource.reset_index().fillna("MISSING").to_dict("records")}

def aggregate_compatible(rows,morph,zero=False):
    # Equal row-weight within species as original compilation. Reject taxonomic
    # conflicts; zeros included only in a separately labelled sensitivity.
    rows=rows[rows.value.notna()&(rows.value.ge(0) if zero else rows.value.gt(0))].copy()
    z=rows.groupby("species").agg(genus=("genus",lambda x:x.iloc[0] if x.nunique()==1 else None),family=("family",lambda x:x.iloc[0] if x.nunique()==1 else None),value=("value","mean")).reset_index()
    z=z.dropna(subset=["genus","family"])
    z=z.merge(morph,on="species",suffixes=("","_m"),validate="1:1")
    z=z[z.genus.eq(z.genus_m)&z.family.eq(z.family_m)].dropna(subset=["tube","symmetry"])
    if zero:z["target"]=np.log10(1+z.value)
    else:z["target"]=np.log10(z.value)
    return z[["species","genus","family","tube","symmetry","target"]].reset_index(drop=True)

def fixed_cv(d,group):
    if len(d)<30 or d[group].nunique()<10:return {"status":"insufficient_support","n":len(d)}
    err={k:np.empty(len(d)) for k in MODELS}
    for i,j in GroupKFold(5).split(d,groups=d[group]):
        pred=model_predictions(d.iloc[i],d.iloc[j])
        for k,v in pred.items():err[k][j]=(v-d.iloc[j].target.to_numpy())**2
    return {"n":len(d),"groups":int(d[group].nunique()),**summary(err)}

def source_transfer(rows,morph):
    # Source-specific reward held out. No test species or test genus occurs in
    # training, even if its other reward rows are from a different source.
    out=[]
    for source in sorted(rows.source.dropna().unique()):
        te=aggregate_compatible(rows[rows.source==source],morph)
        if len(te)<20 or te.genus.nunique()<8:continue
        other=rows[rows.source.notna()&rows.source.ne(source)&~rows.genus.isin(te.genus)]
        tr=aggregate_compatible(other,morph)
        if len(tr)<60 or tr.genus.nunique()<20:continue
        assert not set(tr.genus)&set(te.genus)
        pred=model_predictions(tr,te)
        er={k:(v-te.target.to_numpy())**2 for k,v in pred.items()}
        out.append({"source_label":source,"n_test":len(te),"test_genera":int(te.genus.nunique()),"n_train":len(tr),**summary(er)})
    return {"eligible_source_labels":len(out),"positive_tube_routed_skill_labels":sum(x["skill_vs_no_cue"]["symmetry_tube_routed"]>0 for x in out),"individual":out,"no_independence_claim_for_source_labels":True}

def main():
    p=argparse.ArgumentParser();p.add_argument("--source",type=Path,required=True);p.add_argument("--archives",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args()
    raw=members(a.source)
    if any(hashlib.sha256(raw[k]).hexdigest()!=HASHES[k] for k in HASHES):raise ValueError("original source member digest drift")
    data,audit=load_sources(a.source,a.archives)
    assert audit["both_rewards_species"]==131 and audit["nectar"]["admitted_unique_species"]==858 and audit["pollen"]["admitted_unique_species"]==1490
    pair,conflicts=paired_data(data)
    morph,_=read_table(raw["morphology"],"morphology")
    rows=nectar_rows(raw["nectar"])
    z=zero_audit(raw["nectar"])
    positive=aggregate_compatible(rows,morph)
    incl=aggregate_compatible(rows,morph,True)
    # Compare identical species on the same log1p scale; inclusion of zero
    # rows is sensitivity only. Separately report added all-zero species.
    comm=positive[["species","genus","family","tube","symmetry"]].merge(incl[["species","target"]],on="species",validate="1:1")
    common_pos=positive.merge(comm[["species"]],on="species",validate="1:1")
    common_pos["target"]=np.log10(1+10**common_pos.target)
    common_pos=common_pos.sort_values("species").reset_index(drop=True);comm=comm.sort_values("species").reset_index(drop=True)
    assert common_pos.species.equals(comm.species)
    out={"original_source_hashes":HASHES,"stage119_source_counts_reproduced":True,
         "paired_morphology_and_rewards_n":len(pair),"paired_taxonomic_or_morphology_conflicts":conflicts,
         "matched_cohort":{g:paired_evaluate(pair,g) for g in ("genus","family")},
         "nectar_zero_audit":z,"zero_inclusive_sensitivity":{"common_species_n":len(comm),"added_species_n":len(incl)-len(comm),
             "positive_rows_only_same_log1p_scale":{g:fixed_cv(common_pos,g) for g in ("genus","family")},
             "zero_rows_included_same_log1p_scale":{g:fixed_cv(comm,g) for g in ("genus","family")},
             "all_nonnegative_supported_species":{g:fixed_cv(incl,g) for g in ("genus","family")}},
         "nectar_source_label_and_genus_disjoint_transfer":source_transfer(rows,morph),
         "pollen_source_column_unavailable_no_publication_holdout":True,
         "zero_semantics_not_independently_confirmed":True,"no_adaptive_acquisition_claim":True,"no_holdout_geographic_outcomes":True}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STAGE120_PAIRED_REWARD_SOURCE_TRANSFER",json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
