#!/usr/bin/env python3
"""Stage95A authentic 1991-2020 ERA5-model gust *source pilot*, NO floral fit.

Read SHA-verified Stage94 continental exploration blocks, choose first original
TDWG polygon representative point in each of FIVE distinct fixed blocks before
climate/plant outcomes. Fetch 1991-2020 daily ERA5-model 10m gust maximum and
daily mean 2m temperature via the public historical archive (Open-Meteo API,
models=era5). Strict >15 m/s proportion within 30-year climatologically warm
months (long-term month mean 2m T >5 C), with >10 and >20 sensitivity.

The API output is daily derived from ERA5-model data, NOT a byte-verified CDS
ERA5 hourly '10fg' product and NOT a regional 0.25° area-weighted integral.
Source pilot cannot be promoted to primary regional wind effects without that
cross-check and a spatially representative continental land-masked aggregation.
"""
from __future__ import annotations
import argparse,csv,datetime as dt,hashlib,io,json,math,sys,urllib.parse,urllib.request,urllib.error,zipfile
from pathlib import Path
from collections import defaultdict

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage87"))
from aggregate_global_tdwg3_worldclim_wind import source_polygons

STAGE94_ARTIFACT_SHA="3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833"
STAGE94_CSV_MEMBER="stage94_original_mainland_shared_geoblock_split.csv"
API="https://archive-api.open-meteo.com/v1/archive"
YEARS=((1991,2000),(2001,2010),(2011,2020))
PILOT_SITES=5
GUST_THRESHOLDS=(10.0,15.0,20.0)
PRIMARY_THRESHOLD=15.0
WARM_T_THRESHOLD=5.0

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()

def original_pilot_sites(artifact,tdwg_geo):
    if sha256(artifact)!=STAGE94_ARTIFACT_SHA:
        raise ValueError("STAGE95_MISMATCH_ORIGINAL_STAGE94_GEOGRAPHIC_HOLDOUT_SOURCE")
    with zipfile.ZipFile(artifact) as z:
        if STAGE94_CSV_MEMBER not in z.namelist():raise ValueError("STAGE95_NO_VERIFIED_MAINLAND_SPLIT")
        rows=list(csv.DictReader(io.StringIO(z.read(STAGE94_CSV_MEMBER).decode("utf-8-sig"))))
    if len(rows)!=125 or sum(r["shared_split"]=="exploration" for r in rows)!=88:
        raise ValueError("STAGE95_MAINLAND_125_88_SOURCE_SPLIT_CHANGED")
    candidates=sorted((r for r in rows if r["shared_split"]=="exploration"),
                      key=lambda r:(r["spatial_block_id"],r["TDWG_L3"]))
    selected=[];seen=set()
    for r in candidates:
        block=r["spatial_block_id"]
        if block in seen:continue
        seen.add(block);selected.append(r)
        if len(selected)==PILOT_SITES:break
    if len(selected)!=PILOT_SITES:raise ValueError("STAGE95_FIVE_INDEPENDENT_GEOGRAPHIC_BLOCKS_UNAVAILABLE")
    shapes,invalid,_=source_polygons(tdwg_geo)
    out=[]
    for r in selected:
        code=r["TDWG_L3"]
        if code not in shapes:raise ValueError("STAGE95_ACTUAL_SOURCE_TDWG_GEOMETRY_NOT_FOUND")
        point=shapes[code].representative_point()
        if not (-90<float(point.y)<90 and -180<=float(point.x)<=180):
            raise ValueError("STAGE95_TDWG_SOURCE_REP_POINT_OUT_OF_RANGE")
        out.append({"TDWG_L3":code,"spatial_block_id":r["spatial_block_id"],
                    "source_true_original_TDWG_polygon_sha256":r["polygon_sha256"],
                    "lat":round(float(point.y),5),"lon":round(float(point.x),5),
                    "source_original_TDWG_repaired_polygon":bool(code in invalid),
                    "outcome_blind_exploration_only":True})
    return out

def api_url(sites,start,end):
    params={
       "latitude":",".join(str(r["lat"]) for r in sites),
       "longitude":",".join(str(r["lon"]) for r in sites),
       "start_date":start,"end_date":end,
       "daily":"wind_gusts_10m_max,temperature_2m_mean",
       "models":"era5","timezone":"GMT",
       "wind_speed_unit":"ms",
       "elevation":",".join("nan" for _ in sites),
       "cell_selection":"nearest"}
    return API+"?"+urllib.parse.urlencode(params)

