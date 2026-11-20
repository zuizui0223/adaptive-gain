#!/usr/bin/env python3
"""Stage106: source original TDWG3 × NaturalEarth mainland ERA5 0.25° area weights.

ERA5 CDS daily statistics product is **derived from original hourly ERA5**,
not a substitute for regular 10m wind speed or Open-Meteo model point samples.
Scientific source requests:
  dataset: derived-era5-single-levels-daily-statistics
  10m_wind_gust_since_previous_post_processing: daily_max from 1_hourly
  2m_temperature: daily_mean from 1_hourly
  time_zone utc+00:00
Monthly climatological 1991–2020 daily 2m mean >5 C; eligible days have
gust daily max strictly >15 m/s. Per original 0.25° land grid cell, calculate
fraction of eligible days; regional exposure = geodesic mainland land-intersect
area-weighted mean of cell fractions. No flowers/bee/outcomes are opened.

This PRE-FLIGHT computes REAL source land×grid cell weights and exact CDS
request plans for 3 *smallest area* original continent-connected mainland
regions selected by frozen geometry only. It does NOT download CDS climate
without independently accepted CDS licence & secret. Thus no actual
125-region area-weighted ERA5 gust coefficient is claimed at Stage106.
"""
from __future__ import annotations
import argparse,csv,datetime,hashlib,io,json,math,sys,zipfile
from collections import Counter
from pathlib import Path

import numpy as np
from shapely.geometry import box
from shapely.ops import unary_union

BASE=Path(__file__).resolve().parents[1]
for folder in ("floral_macro_stage87","floral_macro_stage94"):
    sys.path.insert(0,str(BASE/folder))
from aggregate_global_tdwg3_worldclim_wind import source_polygons,TDWG_GIT_BLOB_SHA1
from original_tdwg_naturalearth_strict_mainland import (
    original_natural_earth_land,area_km2,NATURAL_EARTH_LAND_ZIP_SHA256)

SOURCE_STAGE94_GEO_SHA="3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833"
SOURCE_GEO_MEMBER="stage94_original_367_mainland_island_mixed_registry.csv"
CDS_DATASET="derived-era5-single-levels-daily-statistics"
CDS_GRID_DEGREES=0.25
PRIMARY_GUST=15.0
FLOWERING_T_C=5.0

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def gitblob(path):
    p=Path(path).read_bytes()
    return hashlib.sha1(("blob "+str(len(p))+"\0").encode()+p).hexdigest()

def source_mainland_registry(source_zip):
    if sha256(source_zip)!=SOURCE_STAGE94_GEO_SHA:
        raise ValueError("STAGE106_ORIGINAL_STAGE94_MAINLAND_SOURCE_SHA_MISMATCH")
    with zipfile.ZipFile(source_zip) as z:
        if SOURCE_GEO_MEMBER not in z.namelist():
            raise ValueError("STAGE106_SOURCE_GEO_MEMBER_NOT_FOUND")
        rows=list(csv.DictReader(io.StringIO(z.read(SOURCE_GEO_MEMBER).decode("utf-8-sig"))))
    if len(rows)!=367 or len({r["TDWG_L3"] for r in rows})!=367:
        raise ValueError("STAGE106_ORIGINAL_TDWG3_REGION_SET_NOT_367")
    mainland=[r for r in rows if r["land_scope"]=="mainland"]
    if len(mainland)!=125:
        raise ValueError("STAGE106_NOT_STRICT_MAINLAND125_SOURCE_COHORT")
    return rows,sorted(mainland,key=lambda r:(float(r["estimated_mainland_land_km2"]),r["TDWG_L3"]))

def cds_daily_request(variable,stat,year,month,area):
    """Canonical official Copernicus CDS API product schema; not a submission."""
    if (variable,stat) not in (
        ("10m_wind_gust_since_previous_post_processing","daily_max"),
        ("2m_temperature","daily_mean")):
        raise ValueError("STAGE106_INCORRECT_SOURCE_VARIABLE_OR_STATISTIC")
    north,west,south,east=area
    if not (-90<=south<north<=90 and -180<=west<east<=180):
        raise ValueError("STAGE106_CDS_AREA_NOT_VALID_WGS84_NON_DATELINE")
    if not (1991<=year<=2020 and 1<=month<=12):
        raise ValueError("STAGE106_REQUEST_OUTSIDE_PINNED_CLIMATOLOGY")
    from calendar import monthrange
    return {"product_type":"reanalysis",
        "variable":[variable],"year":str(year),
        "month":[f"{month:02d}"],
        "day":[f"{i:02d}" for i in range(1,monthrange(year,month)[1]+1)],
        "daily_statistic":stat,"time_zone":"utc+00:00",
        "frequency":"1_hourly",
        "area":[round(float(z),5) for z in area]}

