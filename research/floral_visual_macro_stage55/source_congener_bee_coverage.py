"""Stage55: all 159 directly measured 2016 UV species × author-modelled bee HEX.

Extends Stage52's 60-plant first-page coverage pilot to the full 159 GBIF
accepted source-measured Koski & Ashman species, retaining Stage54 Kew-native
same-genus, climate-caliper, opposite-UV candidate pairs. Only north-latitude
source windows are used: the original 2016 paper explicitly states that its
studied species' mean latitude spans 21.07–76.49 degrees NORTH.

The primary output is COVERAGE + paired DESCRIPTION, not an ecological or
phylogenetic causal effect. Original herbarium UV state may not apply to each
modern GBIF occurrence; shared Kew WGSRPD L3 nativity is not local sympatry;
first 100 indexed GBIF records per plant within source mean latitude ±4°
are a coverage sample, not a native distribution model; bee HEX measures
predicted source model taxon names, not visits, pollen movement or fitness.
Do not turn missing predicted bee HEX coverage into a true-zero guild.
"""
from __future__ import annotations
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import argparse
import csv
import json
import math
from pathlib import Path
import statistics
import sys

ROOT=Path(__file__).resolve().parents[1]
TIERS=("same_genus_and_overlapping_native_WGSRPD_L3",
       "source_lat10_UVB1200_temp6",
       "source_lat5_UVB700_temp4")
RULES=(("minimum5_records_2_hex",5,2),
       ("minimum15_records_3_hex",15,3))

def read_rows(path):
    with Path(path).open(encoding="utf8",newline="") as fp:
        return list(csv.DictReader(fp))

def original_taxon_task(row):
    key=row["GBIF_accepted_species_key"]
    status=row["UV_2016_original_measured_pattern"]
    lat=float(row["2016_original_latitude_N"])
    if not str(key).isdigit() or status not in (0,1) or not 20<=lat<=80:
        raise ValueError("NO_GO_SOURCE_2016_ACCEPTED_NORTHERN_UV_RECORD")
    return {
       "gbif_accepted_species_key":int(key),
       "original_mean_published_latitude_positive_deg":lat,
       "original_source_UV_pattern_binary":status
    }

def normalise_exposure(observed):
    n=int(observed["n_qualified_original_source_bee_HEX_records"])
    h=int(observed["n_distinct_visited_eligible_bee_hex_cells"])
    status=observed["GBIF_query_status"]
    bombus=observed["modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null"]
    allbee=observed["modelled_all_bee_names_per_visited_bee_hex_equal_cell_mean_or_null"]
    if (bombus is None)!=(allbee is None):
        raise ValueError("NO_GO_BEE_HEX_ONE_RICHNESS_MISSING_ONLY")
    if bombus is not None:
        if not (math.isfinite(bombus) and math.isfinite(allbee)
                and 0<=bombus<=allbee):
            raise ValueError("NO_GO_BEE_HEX_RICHNESS_OUTSIDE_SOURCE_BOUNDS")
    if not status.startswith(("GBIF_ORIGINAL_LATITUDE_WINDOW_ONE_PAGE",
                               "GBIF_API_UNAVAILABLE_UNKNOWN_NOT_ABSENCE")):
        raise ValueError("NO_GO_UNKNOWN_SOURCE_GBIF_STATUS")
    fraction=bombus/allbee if allbee is not None and allbee>0 else None
    return {
      "source_GBIF_status":status,
      "source_qualified_records":n,
      "source_eligible_bee_hex_cells":h,
      "modelled_Bombus_names_mean":bombus,
      "modelled_all_bee_names_mean":allbee,
      "modelled_Bombus_share_ratio_of_means_or_unknown":fraction,
      "source_observed_qualified_plant_records":n>0,
      "GBIF_sample_not_native_range":True
    }

