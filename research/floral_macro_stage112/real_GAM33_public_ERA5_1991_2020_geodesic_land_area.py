#!/usr/bin/env python3
"""Stage112: real 1991–2020 daily ERA5 MODEL wind at 33 original GAM land cells.

GAM was chosen by untouched original source mainland geography in Stage111,
not by source weather, original floral/NHM/WFO/AusTraits or Bombus outcomes.
Source-original two-decimal map is NOT borrowed from one point; every 0.25°
source grid cell intersecting true mainland is weighted by original geodesic
land-intersected km² from SHA-verified Stage111 NaturalEarth×TDWG3 polygons.

Open-Meteo archive, explicit models=era5 / elevation=nan / nearest original
model grid cell / timezone GMT / gust daily max m/s and daily mean 2m T °C,
three disjoint 1991–2000, 2001–2010, 2011–2020 original periods. This is a
model-provider-derived daily ERA5 reanalysis source, NOT original ECMWF CDS
hourly 10fg byte comparison and not observed wind at flowers.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,re,sys,time,zipfile
from pathlib import Path
import numpy as np

BASE=Path(__file__).resolve().parents[1]
for folder in ("floral_macro_stage95","floral_macro_stage109","floral_macro_stage110"):
    sys.path.insert(0,str(BASE/folder))
from original_ERA5_1991_2020_gust_five_mainland_pilot import (
    api_url,parse_decade,climatology,YEARS)
from original_geogrid_public_ERA5_1991_2020_WDC_area_gust import (
    sha256,accepted_grid_coordinates,source_decade_with_bounded_provider_retries)
from original_public_ERA5_model_34cells_DEL_CAB_landarea import (
    normalize_source_era5_response)

SOURCE_STAGE111_ORIGINAL_SHA="c8368faae9b4d2f2e3fe8cc6b307626ab20aa69a99b35d1069ec8c033c9ecf8b"
SOURCE_STAGE111_CELLS="stage111_original_3_new_geoblocks_true_ERA5_025_land_area_cells_NO_climate.csv"
SOURCE_STAGE111_RECEIPT="stage111_original72_source_025_ERA5_grid_budget_receipt_NO_floral_model.json"
SOURCE_CODE="GAM"
FROZEN_SOURCE_CELLCOUNT=33
GROUP_SIZE=5
GROUP_SPACING_SECONDS=68
DECADE_SPACING_SECONDS=12
SOURCE_CORRECTED_MODEL="open-meteo_historical_ERA5_model_daily_derived_NOT_ECMWF_CDS_hourly_10fg"
SOURCE_PRIOR30_COMPLETED_ARTIFACT_SHA="a53db9024a6c3cc35265648cf197281c073f61ff834e68fe9245ce2e7cc61c4a"

def source_verified_prior30_GAM_full_decades(original_prior_source_zip,sites):
    """Restore SIX true completed 5-cell groups, original source SHA + no weather gaps."""
    if sha256(original_prior_source_zip)!=SOURCE_PRIOR30_COMPLETED_ARTIFACT_SHA:
        raise ValueError("STAGE112_PRIOR30_SOURCE_ARTIFACT_SHA_DRIFT")
    groups={}
    with zipfile.ZipFile(original_prior_source_zip) as z:
        if len(z.namelist())!=6:
            raise ValueError("STAGE112_PRIOR30_NOT_EXACT_SIX_SOURCE_GROUPS")
        for i in range(6):
            filename=f"stage112_PARTIAL_source_GAM_group_{i:02d}_NOT_FULL_REGION.json"
            if filename not in z.namelist():
                raise ValueError("STAGE112_PRIOR30_MISSING_SOURCE_GROUP")
            q=json.loads(z.read(filename))
            if (q["source_status"]!="PARTIAL_GROUP_NOT_COMPLETE_GAM33" or
                q["original_frozen_source_stage111_SHA256"]!=SOURCE_STAGE111_ORIGINAL_SHA or
                q["source_group_number"]!=i or
                q["no_complete_region_or_floral_claim_from_partial"] is not True):
                raise ValueError("STAGE112_PRIOR30_GROUP_SOURCE_PROVENANCE_DRIFT")
            original_group=sites[i*GROUP_SIZE:(i+1)*GROUP_SIZE]
            cells=q["source_group_cells"]
            requests=q["source_raw_decade_SHA256_receipts"]
            if len(original_group)!=5 or len(cells)!=5 or len(requests)!=3:
                raise ValueError("STAGE112_PRIOR30_SOURCE_GROUP_SIZE_OR_DECADE_COUNT_CHANGED")
            for requested,actual in zip(original_group,cells):
                if (requested["TDWG_L3"]!=actual["TDWG_L3"] or
                    (requested["lat"],requested["lon"])!=(actual["lat"],actual["lon"]) or
                    requested["source_original_TDWG_polygon_SHA256"]!=actual["source_original_TDWG_polygon_SHA256"] or
                    abs(requested["source_mainland_cell_land_area_km2"]-
                        actual["source_mainland_cell_land_area_km2"])>1e-8 or
                    actual["original_1991_2020_cell_model_ERA5_climatology"]["source_ERA5_observed_30yr_days"]!=10958):
                    raise ValueError("STAGE112_PRIOR30_SOURCE_GEO_OR_30YR_CLIMATE_DRIFT")
                coords=actual["source_returned_model_latlon"]
                accepted_grid_coordinates(requested,
                    {"latitude":coords[0],"longitude":coords[1]})
            for qrequest,(y1,y2) in zip(requests,YEARS):
                if (qrequest["TDWG_L3"]!=SOURCE_CODE or
                    qrequest["original_source_group"]!=i or
                    qrequest["source_years"]!=f"{y1}-{y2}" or
                    qrequest["original_public_historical_ERA5_model_daily_URL"]!=api_url(
                        original_group,f"{y1}-01-01",f"{y2}-12-31") or
                    not re.fullmatch(r"[a-f0-9]{64}",qrequest["source_original_JSON_SHA256"]) or
                    qrequest["original_public_source_bytes"]<10000 or
                    qrequest["source_model"]!="ERA5"):
                    raise ValueError("STAGE112_PRIOR30_ORIGINAL_ERA5_MODEL_SHA_REQUEST_DRIFT")
            groups[i]={"cells":cells,"requests":requests}
    if sum(len(g["cells"]) for g in groups.values())!=30:
        raise ValueError("STAGE112_PRIOR30_NOT_ALL30_REAL_SOURCE_CELLS")
    return groups

def original_source_GAM_cells(stage111):
    if sha256(stage111)!=SOURCE_STAGE111_ORIGINAL_SHA:
        raise ValueError("STAGE112_ORIGINAL_STAGE111_SOURCE_GEOGRAPHY_SHA_DRIFT")
    with zipfile.ZipFile(stage111) as z:
        if not {SOURCE_STAGE111_CELLS,SOURCE_STAGE111_RECEIPT}<=set(z.namelist()):
            raise ValueError("STAGE112_ORIGINAL_LAND_GRID_SOURCE_MEMBER_MISSING")
        original=list(csv.DictReader(io.StringIO(z.read(SOURCE_STAGE111_CELLS).decode("utf-8-sig"))))
        receipt=json.loads(z.read(SOURCE_STAGE111_RECEIPT))
    if (receipt["source_eligible_smallest_geography_only_3_new_region_codes"]!=["GAM","KRY","BGM"] or
        receipt["source_original_72_exploration_regions"]!=72 or
        receipt["source_original_37_holdout_unchanged_and_unopened"]!=37 or
        receipt["source_no_weather_requests_submitted"] is not True or
        receipt["source_no_WFO_NHM_AusTraits_Bombus_outcomes_read"] is not True):
        raise ValueError("STAGE112_STAGE111_OUTCOME_BLIND_SOURCE_SELECTION_CHANGED")
    selected=[r for r in original if r["TDWG_L3"]==SOURCE_CODE]
    other=[r for r in original if r["TDWG_L3"]!=SOURCE_CODE]
    if len(selected)!=FROZEN_SOURCE_CELLCOUNT or len(other)!=174:
        raise ValueError("STAGE112_NOT_ORIGINAL_SOURCE_GAM33_GRID")
    area_record=next(r for r in receipt["source_3_new_exact_mainland_geodesic_cell_regions"]
                     if r["TDWG_L3"]==SOURCE_CODE)
    if (area_record["source_true_intersected_025_ERA5_gridcells"]!=FROZEN_SOURCE_CELLCOUNT
        or area_record["no_1991_2020_climate_retrieved_for_new_region"] is not True):
        raise ValueError("STAGE112_GAM_TRUE_SOURCE_MAINLAND_AREA_RECEIPT_CHANGED")
    sites=[];seen=set()
    for r in selected:
        lat=float(r["ERA5_source_025_grid_latitude"])
        lon=float(r["ERA5_source_025_grid_longitude"])
        km2=float(r["source_original_geodesic_mainland_area_km2"])
        p=(lat,lon)
        if (p in seen or not (-90<=lat<=90 and -180<=lon<=180)
            or abs(lat*4-round(lat*4))>1e-6 or abs(lon*4-round(lon*4))>1e-6
            or not math.isfinite(km2) or km2<=0):
            raise ValueError("STAGE112_ORIGINAL_025_GAM_CELL_OR_LANDWEIGHT_INVALID")
        seen.add(p)
        sites.append({"TDWG_L3":SOURCE_CODE,"lat":lat,"lon":lon,
              "source_mainland_cell_land_area_km2":km2,
              "source_original_TDWG_polygon_SHA256":r["source_original_TDWG_polygon_SHA256"]})
    sites.sort(key=lambda v:(v["lat"],v["lon"]))
    real=float(area_record["source_actual_polygon_mainland_land_area_km2"])
    land_sum=sum(s["source_mainland_cell_land_area_km2"] for s in sites)
    if not (.985<land_sum/real<1.015):
        raise ValueError("STAGE112_GAM_ORIGINAL_LAND_AREA_WEIGHT_CONSERVATION_MISSING")
    if not 9500<real<9700:
        raise ValueError("STAGE112_ORIGINAL_GAM_GEOGRAPHY_LAND_AREA_MISMATCH")
    return sites,area_record

def true_source_region_GAM_area_mean(reports,regional_source):
    if len(reports)!=FROZEN_SOURCE_CELLCOUNT:
        raise ValueError("STAGE112_GAM_NOT_ALL_33_SOURCE_LAND_CELLS")
    weights=np.asarray([x["source_mainland_cell_land_area_km2"] for x in reports],float)
    if not np.all(np.isfinite(weights)) or np.any(weights<=0):
        raise ValueError("STAGE112_GAM_SOURCE_KM2_NOT_POSITIVE")
    area=float(weights.sum())
    true=float(regional_source["source_actual_polygon_mainland_land_area_km2"])
    if not .985<=area/true<=1.015:
        raise ValueError("STAGE112_33_CELL_AREA_SUM_NOT_ORIGINAL_GEOGRAPHY")
    fractions=[r["original_1991_2020_cell_model_ERA5_climatology"][
                   "source_primary_fraction_days_daily_gust_strict_above_15_ms"] for r in reports]
    valid=np.asarray([x is not None for x in fractions])
    coverage=float(weights[valid].sum()/area)
    if coverage<.95:
        raise ValueError("STAGE112_WARM_CLIMATE_MODEL_SOURCE_CELLS_BELOW95PCT_LAND_AREA")
    def average(name):
        vals=np.asarray([r["original_1991_2020_cell_model_ERA5_climatology"][name]
                         for r in reports if r["original_1991_2020_cell_model_ERA5_climatology"][
                            "source_primary_fraction_days_daily_gust_strict_above_15_ms"] is not None],float)
        return float(np.average(vals,weights=weights[valid]))
    f15=np.asarray([x for x in fractions if x is not None],float)
    mean=average("source_primary_fraction_days_daily_gust_strict_above_15_ms")
    var=float(np.average((f15-mean)**2,weights=weights[valid]))
    neff=float(weights[valid].sum()**2/(weights[valid]**2).sum())
    return {
        "TDWG_L3":SOURCE_CODE,
        "source_original_mainland_area_km2":true,
        "source_actual_source_025_land_grid_areas_sum_km2":area,
        "source_1991_2020_complete_original_daily_days_per_025_grid_cell":10958,
        "source_original_region_ERA5_model_land_cells":len(reports),
        "source_effective_025_land_grid_cells":neff,
        "source_1991_2020_Tclim_GT5C_warm_month_land_fraction":coverage,
        "source_1991_2020_daily_10m_gust_gt15_source_geodesic_area_weighted":mean,
        "source_1991_2020_daily_10m_gust_gt10_source_geodesic_area_weighted":
            average("source_fraction_gust_greater_than_10_ms"),
        "source_1991_2020_daily_10m_gust_gt20_source_geodesic_area_weighted":
            average("source_fraction_gust_greater_than_20_ms"),
        "source_original_025_cell_GUST_gt15_min":float(np.min(f15)),
        "source_original_025_cell_GUST_gt15_max":float(np.max(f15)),
        "source_original_025_cell_GUST_gt15_area_weighted_sd":math.sqrt(var),
        "source_true_land_area_weights_not_equal_cell_average":True,
        "source_public_ERA5model_daily_NOT_original_CDS_hourly_10fg":True,
        "no_flower_pollinator_sensory_signal_effect_estimated":True}

def run(original_stage111_zip,outdir,prior_verified30=None):
    sites,region_area=original_source_GAM_cells(original_stage111_zip)
    cached=source_verified_prior30_GAM_full_decades(prior_verified30,sites) if prior_verified30 is not None else {}
    outdir.mkdir(parents=True,exist_ok=True)
    finish=[]
    receipt=[]
    reused_source_cells=0
    for start in range(0,len(sites),GROUP_SIZE):
        group=sites[start:start+GROUP_SIZE]
        batch=start//GROUP_SIZE
        if batch in cached:
            finish.extend(cached[batch]["cells"])
            receipt.extend(cached[batch]["requests"])
            reused_source_cells+=len(cached[batch]["cells"])
            print("STAGE112_REUSED_SOURCE_VERIFIED_ORIGINAL_30YR_GAM_GROUP",
                  {"group":batch,"cached_cells":len(cached[batch]["cells"]),
                   "original_source_artifact_SHA256":SOURCE_PRIOR30_COMPLETED_ARTIFACT_SHA},flush=True)
            continue
        if start:
            print("STAGE112_PUBLIC_SOURCE_ERA5_PROVIDER_GROUP_SPACING",GROUP_SPACING_SECONDS,flush=True)
            time.sleep(GROUP_SPACING_SECONDS)
        collect={i:[] for i in range(len(group))}
        coords={}
        for decade,(y1,y2) in enumerate(YEARS):
            if decade:time.sleep(DECADE_SPACING_SECONDS)
            url=api_url(group,f"{y1}-01-01",f"{y2}-12-31")
            raw,digest,n=source_decade_with_bounded_provider_retries(url)
            frames=normalize_source_era5_response(raw,len(group))
            if len(frames)!=len(group):
                raise ValueError("STAGE112_REAL_SOURCE_GAM_GROUP_CARDINALITY_CHANGED")
            row={
              "TDWG_L3":SOURCE_CODE,"original_source_group":start//GROUP_SIZE,
              "source_years":f"{y1}-{y2}",
              "original_public_historical_ERA5_model_daily_URL":url,
              "source_original_JSON_SHA256":digest,
              "original_public_source_bytes":n,
              "source_model":"ERA5",
              "source_one_source_025_grid_not_downscaled":True}
            for i,(site,frame) in enumerate(zip(group,frames)):
                coord=accepted_grid_coordinates(site,frame)
                this=(round(coord["latitude"],6),round(coord["longitude"],6))
                if i in coords and coords[i]!=this:
                    raise ValueError("STAGE112_PUBLIC_ERA5_GRID_CENTRE_CHANGED_BETWEEN_DECADES")
                coords[i]=this
                collect[i].extend(parse_decade(frame,y1,y2))
            receipt.append(row)
        completed=[]
        for i,site in enumerate(group):
            clim=climatology(collect[i])
            if clim["source_ERA5_observed_30yr_days"]!=10958:
                raise ValueError("STAGE112_REAL_30YR_DAILY_MODEL_CELL_INCOMPLETE")
            completed.append({**site,
               "source_returned_model_latlon":list(coords[i]),
               "original_1991_2020_cell_model_ERA5_climatology":clim})
        finish.extend(completed)
        # Always preserve verified full 30yr data for each 5-cell group,
        # even if later provider transport/quota requests are rejected.
        # Partial source groups are NEVER silently reported as full region.
        (outdir/f"stage112_PARTIAL_source_GAM_group_{start//GROUP_SIZE:02d}_NOT_FULL_REGION.json").write_text(
            json.dumps({"source_status":"PARTIAL_GROUP_NOT_COMPLETE_GAM33",
              "original_frozen_source_stage111_SHA256":SOURCE_STAGE111_ORIGINAL_SHA,
              "source_group_number":start//GROUP_SIZE,
              "source_group_cells":completed,
              "source_raw_decade_SHA256_receipts":receipt[-3:],
              "no_complete_region_or_floral_claim_from_partial":True},
              sort_keys=True,indent=2)+"\n")
        print("STAGE112_GAM_REAL_30YR_MODEL_SOURCE_LANDCELLS_COMPLETED",{
            "complete_climate_cells":len(finish),"source_required_cells":33,
            "original_raw_source_requests":len(receipt)},flush=True)
    if len(finish)!=33 or len(receipt)!=21:
        raise ValueError("STAGE112_REAL_33_CELL_21_HISTORICAL_ERA5_SOURCE_REQUESTS_NOT_COMPLETE")
    region=true_source_region_GAM_area_mean(finish,region_area)
    result={
      "schema":"stage112_real_original_GAM33_grid_public_ERA5_daily_1991_2020_landarea_model",
      "source_original_Stage111_geo_artifact_SHA256":SOURCE_STAGE111_ORIGINAL_SHA,
      "source_original_TDWG3_region":SOURCE_CODE,
      "source_original_ERA5_grid_size_degrees":0.25,
      "source_PRIOR30_verified_completed_climate_cells_reused":reused_source_cells,
      "source_PRIOR30_original_partial_artifact_SHA256":SOURCE_PRIOR30_COMPLETED_ARTIFACT_SHA if cached else None,
      "source_genuine_original_1991_2020_30_year_full_dates":10958,
      "original_source_API_raw_decade_JSON_SHA256_ledger":receipt,
      "source_actual_33_land_cells_with_30year_weather":finish,
      "source_original_GAM_geodesic_landarea_ERA5_model_30yr_gust":region,
      "source_no_CDS_authentication_needed":True,
      "source_provider_model_daily_archive_not_original_ECMWF_CDS_10fg":True,
      "source_new_original_geographic_block_05_03_first_example":True,
      "source_hypothesis_independent_selection_before_model_weather":True,
      "source_37_original_holdout_NHM_WFO_AusTraits_Bombus_NOT_read":True,
      "source_not_all72_original_mainland_ERA5_fully_obtained":True,
      "no_causal_sensory_order_learning_or_wind_flower_effect_claimed":True}
    (outdir/"stage112_REAL_GAM33grid_1991_2020_ERA5_model_025_land_area_daily_gust.json").write_text(
        json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("STAGE112_REAL_NEW_MAINLAND_GEO_BLOCK_GAM33_1991_2020_ERA5_MODEL_WIND",
       json.dumps(region,sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage111-geographic-grid-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--source-original-Stage112-prior30-verified-ZIP",type=Path)
    a=p.parse_args()
    run(a.original_Stage111_geographic_grid_ZIP,a.outdir,
        a.source_original_Stage112_prior30_verified_ZIP)