def index_grid_for_source_bbox(land_region,res=CDS_GRID_DEGREES):
    minx,miny,maxx,maxy=land_region.bounds
    if minx<-179 or maxx>179:
        raise ValueError("STAGE106_SOURCE_GRID_ANTIMERIDIAN_HANDLING_NOT_VERIFIED")
    lon=np.arange(math.floor((minx-res/2)/res)*res,
                  math.ceil((maxx+res/2)/res)*res+res*.1,res)
    lat=np.arange(math.floor((miny-res/2)/res)*res,
                  math.ceil((maxy+res/2)/res)*res+res*.1,res)
    lon=np.round(lon,6);lat=np.round(lat,6)
    lat=lat[(lat>=-90)&(lat<=90)];lon=lon[(lon>=-180)&(lon<=180)]
    if len(lat)*len(lon)>200000:
        raise ValueError("STAGE106_PREVIEW_REGION_GRID_IMPLAUSIBLY_LARGE")
    return lat,lon

def gridcell_land_area_weights(source_mainland_region,lat,lon,res=CDS_GRID_DEGREES):
    """Exact geometry intersection with original mainland land, geodesic m².

    Returns km² of each source 0.25° grid CELL inside the region's mainland
    physically connected landmass, not boolean cell-centre land mask.
    """
    if res<=0:raise ValueError("STAGE106_RESOLUTION_NOT_POSITIVE")
    LATS=np.asarray(lat,dtype=float);LONS=np.asarray(lon,dtype=float)
    if LATS.ndim!=1 or LONS.ndim!=1 or not len(LATS) or not len(LONS):
        raise ValueError("STAGE106_GRID_COORDINATES_MALFORMED")
    if np.any(np.diff(LATS)<=0) or np.any(np.diff(LONS)<=0):
        raise ValueError("STAGE106_COORDINATES_NOT_ASCENDING")
    if np.any(np.abs(np.diff(LATS)-res)>1e-6) or np.any(np.abs(np.diff(LONS)-res)>1e-6):
        raise ValueError("STAGE106_GRID_COORDINATE_SPACING_NOT_025")
    if source_mainland_region.is_empty or not source_mainland_region.is_valid:
        raise ValueError("STAGE106_ORIGINAL_MAINLAND_SOURCE_GEOMETRY_INVALID")
    weights=np.zeros((len(LATS),len(LONS)),float)
    for i,la in enumerate(LATS):
        for j,lo in enumerate(LONS):
            geom=box(lo-res/2,max(-90,la-res/2),lo+res/2,min(90,la+res/2))
            if not source_mainland_region.intersects(geom):continue
            weights[i,j]=area_km2(source_mainland_region.intersection(geom))
    return weights

