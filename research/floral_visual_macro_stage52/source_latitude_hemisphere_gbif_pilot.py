"""Stage52: source-latitude anchored two-hemisphere plant/bee distribution pilot.

Original botanical measurement: Koski & Ashman 2016, New Phytol, directly
measured 177 UV traits (159 GBIF accepted species). All source-published
mean latitudes are numerically POSITIVE. Without knowing whether these
are signed/absolute we test BOTH northern and southern latitude bands,
never substituting a northern range merely because source number >0.

Prespecified 60-source-species balanced stratified PILOT: 10 species
sampled by immutable accepted-key hash in each of the 3 empirical
published-latitude terciles × 2 author UV states. Sample is determined
before ANY present-day GBIF occurrence or bee distribution is read.

GBIF occurrence data are transient: first bounded 100 records per
accepted species × hemisphere within ±4° of the original source
mean latitude, 2000-2026. SpeciesKey, coordinate uncertainty<=10km,
introduced status and *exact original HEX polygon* are audited.
Bee richness is original Laborieux et al. 2026 source tree/PA-cutoff
modelled taxa per eligible HEX, NOT bees observed at those plant flowers.
No source UV phenotype at GBIF points, no native-range/fitness inference
or significance test.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
for folder in ("floral_visual_macro_stage47","floral_visual_macro_stage50"):
    sys.path.insert(0,str(ROOT/folder))
from align_uv_study_sites_to_bee_hex import (
 load_authenticated_shape_sources,polygons_from_original_shapefile,
 matching_original_hex,
)
from pilot_original_uv_species_gbif_bee_hex import (
 _request_json,_is_introduction,
)

STUDY="10.1111/nph.13921"
PILOT_N=60
N_PER_SOURCE_LAT_TERCILE_AND_PATTERN=10
LAT_TOLERANCE_DEG=4.0
MAX_GBIF_PAGE=100
YEAR_RANGE=(2000,2026)
MAX_UNCERTAINTY=10000
SALT="stage52-source-UV-latitude-terciles-hemispheres-20261116"
MAX_WORKERS=5


def select_source_2016(rows):
    if len(rows)!=159:
        raise ValueError("NO_GO_ORIGINAL_2016_ACCEPTED_TAXA_NOT_159")
    distinct={r["gbif_accepted_species_key"] for r in rows}
    if len(distinct)!=159 or not all(k.isdigit() for k in distinct):
        raise ValueError("NO_GO_ORIGINAL_2016_ACCEPTED_SPECIES_NOT_DISTINCT")
    pattern=Counter(r["source_2016_UV_pattern"] for r in rows)
    if pattern!={"0":81,"1":78}:
        raise ValueError("NO_GO_ORIGINAL_2016_ACCEPTED_UV_STATES")
    output=[]
    for state in ("0","1"):
        source=[r for r in rows if r["source_2016_UV_pattern"]==state]
        source.sort(key=lambda r:(float(r["published_latitude_mean"]),
                                  r["gbif_accepted_species_key"]))
        # This is a rank tercile, not a globally comparable angular band.
        bounds=[source[:len(source)//3],
                source[len(source)//3:2*len(source)//3],
                source[2*len(source)//3:]]
        for groupidx,group in enumerate(bounds):
            if len(group)<N_PER_SOURCE_LAT_TERCILE_AND_PATTERN:
                raise ValueError("NO_GO_ORIGINAL_SOURCE_LAT_TERCILE_NOT_BALANCEABLE")
            ranked=sorted(group,key=lambda r:(
                hashlib.sha256((SALT+"|"+r["gbif_accepted_species_key"]).encode()).hexdigest(),
                r["gbif_accepted_species_key"]))
            for i,r in enumerate(ranked[:N_PER_SOURCE_LAT_TERCILE_AND_PATTERN]):
                lat=float(r["published_latitude_mean"])
                if not (0<lat<90):
                    raise ValueError("NO_GO_ORIGINAL_SOURCE_LATITUDE_SIGN_NOT_POSITIVE")
                output.append({
                    "gbif_accepted_species_key":int(r["gbif_accepted_species_key"]),
                    "original_source_UV_pattern_binary":int(state),
                    "original_latitude_tercile_within_pattern":groupidx+1,
                    "original_mean_published_latitude_positive_deg":lat,
                    "original_source_genus":r.get("original_2016_source_genus_or_unknown",""),
                    "original_source_UVB":float(r["published_uvb_mean"]),
                    "original_source_mean_temperature":float(r["published_annual_temp_mean"]),
                    "source_within_tercile_selection_rank":i+1
                })
    if len(output)!=PILOT_N or len({r["gbif_accepted_species_key"] for r in output})!=PILOT_N:
        raise ValueError("NO_GO_UNBALANCED_ORIGINAL_SOURCE_UV_PILOT")
    return output


def _request_hemisphere(taxon,hemisphere):
    mean=taxon["original_mean_published_latitude_positive_deg"]
    center=mean if hemisphere=="N" else -mean
    bounds=(max(-90,center-LAT_TOLERANCE_DEG),min(90,center+LAT_TOLERANCE_DEG))
    if not (-90<=bounds[0]<bounds[1]<=90):
        raise ValueError("NO_GO_ORIGINAL_SOURCE_HEMISPHERE_LAT_BOUNDS")
    q={
      "taxonKey":taxon["gbif_accepted_species_key"],
      "decimalLatitude":f"{bounds[0]:.4f},{bounds[1]:.4f}",
      "year":f"{YEAR_RANGE[0]},{YEAR_RANGE[1]}",
      "occurrenceStatus":"PRESENT",
      "hasCoordinate":"true",
      "hasGeospatialIssue":"false",
      "limit":MAX_GBIF_PAGE,"offset":0
    }
    try:
        res=_request_json(q)
        return {"status":"GBIF_ORIGINAL_LATITUDE_WINDOW_ONE_PAGE",
                "count":res["count"],"records":res["results"],
                "search_latitude_bounds":bounds}
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as err:
        return {"status":"GBIF_API_UNAVAILABLE_UNKNOWN_NOT_ABSENCE",
                "count":None,"records":[],
                "search_latitude_bounds":bounds,
                "error_kind":type(err).__name__}


def read_published_bee_hex_rows(path):
    with Path(path).open(encoding="utf8",newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=10242:
        raise ValueError("NO_GO_ORIGINAL_BEE_MODEL_SOURCE_HEX_COUNT")
    mapping={}
    status=Counter()
    for row in rows:
        cell=row.get("source_siteid")
        if not cell or cell in mapping:
            raise ValueError("NO_GO_DUPLICATE_OR_MISSING_SOURCE_BEE_HEX")
        eligible=row.get("eligibility")=="AUTHOR_TREE_AND_PA_CELL_CUTOFF"
        if eligible:
            n=row.get("n_source_tree_and_pa_cutoff_Bombus_taxa","")
            allbee=row.get("n_source_tree_and_pa_cutoff_all_bee_taxa","")
            if not n.isdigit() or not allbee.isdigit():
                raise ValueError("NO_GO_ELIGIBLE_ORIGINAL_BEE_HEX_NUMERIC")
            n=int(n);allbee=int(allbee)
            if n>allbee or n<0:
                raise ValueError("NO_GO_BEE_SOURCE_RICHNESS_GREATER_THAN_TOTAL")
            status["eligible"]+=1
            status["positive" if n>0 else "zero"]+=1
        else:
            n=allbee=None
            if row.get("n_source_tree_and_pa_cutoff_Bombus_taxa","") not in ("",None):
                raise ValueError("NO_GO_UNKNOWN_HEX_NOT_NULL_BEE_SOURCE")
            status["unknown"]+=1
        mapping[cell]={"eligible":eligible,"bombus":n,"allbee":allbee}
    if status!=Counter({"eligible":2695,"positive":1512,"zero":1183,"unknown":7547}):
        raise ValueError("NO_GO_AUTHENTIC_LABORIEUX_AUTHOR_FILTERED_HEX_STATUS")
    return mapping


def _accumulate(taxon,hemi,source,names,tree,transform,model):
    observed=set()
    cells=defaultdict(int)
    qa=Counter()
    for r in source["records"]:
        rid=r.get("key")
        if not isinstance(rid,int) or rid in observed:
            qa["missing_or_duplicate_GBIF_record_id"]+=1
            continue
        observed.add(rid)
        if r.get("speciesKey")!=taxon["gbif_accepted_species_key"]:
            qa["different_speciesKey"]+=1
            continue
        lon=r.get("decimalLongitude");lat=r.get("decimalLatitude")
        if not isinstance(lat,(int,float)) or not isinstance(lon,(int,float)):
            qa["non_numeric_coordinates"]+=1;continue
        if not (-180<=lon<=180 and source["search_latitude_bounds"][0]-1e-4<=lat<=source["search_latitude_bounds"][1]+1e-4):
            qa["coordinates_outside_requested_region"]+=1;continue
        if _is_introduction(r.get("establishmentMeans")):
            qa["explicit_non_native_or_cultivated"]+=1;continue
        uncertainty=r.get("coordinateUncertaintyInMeters")
        if not isinstance(uncertainty,(int,float)) or not math.isfinite(float(uncertainty)):
            qa["unknown_uncertainty"]+=1;continue
        if not 0<=uncertainty<=MAX_UNCERTAINTY:
            qa["uncertainty_over_10km"]+=1;continue
        match=matching_original_hex(lon,lat,names,tree,transform)
        if len(match)!=1:
            qa["hex_outside_or_boundary"]+=1;continue
        if match[0] not in model:
            raise ValueError("NO_GO_OCCURRENCE_HEX_NOT_IN_PUBLISHED_SOURCE")
        if not model[match[0]]["eligible"]:
            qa["unknown_Bee_model_hex_NOT_ZERO"]+=1;continue
        cells[match[0]]+=1
        qa["source_qualified_original_bee_HEX"]+=1
    values=[model[hexid] for hexid in sorted(cells)]
    return {
      "hemisphere":hemi,
      "GBIF_index_count":source["count"],
      "GBIF_query_status":source["status"],
      "n_first_page_original_records":len(source["records"]),
      "n_qualified_original_source_bee_HEX_records":sum(cells.values()),
      "n_distinct_visited_eligible_bee_hex_cells":len(cells),
      "modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null":(
          statistics.mean(row["bombus"] for row in values) if values else None),
      "modelled_all_bee_names_per_visited_bee_hex_equal_cell_mean_or_null":(
          statistics.mean(row["allbee"] for row in values) if values else None),
      "geospatial_quality_exclusions":dict(sorted(qa.items())),
      "not_source_native_range_or_actual_UV_measurement_sites":True,
    }


def _one_taxon(task,names,tree,transform,model):
    rows=[]
    for hemi in ("N","S"):
        sample=_request_hemisphere(task,hemi)
        rows.append(_accumulate(task,hemi,sample,names,tree,transform,model))
    index_counts={x["hemisphere"]:x["GBIF_index_count"] for x in rows}
    eligible_counts={x["hemisphere"]:x["n_qualified_original_source_bee_HEX_records"] for x in rows}
    sufficient={h:count>=5 for h,count in eligible_counts.items()}
    status=("BOTH_HEMISPHERES_HAVE_QUALIFIED_ORIGINAL_SOURCE" if all(sufficient.values())
            else "ONLY_N_QUALIFIED_IN_LATITUDE_WINDOW" if sufficient["N"]
            else "ONLY_S_QUALIFIED_IN_LATITUDE_WINDOW" if sufficient["S"]
            else "NEITHER_HAS_5_QUALIFIED_SOURCE_OCCURRENCES")
    return {
        **task,
        "comparison_original_published_latitude_signedness":status,
        "original_2016_published_mean_latitude_is_NOT_VERIFIED_as_signed":True,
        "source_hemisphere_N_GBIF":rows[0],
        "source_hemisphere_S_GBIF":rows[1],
        "n_source_hemispheres_meeting_minimum_5_quality_points":sum(sufficient.values()),
        "no_species_native_range_or_Bombus_guide_usage_estimated":True,
    }


def report(rows):
    if len(rows)!=PILOT_N:
        raise ValueError("NO_GO_NOT_60_ORIGINAL_2016_LAT_TERCILE_SPECIES")
    by_state=Counter(x["original_source_UV_pattern_binary"] for x in rows)
    by_tercile=Counter((x["original_source_UV_pattern_binary"],
                       x["original_latitude_tercile_within_pattern"]) for x in rows)
    if by_state!=Counter({0:30,1:30}) or len(by_tercile)!=6 or any(x!=10 for x in by_tercile.values()):
        raise ValueError("NO_GO_ORIGINAL_SOURCE_LATITUDE_TERCILE_UNBALANCED")
    statuses=Counter(x["comparison_original_published_latitude_signedness"] for x in rows)
    desc=[]
    for state in (0,1):
        group=[x for x in rows if x["original_source_UV_pattern_binary"]==state]
        for hemisphere in ("N","S"):
            viable=[x[f"source_hemisphere_{hemisphere}_GBIF"] for x in group
                    if x[f"source_hemisphere_{hemisphere}_GBIF"]["n_qualified_original_source_bee_HEX_records"]>=5
                    and x[f"source_hemisphere_{hemisphere}_GBIF"]["n_distinct_visited_eligible_bee_hex_cells"]>=2]
            desc.append({
              "source_UV_pattern_binary":state,"sampled_hemisphere":hemisphere,
              "n_species_at_least_5_quality_records_and_2_original_bee_cells":len(viable),
              "average_eligible_model_Bombus_names_across_species":(
                  statistics.mean(x["modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null"] for x in viable)
                  if viable else None),
              "average_eligible_model_all_bee_names_across_species":(
                  statistics.mean(x["modelled_all_bee_names_per_visited_bee_hex_equal_cell_mean_or_null"] for x in viable)
                  if viable else None),
              "descriptive_not_an_adjusted_UV_Bombus_hypothesis_test":True
            })
    return {
      "status":"ORIGINAL_2016_UV_60_LATITUDE_TERCILE_TWO_HEMISPHERE_BEE_HEX_SOURCE_COVERAGE",
      "n_pilot_2016_UV_species":len(rows),
      "source_UV_state_counts":dict(sorted(by_state.items())),
      "n_original_source_latitude_tercile_pairs":len(by_tercile),
      "hemispheric_validity_status_counts":dict(sorted(statuses.items())),
      "n_species_any_hemisphere_at_least_5_quality_points":sum(
          x["n_source_hemispheres_meeting_minimum_5_quality_points"]>0 for x in rows),
      "n_original_GBIF_api_query_unavailable":sum(
          x[f"source_hemisphere_{h}_GBIF"]["GBIF_query_status"]=="GBIF_API_UNAVAILABLE_UNKNOWN_NOT_ABSENCE"
          for x in rows for h in ("N","S")),
      "n_source_records_qualified_across_hemisphere_queries":sum(
          x[f"source_hemisphere_{h}_GBIF"]["n_qualified_original_source_bee_HEX_records"]
          for x in rows for h in ("N","S")),
      "group_by_published_UV_pattern_and_sampled_hemisphere":desc,
      "do_not_choose_hemisphere_by_pollinator_richness":True,
      "published_positive_mean_latitude_not_signed_without_author_validation":True,
      "source_GBIF_limited_first_index_page_not_native_range":True,
      "no_global_UV_pattern_by_Bombus_regression_or_significance":True,
      "no_measured_pollinator_information_use_seed_or_fitness":True,
    }


def main():
    args=argparse.ArgumentParser()
    args.add_argument("--source-2016",required=True)
    args.add_argument("--source-hex-model",required=True)
    opts=args.parse_args()
    with Path(opts.source_2016).open(encoding="utf8",newline="") as fp:
        original=list(csv.DictReader(fp))
    taxa=select_source_2016(original)
    model=read_published_bee_hex_rows(opts.source_hex_model)
    members,centroids,_=load_authenticated_shape_sources()
    names,tree,transform,_=polygons_from_original_shapefile(members,centroids)
    if len(names)!=10242 or set(names)!=set(model):
        raise ValueError("NO_GO_SOURCE_BEE_HEX_MODEL_AND_POLYGON_NOT_IDENTICAL")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        result=list(pool.map(
            lambda t:_one_taxon(t,names,tree,transform,model),taxa))
    summary=report(result)
    folder=Path("stage52_2016_original_latitude_occurrence_pilot")
    folder.mkdir(exist_ok=True)
    csvfile=folder/"original_2016_60_UV_species_N_S_latitude_beeHEX_exposure.csv"
    flat=[]
    for x in result:
        flat.append({k:(json.dumps(v,ensure_ascii=False,sort_keys=True)
                    if isinstance(v,(dict,list)) else v) for k,v in x.items()})
    with csvfile.open("w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(flat[0]))
        w.writeheader();w.writerows(flat)
    (folder/"source_hemisphere_and_original_bee_exposure_receipt.json").write_text(
       json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n",
       encoding="utf8")
    print("STAGE52_REAL_2016_UV_LATITUDE_BOTH_HEMISPHERE_OCCURRENCES",json.dumps(summary,sort_keys=True,ensure_ascii=False))
    print("SOURCE_2016_LATITUDE_SIGN_NOT_PROVEN_NO_VALID_UV_BOMBUS_GEOGRAPHIC_EFFECT")

if __name__=="__main__":
    main()
