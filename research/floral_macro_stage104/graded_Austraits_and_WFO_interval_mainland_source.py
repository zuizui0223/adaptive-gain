#!/usr/bin/env python3
"""Stage104 genuine AusTraits measured grade + WFO 2026 botanical source size intervals.

Original species-level source SHA guards. WFO [min,max] and upper-only
observations are botanical SOURCE REPORTS, NOT population confidence
intervals. Never impute point value at upper endpoint, midpoint, or missing.
Compare to independently published AusTraits source-labeled flower_diameter
ONLY as a consistency check; do not assert independent precision accuracy.

Preserve Stage98B actual 72 contact-free mainland exploration and 37 unchanged
holdout. No original ERA5 hourly 10fg, area wind exposure or ecological fit.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,statistics,sys,zipfile
from collections import Counter
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
for folder in ("floral_macro_stage87","floral_macro_stage92"):
    sys.path.insert(0,str(BASE/folder))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions
from austraits7_flower_diameter_source_audit import parse_original_austraits_zip

SOURCE_STAGE103_SHA="95fb60fa049ed4e79673e1f1dc12aaddb97f5fadd1dc27f905d31dd25b8cfe90"
SOURCE_STAGE98B_SHA="8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7"
INTERVAL_MEMBER="stage103_original_WFO_237_flower_source_interval_envelopes_NOT_measured.csv"
INTERVAL_RECEIPT="stage103_WFO_original_flower_size_interval_not_point_receipt.json"
TRAIN_MEMBER="stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv"
HOLDOUT_MEMBER="stage98B_holdout_original_mainland_37_UNCHANGED.csv"
SIZE_CLASSES={
    "bounded_source_range_or_mixed","bounded_plus_upper_limit_sources",
    "upper_limit_only_source_NO_lower_bound","exact_source_singletons",
    "no_eligible_size_evidence"}

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def original_archive_csv(path,sha,member):
    if sha256(path)!=sha:raise ValueError("STAGE104_ORIGINAL_SOURCE_ARTIFACT_SHA_MISMATCH")
    with zipfile.ZipFile(path) as z:
        if member not in z.namelist():raise ValueError("STAGE104_ORIGINAL_SOURCE_MEMBER_MISSING")
        return list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig"))))

def original_interval_species(archive,accepted):
    rows=original_archive_csv(archive,SOURCE_STAGE103_SHA,INTERVAL_MEMBER)
    with zipfile.ZipFile(archive) as z:
        receipt=json.loads(z.read(INTERVAL_RECEIPT))
    if (len(rows)!=237 or
        receipt["source_distinct_species_with_bounded_range"]!=124 or
        receipt["source_distinct_species_with_upper_limit_only"]!=57 or
        receipt["source_distinct_species_with_exact_singleton_phrase"]!=34 or
        receipt["source_distinct_species_with_any_valid_bounded_or_upper_or_singleton"]!=212):
        raise ValueError("STAGE104_ORIGINAL_237_212_WFO_SOURCE_COHORT_CHANGED")
    data={}
    for r in rows:
        sp=r["accepted_species"].casefold().strip()
        if sp in data or not sp or sp not in accepted:raise ValueError("STAGE104_WFO_ORIGINAL_TAXON_DUPLICATE_OR_NONNATIVE")
        state=r["status"]
        if state not in SIZE_CLASSES:raise ValueError("STAGE104_UNKNOWN_SOURCE_SIZE_CLASS")
        rawlo=r.get("lower_mm") or ""
        rawhi=r.get("upper_mm") or ""
        lo=float(rawlo) if rawlo else None
        hi=float(rawhi) if rawhi else None
        if state=="no_eligible_size_evidence":
            if lo is not None or hi is not None:raise ValueError("STAGE104_FALSE_SIZE_ON_UNAVAILABLE_SOURCE")
        else:
            if hi is None or not math.isfinite(hi) or hi<=0:
                raise ValueError("STAGE104_INVALID_ORIGINAL_SOURCE_UPPER")
            if state=="upper_limit_only_source_NO_lower_bound":
                if lo is not None:raise ValueError("STAGE104_UPPER_ONLY_HAS_INVENTED_LOWER")
            elif lo is None or not math.isfinite(lo) or not (0<lo<=hi):
                raise ValueError("STAGE104_POINT_OR_RANGE_MISSING_GENUINE_LOWER")
        data[sp]={
            "status":state,"lower_mm":lo,"upper_mm":hi,
            "contains_bounded_range":int(r.get("n_original_source_bounded_intervals") or 0)>0,
            "contains_original_single_number":int(r.get("n_original_source_exact_entries") or 0)>0,
            "contains_upper_limit":int(r.get("n_original_source_upper_only") or 0)>0,
            "wide_source_span_needs_review":r.get("source_envelope_over_5fold_NEEDS_REVIEW")=="True"}
    if len(data)!=237 or sum(x["status"]!="no_eligible_size_evidence" for x in data.values())!=212:
        raise ValueError("STAGE104_INTERVAL_NUMERIC_EVIDENCE_STATUS_COUNTS_CHANGED")
    return data

def geographic_groups(archive,regions):
    train=original_archive_csv(archive,SOURCE_STAGE98B_SHA,TRAIN_MEMBER)
    hold=original_archive_csv(archive,SOURCE_STAGE98B_SHA,HOLDOUT_MEMBER)
    t={r["TDWG_L3"] for r in train};h={r["TDWG_L3"] for r in hold}
    if (len(t),len(h))!=(72,37) or t&h or not (t|h)<=set(regions):
        raise ValueError("STAGE104_ORIGINAL_MAINLAND_72_37_CHANGED")
    if any(r["land_scope"]!="mainland" or r["shared_split"]!="exploration" for r in train):
        raise ValueError("STAGE104_NONMAINLAND_TRAIN")
    if any(r["land_scope"]!="mainland" or r["shared_split"]!="holdout" for r in hold):
        raise ValueError("STAGE104_NONMAINLAND_HOLDOUT")
    return t,h

def describe_floral_size_sources(native,measured,worded,train,holdout):
    direct=set(measured)
    eligible={k for k,r in worded.items() if r["status"]!="no_eligible_size_evidence"}
    ranged={k for k,r in worded.items() if r["contains_bounded_range"]}
    upper={k for k,r in worded.items() if r["status"]=="upper_limit_only_source_NO_lower_bound"}
    singleton={k for k,r in worded.items() if r["contains_original_single_number"]}
    too_wide={k for k,r in worded.items() if r["wide_source_span_needs_review"]}
    grade={
        "A_original_AusTraits_measured_source":direct,
        "B_original_WFO_all_source_bound_evidence_NOT_manual":eligible,
        "B2_WFO_two_sided_bounded_intervals":ranged,
        "B3_WFO_upper_only_no_lower_bound":upper,
        "B4_WFO_original_single_number_lexical":singleton,
        "A_and_B_exact_species_overlap":direct&eligible,
        "B_only_not_independent_measurement":eligible-direct,
        "A_or_B_total_source_available_NOT_all_measured":direct|eligible
    }
    source_train=set().union(*(native[c] for c in train))
    source_hold=set().union(*(native[c] for c in holdout))
    result={}
    for name,sp in grade.items():
        present_train=sp&source_train
        present_hold=sp&source_hold
        result[name]={
            "global_distinct_accepted_source_species":len(sp),
            "source_train_72_distinct_species":len(present_train),
            "source_holdout_37_distinct_species":len(present_hold),
            "source_holdout_37_exact_species_SHARED_with_train":len(present_hold&present_train),
            "source_holdout_37_distinct_species_UNSEEN_train":len(present_hold-present_train),
            "source_holdout_37_distinct_genera_UNSEEN_train":len(
                {s.split()[0] for s in present_hold}-{s.split()[0] for s in present_train})}
    regional=[]
    for code in sorted(train|holdout):
        plants=native[code]
        regional.append({"TDWG_L3":code,
          "original_source_fixed_fold":"exploration" if code in train else "holdout",
          "n_original_native_source_species":len(plants),
          **{"n_"+name:len(plants&values) for name,values in grade.items()},
          "n_WFO_wide_span_flagged_source_species":len(plants&too_wide),
          "source_only_NOT_ECMWF_ERA5_wind_fit":"TRUE"})
    summary={}
    for fold in ("exploration","holdout"):
        rows=[r for r in regional if r["original_source_fixed_fold"]==fold]
        summary[fold]={
            "source_mainland_regions":len(rows),
            "regions_with_10plus_A_measured":sum(r["n_A_original_AusTraits_measured_source"]>=10 for r in rows),
            "regions_with_10plus_B_WFO_bound":sum(r["n_B_original_WFO_all_source_bound_evidence_NOT_manual"]>=10 for r in rows),
            "regions_with_10plus_A_or_B_total":sum(r["n_A_or_B_total_source_available_NOT_all_measured"]>=10 for r in rows),
            "regions_with_10plus_B2_two_sided_intervals":sum(r["n_B2_WFO_two_sided_bounded_intervals"]>=10 for r in rows),
            "regions_with_10plus_AB_after_removing_wide_source_span":sum(
                len(native[r["TDWG_L3"]]&(grade["A_or_B_total_source_available_NOT_all_measured"]-(too_wide-direct)))>=10 for r in rows)}
    paired=[]
    for sp in sorted(direct&eligible):
        a=float(measured[sp]);v=worded[sp]
        paired.append({"source_species":sp,"AusTraits_source_mm":a,
            "WFO_source_report_type":v["status"],"WFO_lower_mm":v["lower_mm"],
            "WFO_upper_mm":v["upper_mm"],
            "AusTraits_value_within_WFO_reported_size_envelope":(
               a<=v["upper_mm"] and (v["lower_mm"] is None or a>=v["lower_mm"])),
            "direct_independent_population_measurement_equivalence_NOT_verified":True})
    return result,regional,summary,paired

def run(interval_archive,aus_original,nhm,wcvp,geography,outdir):
    nhm_species,_=load_nhm(nhm)
    native,_=wcvp_regions(wcvp,nhm_species)
    allsp=set().union(*native.values())
    if len(native)!=367 or len(allsp)!=55775:
        raise ValueError("STAGE104_ORIGINAL_55775_WCVP_ACCEPTED_NATIVE_SOURCE_CHANGED")
    wfo=original_interval_species(interval_archive,allsp)
    measured,measured_meta=parse_original_austraits_zip(aus_original,allsp)
    if len(measured)!=104:
        raise ValueError("STAGE104_ORIGINAL_AUSTRAITS_EXACT_104_NATIVE_SOURCE_CHANGED")
    train,hold=geographic_groups(geography,native)
    groups,regions,coverage,paired=describe_floral_size_sources(native,measured,wfo,train,hold)
    if (len(regions),coverage["exploration"]["source_mainland_regions"],
        coverage["holdout"]["source_mainland_regions"])!=(109,72,37):
        raise ValueError("STAGE104_MAINLAND_REGION_FRAME_CHANGED")
    rec={
      "schema":"stage104_original_WFO_202606_flower_size_bounds_Austraits7_grade_comparison",
      "original_source_SHA256":{"stage103_authentic_WFO_interval":SOURCE_STAGE103_SHA,
         "stage98B_contact_free_mainland":SOURCE_STAGE98B_SHA,
         "original_AusTraits7":measured_meta["authentic_zipped_source_sha256"]},
      "frozen_original_source_WFO_unreviewed_237":len(wfo),
      "frozen_original_source_AusTraits_labelled_flower_diameter_104":len(measured),
      "source_graded_species":groups,
      "source_graded_mainland_region_support":coverage,
      "source_AusTraits_comparable_WFO_species":len(paired),
      "source_AusTraits_source_mm_within_original_WFO_bounds":sum(
          p["AusTraits_value_within_WFO_reported_size_envelope"] for p in paired),
      "source_bound_size_is_not_population_uncertainty_CI":True,
      "source_qualitative_upper_bound_not_imputed_exact_point":True,
      "original_WFO_source_prose_NOT_manual_validated":True,
      "source_reporting_taxon_geography_bias_unresolved":True,
      "no_area_weighted_ERA5_1991_2020_10fg_raster":True,
      "no_wind_to_flower_size_effect_estimated":True,
      "holdout_identity_original_37_UNCHANGED":True
    }
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage104_original_strict_mainland_109_region_graded_size_support.csv").open(
        "w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(regions[0]));w.writeheader();w.writerows(regions)
    (outdir/"stage104_genuine_WFO_interval_AusTraits_size_support_receipt.json").write_text(
        json.dumps(rec,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    if paired:
        with (outdir/"stage104_AusTraits_vs_WFO_rare_exact_source_species_overlap.csv").open(
            "w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=list(paired[0]));w.writeheader();w.writerows(paired)
    print("STAGE104_TRUE_AUTHOR_SOURCE_INTERVAL_AND_AUSTRAITS_MEASURED_GRADE",
          json.dumps({"global":{k:v["global_distinct_accepted_source_species"] for k,v in groups.items()},
              "mainland":coverage,"original_cross_source_n":len(paired)},sort_keys=True),flush=True)
    return rec

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage103-WFO-interval-source-ZIP",type=Path,required=True)
    p.add_argument("--original-AusTraits7",type=Path,required=True)
    p.add_argument("--original-NHM",type=Path,required=True)
    p.add_argument("--original-WCVP",type=Path,required=True)
    p.add_argument("--original-Stage98B-mainland-source-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    run(a.original_Stage103_WFO_interval_source_ZIP,a.original_AusTraits7,
        a.original_NHM,a.original_WCVP,a.original_Stage98B_mainland_source_ZIP,a.outdir)
