"""Stage77A: independent WorldClim 2.1 WIND/CLIMATE × observed floral guild macro sites.

ORIGINAL SOURCES
- Corrected EuPPollNet v1.3.0, 623476 real visitor records from 54
  independent original publications and 1864 study×network×year keys.
- WorldClim 2.1 1970–2000 10 arc-minute monthly climate NORMALS:
  12 layers of wind speed, average temperature, precipitation, solar
  radiation and water vapour pressure, original UC Davis GeoTIFFs.
  Dataset values are climatically interpolated long-term BACKGROUND;
  they are NOT wind at the actual flower/bee visit or odor-plume forcing.
- NHM source lexical visible floral trait definitions from Stage75
  are joined only in separate Stage77B *after* climate source audit.

No island data. No plant nativeness or 2021 UV one-species experiments.
No false site absence from absent visitor or visit month.
No source scent VOC same-site data across 54 studies, hence VOC mediation
path is mathematically NOT IDENTIFIED and must never be fitted.
"""
from __future__ import annotations
import argparse,csv,datetime,hashlib,io,json,math,re,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path

import numpy as np
from rasterio.io import MemoryFile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_literature_macro_stage69"))
from ingest_original_corrected_EuPPollNet_network_NHM_spectra import (
    fetch_original,dict_rows,year_of,guild_of,is_species,EXPECTED_INTERACTIONS
)

SOURCE_TAG="joseblanuza/EuPPollNet@v1.3.0"
SOURCE_NETWORKS=1864
SOURCE_STUDIES=54
CLIMATE_PERIOD="1970-2000"
SOURCE="https://geodata.ucdavis.edu/climate/worldclim/2_1/base/"
CLIMATE_VARS={
    "wind":"mean_wind_speed_m_s", "tavg":"mean_temperature_C",
    "prec":"mean_precipitation_mm_month",
    "vapr":"mean_water_vapour_pressure_kPa",
    "srad":"mean_solar_radiation_kJ_m2_day"
}
MONTH_FILE=re.compile(r"_([01]?\d)\.tif$",re.I)
ISO_DATE=re.compile(r"^\s*((?:19|20)\d{2})[-/]([01]?\d)(?:[-/]([0-3]?\d))?(?:[T\s].*)?\s*$")
NUM_DATE=re.compile(r"^\s*([0-3]?\d)/([0-3]?\d)/((?:19|20)\d{2})(?:\s.*)?$")
WIND_MIN=0
WIND_MAX=45

