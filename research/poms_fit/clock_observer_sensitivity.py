"""Stage 3d: post-hoc clock/recorder/flower-cover robustness of the wind-guild signal.

Only recorded 10-minute FIT visits to ONE selected floral target are observed.
Do not interpret pair composition or reported leaf movement as a causal wind
experiment, simultaneous-resource choice or sensing routeability.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm

from stage3_full_profile import TABLES
from fit_associations import SOURCE_DATA_SHA256, prepare, read_source
from guild_composition import fit_guild_pair

FAMILY = ("bumblebees", "other_flies")
CLOCK_BINS = ("before_10", "10_to_12", "12_to_14", "14_to_16", "from_16")
CALM = "Leaves still/moving occasionally"
STRONG = "Leaves moving strongly"

# These formats use explicit units/punctuation and are reversible. No guessed
# timezone, fake date, numeric Excel-time or inferred survey start time.
CLOCK_24 = re.compile(r"^(?P<h>[0-9]{1,2}):(?P<m>[0-9]{2})(?::(?P<s>[0-9]{2}))?$")
CLOCK_12 = re.compile(r"^(?P<h>[0-9]{1,2}):(?P<m>[0-9]{2})(?::(?P<s>[0-9]{2}))?\s*(?P<ap>[AaPp][Mm])$")

def parse_clock(value):
    """Return (minutes since midnight, source_format), or (None, reason)."""
    if value is None or pd.isna(value):
        return None,"missing"
    raw=str(value).strip()
    if not raw or raw.lower() in {"nan","na","n/a","not recorded","unknown"}:
        return None,"missing"
    match=CLOCK_12.fullmatch(raw)
    if match:
        hour=int(match["h"]);minute=int(match["m"]);sec=int(match["s"] or "0")
        if not (1<=hour<=12 and 0<=minute<60 and 0<=sec<60):
            return None,"invalid_12h"
        return (hour%12 + (12 if match["ap"].lower()=="pm" else 0))*60 + minute, "clock_12h"
    match=CLOCK_24.fullmatch(raw)
    if match:
        hour=int(match["h"]);minute=int(match["m"]);sec=int(match["s"] or "0")
        if not (0<=hour<24 and 0<=minute<60 and 0<=sec<60):
            return None,"invalid_24h"
        return hour*60 + minute,"clock_24h"
    return None,"unrecognized"

def label_clock(minutes):
    if minutes is None or pd.isna(minutes): return None
    edges=(600,720,840,960)
    return CLOCK_BINS[sum(minutes>=t for t in edges)]

def audit_clock(data):
    parsed=[parse_clock(v) for v in data["count_start_time"]]
    formats=pd.Series([x[1] for x in parsed])
    missing=[str(raw) for raw,p in zip(data["count_start_time"],parsed) if p[0] is None]
    seen=[]
    for value in missing:
        if value not in seen:seen.append(value)
        if len(seen)==16:break
    minutes=pd.Series([p[0] for p in parsed],index=data.index,dtype="float64")
    return minutes,{
        "surveys":len(data),
        "parsed":int(minutes.notna().sum()),
        "parsed_fraction":float(minutes.notna().mean()),
        "formats":{str(k):int(v) for k,v in formats.value_counts(dropna=False).items()},
        "unparsed_raw_examples":seen,
        "clock_bin_counts":{b:int((minutes.apply(label_clock)==b).sum()) for b in CLOCK_BINS}
    }

def formula(surface):
    controls=(" + C(location_code)" if surface=="one_km"
              else " + C(country) + C(habitat_type)")
    return (
        "C(wind_speed, Treatment(reference='Leaves still/moving occasionally'))"
        " + log_flower_units + C(floral_unit) + C(target_flower_corrected)"
        " + C(year) + C(sunshine)"
        " + bs(day_of_year, df=4, degree=3)"
        " + C(clock_bin)"
        " + C(recorder_type_audited)"
        " + C(flower_cover_audited)"
        + controls
    )

def augmented_pair(data,surface):
    cluster="location_code" if surface=="one_km" else "x1km_square"
    pair_valid=(data["bumblebees"].notna() & data["other_flies"].notna() &
                (data["bumblebees"]+data["other_flies"]>0))
    selected=data.loc[pair_valid].copy()
    result={
        "surface":surface,"status":"not_fitted",
        "eligible_surveys":len(data),
        "pair_positive_surveys":len(selected),
        "pair_both_zero_surveys":int((~pair_valid).sum()),
        "cluster_count":int(selected[cluster].nunique()),
        "model_formula":formula(surface),
        "contrasts":"bumblebee vs other-fly odds, conditional on >=1 recorded visit of either group"
    }
    if len(selected)<100 or selected[cluster].nunique()<15:
        result["status"]="insufficient_sample"
        return result
    try:
        matrix=patsy.dmatrix(formula(surface),selected,return_type="dataframe")
        if len(matrix)!=len(selected):
            raise ValueError("design silently drops some original paired surveys")
        y=np.column_stack([selected["bumblebees"].astype(int).to_numpy(),
                           selected["other_flies"].astype(int).to_numpy()])
        rank=int(np.linalg.matrix_rank(matrix.to_numpy()))
        result["design_columns"]=len(matrix.columns)
        result["design_rank"]=rank
        if rank!=len(matrix.columns):
            result["status"]="rank_deficient"
            return result
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            fit=sm.GLM(y,matrix,family=sm.families.Binomial()).fit(
                maxiter=180,cov_type="cluster",
                cov_kwds={"groups":selected[cluster].astype(str).to_numpy()})
        result["fit_warnings"]=[str(w.message) for w in caught][-8:]
        result["converged"]=bool(fit.converged)
        result["pearson_dispersion"]=float(fit.pearson_chi2/fit.df_resid)
        wind=[c for c in fit.params.index if c.startswith("C(wind_speed")]
        strong=[c for c in wind if "Leaves moving strongly" in c]
        ci=fit.conf_int()
        if len(wind)!=2 or len(strong)!=1 or not np.isfinite(ci.loc[wind].to_numpy()).all():
            result["status"]="invalid_wind_terms"
            return result
        if np.max(np.abs(ci.loc[wind].to_numpy()))>100:
            result["status"]="unbounded_wind_intervals"
            return result
        s=strong[0]
        result["status"]="fitted"
        result["strong_wind_or"]=float(np.exp(fit.params[s]))
        result["strong_wind_ci95"]=[float(np.exp(ci.loc[s,0])),float(np.exp(ci.loc[s,1]))]
        result["strong_wind_p"]=float(fit.pvalues[s])
        restriction=np.zeros((2,len(fit.params)))
        for i,c in enumerate(wind):
            restriction[i,fit.params.index.get_loc(c)]=1
        joint=fit.wald_test(restriction,scalar=True)
        result["wind_joint_p"]=float(joint.pvalue)
        result["wind_joint_chi2"]=float(joint.statistic)
    except Exception as exc:
        result["status"]="fit_failed"
        result["error"]=str(exc)
    return result

def run(archive:Path,outdir:Path):
    report={
        "analysis":"post-hoc clock, recorder and flower-cover robustness",
        "fixed_question":"wind association with bumblebee-to-other-fly relative visitation within focal-flower FIT censuses",
        "source_dataset":"UK PoMS FIT 2017-2023",
        "not_routeability_not_causality":True,
        "surfaces":{}
    }
    with zipfile.ZipFile(archive) as z:
        for surface in ("one_km","public"):
            raw=z.read(TABLES[surface])
            digest=hashlib.sha256(raw).hexdigest()
            if digest!=SOURCE_DATA_SHA256[surface]:
                raise ValueError(f"{surface}: official source CSV SHA256 mismatch")
            df,codec=read_source(raw)
            eligible,flow=prepare(df,surface)
            if not {"count_start_time","recorder_type","flower_cover"}<=set(eligible):
                raise ValueError("missing mandatory clock/recorder/cover columns")
            minutes,clock=audit_clock(eligible)
            receipt={
                "raw_surveys":len(df),
                "prepared_surveys":len(eligible),
                "preparation_flow":flow,
                "source_encoding":codec,
                "source_sha256":digest,
                "time_profile":clock,
                "prior_original_model":fit_guild_pair(eligible,"other_flies",surface=surface),
            }
            if clock["parsed_fraction"]<0.95:
                receipt["status"]="clock_parse_gate_failed_no_model"
                report["surfaces"][surface]=receipt
                continue
            eligible=eligible.copy()
            eligible["clock_bin"]=pd.Categorical(
                [label_clock(None if pd.isna(x) else x) for x in minutes],
                categories=list(CLOCK_BINS),ordered=False)
            eligible["recorder_type_audited"]=eligible["recorder_type"].fillna(
                "__SOURCE_MISSING__").astype(str)
            eligible["flower_cover_audited"]=eligible["flower_cover"].fillna(
                "__SOURCE_MISSING__").astype(str)
            kept=eligible.loc[eligible["clock_bin"].notna()].copy()
            receipt["post_clock_surveys"]=len(kept)
            receipt["excluded_unparseable_clock_surveys"]=len(eligible)-len(kept)
            receipt["recorder_levels"]={str(k):int(v) for k,v in kept["recorder_type_audited"].value_counts(dropna=False).items()}
            receipt["cover_levels"]={str(k):int(v) for k,v in kept["flower_cover_audited"].value_counts(dropna=False).items()}
            receipt["baseline_same_clock_subset"]=fit_guild_pair(
                kept,"other_flies",surface=surface)
            receipt["augmented_with_clock_recorder_cover"]=augmented_pair(kept,surface)
            receipt["status"]="analyzed"
            report["surfaces"][surface]=receipt
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"clock_observer_sensitivity.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))
    for surface,r in report["surfaces"].items():
        print("POMS_STAGE3D "+json.dumps({"surface":surface,**r},ensure_ascii=False,allow_nan=False),flush=True)
    print("POMS_STAGE3D_COMPLETE",flush=True)
    return report

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage3_poms_audit")
    a=p.parse_args(argv)
    out=Path(a.out)
    run(out/"poms_fit_2017_2023_source.zip",out)

if __name__=="__main__":
    main()
