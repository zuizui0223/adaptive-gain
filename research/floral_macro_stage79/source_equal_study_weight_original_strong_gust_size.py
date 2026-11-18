"""Stage79K: equal-Study weighting for size×strong-gust macro observational score.

Because Stage79J showed one source publication contains 81.07% of total
Fisher null information across 37 source networks (effective Nstudy 1.51),
this is a prospectively motivated *fragility diagnostic*, not a new primary
hypothesis test. Normalize original null information to sum to ONE within
each original publication BEFORE study-FE regression. This allows sources
rather than prolific original plant encounter counts to dominate.

Contrast primary original Fisher-weighted gust15 estimate vs equal-Study
weighted estimate, while holding actual original field networks, true bee
observed records, and ERA5 exposure fixed. Also report distribution of
simple within-study gust-to-network-null-score slopes where source wind
actually varies within a study, but do not call these causal independent
ecological treatment effects or bird/bee receptor-level cue use.
"""
from __future__ import annotations
import argparse,csv,json,math
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from source_sizefirst_gust_threshold_study_sensitivity import (
    read,join_original_source
)

MAIN="exposure_gust15_primary"
FORMULA="original_source_width_null_score_ratio ~ "+MAIN+" + z_temperature + z_precipitation + C(Study_id)"
MIN_STUDIES=10
MIN_WIND_VARYING=5

def normalize_original_studies(x):
    x=x.copy()
    base=x["original_source_width_local_null_information"]
    study_total=x.groupby("Study_id")["original_source_width_local_null_information"].transform("sum")
    if (study_total<=0).any():
        raise ValueError("STAGE79K_ORIGINAL_STUDY_WITH_ZERO_SOURCE_INFORMATION")
    x["source_equal_study_information_weight"]=base/study_total
    total=x.groupby("Study_id")["source_equal_study_information_weight"].sum()
    if not np.allclose(total.to_numpy(),1.,rtol=1e-10):
        raise ValueError("STAGE79K_SOURCE_STUDY_WEIGHTS_NOT_NORMALIZED")
    return x

def descriptive_fit(df,weight_column):
    formula=FORMULA
    model=smf.wls(formula,df,weights=df[weight_column]).fit()
    rank=int(np.linalg.matrix_rank(model.model.exog))
    if rank!=len(model.params):
        return {"status":"NO_GO_SOURCE_STUDY_FE_RANK_DEFICIENT"}
    robust=model.get_robustcov_results(cov_type="cluster",groups=df["Study_id"])
    i=list(model.params.index).index(MAIN)
    return {
      "status":"DESCRIPTIVE_NULL_SCORE_STUDY_CLUSTER_WLS",
      "original_observational_networks":len(df),
      "source_original_independent_publications":df.Study_id.nunique(),
      "source_frozen_main_gust_threshold":"daily max 10m ERA5 gust >=15m/s",
      "source_formula":formula,
      "source_weight_column":weight_column,
      "source_gust15_moderation_coefficient_per_10_percentage_points":float(robust.params[i]),
      "source_original_study_cluster_95_interval_not_causal":[float(v) for v in robust.conf_int()[i]],
      "source_R2_not_equivalent_causal_fitness":float(model.rsquared),
      "source_repeated_original_species_and_study_effort_NOT_independent":True,
    }

def within_study_simple_slopes(df):
    studies=[]
    for name,grp in sorted(df.groupby("Study_id"),key=lambda x:x[0]):
        if len(grp)<2:continue
        wind=grp[MAIN].to_numpy(dtype=float)
        outcome=grp["original_source_width_null_score_ratio"].to_numpy(dtype=float)
        weight=grp["original_source_width_local_null_information"].to_numpy(dtype=float)
        if np.max(wind)-np.min(wind)<0.1:continue
        w=weight/weight.sum()
        mw=np.sum(w*wind);my=np.sum(w*outcome)
        den=np.sum(w*(wind-mw)**2)
        if den<=0:continue
        studies.append({
           "Study_id":name,"original_informative_networks":len(grp),
           "original_within_study_gust15_range_per_10pp":[float(min(wind)),float(max(wind))],
           "source_simple_original_within_study_null_score_gust_slope":float(np.sum(w*(wind-mw)*(outcome-my))/den),
           "source_study_fraction_of_global_Fisher_information":float(weight.sum()/df["original_source_width_local_null_information"].sum()),
           "source_not_adjusted_for_network_TP_climate_or_taxon":True,
        })
    return studies

def run(exposure,nulls):
    df,coverage=join_original_source(exposure,nulls)
    varying=int((df.groupby("Study_id")[MAIN].agg(["size","std"])
       .pipe(lambda d:((d["size"]>=2)&(d["std"].fillna(0)>1e-7))).sum()))
    if len(df)!=37 or df.Study_id.nunique()!=15 or varying<MIN_WIND_VARYING:
        raise ValueError("STAGE79K_ORIGINAL_STUDY_GUST_INFORMATIVE_FRAME_NOT_FROZEN")
    e=normalize_original_studies(df)
    original=descriptive_fit(e,"original_source_width_local_null_information")
    equal=descriptive_fit(e,"source_equal_study_information_weight")
    if original["status"]!=equal["status"] or original["status"]!="DESCRIPTIVE_NULL_SCORE_STUDY_CLUSTER_WLS":
        raise ValueError("STAGE79K_STUDY_FE_DESCRIPTIVE_FIT_UNIDENTIFIED")
    influences=within_study_simple_slopes(e)
    vals=[v["source_simple_original_within_study_null_score_gust_slope"] for v in influences]
    return {
       "schema":"stage79k_original_petal_width_gust15_Bombus_equal_publication_robustness",
       "source_original_pre_bee_ERA5_networks":coverage["source_original_PRE_Bee_ERA5_networks"],
       "source_original_size_guild_informative_networks":coverage["source_original_STRICT_bee_informative_Width_networks"],
       "source_original_studies":coverage["source_original_independent_study_groups"],
       "source_frozen_primary_15ms_threshold":True,
       "source_information_WEIGHTED_original_score_tendency":original,
       "source_equal_STUDY_weighted_score_tendency":equal,
       "source_equal_publication_weight_displays_within_study_GUST_variation":varying,
       "source_within_study_raw_size_gust_slopes":influences,
       "source_within_study_raw_slopes_n":len(vals),
       "source_within_study_raw_slopes_positive":sum(x>0 for x in vals),
       "source_within_study_raw_slopes_negative":sum(x<0 for x in vals),
       "source_original_bee_visitors_Not_phylogenetic_replicates":True,
       "source_true_visual_cue_order_effect_IDENTIFIED":False,
       "source_VOC_wind_plume_path_IDENTIFIED":False,
       "source_whole_flower_visual_display_MEASURED":False,
       "study_equal_weight_is_not_new_confirmatory_hypothesis":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-ERA5-gust-exposure",type=Path,required=True)
    p.add_argument("--original-size-null-scores",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    result=run(read(a.original_ERA5_gust_exposure),read(a.original_size_null_scores))
    a.outdir.mkdir(parents=True,exist_ok=True)
    (a.outdir/"stage79k_original_equal_study_weight_strong_gust_size_source.json").write_text(
        json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE79K_ORIGINAL_EQUAL_PUBLICATION_GUST15_SIZE_BOMBUS_SCORE",
          json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
