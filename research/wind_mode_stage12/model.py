"""Stage12 frozen single observational wind×nonhoneybee-share movement-mode test.

Source 2026 Dryad provider hashes and original 113-survey gate verified
before model protocol. Result is not a heterospecific cue-use effect.
"""
from __future__ import annotations
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Exact tested Stage11 QR/CR1 library reused without changing its code.
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"wind_reward_stage11"))
from association import clustered_ols, contrast
from source_qa import run as source_audit

def scores(df):
    f=np.asarray(df["flights"],dtype=float)
    w=np.asarray(df["walks"],dtype=float)
    if not np.isfinite(f).all() or not np.isfinite(w).all() or np.any(f<0) or np.any(w<0):
        raise ValueError("NO_GO_SOURCE_MOVEMENT_COUNT_INVALID")
    if np.any(f+w<=0):
        raise ValueError("NO_GO_NO_SOURCE_MOVEMENTS_IN_SURVEY")
    return np.log((f+0.5)/(w+0.5))

def add_within_plant(d):
    z=d.copy()
    if z["survey"].duplicated().any():raise ValueError("NO_GO_SURVEY_PSEUDOREPLICATION")
    if not z["other_share"].between(0,1).all():raise ValueError("NO_GO_BAD_ORIGINAL_SHARE")
    z["w"]=z["beaufort"]-z.groupby("plant")["beaufort"].transform("mean")
    dev=z["other_share"]-z.groupby("plant")["other_share"].transform("mean")
    scale=float(np.std(dev.to_numpy(),ddof=1))
    if not np.isfinite(scale) or scale<=1e-12:raise ValueError("NO_GO_NO_WITHIN_PLANT_OTHER_SHARE_VARIATION")
    z["h"]=dev/scale
    return z,scale

def design(z):
    parts=[np.ones((len(z),1))]
    names=["Intercept"]
    for factor in ("plant","site"):
        levels=sorted(z[factor].astype(str).unique())
        for value in levels[1:]:
            parts.append((z[factor].astype(str)==value).to_numpy(dtype=float)[:,None])
            names.append(factor+":"+value)
    doy=pd.to_datetime(z["date"],errors="raise").dt.dayofyear.to_numpy()
    variables={
        "wind":z["w"].to_numpy(dtype=float),
        "other":z["h"].to_numpy(dtype=float),
        "wind:other":(z["w"]*z["h"]).to_numpy(dtype=float),
        "temperature":z["temperature"].to_numpy(dtype=float),
        "blue_sky_fraction":z["blue_sky"].to_numpy(dtype=float)/100,
        "season_sin":np.sin(2*np.pi*doy/365.25),
        "season_cos":np.cos(2*np.pi*doy/365.25),
        "log1p_density":np.log1p(z["flower_density"].to_numpy(dtype=float)),
    }
    for k,x in variables.items():
        parts.append(np.asarray(x,dtype=float)[:,None])
        names.append(k)
    X=np.column_stack(parts)
    if not np.isfinite(X).all():raise ValueError("NO_GO_NONFINITE_SOURCE_DESIGN")
    if names.count("wind:other")!=1:
        raise ValueError("NO_GO_NOT_EXACTLY_ONE_FROZEN_INTERACTION")
    return X,names