def query_original(url):
    if not url.startswith(API+"?"):raise ValueError("STAGE95_NOT_HISTORICAL_API")
    req=urllib.request.Request(url,headers={"Accept":"application/json",
           "User-Agent":"academic-floral-ERA5-1991-2020-climate-pilot/0.1"})
    try:
        with urllib.request.urlopen(req,timeout=180) as res:
            raw=res.read(12000000)
            mime=res.headers.get("Content-Type","")
    except urllib.error.HTTPError as e:
        reason=e.read(1500).decode("utf-8",errors="replace")
        raise ValueError(f"STAGE95_OPENMETEO_ERA5_API_HTTP_{e.code}_{reason[:350]}") from e
    if not raw or len(raw)>=12000000 or "json" not in mime:
        raise ValueError("STAGE95_API_ORIGINAL_JSON_MISSING_OR_TOO_LARGE")
    payload=json.loads(raw)
    if isinstance(payload,dict) and payload.get("error"):
        raise ValueError("STAGE95_API_SOURCE_ERROR_"+str(payload.get("reason","")))
    return payload,hashlib.sha256(raw).hexdigest(),len(raw)

def date_range(start_year,end_year):
    a=dt.date(start_year,1,1);b=dt.date(end_year,12,31)
    return [(a+dt.timedelta(days=i)).isoformat() for i in range((b-a).days+1)]

def parse_decade(frame,start_year,end_year):
    daily=frame.get("daily") or {}
    units=frame.get("daily_units") or {}
    if units.get("wind_gusts_10m_max")!="m/s":
        raise ValueError("STAGE95_ERA5_GUST_NOT_MS")
    if units.get("temperature_2m_mean") not in ("°C","C","Celsius"):
        raise ValueError("STAGE95_ERA5_2M_TEMP_UNIT_WRONG")
    if frame.get("utc_offset_seconds")!=0:
        raise ValueError("STAGE95_ERA5_DAY_NOT_GMT")
    dates=date_range(start_year,end_year)
    if daily.get("time")!=dates:
        raise ValueError("STAGE95_NONCONTIGUOUS_OR_INCOMPLETE_ORIGINAL_DAILY_DATES")
    gust=daily.get("wind_gusts_10m_max")
    temp=daily.get("temperature_2m_mean")
    if not isinstance(gust,list) or not isinstance(temp,list) or len(gust)!=len(dates) or len(temp)!=len(dates):
        raise ValueError("STAGE95_SOURCE_GUST_OR_TEMP_DAILY_ARRAY_MISSING")
    if any(v is None or not isinstance(v,(int,float)) or not math.isfinite(v)
           for v in gust+temp):
        raise ValueError("STAGE95_MISSING_DAILY_WEATHER_NEVER_IMPUTED_ZERO")
    if any(g<0 or g>150 for g in gust):raise ValueError("STAGE95_IMPOSSIBLE_DAILY_GUST_VALUE")
    return list(zip(dates,[float(g) for g in gust],[float(t) for t in temp]))