def gridded_warmmonth_gust_climatology(times,gust,temperature_K,land_weights_km2,
                                        gust_units="m/s",temperature_units="K"):
    """Per grid cell 1991–2020 true daily max gust, then regional area average."""
    d=np.asarray(times,dtype="datetime64[D]")
    if (gust_units!="m/s" or temperature_units!="K"):
        raise ValueError("STAGE106_ERA5_SOURCE_UNITS_MUST_BE_MS_AND_K")
    expected=np.arange(np.datetime64("1991-01-01"),np.datetime64("2021-01-01"),
                       dtype="datetime64[D]")
    if d.shape!=expected.shape or not np.array_equal(d,expected):
        raise ValueError("STAGE106_1991_2020_DATE_SEQUENCE_NOT_COMPLETE")
    G=np.asarray(gust,float)
    T=np.asarray(temperature_K,float)-273.15
    W=np.asarray(land_weights_km2,float)
    if G.shape!=T.shape or G.shape[0]!=len(expected) or G.shape[1:]!=W.shape:
        raise ValueError("STAGE106_SOURCE_DAILY_TIME_SPACE_SHAPE_MISMATCH")
    if np.any(~np.isfinite(W)) or np.any(W<0) or W.sum()<=0:
        raise ValueError("STAGE106_NO_VALID_MAINLAND_SOURCE_AREA_WEIGHTS")
    months=(d.astype("datetime64[M]").astype(int)%12+1).astype(int)
    N=G.shape[1]*G.shape[2]
    flat_g=G.reshape(len(d),N)
    flat_t=T.reshape(len(d),N)
    flat_w=W.ravel()
    valid=(np.isfinite(flat_g).all(axis=0)&np.isfinite(flat_t).all(axis=0)
           &(flat_g>=0).all(axis=0))
    weighted_weather_coverage=flat_w[valid].sum()/flat_w.sum()
    if weighted_weather_coverage<0.95:
        raise ValueError("STAGE106_NOT_95PCT_LAND_AREA_WITH_COMPLETE_ORIGINAL_DAILY_GRID")
    valid=valid&(flat_w>0)
    cell_fraction=np.full(N,np.nan)
    eligible_days=np.zeros(N,dtype=int)
    eligible_months=np.zeros(N,dtype=int)
    for k in np.flatnonzero(valid):
        warm=np.zeros(12,bool)
        for m in range(1,13):
            warm[m-1]=float(np.mean(flat_t[months==m,k]))>FLOWERING_T_C
        selected=warm[months-1]
        eligible_months[k]=sum(warm)
        eligible_days[k]=sum(selected)
        if selected.any():
            cell_fraction[k]=float(np.mean(flat_g[selected,k]>PRIMARY_GUST))
    available=valid&np.isfinite(cell_fraction)
    value=(float(np.dot(flat_w[available],cell_fraction[available])/flat_w[available].sum())
           if np.any(available) else None)
    return {
       "source_1991_2020_strict_10m_daily_gust_gt_15_fraction_area_weighted":value,
       "source_landarea_total_km2":float(flat_w.sum()),
       "source_weather_complete_area_fraction":float(weighted_weather_coverage),
       "source_flowering_month_eligible_area_fraction":float(flat_w[available].sum()/flat_w.sum()),
       "source_eligible_day_count_min":int(eligible_days[available].min()) if np.any(available) else None,
       "source_eligible_day_count_max":int(eligible_days[available].max()) if np.any(available) else None,
       "source_cellcount_with_positive_landarea":int(np.sum(flat_w>0)),
       "source_cellcount_with_warm_months_and_valid_weather":int(available.sum()),
       "source_area_weighted_cell_fraction_NOT_original_CDS_retrieval_here":True,
       "source_ERA5_hourly_daily_max_gust_gt_15_strict":True,
       "source_ERA5_daily_t2m_mean_climatological_month_gt_5C_strict":True,
    }

