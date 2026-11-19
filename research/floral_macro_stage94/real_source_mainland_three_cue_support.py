#!/usr/bin/env python3
"""Stage94B: source-validated mainland cue *measurement support* only.

Join exact SHA-pinned derived results from original-source Stage91 marking
(never trait negatives), Stage92 AusTraits true labelled flower diameter,
and Stage94 independent geometrical island removal.

Counts by TDWG region are repeated native-species incidences, not independent
species or lineages. No measured wind, floral attraction or VOC is fitted.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,zipfile
from collections import Counter
from pathlib import Path

STAGE91="f1197a050d110d1e3626ab01f3c5d49626ac32fd0588d41ce3a162b44d921cdf"
STAGE92="01d76457aa8423b7964b5fccdfea597f5c158a805c138fd8597e7efd1733a05f"
STAGE94="3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833"
SOURCES={
    "stage91":(STAGE91,"stage91_global_TDWG3_3cue_availability_INCLUDES_ISLANDS.csv"),
    "stage92":(STAGE92,"stage92_AusTraits7_flower_diameter_367_regions_INCLUDES_ISLANDS.csv"),
    "stage94":(STAGE94,"stage94_original_367_mainland_island_mixed_registry.csv"),
    "split":(STAGE94,"stage94_original_mainland_shared_geoblock_split.csv"),
}

def checksum(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def read_derived_zip(path,expected_sha,member):
    if checksum(path)!=expected_sha:raise ValueError("SOURCE_DERIVED_ZIP_SHA_CHANGED_"+member)
    with zipfile.ZipFile(path) as z:
        if member not in z.namelist():raise ValueError("SOURCE_DERIVED_MEMBER_MISSING_"+member)
        rows=list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig"))))
    codes=[r.get("TDWG_L3","") for r in rows]
    if not rows or len(set(codes))!=len(rows) or not all(codes):
        raise ValueError("SOURCE_REGION_DUPLICATE_OR_MISSING")
    return {r["TDWG_L3"]:r for r in rows}

def merge(a,b,geo,split):
    universe=set(a)
    if len(universe)!=367 or set(b)!=universe or set(geo)!=universe:
        raise ValueError("STAGE94_SOURCE_UNIVERSE_367_NOT_EXACT")
    admitted={r for r,g in geo.items() if g["land_scope"]=="mainland"}
    if set(split)!=admitted:raise ValueError("STAGE94_REGION_SCOPE_VIOLATION")
    blocks={}
    out=[]
    for code in sorted(universe):
        x=a[code];y=b[code];g=geo[code];group=split.get(code,{})
        if int(x["n_native"])!=int(y["n_original_WCVP_native_species_in_region"]):
            raise ValueError("STAGE91_STAGE92_SOURCE_NATIVE_SPECIES_DENOMINATOR_MISMATCH_"+code)
        scope=g["land_scope"]
        if scope not in ("mainland","island","mixed"):raise ValueError("UNAUDITED_REGION_SCOPE")
        fold=group.get("shared_split","excluded")
        if scope=="mainland":
            if fold not in ("exploration","holdout"):raise ValueError("MAINLAND_SPLIT_MISSING")
            block=group["spatial_block_id"]
            if block in blocks and blocks[block]!=fold:
                raise ValueError("SOURCE_SPATIAL_BLOCK_LEAKS_BETWEEN_FOLDS")
            blocks[block]=fold
        else:
            if fold!="excluded":raise ValueError("ISLAND_MIXED_IN_MAINLAND_HOLDOUT")
            block=""
        row={"TDWG_L3":code,"source_geographic_scope":scope,"shared_split":fold,
            "spatial_block_id":block,"n_native_source_species":int(x["n_native"]),
            "n_positive_marking_TEXT_SOURCE_CANDIDATES":int(x["n_mark_positive_source_only"]),
            "n_marking_candidate_distinct_genera":int(x["n_marking_positive_genera"]),
            "n_true_AusTraits_LABELLED_flower_diameter_species":int(y["n_original_AusTraits_flower_diameter_species"]),
            "n_diameter_distinct_source_genera":int(y["n_distinct_source_diameter_genera"]),
            "n_diameter_source_GIFT_animal":int(y["n_diameter_species_GIFT_animal"]),
            "n_diameter_source_GIFT_wind":int(y["n_diameter_species_GIFT_wind"]),
            "n_diameter_source_GIFT_unknown":int(y["n_diameter_species_GIFT_UNKNOWN"]),
            "n_matched_VERIFIED_floral_fragrance_source_species":"PENDING_STAGE93_WFO_202606",
            "mainland_gust_flower_effect_fitted":"NO"}
        if (row["n_diameter_source_GIFT_animal"]+row["n_diameter_source_GIFT_wind"]+
            row["n_diameter_source_GIFT_unknown"]!=row["n_true_AusTraits_LABELLED_flower_diameter_species"]):
            raise ValueError("ORIGINAL_SOURCE_GIFT_SIZE_ARM_ACCOUNTING_MISMATCH")
        out.append(row)
    return out,blocks

def summary_for(rows):
    cc=Counter();items=("n_positive_marking_TEXT_SOURCE_CANDIDATES",
       "n_true_AusTraits_LABELLED_flower_diameter_species",
       "n_diameter_source_GIFT_animal","n_diameter_source_GIFT_wind")
    cc["regional_units"]=len(rows)
    for k in items:
        v=[int(r[k]) for r in rows]
        cc[k+"_species_by_region_appearances"]=sum(v)
        for t in (1,5,10,20):
            cc[k+"_regions_at_least_"+str(t)]=sum(x>=t for x in v)
    cc["both_markings_and_diameter_10_or_more_regions"]=sum(
        r["n_positive_marking_TEXT_SOURCE_CANDIDATES"]>=10 and
        r["n_true_AusTraits_LABELLED_flower_diameter_species"]>=10 for r in rows)
    cc["n_distinct_spatial_blocks"]=len({r["spatial_block_id"] for r in rows if r["spatial_block_id"]})
    return dict(cc)

def run(src91,src92,src94,out):
    a=read_derived_zip(src91,STAGE91,SOURCES["stage91"][1])
    b=read_derived_zip(src92,STAGE92,SOURCES["stage92"][1])
    g=read_derived_zip(src94,STAGE94,SOURCES["stage94"][1])
    s=read_derived_zip(src94,STAGE94,SOURCES["split"][1])
    allrows,blocks=merge(a,b,g,s)
    sections={
      "mainland":summary_for([x for x in allrows if x["source_geographic_scope"]=="mainland"]),
      "island_excluded":summary_for([x for x in allrows if x["source_geographic_scope"]=="island"]),
      "mixed_excluded":summary_for([x for x in allrows if x["source_geographic_scope"]=="mixed"]),
      "mainland_exploration":summary_for([x for x in allrows if x["shared_split"]=="exploration"]),
      "mainland_holdout":summary_for([x for x in allrows if x["shared_split"]=="holdout"])
    }
    record={"schema":"Stage94B_original_source_pinned_island_free_3cue_support_only",
        "source_artifact_SHA256":{"stage91":STAGE91,"stage92":STAGE92,"stage94":STAGE94},
        "cohorts":sections,
        "source_GIFT_wind_diameter_zero_regions_with_five_or_more":(
            sections["mainland"]["n_diameter_source_GIFT_wind_regions_at_least_5"]==0),
        "never_count_native_region_appearances_as_independent_evolution":True,
        "markings_source_lexical_positive_only_not_confirmed_true_prevalence":True,
        "petal_width_not_diameter_substitution_performed":False,
        "mainland_original_region_split_never_uses_wind_or_outcome":True,
        "fragrance_usable_estimand_premature":True,
        "ERA5_primary_1991_2020_10fg_not_retrieved":True,
        "no_wind_or_cue_effect_coefficients":True,
        "holdout_geographical_buffer_not_yet_verified":True}
    if sections["mainland"]["regional_units"]!=125 or sections["mainland_exploration"]["regional_units"]!=88 or sections["mainland_holdout"]["regional_units"]!=37:
        raise ValueError("STAGE94_ORIGINAL_MAINLAND_OR_SOURCE_SPLIT_COHORT_CHANGED")
    out.mkdir(parents=True,exist_ok=True)
    with (out/"stage94B_source_admitted_367_region_three_cue_support.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0].keys()));w.writeheader();w.writerows(allrows)
    (out/"stage94B_source_only_mainland_three_cue_measurement_gate.json").write_text(
        json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE94B_ACTUAL_ORIGINAL_DERIVED_CUE_SOURCE_SUPPORT",
          json.dumps(sections,sort_keys=True),flush=True)
    return record

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--stage91-source-zip",type=Path,required=True)
    p.add_argument("--stage92-source-zip",type=Path,required=True)
    p.add_argument("--stage94-geography-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.stage91_source_zip,a.stage92_source_zip,a.stage94_geography_zip,a.outdir)
