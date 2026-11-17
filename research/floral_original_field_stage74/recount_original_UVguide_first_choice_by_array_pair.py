"""Stage74D: ORIGINAL 2021 field UV light × guide size experimental counts.

True-source raw arrays, not original published table counts:
FinnKosk_PollData_Final.xlsx -> UVLightArrays, BackgroundArrays.
Primary unit: paired randomized arrays within original high/low sites.
Records: each flower × insect-guild row, NOT independent treatment unit.

Report raw visit event counts and within-array-pair guide preference
contrasts only; no new confirmatory p/causal meta claim; prior experiment
already published causal interpretation. Spectral evidence source-locked
separately by Stage74C.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_original_field_stage72"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_original_field_stage73"))
from inspect_original_2021_UVguide_field_workbook import (
    manifest_meta,record_files_metadata,safe_source_download
)
from replay_original_kantsa2018_network_voc import read_xlsx_sparse
from audit_original_wisconsin_wind_visits import table_from_sheet

SOURCE_SHEET_NAMES=("UVLightArrays","BackgroundArrays")
REQ_FIELDS={
 "UVLightArrays":{"Elevation","Pop","ArrayNum","ArrayPair",
                  "ArrayType","Date","Flower","FlwType","Poll","FirstVisits"},
 "BackgroundArrays":{"Elevation","Pop","ArrayNum","ArrayPair",
                      "ArrayType","Date","Flower","FlwType","Poll","FirstVisits"}
}
EXPECTED_AUTHOR_DATA_ROWS={"UVLightArrays":648,"BackgroundArrays":312}


def numeric_visitor_count(value):
    s=str(value or "").strip()
    if not s or s.casefold() in {"na","nan","null","none"}:return None
    try:x=float(s)
    except ValueError:return None
    if x<0 or not math.isfinite(x) or x!=int(x):return None
    return int(x)

def source_original_workbook():
    meta,_=manifest_meta()
    listed={x.get("key",""):x for x in record_files_metadata(meta)}
    item=listed.get("FinnKosk_PollData_Final.xlsx")
    if not item:raise ValueError("STAGE74D_AUTHOR_ZENODO_ORIGINAL_VISIT_XLSX_NOT_LISTED")
    raw,proof=safe_source_download(item)
    books=read_xlsx_sparse(raw)
    return books,proof

def summarize_factor_sheet(books,sheet):
    header,rows=table_from_sheet(books[sheet])
    if not REQ_FIELDS[sheet].issubset(set(header)):
        raise ValueError("STAGE74D_ORIGINAL_SOURCE_MISSING_CRITICAL_FACTOR_"+sheet)
    if len(rows)!=EXPECTED_AUTHOR_DATA_ROWS[sheet]:
        raise ValueError(f"STAGE74D_SOURCE_ARRAY_SAMPLE_GRAIN_CHANGED_{sheet}_{len(rows)}")
    categorical={key:Counter() for key in ("Elevation","Pop","ArrayType","FlwType","Poll")}
    observed=Counter()
    array=defaultdict(lambda:defaultdict(Counter))
    pairs=defaultdict(lambda:defaultdict(lambda:defaultdict(Counter)))
    invalid=[]
    for i,row in enumerate(rows,2):
        for key in categorical:
            categorical[key][row[key]]+=1
        n=numeric_visitor_count(row.get("FirstVisits"))
        if n is None:
            invalid.append({"source_row":i,"value":row.get("FirstVisits")})
            continue
        observed["original_rows_with_known_first_visit_event_counts"]+=1
        observed["original_first_visits_all_rows"]+=n
        if n==0:observed["original_zero_recorded_first_visit_plant_guild_rows"]+=1
        if not row.get("ArrayPair") or not row.get("ArrayType"):
            raise ValueError("STAGE74D_SOURCE_ARRAY_TREATMENT_PAIR_NOT_PROVIDED")
        level=row["Elevation"].strip().casefold()
        treatment=row["ArrayType"].strip().casefold()
        choice=row["FlwType"].strip().casefold()
        visitor=row["Poll"].strip().casefold()
        arrkey=(level,row["Pop"].strip(),row["Date"].strip(),
                row["ArrayPair"].strip(),row["ArrayNum"].strip(),treatment)
        pairkey=arrkey[:4]
        array[arrkey][visitor][choice]+=n
        pairs[pairkey][treatment][visitor][choice]+=n
    original_armtypes=set(x[-1] for x in array)
    original_choice_types=set(r["FlwType"].strip().casefold() for r in rows)
    if len(original_choice_types)!=2:
        raise ValueError("STAGE74D_SOURCE_FLOWER_GUIDE_LEVELS_UNEXPECTED")
    if any(t not in {"s","l"} for t in original_choice_types):
        raise ValueError("STAGE74D_SOURCE_FLOWER_GUIDE_CODES_NOT_SMALL_LARGE")
    expected_array_size=12
    # Derive source arrays independently of insect rows, rather than
    # mistaking the original 648 flower×pollinator rows as randomized n.
    arrays=[]
    for key,obs in sorted(array.items()):
        allvis=sum(n for guild in obs.values() for n in guild.values())
        small=sum(guild.get("s",0) for guild in obs.values())
        large=sum(guild.get("l",0) for guild in obs.values())
        arrays.append({"original_array_id":"|".join(key),
          "original_elevation":key[0],
          "original_population":key[1],
          "original_date_Excel_serial":key[2],
          "original_pair_id":key[3],
          "original_array_number":key[4],
          "original_array_treatment":key[5],
          "n_original_first_visits_total":allvis,
          "n_original_first_visits_small_guide":small,
          "n_original_first_visits_large_guide":large,
          "n_original_bee_first_visits":sum(obs.get("bee",{}).values()),
          "n_original_fly_first_visits":sum(obs.get("fly",{}).values()),
          "source_array_treatment_is_one_experimental_unit":True})
    report={
      "original_sheet_name":sheet,
      "original_record_rows_flower_by_visitor":len(rows),
      "source_factor_level_counts_by_record_row":{k:dict(v) for k,v in categorical.items()},
      "source_verified_numeric_first_visit_rows":observed["original_rows_with_known_first_visit_event_counts"],
      "source_raw_first_visit_counts_sum":observed["original_first_visits_all_rows"],
      "source_original_recorded_first_visit_zero_rows":observed["original_zero_recorded_first_visit_plant_guild_rows"],
      "source_missing_invalid_first_visit_rows":invalid[:12],
      "original_distinct_randomized_array_ids":len(array),
      "original_distinct_source_elevation_population_date_pair_keys":len(pairs),
      "source_original_unique_array_treatment_levels":sorted(original_armtypes),
      "source_original_unique_flower_guide_codes":sorted(original_choice_types),
      "source_array_is_experimental_unit_not_row":True,
    }
    return arrays,pairs,report

def normalized_guide_arms(pairs):
    # Descriptive within-pair continuous contrast; do not call it a
    # confirmatory treatment odds ratio, p-value or replicated population.
    out=[]
    for key,arms in sorted(pairs.items()):
        for level,pollcounts in sorted(arms.items()):
            counts=Counter()
            for poll,v in pollcounts.items():
                counts["s"]+=v.get("s",0)
                counts["l"]+=v.get("l",0)
                counts["n"]=counts["s"]+counts["l"]
                counts["bee"]+=sum(v.values()) if poll=="bee" else 0
                counts["fly"]+=sum(v.values()) if poll=="fly" else 0
            out.append({
                "original_source_pair_id":"|".join(key),
                "source_elevation":key[0],
                "source_treatment":level,
                "original_first_visits_large":counts["l"],
                "original_first_visits_small":counts["s"],
                "original_first_visits_total":counts["n"],
                "source_large_guide_visit_fraction_if_recorded":(
                    counts["l"]/counts["n"] if counts["n"] else None),
                "source_bee_first_visits":counts["bee"],
                "source_fly_first_visits":counts["fly"],
                "no_visits_in_array_is_missing_choice_not_false_guide_absence":counts["n"]==0,
            })
    return out

def paired_treatment_summary(arms):
    levels=sorted({r["source_treatment"] for r in arms})
    pairgroup=defaultdict(dict)
    for row in arms:
        pairgroup[row["original_source_pair_id"]][row["source_treatment"]]=row
    result=Counter()
    by_elev=defaultdict(lambda:{"tested":0,"informative":0,"diffs":[]})
    for pair,d in pairgroup.items():
        level=pair.split("|")[0]
        by_elev[level]["tested"]+=1
        if len(d)!=2:
            result["source_pairs_not_two_treatment_arms"]+=1
            continue
        if any(v["source_large_guide_visit_fraction_if_recorded"] is None for v in d.values()):
            result["source_pairs_with_zero_total_first_visits_in_one_arm"]+=1
            continue
        # Only when source original level semantics can be read with confidence.
        ambient=[v for t,v in d.items() if "ambient" in t or t in {"control","normal_uv","uv"}]
        reduced=[v for t,v in d.items() if "reduc" in t or "block" in t]
        if len(ambient)==1 and len(reduced)==1:
            difference=(ambient[0]["source_large_guide_visit_fraction_if_recorded"]
                        -reduced[0]["source_large_guide_visit_fraction_if_recorded"])
            by_elev[level]["informative"]+=1
            by_elev[level]["diffs"].append(difference)
        else:
            result["source_arms_semantics_unresolved_for_paired_contrast"]+=1
    return {
       "source_arm_factor_levels":levels,
       "source_original_n_two_arm_pair_keys":len(pairgroup),
       "original_pair_diagnostic_counts":dict(result),
       "source_by_elevation_within_pair_UV_treatment_large_choice":{
           name:{"original_pair_keys":data["tested"],
                 "n_pairs_both_arms_with_known_visits":data["informative"],
                 "mean_paired_difference_ambient_minus_reduced_large_guide_visit_fraction":
                   sum(data["diffs"])/len(data["diffs"]) if data["diffs"] else None,
                 "n_positive_diff_pairs":sum(x>0 for x in data["diffs"]),
                 "n_negative_diff_pairs":sum(x<0 for x in data["diffs"]),
                 "n_zero_diff_pairs":sum(x==0 for x in data["diffs"])}
           for name,data in by_elev.items()},
       "paired_difference_is_source_descriptive_not_causal_MLE":True,
       "source_original_author_statistical_model_reanalysis_not_yet_done":True,
    }

def run():
    books,proof=source_original_workbook()
    if not all(s in books for s in SOURCE_SHEET_NAMES):
        raise ValueError("STAGE74D_AUTHOR_FIELD_SHEETS_MISSING")
    main_array,main_pairs,a=summarize_factor_sheet(books,"UVLightArrays")
    background,background_pairs,b=summarize_factor_sheet(books,"BackgroundArrays")
    main_arm=normalized_guide_arms(main_pairs)
    back_arm=normalized_guide_arms(background_pairs)
    return {
      "schema":"stage74d_2021_author_original_first_choice_UVguide_background_paired_source",
      "original_study_DOI":"10.1111/nph.17631",
      "source_Zenodo_DOI":"10.5281/zenodo.5110165",
      "source_workbook_sha256":proof["sha256"],
      "original_UV_light_factor_source_grain":a,
      "original_background_factor_source_grain":b,
      "source_original_UV_light_array_treatment_visits":main_array,
      "source_original_background_array_treatment_visits":background,
      "source_original_UV_light_source_pair_arms":main_arm,
      "source_original_background_source_pair_arms":back_arm,
      "source_UVguide_paired_condition_descriptive":paired_treatment_summary(main_arm),
      "source_first_visits_published_reference":377,
      "source_published_377_not_filled_or_imputed":True,
      "source_this_is_one_plant_species_not_macro_taxonomic_replication":True,
      "genuine_field_irradiance_and_background_manipulation_existing_2021":True,
      "no_new_adaptive_generalization_2026":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    args=p.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    d=run()
    (args.outdir/"2021_original_source_UVguide_light_background_first_choice_pair_receipt.json").write_text(
       json.dumps(d,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    # Light derived source summary accessible without redistributing original files
    print("STAGE74D_REAL_AUTHOR_2021_UV_GUIDE_FIRST_VISIT_SOURCE_RECOUNT",
          json.dumps({k:v for k,v in d.items() if k not in
                     ("source_original_UV_light_array_treatment_visits",
                      "source_original_background_array_treatment_visits",
                      "source_original_UV_light_source_pair_arms",
                      "source_original_background_source_pair_arms")},sort_keys=True))
    print("NO_648_ROWS_AS_648_INDEPENDENT_EXPERIMENTS_NO_NEW_CAUSAL_NOVELTY")
if __name__=="__main__":main()
