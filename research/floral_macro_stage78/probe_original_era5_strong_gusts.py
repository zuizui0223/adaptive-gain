"""Stage78A: actual historical ERA5 gusts, not average background wind.

Outcome-blind public field-site pilot: 2018 June, one real EuPPollNet network
per study (5 study IDs) from the original Stage77A 54-study site manifest.
Strong gust exposure = proportion of days max ERA5 reanalysis 10m gust >=15 m/s.
Sensitivity: >=10, >=20 m/s, daily max sustained >=8 m/s, p95 gust.
Source UTC daily reanalysis is not observed bee visit-hour wind or true
turbulent floral VOC plume. Exceedance thresholds fixed before outcome access.
"""
from __future__ import annotations
import argparse,csv,datetime,hashlib,json,math,urllib.parse,urllib.request
from pathlib import Path

STAGE77_SHA="948ac0ecbcfc9b8a2e810753748a5436d998cd586574ea185c6da5db08cbce53"
API="https://archive-api.open-meteo.com/v1/archive"
YEAR=2018
MONTH=6
PILOT_STUDIES=5
SOURCE_GUST_THRESHOLDS=(10.,15.,20.)
SOURCE_MAXSPEED_THRESHOLD=8.

def source_pilot_rows(path):
    data=Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest()!=STAGE77_SHA:
        raise ValueError("STAGE78_SOURCE_FIELD_SITE_SHA_CHANGED")
    with Path(path).open(encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=1864 or len({r["Study_id"] for r in rows})!=54:
        raise ValueError("STAGE78_CORRECTED_SOURCE_1864_54_STUDIES_NOT_VERIFIED")
    sites={}
    for r in sorted(rows,key=lambda r:(r["Study_id"],r["Network_id"])):
        if r["Year"]!=str(YEAR) or str(MONTH) not in r["source_observed_visit_months"].split(","):
            continue
        if r["Study_id"] in sites or not r["Latitude_original"] or not r["Longitude_original"]:
            continue
        sites[r["Study_id"]]={
           "Study_id":r["Study_id"],"Network_id":r["Network_id"],
           "Year":r["Year"],
           "latitude":float(r["Latitude_original"]),
           "longitude":float(r["Longitude_original"]),
           "original_recorded_visit_months":r["source_observed_visit_months"],
           "selected_without_any_insect_outcome":True}
        if len(sites)==PILOT_STUDIES:break
    if len(sites)!=PILOT_STUDIES:
        raise ValueError("STAGE78_EXPECTED_FIVE_INDEPENDENT_STUDY_SITE_PILOT_MISSING")
    return list(sites.values())

def query_sites(rows,start="2018-06-01",end="2018-06-30"):
    params={
       "latitude":",".join(str(round(r["latitude"],5)) for r in rows),
       "longitude":",".join(str(round(r["longitude"],5)) for r in rows),
       "start_date":start,"end_date":end,
       "daily":"wind_gusts_10m_max,wind_speed_10m_max,temperature_2m_mean,precipitation_sum",
       "models":"era5","timezone":"GMT","wind_speed_unit":"ms",
       "elevation":"nan","cell_selection":"nearest",
    }
    return API+"?"+urllib.parse.urlencode(params)

def original_api(url):
    if not url.startswith(API+"?"):
        raise ValueError("STAGE78_NON_OFFICIAL_HISTORICAL_ARCHIVE_ENDPOINT")
    request=urllib.request.Request(url,headers={
       "Accept":"application/json",
       "User-Agent":"academic-floral-strong-gust-research-source-2026-11-18"})
    with urllib.request.urlopen(request,timeout=110) as response:
        raw=response.read(2500000)
        mime=response.headers.get("Content-Type","")
    if not raw or len(raw)>=2500000 or "json" not in mime:
        raise ValueError("STAGE78_SOURCE_API_NOT_REAL_JSON")
    result=json.loads(raw)
    if isinstance(result,dict) and result.get("error"):
        raise ValueError("STAGE78_ERA5_API_ERROR_"+str(result.get("reason"))[:120])
    return result,hashlib.sha256(raw).hexdigest(),len(raw)

def original_wind_summary(site,frame):
    daily=frame.get("daily") or {}
    units=frame.get("daily_units") or {}
    if units.get("wind_gusts_10m_max")!="m/s" or units.get("wind_speed_10m_max")!="m/s":
        raise ValueError("STAGE78_GUST_SOURCE_UNIT_IS_NOT_MS")
    if frame.get("utc_offset_seconds")!=0:
        raise ValueError("STAGE78_SOURCE_NOT_GMT")
    first=datetime.date(YEAR,MONTH,1)
    days=[(first+datetime.timedelta(days=k)).isoformat() for k in range(30)]
    if daily.get("time")!=days:
        raise ValueError("STAGE78_SOURCE_SURVEY_MONTH_DAILY_DATE_MISMATCH")
    g=daily.get("wind_gusts_10m_max")
    w=daily.get("wind_speed_10m_max")
    if not isinstance(g,list) or not isinstance(w,list) or len(g)!=30 or len(w)!=30:
        raise ValueError("STAGE78_SOURCE_DAILY_WIND_GUST_SERIES_MISSING")
    if any(x is None or not isinstance(x,(int,float)) or not math.isfinite(x) or x<0
           for x in g+w):
        raise ValueError("STAGE78_SOURCE_MISSING_GUST_DAYS_NOT_IMPUTED_ZERO")
    ordered=sorted(g)
    summary={**site,"returned_ERA5_grid_latitude":frame.get("latitude"),
             "returned_ERA5_grid_longitude":frame.get("longitude"),
             "source_actual_daily_gust_values":len(g),
             "source_ERA5_month_max_daily_gust_ms":max(g),
             "source_ERA5_month_p95_daily_max_gust_ms":ordered[math.ceil(.95*len(ordered))-1],
             "source_ERA5_mean_daily_max_gust_ms":sum(g)/len(g),
             "source_days_max_sustained_ge_8_ms":sum(x>=8 for x in w),
             "source_gust_is_reanalysis_not_site_anemometer":True,
             "survey_date_hour_specific_gust_recorded":False}
    for t in SOURCE_GUST_THRESHOLDS:
        n=sum(x>=t for x in g)
        summary["source_daily_max_gust_days_ge_"+str(int(t))+"_ms"]=n
        summary["source_daily_max_gust_fraction_ge_"+str(int(t))+"_ms"]=n/len(g)
    return summary

def run(site_csv):
    sites=source_pilot_rows(site_csv)
    url=query_sites(sites)
    data,source_sha,source_bytes=original_api(url)
    if not isinstance(data,list) or len(data)!=len(sites):
        raise ValueError("STAGE78_ERA5_MULTI_SITE_PAYLOAD_NOT_MATCHING_ORIGINAL_SOURCE")
    output=[original_wind_summary(site,frame) for site,frame in zip(sites,data)]
    return {
       "schema":"stage78a_real_ERA5_daily_10m_gust_strong_wind_source_probe",
       "source_field_sites":sites,
       "source_ERA5_original_query":url,
       "source_original_ERA5_API_JSON_SHA256":source_sha,
       "source_original_ERA5_API_JSON_bytes":source_bytes,
       "source_real_strong_gust_overview":output,
       "primary_gust_day_threshold_m_s":15,
       "sensitivity_gust_day_thresholds_m_s":[10,20],
       "alternative_sustained_wind_max_threshold_m_s":8,
       "model_forced_ERA5_consistent_historical":"era5",
       "data_attribution":"ERA5 via Open-Meteo historical weather API, CC BY 4.0",
       "not_survey_hour_and_not_direct_flower_scent_plume":True,
       "sample_selected_before_bumblebee_or_visual_hue_outcomes":True,
       "no_path_effect_estimated_at_pilot":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-original-stage77-sites",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    data=run(a.source_original_stage77_sites)
    a.outdir.mkdir(parents=True,exist_ok=True)
    (a.outdir/"source_ERA5_2018_June_gust_extreme_five_studies.json").write_text(
        json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE78_ORIGINAL_STRONG_GUST_REAL_ERA5_FIVE_STUDY_SITE_PROBE",
          json.dumps(data,sort_keys=True))
    print("STRONG_GUST_NOT_MONTHLY_MEAN_WIND_NOT_DIRECT_VISIT_GUST")
if __name__=="__main__":
    main()
