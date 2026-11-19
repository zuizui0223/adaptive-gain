#!/usr/bin/env python3
"""Stage95C outcome-blind spatial source expansion: first 25 of 125 mainland TDWG3s.

REAL historical ERA5-model 1991–2020 daily gust & 2m temperature, one actual
original TDWG mainland regional representative point per region, no bloom
observations, bee/cue outcomes or area-weighted polygon integration.
Reads full Stage94 source-signed 125 mainland split; source order and grouping
are frozen before seeing ANY wind values. No ecological regression.
"""
from __future__ import annotations
import argparse,csv,io,json,time,zipfile,math
from collections import Counter
from pathlib import Path
from original_ERA5_1991_2020_gust_five_mainland_pilot import (
    STAGE94_ARTIFACT_SHA,STAGE94_CSV_MEMBER,YEARS,sha256,
    source_polygons,api_url,query_original,parse_decade,climatology)
SITES_PER_REQUEST=5
FIRST_SOURCE_REGIONS=25
# Stage95C first source pilot got provider HTTP429 on request 4, with explicit
# "Minutely API request limit exceeded. Please try again in one minute."
# Each group makes exactly three decade requests; do not request another group
# until the published per-minute quota can reset.
INTER_GROUP_PACE_SEC=70
SOURCE_429_PAUSE_SEC=70

def source_mainland_regions(artifact,geo):
    if sha256(artifact)!=STAGE94_ARTIFACT_SHA:
        raise ValueError("STAGE95C_MAINLAND_SOURCE_ARTIFACT_SHA_CHANGED")
    with zipfile.ZipFile(artifact) as z:
        rows=list(csv.DictReader(io.StringIO(z.read(STAGE94_CSV_MEMBER).decode("utf-8-sig"))))
    if len(rows)!=125 or len({r["TDWG_L3"] for r in rows})!=125:
        raise ValueError("STAGE95C_ORIGINAL_MAINLAND_FRAME_CHANGED")
    folds=Counter(r["shared_split"] for r in rows)
    if folds!={"exploration":88,"holdout":37}:
        raise ValueError("STAGE95C_FIXED_88_37_SPLIT_CHANGED")
    regions,invalid,_=source_polygons(geo)
    sites=[]
    for row in sorted(rows,key=lambda r:r["TDWG_L3"]):
        code=row["TDWG_L3"]; p=regions[code].representative_point()
        if not -90<p.y<90 or not -180<=p.x<=180 or not p.is_valid:
            raise ValueError("STAGE95C_ORIGINAL_TDWG_REP_COORD_INVALID_"+code)
        sites.append({"TDWG_L3":code,"shared_split":row["shared_split"],
            "spatial_block_id":row["spatial_block_id"],
            "lat":round(float(p.y),5),"lon":round(float(p.x),5),
            "TDWG_source_polygon_SHA256":row["polygon_sha256"],
            "original_TDWG_source_polygon_repaired":code in invalid,
            "regional_strict_continent_connected_scope":"mainland"})
    return sites

