"""Stage 3e: wind × floral structure in conditional pollinator guild composition.

Observational 10-minute focal-flower FIT Counts, exploratory POST-HOC analysis.
The prior outcome bumblebee-vs-other-fly composition was chosen after inspecting
Stage 3 results. No simultaneous flower choice, competition, adaptation, or
animal-level causal wind response is identified by these models.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import warnings
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm

from fit_associations import SOURCE_DATA_SHA256, WIND, prepare, read_source
from stage3_full_profile import TABLES
from clock_observer_sensitivity import audit_clock, label_clock, CLOCK_BINS

OTHER="Other - please describe below"
OPEN="open"
CLOSED="closed"

def prepare_interaction(df, surface, include_other=False):
    """Preserve exact source 10-min survey grain before conditioning on pair."""
    if surface not in ("one_km","public"):raise ValueError("unknown survey mode")
    d, flow=prepare(df,surface)
    total=len(d)
    minutes,clock=audit_clock(d)
    rec={"raw_surveys":len(df),"eligible_all_surveys":len(d),
         "first_stage_exclusions":flow,"time_profile":clock,
         "include_other_taxa_mixture":bool(include_other)}
    if clock["parsed_fraction"]<.95:
        return None,{**rec,"status":"NO_GO_CLOCK_PARSING_BELOW_95_PERCENT"}
    d=d.copy()
    d["clock_bin"]=pd.Categorical(
        [label_clock(None if pd.isna(t) else t) for t in minutes],
        categories=CLOCK_BINS,ordered=False)
    d=d[d["clock_bin"].notna()].copy()
    rec["unparsed_clock_excluded"]=total-len(d)
    d["structure"]=d["flower_structure"].astype("string").str.strip().str.lower()
    known=d.structure.isin([OPEN,CLOSED])
    rec["uncertain_morphology_excluded"]=int((~known).sum())
    d=d.loc[known].copy()
    if not include_other:
        rec["heterogeneous_other_target_excluded"]=int(d.target_flower_corrected.eq(OTHER).sum())
        d=d.loc[d.target_flower_corrected.ne(OTHER)].copy()
    else:
        rec["heterogeneous_other_target_excluded"]=0
    d["bumblebees"]=pd.to_numeric(d["bumblebees"],errors="raise")
    d["other_flies"]=pd.to_numeric(d["other_flies"],errors="raise")
    if d[["bumblebees","other_flies"]].isna().any().any():
        raise ValueError("unresolved missing insect group data")
    if (d[["bumblebees","other_flies"]]<0).any().any():
        raise ValueError("negative insect group data")
    pair=d["bumblebees"]+d["other_flies"]
    rec["pair_absent_surveys_excluded"]=int((pair==0).sum())
    d=d.loc[pair>0].copy()
    if not len(d):
        rec["status"]="NO_GO_NO_PAIR_POSITIVE_SURVEYS";return None,rec
    d["closed"]=d["structure"].eq(CLOSED).astype(int)
    d["gentle_closed"]=(d.wind_speed==WIND[1]).astype(int)*d.closed
    d["strong_closed"]=(d.wind_speed==WIND[2]).astype(int)*d.closed
    d["recorder_type_audited"]=d.recorder_type.fillna("__SOURCE_MISSING__").astype(str)
    d["flower_cover_audited"]=d.flower_cover.fillna("__SOURCE_MISSING__").astype(str)
    rec["pair_positive_surveys"]=int(len(d))
    cluster="location_code" if surface=="one_km" else "x1km_square"
    rec["clusters"]=int(d[cluster].nunique())
    rec["support_by_structure"]={}
    for s in [OPEN,CLOSED]:
        x=d[d.structure.eq(s)]
        per_wind={w:int((x.wind_speed==w).sum()) for w in WIND}
        both=x[x.wind_speed.isin([WIND[0],WIND[2]])].groupby(
            [cluster,"wind_speed"],observed=True).size().unstack(fill_value=0)
        common=int(((both.get(WIND[0],pd.Series(0,index=both.index))>0)&
                    (both.get(WIND[2],pd.Series(0,index=both.index))>0)).sum())
        rec["support_by_structure"][s]={
            "surveys":len(x),
            "wind_counts":per_wind,
            "sites_with_calm_and_strong":common,
            "named_target_categories":int(x.target_flower_corrected.nunique()),
            "bumble_visits":int(x.bumblebees.sum()),
            "other_fly_visits":int(x.other_flies.sum()),
            "observed_bumble_fraction_by_wind":{
                w:(float(x.loc[x.wind_speed==w,"bumblebees"].sum() /
                         (x.loc[x.wind_speed==w,["bumblebees","other_flies"]].sum().sum()))
                   if (x.loc[x.wind_speed==w,["bumblebees","other_flies"]].sum().sum())>0 else None)
                for w in WIND}}
    failures=[]
    for s,stat in rec["support_by_structure"].items():
        if stat["surveys"]<100:failures.append(f"{s}: pair-positive surveys <100")
        if stat["wind_counts"][WIND[0]]<30:failures.append(f"{s}: calm <30")
        if stat["wind_counts"][WIND[2]]<30:failures.append(f"{s}: strong <30")
        if stat["sites_with_calm_and_strong"]<10:failures.append(f"{s}: site overlap <10")
    if failures:
        rec["status"]="NO_GO_INSUFFICIENT_STRUCTURE_OVERLAP"
        rec["support_failure_reasons"]=failures
        return None,rec
    rec["status"]="ELIGIBLE"
    return d,rec

def _formula(surface,include_other=False):
    """Morphology main effect is aliased with target among named taxa."""
    loc=" + C(location_code)" if surface=="one_km" else " + C(country) + C(habitat_type)"
    formula=(
        "C(wind_speed, Treatment(reference='Leaves still/moving occasionally'))"
        " + log_flower_units + C(target_flower_corrected)"
        " + C(year) + C(sunshine) + bs(day_of_year, df=4, degree=3)"
        " + C(clock_bin) + C(recorder_type_audited) + C(flower_cover_audited)"
        " + gentle_closed + strong_closed"
    )
    if include_other:
        # One heterogeneous target label now contains both annotated structures,
        # so the closed main effect can be identified within that source label.
        formula+=" + closed"
    return formula+loc

def _lin_combo(model, names, weights):
    params=model.params
    v=np.zeros(len(params))
    for name,weight in zip(names,weights):
        if name not in params.index:raise ValueError("missing model coefficient "+name)
        v[params.index.get_loc(name)]+=weight
    estimate=float(v@params.to_numpy())
    variance=float(v@model.cov_params().to_numpy()@v)
    if not np.isfinite([estimate,variance]).all() or variance < 0:
        raise ValueError("invalid linear combination variance")
    se=np.sqrt(variance)
    return {"OR":float(np.exp(estimate)),
            "CI95":[float(np.exp(estimate-1.95996398454*se)),
                    float(np.exp(estimate+1.95996398454*se))],
            "log_odds_coefficient":estimate,
            "cluster_se":float(se)}

def fit_interaction(d,surface,include_other=False):
    cluster="location_code" if surface=="one_km" else "x1km_square"
    out={"status":"not_fitted","surface":surface,
         "analysis_subset":"all_structure_defined_targets" if include_other else "named_targets_only",
         "pair_positive_surveys":len(d),
         "cluster_count":int(d[cluster].nunique()),
         "model_formula":_formula(surface,include_other),
         "posthoc":True}
    if len(d)<100 or d[cluster].nunique()<15:
        out["status"]="NO_GO_TOO_FEW_SITES_OR_SURVEYS";return out
    try:
        X=patsy.dmatrix(out["model_formula"],d,return_type="dataframe")
        if len(X)!=len(d):raise ValueError("design drops pair-positive surveys")
        rank=int(np.linalg.matrix_rank(X.to_numpy()))
        out["design_columns"]=len(X.columns)
        out["design_rank"]=rank
        if rank!=X.shape[1]:
            out["status"]="NO_GO_RANK_DEFICIENT"
            return out
        y=np.column_stack([d.bumblebees.astype(int).to_numpy(),
                           d.other_flies.astype(int).to_numpy()])
        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter("always")
            m=sm.GLM(y,X,family=sm.families.Binomial()).fit(
                maxiter=180,cov_type="cluster",
                cov_kwds={"groups":d[cluster].astype(str).to_numpy()})
        out["warnings"]=[str(w.message) for w in warns][-10:]
        out["converged"]=bool(m.converged)
        out["pearson_dispersion"]=float(m.pearson_chi2/m.df_resid)
        if not m.converged:
            out["status"]="NO_GO_NONCONVERGED"
            return out
        names=["gentle_closed","strong_closed"]
        if not set(names)<=set(m.params.index):
            out["status"]="NO_GO_INTERACTION_TERMS_MISSING";return out
        ci=m.conf_int()
        if not np.isfinite(ci.loc[names].to_numpy()).all():
            out["status"]="NO_GO_NONFINITE_INTERVAL";return out
        r=np.zeros((2,len(m.params)))
        for i,name in enumerate(names):
            r[i,m.params.index.get_loc(name)]=1.0
        test=m.wald_test(r,scalar=True)
        if not np.isfinite([test.statistic,test.pvalue]).all():
            out["status"]="NO_GO_NONFINITE_WALD";return out
        windstrong=[n for n in m.params.index
                    if n.startswith("C(wind_speed") and "Leaves moving strongly" in n]
        if len(windstrong)!=1:
            out["status"]="NO_GO_NO_STRONG_WIND_MAIN_COEFFICIENT";return out
        w=windstrong[0]
        out["status"]="FITTED"
        out["interaction_joint_wald"]={
            "chi2":float(test.statistic),"df":2,"p":float(test.pvalue)}
        out["strong_wind_effect_modification_closed_vs_open"]=_lin_combo(m,["strong_closed"],[1.0])
        out["gentle_wind_effect_modification_closed_vs_open"]=_lin_combo(m,["gentle_closed"],[1.0])
        out["strong_wind_vs_calm_open"]=_lin_combo(m,[w],[1.0])
        out["strong_wind_vs_calm_closed"]=_lin_combo(m,[w,"strong_closed"],[1.0,1.0])
        out["claim_ceiling"]="Within-survey conditional guild odds, not causal flower morphology adaptation or competition"
    except Exception as exc:
        out["status"]="MODEL_FAILURE"
        out["error"]=str(exc)
    return out

def analyze(archive,outdir):
    report={"status":"exploratory_posthoc",
            "question":"Does flower structure modify wind association with bumblebee:other-fly observed visits?",
            "member_sha256":{}, "surfaces":{},
            "limits":"Single-target 10-minute FIT counts; species-specific availability, within-individual decisions, experimental wind, and fitness not measured"}
    with zipfile.ZipFile(archive) as z:
        for surface in ("one_km","public"):
            b=z.read(TABLES[surface])
            h=hashlib.sha256(b).hexdigest()
            if h!=SOURCE_DATA_SHA256[surface]:
                raise ValueError("source CSV hash mismatch "+surface)
            report["member_sha256"][surface]=h
            df,codec=read_source(b)
            summary={"source_encoding":codec,"source_rows":len(df),"analysis":{}}
            for include_other in (False,True):
                k="named_targets_primary" if not include_other else "including_other_sensitivity"
                x,receipt=prepare_interaction(df,surface,include_other=include_other)
                summary["analysis"][k]={"admission":receipt}
                if x is not None:
                    summary["analysis"][k]["model"]=fit_interaction(x,surface,include_other)
                else:
                    summary["analysis"][k]["model"]={"status":"NOT_FIT_ADMISSION_FAILED"}
            report["surfaces"][surface]=summary
    outdir.mkdir(exist_ok=True,parents=True)
    (outdir/"floral_wind_guild_interaction.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))
    for surface,r in report["surfaces"].items():
        print("POMS_STRUCTURE_INTERACTION "+json.dumps({"surface":surface,**r},ensure_ascii=False,allow_nan=False),flush=True)
    print("POMS_STRUCTURE_INTERACTION_COMPLETE",flush=True)
    return report

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage3e_results")
    a=p.parse_args(argv)
    root=Path(a.out)
    analyze(root/"poms_fit_2017_2023_source.zip",root)

if __name__=="__main__":main()