def fit_stage12(d):
    if "survey" not in d or len(d)<80:
        raise ValueError("NO_GO_FROZEN_SURVEY_SAMPLE")
    if d["site"].nunique()!=2:
        raise ValueError("NO_GO_NOT_TWO_ORIGINAL_SOURCE_CITIES")
    groups=(d["site"].astype(str)+"|"+d["date"].astype(str)).to_numpy()
    G=len(np.unique(groups))
    if G<30:raise ValueError("NO_GO_CITY_DATE_REPLICATION")
    z,sd=add_within_plant(d)
    X,names=design(z)
    if X.shape[0]-X.shape[1]<40:raise ValueError("NO_GO_FROZEN_RESIDUAL_DF")
    if np.linalg.matrix_rank(X)!=X.shape[1]:
        raise ValueError("NO_GO_SOURCE_DESIGN_RANK")
    Y=scores(z)
    fit=clustered_ols(X,Y,groups)
    basis=np.eye(len(names))
    primary=contrast(fit,basis[names.index("wind:other")])
    baseline=basis[names.index("wind")]
    modifier=basis[names.index("wind:other")]
    conditional={str(h):contrast(fit,baseline+float(h)*modifier) for h in (-1,0,1)}
    # Separate implementation: actual observed data evaluated in statsmodels
    # to verify the calculated CR1 coefficients, uncertainty and p-values.
    independent=sm.OLS(Y,X).fit(cov_type="cluster",
        cov_kwds={"groups":groups,"use_correction":True},use_t=True)
    db=float(np.max(np.abs(independent.params-fit["beta"])))
    dc=float(np.max(np.abs(independent.cov_params()-fit["cov"])))
    dp=float(abs(independent.pvalues[names.index("wind:other")]-
                 primary["p_two_sided"]))
    if db>1e-9 or dc>1e-9 or dp>1e-9:
        raise ValueError("NO_GO_INDEPENDENT_NUMERICAL_RECONCILIATION")
    return {
        "status":"FROZEN_ORIGINAL_OBSERVATIONAL_STAGE12_ESTIMATED",
        "source":"Harris et al 2026 Dryad v456836",
        "surveys":fit["n"],"city_day_clusters":fit["clusters"],
        "cities":sorted(d["site"].unique().tolist()),
        "native_60s_behavior_rows":int(d["behavior_rows"].sum()),
        "native_flights":int(d["flights"].sum()),
        "native_walks":int(d["walks"].sum()),
        "native_movement_events":int((d["flights"]+d["walks"]).sum()),
        "plant_categories":int(d["plant"].nunique()),
        "design_columns":fit["p"],"design_rank":fit["rank"],
        "residual_df":fit["residual_df"],
        "cr1_city_date_clusters":fit["clusters"],
        "within_plant_heterospecific_share_sd":sd,
        "model_contrast":"wind:other",
        "primary_wind_by_other_share_interaction":primary,
        "secondary_conditional_wind_slopes":conditional,
        "all_frozen_coefficients":dict(zip(names,map(float,fit["beta"]))),
        "independent_statsmodels":{"max_beta_absolute_diff":db,
                                  "max_covariance_absolute_diff":dc,
                                  "primary_p_absolute_diff":dp},
        "survey_weight_semantics":"every original survey equal weight",
        "response":"log((total original flights +0.5)/(total original walks +0.5))",
        "wind":"original ordinal Beaufort, plant centered",
        "other_insects":"other non-honeybee count / all insect counts in same survey, plant centered and pooled SD",
        "not_actual_heterospecific_cue_use":True,
        "not_randomized_wind":True,
        "not_fitness_or_resource_intake":True,
    }

def run(root):
    root=Path(root)
    out=root/"stage12_mode_interaction_result.json"
    d,q=source_audit(root)  # verifies provider source sha, original key QA
    results={"status":"NO_GO_STAGE12_MODEL_NOT_FITTED","source_qa_gate":q.get("source_support_gate")}
    try:
        if q.get("source_support_gate")!="PASS_GRAIN_ONLY":
            raise ValueError("NO_GO_SOURCE_GRAIN_SUPPORT")
        results=fit_stage12(d)
    except Exception as e:
        results={"status":"NO_GO_FROZEN_STAGE12_ORIGINAL_SOURCE_MODEL",
                 "reason":type(e).__name__+": "+str(e),
                 "source_qa_gate":q.get("source_support_gate"),
                 "no_effect_estimate_promoted":True}
        raise
    finally:
        out.write_text(json.dumps(results,indent=2,ensure_ascii=False,allow_nan=False))
        print("STAGE12_REAL_ORIGINAL_MOVEMENT_INTERACTION "+
              json.dumps(results,ensure_ascii=False,allow_nan=False),flush=True)
    return results

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--out",default="stage12_original")
    run(p.parse_args().out)