def run(stage94_geo,tdwg_original,original_naturalearth_land,out):
    registry,qualified=source_mainland_registry(stage94_geo)
    if gitblob(tdwg_original)!=TDWG_GIT_BLOB_SHA1:
        raise ValueError("STAGE106_ORIGINAL_TDWG_GIT_BLOB_DRIFT")
    regions,invalid,_=source_polygons(tdwg_original)
    parts,main,ne_meta=original_natural_earth_land(original_naturalearth_land)
    mainland=unary_union([parts[i] for i in sorted(main)])
    choices=qualified[:3]
    rows=[];regionsummary=[];requests=[]
    for target in choices:
        code=target["TDWG_L3"];shape=regions[code]
        original_land=shape.intersection(mainland)
        if original_land.is_empty:
            raise ValueError("STAGE106_SOURCE_MAINLAND_REGION_LAND_INTERSECTION_ZERO")
        lat,lon=index_grid_for_source_bbox(original_land)
        weights=gridcell_land_area_weights(original_land,lat,lon)
        real_area=area_km2(original_land)
        grid_area=weights.sum()
        if not (.985<=grid_area/real_area<=1.015):
            raise ValueError("STAGE106_GRIDCELL_AREA_INTEGRATION_VS_POLYGON_SOURCE_MISMATCH_"+code)
        nonzero=weights[weights>0]
        max_weight=nonzero.max()
        neff=float(nonzero.sum()**2/np.sum(nonzero**2))
        region_bbox=(min(90,round(float(lat.max()+0.25),5)),
                     max(-180,round(float(lon.min()-0.25),5)),
                     max(-90,round(float(lat.min()-0.25),5)),
                     min(180,round(float(lon.max()+0.25),5)))
        for name,stat in [
              ("10m_wind_gust_since_previous_post_processing","daily_max"),
              ("2m_temperature","daily_mean")]:
            requests.append({"TDWG_L3":code,"dataset":CDS_DATASET,
               "variable_source":name,"statistic":stat,
               "one_month_source_probe_request_NOT_SUBMITTED":
                    cds_daily_request(name,stat,1991,1,region_bbox)})
        for i,la in enumerate(lat):
            for j,lo in enumerate(lon):
                if weights[i,j]<=0:continue
                rows.append({"TDWG_L3":code,"ERA5_atmosphere_source_grid_latitude":la,
                   "ERA5_atmosphere_source_grid_longitude":lo,
                   "source_intersected_original_mainland_land_km2":round(float(weights[i,j]),8),
                   "source_region_original_TDWG_polygon_SHA256":target["polygon_sha256"]})
        regionsummary.append({"TDWG_L3":code,
           "selection":"three_lowest_original_source_mainland_land_area_TDWG3",
           "real_original_mainland_region_land_km2":real_area,
           "source_original_ERA5_grid_area_km2":float(grid_area),
           "area_ratio":float(grid_area/real_area),
           "source_nonzero_land_grid_cells":len(nonzero),
           "source_effective_spatial_grid_cells_Neff":neff,
           "source_regional_wind_fraction_HAS_NOT_BEEN_CALCULATED":"YES"})
    out.mkdir(parents=True,exist_ok=True)
    with (out/"stage106_original_three_mainland_regions_ERA5_025deg_cell_landarea_weights.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    receipt={
       "schema":"stage106_verified_source_TDWG3_land_geom_ERA5_025deg_area_weights_NO_climate",
       "source_original_TDWG_git_blob":TDWG_GIT_BLOB_SHA1,
       "source_original_NaturalEarth_land_SHA256":NATURAL_EARTH_LAND_ZIP_SHA256,
       "source_original_stage94_mainland_regions_source_SHA256":SOURCE_STAGE94_GEO_SHA,
       "CDS_official_dataset":CDS_DATASET,
       "CDS_data_product_is_ERA5_original_hourly_postprocessed_daily_statistics":True,
       "CDS_one_hourly_input_daily_max_10fg_and_daily_mean_2mT_two_separate_calls":True,
       "CDS_original_API_source_request_submitted":False,
       "no_CDS_original_weather_cells_or_climate_wind_outputs_retrieved":True,
       "source_month_1991_01_CDS_request_specs_NOT_submitted":requests,
       "source_three_geometry_only_preflight_regions":regionsummary,
       "source_NaturalEarth_connected_continental_landmass_metadata":ne_meta,
       "actual_area_weights_derived_from_original_source_polygon_intersections":True,
       "no_wind_plant_signal_association_fitted":True,
       "source_global_125_region_climatology_NOT_obtained":True}
    (out/"stage106_original_CDS_ERA5_daily_10fg_1991_2020_area_weighting_PRECHECK.json").write_text(
       json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("STAGE106_ACTUAL_ORIGINAL_TDWG_MAINLAND_ERA5_GRID_INTERSECTION_PREFLIGHT",
        json.dumps({"original_geometry_regions":[{"code":r["TDWG_L3"],
            "land_km2":r["real_original_mainland_region_land_km2"],
            "grid_cell_count":r["source_nonzero_land_grid_cells"],
            "N_effective_cells":r["source_effective_spatial_grid_cells_Neff"]}
            for r in regionsummary],"CDS_calls_NOT_submitted":len(requests)},
            sort_keys=True),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage94-geography-ZIP",required=True,type=Path)
    p.add_argument("--original-TDWG-geojson",required=True,type=Path)
    p.add_argument("--original-NaturalEarth-land-ZIP",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.original_Stage94_geography_ZIP,a.original_TDWG_geojson,
        a.original_NaturalEarth_land_ZIP,a.outdir)
