"""Stage46: georeference original 2026 model-derived Bombus HEX richness.

Match the ORIGINAL source P/A table (396,703 cell/taxon positive rows) to the
ORIGINAL Zenodo Hexgon_shapefile DBF (10,242 centroid records) by siteid.
No GBIF observation counts, no fitted plant model, no synthetic coordinate.
Explicitly distinguish cells with any modeled bee data from unrepresented
source grid cells; 0 Bombus in covered cells is a MODEL code, not true absence.
"""
from __future__ import annotations

from collections import Counter,defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile

from derive_bombus_hex_prediction import _get_model_source,modelled_bombus_coverage
from discover_pollinator_sdm_sources import _get_json
from zip_range_catalog import get_range
from inspect_bee_hex_geography import _dbf_header,HEX_FILE,CHUNK

ZENODO="https://zenodo.org/api/records/20525240"
HEX_DBF="Hexgon_shapefile/hexgrid.dbf"
HEX_RECORDS=10242


def parse_original_dbf_centroids(source):
    original=_dbf_header(source)
    fields=original["field_schema"]
    wanted={"CENTRELON","CENTRELAT","siteid"}
    if not wanted.issubset({z["name"] for z in fields}):
        raise ValueError("NO_GO_ORIGINAL_HEX_DB_FIELDS_NOT_MATCHED")
    count=original["records"]
    header_length,record_length=struct.unpack_from("<HH",source,8)
    if header_length+count*record_length>len(source):
        raise ValueError("NO_GO_ORIGINAL_HEX_DBF_TRUNCATED")
    geo={}
    deleted=0
    for idx in range(count):
        start=header_length+idx*record_length
        rec=source[start:start+record_length]
        if rec[:1]==b"*":
            deleted+=1
            continue
        if rec[:1]!=b" ":
            raise ValueError("NO_GO_ORIGINAL_HEX_DBF_ROW_MARKER")
        current=1
        row={}
        for field in fields:
            value=rec[current:current+field["length"]]
            current+=field["length"]
            if field["name"] in wanted:
                row[field["name"]]=value.decode("ascii",errors="replace").strip()
        name=row.get("siteid","")
        if name in geo or not name.startswith("HEX"):
            raise ValueError("NO_GO_ORIGINAL_HEX_ID_BAD_OR_DUPLICATED")
        try:
            lon=float(row["CENTRELON"])
            lat=float(row["CENTRELAT"])
        except (ValueError,KeyError):
            raise ValueError("NO_GO_HEX_LAT_LON_NONNUMERIC")
        if not -180<=lon<=180 or not -90<=lat<=90:
            raise ValueError("NO_GO_HEX_LAT_LON_OUTSIDE_EARTH")
        geo[name]=(lon,lat)
    return geo,{"source_DB_record_count":count,"deleted_records":deleted,
                "distinct_original_hex_id":len(geo),
                "original_DB_fields":[f["name"] for f in fields]}


def load_original_hex_centroids():
    meta,_=_get_json(ZENODO)
    matches=[x for x in meta.get("files") or [] if x.get("key")==HEX_FILE]
    if len(matches)!=1:
        raise ValueError("NO_GO_ZENODO_HEX_GRID_FILE_NOT_FOUND")
    f=matches[0];url=(f.get("links") or {}).get("self");total=f.get("size")
    if not isinstance(total,int) or total>15_000_000 or not isinstance(url,str):
        raise ValueError("NO_GO_BAD_GLOBAL_BEE_HEX_FILE_SIZE")
    b=b"".join(get_range(url,total,start,min(total,start+CHUNK)-1)
                for start in range(0,total,CHUNK))
    if len(b)!=total or "md5:"+hashlib.md5(b).hexdigest()!=f.get("checksum"):
        raise ValueError("NO_GO_ZENODO_HEX_ZIP_CHECKSUM")
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        names=[x for x in z.namelist() if x==HEX_DBF]
        if len(names)!=1:
            raise ValueError("NO_GO_ZENODO_HEX_DBF_SOURCE_MISSING")
        centers,info=parse_original_dbf_centroids(z.read(HEX_DBF))
    if len(centers)!=HEX_RECORDS:
        raise ValueError("NO_GO_HEX_POLYGON_CENTROID_SOURCE_COUNT")
    info["source_zip_MD5"]=f.get("checksum")
    info["source_dbf_member"]=HEX_DBF
    return centers,info


