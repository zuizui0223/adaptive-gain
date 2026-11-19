#!/usr/bin/env python3
"""Stage96: join verified original source-only fragrance to 125 mainland cue support.

All inputs are SHA256-checked DERIVED GitHub Actions artifacts. Only geographic
eligibility / shared blocks fixed in Stage94; never select areas using wind, floral
signal values, bee richness or significance. Response-specific denominators are
not silently converted to identical species or complete cases. Source-positive
lexical descriptions != authentic physiological VOC or scentless negatives.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,zipfile
from pathlib import Path

SOURCE_SHA={
 "fragrance":"3f838cc1ed6841b136f122b9c8df695b842f46745cdff0edf10820e00905ec38",
 "three_cue":"326815aa9686c0063afb326bf67b9480969d47187759b37f32b9c36e488e0780"}
FILES={
 "fragrance":"stage93_derived/stage93_original_WFO_flora_scent_source_367_region_counts_INCLUDES_ISLANDS.csv",
 "fragrance_receipt":"stage93_derived/stage93_WFO_original_flora_source_scent_coverage.json",
 "three_cue":"stage94B_source_admitted_367_region_three_cue_support.csv"}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def open_zip(path,expected):
    if sha(path)!=expected:raise ValueError("STAGE96_FROZEN_SOURCE_DERIVED_SHA_MISMATCH")
    return zipfile.ZipFile(path)

def rows_from_archive(z,member):
    if member not in z.namelist():raise ValueError("STAGE96_MISSING_REQUIRED_SOURCE_MEMBER")
    items=list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig"))))
    if len(items)!=367:raise ValueError("STAGE96_NATIVE_REGION_NOT_367")
    out={x["TDWG_L3"]:x for x in items}
    if len(out)!=367:raise ValueError("STAGE96_DUPLICATE_OR_INVALID_TDWG3_KEY")
    return out

def join(a,b):
    if set(a)!=set(b) or len(a)!=367:raise ValueError("STAGE96_SOURCE_TDWG_REGION_COHORT_MISMATCH")
    allrows=[]
    for code in sorted(a):
        x=a[code];y=b[code]
        n=int(y["n_full_original_flora_descriptions"])
        pos=int(y["n_flora_scent_positive_SOURCE_CANDIDATE"])
        neg=int(y["n_flora_scent_explicit_negative_SOURCE_CANDIDATE"])
        unc=int(y["n_flora_scent_unmentioned_NOT_negative"])
        con=int(y["n_flora_scent_conflict"])
        if sum((pos,neg,unc,con))!=n:raise ValueError("STAGE96_SCENT_PROSE_NOT_PARTITIONED")
        if int(x["n_native_source_species"])!=int(y["n_native"]):
            raise ValueError("STAGE96_SOURCE_SPECIES_DENOMINATOR_MISMATCH")
        g={k:int(y[f"n_source_scent_positive_GIFT_{k}"]) for k in ("animal","wind","unknown")}
        if sum(g.values())!=pos:raise ValueError("STAGE96_GIFT_INDEPENDENT_MODE_COUNTS_NOT_CONSERVED")
        if x["source_geographic_scope"] not in ("mainland","island","mixed"):
            raise ValueError("STAGE96_UNVERIFIED_MAINLAND_SCOPE")
        if x["source_geographic_scope"]=="mainland" and x["shared_split"] not in ("exploration","holdout"):
            raise ValueError("STAGE96_UNFROZEN_MAINLAND_HOLDOUT")
        if x["source_geographic_scope"]!="mainland" and x["shared_split"]!="excluded":
            raise ValueError("STAGE96_ISLAND_SCOPE_LEAKAGE")
        allrows.append({**x,
           "n_original_WFO_full_flora_description_species":n,
           "n_source_floral_fragrance_lexical_positive":pos,
           "n_source_floral_fragrance_lexical_explicit_negative":neg,
           "n_source_floral_fragrance_lexical_undocumented":unc,
           "n_source_floral_fragrance_lexical_conflict":con,
           "n_source_floral_fragrance_positive_distinct_genera":int(y["n_scent_positive_distinct_genera"]),
           "n_scent_lexical_positive_GIFT_animal":g["animal"],
           "n_scent_lexical_positive_GIFT_wind":g["wind"],
           "n_scent_lexical_positive_GIFT_unknown":g["unknown"],
           "source_lexical_fragrance_fraction_among_explicit_reports":pos/(pos+neg) if pos+neg else "",
           "source_explicit_scent_reporting_fraction_of_descriptions":(pos+neg)/n if n else "",
           "actual_VOC_and_flower_odor_in_field_verified":"NO",
           "source_wind_flower_effect_estimated":"NO"})
    return allrows

def count(rows):
    d={"regions":len(rows),
       "spatial_blocks":len({r["spatial_block_id"] for r in rows if r["spatial_block_id"]})}
    cols=("n_original_WFO_full_flora_description_species",
      "n_source_floral_fragrance_lexical_positive",
      "n_source_floral_fragrance_lexical_explicit_negative",
      "n_scent_lexical_positive_GIFT_animal",
      "n_scent_lexical_positive_GIFT_wind",
      "n_scent_lexical_positive_GIFT_unknown")
    for k in cols:
        vals=[int(x[k]) for x in rows]
        d[k+"_species_x_region_appearances"]=sum(vals)
        for t in (1,5,10):d[k+"_regions_at_least_"+str(t)]=sum(v>=t for v in vals)
    d["regions_with_both_flora_scent_positive_and_explicit_negative"]=sum(
        x["n_source_floral_fragrance_lexical_positive"]>=1 and
        x["n_source_floral_fragrance_lexical_explicit_negative"]>=1 for x in rows)
    d["regions_with_at_least5_of_each_scent_report"]=sum(
        x["n_source_floral_fragrance_lexical_positive"]>=5 and
        x["n_source_floral_fragrance_lexical_explicit_negative"]>=5 for x in rows)
    d["regions_three_distinct_cue_source_counts_ge10_each"]=sum(
        int(x["n_positive_marking_TEXT_SOURCE_CANDIDATES"])>=10 and
        int(x["n_true_AusTraits_LABELLED_flower_diameter_species"])>=10 and
        x["n_source_floral_fragrance_lexical_positive"]>=10 for x in rows)
    return d

def run(fragrance_zip,three_cue_zip,outdir):
    with open_zip(fragrance_zip,SOURCE_SHA["fragrance"]) as z:
        b=rows_from_archive(z,FILES["fragrance"])
        receipt=json.loads(z.read(FILES["fragrance_receipt"]))
    if (receipt["unique_native_source_description_species"]!=27899 or
        receipt["scent_lexical_species_states"]!={"positive_candidate":420,
          "explicit_negative_candidate":105,"unmentioned_or_uncertain":27374}):
        raise ValueError("STAGE96_VERIFIED_ORIGINAL_SOURCE_FRAGRANCE_COHORT_CHANGED")
    with open_zip(three_cue_zip,SOURCE_SHA["three_cue"]) as z:
        a=rows_from_archive(z,FILES["three_cue"])
    joined=join(a,b)
    cohorts={
       "mainland":count([r for r in joined if r["source_geographic_scope"]=="mainland"]),
       "exploration":count([r for r in joined if r["shared_split"]=="exploration"]),
       "holdout":count([r for r in joined if r["shared_split"]=="holdout"]),
       "islands_excluded":count([r for r in joined if r["source_geographic_scope"]=="island"]),
       "mixed_excluded":count([r for r in joined if r["source_geographic_scope"]=="mixed"])}
    if (cohorts["mainland"]["regions"],cohorts["exploration"]["regions"],
        cohorts["holdout"]["regions"])!=(125,88,37):
        raise ValueError("STAGE96_GEOGRAPHIC_AND_HOLDOUT_SCOPE_CHANGED")
    result={"schema":"stage96_source_Sha_pinned_strict_mainland_fragrance_flower_cue_availability",
      "exact_derived_source_artifact_sha256":SOURCE_SHA,"source_cohorts":cohorts,
      "number_distinct_source_description_species_globally":27899,
      "source_420_positive_105_explicit_negative_species_are_lexical_unreviewed":True,
      "species_x_region_repetitions_are_NOT_independent_evolution":True,
      "unknown_fragrance_not_a_negative_phenotype":True,
      "source_plant_lineage_not_held_out_between_regions":True,
      "wind_cue_regression_NOT_fitted":True,
      "geographic_holdout_buffer_NOT_yet_verified":True,
      "three_responses_may_have_DIFFERENT_species_denominators":True}
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage96_native_367_original_floral_three_cue_source_availability.csv").open("w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(joined[0]));wr.writeheader();wr.writerows(joined)
    (outdir/"stage96_true_mainland_3cue_source_coverage_receipt.json").write_text(
        json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("STAGE96_REAL_WFO_MAINLAND_FRAGRANCE_THREE_CUE_SUPPORT",
          json.dumps(cohorts,sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--stage93-source-zip",type=Path,required=True)
    p.add_argument("--stage94B-source-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.stage93_source_zip,a.stage94B_source_zip,a.outdir)
