"""Stage81F: actual Stage79I ERA5 gust x Stage81C REAL flower-age data overlap.

Inputs are original source SHA-locked artifacts, NOT Monte Carlo/synthetic
and NOT claimed optical sensor choice, olfactory plume, or wind at bee landing.
Stage79I cohort was selected on documented floral petal widths, not source
flower-age spectral effect or original observed guild outcomes.
Stage81C score is a first-order binomial NULL score U/I for species-constant
RAW early-to-late age spectral RMS in Japan vs observed EuPP bees in Europe.
Data overlap gives a weak, publication-dominated observational screening
coefficient, NOT a biological wind x information route causal effect.

Author EuPP source paper split one study across IDs 23,24,25. Group these
for interval clustering, keep ID-level nuisance fixed effects.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
ORIGINAL_ERA5_151_SHA="1188e639593437f07c8eaa559730d845269d9b1d2abca52917b7bbd6c2315f90"
ORIGINAL_AGE_BEE_194_SHA="ddc3d56e536b34e7a31f78f0a4f9013739bc732d69c9d294151dec303bcb86ca"
JOIN=("Study_id","Network_id","Year")
WIND="original_ERA5_fraction_days_10m_gust_ge_15_ms"
SOURCE_N_PRE_ERA5=151
SOURCE_N_AGE_INFORMATIVE=194
ORIGINAL_INTERSECTION_NETWORKS=36
ORIGINAL_INTERSECTION_IDS=17
ORIGINAL_INTERSECTION_PUBLICATIONS=16
EXPECTED_WIND_VARYING_PUBLICATIONS=8

def source_frame(path, expected_sha):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_sha:
        raise ValueError("STAGE81F_GENUINE_ORIGINAL_SOURCE_CSV_SHA_CHANGED")
    return pd.read_csv(path)

def publication_id(study):
    src=str(study)
    if src.split("_")[0] in {"23","24","25"}:
        return "23_24_25_ONE_PUBLISHED_STUDY"
    return src

def original_frozen_overlap(era5,age):
    if len(era5)!=SOURCE_N_PRE_ERA5 or len(age)!=SOURCE_N_AGE_INFORMATIVE:
        raise ValueError("STAGE81F_INDEPENDENT_REAL_SOURCE_COHORT_COUNTS_CHANGED")
    e=era5.copy();b=age.copy()
    # Original age file Year_from_original_date is the source year (not capture era)
    e["Year"]=e["Year"].astype(str)
    b["Year"]=b["Year_from_original_date"].astype(str)
    if e.duplicated(list(JOIN)).any() or b.duplicated(list(JOIN)).any():
        raise ValueError("STAGE81F_ORIGINAL_NETWORK_YEAR_KEY_NOT_UNIQUE")
    for name,col in (("temperature","original_ERA5_period_daily_T_mean_C"),
                     ("precipitation","original_ERA5_period_precip_mm_per_day")):
        v=pd.to_numeric(e[col],errors="raise")
        if not np.isfinite(v).all() or v.std(ddof=1)<=0:
            raise ValueError("STAGE81F_ORIGINAL_151_SOURCE_ENVIRONMENT_INVALID")
        # Freeze climate standardization on all 151 weather exposures BEFORE
        # reading the 194 bee-guild outcomes or selecting source 36 overlaps.
        e["z_"+name]=(v-v.mean())/v.std(ddof=1)
    e["gust15pp"]=pd.to_numeric(e[WIND],errors="raise")*10.
    x=e.merge(b,on=list(JOIN),how="inner",validate="one_to_one",suffixes=("_wind","_age"))
    x["published_study"]=x.Study_id.map(publication_id)
    if (len(x)!=ORIGINAL_INTERSECTION_NETWORKS or
       x.Study_id.nunique()!=ORIGINAL_INTERSECTION_IDS or
       x.published_study.nunique()!=ORIGINAL_INTERSECTION_PUBLICATIONS):
        raise ValueError("STAGE81F_ORIGINAL_STRICT_36_SOURCE_OVERLAP_CHANGED")
    if x.published_study.groupby(x.published_study).nunique().empty:
        raise ValueError("STAGE81F_INVALID_PUBLICATION_IDS")
    for field in ("source_null_ratio_U_over_I_not_fitted_beta",
                  "source_I_local_null_fisher_information","gust15pp"):
        x[field]=pd.to_numeric(x[field],errors="raise")
        if not np.isfinite(x[field]).all():raise ValueError("STAGE81F_NONFINITE_SOURCE_DATA")
    if (x["source_I_local_null_fisher_information"]<=0).any():
        raise ValueError("STAGE81F_SOURCE_NULL_INFORMATION_NOT_POSITIVE")
    vary=(x.groupby("published_study")["gust15pp"].agg(["size","nunique"]))
    n_vary=int(((vary["size"]>=2)&(vary["nunique"]>=2)).sum())
    if n_vary!=EXPECTED_WIND_VARYING_PUBLICATIONS:
        raise ValueError("STAGE81F_STUDY_WIND_VARIABILITY_SUPPORT_CHANGED")
    return x,n_vary

def source_wls(x,formula,weights):
    model=smf.wls(formula,x,weights=weights).fit()
    if int(np.linalg.matrix_rank(model.model.exog))!=len(model.params):
        return {"status":"NO_GO_RANK_DEFICIENT"}
    robust=model.get_robustcov_results(cov_type="cluster",groups=x["published_study"])
    i=list(model.params.index).index("gust15pp")
    return {
      "status":"DESCRIPTIVE_ORIGINAL_SOURCE_STUDY_CLUSTER_GUST_AGE_NULLSCORE",
      "source_formula":formula,
      "estimate_per_10pp_days_gust_ge_15mps":float(robust.params[i]),
      "publication_cluster_95_descriptive_interval":[float(v) for v in robust.conf_int()[i]],
      "source_original_study_nuisance_fixed_effects":True,
      "source_not_fitted_binomial_or_biological_behavior_effect":True,
      "source_dof_nuisance":int(model.df_resid),
    }

def analyze(era5,age):
    x,n_vary=original_frozen_overlap(era5,age)
    x["response"]=x["source_null_ratio_U_over_I_not_fitted_beta"]
    w=x.source_I_local_null_fisher_information
    weightpub=w/x.groupby("published_study")["source_I_local_null_fisher_information"].transform("sum")
    formula="response ~ gust15pp + z_temperature + z_precipitation + C(Study_id)"
    frac=x.groupby("published_study")["source_I_local_null_fisher_information"].sum()
    frac=frac/frac.sum()
    output={
       "schema":"stage81f_36_actual_source_networks_age_spectral_RMS_vs_ERA5_gust15",
       "original_source_ERA5_151_networks":len(era5),
       "original_source_age_receiver_guild_194_networks":len(age),
       "original_source_matched_floral_age_plus_strict_bee_guild_plus_ERA5":len(x),
       "original_source_unique_Study_id":x.Study_id.nunique(),
       "original_source_unique_real_publications":x.published_study.nunique(),
       "within_publication_gust_varying":n_vary,
       "source_original_information_largest_published_study_fraction":float(frac.max()),
       "source_original_information_effective_published_studies":float(1/(frac*frac).sum()),
       "primary_source_era5_gust15_age_RMS_information_weighted":source_wls(x,formula,w),
       "study_equal_source_era5_gust15_age_RMS":source_wls(x,formula,weightpub),
       "original_source_no_temperature_precip_adjustment_sensitivity":
          source_wls(x,"response ~ gust15pp + C(Study_id)",w),
       "wind_exposure_is_study_month_10m_ERA5_max_daily_gust_not_visited_flower_instant":True,
       "source_SPECTRA_Japan_EuPP_VISITS_Europe_not_same_site":True,
       "source_original_age_RMS_not_true_honeybee_perceptual_hex_distance":True,
       "source_flower_counts_detectability_and_botanical_phylogeny_uncontrolled":True,
       "source_no_bee_learning_cue_order_odor_plume_or_landing_measurements":True,
       "no_significant_wind_by_spectral_age_mechanism_confirmed":True,
    }
    if x.published_study.nunique()!=16:raise ValueError("NOT_16_ORIGINAL_PUBLICATIONS")
    return output,x
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--stage79i-era5-source",type=Path,required=True)
    ap.add_argument("--stage81c-age-guild-source",type=Path,required=True)
    ap.add_argument("--outdir",type=Path,required=True)
    opt=ap.parse_args()
    out,x=analyze(source_frame(opt.stage79i_era5_source,ORIGINAL_ERA5_151_SHA),
                  source_frame(opt.stage81c_age_guild_source,ORIGINAL_AGE_BEE_194_SHA))
    opt.outdir.mkdir(parents=True,exist_ok=True)
    (opt.outdir/"stage81f_original_gust15_36_age_spectral_real_study_adjusted_readout.json").write_text(
       json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    x.to_csv(opt.outdir/"stage81f_36_real_original_matching_networks.csv",index=False)
    print("STAGE81F_ORIGINAL_REAL_GUST15_SPECTRAL_AGE_36_MACRO",
        json.dumps({k:v for k,v in out.items() if isinstance(v,(float,int))},sort_keys=True),flush=True)
if __name__=="__main__":
    main()
