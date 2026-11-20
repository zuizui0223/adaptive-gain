#!/usr/bin/env python3
"""Stage107 72 strictly mainland source exploratory flora × WorldClim mean wind.

Independent LONG-TERM MEAN WIND (WorldClim 2.1, 1970–2000, 10 arcmin) is
NOT 1991–2020 maximum wind gust >15 m/s; never substitute/compare slope
magnitudes. Original Stage87C source climate all 367 TDWG3 regions includes
48-point area-sampled mean (not exact area integral).

Use ONLY Stage98B source-original 72 contact-free mainland exploration areas.
Never fit any 37 heldout source floral outcomes or excluded 16 contact regions.
Examine separate NHM floral mark word-positive, original WFO explicit scent,
and rare original AusTraits source-labelled flower diameter, with botanical
documentation coverage confounders and climate covariates. Exploratory partial
rank correlation only, no IID p, no phylogenetic adaptation inference.
"""
from __future__ import annotations
import argparse,csv,io,json,math,sys,zipfile
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage105"))
from source_50point_wind_vs_flora_report_bias import (
    archive_member,train_source_split,rank_partial,spearman_safe)

SHA={
 "worldclim":"f2650b0b4a76220c9add1feb4dcc6f93f14ef7c3399976364bcc4160741508de",
 "source96":"99aaf623ac3a7f948c5d0cdad9a8ce8668c2131ee07af6fb5d02d81c573c3149",
 "source91":"f1197a050d110d1e3626ab01f3c5d49626ac32fd0588d41ce3a162b44d921cdf",
 "source92":"01d76457aa8423b7964b5fccdfea597f5c158a805c138fd8597e7efd1733a05f",
 "mainland72":"8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7",
 "gust33":"0d7cc6609c9ee3b85e24aafbbfd5dec307119506c4a4d5f79a579c21ed6c1534"}
MEMBERS={
 "worldclim":"stage87_original_global_TDWG3_NHM_WCVP_WorldClim_regions.csv",
 "source96":"stage96_native_367_original_floral_three_cue_source_availability.csv",
 "source91":"stage91_global_TDWG3_3cue_availability_INCLUDES_ISLANDS.csv",
 "source92":"stage92_AusTraits7_flower_diameter_367_regions_INCLUDES_ISLANDS.csv",
 "mainland72":"stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv",
 "gust33":"stage105_source_33_exploration_regions_ONLY_NO_HOLDOUT.csv"}

def safe_original_stage_train(source,train):
    items=list(csv.DictReader(io.StringIO(source.decode("utf-8-sig"))))
    keys={r["TDWG_L3"] for r in items}
    if len(items)!=367 or len(keys)!=367 or not set(train)<=keys:
        raise ValueError("STAGE107_ORIGINAL_367_REGION_CLIMATE_OR_FLORA_SOURCE_NOT_MATCHED")
    return {r["TDWG_L3"]:r for r in items if r["TDWG_L3"] in train}

