#!/usr/bin/env python3
"""Stage95B independent cold-continental-season implementation check.

Spatial source-only select three northernmost eligible Mainland EXPLORATION
TDWG3 regional representative sites from three distinct frozen Stage94 geo
blocks. Uses exactly the same original 1991-2020 daily ERA5-model source, >5 C
climatological warm month filter and >15m/s daily max gust as Stage95A.

An *actual* high latitude sample must have fewer than 12 warm months.
This validates real month-exclusion, NOT a full mainland area-weighted wind
exposure or floral cause.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,zipfile
from pathlib import Path
from original_ERA5_1991_2020_gust_five_mainland_pilot import (
    sha256,STAGE94_ARTIFACT_SHA,STAGE94_CSV_MEMBER,
    source_polygons,api_url,query_original,parse_decade,climatology,YEARS,
)

N_COLD_SITES=3
LAT_GATE_DEG=50.0

def cold_mainland_sites(geo_artifact,tdwg_geo):
    if sha256(geo_artifact)!=STAGE94_ARTIFACT_SHA:
        raise ValueError("STAGE95B_GEO_SOURCE_SHA_CHANGED")
    with zipfile.ZipFile(geo_artifact) as z:
        if STAGE94_CSV_MEMBER not in z.namelist():raise ValueError("STAGE95B_NO_REAL_MAINLAND_REGION_FRAME")
        rows=list(csv.DictReader(io.StringIO(z.read(STAGE94_CSV_MEMBER).decode("utf-8-sig"))))
    if len(rows)!=125 or len({x["TDWG_L3"] for x in rows})!=125:
        raise ValueError("STAGE95B_125_SOURCE_REGIONS_CHANGED")
    shapes,invalid,_=source_polygons(tdwg_geo)
    candidates=[]
    for r in rows:
        if r["shared_split"]!="exploration":continue
        code=r["TDWG_L3"]
        g=shapes.get(code)
        if g is None:raise ValueError("STAGE95B_MISSING_ORIGINAL_TDWG_REGION")
        p=g.representative_point()
        if not p.is_valid or not math.isfinite(p.x) or not math.isfinite(p.y):
            raise ValueError("STAGE95B_INVALID_REGION_REP_POINT")
        if p.y>=LAT_GATE_DEG:
            candidates.append((float(p.y),r,p))
    candidates.sort(key=lambda item:(-item[0],item[1]["TDWG_L3"]))
    seen=set();out=[]
    for lat,r,p in candidates:
        block=r["spatial_block_id"]
        if block in seen:continue
        seen.add(block)
        out.append({"TDWG_L3":r["TDWG_L3"],"spatial_block_id":block,
                   "lat":round(float(p.y),5),"lon":round(float(p.x),5),
                   "source_true_TDWG_polygon_sha256":r["polygon_sha256"],
                   "original_TDWG_polygon_repaired":r["TDWG_L3"] in invalid,
                   "chosen_high_latitude_source_only":True})
        if len(out)==N_COLD_SITES:break
    if len(out)<N_COLD_SITES:raise ValueError("STAGE95B_THREE_DISTINCT_NORTHERN_MAINLAND_BLOCKS_UNAVAILABLE")
    return out

def run(source_geography,tdwg,outdir):
    sites=cold_mainland_sites(source_geography,tdwg)
    source_data={r["TDWG_L3"]:[] for r in sites};receipts=[]
    for y1,y2 in YEARS:
        url=api_url(sites,f"{y1}-01-01",f"{y2}-12-31")
        frames,digest,size=query_original(url)
        if not isinstance(frames,list) or len(frames)!=len(sites):
            raise ValueError("STAGE95B_ERA5_MULTISITE_RESPONSE_INCOMPLETE")
        receipts.append({"years":[y1,y2],"api_response_SHA256":digest,"bytes":size,"query":url})
        for r,frame in zip(sites,frames):
            source_data[r["TDWG_L3"]].extend(parse_decade(frame,y1,y2))
    results=[]
    for site in sites:
        v=climatology(source_data[site["TDWG_L3"]])
        if not 0<len(v["source_eligible_climatological_months_T2m_strict_above_5C"])<12:
            raise ValueError("STAGE95B_NORTHERN_SOURCE_SEASON_FILTER_HAS_NO_TRUE_EXCLUDED_MONTH")
        results.append({**site,**v})
    receipt={"schema":"stage95B_TRUE_ORIGINAL_ERA5_model_30yr_cold_mainland_month_exclusion",
       "stage94_geometry_source_SHA256":STAGE94_ARTIFACT_SHA,
       "source_selection_latitude_only_before_climate_or_floral_cues":True,
       "not_ERA5_CDS_original_hourly_10fg":True,
       "not_flowering_biological_species_specific":True,
       "not_full_mainland_spatial_area_weighted":True,
       "strict_temperature_warm_months_threshold_C":5,
       "strict_ERA5_model_daily_max_gust_threshold_ms":15,
       "all_source_30yr_days_complete":True,
       "not_an_ecological_effect_or_causal_choice_model":True,
       "original_api_decade_SHA256":receipts,"source_sites":results}
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"stage95B_real_ERA5_1991_2020_source_cold_month_sanity.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE95B_ACTUAL_COLD_MAINLAND_MONTH_FILTER",json.dumps([
       {"code":r["TDWG_L3"],"lat":r["lat"],
        "eligible_months":r["source_eligible_climatological_months_T2m_strict_above_5C"],
        "eligible_days":r["source_eligible_days"],
        "fraction_gt_15":r["source_primary_fraction_days_daily_gust_strict_above_15_ms"]}
       for r in results],sort_keys=True),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage94-geography-ZIP",type=Path,required=True)
    p.add_argument("--original-TDWG3-geojson",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.original_Stage94_geography_ZIP,a.original_TDWG3_geojson,a.outdir)
