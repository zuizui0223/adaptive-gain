"""Stage51: return the 2021 UV study plants to their ORIGINAL Brazil study domain.

The GLOBAL first page of GBIF occurrences was missing Brazilian coverage
for all 30 sampled 2021 study taxa (Stage50). This run re-queries all 71
source-confirmed, accepted Tunes et al. (2021) plant species with Brazil
AND a fixed geographic window surrounding the 3 published original study
locations. Source study sites have no species-specific sample labels:
nearby GBIF observations are NOT proof of measured UV phenotype there.

Exact original bee study HEX polygons/CRS are reauthenticated at runtime;
the only source-model comparison here is original Stage47's fixed
3/4 modeled Bombus names at source study HEX, not an inferential fit.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
import argparse
import csv
import json
import math
from pathlib import Path
import sys
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
for fold in ("floral_visual_macro_stage47","floral_visual_macro_stage50"):
    sys.path.insert(0,str(ROOT/fold))
from align_uv_study_sites_to_bee_hex import (
    STUDY_SITES,load_authenticated_shape_sources,
    polygons_from_original_shapefile,matching_original_hex
)
from pilot_original_uv_species_gbif_bee_hex import (
    read_verified_source_species,_request_json,_is_introduction
)

SOURCE_DOI="10.3389/fpls.2021.618028"
COUNTRY="BR"
LAT_RANGE=(-23.5,-19.5)
LON_RANGE=(-50.0,-45.5)
YEAR_RANGE=(2010,2026)
PAGE_LIMIT=150
WORKERS=6
MAX_UNCERTAINTY=10000.0
SITE_HEX_BOMBUS_MODEL={"HEX8285":4,"HEX8318":3,"HEX8252":4}
SITE_HEX_ALLBEES_MODEL={"HEX8285":132,"HEX8318":137,"HEX8252":124}
NEAR_SITE_KM=50.


def select_original_source_species(rows):
    if len(rows)!=262:
        raise ValueError("NO_GO_ACCEPTED_LITERATURE_262_SOURCE_UNIVERSE")
    chosen=sorted(
      [{"key":int(r["gbif_accepted_species_key"]),
        "UV_binary":int(r["source_measured_UV_spatial_pattern_or_missing"])}
       for r in rows if SOURCE_DOI in r["source_study_DOIs"].split("|")],
      key=lambda x:x["key"])
    if len(chosen)!=71 or len({r["key"] for r in chosen})!=71:
        raise ValueError("NO_GO_2021_ORIGINAL_ACCEPTED_UV_TAXA_NOT_71")
    if any(x["UV_binary"] not in (0,1) for x in chosen):
        raise ValueError("NO_GO_ORIGINAL_UV_CATEGORY_NOT_DIRECT_BINARY")
    return chosen


def _haversine_km(lon,lat,otherlon,otherlat):
    la1=math.radians(lat);la2=math.radians(otherlat)
    dlat=la2-la1;dlon=math.radians(otherlon-lon)
    h=math.sin(dlat/2)**2+math.cos(la1)*math.cos(la2)*math.sin(dlon/2)**2
    return 2*6371.0088*math.asin(min(1.0,math.sqrt(h)))


def _near_original_site(lon,lat):
    # Santa Barbara's center is a DESCRIPTIVE midpoint of the original
    # published rectangle, not a point where a named source taxon was found.
    return min(_haversine_km(lon,lat,*s["coordinates_lonlat"][-1])
               for s in STUDY_SITES)<=NEAR_SITE_KM


def original_site_hexes(names,tree,transform):
    found=set()
    for site in STUDY_SITES:
        for lon,lat in site["coordinates_lonlat"]:
            matches=matching_original_hex(lon,lat,names,tree,transform)
            if len(matches)!=1:
                raise ValueError("NO_GO_ORIGINAL_2021_SITE_POINT_HEX_UNRESOLVED")
            found.add(matches[0])
    if found!=set(SITE_HEX_BOMBUS_MODEL):
        raise ValueError("NO_GO_ORIGINAL_2021_STUDY_HEX_DRIFT")
    return found


def _page(species):
    q={"taxonKey":species["key"],
       "country":COUNTRY,
       "decimalLatitude":",".join(map(str,LAT_RANGE)),
       "decimalLongitude":",".join(map(str,LON_RANGE)),
       "year":",".join(map(str,YEAR_RANGE)),
       "hasCoordinate":"true","hasGeospatialIssue":"false",
       "occurrenceStatus":"PRESENT",
       "limit":PAGE_LIMIT,"offset":0}
    try:
        obj=_request_json(q)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as e:
        return {"status":"GBIF_SOURCE_API_UNAVAILABLE_UNKNOWN_NOT_ZERO",
                "index_count":None,"records":[],"error":type(e).__name__}
    return {"status":"GBIF_BRAZIL_STUDY_REGION_ONE_INDEX_PAGE",
            "index_count":obj["count"],"records":obj["results"],"error":""}


def evaluate_taxon(species,page,names,tree,transform):
    quality=Counter()
    matched=set()
    sitehex=Counter()
    nnear=0
    raw=page["records"]
    ids=set()
    for r in raw:
        rid=r.get("key")
        if not isinstance(rid,int) or rid in ids:
            quality["duplicated_or_missing_gbif_record_key"]+=1;continue
        ids.add(rid)
        if r.get("speciesKey")!=species["key"]:
            quality["not_original_accepted_species_key"]+=1;continue
        lat=r.get("decimalLatitude");lon=r.get("decimalLongitude")
        if not isinstance(lat,(int,float)) or not isinstance(lon,(int,float)) or not (
            LAT_RANGE[0]<=lat<=LAT_RANGE[1] and LON_RANGE[0]<=lon<=LON_RANGE[1]):
            quality["not_valid_regional_WGS84_point"]+=1;continue
        if str(r.get("country","")).upper()!=COUNTRY:
            quality["not_Brazil_record"]+=1;continue
        if _is_introduction(r.get("establishmentMeans")):
            quality["reported_introduced_or_managed"]+=1;continue
        unc=r.get("coordinateUncertaintyInMeters")
        if not isinstance(unc,(int,float)) or not math.isfinite(float(unc)):
            quality["uncertainty_missing_not_accepted"]+=1;continue
        if not 0<=unc<=MAX_UNCERTAINTY:
            quality["coordinate_uncertainty_above_10km"]+=1;continue
        hits=matching_original_hex(lon,lat,names,tree,transform)
        if len(hits)!=1:
            quality["not_single_original_bee_polygon"]+=1;continue
        cell=hits[0]
        matched.add(cell)
        quality["quality_qualified_region_and_original_grid_point"]+=1
        if cell in SITE_HEX_BOMBUS_MODEL:
            sitehex[cell]+=1
            quality["original_source_3_study_site_HEX_record"]+=1
        if _near_original_site(lon,lat):
            nnear+=1
    return {
       "gbif_accepted_species_key":species["key"],
       "direct_original_UV_pattern_binary":species["UV_binary"],
       "original_UV_study_DOI":SOURCE_DOI,
       "source_gbif_region_index_count_or_unknown":page["index_count"],
       "source_api_status":page["status"],
       "n_GBIF_source_region_first_page_records":len(raw),
       "n_qualified_in_predeclared_region_and_original_bee_hex":quality[
           "quality_qualified_region_and_original_grid_point"],
       "n_qualified_points_within_50km_of_original_study_site":nnear,
       "n_qualified_points_in_original_study_site_candidate_HEX":sum(sitehex.values()),
       "original_study_site_candidate_HEX":sorted(sitehex),
       "n_original_study_site_candidate_HEX":len(sitehex),
       "original_site_source_modelled_Bombus_names_if_site_hex_covered":[
           SITE_HEX_BOMBUS_MODEL[x] for x in sorted(sitehex)],
       "original_site_source_modelled_all_bee_names_if_site_hex_covered":[
           SITE_HEX_ALLBEES_MODEL[x] for x in sorted(sitehex)],
       "n_all_original_hex_visited_in_regional_GBIF_bounded_page":len(matched),
       "quality_diagnostic_counts":dict(sorted(quality.items())),
       "no_original_taxon_by_exact_UV_measurement_site_annotation":True,
       "GBIF_record_no_proof_source_plant_UV_phenotype_measured_here":True,
       "not_complete_native_species_distribution_or_pollination":True
    }


def summary(rows):
    if len(rows)!=71:
        raise ValueError("NO_GO_NOT_ALL_71_ORIGINAL_ACCEPTED_STUDY_TAXA")
    states=Counter(x["direct_original_UV_pattern_binary"] for x in rows)
    group=[]
    for state in (0,1):
        sub=[r for r in rows if r["direct_original_UV_pattern_binary"]==state]
        group.append({
          "direct_original_UV_pattern_binary":state,
          "n_original_study_species":len(sub),
          "n_with_positive_GBIF_region_index_count":sum(
              (r["source_gbif_region_index_count_or_unknown"] or 0)>0 for r in sub),
          "n_with_high_quality_region_model_HEX_records":sum(
              r["n_qualified_in_predeclared_region_and_original_bee_hex"]>0 for r in sub),
          "n_with_any_record_in_original_site_candidate_HEX":sum(
              r["n_qualified_points_in_original_study_site_candidate_HEX"]>0 for r in sub)
        })
    return {
      "status":"ORIGINAL_2021_71_UV_SPECIES_BRAZIL_REGION_GBIF_AND_AUTHENTIC_SOURCE_HEX_FEASIBILITY",
      "original_direct_UV_taxa":len(rows),
      "original_pattern_class_counts":dict(sorted(states.items())),
      "n_species_with_positive_filtered_Brazil_region_GBIF_index":sum(
          (r["source_gbif_region_index_count_or_unknown"] or 0)>0 for r in rows),
      "n_species_with_valid_original_bee_source_polygon_record":sum(
          r["n_qualified_in_predeclared_region_and_original_bee_hex"]>0 for r in rows),
      "n_species_with_source_study_site_candidate_HEX_record":sum(
          r["n_qualified_points_in_original_study_site_candidate_HEX"]>0 for r in rows),
      "n_source_index_query_failures_not_absences":sum(
          r["source_api_status"]=="GBIF_SOURCE_API_UNAVAILABLE_UNKNOWN_NOT_ZERO" for r in rows),
      "total_source_region_GBIF_records_retrieved":sum(
          r["n_GBIF_source_region_first_page_records"] for r in rows),
      "total_quality_qualified_source_region_records":sum(
          r["n_qualified_in_predeclared_region_and_original_bee_hex"] for r in rows),
      "n_distinct_site_HEX_reached":len({v for r in rows
                                       for v in r["original_study_site_candidate_HEX"]}),
      "source_site_hex_modelled_Bombus_names":dict(SITE_HEX_BOMBUS_MODEL),
      "original_site_region_study_coords_2019_2021_not_species_specific":True,
      "bounded_Brazil_study_region_lonlat":{
          "longitude":list(LON_RANGE),"latitude":list(LAT_RANGE)},
      "by_UV_pattern_GBIF_spatial_support":group,
      "source_species_original_sample_sites_unknown":True,
      "not_same_as_GBIF_global_first_page_query":True,
      "not_UV_bee_causal_association_or_native_range":True,
      "not_a_valid_source_site_trait_SDM_regression":True
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--accepted-literature-csv",required=True)
    args=ap.parse_args()
    rows=read_verified_source_species(args.accepted_literature_csv)
    species=select_original_source_species(rows)
    members,centroids,_=load_authenticated_shape_sources()
    names,tree,transform,_=polygons_from_original_shapefile(members,centroids)
    original_site_hexes(names,tree,transform)
    with ThreadPoolExecutor(max_workers=WORKERS) as p:
        pages=list(p.map(_page,species))
    results=[
        evaluate_taxon(s,obs,names,tree,transform)
        for s,obs in zip(species,pages)
    ]
    report=summary(results)
    dest=Path("stage51_original_2021_Brazil_UV_species")
    dest.mkdir(exist_ok=True)
    with (dest/"71_Tunes_2021_UV_original_species_Brazil_study_region_GBIF_HEX.csv").open(
        "w",newline="",encoding="utf8") as f:
        flat=[{k:(json.dumps(v,ensure_ascii=False,sort_keys=True)
                  if isinstance(v,(list,dict)) else v)
               for k,v in r.items()} for r in results]
        w=csv.DictWriter(f,fieldnames=list(flat[0]))
        w.writeheader();w.writerows(flat)
    (dest/"source_restricted_Brazil_original_2021_UV_region_receipt.json").write_text(
         json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+"\n",
         encoding="utf8")
    print("STAGE51_ORIGINAL_UV_BRAZIL_REGION_COVERAGE",
          json.dumps(report,sort_keys=True,ensure_ascii=False,allow_nan=False))
    print("NO_ORIGINAL_SPECIES_MEASURED_SITE_ID_OR_UV_BOMBUS_CAUSAL_EFFECT")

if __name__=="__main__":
    main()