def hash_stream(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def original_month(value):
    s=str(value or "").strip()
    m=ISO_DATE.fullmatch(s)
    if m:
        year,mon,day=map(lambda x:int(x) if x else None,m.groups())
        if mon is None or not 1<=mon<=12:return None,"INVALID_MONTH"
        if day is not None:
            try:datetime.date(year,mon,day)
            except ValueError:return None,"INVALID_DATE"
        return mon,"DIRECT_YEAR_FIRST"
    m=NUM_DATE.fullmatch(s)
    if m:
        left,right,year=map(int,m.groups())
        # Preserve ambiguity! 04/05/YYYY is NOT automatically April or May.
        if 1<=left<=12 and 1<=right<=12:return None,"AMBIGUOUS_DAY_MONTH"
        if 12<left<=31 and 1<=right<=12:
            try:datetime.date(year,right,left)
            except ValueError:return None,"INVALID_DATE"
            return right,"DAY_FIRST_UNAMBIGUOUS"
        if 1<=left<=12 and 12<right<=31:
            try:datetime.date(year,left,right)
            except ValueError:return None,"INVALID_DATE"
            return left,"MONTH_FIRST_UNAMBIGUOUS"
        return None,"INVALID_DATE"
    return None,"UNKNOWN_SOURCE_DATE_FORMAT"

def safe_coord(v,limit):
    try:x=float(v)
    except (TypeError,ValueError):return None
    return round(x,7) if math.isfinite(x) and -limit<=x<=limit else None

def source_network_sites():
    original=fetch_original("Interaction_data.csv.gz")
    coord=defaultdict(set)
    months=defaultdict(set)
    month_status=Counter()
    raw_examples=[]
    visits=defaultdict(Counter)
    raw_guild=defaultdict(Counter)
    study=set()
    n=0
    for r in dict_rows(original,compressed=True):
        n+=1
        k=(r["Study_id"].strip(),r["Network_id"].strip(),year_of(r["Date"]))
        study.add(k[0])
        la=safe_coord(r.get("Latitude"),90)
        lo=safe_coord(r.get("Longitude"),180)
        if la is not None and lo is not None:coord[k].add((la,lo))
        else:coord[k]  # retain source key even with missing coords
        mon,status=original_month(r["Date"])
        month_status[status]+=1
        if mon is not None:months[k].add(mon)
        elif len(raw_examples)<16 and r["Date"] not in raw_examples:
            raw_examples.append(r["Date"])
        raw_guild[k][guild_of(r)]+=1
        if not is_species(r):continue
        if r.get("Pollinator_rank","").strip().casefold()!="species":continue
        if r.get("Pollinator_unsure_id","").strip().casefold() in {"yes","true","1","y"}:continue
        guild=guild_of(r)
        if guild=="Bombus":visits[k]["B"]+=1
        elif guild=="other_bee":visits[k]["O"]+=1
    if n!=EXPECTED_INTERACTIONS or len(coord)!=SOURCE_NETWORKS or len(study)!=SOURCE_STUDIES:
        raise ValueError("STAGE77_NOT_CORRECTED_ORIGINAL_623476_1864_54_SOURCE")
    return coord,months,visits,raw_guild,{
        "source_original_record_count":n,
        "source_real_unique_study_network_year_keys":len(coord),
        "source_real_unique_original_publication_IDs":len(study),
        "original_source_date_parse_record_status":dict(month_status),
        "original_unresolved_source_Date_examples_not_interpreted":raw_examples,
        "source_networks_with_unique_coordinate":sum(len(v)==1 for v in coord.values()),
        "source_networks_with_multiple_source_coordinates":sum(len(v)>1 for v in coord.values()),
        "source_networks_with_at_least_one_unambiguous_observed_month":sum(bool(months.get(k)) for k in coord),
        "source_visit_positive_months_not_true_flowering_time_without_visits":True,
    }

def archive_tiff_members(z,variable):
    tif=[s for s in z.namelist() if s.lower().endswith(".tif")]
    result={}
    for name in tif:
        match=MONTH_FILE.search(name)
        if match is None:raise ValueError("STAGE77_CLIMATE_TIFF_MONTH_FILENAME_NOT_RECOGNIZED")
        mon=int(match.group(1))
        if not 1<=mon<=12 or mon in result:
            raise ValueError("STAGE77_CLIMATE_ARCHIVE_MONTH_DUPLICATED_OR_INVALID")
        result[mon]=name
    if set(result)!=set(range(1,13)):
        raise ValueError(f"STAGE77_WORLDCLIM_12_MONTHS_NOT_AVAILABLE_{variable}")
    return result

def validate_sample(var,x):
    if not math.isfinite(x):return None
    if var=="wind" and not WIND_MIN<=x<=WIND_MAX:
        return None
    if var=="tavg" and not -75<=x<=65:return None
    if var=="prec" and not 0<=x<=6000:return None
    if var=="vapr" and not 0<=x<=10:return None
    if var=="srad" and not 0<=x<=60000:return None
    return x

def retrieve_source_worldclim(points,dir_path):
    if not points:return {},{}
    source={}
    for var in CLIMATE_VARS:
        f=dir_path/f"wc2.1_10m_{var}.zip"
        if not f.is_file() or f.stat().st_size<100000:
            raise ValueError("STAGE77_WORLDCLIM_SOURCE_MISSING_OR_FAKE_"+var)
        source[var]={"original_public_10m_zip_sha256":hash_stream(f),
                     "actual_source_zip_bytes":f.stat().st_size,
                     "provider_URL":SOURCE+f.name}
    result={k:{var:{} for var in CLIMATE_VARS} for k in points}
    ordered=sorted(points)
    loc=[(lon,lat) for lat,lon in ordered]
    nodata=Counter()
    resolution={}
    for var in CLIMATE_VARS:
        path=dir_path/f"wc2.1_10m_{var}.zip"
        with zipfile.ZipFile(path) as z:
            layer=archive_tiff_members(z,var)
            for month,name in sorted(layer.items()):
                raw=z.read(name)
                with MemoryFile(raw) as mem,mem.open() as ds:
                    if len(ds.indexes)!=1 or ds.count!=1:
                        raise ValueError("STAGE77_CLIMATE_GEOTIFF_NOT_SINGLE_BAND")
                    if ds.crs is None or ds.crs.to_epsg()!=4326:
                        raise ValueError("STAGE77_SOURCE_WORLDCLIM_NOT_EPSG4326")
                    if ds.res[0]<0.15 or ds.res[0]>0.18:
                        raise ValueError("STAGE77_WORLDCLIM_SOURCE_RESOLUTION_NOT_10_ARCMIN")
                    resolution[var]=list(ds.res)
                    # Only read original source coordinate pixels, not
                    # arbitrary interpolation/extrapolation outside land raster.
                    for (latlon,),sample in zip(((p,) for p in ordered),ds.sample(loc,masked=True)):
                        if bool(np.ma.is_masked(sample[0])):
                            nodata[(var,month)]+=1
                            continue
                        value=validate_sample(var,float(sample[0]))
                        if value is None:
                            nodata[(var,month)]+=1
                            continue
                        result[latlon][var][month]=value
    source["_source_summary"]={
      "provider":"WorldClim v2.1, original UC Davis geodata",
      "source_baseline_period":"1970–2000 long-term 12 calendar-month normals",
      "resolution":"10 arcminutes (~18 km north-south; variable east-west)",
      "source_epsg":"EPSG:4326",
      "source_monthly_geotiff_layers_per_variable":12,
      "source_original_geotiff_raster_resolutions":resolution,
      "source_original_raster_nodata_count_by_month":{
          var+"_"+str(month):count for (var,month),count in sorted(nodata.items())},
      "source_raster_not_visit_date_instantaneous_wind_or_scent_plume":True,
      "source_climate_1970_2000_vs_visit_year_mismatch_not_resolved":True,
      "no_raster_bilinear_fabrication_or_nearest-land-extrapolation":True,
    }
    return result,source

def mean(values):
    return sum(values)/len(values) if values else None

def site_climate_table(coords,months,bees,raw_guild,rasters):
    out=[];aud=Counter()
    for study,network,year in sorted(coords):
        key=(study,network,year)
        sites=coords[key]
        actual_months=sorted(months.get(key,set()))
        if len(sites)==1:
            lat,lon=next(iter(sites))
            d=rasters.get((lat,lon),{})
        else:
            lat=lon=None;d={}
        r={"Study_id":study,"Network_id":network,"Year":year,
           "Latitude_original":lat if lat is not None else "",
           "Longitude_original":lon if lon is not None else "",
           "source_network_original_distinct_coordinate_count":len(sites),
           "source_observed_visit_months":",".join(str(m) for m in actual_months),
           "source_unique_observed_visit_months":len(actual_months),
           "source_seasonal_month_identified":int(bool(actual_months)),
           "source_actual_strict_species_rank_Bombus_records":bees.get(key,Counter()).get("B",0),
           "source_actual_strict_species_rank_other_bees_records":bees.get(key,Counter()).get("O",0),
           "source_observed_no_Bombus_not_biological_absence":True}
        B=r["source_actual_strict_species_rank_Bombus_records"];O=r["source_actual_strict_species_rank_other_bees_records"]
        r["source_Bombus_fraction_of_recorded_identified_bees"]=B/(B+O) if B+O else ""
        r["source_Bombus_fraction_is_realized_visit_composition_not_receiver_range"]=True
        all_present=True
        seasonal_present=bool(actual_months)
        for var,col in CLIMATE_VARS.items():
            full=d.get(var,{})
            annual=[full[m] for m in range(1,13) if m in full]
            season=[full[m] for m in actual_months if m in full]
            r["WorldClim1970_2000_annual_"+col]=mean(annual) if len(annual)==12 else ""
            r["WorldClim1970_2000_observed_month_"+col]=mean(season) if len(season)==len(actual_months) and season else ""
            r["WorldClim1970_2000_valid_months_"+var]=len(full)
            all_present&=(len(annual)==12)
            seasonal_present&=(len(season)==len(actual_months) and bool(season))
        r["full_5variable_annual_climate_admitted"]=int(all_present)
        r["full_5variable_visit_month_climate_admitted"]=int(seasonal_present)
        aud["source_all_networks"]+=1
        aud["networks_with_unique_coordinate"]+=(len(sites)==1)
        aud["networks_with_5climate_annual"]+=all_present
        aud["networks_with_5climate_visit_month"]+=seasonal_present
        aud["networks_with_strict_bee_records"]+=B+O>0
        out.append(r)
    return out,dict(aud)

def save_csv(path,rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run(worldclim_dir):
    coords,months,bees,raw_guild,original=source_network_sites()
    unique={next(iter(pts)) for pts in coords.values() if len(pts)==1}
    climatic,meta=retrieve_source_worldclim(unique,worldclim_dir)
    rows,coverage=site_climate_table(coords,months,bees,raw_guild,climatic)
    report={
      "schema":"stage77a_actual_original_1864_EuPPollNet_site_climatological_wind_T_prec_vapr_srad",
      "source_corrected_EuPPollNet_release":SOURCE_TAG,
      "source_corrected_plant_visitation_record_count":EXPECTED_INTERACTIONS,
      "source_study_network_year_count":SOURCE_NETWORKS,
      "source_source_study_ID_count":SOURCE_STUDIES,
      "original_pollinator_month_and_geography_audit":original,
      "original_WorldClim_source_zip_manifest":meta,
      "site_climate_coverage":coverage,
      "climate_is_longterm_normal_NOT_coincident_original_visit_weather":True,
      "site_climatological_wind_is_NOT_actual_odor_turbulence_or_plume":True,
      "visual_trait_not_imputed_from_climate_or_photo":True,
      "VOC_emissions_and_same_site_scent_not_measured_here":True,
      "nonrecorded_guild_not_ecological_zero":True,
      "causal_visual_scent_wind_path_or_mediation_fitted":False,
      "climate_effects_on_Bombus_vs_flower_colour_estimated":False,
      "source_original_1950_2025_weather_not_claimed":True,
    }
    return rows,report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--worldclim-source-dir",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    a.outdir.mkdir(exist_ok=True,parents=True)
    rows,report=run(a.worldclim_source_dir)
    save_csv(a.outdir/"original_1864_network_sites_worldclim_wind_climate_normals.csv",rows)
    (a.outdir/"original_source_WorldClim_wind_climate_1864_site_matching_receipt.json").write_text(
        json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("STAGE77A_REAL_SOURCE_1864_BOMBUS_FIELD_NETWORKS_WORLDCLIM_WIND",json.dumps(report,sort_keys=True))
    print("NO_SAME_DAY_WIND_NO_VOC_MEDIATION_NO_SPECTRAL_UV_IMPUTATION")
if __name__=="__main__":
    main()
