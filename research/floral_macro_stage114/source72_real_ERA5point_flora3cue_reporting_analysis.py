#!/usr/bin/env python3
"""Stage114: 72 authentic mainland exploratory ERA5 POINT gust × 3 floral-source indicators.

Original source floor:
- Stage113 genuine 1991-2020 Open-Meteo delivered ERA5 model daily gust
  representative-point climatology for exactly frozen original 72 contact-free
  mainland exploration TDWG3 regions (37 source holdout excluded).
- Stage107 authentic source WCVP/NHM 367-region original accepted native plant
  lexical markings/colour-field reporting, original WFO floral-fragrance
  positive/explicit-negative source descriptions and AusTraits v7 flower
  diameter; only Stage107 72 exploration region source rows read.
- Stage105 prior 33 exploratory source wind/trait results independently
  replayed at exact same region keys to catch trait-grain drift.

This is strictly descriptive SOURCE/reporting-bias sensitivity, not an
adaptive effect, observed floral UV nectar guides, actual scent plume, bee
landing or neural cue learning. At most 72 spatially, taxonomically and
bibliographically dependent regions from 17 geographic coarse blocks.
No IID p-values, no causal path coefficients, no holdout outcomes.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,re,statistics,sys,zipfile
from collections import Counter
from pathlib import Path
import numpy as np

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage105"))
from source_50point_wind_vs_flora_report_bias import spearman_safe,rank_partial

SRC107_SHA="8bdd375003ed7a7e9de03d13543b76a7c8542f092c0c28344925e51f0b418c1a"
SRC105_SHA="0d7cc6609c9ee3b85e24aafbbfd5dec307119506c4a4d5f79a579c21ed6c1534"
SRC107_MEMBER="stage107_true_72_exploration_WorldClim_meanwind_3_flora_source_proxies.csv"
SRC105_MEMBER="stage105_source_33_exploration_regions_ONLY_NO_HOLDOUT.csv"
STAGE113_MEMBER="stage113_TRUE_72_original_mainland_ERA5model_1991_2020_point_climate_NO_floral.json"
SOURCE_EXPOSURES={
    "gust15_ERA5model_1991_2020_point":"source_primary_fraction_days_daily_gust_strict_above_15_ms",
    "gust10_secondary":"source_fraction_gust_greater_than_10_ms",
    "gust20_secondary":"source_fraction_gust_greater_than_20_ms"}
TARGETS={
    "near_visual_NHM_word_positive_per_native":
        ("floral_marking_lexical_report_per_native",0),
    "near_visual_NHM_word_positive_per_colour_described":
        ("floral_marking_lexical_report_per_colour_field_species",0),
    "chemical_WFO_positive_fragrance_per_description":
        ("fragrance_positive_source_mention_per_flora_description",0),
    "chemical_WFO_positive_among_explicit_posneg":
        ("fragrance_positive_among_explicit_pos_and_neg",0),
    "far_visual_AusTraits_measured_labelled_median_mm_ge3":
        ("AusTraits_original_measured_grade_median_mm",3),
    "far_visual_AusTraits_measured_labelled_median_mm_ge10":
        ("AusTraits_original_measured_grade_median_mm",10),
    "SOURCE_NHM_colour_reported_fraction":
        ("NHM_colour_field_description_coverage",0),
    "SOURCE_WFO_full_flora_prose_reporting_fraction":
        ("WFO_original_flora_description_coverage",0)}
DOC_FIELDS=("NHM_colour_field_description_coverage","WFO_original_flora_description_coverage")
CLIM_FIELDS=("source_ERA5_point_latitude","source_ERA5_1991_2020_mean_temperature_C",
             "WorldClim_1970_2000_precip_mm_month")

def sha256(path):
    digest=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):digest.update(b)
    return digest.hexdigest()

def verified_zip_member(path,expected_sha,member):
    if not re.fullmatch(r"[a-f0-9]{64}",expected_sha):
        raise ValueError("STAGE114_ORIGINAL_ARTIFACT_SHA_NOT_PINNED")
    if sha256(path)!=expected_sha:
        raise ValueError("STAGE114_IMMUTABLE_PRIOR_SOURCE_ZIP_SHA_DRIFT_"+member)
    with zipfile.ZipFile(path) as z:
        if member not in z.namelist():
            raise ValueError("STAGE114_SOURCE_MEMBER_NOT_FOUND_"+member)
        return z.read(member)

def original_climate_72(archive,sha):
    o=json.loads(verified_zip_member(archive,sha,STAGE113_MEMBER))
    if (o["source_original_stage98B_72_37_SHA256"]!="8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7"
        or o["source_first50_existing_33_train_points_reused"]!=33
        or o["source_new_39_original_train_points_ERA5_model_30years"]!=39
        or o["source_final_72_original_mainland_exploration_gust15_POINT_regions"]!=72
        or o["source_original17_geographic_blocks"]!=17
        or not o["source_original_37_holdout_floral_outcomes_NOT_read"]
        or not o["source_72_area_weighted_gust_NOT_obtained"]
        or not o["source_real_Public_OpenMeteo_ERA5model_daily_not_CDS_hourly_10fg"]):
        raise ValueError("STAGE114_SOURCE_STAGE113_DATA_OR_HOLDOUT_SCOPE_NOT_EXACT")
    values={}
    for r in o["source_72_true_original_model_ERA5_representative_points"]:
        code=r["TDWG_L3"]
        if code in values or r["shared_split"]!="exploration":
            raise ValueError("STAGE114_SOURCE_72_NOT_EXPLORATION_UNIQUE")
        if r["source_ERA5_observed_30yr_days"]!=10958:
            raise ValueError("STAGE114_SOURCE_NOT_30YEAR_DAILY_CLIMATOLOGY")
        for field in SOURCE_EXPOSURES.values():
            val=r.get(field)
            if val is not None and not 0<=float(val)<=1:
                raise ValueError("STAGE114_SOURCE_PRIMARY_OR_SENSITIVITY_GUST_INVALID")
        if set(r["source_monthly_30yr_mean_T2m_C"])!=set(str(m) for m in range(1,13)):
            raise ValueError("STAGE114_12_MONTH_SOURCE_T_CLIMATOLOGY_MISSING")
        values[code]=r
    if len(values)!=72 or len({r["spatial_block_id"] for r in values.values()})!=17:
        raise ValueError("STAGE114_SOURCE_72_17_BLOCKS_NOT_VERIFIED")
    return values,o

def original_72_trait_source(archive):
    original=verified_zip_member(archive,SRC107_SHA,SRC107_MEMBER)
    data=list(csv.DictReader(io.StringIO(original.decode("utf-8-sig"))))
    if len(data)!=72 or len({r["TDWG_L3"] for r in data})!=72:
        raise ValueError("STAGE114_ORIGINAL_STAGE107_72_SOURCE_TRAITS_CHANGED")
    result={}
    for r in data:
        code=r["TDWG_L3"]
        if r["no_holdout_climate_or_floral_effect_fitted"]!="YES":
            raise ValueError("STAGE114_SOURCE_FLORISTIC_SAMPLE_STATUS_CHANGED")
        n=int(r["n_WCVP_native_source_species"])
        if n<=0:raise ValueError("STAGE114_SOURCE_NATIVE_SPECIES_DENOMINATOR_INVALID")
        for key in DOC_FIELDS:
            v=float(r[key])
            if not 0<=v<=1:raise ValueError("STAGE114_REPORTING_FRACTION_INVALID")
        result[code]=r
    return result

def stage105_prior33_source(archive,clim,traits):
    data=list(csv.DictReader(io.StringIO(
        verified_zip_member(archive,SRC105_SHA,SRC105_MEMBER).decode("utf-8-sig"))))
    if len(data)!=33 or len({r["TDWG_L3"] for r in data})!=33:
        raise ValueError("STAGE114_PRIOR33_ORIGINAL_BASELINE_CORRUPT")
    probes={
       "marking_lexical_positive_per_native":"floral_marking_lexical_report_per_native",
       "marking_lexical_positive_per_colour_described":"floral_marking_lexical_report_per_colour_field_species",
       "fragrance_positive_reports_per_WFO_description":"fragrance_positive_source_mention_per_flora_description",
       "NHM_flower_colour_documentation_coverage":"NHM_colour_field_description_coverage",
       "WFO_flora_description_coverage":"WFO_original_flora_description_coverage"}
    for row in data:
        code=row["TDWG_L3"]
        if code not in clim or code not in traits:
            raise ValueError("STAGE114_PRIOR33_SOURCE_REGION_ABSENT_IN_72")
        if (row["source_geographic_block"]!=clim[code]["spatial_block_id"] or
            row["source_geographic_block"]!=traits[code]["source_geographic_block"]):
            raise ValueError("STAGE114_ORIGINAL_PRIOR33_SOURCE_GEOGRAPHY_CHANGED")
        x=float(row["one_region_representative_point_ERA5_derived_daily_gust15_fraction"])
        if abs(x-float(clim[code][SOURCE_EXPOSURES["gust15_ERA5model_1991_2020_point"]]))>1e-12:
            raise ValueError("STAGE114_PRIOR33_SOURCE_GUST_NOT_IDENTICAL")
        for a,b in probes.items():
            if abs(float(row[a])-float(traits[code][b]))>1e-12:
                raise ValueError("STAGE114_PRIOR33_FLORAL_REPORTING_SOURCE_NOT_IDENTICAL_"+b)
    return {r["TDWG_L3"] for r in data}

def join_source_frame(clim,source_traits):
    if set(clim)!=set(source_traits):
        raise ValueError("STAGE114_SOURCE_72_GEO_IDENTITY_NOT_MATCHED")
    rows=[]
    for code in sorted(clim):
        c=clim[code];t=source_traits[code]
        if c["spatial_block_id"]!=t["source_geographic_block"]:
            raise ValueError("STAGE114_SOURCE_GEO_BLOCK_CHANGED_"+code)
        row={"TDWG_L3":code,
             "source_geographic_block":c["spatial_block_id"],
             "source_ERA5_point_latitude":float(c["lat"]),
             "source_ERA5_point_longitude":float(c["lon"]),
             "source_ERA5_1991_2020_mean_temperature_C":
                  statistics.mean(float(x) for x in c["source_monthly_30yr_mean_T2m_C"].values()),
             "source_exposure_is_one_representative_point_NOT_landarea":True,
             "source_original_TDWG3_30year_climate_calendar_days":10958,
             "source_n_original_native_species":int(t["n_WCVP_native_source_species"])}
        for name,key in SOURCE_EXPOSURES.items():
            row[name]=float(c[key]) if c.get(key) is not None else None
        for k in DOC_FIELDS:
            row[k]=float(t[k])
        for k in ("WorldClim_1970_2000_precip_mm_month",
                  "WorldClim2_1_1970_2000_mean_wind_m_s_NOT_ERA5_gust"):
            row[k]=float(t[k])
        for k,(col,_) in TARGETS.items():
            raw=t[col]
            row[k]=float(raw) if raw!="" else None
        row["n_AusTraits_original_measured_size_species"]=int(
            t["n_AusTraits_original_measured_size_species"])
        rows.append(row)
    if len(rows)!=72:raise ValueError("STAGE114_NOT_72_ORIGINAL_EXPLORATION_REGION_OBSERVATIONS")
    return rows

def _partial_rank_with_source_blocks(eligible,wind_key,outcome_key,covariates):
    blocks=sorted({r["source_geographic_block"] for r in eligible})
    controls=[[r[k] for r in eligible] for k in covariates]
    # One reference category to prevent redundant group control variables.
    controls.extend([[int(r["source_geographic_block"]==block) for r in eligible]
                     for block in blocks[1:]])
    if len(eligible)<len(controls)+6:
        return None
    return rank_partial([r[wind_key] for r in eligible],
                        [r[outcome_key] for r in eligible],controls)

def true_source_association_sensitivity(rows):
    controls=list(DOC_FIELDS)
    covariates=controls+list(CLIM_FIELDS)
    results={}
    for exposure,xkey in SOURCE_EXPOSURES.items():
        inside={}
        for name,(_,minsize) in TARGETS.items():
            eligible=[r for r in rows if r[xkey] is not None and r[name] is not None
                and r["n_AusTraits_original_measured_size_species"]>=minsize]
            n=len(eligible);blocks=sorted({r["source_geographic_block"] for r in eligible})
            x=[r[xkey] for r in eligible];y=[r[name] for r in eligible]
            raw=spearman_safe(x,y)
            partial_doc=rank_partial(x,y,[[r[k] for r in eligible] for k in controls])
            partial_clim=rank_partial(x,y,[[r[k] for r in eligible] for k in covariates])
            block_adj=_partial_rank_with_source_blocks(eligible,xkey,name,covariates)
            # Leave-one-block-out is a leverage diagnostic, not a sampling CI.
            samples=[]
            for block in blocks:
                subset=[r for r in eligible if r["source_geographic_block"]!=block]
                v=spearman_safe([r[xkey] for r in subset],[r[name] for r in subset])
                if v is not None:samples.append(v)
            inside[name]={
                "n_original_exploratory_mainland_regions":n,
                "n_original_geographic_blocks":len(blocks),
                "source_raw_Spearman_rho":raw,
                "source_partial_rank_after_NHM_WFO_documentation":partial_doc,
                "source_partial_rank_after_documentation_lat_T_rain":partial_clim,
                "source_partial_rank_after_doc_climate_geoBLOCK_fixed_effects":block_adj,
                "source_leave_one_geographic_block_raw_rho_min":min(samples) if samples else None,
                "source_leave_one_geographic_block_raw_rho_max":max(samples) if samples else None,
                "source_leave_one_geographic_block_valid_runs":len(samples),
                "NO_source_region_IID_pvalue_or_causal_effect":True}
        results[exposure]=inside
    return results

def run(stage113,stage113_sha,stage107,stage105,outdir):
    climate,met=original_climate_72(stage113,stage113_sha)
    traits=original_72_trait_source(stage107)
    validated_old=stage105_prior33_source(stage105,climate,traits)
    rows=join_source_frame(climate,traits)
    estimates=true_source_association_sensitivity(rows)
    receipt={
       "schema":"stage114_original_72_contactfree_mainland_ERA5_model_1991_2020_POINT_gust_three_cue_source_reporting_sensitivity",
       "original_stage113_source_72_model_point_ZIP_SHA256":stage113_sha,
       "original_stage107_72_source_floral_reports_ZIP_SHA256":SRC107_SHA,
       "original_stage105_prior33_source_calibration_ZIP_SHA256":SRC105_SHA,
       "original_exact_old33_source_climate_and_floral_report_values_reproduced":len(validated_old),
       "original_full_72_exploration_climate_source_regions":len(rows),
       "original_geo_blocks":len({r["source_geographic_block"] for r in rows}),
       "source_37_original_holdout_floral_outcomes_NOT_read":True,
       "wind_is_point_proxy_not_real_0p25_landarea_regional_average":True,
       "original_CDS_hourly_10fg_gust_NOT_obtained":True,
       "original_WorldClim_1970_2000_rain_covar_distinct_from_1991_2020_ERA5_model":True,
       "NHM_lexical_flower_patterns_not_independently_verified_nectar_guides":True,
       "WFO_fragrance_source_mention_NOT_VOC_emission_or_absence":True,
       "source_AusTraits_region_median_reuses_source_species_and_not_independent_measured_phenotype":True,
       "original_SOURCE_report_ascertainment_cannot_be_causally_adjusted_by_simple_regression":True,
       "original_species_identity_leakage_and_phylogenetic_nonindependence_unresolved":True,
       "geoblocks_are_coarse_and_no_spatially_valid_inference_test":True,
       "NO_IID_pvalues_NO_fitness_OR_pollinator_sensory_order_inference":True,
       "outcomes_and_source_reporting_diagnostics":estimates}
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage114_original72_contactfree_mainland_ERA5point_3cue_reporting_frame_ONLY.csv").open(
        "w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (outdir/"stage114_original72_source_ERA5point_cue_reporting_bias_diagnostics_NO_CAUSAL.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print("STAGE114_AUTHENTIC_72_MAINLAND_ERA5_POINT_CUE_REPORTING_SENSITIVITY",
      json.dumps({"source_region_count":len(rows),
        "old33_reproduced":len(validated_old),
        "primary_gust15":{k:{"n":v["n_original_exploratory_mainland_regions"],
              "raw":v["source_raw_Spearman_rho"],
              "reporting_adjusted":v["source_partial_rank_after_NHM_WFO_documentation"],
              "reporting_geo_climate":v["source_partial_rank_after_documentation_lat_T_rain"],
              "geo_block_fixed_effects":v["source_partial_rank_after_doc_climate_geoBLOCK_fixed_effects"]}
              for k,v in estimates["gust15_ERA5model_1991_2020_point"].items()}},
        sort_keys=True),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage113-ERA5model-72source-ZIP",required=True,type=Path)
    p.add_argument("--source-Stage113-ZIP-SHA256",required=True)
    p.add_argument("--original-Stage107-72-flora-source-ZIP",required=True,type=Path)
    p.add_argument("--original-Stage105-33-point-bias-source-ZIP",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.original_Stage113_ERA5model_72source_ZIP,a.source_Stage113_ZIP_SHA256,
        a.original_Stage107_72_flora_source_ZIP,
        a.original_Stage105_33_point_bias_source_ZIP,a.outdir)