def run(artifact,tdwg,outdir,max_sites=FIRST_SOURCE_REGIONS):
    # Validate arguments BEFORE accessing any archived source files.
    if not 1<=max_sites<=125 or max_sites%SITES_PER_REQUEST:
        raise ValueError("STAGE95C_MAX_SITES_MUST_BE_POSITIVE_MULTIPLE_OF_FIVE")
    allsites=source_mainland_regions(artifact,tdwg)
    if max_sites>len(allsites):
        raise ValueError("STAGE95C_MAX_SITES_EXCEEDS_ORIGINAL_MAINLAND_REGIONS")
    # The selection is by original TDWG code only, never climate, trait, or
    # pollinator outcome. The remaining original mainland frame is preserved.
    chosen=allsites[:max_sites]
    receipts=[];regional=[];quota_pause_events=[]
    for j in range(0,len(chosen),SITES_PER_REQUEST):
        if j:
            print("STAGE95C_SOURCE_QUOTA_PACE_SECS",INTER_GROUP_PACE_SEC,
                  "before_next_five_source_sites",flush=True)
            time.sleep(INTER_GROUP_PACE_SEC)
        sites=chosen[j:j+SITES_PER_REQUEST]
        series={s["TDWG_L3"]:[] for s in sites}
        for a,b in YEARS:
            url=api_url(sites,f"{a}-01-01",f"{b}-12-31")
            try:
                result,digest,n=query_original(url)
            except ValueError as exc:
                # Bounded, visible, provider-grounded 429 recovery ONLY.
                # A second 429 is a hard failure and stops all source claims.
                if "STAGE95_OPENMETEO_ERA5_API_HTTP_429_" not in str(exc):
                    raise
                print("STAGE95C_PROVIDER_HTTP_429_QUOTA",str(exc)[:240],
                      "waiting_seconds",SOURCE_429_PAUSE_SEC,flush=True)
                quota_pause_events.append({"batch":j//SITES_PER_REQUEST,
                                           "decade":[a,b],
                                           "pause_seconds":SOURCE_429_PAUSE_SEC})
                time.sleep(SOURCE_429_PAUSE_SEC)
                result,digest,n=query_original(url)
            if not isinstance(result,list) or len(result)!=len(sites):
                raise ValueError("STAGE95C_ORIGINAL_ERA5_MULTI_SITE_RESULT_WRONG_LENGTH")
            receipts.append({"batch_id":j//SITES_PER_REQUEST,
                "source_TDWG_codes":[s["TDWG_L3"] for s in sites],
                "source_query_years":f"{a}-{b}","query_sha256":digest,
                "source_JSON_bytes":n,"original_ERA5_query":url})
            for site,frame in zip(sites,result):
                if not (-90<=float(frame["latitude"])<=90 and
                    -180<=float(frame["longitude"])<=180):
                    raise ValueError("STAGE95C_ERA5_SOURCE_GRID_LOCATION_MISSING")
                if (abs(float(frame["latitude"])-site["lat"])>1.0 or
                    abs(float(frame["longitude"])-site["lon"])>1.0):
                    raise ValueError("STAGE95C_ERA5_REANALYSIS_GRID_CELL_MISMATCH")
                series[site["TDWG_L3"]].extend(parse_decade(frame,a,b))
        for site in sites:
            r=climatology(series[site["TDWG_L3"]])
            if r["source_ERA5_observed_30yr_days"]!=10958 or r["source_eligible_days"]==0:
                # A real no-warm-month region is not zero wind: it needs NA.
                if r["source_eligible_days"]==0:r["source_cold_months_eligibility_NA"]=True
            regional.append({**site,**r})
        print("STAGE95C_TRUE_ORIGINAL_ERA5_REGION_BATCH",
              json.dumps({"batch":j//SITES_PER_REQUEST,"sites":[r["TDWG_L3"] for r in sites],
                  "completed":len(regional),"total_expected":max_sites},sort_keys=True),flush=True)
    counts=Counter(r["shared_split"] for r in regional)
    wind=[r["source_primary_fraction_days_daily_gust_strict_above_15_ms"]
          for r in regional if r["source_primary_fraction_days_daily_gust_strict_above_15_ms"] is not None]
    summary={
       "schema":"stage95C_real_ERA5_model_30yr_first25_mainland_source_grid_points_not_regional_exposure",
       "signed_original_stage94_geo_artifact_sha256":STAGE94_ARTIFACT_SHA,
       "original_mainland_regions_preoutcome":125,
       "source_exploration_regions":88,"source_holdout_regions":37,
       "source_region_selection":"lexical_original_TDWG_region_key_first25",
       "source_requested_region_count":max_sites,
       "source_completed_region_count":len(regional),
       "source_selected_folds":dict(counts),
       "source_regions_not_yet_downloaded":125-max_sites,
       "original_api_requests_count":len(receipts),
       "source_provider_explicit_minutely_quota_429_recoveries":quota_pause_events,
       "source_pace_seconds_between_groups":INTER_GROUP_PACE_SEC,
       "real_ERA5_model_requested_30yr_days_per_site":10958,
       "regional_gust_source_site_fraction_min":min(wind) if wind else None,
       "regional_gust_source_site_fraction_max":max(wind) if wind else None,
       "source_queries_with_SHA256":receipts,
       "sites":regional,
       "no_source_regional_area_weighting":True,
       "no_CDS_ERA5_hourly_10fg_independent_crosscheck":True,
       "no_wind_to_signal_or_pollinator_ecological_regression":True,
       "no_holdout_cue_outcomes_seen":True}
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"stage95C_true_source_first25_mainland_site_gust_30yr.json").write_text(
       json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE95C_25_REAL_ERA5_MODEL_REGIONAL_SAMPLING_SOURCE",
          json.dumps({"completed":len(regional),"full_mainland":125,
          "strict15_fraction_range":[summary["regional_gust_source_site_fraction_min"],
                                    summary["regional_gust_source_site_fraction_max"]],
          "folds":dict(counts),"request_sha_count":len(receipts)},sort_keys=True),flush=True)
    return summary

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-stage94-geography-zip",type=Path,required=True)
    p.add_argument("--original-TDWG3-geojson",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--limit-region-count",type=int,default=FIRST_SOURCE_REGIONS)
    args=p.parse_args();run(args.original_stage94_geography_zip,args.original_TDWG3_geojson,
                            args.outdir,args.limit_region_count)
