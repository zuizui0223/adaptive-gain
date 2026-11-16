"""Stage46: source file-grain verification for *modeled* Bombus distribution and UV guides.

No synthetic suitability is returned as evidence. Read Zenodo/Dryad metadata,
file names, declared bytes, available spatial formats, license and authors.
Do NOT download large rasters and do NOT label original occurrence as SDM.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import urllib.error

MAX_META_BYTES=8_000_000
SOURCE_LIST={
    "global_bee_range_model_2026":("https://zenodo.org/api/records/20525239","zenodo"),
    "europe_bombus_ENM_2026":("https://zenodo.org/api/records/21620753","zenodo"),
    "global_bee_plant_GloBI_2026":("https://zenodo.org/api/records/18303036","zenodo"),
    "UV_pattern_Potentilleae_2021":(
       "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.k98sf7m3z","dryad"),
    "UV_pigment_herbarium_2020":(
       "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.ttdz08kw1","dryad"),
    "UV_Mimulus_geographic_2016":(
       "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.3q6n0","dryad"),
}
ALLOWED={"zenodo.org","datadryad.org"}


def _get_json(url):
    parsed=urllib.parse.urlparse(url)
    if parsed.scheme!="https" or parsed.hostname not in ALLOWED:
        raise ValueError("NO_GO_ARCHIVE_METADATA_UNTRUSTED_HOST")
    req=urllib.request.Request(url,headers={
       "Accept":"application/json",
       "User-Agent":"adaptive-gain-floral-UV-Bombus-archive-discovery/2026"
    })
    with urllib.request.urlopen(req,timeout=42) as resp:
        b=resp.read(MAX_META_BYTES+1)
    if len(b)>MAX_META_BYTES:
        raise ValueError("NO_GO_ARCHIVE_METADATA_TOO_LARGE")
    obj=json.loads(b.decode("utf-8-sig"))
    if not isinstance(obj,dict):
        raise ValueError("NO_GO_ARCHIVE_METADATA_NOT_JSON_OBJECT")
    return obj,hashlib.sha256(b).hexdigest()


def _zenodo_summary(meta):
    metadata=meta.get("metadata") or {}
    raw=meta.get("files") or {}
    if isinstance(raw,list):
        files=raw
    elif isinstance(raw,dict):
        files=list((raw.get("entries") or {}).values())
    else:
        files=[]
    out=[]
    for f in files:
        if not isinstance(f,dict):continue
        links=f.get("links") or {}
        size=f.get("size") or 0
        if isinstance(size,dict):size=size.get("bytes",0)
        name=f.get("key") or f.get("filename") or f.get("name") or ""
        out.append({"name":str(name),
                    "size_bytes":size if isinstance(size,int) else 0,
                    "checksum":f.get("checksum") or "",
                    "file_download_url":links.get("self") or links.get("content") or "",
                    "extension":Path(str(name)).suffix.lower()})
    return {
      "record_title":metadata.get("title") or "",
      "record_doi":meta.get("doi") or "",
      "published":meta.get("publication_date") or "",
      "rights":(metadata.get("license") or {}),
      "file_count":len(out),
      "files":out,
    }


def _dryad_summary(meta):
    version=meta.get("version") or {}
    links=meta.get("_links") or {}
    names=[]
    embedded=meta.get("_embedded") or {}
    for key in ("files","stash:files"):
        if isinstance(embedded.get(key),list):
            names=[x for x in embedded[key] if isinstance(x,dict)]
            break
    out=[]
    for f in names:
        out.append({"name":f.get("path") or f.get("name") or "",
                    "size_bytes":f.get("size") or 0})
    return {"record_title":meta.get("title") or "",
            "record_doi":meta.get("identifier") or "",
            "version":version,
            "license":meta.get("license") or "",
            "links":{k:v.get("href") if isinstance(v,dict) else v
                     for k,v in links.items()},
            "embedded_file_count":len(out),"files":out}


def discover():
    receipt={"status":"ORIGINAL_SOURCE_METADATA_ONLY_NO_SDM_PREDICTION",
             "sources":{},"unavailable":{}}
    for name,(url,kind) in SOURCE_LIST.items():
        try:
            data,sha=_get_json(url)
            summary=_zenodo_summary(data) if kind=="zenodo" else _dryad_summary(data)
            summary["metadata_url"]=url
            summary["source_metadata_sha256"]=sha
            summary["response_class"]=kind
            summary["original_spatial_raster_data_downloaded"]=False
            receipt["sources"][name]=summary
        except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
                TimeoutError,json.JSONDecodeError,KeyError,TypeError) as err:
            receipt["unavailable"][name]={"error_kind":type(err).__name__,
                      "message":str(err)[:180], "missing_is_not_negative_evidence":True}
    return receipt


def main():
    result=discover()
    folder=Path("stage46_source_index");folder.mkdir(exist_ok=True)
    (folder/"published_pollinator_sdm_and_uv_sources.json").write_text(
       json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2,
                  allow_nan=False)+"\n",encoding="utf8")
    print("STAGE46_SDM_AND_UV_ARCHIVE_MANIFEST",json.dumps(result,sort_keys=True))
    if not result["sources"]:
        raise SystemExit("NO_GO_NO_PUBLISHED_MODEL_OR_UV_ORIGINAL_SOURCE_METADATA")


if __name__=="__main__":
    main()