def common_train_regions(wind,trait,colour,size,train):
    data=[]
    for code in sorted(train):
        w=wind[code];p=trait[code];c=colour[code];z=size[code]
        if w["source_all_5climate_variables_at_12_or_more_points"]!="1":
            continue
        n=int(p["n_native_source_species"])
        if n<=0 or n!=int(c["n_native"]) or n!=int(z["n_original_WCVP_native_species_in_region"]):
            raise ValueError("STAGE107_NATIVE_SOURCE_DENOMINATOR_CHANGED_"+code)
        missing=int(c["n_source_colour_missing"])
        color=n-missing
        desc=int(p["n_original_WFO_full_flora_description_species"])
        mark=int(p["n_positive_marking_TEXT_SOURCE_CANDIDATES"])
        positive=int(p["n_source_floral_fragrance_lexical_positive"])
        negative=int(p["n_source_floral_fragrance_lexical_explicit_negative"])
        if not (0<=mark<=color<=n and 0<=positive+negative<=desc<=n):
            raise ValueError("STAGE107_SOURCE_PROSE_NOT_PARTITIONED")
        size_n=int(z["n_original_AusTraits_flower_diameter_species"])
        size_med=float(z["diameter_median_mm_of_source_species"]) if z["diameter_median_mm_of_source_species"] else None
        value=float(w["worldclim_baseline_wind_m_s"])
        if not (0<=value<45):
            raise ValueError("STAGE107_WORLDCLIM_MEAN_NOT_MS_SOURCE")
        data.append({
          "TDWG_L3":code,"source_geographic_block":train[code]["spatial_block_id"],
          "WorldClim2_1_1970_2000_mean_wind_m_s_NOT_ERA5_gust":value,
          "source_region_sampling_latitude":float(w["region_sampling_latitude_mean"]),
          "WorldClim_1970_2000_mean_temperature_C":float(w["worldclim_baseline_mean_temperature_C"]),
          "WorldClim_1970_2000_precip_mm_month":float(w["worldclim_baseline_precip_mm_month"]),
          "WorldClim_original_wind_raster_valid_sampling_points":int(w["worldclim_baseline_wind_m_s_valid_points"]),
          "n_WCVP_native_source_species":n,
          "NHM_colour_field_description_coverage":color/n,
          "WFO_original_flora_description_coverage":desc/n,
          "floral_marking_lexical_report_per_native":mark/n,
          "floral_marking_lexical_report_per_colour_field_species":mark/color if color else None,
          "fragrance_positive_source_mention_per_flora_description":positive/desc if desc else None,
          "fragrance_positive_among_explicit_pos_and_neg":positive/(positive+negative) if positive+negative else None,
          "AusTraits_original_measured_grade_median_mm":size_med,
          "n_AusTraits_original_measured_size_species":size_n,
          "no_holdout_climate_or_floral_effect_fitted":"YES"})
    if len(data)!=72 or len({r["source_geographic_block"] for r in data})!=17:
        raise ValueError("STAGE107_NOT_EXACT_72_GEOGRAPHY_SOURCE_WIND_FRAME")
    return data

def rank_summary(rows):
    wind="WorldClim2_1_1970_2000_mean_wind_m_s_NOT_ERA5_gust"
    controls=("NHM_colour_field_description_coverage",
              "WFO_original_flora_description_coverage",
              "source_region_sampling_latitude",
              "WorldClim_1970_2000_mean_temperature_C",
              "WorldClim_1970_2000_precip_mm_month")
    outcomes={
       "near_visual_pattern_lexical_per_original_native":
            ("floral_marking_lexical_report_per_native",0),
       "near_visual_pattern_lexical_per_colour_described":
            ("floral_marking_lexical_report_per_colour_field_species",0),
       "chemical_floral_fragrance_report_per_WFO_description":
            ("fragrance_positive_source_mention_per_flora_description",0),
       "chemical_floral_fragrance_pos_over_explicit_pos_plus_neg":
            ("fragrance_positive_among_explicit_pos_and_neg",0),
       "far_visual_AusTraits_source_median_diameter_mm_n_at_least3":
            ("AusTraits_original_measured_grade_median_mm",3),
       "far_visual_AusTraits_source_median_diameter_mm_n_at_least10":
            ("AusTraits_original_measured_grade_median_mm",10),
       "SOURCE_NHM_colour_field_documentation_coverage":
            ("NHM_colour_field_description_coverage",0),
       "SOURCE_WFO_full_original_flora_description_coverage":
            ("WFO_original_flora_description_coverage",0)}
    result={}
    for name,(out,minsize) in outcomes.items():
        eligible=[r for r in rows if r[out] is not None and
           r["n_AusTraits_original_measured_size_species"]>=minsize]
        x=[r[wind] for r in eligible]
        y=[r[out] for r in eligible]
        cov=[[r[k] for r in eligible] for k in controls]
        result[name]={
          "n_source_regions":len(eligible),
          "n_source_geoblocks":len({r["source_geographic_block"] for r in eligible}),
          "unadjusted_WorldClim_mean_wind_Spearman_rho":spearman_safe(x,y),
          "partial_rank_corr_after_source_reporting_two_fields":
              rank_partial(x,y,cov[:2]),
          "partial_rank_corr_after_reporting_latitude_temperature_precip":
              rank_partial(x,y,cov),
          "source_1970_2000_mean_wind_not_ERA5_1991_2020_gust":True,
          "no_IID_pvalue_or_causal_inference":True}
    return result

