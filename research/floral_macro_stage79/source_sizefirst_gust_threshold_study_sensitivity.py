"""Stage79J: REGISTRY-FIXED gust threshold/study influence sensitivity of petal width macro.

Read only authenticated original Stage79I 151 size-first ERA5 exposures and
37 original within-network strictly identified bee null score ratios (15
independent source study IDs). Predictions 10, 15, 20m/s daily MAX GUST and
daily gust p95 were frozen BEFORE observing guild outcomes.

WLS: y_k = U_k/I_k first-order within-field network size null score ratio.
Predictors: gust exceedance, mean daily T/precip in original visited calendar
months, source Study ID fixed effects. Weight source expected null information
I_k, robust covariance clustering original studies; this is NOT a fitted
binomial regression or causal pollination-effect. Study leave-one-out and
top-contribution show whether a few studies dominate.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

EXPOSURE_FIELDS={
 "gust10":"original_ERA5_fraction_days_10m_gust_ge_10_ms",
 "gust15_primary":"original_ERA5_fraction_days_10m_gust_ge_15_ms",
 "gust20":"original_ERA5_fraction_days_10m_gust_ge_20_ms",
 "gust95":"original_ERA5_daily_max_gust_p95_m_s",
}
REQUIRED_EXPOSURES=151
REQUIRED_SCORES=37
REQUIRED_STUDIES=15
PRE_FIXED_MIN_STUDIES_WITH_WIND_VARIABILITY=5

def read(path):
    with Path(path).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def join_original_source(exposures,scores):
    if len(exposures)!=REQUIRED_EXPOSURES or len(scores)!=REQUIRED_SCORES:
        raise ValueError("STAGE79J_TRUE_151_37_SIZE_FIRST_GUST_SOURCE_SAMPLE_CHANGED")
    fields=("Study_id","Network_id","Year")
    a=pd.DataFrame(exposures)
    b=pd.DataFrame(scores)
    if a.duplicated(list(fields)).any() or b.duplicated(list(fields)).any():
        raise ValueError("STAGE79J_DUPLICATED_REAL_SOURCE_STUDY_NETWORK_YEAR")
    if b.Study_id.nunique()!=REQUIRED_STUDIES:
        raise ValueError("STAGE79J_SOURCE_15_INDEPENDENT_STUDIES_CHANGED")
    pre=a.copy()
    for var in ("temperature","precipitation"):
        x=("original_ERA5_period_daily_T_mean_C" if var=="temperature"
           else "original_ERA5_period_precip_mm_per_day")
        v=pd.to_numeric(pre[x],errors="raise")
        scale=float(v.std())
        if scale<=0:raise ValueError("STAGE79J_SOURCE_ENVIRONMENT_HAS_NO_VARIATION")
        pre["z_"+var]=(v-float(v.mean()))/scale
    for k,v in EXPOSURE_FIELDS.items():
        pre["exposure_"+k]=pd.to_numeric(pre[v],errors="raise")*(
             1 if k=="gust95" else 10)
    x=b.merge(pre,on=list(fields),how="left",validate="one_to_one",indicator=True)
    if not (x["_merge"]=="both").all():
        raise ValueError("STAGE79J_GUILD_NETWORK_NOT_IN_SOURCE_PRESELECTED_ERA5_COHORT")
    x["original_source_width_null_score_ratio"]=pd.to_numeric(
        x["original_source_width_null_score_ratio"],errors="raise")
    x["original_source_width_local_null_information"]=pd.to_numeric(
        x["original_source_width_local_null_information"],errors="raise")
    if (x["original_source_width_local_null_information"]<=0).any():
        raise ValueError("STAGE79J_NONPOSITIVE_EXPECTED_NULL_INFORMATION")
    return x,{"source_original_PRE_Bee_ERA5_networks":len(pre),
       "source_original_STRICT_bee_informative_Width_networks":len(x),
       "source_original_independent_study_groups":b.Study_id.nunique(),
       "source_climate_scaling_defined_before_admitting_any_bee_outcome":True,
       "source_size_trait_not_same_field_population_measured":True,
       "source_null_score_ratio_not_actual_Bombus_preference_beta":True}

def robust_study_wls(x,windfield,check=True):
    wind=x[windfield]
    info={
      "source_wind_regressor":windfield,
      "original_source_no_gust_event_networks":int((wind==0).sum()),
      "within_source_study_wind_variation_groups":int((
          x.groupby("Study_id")[windfield].agg(["size","std"])
          .pipe(lambda d:(d["size"]>=2)&(d["std"].fillna(0)>1e-7))).sum()),
      "source_independent_study_count":x.Study_id.nunique(),
      "source_informative_networks":len(x),
    }
    if info["within_source_study_wind_variation_groups"]<PRE_FIXED_MIN_STUDIES_WITH_WIND_VARIABILITY:
        return {"status":"NO_GO_TOO_FEW_STUDIES_WITH_WITHIN_STUDY_GUST_VARIATION",**info}
    formula=("original_source_width_null_score_ratio ~ "+windfield+
             " + z_temperature + z_precipitation + C(Study_id)")
    fit=smf.wls(formula,x,weights=x["original_source_width_local_null_information"]).fit()
    rank=int(np.linalg.matrix_rank(fit.model.exog))
    if rank<len(fit.params):
        return {"status":"NO_GO_STUDY_FIXED_EFFECTS_RANK_DEFICIENT",
                **info,"source_columns":len(fit.params),"source_rank":rank}
    robust=fit.get_robustcov_results(cov_type="cluster",groups=x["Study_id"])
    idx=list(fit.params.index).index(windfield)
    est=float(robust.params[idx])
    ci=[float(y) for y in robust.conf_int()[idx]]
    info.update({
       "status":"EXPLORATORY_STUDY_CLUSTER_WEIGHTED_NULL_SCORE_GUST_TENDENCY",
       "source_formula":formula,
       "source_ERA5_climate_and_study_adjusted_gust_coefficient":est,
       "source_study_cluster_95_sampling_interval_NOT_causal":ci,
       "source_model_ordinary_R2_NOT_fitness":float(fit.rsquared),
       "source_null_information_weighted_source_studies":len(x.Study_id.unique()),
       "source_study_level_effect_NOT_full_phylogenetic_cluster":True,
       "source_gust_source_is_max_daily_ERA5_model_not_gust_at_bee_flight":True,
    })
    if not check:return info
    leave=[]
    for study in sorted(x.Study_id.unique()):
        subset=x.loc[x.Study_id!=study]
        if subset.Study_id.nunique()<10:continue
        sub=robust_study_wls(subset,windfield,check=False)
        if sub["status"]=="EXPLORATORY_STUDY_CLUSTER_WEIGHTED_NULL_SCORE_GUST_TENDENCY":
            leave.append((study,sub["source_ERA5_climate_and_study_adjusted_gust_coefficient"]))
    info["source_leave_one_study_out_replicates_successful"]=len(leave)
    info["source_leave_one_study_out_min_max"]=(
        [min(v for k,v in leave),max(v for k,v in leave)] if leave else None)
    info["source_leave_one_study_out_sign_flips"]=sum((v>0)!=(est>0) for k,v in leave)
    info["source_leave_one_study_out_value_by_study"]=[
      {"original_Study_id":k,"source_gust_tendency_without_study":v} for k,v in leave]
    return info

def analyze(exposure,source_score):
    x,source=join_original_source(exposure,source_score)
    bystudy=(x.groupby("Study_id")["original_source_width_local_null_information"]
       .agg(["sum","size"]).sort_values("sum",ascending=False))
    contributions=bystudy["sum"]/bystudy["sum"].sum()
    r={"schema":"stage79j_true_151_source_37_strict_bee_size_network_study_gust_robustness",
       "original_source_predefined_ERA5_thresholds":list(EXPOSURE_FIELDS),
       "source_original_preguild_frame":source,
       "source_source_null_information_concentration":{
          "largest_single_study_information_fraction":float(contributions.max()),
          "largest_three_studies_information_fraction":float(contributions.iloc[:3].sum()),
          "effective_independent_study_number_by_information_weights":
              float(1/(contributions.pow(2).sum())),
          "number_of_original_source_studies":len(bystudy),
          "original_source_study_cluster_not_independent_plant_phylogeny":True,
       },
       "original_gust_threshold_sensitivity":{
           k:robust_study_wls(x,"exposure_"+k) for k in EXPOSURE_FIELDS},
       "source_no_validated_colourchange_negative_or_UV_spatial_guide":True,
       "source_NO_same_site_VOC_scent_or_true_pollination_fitness":True,
       "source_no_adaptive_cue_order_inferred":True}
    return r

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--original-size-first-gust-exposures",type=Path,required=True)
    a.add_argument("--original-source-network-width-null-scores",type=Path,required=True)
    a.add_argument("--outdir",type=Path,required=True)
    arg=a.parse_args()
    result=analyze(read(arg.original_size_first_gust_exposures),
                   read(arg.original_source_network_width_null_scores))
    arg.outdir.mkdir(exist_ok=True,parents=True)
    (arg.outdir/"stage79j_original_petalwidth_gust_threshold_study_robustness.json").write_text(
        json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE79J_ORIGINAL_SIZE_FIRST_15mps_GUST_STUDY_ROBUSTNESS",
          json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
