"""Stage87C GLOBAL native floral text geographic ranges × WorldClim wind/T/P.

Input: 367 accepted WCVP TDWG3 native regions with original floral text.
Original WGSRPD/TDWG official geometries, 19 invalid source features repaired
ONLY for explicitly labeled sensitivity (not silently treated as valid).
WorldClim 2.1 10-arc-minute 1970–2000 climate normals: monthly wind m/s,
temperature C, precipitation mm, radiation kJ/m2/day and water vapour pressure
kPa. Area-sampled point means are not exact region-wide raster integrals,
and are *not* gust-at-bee-hour, odour plume or flower-landing wind.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,re,zipfile
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from shapely.geometry import shape,Point
from shapely.validation import make_valid
from rasterio.io import MemoryFile

TDWG_GIT_BLOB_SHA1="91104e5159e31f88154833a51d3b0d1c9271083f"
GEOM_CODES="LEVEL3_COD"
WCVP_REGION_SOURCE_SHA256="f8a84a979db18a7137a125df656cb719a5f864a8111f3babc8eaa9b470b0a2bb"
SAMPLED_PER_SOURCE_REGION=48
CLIMATE_VARIABLES={
 "wind":"worldclim_baseline_wind_m_s",
 "tavg":"worldclim_baseline_mean_temperature_C",
 "prec":"worldclim_baseline_precip_mm_month",
 "srad":"worldclim_baseline_solar_kJ_m2_day",
 "vapr":"worldclim_baseline_vapour_kPa"}
CLIM_BASE="https://geodata.ucdavis.edu/climate/worldclim/2_1/base/"
MONTH=re.compile(r"_([01]?\d)\.tif$",re.I)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def original_blob_sha(raw):
    return hashlib.sha1(("blob "+str(len(raw))+"\0").encode()+raw).hexdigest()

def source_regions(source_csv):
    if sha(source_csv)!=WCVP_REGION_SOURCE_SHA256:
        raise ValueError("STAGE87C_AUTHENTIC_STAGE87A_GLOBAL_NATIVE_REGIONS_CSV_DIGEST_CHANGED")
    with Path(source_csv).open(newline="",encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=367 or len({x["TDWG_L3"] for x in rows})!=367:
        raise ValueError("STAGE87C_ORIGINAL_SOURCE_GLOBAL_367_REGION_COHORT_CHANGED")
    return {r["TDWG_L3"]:r for r in rows}

def source_polygons(path):
    data=Path(path).read_bytes()
    if original_blob_sha(data)!=TDWG_GIT_BLOB_SHA1:
        raise ValueError("STAGE87C_ORIGINAL_TDWG_L3_GIT_SOURCE_SHA_CHANGED")
    features=json.loads(data)["features"]
    geoms=defaultdict(list);invalid=Counter();names={}
    for f in features:
        props=f["properties"]
        code=str(props.get(GEOM_CODES,"")).strip().upper()
        if not code:raise ValueError("STAGE87C_SOURCE_POLYGON_HAS_NO_TDWG3_CODE")
        g=shape(f["geometry"])
        if not g.is_valid:
            invalid[code]+=1
            # Keep the repaired original invalid source geometric form as
            # an explicit sensitivity. No new basemap substitute.
            g=make_valid(g)
        if g.is_empty:continue
        geoms[code].append(g)
        names[code]={k:str(v) for k,v in props.items() if k.endswith("_NAM")}
    if sum(invalid.values())!=19:
        raise ValueError("STAGE87C_TDWG_19_INVALID_ORIGINAL_FEATURES_CHANGED")
    from shapely.ops import unary_union
    merged={k:unary_union(v) for k,v in geoms.items()}
    return merged,invalid,names

def sample_source_region_points(geo):
    samples={};reasons=Counter()
    for code,poly in sorted(geo.items()):
        if poly.is_empty:continue
        p=poly.representative_point()
        xmin,ymin,xmax,ymax=poly.bounds
        if xmax<=xmin or ymax<=ymin:continue
        seed=int(hashlib.sha256(code.encode()).hexdigest()[:16],16)
        rng=np.random.default_rng(seed)
        pointset={(round(p.x,5),round(p.y,5))}
        # Sampling uniformly in longitude/latitude is approximately area-
        # corrected downstream by cos(latitude), not a claim of exact
        # area-weighted raster integral over large or discontinuous regions.
        ntry=0
        while len(pointset)<SAMPLED_PER_SOURCE_REGION and ntry<15000:
            ntry+=1
            lon=float(rng.uniform(xmin,xmax))
            lat=float(rng.uniform(ymin,ymax))
            if poly.contains(Point(lon,lat)):
                pointset.add((round(lon,5),round(lat,5)))
        if len(pointset)<SAMPLED_PER_SOURCE_REGION:
            reasons["regions_below_48_boundary_safe_points"]+=1
        samples[code]=[(lon,lat) for lon,lat in sorted(pointset)]
    return samples,dict(reasons)

def read_months(z):
    files={}
    for filename in z.namelist():
        if not filename.casefold().endswith(".tif"):continue
        x=MONTH.search(filename)
        if x is None:raise ValueError("STAGE87C_WORLDCLIM_TIFF_MONTH_AMBIGUOUS")
        m=int(x.group(1))
        if m in files or not 1<=m<=12:raise ValueError("STAGE87C_WORLDCLIM_DUPLICATED_MONTH")
        files[m]=filename
    if set(files)!=set(range(1,13)):
        raise ValueError("STAGE87C_WORLDCLIM_NOT_FULL_12_MONTH_VARIABLE")
    return files

def validate_climate(var,v):
    if not math.isfinite(v):return False
    return {
      "wind":0<=v<=45,
      "tavg":-75<=v<=65,
      "prec":0<=v<=6000,
      "srad":0<=v<=60000,
      "vapr":0<=v<=10}[var]

def source_climate(samples,dir_):
    sample_keys=[(code,lon,lat) for code,points in sorted(samples.items()) for lon,lat in points]
    coords=[(lon,lat) for _,lon,lat in sample_keys]
    n=len(coords)
    array={var:np.full((n,12),np.nan,dtype=float) for var in CLIMATE_VARIABLES}
    manifest={}
    for var in CLIMATE_VARIABLES:
        path=Path(dir_)/("wc2.1_10m_"+var+".zip")
        if not path.is_file() or path.stat().st_size<100000:
            raise ValueError("STAGE87C_NOT_ORIGINAL_WORLDCLIM_10m_ZIP_"+var)
        manifest[var]={"original_worldclim_source_zip_SHA256":sha(path),
          "source_original_bytes":path.stat().st_size,"source_url":CLIM_BASE+path.name}
        with zipfile.ZipFile(path) as z:
            months=read_months(z)
            for m,filename in sorted(months.items()):
                with MemoryFile(z.read(filename)) as mem,mem.open() as ds:
                    if ds.count!=1 or ds.crs is None or ds.crs.to_epsg()!=4326:
                        raise ValueError("STAGE87C_ORIGINAL_WORLDCLIM_GEOREF_NOT_EPSG4326")
                    if not .15<ds.res[0]<.18:
                        raise ValueError("STAGE87C_CLIM_NOT_10ARCMIN")
                    values=ds.sample(coords,masked=True)
                    for j,val in enumerate(values):
                        if np.ma.is_masked(val[0]):continue
                        v=float(val[0])
                        if validate_climate(var,v):array[var][j,m-1]=v
    regions=defaultdict(list)
    for i,(code,lon,lat) in enumerate(sample_keys):
        regions[code].append(i)
    out={}
    for code,idx in regions.items():
        vals={}
        # Long-term averages, not observed bloom month.
        for var,col in CLIMATE_VARIABLES.items():
            arr=array[var][idx,:]
            good=np.isfinite(arr).all(axis=1)
            valid_idx=np.where(good)[0]
            rowmean=arr[good,:].mean(axis=1) if good.any() else np.array([])
            weights=np.array([max(0.0001,math.cos(math.radians(sample_keys[idx[k]][2])))
                  for k in valid_idx])
            v=float(np.average(rowmean,weights=weights)) if rowmean.size else None
            vals[col]=v
            vals[col+"_sd_within_region"]=float(np.std(rowmean)) if rowmean.size>1 else None
            vals[col+"_valid_points"]=int(good.sum())
        out[code]=vals
        out[code]["region_original_sample_locations_requested"]=len(idx)
        out[code]["region_sampling_latitude_mean"]=float(np.mean([sample_keys[i][2] for i in idx]))
        out[code]["region_sampling_longitude_mean"]=float(np.mean([sample_keys[i][1] for i in idx]))
    return out,manifest

def combine(native,climate,invalid,names):
    output=[];state=Counter()
    for code,row in native.items():
        c=climate.get(code)
        if c is None:state["source_missing_GIS_region_code"]+=1;continue
        vals={**row,**c,
         "TDWG_level3_name":names.get(code,{}).get("LEVEL3_NAM",""),
         "TDWG_level2_name":names.get(code,{}).get("LEVEL2_NAM",""),
         "TDWG_level1_name":names.get(code,{}).get("LEVEL1_NAM",""),
         "source_original_TDWG_polygon_geometry_repaired_sensitivity":int(code in invalid),
         "climate_is_1970_2000_normal_not_visit_year":"YES",
         "climate_wind_is_not_flower_odor_plume_or_ERA5_gust":"YES"}
        ok=all(c[CLIMATE_VARIABLES[var]] is not None
               and c[CLIMATE_VARIABLES[var]+"_valid_points"]>=12 for var in CLIMATE_VARIABLES)
        vals["source_all_5climate_variables_at_12_or_more_points"]=int(ok)
        state["region_complete_5variable_climate"]+=ok
        output.append(vals)
    return output,dict(state)

def run(orig,geo,worldclim,out):
    native=source_regions(orig)
    shapes,invalid,names=source_polygons(geo)
    samples,sampling=sample_source_region_points(shapes)
    clim,manifest=source_climate(samples,worldclim)
    rows,state=combine(native,clim,invalid,names)
    if len(rows)<300 or state["region_complete_5variable_climate"]<250:
        raise ValueError("STAGE87C_GLOBAL_SOURCE_CLIMATE_COVERAGE_NOT_ENOUGH")
    out.mkdir(parents=True,exist_ok=True)
    columns=sorted(set().union(*(set(x) for x in rows)))
    with (out/"stage87_original_global_TDWG3_NHM_WCVP_WorldClim_regions.csv").open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=columns);wr.writeheader();wr.writerows(rows)
    receipt={"schema":"stage87C_world_wcvp_native_flower_text_x_WorldClim2_1_climate_normals",
      "source_original_GIS_TDWG_feature_git_blob_SHA1":TDWG_GIT_BLOB_SHA1,
      "source_original_worldclim_10arcmin_climate":manifest,
      "source_original_global_native_region_input":len(native),
      "source_GIS_polygon_regions":len(shapes),
      "source_GIS_invalid_features_repaired_for_explicit_sensitivity":sum(invalid.values()),
      "source_GIS_regions_with_repaired_feature":len(invalid),
      "source_original_climate_region_source_join":state,
      "original_sampling_per_region":SAMPLED_PER_SOURCE_REGION,
      "source_original_polygon_sampling_counts":sampling,
      "worldclim_baseline_years":"1970-2000",
      "source_no_measured_true_at_flower_voc_or_landing_wind":True,
      "source_no_false_Bombus_absence":True,
      "source_all_hue_fraction_labels_are_source_text_not_colorimetry":True}
    (out/"stage87C_real_worldclim_TDWG3_flower_spatial_receipt.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("STAGE87C_REAL_GLOBAL_WCVP_CLIMATE",json.dumps({
       k:v for k,v in receipt.items() if k!="source_original_worldclim_10arcmin_climate"},sort_keys=True),flush=True)
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-native-flora",type=Path,required=True)
    p.add_argument("--original-tdwg-geojson",type=Path,required=True)
    p.add_argument("--worldclim-directory",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    z=p.parse_args();run(z.original_native_flora,z.original_tdwg_geojson,z.worldclim_directory,z.outdir)
if __name__=="__main__":main()
