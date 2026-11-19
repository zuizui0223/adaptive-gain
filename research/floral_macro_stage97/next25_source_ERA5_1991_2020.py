#!/usr/bin/env python3
"""Stage97 original ERA5-model daily gust 1991–2020: second 25 mainland regions.

Source-only extension of successful Stage95C: exactly the next 25 TDWG3 codes
(0-based rank positions 25:50) from the same original, outcome-blind sorted
125-region mainland geometry. Verify prior independently SHA-pinned first-25
result, with zero region overlap; preserve original 88/37 partition.

NOT source CDS raw hourly ERA5 10fg and NOT area-weighted regional wind.
NO floral signal/cognition/landing/fitness or ecological regression fit.
"""
from __future__ import annotations
import argparse,datetime,hashlib,io,json,time,zipfile,sys,ssl,urllib.error
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage95"))
from original_ERA5_1991_2020_regional_25point_source_probe import (
    source_mainland_regions, SITES_PER_REQUEST
)
# Stage96 branch did not inherit later Stage95C quota-pacing amendments.
# Freeze the source-provider's previously observed quota recovery locally;
# do NOT depend on whichever stacked Stage95 file version happens to exist.
INTER_GROUP_PACE_SEC=70
SOURCE_429_PAUSE_SEC=70
from original_ERA5_1991_2020_gust_five_mainland_pilot import (
    api_url,query_original,parse_decade,climatology,YEARS,sha256
)

FIRST25_SHA="7c98421306466b589b1f80ec97d4ca32ba58e73ba7807f0c2330a7f082fe6b67"
FIRST25_MEMBER="stage95C_true_source_first25_mainland_site_gust_30yr.json"
START=25
COUNT=25
TLS_TRANSIENT_RETRY_DELAYS_SEC=(20,60)

def original_source_with_bounded_transient_retries(url):
    """Retry *connection* transport failures, never changed scientific data.

    HTTP source/provider errors are handled separately, not swallowed.
    """
    for attempt in range(len(TLS_TRANSIENT_RETRY_DELAYS_SEC)+1):
        try:
            return query_original(url)
        except (urllib.error.URLError,TimeoutError,ConnectionError,ssl.SSLError) as exc:
            if attempt==len(TLS_TRANSIENT_RETRY_DELAYS_SEC):
                raise RuntimeError("STAGE97_ORIGINAL_ERA5_TLS_CONNECTIVITY_RETRIES_EXHAUSTED") from exc
            pause=TLS_TRANSIENT_RETRY_DELAYS_SEC[attempt]
            print("STAGE97_SOURCE_CONNECTION_TRANSIENT_RETRY",
                  {"attempt":attempt+1,"pause_seconds":pause,
                   "error_type":type(exc).__name__,
                   "reason":str(exc)[:160]},flush=True)
            time.sleep(pause)

def verified_prior25(path,allsites):
    """Require frozen original Stage95C signed first-25 sites, not guessed ranks."""
    if sha256(path)!=FIRST25_SHA:
        raise ValueError("STAGE97_ORIGINAL_25_SOURCE_ARTIFACT_SHA_DRIFT")
    with zipfile.ZipFile(path) as z:
        names=[n for n in z.namelist() if
               n==FIRST25_MEMBER or n.endswith("/"+FIRST25_MEMBER)]
        if len(names)!=1:raise ValueError("STAGE97_ORIGINAL_25_SOURCE_MEMBER_MISSING")
        data=json.loads(z.read(names[0]))
    if data.get("source_completed_region_count")!=25 or len(data.get("sites",[]))!=25:
        raise ValueError("STAGE97_SOURCE_STAGE95C_NOT_25_COMPLETE")
    previous=[r["TDWG_L3"] for r in data["sites"]]
    current=[r["TDWG_L3"] for r in allsites[:START]]
    if previous!=current or len(set(previous))!=25:
        raise ValueError("STAGE97_PREVIOUS_25_SOURCE_IDS_CHANGED")
    if data.get("no_source_regional_area_weighting") is not True:
        raise ValueError("STAGE97_PREVIOUS_25_SOURCE_MISDESCRIBED")
    return previous

