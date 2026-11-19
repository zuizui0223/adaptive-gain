#!/usr/bin/env python3
"""Stage94: reproducible GLOBAL TDWG3 land topology + *strict mainland* source split.

Original source TDWG 3 region boundaries and independent Natural Earth 10m
physical land polygons. The six anchor points select CONTINENTAL landmasses
only: no 'large land = continent' area cutoff (Greenland is an island).

A TDWG3 polygon may cover a mainland area PLUS real islands, so the regional
flora is NOT mainland-only unless the polygon's nonmainland land intersection
is negligible under a declared coastline numerical-tolerance threshold.

This excludes mixed regions, not re-assigns their plants to mainland. Stage91
shared split is applied ONLY after objective geometry source joins and frozen
without reading wind/cue/bombus outcomes. Results are not a wind analysis.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path

from pyproj import Geod
from shapely.geometry import Point,shape
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely.strtree import STRtree
from shapely import to_wkb

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage87"))
sys.path.insert(0,str(BASE/"floral_macro_stage91"))
from aggregate_global_tdwg3_worldclim_wind import source_polygons, TDWG_GIT_BLOB_SHA1
from freeze_mainland_region_frame import split_regions

NATURAL_EARTH_LAND_ZIP_SHA256="e547d749445eaa0964aba76738090ec88f5e63c4585122170f98c67a7ea922dc"
NATURAL_EARTH_URL="https://naciscdn.org/naturalearth/10m/physical/ne_10m_land.zip"
REGISTRY_SOURCE_ARTIFACT_SHA256="f1197a050d110d1e3626ab01f3c5d49626ac32fd0588d41ce3a162b44d921cdf"
REGION_MEMBER="stage91_global_TDWG3_3cue_availability_INCLUDES_ISLANDS.csv"
ANCHORS={
    "eurasia":(72.0,46.0),
    "africa":(20.0,-12.0),
    "north_america":(-103.0,40.0),
    "south_america":(-60.0,-15.0),
    "australia":(134.0,-26.0),
    "antarctica":(0.0,-80.0),
}
GEOD=Geod(ellps="WGS84")
# Maximum numerical border discrepancy tolerated as "no island".
# Any source island overlap >= 0.1 km2 is mixed, and excluded.
COAST_DISCREPANCY_TOL_KM2=0.1
MIN_REGION_LAND_KM2=5.0

def digest(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda:handle.read(1024*1024),b""):h.update(block)
    return h.hexdigest()

def area_km2(g):
    if g.is_empty:return 0.0
    if g.geom_type=="Polygon":
        return abs(GEOD.geometry_area_perimeter(orient(g,sign=1.0))[0])/1e6
    if hasattr(g,"geoms"):
        return sum(area_km2(x) for x in g.geoms)
    return 0.0

def read_original_native_367(artifact_zip):
    if digest(artifact_zip)!=REGISTRY_SOURCE_ARTIFACT_SHA256:
        raise ValueError("STAGE94_RETRIEVED_STAGE91_TRUE_ORIGINAL_SOURCE_ARTIFACT_SHA_DRIFT")
    with zipfile.ZipFile(artifact_zip) as z:
        if REGION_MEMBER not in z.namelist():
            raise ValueError("STAGE94_REGION_MEMBER_NOT_IN_ORIGINAL_STAGE91_ARTIFACT")
        with io.TextIOWrapper(z.open(REGION_MEMBER),encoding="utf-8-sig",newline="") as f:
            records=list(csv.DictReader(f))
    codes={r["TDWG_L3"] for r in records}
    if len(records)!=367 or len(codes)!=367:
        raise ValueError("STAGE94_STAGE91_EXACT_367_TDWG_SOURCE_REGIONS_CHANGED")
    return codes

def original_natural_earth_land(path):
    if digest(path)!=NATURAL_EARTH_LAND_ZIP_SHA256:
        raise ValueError("STAGE94_PINNED_NATURAL_EARTH_V511_ZIP_SHA_CHANGED")
    from fiona.io import ZipMemoryFile
    raw=Path(path).read_bytes()
    polys=[]
    with ZipMemoryFile(raw) as fz:
        entries=fz.listdir()
        options=[str(x) for x in entries if str(x).casefold().endswith("ne_10m_land.shp")]
        if len(options)!=1:
            raise ValueError("NATURAL_EARTH_ZIP_HAS_NO_UNIQUE_10M_LAND_SHP")
        with fz.open(options[0]) as f:
            if f.crs and "4326" not in str(f.crs):
                raise ValueError("NATURAL_EARTH_NOT_WGS84_LON_LAT")
            for rec in f:
                if rec["geometry"] is None:continue
                g=shape(rec["geometry"])
                if not g.is_valid:raise ValueError("NATURAL_EARTH_INVALID_ORIGINAL_LAND_GEOMETRY")
                if not g.is_empty:polys.append(g)
    if len(polys)<100:
        raise ValueError("NATURAL_EARTH_LAND_POLYGON_COUNT_IMPLAUSIBLE")
    dissolved=unary_union(polys)
    components=(list(dissolved.geoms) if dissolved.geom_type=="MultiPolygon" else [dissolved])
    if len(components)<50:raise ValueError("NATURAL_EARTH_ISLANDS_MISSING_IN_LAND_DISSOLVE")
    main_idx={}
    for label,(lon,lat) in ANCHORS.items():
        matches=[i for i,p in enumerate(components) if p.covers(Point(lon,lat))]
        if len(matches)!=1:
            raise ValueError("STAGE94_MAINLAND_ANCHOR_NOT_IDENTIFIED_"+label)
        main_idx[label]=matches[0]
    # This allows Suez/Panama continental connection under Natural Earth
    # topology, but NEVER selects Greenland merely because it is large.
    # Test known land-islands in original source as geographic guard.
    for label,(lon,lat) in {"greenland":(-40,72),"madagascar":(47,-20),
                             "bali":(115,-8.4),"great_britain":(-2,54)}.items():
        if any(components[i].covers(Point(lon,lat)) for i in set(main_idx.values())):
            raise ValueError("STAGE94_ISLAND_FALSE_MAINLAND_"+label)
    return components,set(main_idx.values()),{"source_original_land_polygon_count":len(polys),
        "dissolved_connected_land_components":len(components),
        "six_point_continental_anchor_components":main_idx,
        "number_distinct_major_mainland_landmasses":len(set(main_idx.values())),
        "rejected_named_large_islands":["greenland","madagascar","bali","great_britain"]}

def geometry_class(main_km2,island_km2,*,tol=COAST_DISCREPANCY_TOL_KM2):
    if min(main_km2,island_km2)<0:raise ValueError("negative source land area")
    total=main_km2+island_km2
    if total<MIN_REGION_LAND_KM2:return "mixed"
    if main_km2<tol and island_km2>=tol:return "island"
    if island_km2<tol and main_km2>=tol:return "mainland"
    return "mixed"

def classify_original_regions(native_codes, original_tdgw, components, mainland_idx):
    regions,invalid,_=source_polygons(original_tdgw)
    missing=native_codes-set(regions)
    if missing:raise ValueError("STAGE94_SOURCE_TDWG_CODE_GEOMETRY_MISSING_"+str(sorted(missing)[:8]))
    tree=STRtree(components)
    out=[];stats=Counter()
    for code in sorted(native_codes):
        g=regions[code]
        if g.is_empty:raise ValueError("TDWG_REGION_EMPTY")
        mainland_area=0.0;island_area=0.0
        for i in tree.query(g):
            j=int(i)
            part=components[j]
            if not g.intersects(part):continue
            overlap=area_km2(g.intersection(part))
            if overlap<=0:continue
            if j in mainland_idx:mainland_area+=overlap
            else:island_area+=overlap
        scope=geometry_class(mainland_area,island_area)
        stats[scope]+=1
        stats["region_invalid_original_TDWG_feature"]+=(code in invalid)
        h=hashlib.sha256(to_wkb(g,byte_order=1)).hexdigest()
        # Avoid assign block using shape of entire mixed-region.
        # Only mainland candidates receive a block; excluded records
        # retain a deterministic placeholder never used in the split.
        point=g.representative_point()
        if scope=="mainland":
            lon=float(point.x);lat=float(point.y)
            # The source representative point itself must be in the mainland
            # landmass. Failure is ambiguous and conservatively excluded.
            if not any(components[j].covers(point) for j in mainland_idx):
                scope="mixed"
                stats["mainland_candidate_without_mainland_representative_point"]+=1
                stats["mainland"]-=1;stats["mixed"]+=1
                block="EXCLUDED_MIXED_REP_POINT"
            else:
                latbin=int(math.floor((lat+90.0)/20.0))
                lonbin=int(math.floor((lon+180.0)/45.0))
                block=f"TDWG-mainland-geoblock-20x45-{latbin:02d}-{lonbin:02d}"
        else:block="EXCLUDED_"+scope.upper()
        out.append({"TDWG_L3":code,"land_scope":scope,"spatial_block_id":block,
          "polygon_sha256":h,
          "geometry_source":"TDWG WGSRPD original immutable 91104e5159e31f88154833a51d3b0d1c9271083f × pinned NaturalEarth land v5.1.1 e547d749 (geodesic land-area topology; automated)",
          "original_TDWG_invalid_polygon_repaired":int(code in invalid),
          "estimated_mainland_land_km2":round(mainland_area,4),
          "estimated_nonmainland_island_land_km2":round(island_area,4),
          "estimated_mainland_land_fraction":mainland_area/(mainland_area+island_area)
             if mainland_area+island_area else "",
          "source_topology_method":"original_tdwg_intersection_NaturalEarth_land_dissolved_anchor_connected_components",
          "strict_source_coast_mismatch_tolerance_km2":COAST_DISCREPANCY_TOL_KM2,
          "region_land_area_valid_min_km2":MIN_REGION_LAND_KM2})
    return out,dict(stats)

def run(native_artifact,tdwg_geojson,ne_zip,out):
    codes=read_original_native_367(native_artifact)
    parts,main,meta=original_natural_earth_land(ne_zip)
    registry,count=classify_original_regions(codes,tdwg_geojson,parts,main)
    if len(registry)!=367 or not all(r["polygon_sha256"] for r in registry):
        raise ValueError("STAGE94_UNVERIFIED_TDWG_SOURCE_REGISTRY")
    # Existing Stage91 API accepts original source columns.
    # The same assigner applies to all cue endpoints; no trait outcomes.
    split,contract=split_regions(sorted(codes),registry)
    out.mkdir(parents=True,exist_ok=True)
    for name,rows in (("stage94_original_367_mainland_island_mixed_registry.csv",registry),
                      ("stage94_original_mainland_shared_geoblock_split.csv",split)):
        with (out/name).open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=rows[0].keys())
            writer.writeheader();writer.writerows(rows)
    response={"schema":"stage94_TDWG3_genuine_source_NaturalEarth_mainland_only_spatial_holdout",
       "pinned_TDWG_original_git_blob_sha1":TDWG_GIT_BLOB_SHA1,
       "pinned_NaturalEarth10m_land_zip_sha256":NATURAL_EARTH_LAND_ZIP_SHA256,
       "source_stage91_regional_artifact_sha256":REGISTRY_SOURCE_ARTIFACT_SHA256,
       "source_TDWG_regions":len(codes),"strict_regional_land_scope_counts":count,
       "source_mainland_connected_component_checks":meta,
       "source_area_min_and_island_tolerance_km2":{"min":MIN_REGION_LAND_KM2,
                                                   "island":COAST_DISCREPANCY_TOL_KM2},
       "same_frozen_block_holdout_for_three_separate_cues":contract,
       "source_geographic_polygon_based_not_plant_cue_or_wind_based":True,
       "regional_polygon_does_not_remove_individual_island_localities_from_mainland_TDWG_area":True,
       "coastline_cross_dataset_mismatch_requires_region_review":True,
       "spatial_buffer_between_heldout_train_regions_verified":False,
       "no_cue_direction_or_wind_regression_performed":True}
    (out/"stage94_original_mainland_island_mixed_geometry_receipt.json").write_text(
          json.dumps(response,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE94_REAL_GLOBAL_TDWG_MAINLAND_SOURCE_GEOMETRY",json.dumps({
      "regional_scope_counts":count,"split":contract["block_split_counts"],
      "distinct_mainland_blocks":contract["distinct_mainland_blocks"],
      "continent_component_count":len(main)},sort_keys=True))
    return response

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source-original-stage91-region-artifact",type=Path,required=True)
    p.add_argument("--source-original-TDWG-geospatial-geojson",type=Path,required=True)
    p.add_argument("--source-original-NaturalEarth-land-ZIP",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    run(a.source_original_stage91_region_artifact,
        a.source_original_TDWG_geospatial_geojson,
        a.source_original_NaturalEarth_land_ZIP,a.outdir)
