#!/usr/bin/env python3
"""Stage105 deliberately EXPLORATORY source-documentation-bias diagnostic.

Source-authenticated 1991–2020 Open-Meteo ERA5 MODEL **ONE POINT PER REGION**
source gust climate at first 50 of 125 mainland TDWG3s, joined ONLY to
source-geography-certified 72 contact-free exploration regions (never original
37 holdout signal outcomes or source-contact-excluded 16 regions). Of first50,
currently 33 exploration regions across 15 geographic blocks.

This is NOT the preregistered CDS area-weighted original hourly 10fg and is
not a valid independent multi-species evolutionary selection test.  It tests
how the sign/size of a descriptive wind-vs-signal SOURCE mention association
depends on floral documentation bias and explicit-negative denominator.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,statistics,zipfile
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from scipy.stats import rankdata,spearmanr

SHA={
    "first25":"7c98421306466b589b1f80ec97d4ca32ba58e73ba7807f0c2330a7f082fe6b67",
    "second25":"5e5ee1c325cc85abfb3cfb98a85d9b3faecacd116db9d917eaebdd3a0c453d79",
    "mainland72":"8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7",
    "source96":"99aaf623ac3a7f948c5d0cdad9a8ce8668c2131ee07af6fb5d02d81c573c3149",
    "source91":"f1197a050d110d1e3626ab01f3c5d49626ac32fd0588d41ce3a162b44d921cdf",
    "source92":"01d76457aa8423b7964b5fccdfea597f5c158a805c138fd8597e7efd1733a05f",
}
MEMBERS={
 "first25":"stage95C_true_source_first25_mainland_site_gust_30yr.json",
 "second25":"stage97_real_1991_2020_next25_original_mainland_ERA5_model_gust.json",
 "mainland72":"stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv",
 "source96":"stage96_native_367_original_floral_three_cue_source_availability.csv",
 "source91":"stage91_global_TDWG3_3cue_availability_INCLUDES_ISLANDS.csv",
 "source92":"stage92_AusTraits7_flower_diameter_367_regions_INCLUDES_ISLANDS.csv",
}
CONFOUNDERS=("NHM_flower_colour_documentation_coverage",
             "WFO_flora_description_coverage",
             "latitude","mean_annual_T2m_C")
SEED=20261120

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for c in iter(lambda:f.read(1<<20),b""):h.update(c)
    return h.hexdigest()

def archive_member(path,expected,member):
    if sha256(path)!=expected:raise ValueError("STAGE105_IMMUTABLE_ORIGINAL_SOURCE_SHA_DRIFT_"+member)
    with zipfile.ZipFile(path) as z:
        if member not in z.namelist():raise ValueError("STAGE105_SOURCE_MEMBER_MISSING_"+member)
        return z.read(member)

def weather_sources(first25,second25):
    a=json.loads(first25);b=json.loads(second25)
    if (a["source_completed_region_count"]!=25 or
        b["source_returned_distinct_region_count"]!=25 or
        a["no_source_regional_area_weighting"] is not True or
        b["region_area_weighting_performed"] is not False or
        b["source_prior25_exact_region_codes"]!=[r["TDWG_L3"] for r in a["sites"]]):
        raise ValueError("STAGE105_NOT_GENUINE_25_PLUS_25_SOURCE_POINT_SERIES")
    w={}
    for s in a["sites"]+b["regions"]:
        k=s["TDWG_L3"]
        if k in w:raise ValueError("STAGE105_REPEATED_ORIGINAL_WEATHER_SOURCE_REGION")
        if s["source_ERA5_observed_30yr_days"]!=10958:raise ValueError("STAGE105_ORIGINAL_30YR_DAILY_DATA_NOT_COMPLETE")
        value=s["source_primary_fraction_days_daily_gust_strict_above_15_ms"]
        if value is not None and not (0<=float(value)<=1):
            raise ValueError("STAGE105_PRIMARY_GUST_SOURCE_FRACTION_INVALID")
        w[k]=s
    if len(w)!=50:raise ValueError("STAGE105_SOURCE_FIRST50_NOT_COMPLETE")
    return w

def train_source_split(train_bytes):
    rows=list(csv.DictReader(io.StringIO(train_bytes.decode("utf-8-sig"))))
    if len(rows)!=72 or len({r["TDWG_L3"] for r in rows})!=72:
        raise ValueError("STAGE105_FIXED_CONTACT_FREE_TRAIN72_DRIFT")
    if any(r["land_scope"]!="mainland" or r["shared_split"]!="exploration" for r in rows):
        raise ValueError("STAGE105_NOMINAL_TRAIN_CONTAINS_HOLDOUT_OR_ISLAND")
    return {r["TDWG_L3"]:r for r in rows}

def qualified_training_data(weather,train,stage96,stage91,stage92):
    # Scan 367-row original source tables, but retain ONLY geography-frozen
    # 72 exploration keys. Holdout trait values are never stored or fitted.
    source={}
    for label,source_data in [("source96",stage96),("source91",stage91),("source92",stage92)]:
        reader=csv.DictReader(io.StringIO(source_data.decode("utf-8-sig")))
        seen=set();values={}
        for row in reader:
            code=row["TDWG_L3"]
            if code in seen:raise ValueError("STAGE105_SOURCE_REGION_DUPLICATE_"+label)
            seen.add(code)
            if code in train:values[code]=row
        if len(seen)!=367 or set(values)!=set(train):
            raise ValueError("STAGE105_ORIGINAL_367_REGION_SOURCE_MISMATCH_"+label)
        source[label]=values
    data=[]
    for code in sorted(set(weather)&set(train)):
        w=weather[code];c=source["source96"][code];s=source["source91"][code]
        t=source["source92"][code]
        if w["shared_split"]!="exploration":
            raise ValueError("STAGE105_HOLDOUT_ORIGINAL_WEATHER_IN_SOURCE_TRAIN")
        n=int(c["n_native_source_species"])
        if (n<=0 or n!=int(s["n_native"]) or
            n!=int(t["n_original_WCVP_native_species_in_region"])):
            raise ValueError("STAGE105_NATIVE_SPECIES_SOURCE_DENOMINATOR_DRIFT")
        colour_missing=int(s["n_source_colour_missing"])
        if not 0<=colour_missing<=n:raise ValueError("STAGE105_NEGATIVE_OR_EXCESS_COLOUR_MISSING")
        colour_n=n-colour_missing
        mark=int(c["n_positive_marking_TEXT_SOURCE_CANDIDATES"])
        if mark>colour_n:raise ValueError("STAGE105_PATTERN_SOURCE_POSITIVE_EXCEEDS_RECORDED_COLOUR")
        desc=int(c["n_original_WFO_full_flora_description_species"])
        pos=int(c["n_source_floral_fragrance_lexical_positive"])
        neg=int(c["n_source_floral_fragrance_lexical_explicit_negative"])
        if not 0<=pos+neg<=desc<=n:
            raise ValueError("STAGE105_WFO_SCENT_SOURCE_NOT_EXPLICIT_BINARY_SUBSET")
        size_n=int(t["n_original_AusTraits_flower_diameter_species"])
        size=float(t["diameter_median_mm_of_source_species"]) if t["diameter_median_mm_of_source_species"] else None
        if size_n==0 and size is not None:raise ValueError("STAGE105_FALSE_ZERO_ABSENT_FLOWER_SIZE")
        m=w["source_monthly_30yr_mean_T2m_C"]
        if set(m)!=set(str(k) for k in range(1,13)):
            raise ValueError("STAGE105_ORIGINAL_12_MONTHS_T_CLIMATOLOGY_CHANGED")
        line={
            "TDWG_L3":code,"source_geographic_block":train[code]["spatial_block_id"],
            "one_region_representative_point_ERA5_derived_daily_gust15_fraction":
                   float(w["source_primary_fraction_days_daily_gust_strict_above_15_ms"]),
            "latitude":float(w["lat"]),"longitude":float(w["lon"]),
            "mean_annual_T2m_C":statistics.mean(float(v) for v in m.values()),
            "n_source_native_species":n,
            "n_WFO_original_botanical_description_species":desc,
            "n_NHM_flower_colour_source_descriptions":colour_n,
            "n_source_positive_marking_lexical_candidates":mark,
            "n_source_positive_floral_fragrance_lexical_reports":pos,
            "n_source_explicit_negative_floral_fragrance_lexical_reports":neg,
            "n_original_AusTraits_measured_source_flower_diameter_species":size_n,
            "NHM_flower_colour_documentation_coverage":colour_n/n,
            "WFO_flora_description_coverage":desc/n,
            "marking_lexical_positive_per_native":mark/n,
            "marking_lexical_positive_per_colour_described":mark/colour_n if colour_n else None,
            "fragrance_positive_reports_per_WFO_description":pos/desc if desc else None,
            "fragrance_positive_fraction_among_explicit_pos_and_neg":pos/(pos+neg) if pos+neg else None,
            "AusTraits_source_median_flower_diameter_mm":size,
            "NO_heldout_floral_outcomes_USED":"YES",
            "NO_regional_land_area_wind_computation":"YES"}
        data.append(line)
    if len(data)!=33 or len({x["source_geographic_block"] for x in data})!=15:
        raise ValueError("STAGE105_ORIGINAL_ALPHABETIC_FIRST50_SOURCE_TRAIN_COHORT_NOT_33_BLOCKS15")
    return data

def spearman_safe(x,y):
    x=np.asarray(x,float);y=np.asarray(y,float)
    if len(x)<5 or np.std(x)<1e-12 or np.std(y)<1e-12:return None
    v=float(spearmanr(x,y).statistic)
    return v if math.isfinite(v) else None

def rank_partial(wind,signal,controls):
    """Partial rank correlation, never its IID significance p-value."""
    arr=np.asarray([wind,signal]+controls,float).T
    if len(arr)<len(controls)+6:return None
    if not np.all(np.isfinite(arr)) or np.std(arr[:,0])<1e-12 or np.std(arr[:,1])<1e-12:
        return None
    ranks=np.apply_along_axis(rankdata,axis=0,arr=arr)
    c=ranks[:,2:]
    c=(c-c.mean(axis=0))/(c.std(axis=0)+1e-12)
    X=np.column_stack((np.ones(len(arr)),c))
    y=ranks[:,:2]
    residual=y-X@np.linalg.lstsq(X,y,rcond=None)[0]
    if np.any(residual.std(axis=0)<1e-8):return None
    value=float(np.corrcoef(residual.T)[0,1])
    return value if math.isfinite(value) else None

def analyse(data):
    outcomes={
      "near_visual_source_positive_marking_per_native":
          ("marking_lexical_positive_per_native",0),
      "near_visual_source_positive_marking_per_colour_described":
          ("marking_lexical_positive_per_colour_described",0),
      "chemical_source_positive_floral_fragrance_per_description":
          ("fragrance_positive_reports_per_WFO_description",0),
      "chemical_explicit_positive_fraction_pos_vs_explicit_negative":
          ("fragrance_positive_fraction_among_explicit_pos_and_neg",0),
      "far_visual_original_AusTraits_median_flower_diameter_mm_n>=3":
          ("AusTraits_source_median_flower_diameter_mm",3),
      "far_visual_original_AusTraits_median_flower_diameter_mm_n>=10":
          ("AusTraits_source_median_flower_diameter_mm",10),
      "SOURCE_ascertainment_NHM_colour_coverage":
          ("NHM_flower_colour_documentation_coverage",0),
      "SOURCE_ascertainment_WFO_full_flora_description_coverage":
          ("WFO_flora_description_coverage",0)
    }
    windkey="one_region_representative_point_ERA5_derived_daily_gust15_fraction"
    results={}
    for label,(column,minsize) in outcomes.items():
        eligible=[r for r in data if r[column] is not None and
            r["n_original_AusTraits_measured_source_flower_diameter_species"]>=minsize]
        x=[r[windkey] for r in eligible];y=[r[column] for r in eligible]
        controls=[[r[k] for r in eligible] for k in CONFOUNDERS]
        estimates={
            "n_source_regions":len(eligible),
            "n_geographic_blocks":len({r["source_geographic_block"] for r in eligible}),
            "unadjusted_region_Spearman_rho":spearman_safe(x,y),
            "partial_rank_correlation_after_flower_colour_coverage":
                rank_partial(x,y,[controls[0]]),
            "partial_rank_correlation_after_both_documentation_covariates":
                rank_partial(x,y,controls[:2]),
            "partial_rank_correlation_after_documentation_latitude_temperature":
                rank_partial(x,y,controls),
            "spatially_dependent_region_source_observations_NOT_independent":True,
            "NO_p_value_or_evolutionary_hypothesis_test":True}
        leave=[]
        for block in sorted({r["source_geographic_block"] for r in eligible}):
            selected=[r for r in eligible if r["source_geographic_block"]!=block]
            z=spearman_safe([r[windkey] for r in selected],[r[column] for r in selected])
            if z is not None:leave.append(z)
        estimates["geoblock_leave1out_raw_rho_min"] = min(leave) if leave else None
        estimates["geoblock_leave1out_raw_rho_max"] = max(leave) if leave else None
        estimates["geoblock_leave1out_valid_runs"]=len(leave)
        results[label]=estimates
    return results

def run(first25,second25,geography,source96,source91,source92,out):
    w=weather_sources(
        archive_member(first25,SHA["first25"],MEMBERS["first25"]),
        archive_member(second25,SHA["second25"],MEMBERS["second25"]))
    train=train_source_split(archive_member(geography,SHA["mainland72"],MEMBERS["mainland72"]))
    data=qualified_training_data(
        w,train,
        archive_member(source96,SHA["source96"],MEMBERS["source96"]),
        archive_member(source91,SHA["source91"],MEMBERS["source91"]),
        archive_member(source92,SHA["source92"],MEMBERS["source92"]))
    values=analyse(data)
    result={
      "schema":"stage105_50_points_33_safe_train_regions_3cue_documentation_bias_EXPLORATORY_ONLY",
      "SHA256_immutable_original_source_derivations":SHA,
      "source_all_original_ERA5_model_point_regions":len(w),
      "source_train_contact_free_wind_regions":len(data),
      "source_original_fixed_72_mainland_exploration_regions":len(train),
      "source_geoblocks_in_current_33_region_model":len({r["source_geographic_block"] for r in data}),
      "original_37_mainland_holdout_source_traits_NOT_fit_or_reported":True,
      "original_16_removed_contact_regions_NOT_fit":True,
      "original_ERA5_CDS_hourly_10fg_NOT_verified":True,
      "one_source_point_per_region_NOT_land_area_weighted":True,
      "WFO_original_prose_fragrance_unknowns_NOT_biological_negative":True,
      "NHM_positive_marking_prose_NOT_true_nectar_guides":True,
      "AusTraits_measured_source_median_by_repeated_native_species_NOT_phylogenetically_independent":True,
      "nonrandom_first50_original_alphabetical_TDWG_region_subset":True,
      "floral_reporting_probability_may_depend_on_region_and_wind":True,
      "direct_geography_touches_excluded_but_spatial_source_taxon_dependence_remains":True,
      "rank_partial_controlled_source_coverage_is_diagnostic_NOT_causal_adjustment":True,
      "no_IID_p_values_reported":True,
      "not_holdout_validation_or_confirmatory_selection":True,
      "outcomes":values}
    out.mkdir(parents=True,exist_ok=True)
    (out/"stage105_source_33_exploration_regions_ONLY_NO_HOLDOUT.csv").open(
        "w",newline="",encoding="utf-8").close()
    with (out/"stage105_source_33_exploration_regions_ONLY_NO_HOLDOUT.csv").open(
        "w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(data[0]))
        writer.writeheader();writer.writerows(data)
    (out/"stage105_wind_to_three_source_cues_33_regions_EXPLORATORY_not_adjusted_causal.json").write_text(
        json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print("STAGE105_50_SOURCE_ERA5_POINTS_33_TRAIN_CUE_DOCUMENTATION_BIAS_SCREEN",
        json.dumps({"source_train_regions":len(data),
        "geoblocks":result["source_geoblocks_in_current_33_region_model"],
        "source_outcomes_raw_vs_rank_partial":{
          k:{"n":v["n_source_regions"],"raw":v["unadjusted_region_Spearman_rho"],
             "adjusted_four_covariates":v["partial_rank_correlation_after_documentation_latitude_temperature"]}
          for k,v in values.items()}},sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("stage95C-first25-source-ZIP","stage97-next25-source-ZIP",
                 "stage98B-mainland-72-37-ZIP","stage96-mainland-3cues-ZIP",
                 "stage91-source-marking-ZIP","stage92-source-diameter-ZIP"):
        p.add_argument("--"+name,required=True,type=Path)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    run(a.stage95C_first25_source_ZIP,a.stage97_next25_source_ZIP,
        a.stage98B_mainland_72_37_ZIP,a.stage96_mainland_3cues_ZIP,
        a.stage91_source_marking_ZIP,a.stage92_source_diameter_ZIP,a.outdir)