def next25(allsites,previous):
    if len(allsites)!=125:
        raise ValueError("STAGE97_ORIGINAL_MAINLAND_UNIVERSE_CHANGED")
    rows=allsites[START:START+COUNT]
    labels=[s["TDWG_L3"] for s in rows]
    if len(rows)!=COUNT or set(labels)&set(previous) or len(set(labels))!=COUNT:
        raise ValueError("STAGE97_25_49_SELECTION_MISSING_OR_DUPLICATES")
    if any(r.get("regional_strict_continent_connected_scope")!="mainland" for r in rows):
        raise ValueError("STAGE97_NONMAINLAND_SITE_ENTERED_SOURCE_BATCH")
    if {s["shared_split"] for s in rows}-{"exploration","holdout"}:
        raise ValueError("STAGE97_SPLIT_NOT_FROZEN")
    return rows

def run(geography_zip,tdwg_geo,first25_archive,outdir):
    sites=source_mainland_regions(geography_zip,tdwg_geo)
    prior=verified_prior25(first25_archive,sites)
    selection=next25(sites,prior)
    original_queries=[];regional=[];quota_retries=[]
    outdir.mkdir(parents=True,exist_ok=True)
    for start in range(0,COUNT,SITES_PER_REQUEST):
        if start:
            print("STAGE97_PAUSE_BETWEEN_PROVIDER_SOURCE_GROUPS",INTER_GROUP_PACE_SEC,flush=True)
            time.sleep(INTER_GROUP_PACE_SEC)
        group=selection[start:start+SITES_PER_REQUEST]
        original_daily={r["TDWG_L3"]:[] for r in group}
        for y1,y2 in YEARS:
            url=api_url(group,f"{y1}-01-01",f"{y2}-12-31")
            try:
                frames,source_sha,n_bytes=original_source_with_bounded_transient_retries(url)
            except ValueError as exc:
                if "STAGE95_OPENMETEO_ERA5_API_HTTP_429_" not in str(exc):
                    raise
                print("STAGE97_QUOTA_HTTP429_EXPLICIT_PROVIDER",str(exc)[:200],flush=True)
                quota_retries.append({"source_batch":start//SITES_PER_REQUEST,
                                      "original_decade":f"{y1}-{y2}",
                                      "wait_seconds":SOURCE_429_PAUSE_SEC})
                time.sleep(SOURCE_429_PAUSE_SEC)
                frames,source_sha,n_bytes=original_source_with_bounded_transient_retries(url)
            if not isinstance(frames,list) or len(frames)!=len(group):
                raise ValueError("STAGE97_ORIGINAL_FIVE_SOURCE_RESPONSE_COUNT_MISMATCH")
            original_queries.append({
                "original_fixed_source_batch":start//SITES_PER_REQUEST,
                "original_era5_source_years":f"{y1}-{y2}",
                "requested_TDWG3_region_codes":[r["TDWG_L3"] for r in group],
                "raw_API_JSON_SHA256":source_sha,
                "source_JSON_bytes":n_bytes,
                "source_query":url})
            for row,frame in zip(group,frames):
                returned=(frame.get("latitude"),frame.get("longitude"))
                if not all(isinstance(v,(int,float)) for v in returned):
                    raise ValueError("STAGE97_NO_RETURNED_ORIGINAL_ERA5_GRID_COORDINATES")
                if abs(returned[0]-row["lat"])>1 or abs(returned[1]-row["lon"])>1:
                    raise ValueError("STAGE97_SOURCE_RETURNED_GRID_VS_TDWG_SITE_MISMATCH")
                original_daily[row["TDWG_L3"]].extend(parse_decade(frame,y1,y2))
        for row in group:
            response=climatology(original_daily[row["TDWG_L3"]])
            if response["source_ERA5_observed_30yr_days"]!=10958:
                raise ValueError("STAGE97_GUST_SOURCE_30YR_DAILY_INCOMPLETE")
            regional.append({**row,**response})
        # On a later batch failure, the workflow's if-always artifact will
        # still preserve this complete source-derived batch and its SHA ledger.
        # Never mistake a partial artifact for a complete 25-region result.
        batch_idx=start//SITES_PER_REQUEST
        (outdir/f"stage97_partial_source_batch_{batch_idx:02d}_NOT_25_COMPLETE.json").write_text(
            json.dumps({"schema":"stage97_provisional_SOURCE_BATCH_NOT_FULL_25",
                        "source_batch":batch_idx,
                        "source_original_TDWG_codes":[r["TDWG_L3"] for r in group],
                        "original_ERA5_source_query_receipts":
                           [x for x in original_queries
                            if x["original_fixed_source_batch"]==batch_idx],
                        "source_30yr_derived_sites":[r for r in regional
                            if r["TDWG_L3"] in {x["TDWG_L3"] for x in group}],
                        "not_a_completed_25_region_analysis":True},
                       indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print("STAGE97_SOURCE_ERA5_BATCH_COMPLETE",json.dumps({
            "batch_number":batch_idx,
            "source_region_codes":[r["TDWG_L3"] for r in group],
            "completed_regions":len(regional)},sort_keys=True),flush=True)
    if len(regional)!=COUNT:
        raise ValueError("STAGE97_INCOMPLETE_25_REGION_SOURCE")
    nonmissing=[x["source_primary_fraction_days_daily_gust_strict_above_15_ms"]
                for x in regional if x["source_primary_fraction_days_daily_gust_strict_above_15_ms"] is not None]
    info={
      "schema":"stage97_second25_verified_1991_2020_ERA5_model_30yr_mainland_points_source",
      "original_supplemental_source":"Stage95C_first25",
      "source_original_stage95C_first25_ZIP_SHA256":FIRST25_SHA,
      "source_prior25_exact_region_codes":prior,
      "source_sorted_TDWG3_zero_based_region_position_range":[START,START+COUNT-1],
      "source_new25_original_region_codes":[r["TDWG_L3"] for r in regional],
      "original_mainland_region_frame":125,
      "original_partition_size":{"exploration":88,"holdout":37},
      "source_new25_partition":dict(Counter(r["shared_split"] for r in regional)),
      "source_zero_overlap_prior25":True,
      "original_daily_ERA5_model_complete_1991_2020_30yr_days_per_region":10958,
      "source_returned_distinct_region_count":len(regional),
      "source_daily_primary_gust_strict_above_15_ms_eligible_T2m_months_strict_above_5C":True,
      "source_monthly_temperature_eligibility_fixed_from_1991_2020":True,
      "source_gust_fraction_nonmissing_region_count":len(nonmissing),
      "source_point_fraction_min":min(nonmissing) if nonmissing else None,
      "source_point_fraction_max":max(nonmissing) if nonmissing else None,
      "original_raw_source_JSON_SHA256_queries":original_queries,
      "source_429_quota_retry_log":quota_retries,
      "source_batch_pace_seconds":INTER_GROUP_PACE_SEC,
      "regions":regional,
      "region_area_weighting_performed":False,
      "independent_original_CDS_hourly_10fg_comparison_performed":False,
      "biological_ecological_wind_signal_coefficient_estimated":False,
      "holdout_flora_signal_outcomes_opened":False
    }
    if len(original_queries)!=15 or len(set(x["raw_API_JSON_SHA256"] for x in original_queries))!=15:
        raise ValueError("STAGE97_INCOMPLETE_OR_DUPLICATED_RAW_API_REQUESTS")
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"stage97_real_1991_2020_next25_original_mainland_ERA5_model_gust.json").write_text(
        json.dumps(info,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE97_ORIGINAL_NEXT25_MAINLAND_GUST_SOURCE_SUCCESS",
          json.dumps({"n":len(regional),"q":len(original_queries),
                      "range":[info["source_point_fraction_min"],info["source_point_fraction_max"]],
                      "folds":info["source_new25_partition"]},sort_keys=True),flush=True)
    return info

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-stage94-mainland-geo-ZIP",type=Path,required=True)
    p.add_argument("--original-TDWG3-geojson",type=Path,required=True)
    p.add_argument("--original-first25-ERA5-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    run(a.original_stage94_mainland_geo_ZIP,a.original_TDWG3_geojson,
        a.original_first25_ERA5_ZIP,a.outdir)