def climatology(daily):
    if len(daily)!=len(date_range(1991,2020)):
        raise ValueError("STAGE95_NOT_A_COMPLETE_30_YEAR_DAILY_PERIOD")
    if [r[0] for r in daily]!=date_range(1991,2020):
        raise ValueError("STAGE95_DAILY_DATE_GAP_OR_DUPLICATE")
    monthtemps=defaultdict(list)
    for d,g,t in daily:
        monthtemps[int(d[5:7])].append(t)
    if set(monthtemps)!=set(range(1,13)):
        raise ValueError("STAGE95_SOURCE_SEASONAL_CLIMATOLOGY_MONTHS_MISSING")
    means={m:sum(v)/len(v) for m,v in sorted(monthtemps.items())}
    months=[m for m,t in means.items() if t>WARM_T_THRESHOLD]
    eligible=[g for d,g,t in daily if int(d[5:7]) in months]
    if not months or not eligible:
        primary=None
    else:
        primary=sum(g>PRIMARY_THRESHOLD for g in eligible)/len(eligible)
    return {
        "source_ERA5_years":"1991-2020",
        "source_ERA5_observed_30yr_days":len(daily),
        "source_monthly_30yr_mean_T2m_C":{str(k):v for k,v in means.items()},
        "source_eligible_climatological_months_T2m_strict_above_5C":months,
        "source_eligible_days":len(eligible),
        "source_primary_fraction_days_daily_gust_strict_above_15_ms":primary,
        "source_fraction_gust_greater_than_10_ms":sum(g>10 for g in eligible)/len(eligible) if eligible else None,
        "source_fraction_gust_greater_than_20_ms":sum(g>20 for g in eligible)/len(eligible) if eligible else None,
        "source_fraction_gust_greater_OR_EQUAL_15_ms_DIAGNOSTIC_NOT_PRIMARY":sum(g>=15 for g in eligible)/len(eligible) if eligible else None,
        "source_full_period_daily_gust_max_m_s":max(g for _,g,_ in daily),
        "source_daily_NOT_direct_CDS_hourly_10fg":True,
    }

def run(stage94_zip,tdwg,output):
    sites=original_pilot_sites(stage94_zip,tdwg)
    series={r["TDWG_L3"]:[] for r in sites};requests=[]
    for y1,y2 in YEARS:
        url=api_url(sites,f"{y1}-01-01",f"{y2}-12-31")
        frames,digest,n_bytes=query_original(url)
        if not isinstance(frames,list) or len(frames)!=len(sites):
            raise ValueError("STAGE95_MULTI_SITE_ERA5_SOURCE_RECORD_COUNT_WRONG")
        requests.append({"years":f"{y1}-{y2}","url":url,"source_SHA256":digest,"size_bytes":n_bytes})
        for r,frame in zip(sites,frames):
            if not isinstance(frame,dict) or not all(math.isfinite(float(frame[k]))
               for k in ("latitude","longitude")):raise ValueError("STAGE95_MISSING_SOURCE_GRID_COORDS")
            series[r["TDWG_L3"]].extend(parse_decade(frame,y1,y2))
    results=[]
    for site in sites:
        item=climatology(series[site["TDWG_L3"]])
        if item["source_primary_fraction_days_daily_gust_strict_above_15_ms"] is None:
            raise ValueError("STAGE95_PILOT_SITE_NO_CLIMATOLOGICAL_WARM_MONTHS")
        results.append({**site,**item})
    receipt={
       "schema":"stage95A_original_ERA5_model_1991_2020_strong_gust_five_mainland_exploration_sites",
       "original_stage94_mainland_geo_source_SHA256":STAGE94_ARTIFACT_SHA,
       "study_sites_selected_geography_only_from_distinct_mainland_exploration_blocks":True,
       "model":"era5","source_access":"Open-Meteo historical archive daily ERA5 model",
       "source_daily_not_CDS_original_hourly_10fg_independent_validation_pending":True,
       "temperature_climatology_30yr_monthly_mean_strict_above_5_C":True,
       "wind_10m_gust_daily_max_strict_above_15_m_s":True,
       "source_full_30yr_daily_series_complete_by_date":True,
       "no_area_aggregation_or_mainland_wind_signal_coefficients_estimated":True,
       "no_raster_CDS_hourly_gust_original_byte_comparison":True,
       "number_pilot_source_sites":len(sites),
       "original_query_decade_sha256":requests,"sites":results}
    output.mkdir(parents=True,exist_ok=True)
    (output/"stage95A_original_model_ERA5_gust_climatology_5_mainland_sources.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE95A_REAL_1991_2020_ERA5_MODEL_GUST_PILOT",json.dumps({
        "n_sites":len(results),"site_results":[{"region":r["TDWG_L3"],"eligible_days":r["source_eligible_days"],
        "fraction_strict_15m_s":r["source_primary_fraction_days_daily_gust_strict_above_15_ms"]}
        for r in results],"raw_request_sha256":[r["source_SHA256"] for r in requests]},
        sort_keys=True),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage94-geography-ZIP",type=Path,required=True)
    p.add_argument("--original-TDWG3-geojson",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.original_Stage94_geography_ZIP,a.original_TDWG3_geojson,a.outdir)
