#!/usr/bin/env python3
"""Stage98 original TDWG3 polygon adjacency of fixed mainland 88/37 split.

This is a BLIND geography-only diagnostic. Reuses original TDWG geometry
source and Stage94 exact SHA-verified region split without opening floral
signals or climatic wind. Nearby regional polygon boundaries compromise
interpretation of a 'spatially heldout' prediction. Detect shared boundaries
or overlaps exactly with native lon/lat geometry. Noncontact distance is only
a rough geodesic diagnostic based on planar nearest WGS84 points; does not
certify a geographically buffered holdout, especially near the antimeridian.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,statistics,sys,zipfile
from collections import Counter
from pathlib import Path
from shapely.ops import nearest_points
from pyproj import Geod

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage87"))
from aggregate_global_tdwg3_worldclim_wind import source_polygons,TDWG_GIT_BLOB_SHA1

STAGE94_SHA256="3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833"
STAGE94_MEMBER="stage94_original_mainland_shared_geoblock_split.csv"
GEOD=Geod(ellps="WGS84")

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def read_locked_mainland_split(path):
    if sha256(path)!=STAGE94_SHA256:
        raise ValueError("STAGE98_ORIGINAL_MAINLAND_SOURCE_ZIP_SHA_CHANGED")
    with zipfile.ZipFile(path) as z:
        if STAGE94_MEMBER not in z.namelist():
            raise ValueError("STAGE98_MISSING_ORIGINAL_GEO_SHARED_SPLIT")
        rows=list(csv.DictReader(io.StringIO(z.read(STAGE94_MEMBER).decode("utf-8-sig"))))
    if len(rows)!=125 or len({r["TDWG_L3"] for r in rows})!=125:
        raise ValueError("STAGE98_ORIGINAL_125_SOURCE_REGIONS_DRIFT")
    folds=Counter(x["shared_split"] for x in rows)
    if folds!={"exploration":88,"holdout":37}:
        raise ValueError("STAGE98_88_37_SHARED_SPLIT_CHANGED")
    if any(r["land_scope"]!="mainland" for r in rows):
        raise ValueError("STAGE98_ISLAND_OR_MIXED_IN_SOURCE")
    byblock={}
    for r in rows:
        block=r["spatial_block_id"]
        if block in byblock and byblock[block]!=r["shared_split"]:
            raise ValueError("STAGE98_ORIGINAL_SPATIAL_BLOCK_LEAK")
        byblock[block]=r["shared_split"]
    return rows

def edge_geodesic_approx_km(a,b):
    """Use shapely planar-nearest WGS84 points, THEN ellipsoid great-circle.

    This is not an exact geodesic distance between irregular polygons.
    Touching or intersecting source polygons are exactly distance 0.
    """
    if a.intersects(b):return 0.0
    p,q=nearest_points(a,b)
    _,_,distance_m=GEOD.inv(float(p.x),float(p.y),float(q.x),float(q.y))
    return max(0.0,float(distance_m)/1000)

def diagnose_crossfold_region_boundaries(rows,shapes):
    if len(set(x["TDWG_L3"] for x in rows))!=len(rows):
        raise ValueError("STAGE98_DUPLICATE_REGIONS")
    training=sorted((r for r in rows if r["shared_split"]=="exploration"),
                    key=lambda r:r["TDWG_L3"])
    holdout=sorted((r for r in rows if r["shared_split"]=="holdout"),
                   key=lambda r:r["TDWG_L3"])
    missing={r["TDWG_L3"] for r in rows}-set(shapes)
    if missing:raise ValueError("STAGE98_ORIGINAL_TDWG_GEOMETRY_MISSING_"+str(sorted(missing)[:5]))
    pairwise=[];by_holdout=[];contact=Counter()
    for row in holdout:
        h=row["TDWG_L3"];poly=shapes[h]
        dist=[]
        for train in training:
            t=train["TDWG_L3"];other=shapes[t]
            # Exact planar lonlat polygon topology. Shared boundary is a
            # genuine no-buffer warning, not necessarily geographic overlap.
            touches=bool(poly.touches(other))
            overlaps=bool(poly.overlaps(other))
            intersects=bool(poly.intersects(other))
            km=edge_geodesic_approx_km(poly,other)
            if intersects:
                contact["intersecting_train_holdout_pairs"]+=1
                contact["touching_pairs"]+=touches
                contact["overlap_pairs"]+=overlaps
                contact["intersecting_identical_block_count"]+=int(
                    row["spatial_block_id"]==train["spatial_block_id"])
                pairwise.append({"holdout_TDWG_L3":h,
                    "exploration_TDWG_L3":t,"pair_source_geometry_intersects":intersects,
                    "pair_source_geometry_touches":touches,
                    "pair_source_geometry_overlaps":overlaps,
                    "approx_boundary_gap_km":0.0,
                    "holdout_block":row["spatial_block_id"],
                    "exploration_block":train["spatial_block_id"]})
            dist.append((km,t,touches,overlaps,intersects))
        if not dist:raise ValueError("STAGE98_NO_EXPLORATION_GEOGRAPHY")
        nearest=min(dist,key=lambda item:(item[0],item[1]))
        n0=sum(x[4] for x in dist)
        by_holdout.append({"TDWG_L3":h,
            "shared_split":"holdout",
            "spatial_block_id":row["spatial_block_id"],
            "nearest_exploration_TDWG_L3":nearest[1],
            "nearest_source_TDWG_polygon_boundary_gap_approx_km":nearest[0],
            "n_source_intersecting_exploration_polygons":n0,
            "source_direct_polygon_contact_or_overlap":n0>0,
            "approx_boundary_gap_less_100_km_not_a_certified_buffer":nearest[0]<100,
            "full_physical_geodesic_100km_holdout_buffer_certified":"NO"})
    return by_holdout,pairwise,{
        "n_train_regions":len(training),
        "n_holdout_regions":len(holdout),
        "total_train_holdout_region_pairs_evaluated":len(training)*len(holdout),
        "holdout_regions_touching_or_intersecting_any_exploration_polygon":sum(
              x["source_direct_polygon_contact_or_overlap"] for x in by_holdout),
        "holdout_regions_geodesic_approx_boundary_distance_below100km":sum(
              x["approx_boundary_gap_less_100_km_not_a_certified_buffer"] for x in by_holdout),
        "shortest_approx_boundary_gap_km":min(
            x["nearest_source_TDWG_polygon_boundary_gap_approx_km"] for x in by_holdout),
        "median_approx_nearest_boundary_gap_km":statistics.median(
            x["nearest_source_TDWG_polygon_boundary_gap_approx_km"] for x in by_holdout),
        **dict(contact)
    }

def run(geo_source_zip,tdwg_original,outdir):
    rows=read_locked_mainland_split(geo_source_zip)
    shapes,invalid,_=source_polygons(tdwg_original)
    holdout,pairs,summary=diagnose_crossfold_region_boundaries(rows,shapes)
    if len(holdout)!=37 or summary["total_train_holdout_region_pairs_evaluated"]!=3256:
        raise ValueError("STAGE98_NOT_EXACT_CROSS_FOLD_ORIGINAL_SOURCE")
    if summary.get("intersecting_identical_block_count",0)>0:
        raise ValueError("STAGE98_BLOCK_LEAKAGE_IN_SOURCE")
    result={
      "schema":"stage98_original_TDWG3_shared_holdout_source_polygon_adjacency_ONLY",
      "original_stage94_geo_artifact_sha256":STAGE94_SHA256,
      "original_TDWG_level3_geojson_git_blob_sha1":TDWG_GIT_BLOB_SHA1,
      "source_TDWG_original_repaired_polygons_among_all_original_features":len(invalid),
      "source_region_counts":summary,
      "topologically_exact_contact_not_nearest_geodesic":True,
      "noncontact_approx_distance_is_NOT_a_certified_geodesic_buffer":True,
      "regional_polygon_boundaries_may_cross_different_data_snapshots":True,
      "no_wind_signal_or_Bombus_data_opened":True,
      "original_holdout_exploration_partition_UNCHANGED":True,
      "verified_physical_distance_buffer_success":False,
      "claim_ceiling":"source geography leakage gate not ecological response"
    }
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage98_original_holdout_source_nearest_boundary_audit.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(holdout[0]));w.writeheader();w.writerows(holdout)
    with (outdir/"stage98_source_exact_contact_region_pairs.csv").open("w",newline="") as f:
        if pairs:
            w=csv.DictWriter(f,fieldnames=list(pairs[0]));w.writeheader();w.writerows(pairs)
        else:
            f.write("holdout_TDWG_L3,exploration_TDWG_L3\n")
    (outdir/"stage98_original_frozen_holdout_geography_adjacency_receipt.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print("STAGE98_ORIGINAL_TDWG_MAINLAND_HOLDOUT_GEOGRAPHY",json.dumps(summary,sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--stage94-geo-source-zip",required=True,type=Path)
    p.add_argument("--original-TDWG-geojson",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args();run(a.stage94_geo_source_zip,a.original_TDWG_geojson,a.outdir)