def paired_contrasts(pairs,by_species,pattern_by_key):
    out=[]
    used_by_tier={}
    for p in pairs:
        tier=p["comparison_tier"]
        if tier not in TIERS:raise ValueError("NO_GO_UNRECOGNISED_CALIPER_TIER")
        a=str(p["UV_patterned_GBIF_key"])
        b=str(p["UV_uniform_GBIF_key"])
        if pattern_by_key.get(a)!=1 or pattern_by_key.get(b)!=0 or a==b:
            raise ValueError("NO_GO_DIRECT_UV_PATTERN_VS_UNIFORM_LABEL_MISMATCH")
        seen=used_by_tier.setdefault(tier,set())
        if a in seen or b in seen:
            raise ValueError("NO_GO_PAIR_NONINDEPENDENCE_WITHIN_TIER")
        seen.update((a,b))
        xa=by_species.get(a)
        xb=by_species.get(b)
        if xa is None or xb is None:
            raise ValueError("NO_GO_SOURCE_159_EXPOSURE_MISSING_TAXON_ROW")
        row={
            "comparison_tier":tier,
            "UV_patterned_GBIF_key":a,
            "UV_uniform_GBIF_key":b,
            "original_source_genus":p["same_original_study_genus"],
            "native_WGSRPD_L3_overlap_count":p["n_shared_Kew_verified_native_WGSRPD_L3"],
            "GBIF_first_index_page_not_verified_native_occurrence":True,
        }
        for label,nmin,hmin in RULES:
            okay=(xa["source_GBIF_status"]=="GBIF_ORIGINAL_LATITUDE_WINDOW_ONE_PAGE"
                  and xb["source_GBIF_status"]=="GBIF_ORIGINAL_LATITUDE_WINDOW_ONE_PAGE"
                  and xa["source_qualified_records"]>=nmin
                  and xb["source_qualified_records"]>=nmin
                  and xa["source_eligible_bee_hex_cells"]>=hmin
                  and xb["source_eligible_bee_hex_cells"]>=hmin
                  and xa["modelled_Bombus_share_ratio_of_means_or_unknown"] is not None
                  and xb["modelled_Bombus_share_ratio_of_means_or_unknown"] is not None)
            row[label+"_paired_coverage_ok"]=bool(okay)
            row[label+"_source_modelled_Bombus_fraction_pattern_minus_uniform"]=(
                xa["modelled_Bombus_share_ratio_of_means_or_unknown"]
                -xb["modelled_Bombus_share_ratio_of_means_or_unknown"]
                if okay else None)
            row[label+"_source_modelled_Bombus_names_pattern_minus_uniform"]=(
                xa["modelled_Bombus_names_mean"]-xb["modelled_Bombus_names_mean"]
                if okay else None)
            row[label+"_reason_if_unavailable"]=("" if okay else
                "UNKNOWN_OR_INSUFFICIENT_GBIF_SOURCE_COVERAGE_NOT_ZERO")
        out.append(row)
    return out

