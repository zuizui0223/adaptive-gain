#!/usr/bin/env python3
"""Stage111: REAL original-source 72 mainland exploration region 0.25° grid demand.

Freeze source identity before any weather/visual/olfactory/Bombus outcome:
  original Stage94 367 TDWG3 source topology, exactly 125 strict mainland
  original Stage98B 72 contact-free exploratory vs untouched 37 holdout
  original TDWG level3 polygon Git blob + Natural Earth10m continental land

First quantify COST of full grid-by-30yr Open-Meteo ERA5 model daily retrieval
as a lower-bound number of cells using maximum 800km2/0.25° WGS84 cell, and
an explicit geometric bounding-box upper envelope. Do NOT launch thousands
of public API queries from an unbudgeted pull-request.

Then select first THREE already-unrepresented geography blocks with source
mainland area <=40,000km2 and no repaired polygons, one smallest area region
per block, independent of climatic/plant/cue outcomes. Exact genuine WGS84
source mainland land area per 0.25° ERA5 cell is materialized ONLY for the
three predeclared candidate regions. Source future requests are not submitted.

All source original geometry/daily climatology semantics are explicit.
Any bloom-month gust/cue result remains UNESTIMATED in this stage.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from shapely.ops import unary_union
from shapely import to_wkb

BASE=Path(__file__).resolve().parents[1]
for folder in ("floral_macro_stage87","floral_macro_stage94","floral_macro_stage106"):
    sys.path.insert(0,str(BASE/folder))
from aggregate_global_tdwg3_worldclim_wind import (
   source_polygons,TDWG_GIT_BLOB_SHA1
)
from original_tdwg_naturalearth_strict_mainland import (
    original_natural_earth_land,area_km2,NATURAL_EARTH_LAND_ZIP_SHA256
)
from original_CDS_ERA5_025deg_mainland_area_weights import (
    source_mainland_registry,gitblob,index_grid_for_source_bbox,
    gridcell_land_area_weights,CDS_GRID_DEGREES,
    SOURCE_STAGE94_GEO_SHA
)

ORIGINAL_STAGE98B_SHA="8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7"
SOURCE_STAGE98B_TRAIN="stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv"
SOURCE_STAGE98B_HOLDOUT="stage98B_holdout_original_mainland_37_UNCHANGED.csv"
ALREADY_TRUE_GRID_REGION_CODES=("WDC","DEL","CAB")
EXPECTED_NEW_SOURCE_BLOCK_CODES=("GAM","KRY","BGM")
SOURCE_MAX_NEW_BUDGET_REGION_MAINLAND_KM2=40_000
SOURCE_NUMBER_NEW_GEOGRAPHIC_BLOCKS=3
SOURCE_MIN_CELL_KM2_LOWER_BOUND=800.0 # true max 0.25° WGS84 cell ~773 km2 at equator
SOURCE_MAX_SITES_PER_PROVIDER_QUERY=5
SOURCE_NUMBER_DECADES=3

def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def frozen_original_source_72(stage94,stage98B):
    registry,mainland=source_mainland_registry(stage94)
    reg={r["TDWG_L3"]:r for r in registry}
    if sha256(stage98B)!=ORIGINAL_STAGE98B_SHA:
        raise ValueError("STAGE111_ORIGINAL_72_37_GEOGRAPHY_SHA_DRIFT")
    with zipfile.ZipFile(stage98B) as z:
        if not {SOURCE_STAGE98B_TRAIN,SOURCE_STAGE98B_HOLDOUT}<=set(z.namelist()):
            raise ValueError("STAGE111_ORIGINAL_CONTACT_FREE_HOLDOUT_SOURCE_MISSING")
        train=list(csv.DictReader(io.StringIO(z.read(SOURCE_STAGE98B_TRAIN).decode("utf-8-sig"))))
        hold=list(csv.DictReader(io.StringIO(z.read(SOURCE_STAGE98B_HOLDOUT).decode("utf-8-sig"))))
    original_train={r["TDWG_L3"]:r for r in train}
    original_hold={r["TDWG_L3"]:r for r in hold}
    if ((len(original_train),len(original_hold))!=(72,37) or
        set(original_train)&set(original_hold) or
        not set(original_train)<=set(x["TDWG_L3"] for x in mainland) or
        not set(original_hold)<=set(x["TDWG_L3"] for x in mainland)):
        raise ValueError("STAGE111_ORIGINAL_FROZEN_SOURCE_MAINLAND_72_37_CHANGED")
    for code,r in original_train.items():
        if (r["land_scope"]!="mainland" or r["shared_split"]!="exploration"
            or r["admission"]!="exploration_contact_free"
            or r["spatial_block_id"]!=reg[code]["spatial_block_id"]
            or r["polygon_sha256"]!=reg[code]["polygon_sha256"]):
            raise ValueError("STAGE111_TRAIN_NOT_AUTHENTIC_FROZEN_MAINLAND_GEOGRAPHY")
    if any(r["shared_split"]!="holdout" for r in hold):
        raise ValueError("STAGE111_HOLDOUT_ORIGINAL_REASSIGNED")
    return reg,original_train,original_hold

def independent_geographic_choice(reg,train):
    included={train[c]["spatial_block_id"] for c in ALREADY_TRUE_GRID_REGION_CODES}
    if len(included)!=2 or len(set(train[c]["spatial_block_id"] for c in train))!=17:
        raise ValueError("STAGE111_ALREADY_VERIFIED_TWO_OF_SEVENTEEN_GEO_BLOCKS_CHANGED")
    rows=sorted((r for c,r in reg.items() if c in train),
        key=lambda r:(float(r["estimated_mainland_land_km2"]),r["TDWG_L3"]))
    chosen=[];used=set(included)
    for r in rows:
        code=r["TDWG_L3"];block=r["spatial_block_id"]
        if code in ALREADY_TRUE_GRID_REGION_CODES or block in used:
            continue
        if float(r["estimated_mainland_land_km2"])>SOURCE_MAX_NEW_BUDGET_REGION_MAINLAND_KM2:
            continue
        if int(r["original_TDWG_invalid_polygon_repaired"])!=0:
            continue
        used.add(block);chosen.append(code)
        if len(chosen)==SOURCE_NUMBER_NEW_GEOGRAPHIC_BLOCKS:break
    if tuple(chosen)!=EXPECTED_NEW_SOURCE_BLOCK_CODES:
        raise ValueError("STAGE111_SOURCE_GEOGRAPHY_ONLY_SELECTED_THREE_BLOCKS_DRIFT")
    return chosen

def cheap_all72_source_grid_demand(reg,train,source_geoms):
    rows=[]
    for code in sorted(train):
        r=reg[code];poly=source_geoms[code]
        source_hash=hashlib.sha256(to_wkb(poly,byte_order=1)).hexdigest()
        if source_hash!=r["polygon_sha256"]:
            raise ValueError("STAGE111_ORIGINAL_TDWG_WKB_HASH_MISMATCH_"+code)
        area=float(r["estimated_mainland_land_km2"])
        if area<=0:raise ValueError("STAGE111_NONPOSITIVE_ORIGINAL_SOURCE_MAINLAND_AREA")
        # Lower bound even at equator; may double-count the SAME reanalysis
        # grid cell in adjacent regions. This is a per-region demand measure.
        minimum=math.ceil(area/SOURCE_MIN_CELL_KM2_LOWER_BOUND)
        bounds=poly.bounds
        status="bbox_grid_ok"
        try:
            lat,lon=index_grid_for_source_bbox(poly)
            bbox_n=len(lat)*len(lon)
        except ValueError as exc:
            # Do not pretend regions crossing the antimeridian or projected
            # seam are trivially defined by WGS84 [-180,180) bounding cells.
            bbox_n=None
            status="UNRESOLVED_SOURCE_DATELINE_OR_GRID_BBOX_"+str(exc)[:100]
        rows.append({
            "TDWG_L3":code,
            "original_fixed_geographic_split":"exploration",
            "source_original_spatial_block":train[code]["spatial_block_id"],
            "source_original_mainland_land_km2":round(area,4),
            "source_unrepaired_TDWG_original_polygon":int(r["original_TDWG_invalid_polygon_repaired"])==0,
            "source_original_TDWG_WKB_SHA256":source_hash,
            "source_geometry_bbox_lonlat":json.dumps(list(bounds)),
            "source_025_gridcell_count_GEODESIC_AREA_LOWER_BOUND":minimum,
            "source_025_gridcell_count_POLYGON_BBOX_UPPER_BOUND":bbox_n,
            "source_5sites_three_decades_HTTP_requests_per_region_LOWER_BOUND":
                SOURCE_NUMBER_DECADES*math.ceil(minimum/SOURCE_MAX_SITES_PER_PROVIDER_QUERY),
            "source_5sites_three_decades_HTTP_requests_per_region_BBOX_UPPER_BOUND":
                SOURCE_NUMBER_DECADES*math.ceil(bbox_n/SOURCE_MAX_SITES_PER_PROVIDER_QUERY)
                 if bbox_n is not None else None,
            "source_GRID_EXACT_NEEDS_LANDCELL_INTERSECTION":"YES",
            "source_weather_source_not_queried":"YES",
            "source_grid_bbox_diagnostic_status":status})
    if len(rows)!=72:raise ValueError("STAGE111_NOT_72_SOURCE_GEO_REGIONS")
    return rows

def exact_new_landsource_weights(chosen,reg,geoms,mainland):
    rows=[];receipts=[]
    for code in chosen:
        source_land=geoms[code].intersection(mainland)
        if source_land.is_empty or not source_land.is_valid:
            raise ValueError("STAGE111_MAINLAND_REGION_TRUE_LAND_INTERSECTION_INVALID_"+code)
        lat,lon=index_grid_for_source_bbox(source_land)
        W=gridcell_land_area_weights(source_land,lat,lon)
        area=area_km2(source_land)
        total=float(W.sum())
        if not (.985<=total/area<=1.015):
            raise ValueError("STAGE111_TRUE_CELL_AREAS_DO_NOT_SUM_TO_REGION_MAINLAND_"+code)
        prior=float(reg[code]["estimated_mainland_land_km2"])
        if not (.985<=area/prior<=1.015):
            raise ValueError("STAGE111_REAL_NATURAL_EARTH_REGION_MAINLAND_AREA_CHANGED_"+code)
        coords=[]
        for (i,j),weight in np.ndenumerate(W):
            if weight<=0:continue
            cell={"TDWG_L3":code,
              "ERA5_source_025_grid_latitude":float(lat[i]),
              "ERA5_source_025_grid_longitude":float(lon[j]),
              "source_original_geodesic_mainland_area_km2":round(float(weight),8),
              "source_original_TDWG_polygon_SHA256":reg[code]["polygon_sha256"],
              "source_no_weather_data_retrieved":"YES"}
            coords.append(cell)
        weights=np.asarray([v["source_original_geodesic_mainland_area_km2"] for v in coords])
        if not len(weights):
            raise ValueError("STAGE111_NO_REAL_SOURCE_LAND_GRID_INTERSECTIONS")
        neff=float(weights.sum()**2/np.sum(weights**2))
        # Source identity and 0.25° centre are both necessary; the public
        # delivery provider may return a different point and must fail.
        receipts.append({
            "TDWG_L3":code,
            "source_original_geographic_block":reg[code]["spatial_block_id"],
            "source_actual_polygon_mainland_land_area_km2":float(area),
            "source_actual_025_grid_land_intersection_area_km2":total,
            "source_true_intersected_025_ERA5_gridcells":len(coords),
            "source_effective_land_gridcell_number":neff,
            "source_original_025_gridcell_lat_bounds":[float(lat.min()),float(lat.max())],
            "source_original_025_gridcell_lon_bounds":[float(lon.min()),float(lon.max())],
            "source_5site_x_3decade_requests_for_COMPLETE_REGION":(
                  3*math.ceil(len(coords)/5)),
            "no_1991_2020_climate_retrieved_for_new_region":True,
            "no_biological_response_opened":True})
        rows.extend(coords)
    if len({(r["ERA5_source_025_grid_latitude"],r["ERA5_source_025_grid_longitude"])
            for r in rows})!=len(rows):
        raise ValueError("STAGE111_CROSS_REGION_SELECTED_SOURCE_GRID_CELL_COLLISION")
    return rows,receipts

def run(stage94,stage98B,tdwg_source,naturalearth_source,outdir):
    reg,train,hold=frozen_original_source_72(stage94,stage98B)
    chosen=independent_geographic_choice(reg,train)
    if gitblob(tdwg_source)!=TDWG_GIT_BLOB_SHA1:
        raise ValueError("STAGE111_NOT_ORIGINAL_TDWG_GIT_BLOB")
    source_geoms,_,_=source_polygons(tdwg_source)
    plan=cheap_all72_source_grid_demand(reg,train,source_geoms)
    parts,main,meta=original_natural_earth_land(naturalearth_source)
    mainland=unary_union([parts[i] for i in sorted(main)])
    exact,region=exact_new_landsource_weights(chosen,reg,source_geoms,mainland)
    if any(next(x for x in plan if x["TDWG_L3"]==r["TDWG_L3"])[
        "source_025_gridcell_count_GEODESIC_AREA_LOWER_BOUND"]>
        r["source_true_intersected_025_ERA5_gridcells"] for r in region):
        raise ValueError("STAGE111_AREA_LOWER_BOUND_SOURCE_GRIDCELL_TOO_HIGH")
    total_lower=sum(x["source_025_gridcell_count_GEODESIC_AREA_LOWER_BOUND"] for x in plan)
    min_requests=sum(x["source_5sites_three_decades_HTTP_requests_per_region_LOWER_BOUND"] for x in plan)
    receipt={
        "schema":"stage111_original_source_72_contact_free_mainland_ERA5_025_grid_demand",
        "source_stage94_original_geography_SHA256":SOURCE_STAGE94_GEO_SHA,
        "source_stage98B_original_train72_holdout37_SHA256":ORIGINAL_STAGE98B_SHA,
        "source_TDWG_original_geojson_Git_blob":TDWG_GIT_BLOB_SHA1,
        "source_NaturalEarth_original_mainland_land_ZIP_SHA256":NATURAL_EARTH_LAND_ZIP_SHA256,
        "source_continent_connected_landmass_metadata":meta,
        "source_original_72_exploration_regions":len(train),
        "source_original_37_holdout_unchanged_and_unopened":len(hold),
        "source_geography_blocks_in_72":len({x["spatial_block_id"] for x in train.values()}),
        "source_original_three_complete_model_area_region_codes":list(ALREADY_TRUE_GRID_REGION_CODES),
        "source_original_model_area_regions_cover_geographic_blocks":2,
        "source_original_exploration_total_land_area_km2":sum(
             float(reg[k]["estimated_mainland_land_km2"]) for k in train),
        "source_lower_bound_separate_region_025_gridcells_using_800km2_max_cell":total_lower,
        "source_lower_bound_separate_region_requests_five_sites_three_decades":min_requests,
        "source_lower_bound_ignores_reuse_of_adjacent_region_shared_cells":True,
        "source_data_provider_quota_must_be_respected_no_bulk72_automatic_query":True,
        "source_eligible_smallest_geography_only_3_new_region_codes":chosen,
        "source_3_new_exact_mainland_geodesic_cell_regions":region,
        "source_no_weather_requests_submitted":True,
        "source_no_ERA5_CDS_hourly_10fg_source_obtained":True,
        "source_no_WFO_NHM_AusTraits_Bombus_outcomes_read":True,
        "original_holdout_37_cue_data_NOT_used_in_selection":True,
        "source_full72_original_0p25_geodesic_area_grid_weights_NOT_YET_COMPUTED":True}
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage111_original72_mainland_geographic_025grid_budget_NO_outcomes.csv").open(
         "w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(plan[0]));w.writeheader();w.writerows(plan)
    with (outdir/"stage111_original_3_new_geoblocks_true_ERA5_025_land_area_cells_NO_climate.csv").open(
        "w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(exact[0]));w.writeheader();w.writerows(exact)
    (outdir/"stage111_original72_source_025_ERA5_grid_budget_receipt_NO_floral_model.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print("STAGE111_GENUINE_SOURCE_72_MAINLAND_GEOGRAPHIC_GRID_DEMAND",json.dumps({
        "source_exploration_region_n":len(train),"geographic_blocks_n":receipt["source_geography_blocks_in_72"],
        "source_land_area_km2":round(receipt["source_original_exploration_total_land_area_km2"]),
        "separate_region_gridcell_lower_bound":total_lower,
        "separate_region_public_ERA5_model_5sites_3decades_request_lower_bound":min_requests,
        "exact_new_3_regions":{x["TDWG_L3"]:x["source_true_intersected_025_ERA5_gridcells"] for x in region},
        "no_botanical_outcomes_opened":True},sort_keys=True),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage94-geography-ZIP",required=True,type=Path)
    p.add_argument("--original-Stage98B-geographic-training-ZIP",required=True,type=Path)
    p.add_argument("--original-TDWG-geojson",required=True,type=Path)
    p.add_argument("--original-NaturalEarth-land-ZIP",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.original_Stage94_geography_ZIP,
        a.original_Stage98B_geographic_training_ZIP,
        a.original_TDWG_geojson,a.original_NaturalEarth_land_ZIP,a.outdir)
