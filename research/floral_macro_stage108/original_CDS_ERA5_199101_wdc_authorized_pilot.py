#!/usr/bin/env python3
"""Stage108: official Copernicus CDS ERA5 daily 10fg AUTHENTIC source pilot.

Official 1991-01 small region WDC, 2 land-intersecting 0.25° cells, original
Stage106 source area weights. Two independent CDS requests (daily max 10fg,
daily mean 2m temperature) and NetCDF-in-ZIP inspection.

Fail closed. No secret printed or saved. CDS PERSONAL ACCESS TOKEN must have
been configured in GitHub Actions; dataset licence must ALREADY be accepted
by account owner on official dataset site. We NEVER accept terms on behalf of
the owner or try to bypass a CDS licence failure.

One January 1991 month CANNOT estimate the target 1991-2020 regional gust
fraction for climatologically flowering months. This is only source semantics
and data-retrievability proof. No flower/bee outcomes are opened.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,os,re,sys,tempfile,zipfile
from pathlib import Path
from datetime import date,timedelta
from collections import Counter
import numpy as np
import xarray as xr

CDS_URL="https://cds.climate.copernicus.eu/api"
CDS_DATASET="derived-era5-single-levels-daily-statistics"
SOURCE_STAGE106_SHA="09c65542c221daecd1867baf250b694e9229f7c85fc09d401849765aa234b6b8"
SOURCE_GRID_MEMBER="stage106_original_three_mainland_regions_ERA5_025deg_cell_landarea_weights.csv"
SOURCE_REQUESTS="stage106_original_CDS_ERA5_daily_10fg_1991_2020_area_weighting_PRECHECK.json"
SOURCE_TDWG="WDC"
PERIOD="1991-01"
TYPES={
    "gust":("10m_wind_gust_since_previous_post_processing","daily_max"),
    "temperature":("2m_temperature","daily_mean")}
EXPECTED_DAYS=[date(1991,1,day).isoformat() for day in range(1,32)]
SOURCE_PROVENANCE="official_CDS_ERA5_daily_postprocessed_hourly_source_not_OpenMeteo"
MAX_ORIGINAL_DOWNLOAD_BYTES=90_000_000
GUST_UNITS={"m/s","m s-1","m s^-1","m s**-1","m s⁻¹","m s^{-1}"}
TEMP_UNITS={"k","kelvin"}
COORD_LAT={"lat","latitude"}
COORD_LON={"lon","longitude"}
COORD_TIME={"time","valid_time"}

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()

def exact_stage106_source(path):
    if sha256(path)!=SOURCE_STAGE106_SHA:
        raise ValueError("STAGE108_ORIGINAL_STAGE106_AREA_SOURCE_SHA_DRIFT")
    with zipfile.ZipFile(path) as z:
        if not {SOURCE_GRID_MEMBER,SOURCE_REQUESTS}<=set(z.namelist()):
            raise ValueError("STAGE108_AREA_WEIGHT_OR_OFFICIAL_REQUEST_RECEIPT_MISSING")
        receipt=json.loads(z.read(SOURCE_REQUESTS))
        rows=list(csv.DictReader(io.StringIO(z.read(SOURCE_GRID_MEMBER).decode("utf-8-sig"))))
    if (receipt["CDS_official_dataset"]!=CDS_DATASET or
        receipt["CDS_original_API_source_request_submitted"] is not False or
        receipt["source_global_125_region_climatology_NOT_obtained"] is not True):
        raise ValueError("STAGE108_ORIGINAL_SOURCE_CDS_CONTRACT_CHANGED")
    cells=[r for r in rows if r["TDWG_L3"]==SOURCE_TDWG]
    if len(cells)!=2:
        raise ValueError("STAGE108_WDC_ORIGINAL_TWO_GEO_LAND_CELLS_CHANGED")
    weights={}
    for r in cells:
        la=float(r["ERA5_atmosphere_source_grid_latitude"])
        lo=float(r["ERA5_atmosphere_source_grid_longitude"])
        km2=float(r["source_intersected_original_mainland_land_km2"])
        if not (math.isfinite(km2) and km2>0 and (la,lo) not in weights):
            raise ValueError("STAGE108_DUPLICATE_OR_NONPOSITIVE_GEO_CELL")
        weights[la,lo]=km2
    if not 180<sum(weights.values())<190:
        raise ValueError("STAGE108_WDC_AREA_SOURCE_INTEGRAL_CHANGED")
    req={}
    for r in receipt["source_month_1991_01_CDS_request_specs_NOT_submitted"]:
        if r["TDWG_L3"]!=SOURCE_TDWG:continue
        source=r["one_month_source_probe_request_NOT_SUBMITTED"]
        pair=(r["variable_source"],r["statistic"])
        if pair not in TYPES.values():continue
        label=next(k for k,v in TYPES.items() if v==pair)
        if label in req:raise ValueError("STAGE108_DUPLICATE_SOURCE_REQUEST_VARIABLE")
        if (source["product_type"]!="reanalysis" or
            source["frequency"]!="1_hourly" or
            source["time_zone"]!="utc+00:00" or
            source["year"]!="1991" or source["month"]!=["01"] or
            source["day"]!=[f"{d:02d}" for d in range(1,32)]):
            raise ValueError("STAGE108_SOURCE_DATE_OR_AGGREGATION_SPEC_CHANGED")
        req[label]=source
    if set(req)!=set(TYPES):
        raise ValueError("STAGE108_MISSING_ONE_OF_TWO_OFFICIAL_SOURCE_REQUESTS")
    return weights,req

def _time_days(arr):
    try:
        times=np.asarray(arr.values).astype("datetime64[D]")
    except Exception as exc:
        raise ValueError("STAGE108_ORIGINAL_CDS_NETCDF_TIME_COORDINATES_UNPARSEABLE") from exc
    result=[np.datetime_as_string(v,unit="D") for v in times]
    if result!=EXPECTED_DAYS:
        raise ValueError("STAGE108_JAN_1991_31_DAILY_NETCDF_COORDINATES_INCOMPLETE")
    return result

def _coordinate_name(ds,choices):
    candidate=[x for x in list(ds.coords)+list(ds.dims) if x.casefold() in choices]
    if not candidate:
        raise ValueError("STAGE108_CDS_NETCDF_MISSING_TIME_OR_GRID_COORD")
    return candidate[0]

def _variable(ds,kind,axis):
    candidates=[]
    for name,var in ds.data_vars.items():
        if not all(x in var.dims for x in axis.values()):
            continue
        # Prevent accepting multi-variable climate response by arbitrarily
        # choosing the first field; select source name or single original.
        candidates.append((name,var))
    if len(candidates)!=1:
        raise ValueError("STAGE108_CDS_NETCDF_NOT_UNIQUE_CLIMATE_VARIABLE")
    name,var=candidates[0]
    normalized=str(var.attrs.get("units","")).strip().casefold().replace(" "," ")
    allowed=GUST_UNITS if kind=="gust" else TEMP_UNITS
    if normalized not in allowed:
        raise ValueError("STAGE108_CDS_NETCDF_SOURCE_UNIT_INCONSISTENT_"+kind)
    check=(name+" "+
           str(var.attrs.get("long_name",""))+" "+
           str(var.attrs.get("GRIB_shortName",""))).lower()
    if kind=="gust":
        if not any(x in check for x in ("10fg","fg10","gust")):
            raise ValueError("STAGE108_CDS_NETCDF_VARIABLE_NOT_10FG_GUST")
    else:
        if not any(x in check for x in ("t2m","2t","2m","temperature")):
            raise ValueError("STAGE108_CDS_NETCDF_VARIABLE_NOT_2M_TEMPERATURE")
    return name,var

def inspect_original_cds_netcdf_bytes(raw_zip,kind,expected_locations):
    """Validate authentic NetCDF schema, exact days, units and SOURCE cells.

    Testable with synthetic NetCDF ZIP, no CDS credentials.
    """
    if len(raw_zip)>=MAX_ORIGINAL_DOWNLOAD_BYTES:
        raise ValueError("STAGE108_OFFICIAL_SMALL_SOURCE_ZIP_TOO_LARGE")
    if not zipfile.is_zipfile(io.BytesIO(raw_zip)):
        raise ValueError("STAGE108_CDS_DAILY_STATISTICS_MUST_BE_NETCDF_IN_ZIP")
    with zipfile.ZipFile(io.BytesIO(raw_zip)) as z:
        netcdfs=[k for k in z.namelist() if k.lower().endswith((".nc",".nc4")) and not k.endswith("/")]
        if len(netcdfs)!=1:
            raise ValueError("STAGE108_CDS_ONE_VARIABLE_PER_OFFICIAL_DAILY_ZIP_EXPECTED")
        member=netcdfs[0]
        info=z.getinfo(member)
        if info.file_size>MAX_ORIGINAL_DOWNLOAD_BYTES:
            raise ValueError("STAGE108_CDS_SMALL_SOURCE_NETCDF_UNPACKED_TOO_LARGE")
        raw=z.read(member)
    with tempfile.TemporaryDirectory(prefix="stage108_authentic_cds_") as d:
        loc=Path(d)/"source.nc"
        loc.write_bytes(raw)
        with xr.open_dataset(loc,decode_times=True,mask_and_scale=True) as dataset:
            axis={
              "time":_coordinate_name(dataset,COORD_TIME),
              "latitude":_coordinate_name(dataset,COORD_LAT),
              "longitude":_coordinate_name(dataset,COORD_LON)}
            days=_time_days(dataset[axis["time"]])
            name,var=_variable(dataset,kind,axis)
            compact=var.transpose(axis["time"],axis["latitude"],axis["longitude"])
            lat=np.asarray(dataset[axis["latitude"]].values,float)
            lon=np.asarray(dataset[axis["longitude"]].values,float)
            source=np.asarray(compact.values,float)
            if source.shape!=(31,len(lat),len(lon)):
                raise ValueError("STAGE108_SOURCE_NETCDF_TIMEGRID_SHAPE_DRIFT")
            mapped={}
            for (la,lo),land_km2 in expected_locations.items():
                latselect=np.where(np.abs(lat-la)<1e-6)[0]
                mapped_lons=np.where(np.abs(((lon-lo+180)%360)-180)<1e-6)[0]
                if len(latselect)!=1 or len(mapped_lons)!=1:
                    raise ValueError("STAGE108_ORIGINAL_WDC_AREA_WEIGHT_025_CELL_MISSING_IN_CDS")
                data=source[:,int(latselect[0]),int(mapped_lons[0])]
                if np.any(~np.isfinite(data)):
                    raise ValueError("STAGE108_MISSING_CLIMATE_AT_INTERSECTING_MAINLAND_CELL")
                if (kind=="gust" and (np.any(data<0) or np.any(data>150))) or (
                    kind=="temperature" and (np.any(data<180) or np.any(data>350))):
                    raise ValueError("STAGE108_SOURCE_CLIMATE_PHYSICALLY_IMPLAUSIBLE")
                mapped[f"{la:.6f},{lo:.6f}"]={
                   "latitude":la,"longitude":lo,"source_area_km2":land_km2,
                   "daily":data.tolist()}
            original_attrs={
              "dataset_dimensions":{name:int(size) for name,size in dataset.sizes.items()},
              "variable_name":name,"source_native_units":str(var.attrs.get("units","")),
              "source_native_long_name":str(var.attrs.get("long_name",""))[:160],
              "original_CDS_daily_dates":len(days),
              "original_CDS_latitude_grid_count":len(lat),
              "original_CDS_longitude_grid_count":len(lon),
              "original_NetCDF_member":member}
    return mapped,original_attrs

def validate_199101_original_small_pilot(gust,temp,weights):
    if set(gust)!=set(temp) or len(gust)!=len(weights):
        raise ValueError("STAGE108_CDS_GUST_TEMP_OR_MAINLAND_WEIGHT_CELL_MISMATCH")
    included=[]
    for key in sorted(gust):
        g=np.asarray(gust[key]["daily"],float)
        t=np.asarray(temp[key]["daily"],float)
        if len(g)!=31 or len(t)!=31:
            raise ValueError("STAGE108_CDS_199101_NOT_31_DAYS")
        included.append({
          "ERA5_cell_coordinate":key,
          "original_mainland_intersection_km2":float(gust[key]["source_area_km2"]),
          "original_1991_Jan_daily_max_10fg_above_15_days":int(np.sum(g>15)),
          "original_1991_Jan_daily_max_gust_mean_m_s":float(np.mean(g)),
          "original_1991_Jan_daily_mean_t2m_mean_C":float(np.mean(t)-273.15)})
    frac=sum(r["original_1991_Jan_daily_max_10fg_above_15_days"]/31*
         r["original_mainland_intersection_km2"] for r in included)/sum(
         r["original_mainland_intersection_km2"] for r in included)
    return {
       "source_original_month":"1991-01",
       "source_exact_31_Jan_days_per_cell":True,
       "source_original_region_CDS_area_weighted_Jan_only_gust15_fraction":frac,
       "source_two_original_mainland_cell_monthly_summaries":included,
       "source_NOT_1991_2020_flowering_month_gust_climatology":True,
       "source_NO_flower_cue_response_or_selection_estimated":True}

def category_from_CDS_exception(exc):
    """Output only broad failure category, NEVER the secret or raw exception."""
    s=str(exc).casefold()
    if any(x in s for x in ("licence","license","terms of use","agreement")):
        return "DATASET_TERMS_NOT_YET_ACCEPTED_OR_LICENCE_REJECTED"
    if any(x in s for x in ("401","403","unauthorized","forbidden","permission")):
        return "PERSONAL_TOKEN_AUTHORIZATION_OR_LICENCE_GATE"
    if any(x in s for x in ("429","queue","rate limit","too many requests")):
        return "CDS_PROVIDER_QUOTA_OR_QUEUE"
    if any(x in s for x in ("invalid request","bad request","400","unknown variable")):
        return "OFFICIAL_DATASET_REQUEST_SCHEMA_REJECTED"
    if any(x in s for x in ("connection","timeout","ssl","network")):
        return "CDS_TRANSPORT_FAILURE"
    return "CDS_SOURCE_ERROR_NEEDS_AUTHORIZED_LOG_REVIEW"

def run(original_geo,outdir,enable_retrieve=False):
    weights,req=exact_stage106_source(original_geo)
    outdir.mkdir(parents=True,exist_ok=True)
    token=os.environ.get("CDSAPI_KEY","").strip()
    receipt={
       "schema":"stage108_official_CDS_daily_10fg_and_2mt_auth_source_1991_January_WDC",
       "official_source_CDS_dataset":CDS_DATASET,
       "source_stage106_original_geometry_ZIP_SHA256":SOURCE_STAGE106_SHA,
       "small_original_region":SOURCE_TDWG,
       "source_true_mainland_landcell_count":len(weights),
       "official_original_199101_source_requests":req,
       "original_CDS_personal_access_token_present":bool(token),
       "original_CDS_dataset_licence_acceptance_checked_by_account":False,
       "actual_official_CDS_download_successful":False,
       "source_1991_Jan_month_only_NOT_1991_2020_full_baseline":True,
       "never_report_1991_Jan_as_climatological_flowering_month_exposure":True,
       "no_flower_community_or_pollinator_data_opened":True,
       "climate_variable_10fg_is_a_gust_not_mean_wind":True,
       "auth_source_NOT_OpenMeteo_point_proxy":True}
    target=outdir/"stage108_official_CDS_199101_auth_gate_and_source_receipt.json"
    if not enable_retrieve:
        receipt["status"]="SOURCE_CONTRACT_ONLY_NO_REQUEST_SENT"
        target.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        print("STAGE108_OFFICIAL_CDS_CONTRACT_ONLY",{
           "WDC_cells":len(weights),"requests":sorted(req)})
        return receipt
    if not token:
        receipt["status"]="BLOCKED_NO_EXISTING_CDS_PERSONAL_ACCESS_TOKEN"
        target.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        print("STAGE108_OFFICIAL_CDS_AUTH_GATE",receipt["status"],flush=True)
        return receipt
    try:
        import cdsapi
        client=cdsapi.Client(url=CDS_URL,key=token,quiet=True,progress=False,
                             verify=True,timeout=180)
        collected={};sources={}
        for kind in ("gust","temperature"):
            output=outdir/("stage108_original_CDS_199101_"+kind+".zip")
            print("STAGE108_AUTHENTIC_ORIGINAL_CDS_199101_SUBMIT",kind,flush=True)
            client.retrieve(CDS_DATASET,req[kind],str(output))
            if not output.is_file() or output.stat().st_size<100:
                raise ValueError("STAGE108_NO_AUTHENTIC_OFFICIAL_CDS_NETCDF_ZIP_OUTPUT")
            data,metadata=inspect_original_cds_netcdf_bytes(
                output.read_bytes(),kind,weights)
            sources[kind]={
               "actual_original_CDS_response_zip_SHA256":sha256(output),
               "source_NetCDF_schema":metadata,
               "source_original_postprocessed_1hourly_daily":TYPES[kind][1]}
            collected[kind]=data
            output.unlink()  # Do not upload large raw response data as artifact.
        weather=validate_199101_original_small_pilot(collected["gust"],collected["temperature"],weights)
        receipt["status"]="SUCCESS_OFFICIAL_CDS_TWO_VARIABLE_ORIGINAL_199101"
        receipt["actual_official_CDS_download_successful"]=True
        receipt["original_CDS_dataset_licence_acceptance_checked_by_account"]=True
        receipt["original_CDS_responses"]=sources
        receipt["199101_original_CDS_area_weighted_diagnostic_ONLY"]=weather
        print("STAGE108_REAL_ORIGINAL_CDS_199101_TWO_VARIABLE_GUST_TEMP",
          json.dumps({"WDC_original_source_cells":len(weights),
              "Jan_1991_gust_above15_fraction":weather["source_original_region_CDS_area_weighted_Jan_only_gust15_fraction"],
              "no_1991_2020_full_period_climate":True},sort_keys=True),flush=True)
    except Exception as exc:
        receipt["status"]="BLOCKED_AUTHENTIC_CDS_SOURCE_DOWNLOAD_OR_SCHEMA"
        receipt["safe_failure_classification"]=category_from_CDS_exception(exc)
        target.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
        print("STAGE108_CDS_FAIL_CLOSED",receipt["safe_failure_classification"],flush=True)
        raise RuntimeError("STAGE108_NO_VERIFIED_CDS_CLIMATE_SOURCE") from None
    finally:
        # Delete any partially downloaded raw climate not part of derived
        # artifact; never touch PAT or log its value.
        for kind in TYPES:
            q=outdir/("stage108_original_CDS_199101_"+kind+".zip")
            if q.exists():q.unlink()
    target.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage106-grid-area-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    p.add_argument("--retrieve-if-authorized",action="store_true")
    a=p.parse_args()
    run(a.original_Stage106_grid_area_ZIP,a.outdir,a.retrieve_if_authorized)
