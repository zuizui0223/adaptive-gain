"""Stage47: exact study-site × source bee-HEX polygon overlap feasibility.

Botanical study sites are *as reported* by Tunes et al. (2021), doi
10.3389/fpls.2021.618028, not inferred GBIF plant observations.
Bee model is the original Laborieux et al. (2026) Zenodo 20525240 source,
with author tree tip filter and >=5 taxon/cell rule from Stage46.

Shapefile points are transformed from WGS84 to the original source .prj
and assigned by polygon intersection, NEVER nearest HEX centroid.
Original Santa Barbara coordinates are a published BOUNDING RANGE; check
the four geographic corners and midpoint, not a fake sampled point.

This is *only* model-coverage/contrast feasibility, not an UV-guide × bee
association. No original taxon-to-individual-study-site table is available.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage46"))

from discover_pollinator_sdm_sources import _get_json
from inspect_bee_hex_geography import HEX_FILE,CHUNK
from zip_range_catalog import get_range
from georeference_bombus_prediction import parse_original_dbf_centroids
from author_tree_filtered_bombus import (
    fetch_author_small_sources,source_parameter_and_taxa,
    trim_original_bee_matrix,materialize_join,
)
from derive_bombus_hex_prediction import _get_model_source,modelled_bombus_coverage

ZENODO="https://zenodo.org/api/records/20525240"
HEX_ZIP_MD5="md5:999c8c9eb6688628588d0d794ac390e1"
SOURCE_MEMBERS=(
    "Hexgon_shapefile/hexgrid.shp",
    "Hexgon_shapefile/hexgrid.shx",
    "Hexgon_shapefile/hexgrid.dbf",
    "Hexgon_shapefile/hexgrid.prj",
)
SOURCE_HEX_N=10242
# Public study sites. Source Botucatu DMS 22°54'45"S 48°30'13"W
# Serra da Canastra 20°14'01"S 46°26'40"W
# Santa Barbara E.E. 22°46'-22°41'S and 49°16'-49°10'W
# No taxon-specific original study-site assignment available in Table S2.
STUDY_SITES=(
    {"name":"Botucatu","country":"Brazil",
     "kind":"published_single_coordinate",
     "coordinates_lonlat":[(-48-30/60-13/3600,-22-54/60-45/3600)]},
    {"name":"Santa Bárbara Ecological Station","country":"Brazil",
     "kind":"published_coordinate_rectangle_not_point",
     "coordinates_lonlat":[
          (-49-16/60,-22-46/60),(-49-10/60,-22-46/60),
          (-49-16/60,-22-41/60),(-49-10/60,-22-41/60),
          (-49-13/60,-22-43.5/60)
      ]},
    {"name":"Serra da Canastra National Park","country":"Brazil",
     "kind":"published_single_coordinate",
     "coordinates_lonlat":[(-46-26/60-40/3600,-20-14/60-1/3600)]},
)

def load_authenticated_shape_sources():
    meta,_=_get_json(ZENODO)
    matches=[x for x in meta.get("files",[]) if x.get("key")==HEX_FILE]
    if len(matches)!=1:
        raise ValueError("NO_GO_AUTHOR_HEX_ZIP_NOT_IDENTIFIED")
    z=matches[0]
    total=z.get("size");url=(z.get("links") or {}).get("self")
    if not isinstance(total,int) or total<=0 or total>15_000_000:
        raise ValueError("NO_GO_HEX_ZIP_SIZE")
    if not isinstance(url,str) or z.get("checksum")!=HEX_ZIP_MD5:
        raise ValueError("NO_GO_ORIGINAL_HEX_SOURCE_METADATA_DRIFT")
    raw=b"".join(get_range(url,total,i,min(total,i+CHUNK)-1)
                for i in range(0,total,CHUNK))
    if len(raw)!=total or "md5:"+hashlib.md5(raw).hexdigest()!=HEX_ZIP_MD5:
        raise ValueError("NO_GO_HEX_ZIP_EXACT_MD5")
    with zipfile.ZipFile(io.BytesIO(raw)) as f:
        present=set(f.namelist())
        if not set(SOURCE_MEMBERS).issubset(present):
            raise ValueError("NO_GO_HEX_SHAPEFILE_PRJ_SHP_SHX_DBF_NOT_ALL_PRESENT")
        members={name:f.read(name) for name in SOURCE_MEMBERS}
    centroids,info=parse_original_dbf_centroids(members[SOURCE_MEMBERS[2]])
    if len(centroids)!=SOURCE_HEX_N or info["distinct_original_hex_id"]!=SOURCE_HEX_N:
        raise ValueError("NO_GO_ORIGINAL_HEX_ID_COUNT_CHANGED")
    return members,centroids,{
       "source_hex_zip_md5":HEX_ZIP_MD5,
       "original_source_hex_shape_count":SOURCE_HEX_N,
       "original_projected_source_crs_from_prj_not_assumed_wgs84":True
    }


def polygons_from_original_shapefile(members,centroids):
    import shapefile
    from shapely.geometry import shape
    from shapely.strtree import STRtree
    from pyproj import CRS,Transformer
    original_wkt=members[SOURCE_MEMBERS[3]].decode("latin1").strip()
    crs=CRS.from_wkt(original_wkt)
    if not crs.is_projected:
        raise ValueError("NO_GO_ORIGINAL_BEE_HEX_PROJECTION_NOT_PROJECTED")
    transform=Transformer.from_crs("EPSG:4326",crs,always_xy=True)
    with shapefile.Reader(
        shp=io.BytesIO(members[SOURCE_MEMBERS[0]]),
        shx=io.BytesIO(members[SOURCE_MEMBERS[1]]),
        dbf=io.BytesIO(members[SOURCE_MEMBERS[2]]),
        encoding="utf8",
    ) as reader:
        if reader.numRecords!=SOURCE_HEX_N:
            raise ValueError("NO_GO_SOURCE_SHAPE_RECORD_COUNT")
        names=[]
        geometries=[]
        for item in reader.iterShapeRecords():
            row=item.record.as_dict()
            name=str(row.get("siteid",""))
            if name not in centroids or name in names:
                raise ValueError("NO_GO_ORIGINAL_HEX_SHP_DBF_LINK_BAD")
            geom=shape(item.shape.__geo_interface__)
            if geom.is_empty or geom.geom_type not in ("Polygon","MultiPolygon"):
                raise ValueError("NO_GO_SHAPE_EMPTY_OR_NOT_A_POLYGON")
            names.append(name)
            geometries.append(geom)
    if len(set(names))!=SOURCE_HEX_N or set(names)!=set(centroids):
        raise ValueError("NO_GO_SHAPE_ID_NOT_THE_SAME_AS_CENTER_TABLE")
    return names,STRtree(geometries),transform,{
        "original_source_projection_name":crs.name,
        "original_original_prj_sha256":hashlib.sha256(members[SOURCE_MEMBERS[3]]).hexdigest(),
        "no_nearest_centroid_or_assumed_equal_area":True,
    }


def matching_original_hex(lon,lat,names,tree,transform):
    from shapely.geometry import Point
    if not (-180<=lon<=180 and -90<=lat<=90):
        raise ValueError("NO_GO_PUBLISHED_SITE_COORDINATE_OUTSIDE_EARTH")
    px,py=transform.transform(lon,lat)
    if not (abs(px)<1e9 and abs(py)<1e9):
        raise ValueError("NO_GO_GIS_PROJECTION_BAD")
    point=Point(px,py)
    hit=sorted({names[int(i)] for i in tree.query(point)
                if tree.geometries[int(i)].covers(point)})
    return hit


def assign_study_sites(sites,names,tree,transform,model_lookup):
    out=[]
    for site in sites:
        point_ids=[matching_original_hex(lon,lat,names,tree,transform)
                   for lon,lat in site["coordinates_lonlat"]]
        if any(len(ids)!=1 for ids in point_ids):
            status="NO_GO_POINT_UNASSIGNED_OR_ON_POLYGON_BOUNDARY"
            unique=set(x for ids in point_ids for x in ids)
        else:
            unique=set(x[0] for x in point_ids)
            status=("SINGLE_ORIGINAL_SOURCE_HEX_STABLE_WITHIN_PUBLISHED_COORDS"
                    if len(unique)==1 else
                    "SOURCE_PUBLISHED_COORDINATE_RANGE_CROSSES_MULTIPLE_HEX")
        candidates=[]
        for hexid in sorted(unique):
            model=model_lookup.get(hexid)
            if model is None:
                raise ValueError("NO_GO_HEX_NOT_IN_MODELLED_SOURCE_CENTROID_LIST")
            candidates.append({
                "source_hex_id":hexid,
                "author_pa_cutoff_eligible":model["eligibility"]=="AUTHOR_TREE_AND_PA_CELL_CUTOFF",
                "n_modelled_source_Bombus_taxa_or_null":model["n_source_tree_and_pa_cutoff_Bombus_taxa"],
                "n_modelled_source_all_bee_taxa_or_null":model["n_source_tree_and_pa_cutoff_all_bee_taxa"],
                "not_population_or_fitness":True,
            })
        out.append({
           "original_study_location":site["name"],
           "country":"Brazil",
           "source_location_coordinate_kind":site["kind"],
           "n_tested_source_site_coordinates":len(site["coordinates_lonlat"]),
           "hex_assignment_status":status,
           "candidate_author_model_hex_cells":candidates,
           "original_source_study_sites_are_not_taxon_specific_UV_measurements":True,
        })
    return out


def summarize(rows):
    allids={z["source_hex_id"] for x in rows for z in x["candidate_author_model_hex_cells"]}
    source_values={
       z["source_hex_id"]:z for x in rows for z in x["candidate_author_model_hex_cells"]
    }
    eligible=[v for v in source_values.values() if v["author_pa_cutoff_eligible"]]
    return {
        "status":"ORIGINAL_CERRADO_STUDY_SITE_TO_PUBLISHED_BEE_HEX_COVERAGE_AUDIT",
        "source_sites_tested":len(rows),
        "distinct_source_grid_hex_in_site_range":len(allids),
        "n_source_study_hex_author_eligible":len(eligible),
        "n_source_study_hex_author_unmodelled_unknown":len(allids)-len(eligible),
        "n_eligible_hex_with_positive_source_Bombus":sum(
            (v["n_modelled_source_Bombus_taxa_or_null"] or 0)>0 for v in eligible),
        "n_eligible_hex_with_zero_source_Bombus":sum(
            v["n_modelled_source_Bombus_taxa_or_null"]==0 for v in eligible),
        "distinct_Bombus_source_modelled_richness_values":sorted(set(
            v["n_modelled_source_Bombus_taxa_or_null"] for v in eligible)),
        "distinct_all_bee_source_modelled_richness_values":sorted(set(
            v["n_modelled_source_all_bee_taxa_or_null"] for v in eligible)),
        "not_a_valid_between_species_UV_suitability_correlation":True,
        "source_article_species_site_mapping_not_available":True,
        "source_NHM_UV_guide_absence_not_inferred":True,
        "no_new_Bombus_field_presence_or_visitation_claim":True,
    }


def main():
    members,centers,source_info=load_authenticated_shape_sources()
    names,tree,transform,geometry_info=polygons_from_original_shapefile(members,centers)
    script,phylo=fetch_author_small_sources()
    p,phylo_taxa=source_parameter_and_taxa(script,phylo)
    original_model=_get_model_source()
    rawstats,_,_=modelled_bombus_coverage(original_model)
    filtered,retained,shared=trim_original_bee_matrix(original_model,phylo_taxa,p["pa_cutoff"])
    records=materialize_join(retained,centers)
    if len(records)!=10242 or filtered["source_taxa_after_tree_and_cell_cutoff"]!=3370:
        raise ValueError("NO_GO_SOURCE_PAPER_FILTER_NOT_REPRODUCED")
    locations=assign_study_sites(STUDY_SITES,names,tree,transform,{
       x["source_siteid"]:x for x in records})
    result=summarize(locations)
    result.update({
        "source_study_doi":"10.3389/fpls.2021.618028",
        "model_source_doi":"10.5281/zenodo.20525239",
        "paper_filtered_global_Bombus_names":filtered["source_Bombus_species_after_tree_cell_cutoff"],
        "paper_filtered_global_bee_names":filtered["source_taxa_after_tree_and_cell_cutoff"],
        "source_geography":source_info,
        "source_geometry":geometry_info,
        "site_assignments":locations,
    })
    dest=Path("stage47_source_site_feasibility")
    dest.mkdir(exist_ok=True)
    (dest/"original_three_UV_study_sites_x_original_3370_bee_model.json").write_text(
       json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+"\n",
       encoding="utf8")
    print("STAGE47_REAL_SOURCE_THREE_UV_STUDY_SITE_BEE_EXPOSURES",
          json.dumps(result,sort_keys=True,ensure_ascii=False))
    print("NO_UV_BOMBUS_MACRO_ASSOCIATION_ESTIMATED")


if __name__=="__main__":
    main()
