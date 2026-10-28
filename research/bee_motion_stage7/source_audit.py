"""Stage7: Dryad API-source audit of actual two-hive bumblebee landing tracks.

Original Fig/data publisher: de Vries et al. 2025 JEB; dataset
doi:10.5061/dryad.qbzkh18tj. All file IDs are retrieved from native Dryad
API metadata; none are inferred or hardcoded from guessed website URLs.
The 17.31 MB .7z stays ephemeral; CI uploads schema/hash receipts only.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
import urllib.request
from urllib.parse import quote,urljoin
import time

API="https://datadryad.org/api/v2"
DOI="10.5061/dryad.qbzkh18tj"
ENC=quote("doi:"+DOI,safe="")
ARCHIVE_NAME="data_bumblebee_landing_moving_flower.7z"
README_NAME="README.md"
MAX_RESPONSE=8*1024*1024
MAX_ARCHIVE=32*1024*1024
MAX_UNCOMPRESSED=850*1024*1024
ACCEPT={"README.md",ARCHIVE_NAME}

def read_https(url,cap=MAX_RESPONSE):
    if not url.startswith("https://"):
        raise ValueError("NO_GO_DRYAD_URL_NOT_HTTPS")
    req=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-source-audited-open-science-trajectory-provenance/1.0",
        "Accept":"application/json,application/octet-stream,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=90) as rsp:
        data=rsp.read(cap+1)
        actual=getattr(rsp,"status",200)
        typ=rsp.headers.get("Content-Type","")
        location=rsp.url
    if len(data)>cap:
        raise ValueError(f"NO_GO_DRYAD_RESPONSE_TOO_LARGE size>{cap}")
    if not data or data[:128].lstrip().lower().startswith((b"<html",b"<!doctype")):
        raise ValueError("NO_GO_DRYAD_NONDATA_CONTENT")
    return data,{"status":actual,"content_type":typ,
                 "final_host":urllib.request.urlparse(location).netloc if False else
                              location.split("/",3)[2]}

def json_get(url):
    b,headers=read_https(url)
    try:return json.loads(b.decode("utf-8")),headers
    except Exception as e:raise ValueError("NO_GO_DRYAD_NON_JSON_METADATA") from e

def get_href(metadata,name):
    links=metadata.get("_links",{})
    obj=links.get(name,links.get("stash:"+name))
    if isinstance(obj,dict) and obj.get("href"):return obj["href"]
    return None

def follow(base,href):
    full=urljoin(base,href)
    if not full.startswith(("https://datadryad.org/","https://v3.datadryad.org/")):
        raise ValueError("NO_GO_METADATA_LINK_NONDRYAD: "+full)
    return full

def retrieve_file_record():
    entry=f"{API}/datasets/{ENC}"
    data,_=json_get(entry)
    version_href=get_href(data,"version")
    if version_href:
        version_url=follow(entry,version_href)
        v,_=json_get(version_url)
    else:
        # Documented alternative API route, never invent version IDs.
        versions,_=json_get(entry+"/versions")
        arr=versions.get("_embedded",{}).get("stash:versions",[])
        if not arr:raise ValueError("NO_GO_DRYAD_NO_PUBLIC_VERSION")
        v=arr[0]
        version_url=v.get("_links",{}).get("self",{}).get("href","")
        if not version_url:raise ValueError("NO_GO_DRYAD_MISSING_VERSION_URL")
        version_url=follow(entry,version_url)
    files_href=get_href(v,"files")
    if not files_href:raise ValueError("NO_GO_DRYAD_MISSING_FILES_LINK")
    file_list_url=follow(version_url,files_href)
    all_files=[]
    next_url=file_list_url
    while next_url:
        f,_=json_get(next_url)
        arr=f.get("_embedded",{}).get("stash:files")
        if not isinstance(arr,list):
            raise ValueError("NO_GO_DRYAD_FILE_LIST_SCHEMA")
        all_files.extend(arr)
        nxt=get_href(f,"next")
        next_url=follow(next_url,nxt) if nxt else None
        if len(all_files)>150:raise ValueError("NO_GO_TOO_MANY_SOURCE_FILES")
    results={}
    metadata=[]
    for f in all_files:
        name=f.get("path",f.get("name"))
        if name not in ACCEPT:continue
        href=get_href(f,"download")
        if not href:raise ValueError("NO_GO_NO_ACTUAL_DOWNLOAD_LINK_FOR_"+name)
        file_url=follow(file_list_url,href)
        results[name]={"path":name,
                       "download_url":file_url,
                       "api_record":{k:f.get(k) for k in ("id","path","size","digest","digestType","mimeType")},
                       "metadata_version_url":version_url}
    for name in ACCEPT:
        if name not in results:raise ValueError("NO_GO_REQUIRED_DRYAD_FILE_NOT_LISTED "+name)
    audit={"dataset_identifier":data.get("identifier",data.get("id")),
           "version_url":version_url,"file_manifest_url":file_list_url,
           "listed_files_count":len(all_files),
           "selected_files":[{k:v for k,v in r.items() if k!="download_url"} for r in results.values()],
           "source_metadata_api_url":entry}
    return results,audit

def download_source_file(info,folder):
    name=info["path"]
    limit=MAX_ARCHIVE if name==ARCHIVE_NAME else MAX_RESPONSE
    data,metadata=read_https(info["download_url"],cap=limit)
    expected_size=info["api_record"].get("size")
    if expected_size is not None and int(expected_size)!=len(data):
        raise ValueError(f"NO_GO_SOURCE_SIZE_MISMATCH {name}: {expected_size} != {len(data)}")
    provider=info["api_record"].get("digest")
    dtype=str(info["api_record"].get("digestType") or "").lower()
    if provider:
        if dtype=="md5":
            if hashlib.md5(data).hexdigest()!=provider:raise ValueError("NO_GO_DRYAD_MD5_MISMATCH")
        elif dtype=="sha256":
            if hashlib.sha256(data).hexdigest()!=provider:raise ValueError("NO_GO_DRYAD_SHA256_MISMATCH")
        else:
            raise ValueError("NO_GO_UNKNOWN_SOURCE_DIGEST_TYPE "+dtype)
    out=folder/name
    out.write_bytes(data)
    return {"filename":name,"size":len(data),
            "source_sha256":hashlib.sha256(data).hexdigest(),
            "api_digest":provider,"api_digest_type":dtype,
            "http_source":metadata,
            "resolved_provider_download_url":info["download_url"]}

def inspect_7z(path):
    import py7zr
    if not py7zr.is_7zfile(path):
        raise ValueError("NO_GO_DRYAD_NOT_7Z")
    with py7zr.SevenZipFile(path,mode="r") as archive:
        members=archive.list()
        entries=[]
        total=0
        for f in members:
            name=f.filename
            normalized=Path(name)
            if normalized.is_absolute() or ".." in normalized.parts:
                raise ValueError("NO_GO_UNSAFE_ARCHIVE_MEMBER_PATH")
            size=int(f.uncompressed)
            if size<0 or size>100*1024*1024:
                raise ValueError("NO_GO_SOURCE_7Z_MEMBER_OVERSIZE")
            total+=size
            entries.append({"relative_path":name,
                            "uncompressed_size":size,
                            "is_directory":bool(f.is_directory)})
            if len(entries)>500:raise ValueError("NO_GO_UNEXPECTED_ARCHIVE_MEMBER_COUNT")
        if total>MAX_UNCOMPRESSED:raise ValueError("NO_GO_EXPANDED_SIZE_CAP")
    return {"member_count":len(entries),"total_declared_uncompressed_bytes":total,
            "member_paths":[x["relative_path"] for x in entries if not x["is_directory"]],
            "source_members":entries,
            "is_all_native_files_preserved":True}

def run(outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    manifest,audit=retrieve_file_record()
    receipt={"source":"Dryad API v2",
             "doi":DOI,"manifest":audit,
             "file_receipts":{}}
    (outdir/"moving_flower_source_manifest.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE7_DRYAD_PROVIDER_MANIFEST "+
          json.dumps({
            "version_url":audit["version_url"],
            "files":[{"name":name,
                      "file_api_metadata":info["api_record"],
                      "file_url_path":info["download_url"].split("?",1)[0]}
                    for name,info in manifest.items()]},ensure_ascii=False),flush=True)
    for name,info in manifest.items():
        try:
            file_record=download_source_file(info,outdir)
        except Exception as exc:
            receipt["source_download_failure"]={
                "attempted_filename":name,
                "exception_type":type(exc).__name__,
                "http_status":getattr(exc,"code",None),
                "message":str(exc)[:600]}
            (outdir/"moving_flower_source_manifest.json").write_text(
                json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False))
            print("STAGE7_DRYAD_DOWNLOAD_BLOCK "+
                  json.dumps(receipt["source_download_failure"]),flush=True)
            raise
        receipt["file_receipts"][name]=file_record
        print("STAGE7_DRYAD_FILE "+json.dumps(file_record,ensure_ascii=False),flush=True)
    receipt["readme_text"]= (outdir/README_NAME).read_text(
        encoding="utf-8-sig",errors="strict")[:30000]
    receipt["archive_profile"]=inspect_7z(outdir/ARCHIVE_NAME)
    (outdir/"moving_flower_source_manifest.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE7_DRYAD_SOURCE_AUDIT "+json.dumps(receipt,ensure_ascii=False),flush=True)
    print("STAGE7_DRYAD_SOURCE_AUDIT_COMPLETE",flush=True)
    return receipt

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="moving_flower_source")
    args=parser.parse_args()
    run(Path(args.out))
