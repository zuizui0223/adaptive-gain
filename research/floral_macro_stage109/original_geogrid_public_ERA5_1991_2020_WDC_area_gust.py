#!/usr/bin/env python3
"""Stage109: NO-CDS-TOKEN alternative, genuine 30-year WDC multi-cell source wind.

Recover real, model-specific Open-Meteo historical *ERA5* derived daily data
at each exact frozen 0.25deg source land-grid centre from Stage106 (WDC 2
original physically weighted intersecting cells). Original source SHA-verified
geography independent of wind and floral trait results.

Per model grid cell: calendar-month 1991–2020 mean daily 2m temperature
strict >5 C; among all 30yr days in those eligible months, fraction with
original-source daily max 10m gust STRICT >15m/s. Integrate *cell fractions*
by physically intersected mainland land area km2. Exceedance 10/20 m/s
sensitivity is prespecified. Never pretend this is original ECMWF hourly CDS
10fg, or a global 125-region response. Do not look at plant traits/holdout.

The API endpoint is unauthenticated for noncommercial research (subject to
provider terms), models=era5, cell_selection=nearest, elevation=nan,
timezone=GMT, gust units ms. Returned coordinates MUST match original exact
grid centres; no hidden downscaling/substitution or missing daily cells.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,sys,time,ssl,urllib.error,zipfile
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/"floral_macro_stage95"))
from original_ERA5_1991_2020_gust_five_mainland_pilot import (
    api_url,query_original,parse_decade,climatology,YEARS,PRIMARY_THRESHOLD,
    GUST_THRESHOLDS
)

SOURCE_STAGE106_GEO_SHA="09c65542c221daecd1867baf250b694e9229f7c85fc09d401849765aa234b6b8"
GEO_MEMBER="stage106_original_three_mainland_regions_ERA5_025deg_cell_landarea_weights.csv"
GEO_RECEIPT="stage106_original_CDS_ERA5_daily_10fg_1991_2020_area_weighting_PRECHECK.json"
FIRST_REGION="WDC"
MAX_CELL_COORD_DIFF_DEGREES=.051
SECONDS_BETWEEN_DECADES=18
TRANSPORT_BACKOFF_SEC=(15,45)
QUOTA_BACKOFF_SEC=(75,125)

def sha256(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def original_geodesic_source_land_cells(path):
    if sha256(path)!=SOURCE_STAGE106_GEO_SHA:
        raise ValueError("STAGE109_ORIGINAL_STAGE106_GEOMETRY_SOURCE_SHA_CHANGED")
    with zipfile.ZipFile(path) as z:
        if not {GEO_MEMBER,GEO_RECEIPT}<=set(z.namelist()):
            raise ValueError("STAGE109_ORIGINAL_STAGE106_MEMBERS_MISSING")
        rows=list(csv.DictReader(io.StringIO(z.read(GEO_MEMBER).decode("utf-8-sig"))))
        receipt=json.loads(z.read(GEO_RECEIPT))
    if receipt["CDS_original_API_source_request_submitted"] or (
       not receipt["actual_area_weights_derived_from_original_source_polygon_intersections"]):
        raise ValueError("STAGE109_GEO_SOURCE_SEMANTICS_CHANGED")
    desired=[r for r in rows if r["TDWG_L3"]==FIRST_REGION]
    if len(desired)!=2:raise ValueError("STAGE109_WDC_ORIGINAL_TRUE_2_LANDCELLS_NOT_FOUND")
    sites=[];seen=set()
    for r in sorted(desired,key=lambda x:(float(x["ERA5_atmosphere_source_grid_latitude"]),
                                         float(x["ERA5_atmosphere_source_grid_longitude"]))):
        lat=float(r["ERA5_atmosphere_source_grid_latitude"])
        lon=float(r["ERA5_atmosphere_source_grid_longitude"])
        km2=float(r["source_intersected_original_mainland_land_km2"])
        if not math.isfinite(km2) or km2<=0 or (lat,lon) in seen:
            raise ValueError("STAGE109_ORIGINAL_LANDGRID_INVALID_OR_DUPLICATE")
        if abs(lat*4-round(lat*4))>1e-6 or abs(lon*4-round(lon*4))>1e-6:
            raise ValueError("STAGE109_NOT_ERA5_025_SOURCE_GRID_CENTRE")
        seen.add((lat,lon))
        sites.append({"TDWG_L3":FIRST_REGION,"lat":lat,"lon":lon,
            "source_grid_land_area_km2":km2,
            "source_TDWG_polygon_sha256":r["source_region_original_TDWG_polygon_SHA256"]})
    if not 180<sum(x["source_grid_land_area_km2"] for x in sites)<190:
        raise ValueError("STAGE109_ORIGINAL_MAINLAND_AREA_NOT_185KM2")
    return sites

def source_decade_with_bounded_provider_retries(url):
    for transport_attempt in range(len(TRANSPORT_BACKOFF_SEC)+1):
        try:
            return query_original(url)
        except ValueError as exc:
            if "STAGE95_OPENMETEO_ERA5_API_HTTP_429_" in str(exc):
                if transport_attempt==len(QUOTA_BACKOFF_SEC):
                    raise ValueError("STAGE109_OPENMETEO_SOURCE_RATE_LIMIT_EXHAUSTED") from None
                delay=QUOTA_BACKOFF_SEC[transport_attempt]
                print("STAGE109_SOURCE_PUBLIC_PROVIDER_QUOTA_WAIT",
                      {"attempt":transport_attempt+1,"wait_sec":delay},flush=True)
                time.sleep(delay)
                continue
            raise
        except (TimeoutError,urllib.error.URLError,ConnectionError,ssl.SSLError) as exc:
            if transport_attempt==len(TRANSPORT_BACKOFF_SEC):
                raise ValueError("STAGE109_SOURCE_TRANSPORT_RETRY_EXHAUSTED") from None
            delay=TRANSPORT_BACKOFF_SEC[transport_attempt]
            print("STAGE109_SOURCE_TRANSIENT_TRANSPORT_RETRY",
                  {"attempt":transport_attempt+1,"wait_sec":delay},flush=True)
            time.sleep(delay)
    raise ValueError("STAGE109_SOURCE_REQUEST_NOT_COMPLETED")

def accepted_grid_coordinates(original,frame):
    for key in ("latitude","longitude"):
        if key not in frame:
            raise ValueError("STAGE109_UNDISCLOSED_SOURCE_MODEL_GRID_COORDINATES")
    lat=float(frame["latitude"]);lon=float(frame["longitude"])
    if not math.isfinite(lat) or not math.isfinite(lon):
        raise ValueError("STAGE109_INVALID_SOURCE_COORDINATES")
    diff_lon=abs((lon-original["lon"]+180)%360-180)
    if (abs(lat-original["lat"])>MAX_CELL_COORD_DIFF_DEGREES or
        diff_lon>MAX_CELL_COORD_DIFF_DEGREES):
        raise ValueError("STAGE109_OPENMETEO_RETURNED_DIFFERENT_ERA5_MODEL_CELL")
    return {"latitude":lat,"longitude":lon,
            "coordinate_offset_deg_lat":lat-original["lat"],
            "coordinate_offset_deg_lon":((lon-original["lon"]+180)%360-180)}

def actual_source_area_averaged_climatology(cell_results):
    if len(cell_results)!=2:raise ValueError("STAGE109_NOT_WDC_TWO_GRID_CELLS")
    valid=[r for r in cell_results
           if r["source_1991_2020_climatology"]["source_primary_fraction_days_daily_gust_strict_above_15_ms"] is not None]
    total=sum(r["source_grid_land_area_km2"] for r in cell_results)
    coverage=sum(r["source_grid_land_area_km2"] for r in valid)/total
    if coverage<.95:raise ValueError("STAGE109_WARM_MONTH_GRID_LAND_COVERAGE_BELOW_95PCT")
    estimate={}
    for label,key in [
        ("main_15_ms","source_primary_fraction_days_daily_gust_strict_above_15_ms"),
        ("sensitivity_10_ms","source_fraction_gust_greater_than_10_ms"),
        ("sensitivity_20_ms","source_fraction_gust_greater_than_20_ms")]:
        numer=sum(r["source_grid_land_area_km2"]*
                 r["source_1991_2020_climatology"][key] for r in valid)
        estimate[label]=numer/sum(r["source_grid_land_area_km2"] for r in valid)
        if not 0<=estimate[label]<=1:raise ValueError("STAGE109_BAD_SOURCE_GUST_EXCEEDANCE_FRACTION")
    vals=[r["source_1991_2020_climatology"]["source_primary_fraction_days_daily_gust_strict_above_15_ms"]
          for r in valid]
    return {
      "geographic_original_TDWG3_code":FIRST_REGION,
      "source_original_land_area_total_km2":total,
      "source_original_land_area_with_warm_climate_fraction":coverage,
      "source_gridcell_count":len(cell_results),
      "source_1991_2020_original_ERA5_model_daily_gust15_frequency_area_weighted":estimate["main_15_ms"],
      "source_gust_gt10_model_daily_area_weighted":estimate["sensitivity_10_ms"],
      "source_gust_gt20_model_daily_area_weighted":estimate["sensitivity_20_ms"],
      "source_original_land_cell_gust15_min":min(vals),
      "source_original_land_cell_gust15_max":max(vals),
      "source_single_point_vs_area_weighted_difference_auditable":True,
      "source_NO_original_CDS_hourly_10fg_byte_verification":True,
      "source_model_openmeteo_daily_archive_derivation_NOT_original_CDS":True}

def run(geometry,outdir):
    sites=original_geodesic_source_land_cells(geometry)
    series={i:[] for i in range(len(sites))}
    query_receipts=[]
    for i,(y1,y2) in enumerate(YEARS):
        if i:time.sleep(SECONDS_BETWEEN_DECADES)
        url=api_url(sites,f"{y1}-01-01",f"{y2}-12-31")
        # Source provider URL contains no key; this is a FREE historical ERA5
        # model projection, not original ECMWF CDS hourly 10fg.
        frames,sourcehash,sourcebytes=source_decade_with_bounded_provider_retries(url)
        if not isinstance(frames,list) or len(frames)!=len(sites):
            raise ValueError("STAGE109_MULTISITE_HISTORICAL_ERA5_RESPONSE_COUNT_CHANGED")
        row={"source_years":f"{y1}-{y2}",
            "public_API_url":url,"original_unmodified_JSON_SHA256":sourcehash,
            "source_JSON_bytes":sourcebytes,"source_model":"era5",
            "source_model_data_and_time_range_NOT_hypothesis_fitted":True}
        for j,frame in enumerate(frames):
            coordinates=accepted_grid_coordinates(sites[j],frame)
            previous=next((r for r in query_receipts if r.get("site_index")==j),None)
            # Keep per-decade returned coordinates to detect changing model cells.
            series[j].extend(parse_decade(frame,y1,y2))
            row[f"site_{j}_actual_returned_lat_lon"]=(coordinates["latitude"],coordinates["longitude"])
        query_receipts.append(row)
        # Source fingerprint checkpoint; only complete decade, no fake 30y
        # claim if the provider stops during subsequent requests.
        outdir.mkdir(parents=True,exist_ok=True)
        (outdir/f"stage109_source_decade_{y1}_{y2}_ONLY_NOT_FULL30YR.json").write_text(
            json.dumps({"status":"SOURCE_DECADE_ONLY_NOT_FULL30YR",
                        "source":row,
                        "original_land_cells":len(sites)},indent=2,sort_keys=True)+"\n")
        print("STAGE109_REAL_PUBLIC_ERA5_TWO_GRIDCELL_DECADE_SOURCE",
              {"years":f"{y1}-{y2}","source_JSON_SHA256":sourcehash},flush=True)
    climates=[]
    for j,site in enumerate(sites):
        src=climatology(series[j])
        if src["source_ERA5_observed_30yr_days"]!=10958:
            raise ValueError("STAGE109_NOT_COMPLETE30Y_WDC_SOURCE_DATES")
        climates.append({**site,"source_1991_2020_climatology":src})
    if len({tuple(q[f"site_{j}_actual_returned_lat_lon"])
         for j in range(len(sites)) for q in query_receipts})!=len(sites):
        # THIS gate specifically requires original ERA5 MODEL grid cells
        # identical across all three decades. Each cell appears in 3
        # receipts; number distinct return coordinates must remain 2.
        raise ValueError("STAGE109_SOURCE_MODEL_CELL_CHANGES_ACROSS_DECADES")
    combined=actual_source_area_averaged_climatology(climates)
    receipt={
      "schema":"stage109_first_real_source_1991_2020_two_original_WDC_land_cells_openmeteo_ERA5_model",
      "original_stage106_true_mainland_025_geo_SHA256":SOURCE_STAGE106_GEO_SHA,
      "original_API_model":"era5","original_API_cell_selection":"nearest",
      "original_API_request_elevation":"nan",
      "source_original_30year_complete_daily_climatology":True,
      "source_no_CDS_token_required_and_no_licence_bypass_performed":True,
      "source_only_model_ERA5_daily_derived_not_raw_hourly_original_CDS_10fg":True,
      "source_fixed_geography_selected_prior_to_gust_and_flower_outcomes":True,
      "no_NHM_WFO_flower_Bombus_or_holdout_data_read":True,
      "not_125_full_mainland_area_exposure":True,
      "source_daily_site_weather_and_frozen_area_weights":climates,
      "original_source_decade_JSON_SHA256_query_receipts":query_receipts,
      "source_geographic_area_weighted_ERA5_model_climate":combined}
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"stage109_WDC_two_true_mainland_025deg_cells_30yr_public_ERA5_model_area_gust.json").write_text(
         json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE109_REAL_NO_CDS_ERA5_MODEL_1991_2020_MAINLAND_2CELL_WIND",
          json.dumps(combined,sort_keys=True),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage106-land-grid-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.original_Stage106_land_grid_ZIP,a.outdir)