def summarize(exposures,pairs):
    result={}
    for tier in TIERS:
        group=[x for x in pairs if x["comparison_tier"]==tier]
        rules={}
        for label,nmin,hmin in RULES:
            eligible=[x for x in group if x[label+"_paired_coverage_ok"]]
            differences=[x[label+"_source_modelled_Bombus_fraction_pattern_minus_uniform"]
                         for x in eligible]
            loo=[statistics.mean(differences[:i]+differences[i+1:])
                 for i in range(len(differences))] if len(differences)>1 else []
            rules[label]={
               "minimum_source_qualified_GBIF_points_per_plant":nmin,
               "minimum_distinct_original_eligible_bee_HEX_per_plant":hmin,
               "n_pairs_with_both_modelled_exposures":len(eligible),
               "n_pairs_missing_any_endpoint_not_zero":len(group)-len(eligible),
               "n_distinct_source_genera_among_eligible_pairs":len(
                   {x["original_source_genus"] for x in eligible}),
               "mean_pattern_minus_uniform_modelled_Bombus_fraction_or_unknown":(
                   statistics.mean(differences) if differences else None),
               "median_pattern_minus_uniform_modelled_Bombus_fraction_or_unknown":(
                   statistics.median(differences) if differences else None),
               "positive_minus_negative_pair_counts":{
                   "positive":sum(x>0 for x in differences),
                   "negative":sum(x<0 for x in differences),
                   "zero":sum(x==0 for x in differences)},
               "leave_one_pair_out_mean_range_or_unknown":(
                   [min(loo),max(loo)] if loo else None),
               "two_genera_or_low_pair_coverage_not_an_independent_clade_test":True
            }
        result[tier]={"n_original_source_selected_opposite_UV_congener_pairs":len(group),
                      "coverage_tiers":rules}
    return {
       "status":"ORIGINAL_2016_SOURCE_159_UV_PLANTS_NORTHERN_GBIF_BEE_HEX_CONGENER_COVERAGE",
       "n_2016_source_measured_unique_GBIF_accepted_species":len(exposures),
       "n_original_159_with_any_qualified_Bee_HEX_plant_records":sum(
          x["source_qualified_records"]>0 for x in exposures.values()),
       "n_GBIF_API_unavailable_species":sum(
          x["source_GBIF_status"]=="GBIF_API_UNAVAILABLE_UNKNOWN_NOT_ABSENCE"
          for x in exposures.values()),
       "n_original_2016_source_species_with_at_least_5_quality_records_and_2_eligible_hex":sum(
          x["source_qualified_records"]>=5 and x["source_eligible_bee_hex_cells"]>=2
          for x in exposures.values()),
       "comparison_tiers":result,
       "never_claim_sister_species_or_local_native_cooccurrence":True,
       "do_not_advance_to_species_selection_or_pollinator_caused_fitness":True,
       "GBIF_first_index_page_not_native_range_or_random_occurrences":True,
       "modelled_Bombus_fraction_not_floral_visitor_function":True,
       "no_p_values_due_to_source_genera_and_nonrandom_data":True,
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-2016-159",required=True)
    parser.add_argument("--source-WCVP-159",required=True)
    parser.add_argument("--original-author-bee-hex-10242",required=True)
    args=parser.parse_args()
    for name in ("floral_visual_macro_stage54","floral_visual_macro_stage52",
                 "floral_visual_macro_stage47"):
        sys.path.insert(0,str(ROOT/name))
    from match_uv_measured_negative_congeners_native import data_join,analysis
    from source_latitude_hemisphere_gbif_pilot import (
        _request_hemisphere,_accumulate,read_published_bee_hex_rows)
    from align_uv_study_sites_to_bee_hex import (
        load_authenticated_shape_sources,polygons_from_original_shapefile)
    joined=data_join(read_rows(args.source_2016_159),read_rows(args.source_WCVP_159))
    pairrows,prior=analysis(joined)
    if len(joined)!=159:
        raise ValueError("NO_GO_NOT_159_KOSKI_ASHMAN_SOURCE_SPECIES")
    expected={"same_genus_and_overlapping_native_WGSRPD_L3":61,
              "source_lat10_UVB1200_temp6":53,
              "source_lat5_UVB700_temp4":45}
    if {k:v["n_nonoverlapping_opposite_UV_source_measured_congener_pairs"]
        for k,v in prior["tiers"].items()}!=expected:
        raise ValueError("NO_GO_SOURCE_NATIVE_CONGENER_PAIRS_CHANGED")
    model=read_published_bee_hex_rows(args.original_author_bee_hex_10242)
    members,centroids,_=load_authenticated_shape_sources()
    names,tree,transform,_=polygons_from_original_shapefile(members,centroids)
    if len(names)!=10242 or set(names)!=set(model):
        raise ValueError("NO_GO_ORIGINAL_BEE_PREDICTION_HEX_GEOMETRY_MISMATCH")
    tasks=[original_taxon_task(row) for row in joined]
    def one(task):
        source=_request_hemisphere(task,"N")
        measured=_accumulate(task,"N",source,names,tree,transform,model)
        return str(task["gbif_accepted_species_key"]),normalise_exposure(measured)
    with ThreadPoolExecutor(max_workers=5) as pool:
        exposures=dict(pool.map(one,tasks))
    if len(exposures)!=159:
        raise ValueError("NO_GO_SOURCE_ACCEPTED_PLANT_EXPOSURE_SET_UNIQUE")
    by_status={r["GBIF_accepted_species_key"]:r["UV_2016_original_measured_pattern"]
               for r in joined}
    contrasts=paired_contrasts(pairrows,exposures,by_status)
    receipt=summarize(exposures,contrasts)
    receipt["source_original_2016_DOI"]="10.1111/nph.13921"
    receipt["source_global_bee_model"]="Laborieux et al. 2026 author-tree PA-cutoff=5"
    receipt["source_original_bee_HEX_total"]=len(model)
    receipt["source_original_eligible_bee_HEX"]=sum(x["eligible"] for x in model.values())
    receipt["source_GBIF_occurrence_years"]="2000-2026"
    receipt["source_original_author_mean_latitude_window_degrees"]=4.0
    receipt["no_southern_hemisphere_inferred_from_author_original_northern_ranges"]=True
    output=Path("stage55_source_159_congener_bee_coverage")
    output.mkdir(exist_ok=True)
    with (output/"159_original_UV_species_first_page_Bombus_source_HEX_exposures.csv").open(
         "w",encoding="utf8",newline="") as fp:
        items=[{"gbif_accepted_species_key":k,**v} for k,v in sorted(exposures.items())]
        writer=csv.DictWriter(fp,fieldnames=list(items[0]))
        writer.writeheader();writer.writerows(items)
    with (output/"61_53_45_original_native_congener_source_Bombus_paired_coverage.csv").open(
         "w",encoding="utf8",newline="") as fp:
        writer=csv.DictWriter(fp,fieldnames=list(contrasts[0]))
        writer.writeheader();writer.writerows(contrasts)
    (output/"source_159_UV_congener_Bombus_coverage_receipt.json").write_text(
        json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+chr(10),
        encoding="utf8")
    print("STAGE55_ALL_159_ORIGINAL_SOURCE_UV_CONGENER_BEE_HEX_COVERAGE",
          json.dumps(receipt,ensure_ascii=False,sort_keys=True,allow_nan=False))
    print("NO_CAUSAL_ADAPTATION_NO_FIELD_BEE_VISIT_NO_SISTER_PHYLOGENY_INFERENCE")

if __name__=="__main__":
    main()
