#!/usr/bin/env python3
"""Stage110: public ERA5 model 1991-2020 mainland 0.25° grids, DEL & CAB.

34 independently source-geometric preselected original model grid centres:
DEL Delaware United States 16 (NOT Delhi India); CAB Cabinda Angola 18.
Original mainland-only region intersection area already SHA-validated Stage106.
For each 0.25° model centre: retrieve real daily 10m wind gust MAX (m/s) and
2m temperature MEAN (C) across 1991–2020 from Open-Meteo model=ERA5 public
historical archive; compute its own 30yr monthly T>5C flowering season
and fraction daily gust strictly>15m/s (10,20 sensitivity), then geodesic
original-cell mainland-intersection km² weighted area mean.

Not a source-validated ECMWF CDS original hourly 10fg, not a global 125-region
result, not bee landing, cue ordering, or independently measured flower size.
Never open plant/fungus/bee/holdout outcomes; fail on source model cell shift.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,re,sys,time,zipfile
from collections import Counter
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage95"))
sys.path.insert(0,str(BASE/"floral_macro_stage109"))
from original_ERA5_1991_2020_gust_five_mainland_pilot import (
    api_url,parse_decade,climatology,YEARS)
from original_geogrid_public_ERA5_1991_2020_WDC_area_gust import (
    sha256,GEO_MEMBER,GEO_RECEIPT,SOURCE_STAGE106_GEO_SHA,
    accepted_grid_coordinates,source_decade_with_bounded_provider_retries)

REQUEST_GROUP_MAX=5
SECONDS_BETWEEN_GROUPS=68
SECONDS_BETWEEN_DECADES=12
SOURCE_REGIONS=("DEL","CAB")
EXPECTED_COUNTS={"DEL":16,"CAB":18}
# Original Stage106 three source-smallest strictly continent-connected
# mainland regions are WDC, DEL, CAB. Exclude WDC in this new independent
# source extension because it has already completed Stage109.
ORIGINAL_LANDAREA_TOLERANCE_RATIO=.015

# Source-authenticated actual prior CI #44743993401 15 DEL original source cells.
# This is a REAL derived climatology artifact, not a substitute for raw CDS.
PRIOR_STAGE110_15DEL_SOURCE_SHA256="971320cc978ec35e2eb1b2f2492c541d948aaa337d92294e186ea16cf9c78b5a"

def normalize_source_era5_response(payload,requested_sites):
    """Open-Meteo one coordinate => dict; >=2 coordinates => list."""
    if requested_sites==1 and isinstance(payload,dict) and "daily" in payload:
        return [payload]
    if isinstance(payload,list) and len(payload)==requested_sites and all(
            isinstance(x,dict) and "daily" in x for x in payload):
        return payload
    raise ValueError("STAGE110_SOURCE_RESPONSE_SHAPE_OR_SITE_COUNT_INVALID")

def original_verified_partial_DEL15(source_artifact,by_region):
    """Reuse exactly 15 full 30-year source cells and verify original request hashes."""
    if sha256(source_artifact)!=PRIOR_STAGE110_15DEL_SOURCE_SHA256:
        raise ValueError("STAGE110_PRIOR_REAL_15_SOURCE_ARCHIVE_SHA_MISMATCH")
    output={}
    with zipfile.ZipFile(source_artifact) as z:
        if len(z.namelist())!=3:
            raise ValueError("STAGE110_PRIOR_SOURCE_PARTIAL_ARCHIVE_NOT_EXACT_3_GROUPS")
        for i in range(3):
            name=f"stage110_partial_source_DEL_group_{i:02d}_NOT_full_region.json"
            if name not in z.namelist():
                raise ValueError("STAGE110_SOURCE_COMPLETED_GROUP_ID_MISSING")
            d=json.loads(z.read(name))
            if (d["source_status"]!="PARTIAL_REGION_GROUP_NOT_ALL_34_SOURCE_CELLS"
                or d["original_region"]!="DEL"
                or d["source_group_index"]!=i
                or d["original_cellcount_in_group"]!=5
                or not d["never_claim_full_region_if_remaining_groups_fail"]):
                raise ValueError("STAGE110_PARTIAL_SOURCE_PRIOR_METADATA_DRIFT")
            sites=by_region["DEL"][i*5:(i+1)*5]
            prior=d["source_original_1991_2020_cell_climatologies"]
            reqs=d["original_API_request_SHAs_last_group"]
            if len(prior)!=len(sites) or len(reqs)!=len(YEARS):
                raise ValueError("STAGE110_PARTIAL_SOURCE_PRIOR_ORIGINAL_SITE_OR_DECADE_COUNT")
            for site,src in zip(sites,prior):
                if (site["TDWG_L3"]!=src["TDWG_L3"]
                    or site["lat"]!=src["lat"] or site["lon"]!=src["lon"]
                    or abs(site["source_grid_mainland_intersection_km2"]-
                           src["source_grid_mainland_intersection_km2"])>1e-7
                    or site["source_original_TDWG_polygon_SHA256"]!=src["source_original_TDWG_polygon_SHA256"]
                    or src["original_30y_cell_ERA5_model_daily"]["source_ERA5_observed_30yr_days"]!=10958):
                    raise ValueError("STAGE110_CACHED_SOURCE_REGION_GEODESIC_OR_30YR_IDENTITY_DRIFT")
                la,lo=src["original_model_returned_grid_latlon"]
                accepted_grid_coordinates(site,{"latitude":la,"longitude":lo})
            for req,(y1,y2) in zip(reqs,YEARS):
                if (req["TDWG_L3"]!="DEL" or req["source_group"]!=i
                    or req["source_decade"]!=f"{y1}-{y2}"
                    or req["source_variable_model"]!="ERA5"
                    or req["original_ERA5_daily_model_API_URL"]!=
                       api_url(sites,f"{y1}-01-01",f"{y2}-12-31")
                    or not re.fullmatch(r"[a-f0-9]{64}",req["original_unmodified_public_source_JSON_SHA256"])
                    or int(req["original_source_response_bytes"])<10000):
                    raise ValueError("STAGE110_PRIOR_DERIVED_SOURCE_ORIGINAL_REQUEST_SHAS_DRIFT")
            output[i]={"sites":prior,"requests":reqs}
    return output

def frozen_original_mainland_cell_sets(geo_artifact):
    if sha256(geo_artifact)!=SOURCE_STAGE106_GEO_SHA:
        raise ValueError("STAGE110_NOT_STAGE106_TRUE_ORIGINAL_SOURCE_LANDAREA_SHA")
    with zipfile.ZipFile(geo_artifact) as z:
        if not {GEO_MEMBER,GEO_RECEIPT}<=set(z.namelist()):
            raise ValueError("STAGE110_ORIGINAL_SOURCE_AREA_MEMBER_MISSING")
        rows=list(csv.DictReader(io.StringIO(z.read(GEO_MEMBER).decode("utf-8-sig"))))
        receipt=json.loads(z.read(GEO_RECEIPT))
    q={x["TDWG_L3"]:x for x in receipt["source_three_geometry_only_preflight_regions"]}
    if set(q)!={"WDC","DEL","CAB"}:
        raise ValueError("STAGE110_ORIGINAL_GEOGRAPHY_SELECTION_CHANGED")
    by_region={}
    all_coords=set()
    for code in SOURCE_REGIONS:
        items=[r for r in rows if r["TDWG_L3"]==code]
        if len(items)!=EXPECTED_COUNTS[code]:
            raise ValueError("STAGE110_ORIGINAL_REGION_SOURCE_CELLCOUNT_DRIFT_"+code)
        sites=[]
        for r in sorted(items,key=lambda r:(float(r["ERA5_atmosphere_source_grid_latitude"]),
                                              float(r["ERA5_atmosphere_source_grid_longitude"]))):
            lat=float(r["ERA5_atmosphere_source_grid_latitude"])
            lon=float(r["ERA5_atmosphere_source_grid_longitude"])
            weight=float(r["source_intersected_original_mainland_land_km2"])
            key=(lat,lon)
            if key in all_coords or not math.isfinite(weight) or weight<=0:
                raise ValueError("STAGE110_SOURCE_GEO_DUPLICATE_OR_INVALID_WEIGHT")
            if abs(lat*4-round(lat*4))>1e-6 or abs(lon*4-round(lon*4))>1e-6:
                raise ValueError("STAGE110_ORIGINAL_GEO_NOT_025ERA5_GRID")
            all_coords.add(key)
            sites.append({"TDWG_L3":code,"lat":lat,"lon":lon,
              "source_grid_mainland_intersection_km2":weight,
              "source_original_TDWG_polygon_SHA256":r["source_region_original_TDWG_polygon_SHA256"]})
        original_area=float(q[code]["real_original_mainland_region_land_km2"])
        ratio=sum(v["source_grid_mainland_intersection_km2"] for v in sites)/original_area
        if not 1-ORIGINAL_LANDAREA_TOLERANCE_RATIO<=ratio<=1+ORIGINAL_LANDAREA_TOLERANCE_RATIO:
            raise ValueError("STAGE110_ORIGINAL_REGION_POLYGON_AREA_CELLS_NOT_CONSERVED")
        by_region[code]=sites
    if len(all_coords)!=34:
        raise ValueError("STAGE110_NOT_TRUE_34_ERA5_MAINLAND_SOURCE_GRID_CENTRES")
    return by_region,receipt

def true_geodesic_region_area_average(site_results,expected_region_code,original_polygon_area):
    if len(site_results)!=EXPECTED_COUNTS[expected_region_code]:
        raise ValueError("STAGE110_NOT_TRUE_SOURCE_REGION_COMPLETE_GRID")
    km2=sum(r["source_grid_mainland_intersection_km2"] for r in site_results)
    if not (1-ORIGINAL_LANDAREA_TOLERANCE_RATIO<=km2/original_polygon_area<=
            1+ORIGINAL_LANDAREA_TOLERANCE_RATIO):
        raise ValueError("STAGE110_SOURCE_TOTAL_GEO_AREA_NOT_CONSERVED")
    valid=[r for r in site_results if r["original_30y_cell_ERA5_model_daily"]["source_primary_fraction_days_daily_gust_strict_above_15_ms"] is not None]
    valid_area=sum(r["source_grid_mainland_intersection_km2"] for r in valid)
    coverage=valid_area/km2
    if coverage<.95:
        raise ValueError("STAGE110_WARM_CLIMATOLOGICAL_CELL_LAND_COVERAGE_BELOW95PCT")
    def area_mean(key):
        return sum(r["source_grid_mainland_intersection_km2"]*
                   r["original_30y_cell_ERA5_model_daily"][key] for r in valid)/valid_area
    f15=[r["original_30y_cell_ERA5_model_daily"]["source_primary_fraction_days_daily_gust_strict_above_15_ms"] for r in valid]
    ww=[r["source_grid_mainland_intersection_km2"] for r in valid]
    mean=area_mean("source_primary_fraction_days_daily_gust_strict_above_15_ms")
    sd=math.sqrt(sum(w*(v-mean)**2 for w,v in zip(ww,f15))/sum(ww))
    return {"original_mainland_TDWG_code":expected_region_code,
      "original_source_model_land_intersected_km2":km2,
      "original_source_mainland_polygon_area_km2":original_polygon_area,
      "source_original_025_model_land_cells":len(site_results),
      "source_original_effective_land_grid_cells":sum(ww)**2/sum(w*w for w in ww),
      "source_30year_T_GT5C_eligible_land_area_fraction":coverage,
      "source_1991_2020_ERA5model_daily_gust_gt15_area_weighted_fraction":mean,
      "source_1991_2020_ERA5model_daily_gust_gt10_area_weighted_fraction":
           area_mean("source_fraction_gust_greater_than_10_ms"),
      "source_1991_2020_ERA5model_daily_gust_gt20_area_weighted_fraction":
           area_mean("source_fraction_gust_greater_than_20_ms"),
      "source_between_original_025_landcells_gust_gt15_fraction_min":min(f15),
      "source_between_original_025_landcells_gust_gt15_fraction_max":max(f15),
      "source_within_region_land_area_weighted_cell_sd_gust_gt15_fraction":sd,
      "source_uncertainty_from_model_not_station_crossvalidation":True,
      "source_external_ERA5_model_daily_not_original_CDS_hourly_10fg":True}

def run(geo,outdir,prior_artifact=None):
    groups,geo_meta=frozen_original_mainland_cell_sets(geo)
    outdir.mkdir(parents=True,exist_ok=True)
    prior=original_verified_partial_DEL15(prior_artifact,groups) if prior_artifact is not None else {}
    derived={}
    requests=[]
    total_group=0
    reused_cells=0
    for code in SOURCE_REGIONS:
        sites=groups[code]
        finished=[]
        for start in range(0,len(sites),REQUEST_GROUP_MAX):
            if total_group in prior:
                cached=prior[total_group]
                finished.extend(cached["sites"])
                requests.extend(cached["requests"])
                reused_cells+=len(cached["sites"])
                print("STAGE110_REUSED_IMMUTABLE_VERIFIED_30YEAR_DEL_SOURCE_GROUP",{
                  "group":total_group,"count":len(cached["sites"]),
                  "original_zip_SHA256":PRIOR_STAGE110_15DEL_SOURCE_SHA256},flush=True)
                total_group+=1
                continue
            if total_group:
                print("STAGE110_SOURCE_PROVIDER_FIVE_SITE_GROUP_PACE",
                      {"sleep_seconds":SECONDS_BETWEEN_GROUPS,
                       "previous_groups":total_group},flush=True)
                time.sleep(SECONDS_BETWEEN_GROUPS)
            group=sites[start:start+REQUEST_GROUP_MAX]
            original_daily={j:[] for j in range(len(group))}
            original_cells_over_decades={}
            for decade_idx,(y1,y2) in enumerate(YEARS):
                if decade_idx:time.sleep(SECONDS_BETWEEN_DECADES)
                url=api_url(group,f"{y1}-01-01",f"{y2}-12-31")
                payload,digest,bytesize=source_decade_with_bounded_provider_retries(url)
                payload=normalize_source_era5_response(payload,len(group))
                receipt={"TDWG_L3":code,"source_group":total_group,
                         "source_decade":f"{y1}-{y2}",
                         "original_ERA5_daily_model_API_URL":url,
                         "original_unmodified_public_source_JSON_SHA256":digest,
                         "original_source_response_bytes":bytesize,
                         "source_variable_model":"ERA5",
                         "source_years_not_floral_hypothesis_selected":True}
                for j,(g,p) in enumerate(zip(group,payload)):
                    coord=accepted_grid_coordinates(g,p)
                    c=(round(coord["latitude"],6),round(coord["longitude"],6))
                    if j in original_cells_over_decades and original_cells_over_decades[j]!=c:
                        raise ValueError("STAGE110_SOURCE_MODEL_GRID_CELL_CHANGED_OVER_DECADES")
                    original_cells_over_decades[j]=c
                    original_daily[j].extend(parse_decade(p,y1,y2))
                requests.append(receipt)
            for j,g in enumerate(group):
                climate=climatology(original_daily[j])
                if climate["source_ERA5_observed_30yr_days"]!=10958:
                    raise ValueError("STAGE110_SOURCE_1991_2020_DAILY_INCOMPLETE")
                finished.append({**g,"original_model_returned_grid_latlon":
                    list(original_cells_over_decades[j]),
                    "original_30y_cell_ERA5_model_daily":climate})
            # Preserve only derived 30y per-cell quantities, not raw copied daily
            # service JSON; if later 429 fails the completed source groups remain
            # visibly PARTIAL and never misreported as a 34-cell full result.
            group_receipt={
                 "source_status":"PARTIAL_REGION_GROUP_NOT_ALL_34_SOURCE_CELLS",
                 "original_region":code,"source_group_index":total_group,
                 "original_cellcount_in_group":len(group),
                 "source_original_1991_2020_cell_climatologies":
                     finished[-len(group):],
                 "original_API_request_SHAs_last_group":requests[-3:],
                 "never_claim_full_region_if_remaining_groups_fail":True}
            (outdir/f"stage110_partial_source_{code}_group_{total_group:02d}_NOT_full_region.json").write_text(
                 json.dumps(group_receipt,indent=2,sort_keys=True)+"\n")
            total_group+=1
            print("STAGE110_REAL_PUBLIC_ERA5_MODEL_COMPLETED_5CELL_GROUP",
              {"region":code,"original_completed_cells":len(finished),
               "region_source_total_cells":len(sites),
               "original_decade_receipts":len(requests)},flush=True)
        if len(finished)!=len(sites):
            raise ValueError("STAGE110_REGION_SOURCE_GRID_GROUP_INCOMPLETE")
        entry=next(r for r in geo_meta["source_three_geometry_only_preflight_regions"] if r["TDWG_L3"]==code)
        regional=true_geodesic_region_area_average(
            finished,code,float(entry["real_original_mainland_region_land_km2"]))
        derived[code]={"original_cell_climates":finished,"regional_ERA5model_climate":regional}
    if (len(requests),total_group)!=(24,8):
        raise ValueError("STAGE110_NOT_ALL_ORIGINAL_34_PUBLIC_ERA5_MODEL_GRIDCELL_DECADES")
    result={
        "schema":"stage110_genuine_1991_2020_public_ERA5model_DEL_CAB_gridded_mainland_wind_area",
        "original_source_Stage106_geographic_ZIP_SHA256":SOURCE_STAGE106_GEO_SHA,
        "original_ERA5_grid_model_daily_API":"Open-Meteo historical model=era5",
        "source_no_CDS_token_required":True,
        "source_NO_original_ECMWF_CDS_hourly_10fg_file_has_been_used":True,
        "source_BOTH_original_mainland_geographies_not_flower_selected":True,
        "source_original_two_regions":list(SOURCE_REGIONS),
        "source_original_site_counts":{"DEL":16,"CAB":18},
        "source_1991_2020_full_calendar_days_per_source_cell":10958,
        "source_prior_original_15_DEL_cells_derived_SHA_verified":reused_cells==15,
        "source_prior_original_15_DEL_cells_SHA256":PRIOR_STAGE110_15DEL_SOURCE_SHA256 if prior else None,
        "original_source_public_daily_JSON_SHA256_ledger":requests,
        "source_real_geodesic_weighted_region_results":{k:v["regional_ERA5model_climate"] for k,v in derived.items()},
        "source_original_34_cell_30year_ERA5model_derived_climates":{k:v["original_cell_climates"] for k,v in derived.items()},
        "source_137_plus_flora_taxa_or_37_holdout_source_outcomes_NOT_read":True,
        "source_not_125_region_global_climate_analysis":True,
        "no_adaptive_wind_flower_ecological_coefficient_estimated":True}
    (outdir/"stage110_REAL_DEL_CAB_34grid_landarea_1991_2020_ERA5model_daily_gust.json").write_text(
        json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("STAGE110_REAL_NO_CDS_TWO_MAINLAND_REGION_ERA5_MODEL_30YR_GUST",
        json.dumps(result["source_real_geodesic_weighted_region_results"],sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-original-Stage106-mainland-geogrid-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--original-verified-partial-15-DEL-source-ZIP",type=Path)
    a=p.parse_args()
    run(a.source_original_Stage106_mainland_geogrid_ZIP,a.outdir,
        a.original_verified_partial_15_DEL_source_ZIP)
