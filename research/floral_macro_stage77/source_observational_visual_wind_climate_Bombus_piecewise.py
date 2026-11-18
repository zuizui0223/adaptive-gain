"""Stage77B observational MACRO piecewise path-screen for floral signals × Bombus.

This is NOT a causal structural equation model or identified odor mediation.
Real source: 59,369 source botanical TEXT descriptors (NO photos, NO direct UV
guide), 18,798 original species×field network source-positive visitor units,
and original corrected 623,476 real insect visits over 54 studies.
Source independent WorldClim 2.1 1970–2000 monthly climate NORMALS W,T,P,VAPR,
SRAD at the same 1,864 network locations via verified Stage77A artifact.

DAG of OBSERVATIONAL ASSOCIATIONS only:
 (W, T, P) -> V := share of single-explicit-hue YELLOW source plant names
 (V, W, V×W, T, P) -> B := realized STRICT species bee Bombus/other-bee logit
                         controlling source study fixed effects.

Both Vs are measured in a visitor-conditioned plant sample, not an
exhaustive plant community or field measured pollinator receptor contrast.
B is realized recorded visitors, NOT Bombus SDM range/availability or true
absence. Scent VOC is UNOBSERVED in common 54-study network units.
Wind is coarse 1970-2000 climate, NOT actual plume or wind manipulation.
These are descriptive study-cluster-sensitive source associations.
P-values/CI do not establish evolutionary adaptation or causal mediation.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage75"))
from authentic_continental_text_signal_guild_macro import source_text_trait,key

SOURCES={
 "nhm":"b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a",
 "network":"475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617",
 "climate":"948ac0ecbcfc9b8a2e810753748a5436d998cd586574ea185c6da5db08cbce53",
 "climate_receipt":"c01268ed200ad20da7f16888c041fcd71a47cad8f21dde58cc27309d08e45af5",
}
CLIM={
 "wind":"WorldClim1970_2000_observed_month_mean_wind_speed_m_s",
 "temperature":"WorldClim1970_2000_observed_month_mean_temperature_C",
 "precipitation":"WorldClim1970_2000_observed_month_mean_precipitation_mm_month",
 "srad":"WorldClim1970_2000_observed_month_mean_solar_radiation_kJ_m2_day",
 "vapr":"WorldClim1970_2000_observed_month_mean_water_vapour_pressure_kPa",
}
MIN_STUDIES=10
MIN_PRIMARY_HUE_SPECIES=2
PRIMARY_CONTRASTING_FAMILY_COUNT=2
MODEL_FORMULA_V="visual_reported_yellow_logodds ~ z_wind + z_temperature + z_precipitation + C(Study_id)"
MODEL_FORMULA_B="Bombus_observed_bee_logodds ~ visual_reported_yellow_logodds * z_wind + z_temperature + z_precipitation + C(Study_id)"
SENS_FORMULA_B="Bombus_observed_bee_logodds ~ visual_reported_yellow_logodds * z_wind + z_vapr + z_srad + C(Study_id)"
SECONDARY_FORMULA_B="Bombus_observed_bee_logodds ~ visual_reported_yellow_logodds * z_wind + z_temperature + z_precipitation + C(Study_id)"

def verify(path,want):
    h=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if h!=want:raise ValueError("STAGE77B_SOURCE_ARTIFACT_SHA256_CHANGED")
    return h

def load(path):
    with Path(path).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def build_original_positive_visual_networks(nhm,observed):
    if len(nhm)!=59369 or len(observed)!=18798:
        raise ValueError("STAGE77B_ORIGINAL_MACRO_59369_18798_SOURCE_GRAIN_CHANGED")
    targets={key(r["Original_plant_accepted_name_literal"]) for r in observed}
    if len(targets)!=1408:
        raise ValueError("STAGE77B_ORIGINAL_1408_PLANTS_CHANGED")
    hue={}
    for plant in nhm:
        tax=key(plant["taxon"])
        if tax not in targets:continue
        report=source_text_trait(plant)
        if report["source_exclusive_lexical_hue"]:
            hue[tax]=report["source_exclusive_lexical_hue"]
    if len(hue)!=233:
        raise ValueError("STAGE77B_ORIGINAL_233_SINGLE_HUE_SOURCE_SPECIES_CHANGED")
    data=[]
    for plant in observed:
        tax=key(plant["Original_plant_accepted_name_literal"])
        if tax not in hue:continue
        data.append({
          "Study_id":plant["Study_id"],"Network_id":plant["Network_id"],
          "Year":plant["Year_from_original_date"],
          "species":tax,"source_reported_single_hue":hue[tax],
          "source_is_actual_spatial_UV_pattern_measurement":False,
          "source_flowering_plant_unvisited_absence_known":False,
        })
    if len(data)!=2523:
        raise ValueError("STAGE77B_ORIGINAL_2523_RECORDED_SINGLE_HUE_NETWORK_ROWS_CHANGED")
    df=pd.DataFrame(data)
    k=("Study_id","Network_id","Year")
    if df.duplicated(list(k)+["species"]).any():
        raise ValueError("STAGE77B_ORIGINAL_SOURCE_PLANT_NETWORK_DUPLICATED")
    df["is_yellow"]=(df.source_reported_single_hue=="yellow").astype(int)
    agg=df.groupby(list(k),sort=True).agg(
       n_reported_hue_species=("species","nunique"),
       n_yellow_reported_species=("is_yellow","sum"),
       n_distinct_reported_hue_families=("source_reported_single_hue","nunique"),
       n_distinct_reported_genera=("species",lambda x: len({s.split()[0] for s in x})),
    ).reset_index()
    if len(agg)!=1178 or (agg.n_reported_hue_species>=2).sum()!=625 or (
        agg.n_distinct_reported_hue_families>=2).sum()!=424:
        raise ValueError("STAGE77B_ORIGINAL_1178_625_424_COLOR_ASSEMBLY_RECOUNT_CHANGED")
    return agg,{"original_visual_hue_taxa":len(hue),
                "original_visual_source_plant_network_units":len(data),
                "original_study_network_year_keys_with_any_reported_single_hue":len(agg),
                "original_network_keys_with_two_reported_hue_species":
                    int((agg.n_reported_hue_species>=2).sum()),
                "original_network_keys_with_two_DISTINCT_reported_hue_states":
                    int((agg.n_distinct_reported_hue_families>=2).sum()),
                "no_original_source_field_spectrometer_UV_nectarguide_measurement":True}

def make_path_frame(visual,worldclim):
    field=pd.DataFrame(worldclim)
    if len(field)!=1864 or field.Study_id.nunique()!=54:
        raise ValueError("STAGE77B_ORIGINAL_1864_NETWORK_54_STUDY_SITES_CHANGED")
    if field.duplicated(["Study_id","Network_id","Year"]).any():
        raise ValueError("STAGE77B_ORIGINAL_FIELD_SITE_DUPLICATE_ID")
    out=visual.merge(field,on=["Study_id","Network_id","Year"],
                     how="left",validate="one_to_one",indicator=True)
    if not (out["_merge"]=="both").all():
        raise ValueError("STAGE77B_SOURCE_VISUAL_NETWORK_WITHOUT_SOURCE_FIELD_SITE")
    out.drop(columns=["_merge"],inplace=True)
    for a,b in {
       "B":"source_actual_strict_species_rank_Bombus_records",
       "O":"source_actual_strict_species_rank_other_bees_records"}.items():
        out[a]=pd.to_numeric(out[b],errors="raise")
        if (out[a]<0).any():raise ValueError("STAGE77B_NEGATIVE_ORIGINAL_SOURCE_BEE_RECORD")
    out["n_strict_recorded_bees"]=out["B"]+out["O"]
    out["visual_reported_yellow_logodds"]=np.log(
          (out.n_yellow_reported_species+0.5)/
          (out.n_reported_hue_species-out.n_yellow_reported_species+0.5))
    out["Bombus_observed_bee_logodds"]=np.log((out.B+0.5)/(out.O+0.5))
    for new,source in CLIM.items():
        out["clim_"+new]=pd.to_numeric(out[source],errors="coerce")
    return out

def to_sample(df,mode):
    if mode=="cross_hue":
        return df.loc[(df.n_reported_hue_species>=2)&
                  (df.n_distinct_reported_hue_families>=2)].copy()
    if mode=="two_species":
        return df.loc[df.n_reported_hue_species>=2].copy()
    if mode=="any_reported_hue":
        return df.copy()
    raise ValueError("STAGE77B_UNKNOWN_PREOUTCOME_NETWORK_VISUAL_FRAME")

def standardized_within_preoutcome(pre,columns=("wind","temperature","precipitation","srad","vapr")):
    available=pre.dropna(subset=["clim_"+x for x in columns]).copy()
    means={}
    scales={}
    for var in columns:
        x=available["clim_"+var]
        sd=float(x.std(ddof=1))
        if sd<=0 or not np.isfinite(sd):
            raise ValueError("STAGE77B_ZERO_CLIMATE_SOURCE_VARIATION_"+var)
        means[var]=float(x.mean());scales[var]=sd
        available["z_"+var]=(x-means[var])/sd
    return available,{"source_climate_preoutcome_mean":means,
                      "source_climate_preoutcome_scale_sd":scales,
                      "source_never_restandardized_from_observed_Bombus_outcomes":True}

def study_within_variation(df,var):
    s=df.groupby("Study_id")[var].agg(["size","std"])
    return {
      "original_studies_in_frame":len(s),
      "original_studies_with_two_or_more_networks":int((s["size"]>=2).sum()),
      "original_studies_with_wind_difference_over_0_05_frame_SD":
          int((s["std"].fillna(0)>0.05*float(df[var].std())).sum()),
      "source_study_within_sd_median":float(s["std"].median()) if s["std"].notna().any() else None,
      "source_between_study_mean_sd":float(df.groupby("Study_id")[var].mean().std()) if len(s)>1 else None,
    }

def fit_descriptive_path(formula,data):
    fit=smf.ols(formula,data=data).fit()
    if len(data)<100 or data.Study_id.nunique()<MIN_STUDIES:
        raise ValueError("STAGE77B_SAMPLE_TOO_SMALL_FOR_SOURCE_STUDY_PATH_DIAGNOSTIC")
    cov=fit.get_robustcov_results(cov_type="cluster",groups=data["Study_id"],
                                  use_correction=True)
    coefs=[]
    for name,value,err,lower,upper in zip(fit.params.index,cov.params,
                                          cov.bse,*cov.conf_int().T):
        if name.startswith("C(Study_id)"):
            continue
        coefs.append({"term":name,"estimate_equal_source_network_weight":float(value),
             "study_cluster_robust_se_descriptive":float(err),
             "study_cluster_robust_sampling_interval_95_descriptive":[float(lower),float(upper)],
             "NOT_confirmatory_causal_or_phylogenetic_effect":True})
    return fit,{"source_descriptive_path_formula":formula,
            "observational_network_units":len(data),
            "source_independent_study_ID_groups":data.Study_id.nunique(),
            "ordinary_network_equal_weight_OLS_R2_descriptive":float(fit.rsquared),
            "source_design_matrix_columns":len(fit.params),
            "source_design_matrix_rank":int(np.linalg.matrix_rank(fit.model.exog)),
            "source_condition_number":float(fit.condition_number),
            "observed_coefficient_and_cluster_sampling_intervals":coefs,
            "cluster_robust_interval_NOT_causal_SEM_interval":True,
            "source_species_and_study_observation_process_unidentified":True}

def leave_study_out(formula,data,terms):
    base=smf.ols(formula,data).fit()
    orig=base.params
    tests=[]
    for study in sorted(data.Study_id.unique()):
        keep=data.loc[data.Study_id!=study]
        if keep.Study_id.nunique()<MIN_STUDIES:continue
        try:f=smf.ols(formula,keep).fit()
        except Exception:continue
        tests.append({"excluded_Study_id":study,
            **{name:float(f.params.get(name,float("nan"))) for name in terms}})
    return {
       "source_study_leave_one_out_n":len(tests),
       "source_study_leave_one_out_terms":{term:{
           "full_data_estimate":float(orig.get(term,float("nan"))),
           "leave_study_out_range_min":min(x[term] for x in tests) if tests else None,
           "leave_study_out_range_max":max(x[term] for x in tests) if tests else None,
           "leave_study_out_sign_flips":
             sum((x[term]>0)!=(orig.get(term,0)>0) for x in tests),
         } for term in terms},
       "site_n_study_exclusion_does_not_make_species_independent":True}

def audit(nhm,network,climate,climate_receipt):
    visual,frame=build_original_positive_visual_networks(nhm,network)
    full=make_path_frame(visual,climate)
    c=climate_receipt
    if not (c["climate_is_longterm_normal_NOT_coincident_original_visit_weather"] and
            c["site_climate_coverage"]["networks_with_5climate_annual"]==1858 and
            c["VOC_emissions_and_same_site_scent_not_measured_here"]):
        raise ValueError("STAGE77B_ORIGINAL_WIND_FROM_1970_2000_NOT_VERIFIED")
    diagnostics={}
    for name in ("cross_hue","two_species","any_reported_hue"):
        pre=to_sample(full,name)
        pre_clim,standard=standardized_within_preoutcome(pre)
        withbees=pre_clim.loc[pre_clim.n_strict_recorded_bees>0].copy()
        wind_corr=pre_clim[
            ["clim_"+v for v in CLIM]].corr().to_dict()
        summary={
         "source_base_frame_unconditioned_on_recorded_Bombus":len(pre),
         "source_studies_before_Bombus_admission":pre.Study_id.nunique(),
         "source_networks_5_climatology_monthly":len(pre_clim),
         "source_studies_with_monthly_climatology":pre_clim.Study_id.nunique(),
         "source_networks_with_any_strict_recorded_bee_after_preselection":len(withbees),
         "source_studies_with_strict_bees":withbees.Study_id.nunique(),
         "source_study_variation_in_wind_normal":
             study_within_variation(pre_clim,"clim_wind"),
         "original_wind_temperature_and_vapour_covariation_matrix":wind_corr,
         "pre_Bombus_source_climate_standardization":standard,
         "source_Bombus_absent_records_NOT_true_Bombus_absence":True,
         "source_hues_are_positive_taxon_descriptions_NOT_field_UV":True,
         "source_wind_climatology_not_instantaneous_source_odor_plume":True,
        }
        if name=="cross_hue":
            if len(pre)!=424 or pre.Study_id.nunique()!=43:
                raise ValueError("STAGE77B_ORIGINAL_STAGE75_424_43_MAIN_FRAME_CHANGED")
            if len(withbees)<100:
                raise ValueError("STAGE77B_NO_USABLE_GUILD_VISUAL_MACRO_COHORT")
            vf,visual_result=fit_descriptive_path(MODEL_FORMULA_V,pre_clim)
            bf,bee_result=fit_descriptive_path(MODEL_FORMULA_B,withbees)
            sbf,sens_bee=fit_descriptive_path(SENS_FORMULA_B,withbees)
            summary.update({
              "model_V_climate_to_positive_reported_color_composition":visual_result,
              "model_B_climate_wind_visual_to_realized_Bombus_recorded_share":bee_result,
              "model_B_srad_vapr_instead_of_highly_collinear_T":sens_bee,
              "study_leave_out_visual_to_Bombus_and_wind_interaction":
                 leave_study_out(MODEL_FORMULA_B,withbees,[
                   "visual_reported_yellow_logodds","z_wind",
                   "visual_reported_yellow_logodds:z_wind"]),
              "VOC_to_Bombus_path":"NOT_IDENTIFIED_NO_COMMON_ORIGINAL_SAME_SITE_VOC",
              "wind_to_VOC_to_Bombus_indirect_path":"NOT_IDENTIFIED_NO_SAME_SITE_VOC_PLUME",
              "wind_moderates_visual_to_Bombus_causal_path":"NOT_IDENTIFIED_SOURCE_CLIMATOLOGY_AND_TAXON_STUDY_CONFOUND",
              "source_observational_piecewise_path_SCREEN_ONLY":True,
              "confirmed_phylogenetic_adaptation_or_causal_SEM_fitted":False,
            })
        diagnostics[name]=summary
    return {
       "schema":"stage77b_original_EuPPollNet_WorldClim_NHM_visual_Bombus_wind_environment_observational_piecewise",
       "original_NHM_botanical_source_lexical_colour":True,
       "original_EuPPollNet_visits_observed_not_range_model":True,
       "original_climatological_Wind_T_P_VAPR_SRAD":True,
       "source_Europe_study_networks":1864,
       "source_original_study_IDs":54,
       "source_positive_lexical_hue_plant_network_audit":frame,
       "source_environment_path_macro_models":diagnostics,
       "source_scent_VOC_availability_in_same_54_Europe_studies":0,
       "odor_wind_visual_three_modal_causal_mediation_identifiable":False,
       "source_richer_direct_scent_studies_not_grafted_as_site_climate_VOC":True,
       "source_site_year_actual_instantaneous_wind_recorded":False,
       "new_global_Bombus_SDM_or_phylogenetic_effect_estimated":False,
       "source_mediator_plume_latent_with_no_indicators_is_unidentified":True,
       "no_external_island_botanical_data_in_model":True,
    }

def native_numeric_json(value):
    # Source scientific output uses NumPy/Pandas scalar integers. Do not
    # stringify these and lose machine-readable quantitative receipts.
    if isinstance(value,np.integer):return int(value)
    if isinstance(value,np.floating):return float(value)
    if isinstance(value,np.bool_):return bool(value)
    if isinstance(value,np.ndarray):return value.tolist()
    raise TypeError(f"unsupported scientific result JSON value: {type(value).__name__}")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-NHM",required=True,type=Path)
    p.add_argument("--source-original-networks",required=True,type=Path)
    p.add_argument("--source-worldclim-sites",required=True,type=Path)
    p.add_argument("--source-worldclim-receipt",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    for label,path in (("nhm",a.source_NHM),("network",a.source_original_networks),
        ("climate",a.source_worldclim_sites),
        ("climate_receipt",a.source_worldclim_receipt)):
        verify(path,SOURCES[label])
    d=audit(load(a.source_NHM),load(a.source_original_networks),
            load(a.source_worldclim_sites),json.loads(a.source_worldclim_receipt.read_text()))
    a.outdir.mkdir(exist_ok=True,parents=True)
    (a.outdir/"original_worldclim_flower_visual_Bombus_piecewise_path_screen.json").write_text(
        json.dumps(d,indent=2,sort_keys=True,ensure_ascii=False,default=native_numeric_json)+"\n",encoding="utf-8")
    main=d["source_environment_path_macro_models"]["cross_hue"]
    print("STAGE77B_REAL_CLIMATE_ADJUSTED_VISUAL_BOMBUS_OBSERVATIONAL_PATH_SCREEN",
          json.dumps({
              "source":d["source_positive_lexical_hue_plant_network_audit"],
              "n_source_networks_before_Bombus":main["source_base_frame_unconditioned_on_recorded_Bombus"],
              "n_source_networks_after_Bombus":main["source_networks_with_any_strict_recorded_bee_after_preselection"],
              "source_studies":main["source_studies_with_strict_bees"],
              "study_wind_variability":main["source_study_variation_in_wind_normal"],
              "model_V":main["model_V_climate_to_positive_reported_color_composition"],
              "model_B":main["model_B_climate_wind_visual_to_realized_Bombus_recorded_share"],
              "model_B_secondary":main["model_B_srad_vapr_instead_of_highly_collinear_T"],
              "leave_study_out":main["study_leave_out_visual_to_Bombus_and_wind_interaction"],
              "source_UNMEASURED_scent":d["source_scent_VOC_availability_in_same_54_Europe_studies"],
              "scent_mediation_identifiable":d["odor_wind_visual_three_modal_causal_mediation_identifiable"]
          },sort_keys=True,default=native_numeric_json))
    print("NOT_CAUSAL_PATH_SEM_NO_SITE_WIND_NO_VOC_AND_NO_VISUAL_UV_SPECTRA")
if __name__=="__main__":
    main()
