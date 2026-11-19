#!/usr/bin/env python3
"""Stage101: source-aware union of authentic AusTraits numeric diameter + WFO prose.

This is ONLY a source-coverage audit across frozen 72 contact-free mainland
exploration and unchanged 37 mainland holdouts. Original AusTraits v7 numeric
flower_diameter values have published units; WFO 2026 eFloras prose candidates
are *unreviewed lexical extraction* and never silently promoted to direct
whole-flower measurement. Source-grade traits remain distinct.

Input:
 - exact original AusTraits source SHA verified by Stage92 parser.
 - source-derived original WFO/2026 exact species candidate ledger, with its
   immutable GitHub Actions artifact SHA supplied and verified.
 - original NHM/WCVP native plant ranges, SHA verified by Stage87 parser.
 - original Stage98B 72/37 geographic only cohort, SHA fixed.
No wind, bee encounter, learning, plume or response model fitted.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,statistics,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
for folder in ("floral_macro_stage87","floral_macro_stage92"):
    sys.path.insert(0,str(BASE/folder))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions
from austraits7_flower_diameter_source_audit import parse_original_austraits_zip

STAGE98B_SHA="8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7"
WFO_MEMBER="stage100_WFO_original_accepted_species_whole_flower_diameter_SOURCE_CANDIDATE.csv"
WFO_RECEIPT="stage100_original_eflora_flower_diameter_prose_candidate_receipt.json"
TRAIN_MEMBER="stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv"
HOLDOUT_MEMBER="stage98B_holdout_original_mainland_37_UNCHANGED.csv"

def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def source_ledger(path,expected_sha,accepted):
    if len(expected_sha)!=64 or any(x not in "0123456789abcdef" for x in expected_sha):
        raise ValueError("STAGE101_UNPINNED_SOURCE_WFO_DIGEST")
    if digest(path)!=expected_sha:
        raise ValueError("STAGE101_WFO_ORIGINAL_DERIVED_ARTIFACT_DIGEST_MISMATCH")
    with zipfile.ZipFile(path) as z:
        if WFO_MEMBER not in z.namelist() or WFO_RECEIPT not in z.namelist():
            raise ValueError("STAGE101_WFO_ORIGINAL_SPECIES_SOURCE_MEMBERS_MISSING")
        rows=list(csv.DictReader(io.StringIO(z.read(WFO_MEMBER).decode("utf-8-sig"))))
        receipt=json.loads(z.read(WFO_RECEIPT))
    if (receipt.get("n_original_source_unreviewed_flower_diameter_phrase_species")!=237 or
        receipt.get("n_original_source_only_corolla_width_not_whole_flower_species")!=58 or
        len(rows)!=295 or receipt.get("source_species_ledger_exact_rows")!=295):
        raise ValueError("STAGE101_WFO_TRUE_ORIGINAL_237_58_SOURCE_COHORT_CHANGED")
    results={};corolla={};providers={};modes={}
    for row in rows:
        sp=row["accepted_species_exact_WCVP"].casefold().strip()
        if not sp or sp not in accepted or sp in results or sp in corolla:
            raise ValueError("STAGE101_NONEXACT_OR_DUPLICATE_SOURCE_WFO_SPECIES")
        state=row["source_202606_WFO_prose_state"]
        if row["floral_size_description_manual_validation"]!="PENDING":
            raise ValueError("STAGE101_UNSUPPORTED_MANUALLY_VALIDATED_SIZE_CLAIM")
        mm=row.get("source_unreviewed_prose_whole_flower_diameter_mm") if state=="candidate_flower_diameter_from_prose" else row.get("source_corolla_width_only_NOT_whole_flower_mm")
        try:v=float(mm)
        except (TypeError,ValueError):raise ValueError("STAGE101_SIZE_CANDIDATE_NUMERIC_SOURCE_INVALID")
        if not 0.1<=v<=250:raise ValueError("STAGE101_ORIGINAL_PROSE_VALUE_OUT_OF_BOUNDS")
        if state=="candidate_flower_diameter_from_prose":
            results[sp]=v
        elif state=="candidate_corolla_width_only_NOT_whole_flower":
            corolla[sp]=v
        else:raise ValueError("STAGE101_NONWHOLERADIUS_SOURCE_STATE_IN_SIZE_LEDGER")
        providers[sp]=row["source_original_flora_providers"]
        modes[sp]=row["independent_GIFT_pollen_vector_mode"]
    if len(results)!=237 or len(corolla)!=58 or set(results)&set(corolla):
        raise ValueError("STAGE101_ORIGINAL_WFO_SIZE_SOURCE_DIAMETER_AND_COROLLA_COUNTS_CHANGED")
    return results,corolla,providers,modes

def frozen_mainland_codes(path):
    if digest(path)!=STAGE98B_SHA:
        raise ValueError("STAGE101_ORIGINAL_STAGE98B_GEOGRAPHY_SHA_CHANGED")
    with zipfile.ZipFile(path) as z:
        def read(member):
            if member not in z.namelist():raise ValueError("STAGE101_STAGE98B_MEMBER_MISSING")
            return list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig"))))
        t=read(TRAIN_MEMBER);h=read(HOLDOUT_MEMBER)
    train={r["TDWG_L3"] for r in t};holdout={r["TDWG_L3"] for r in h}
    if len(train)!=72 or len(holdout)!=37 or train&holdout:
        raise ValueError("STAGE101_STAGE98B_CONTACT_FREE_MAINLAND_FOLD_NOT_72_37")
    if any(r["land_scope"]!="mainland" or r["shared_split"]!="exploration" for r in t):
        raise ValueError("STAGE101_NONMAINLAND_TRAIN")
    if any(r["land_scope"]!="mainland" or r["shared_split"]!="holdout" for r in h):
        raise ValueError("STAGE101_NONMAINLAND_HOLDOUT")
    return train,holdout

def size_source_groups(native,aus,wfo,corolla,train_codes,holdout_codes):
    """Partition by geography and grade, never re-label prose as measured."""
    measured=set(aus);prose=set(wfo)
    both=measured&prose
    strict_measured_only=measured-prose
    prose_only=prose-measured
    union=measured|prose
    train_native=set().union(*(native[r] for r in train_codes))
    hold_native=set().union(*(native[r] for r in holdout_codes))
    grades={"AusTraits_measured_grade":measured,
        "WFO_textual_candidate_unreviewed":prose,
        "AusTraits_and_WFO_exact_species_overlap":both,
        "WFO_textual_only_not_direct_measured":prose_only,
        "source_union_ANY_size_record_not_all_direct_measured":union}
    summaries={}
    for label,source in grades.items():
        t=source&train_native;h=source&hold_native
        summaries[label]={
          "source_distinct_global_species":len(source),
          "source_contact_free_train_species":len(t),
          "source_original_holdout_species":len(h),
          "exact_reused_species_train_and_holdout":len(t&h),
          "distinct_holdout_species_NOT_seen_in_train":len(h-t),
          "distinct_holdout_genera_NOT_seen_in_train":len(
                 {s.split()[0] for s in h}-{s.split()[0] for s in t})}
    byregion=[]
    for code in sorted(train_codes|holdout_codes):
        species=native[code]
        vals={grade:len(species&grp) for grade,grp in grades.items()}
        byregion.append({"TDWG_L3":code,
           "predeclared_original_geographic_source_fold":"exploration" if code in train_codes else "holdout",
           "original_WCVP_native_species_total":len(species),
           **{"n_"+k:v for k,v in vals.items()},
           "n_unreviewed_WFO_corolla_width_only_NOT_whole_flower":len(species&set(corolla))})
    return summaries,byregion,grades

def run(wfo_archive,wfo_sha,aus_zip,nhm,wcvp,geo,outdir):
    traits,nhm_meta=load_nhm(nhm)
    native,wcvp_meta=wcvp_regions(wcvp,traits)
    universe=set().union(*native.values())
    if len(native)!=367 or len(universe)!=55775:
        raise ValueError("STAGE101_WCVP_ORIGINAL_NATIVE_55775_COHORT_CHANGED")
    aus,aus_receipt=parse_original_austraits_zip(aus_zip,universe)
    if len(aus)!=104:
        raise ValueError("STAGE101_ORIGINAL_AUSTRAITS104_SOURCE_UNIVERSE_DRIFTED")
    wfo,corolla,providers,wfo_modes=source_ledger(wfo_archive,wfo_sha,universe)
    train,holdout=frozen_mainland_codes(geo)
    if not ((train|holdout)<=set(native)):
        raise ValueError("STAGE101_GEOGRAPHIC_KEYS_NOT_IN_ORIGINAL_WCVP")
    groups,regions,cohorts=size_source_groups(native,aus,wfo,corolla,train,holdout)
    anysize=cohorts["source_union_ANY_size_record_not_all_direct_measured"]
    # Exact measured-vs-prose numeric agreement must not be assumed.
    both=sorted(set(aus)&set(wfo))
    ratios=[wfo[s]/aus[s] for s in both]
    ratios=[v for v in ratios if math.isfinite(v) and v>0]
    source_ratio={"n_exact_shared_species":len(both),
       "n_source_mappable_numeric_ratio":len(ratios),
       "median_WFO_prose_mm_over_author_AusTraits_mm":statistics.median(ratios) if ratios else None,
       "n_ratio_within_half_to_double":sum(.5<=v<=2 for v in ratios),
       "source_ratio_NOT_validated_same_flower_stage_or_population":True}
    source_cohort_stat={}
    for fold in ("exploration","holdout"):
        rows=[r for r in regions if r["predeclared_original_geographic_source_fold"]==fold]
        source_cohort_stat[fold]={
          "source_region_count":len(rows),
          "regions_with_at_least_10_original_AusTraits_measured":sum(
            r["n_AusTraits_measured_grade"]>=10 for r in rows),
          "regions_with_at_least_10_original_WFO_textual_candidate":sum(
            r["n_WFO_textual_candidate_unreviewed"]>=10 for r in rows),
          "regions_with_at_least_10_original_ANY_grade_size":sum(
            r["n_source_union_ANY_size_record_not_all_direct_measured"]>=10 for r in rows),
          "regions_with_at_least_5_original_ANY_grade_size":sum(
            r["n_source_union_ANY_size_record_not_all_direct_measured"]>=5 for r in rows)}
    out={"schema":"stage101_source_original_WCVP_mainland_size_grades_join_NOT_wind_fit",
      "original_source_artifact_SHA256":{"original_WFO_textual_candidates":wfo_sha,
         "original_Stage98B_72_37_geography":STAGE98B_SHA,
         "author_AusTraits7_original":aus_receipt["authentic_zipped_source_sha256"]},
      "source_grade_exact_species_and_holdout_overlap":groups,
      "source_old_AusTraits104_and_new_WFO237_overlap":source_ratio,
      "original_mainland_72exploration_37holdout_coverage":source_cohort_stat,
      "size_prose_candidate_is_NOT_confirmed_measurement":True,
      "corolla_width_candidate_never_promoted_to_flower_display":True,
      "source_size_unknown_not_a_zero_trait":True,
      "original_mainland_geo_and_species_names_unchanged":True,
      "no_wind_flower_size_ecological_coefficients_estimated":True,
      "phylogenetic_independence_NOT_established":True}
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage101_original_mainland_source_grade_flower_size_109_regions.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(regions[0]));w.writeheader();w.writerows(regions)
    (outdir/"stage101_original_mainland_3cue_size_source_union_receipt.json").write_text(
        json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("STAGE101_REAL_WFO_X_AUSTRAITS_DIAMETER_MAINLAND_SOURCE",
          json.dumps({"source_grades":groups,"numeric_overlap":source_ratio,
             "mainland_region_support":source_cohort_stat},sort_keys=True),flush=True)
    return out

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-WFO-stage100-artifact",type=Path,required=True)
    p.add_argument("--original-WFO-stage100-SHA256",required=True)
    p.add_argument("--original-AusTraits7",type=Path,required=True)
    p.add_argument("--original-NHM",type=Path,required=True)
    p.add_argument("--original-WCVP",type=Path,required=True)
    p.add_argument("--source-mainland-Stage98B-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    run(a.original_WFO_stage100_artifact,a.original_WFO_stage100_SHA256,
        a.original_AusTraits7,a.original_NHM,a.original_WCVP,
        a.source_mainland_Stage98B_ZIP,a.outdir)