def source_wind_proxy_overlap(data,gust33):
    bycode={r["TDWG_L3"]:r for r in data}
    items=list(csv.DictReader(io.StringIO(gust33.decode("utf-8-sig"))))
    codes=[r["TDWG_L3"] for r in items]
    if len(items)!=33 or len(set(codes))!=33 or not set(codes)<=set(bycode):
        raise ValueError("STAGE107_ORIGINAL_STAGE105_33_MAINLAND_POINT_COHORT_CHANGED")
    x=[float(bycode[c]["WorldClim2_1_1970_2000_mean_wind_m_s_NOT_ERA5_gust"]) for c in codes]
    y=[float(r["one_region_representative_point_ERA5_derived_daily_gust15_fraction"]) for r in items]
    return {"n_source_identical_TDWG_region_codes":len(codes),
       "SOURCE_WorldClim_average_vs_ERA5_point_30yr_gust_Spearman_rho":spearman_safe(x,y),
       "different_time_period_source_and_physical_variable_not_interchangeable":True}

def run(worldclim,source96,source91,source92,geography,gust33,out):
    train=train_source_split(archive_member(geography,SHA["mainland72"],MEMBERS["mainland72"]))
    a=safe_original_stage_train(archive_member(worldclim,SHA["worldclim"],MEMBERS["worldclim"]),train)
    b=safe_original_stage_train(archive_member(source96,SHA["source96"],MEMBERS["source96"]),train)
    c=safe_original_stage_train(archive_member(source91,SHA["source91"],MEMBERS["source91"]),train)
    d=safe_original_stage_train(archive_member(source92,SHA["source92"],MEMBERS["source92"]),train)
    rows=common_train_regions(a,b,c,d,train)
    estimates=rank_summary(rows)
    proxy=source_wind_proxy_overlap(rows,archive_member(gust33,SHA["gust33"],MEMBERS["gust33"]))
    rec={
       "schema":"stage107_global_mainland_72_SOURCE_ONLY_WorldClim_mean_wind_flower_source_reporting_bias",
       "original_verified_zip_SHA256":SHA,
       "source_geographically_contact_free_exploration_region_count":len(rows),
       "original_FIXED_holdout_37_plant_signal_outcomes_not_used":True,
       "source_plant_species_repeated_in_spatial_regions":True,
       "WorldClim2_1_1970_2000_mean_NOT_original_ERA5_10fg_gust":True,
       "WorldClim_10arcmin_source_48_point_sampling_not_exact_025_CDS_area_integral":True,
       "true_flower_visits_landings_training_and_VOC_not_observed":True,
       "source_WFO_and_NHM_description_reporting_not_independent_of_environment":True,
       "no_IID_pvalues_reported":True,
       "no_holdout_validation_or_selection_effect_estimated":True,
       "source_outcomes":estimates,
       "same_source_33_ERA5_point_gust_vs_WorldClim_mean_wind":proxy}
    out.mkdir(parents=True,exist_ok=True)
    with (out/"stage107_true_72_exploration_WorldClim_meanwind_3_flora_source_proxies.csv").open(
        "w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (out/"stage107_original_72_mainland_WorldClim_wind_flora_reporting_sensitivity.json").write_text(
       json.dumps(rec,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE107_REAL_72_MAINLAND_WorldClim_1970_2000_SOURCE_SENSITIVITY",
       json.dumps({"regions":len(rows),"proxy":proxy,
        "report_outcomes":{k:{"n":v["n_source_regions"],
             "raw":v["unadjusted_WorldClim_mean_wind_Spearman_rho"],
             "after_source_reporting":v["partial_rank_corr_after_source_reporting_two_fields"],
             "after_geography_climate":v["partial_rank_corr_after_reporting_latitude_temperature_precip"]}
             for k,v in estimates.items()}},sort_keys=True),flush=True)
    return rec

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for item in ("worldclim-original-TDWG3-ZIP","stage96-original-three-cues-ZIP",
                 "stage91-original-marking-source-ZIP","stage92-original-size-source-ZIP",
                 "stage98B-original-mainland-ZIP","stage105-original-33-point-ERA5-ZIP"):
       p.add_argument("--"+item,required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.worldclim_original_TDWG3_ZIP,a.stage96_original_three_cues_ZIP,
       a.stage91_original_marking_source_ZIP,a.stage92_original_size_source_ZIP,
       a.stage98B_original_mainland_ZIP,a.stage105_original_33_point_ERA5_ZIP,
       a.outdir)