def join_modelled_bombus_and_centroids(grid,centers):
    allowed=set(centers)
    from_model={cell:(bombus,otherbee) for cell,bombus,otherbee in grid}
    if len(from_model)!=len(grid) or not set(from_model).issubset(allowed):
        raise ValueError("NO_GO_BEE_PA_SITEID_NOT_IN_ORIGINAL_SOURCE_HEX_GRID")
    result=[]
    bands=defaultdict(list)
    for siteid,(lon,lat) in sorted(centers.items()):
        available=siteid in from_model
        bombus,allbee=from_model[siteid] if available else (None,None)
        if available and not (isinstance(bombus,int) and isinstance(allbee,int)
                              and 0<=bombus<=allbee):
            raise ValueError("NO_GO_HEX_RICHNESS_LOGIC")
        result.append({
          "source_siteid":siteid,"longitude":lon,"latitude":lat,
          "n_source_modelled_Bombus_taxa":bombus,
          "n_source_modelled_all_bee_taxa":allbee,
          "model_support_status":("SOURCE_BEE_PA_CELL" if available
              else "NO_SOURCE_BEE_PA_CELL_NOT_TRUE_ABSENCE"),
          "source_model":"10.5281/zenodo.20525239",
          "interpretation":"modelled range/polygon overlap, not observed bee density"
        })
        if available:
            low=int((lat+90)//15)*15-90
            band=(low,low+15)
            bands[band].append(bombus)
    summaries=[]
    for (low,high),values in sorted(bands.items()):
        summaries.append({
           "latitude_band_lower":low,"latitude_band_upper":high,
           "n_cells_with_modelled_bees":len(values),
           "n_cells_with_positive_modelled_Bombus":sum(v>0 for v in values),
           "mean_source_modelled_Bombus_taxa_per_covered_cell":sum(values)/len(values),
           "max_source_modelled_Bombus_taxa_in_covered_cell":max(values)
        })
    return result,summaries


def main():
    raw=_get_model_source()
    source_stats,grid,species=modelled_bombus_coverage(raw)
    centroids,geo_stats=load_original_hex_centroids()
    records,latbands=join_modelled_bombus_and_centroids(grid,centroids)
    output=Path("stage46_georeferenced_Bombus_prediction")
    output.mkdir(exist_ok=True)
    path=output/"source_modelled_Bombus_richness_lonlat_10242_HEX.csv"
    with path.open("w",encoding="utf8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(records[0]))
        wr.writeheader()
        wr.writerows(records)
    summary={
      "status":"ORIGINAL_SOURCE_BOMBUS_PREDICTION_10242_HEX_GEOGRAPHICALLY_LINKED",
      "source_modelled_bee_matrix_SHA256":source_stats["source_member_SHA256"],
      "source_modelled_Bombus_taxon_names":source_stats["n_distinct_modelled_Bombus_taxon_strings"],
      "source_global_hex_dbf_records":geo_stats["source_DB_record_count"],
      "source_hex_coverage":len(records),
      "modelled_bee_PA_source_hex_coverage":sum(
         r["model_support_status"]=="SOURCE_BEE_PA_CELL" for r in records),
      "unrepresented_hex_no_true_bee_absence_inference":sum(
         r["model_support_status"]!="SOURCE_BEE_PA_CELL" for r in records),
      "hex_with_source_modelled_Bombus":sum(
         (r["n_source_modelled_Bombus_taxa"] or 0)>0 for r in records),
      "hex_with_modelled_bees_but_Bombus_zero":sum(
          r["n_source_modelled_Bombus_taxa"]==0 for r in records),
      "max_source_modelled_Bombus_taxon_richness":source_stats["max_modelled_bombus_richness"],
      "source_hex_zip_MD5":geo_stats["source_zip_MD5"],
      "source_centroid_coordinate_fields":"CENTRELON,CENTRELAT",
      "latitude_band_descriptive":latbands,
      "original_global_Bombus_taxonomy_not_accepted_independently":True,
      "not_true_Bombus_occupation_or_pollination_service":True,
      "not_a_plant_trait_x_Bombus_suitability_analysis_yet":True
    }
    (output/"source_hex_geographic_join_receipt.json").write_text(
       json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+"\n")
    print("STAGE46_GEOREFERENCED_BOMBUS_MODELLED_RICHNESS",json.dumps(summary,sort_keys=True))
    print("STAGE46_NO_NATIVE_BOMBUS_OR_FLORAL_GUIDE_CAUSAL_INFERENCE")

if __name__=="__main__":
    main()
