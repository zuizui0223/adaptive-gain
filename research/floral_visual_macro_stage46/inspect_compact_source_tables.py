"""Stage46: inspect ORIGINAL compact global bee SDM README and Dryad UV file list.

Never download 21+ GB SDM archive. Verify text bytes to published checksum,
read source definitions for equal-area hex cells, plant/bee taxon grain.
No derived biological effect or unverified Bombus predictions.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request
from discover_pollinator_sdm_sources import _get_json

ZENODO="https://zenodo.org/api/records/20525239"
DRYAD="https://datadryad.org/api/v2/versions/101476/files"
ALLOWED={"zenodo.org","datadryad.org"}
MAX_SMALL_BYTES=120_000


def original_bytes(url,max_bytes=MAX_SMALL_BYTES):
    parsed=urllib.parse.urlparse(url)
    if parsed.scheme!="https" or parsed.hostname not in ALLOWED:
        raise ValueError("NO_GO_ORIGINAL_SOURCE_HOST")
    req=urllib.request.Request(url,headers={
       "User-Agent":"adaptive-gain-stage46-original-bee-matrix-reader/2026",
       "Accept":"application/octet-stream,text/plain,application/json"})
    with urllib.request.urlopen(req,timeout=50) as resp:
        blob=resp.read(max_bytes+1)
    if len(blob)>max_bytes:
        raise ValueError("NO_GO_SOURCE_FILE_TOO_LARGE")
    return blob


def source_text_files():
    meta,_=_get_json(ZENODO)
    files=meta.get("files") or []
    selected={}
    for f in files:
        name=f.get("key","")
        if name not in ("readme.txt","3_Bee_generate_PA_mat.r",
                        "2_Bee_process_range_estimates.r",
                        "4_Bee_bioregion_analysis_data_export.r"):
            continue
        url=(f.get("links") or {}).get("self") or ""
        declared=f.get("checksum") or ""
        source=original_bytes(url)
        md5="md5:"+hashlib.md5(source).hexdigest()
        sha256="sha256:"+hashlib.sha256(source).hexdigest()
        if declared and declared.lower()!=md5.lower() and declared.lower()!=sha256.lower():
            raise ValueError("NO_GO_ZENODO_SOURCE_FILE_CHECKSUM_"+name)
        txt=source.decode("utf-8-sig",errors="replace")
        selected[name]={
           "url":url,"size_bytes":len(source),
           "original_checksum":declared,
           "verified_checksum":md5 if declared.startswith("md5:") else sha256,
           "line_count":len(txt.splitlines()),
           "original_source_readme_first_2600_chars":txt[:2600] if name=="readme.txt" else "",
           "relevant_keywords":[x for x in ("data.zip","PA_mat","sdm.zip",
                "Hexgon_shapefile","species","Bombus","hex","raster","output.zip")
                if x.casefold() in txt.casefold()],
           "no_raw_file_redistributed":True,
        }
    if "readme.txt" not in selected:
        raise ValueError("NO_GO_MISSING_ZENODO_SDM_README")
    return selected


def dryad_file_manifest():
    obj,_=_get_json(DRYAD)
    files=obj.get("_embedded") or {}
    rows=files.get("stash:files") or files.get("files") or obj.get("files") or []
    if not isinstance(rows,list):
        rows=[]
    res=[]
    for row in rows:
        if not isinstance(row,dict):continue
        links=row.get("_links") or {}
        res.append({
          "name":row.get("path") or row.get("name") or row.get("fileName") or "",
          "size":row.get("size") or row.get("sizeBytes"),
          "file_id":row.get("id") or row.get("fileId"),
          "links":{k:v.get("href") if isinstance(v,dict) else v
                   for k,v in links.items() if "download" in k.lower() or "self"==k},
        })
    return {
      "api_url":DRYAD,
      "top_keys":sorted(obj.keys()),
      "file_count_page":len(res),
      "source_files":res[:40],
      "no_source_traits_extracted_yet":True,
    }


def main():
    report={"status":"VERIFIED_PUBLISHED_BEE_MODEL_SOURCE_README_AND_DRYAD_UV_FILE_GRAIN",
            "original_bee_model":source_text_files(),
            "dryad_UV_Potentilleae":dryad_file_manifest(),
            "no_predicted_Bombus_map_calculated":True}
    folder=Path("stage46_compact_source");folder.mkdir(exist_ok=True)
    (folder/"original_bee_grid_readme_and_UV_files.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n",
        encoding="utf8")
    print("STAGE46_ORIGINAL_BEE_SOURCE_README_AND_DRYAD",json.dumps(report,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
