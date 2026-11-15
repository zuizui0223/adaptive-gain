"""Stage35: retrieve original Crall et al. orchid-bee wind data from Zenodo.

THIS MODULE ONLY AUTHENTICATES AND PROFILES ORIGINAL DOWNLOADS. It does
NOT claim to reproduce the 2020 Poisson GLMM or a wind x odor 2x2.
The 2020 article cites Zenodo version 3743898; an openly indexed
CrallEtAl_OrchidBeeWindEcology.zip exists at record 3675327. Examine
versions independently and don't silently substitute dataset identity.
A source-free fixture exercises the parsing, not the ecological result.

No raw author data copied into the GitHub repo or Actions artifacts.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from urllib.parse import urlparse

DOI_PAPER="10.1098/rsbl.2020.0103"
DATASET_IDS=(3743898,3675327)
MAX_DOWNLOAD=5_000_000
MAX_ZIP_CONTENT=15_000_000
MAX_CSV=3_000_000


def _fetch(url):
    parsed=urlparse(url)
    if parsed.scheme!="https" or parsed.hostname!="zenodo.org":
        raise ValueError("NO_GO_EXTERNAL_SOURCE_HOST_UNAUTHORIZED")
    req=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-source-grain-audit/2026-11-15",
        "Accept":"application/json,application/zip,application/octet-stream,*/*"
    })
    with urllib.request.urlopen(req,timeout=25) as response:
        content=response.read(MAX_DOWNLOAD+1)
    if len(content)>MAX_DOWNLOAD:
        raise ValueError("NO_GO_OVERSIZED_SOURCE")
    return content


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _csv_profile(source):
    if len(source)>MAX_CSV:
        raise ValueError("NO_GO_OVERSIZED_CSV")
    try:
        text=source.decode("utf-8-sig")
    except UnicodeDecodeError:
        # Older ecology files occasionally use Windows Latin-1, record this.
        text=source.decode("latin-1")
        encoding="latin-1"
    else:
        encoding="utf-8-sig"
    start=text[:2000]
    reader=csv.reader(io.StringIO(text,newline=""))
    try:
        header=next(reader)
    except StopIteration:
        raise ValueError("NO_GO_CSV_EMPTY")
    if not header or any(not s.strip() for s in header):
        raise ValueError("NO_GO_CSV_NO_HEADER")
    if len(header)>256:
        raise ValueError("NO_GO_CSV_TOO_MANY_COLUMNS")
    counts=[0]*len(header)
    missing=[0]*len(header)
    numeric=[0]*len(header)
    minimum=[None]*len(header)
    maximum=[None]*len(header)
    n=0
    for row in reader:
        if not row or (len(row)==1 and not row[0].strip()):
            continue
        if len(row)!=len(header):
            raise ValueError("NO_GO_CSV_FIELD_ARITY_MISMATCH")
        n+=1
        if n>150_000:
            raise ValueError("NO_GO_UNEXPECTED_UNBOUNDED_CSV")
        for j,s in enumerate(row):
            s=s.strip()
            if not s or s.lower() in ("na","nan","null"):
                missing[j]+=1
                continue
            counts[j]+=1
            try:
                x=float(s)
            except ValueError:
                continue
            if not (-1e300<x<1e300):
                continue
            numeric[j]+=1
            minimum[j]=x if minimum[j] is None else min(minimum[j],x)
            maximum[j]=x if maximum[j] is None else max(maximum[j],x)
    return {
        "n_records":n, "n_columns":len(header),
        "header":header, "encoding":encoding,
        "column_profiles":[{
          "column":key,
          "nonmissing":counts[i],
          "missing":missing[i],
          "numeric_valid":numeric[i],
          "numeric_min":minimum[i],"numeric_max":maximum[i]
        } for i,key in enumerate(header)],
        "no_individual_original_rows_redistributed":True
    }


def _safe_zip_inventory(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError("NO_GO_NOT_ZIP")
    files=[]
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        entries=[e for e in archive.infolist() if not e.is_dir()]
        if not entries or len(entries)>150:
            raise ValueError("NO_GO_ZIP_FILE_COUNT")
        if sum(z.file_size for z in entries)>MAX_ZIP_CONTENT:
            raise ValueError("NO_GO_DECOMPRESS_LIMIT")
        for file in entries:
            name=file.filename
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError("NO_GO_UNSAFE_ZIP_PATH")
            record={"path":name,"source_uncompressed_bytes":file.file_size}
            if Path(name).suffix.lower() in (".csv",".tsv"):
                raw=archive.read(file)
                record["raw_sha256"]=_sha(raw)
                if name.lower().endswith(".csv"):
                    try:
                        record["csv"]=_csv_profile(raw)
                        record["csv"]["status"]="PARSED_ORIGINAL_CSV"
                    except ValueError as err:
                        # Preserve a malformed/empty CSV source and its exact
                        # hash; do NOT invalidate other legitimate files.
                        record["csv"]={
                           "status":"CSV_SOURCE_QA_FAILURE",
                           "diagnostic":str(err)[:180],
                           "n_records":None,
                           "header":None}
                else:
                    record["tsv"]={
                      "status":"TSV_SOURCE_NOT_PROFILED_AS_CSV",
                      "source_uncompressed_bytes":file.file_size}
            files.append(record)
    return files


def _candidate_download_urls(metadata):
    files=metadata.get("files",[])
    if not isinstance(files,list):
        return []
    result=[]
    for file in files:
        key=file.get("key") or file.get("filename") or ""
        if not key.lower().endswith(".zip"):
            continue
        links=file.get("links") or {}
        for link in (links.get("self"),links.get("content"),links.get("download")):
            if isinstance(link,str) and link.startswith("https://zenodo.org/"):
                result.append((key,link,file.get("checksum"),file.get("size")))
                break
    return result


def assess_api_metadata(metadata,record_id):
    if not isinstance(metadata,dict):
        raise ValueError("NO_GO_ZENODO_METADATA_NOT_OBJECT")
    m=metadata.get("metadata") or {}
    title=(m.get("title") or "").strip()
    if "wind" not in title.lower() or "pollinator" not in title.lower():
        raise ValueError("NO_GO_UNRELATED_ZENODO_RECORD")
    creators=m.get("creators") or []
    if not any("Crall" in (x.get("name") or "") for x in creators):
        raise ValueError("NO_GO_NOT_CRALL_AUTHOR")
    candidates=_candidate_download_urls(metadata)
    return {
      "record_id_requested":record_id,
      "record_id_metadata":metadata.get("id"),
      "title":title,
      "doi":metadata.get("doi",m.get("doi")),
      "version":m.get("version"),
      "zip_candidates":candidates,
      "source_metadata_version_verified":True,
      "cannot_conflate_versions":True
    }


def _verify_md5_if_declared(blob,checksum):
    if not checksum:
        return {"declared_checksum":None,"passed":None}
    if checksum.startswith("md5:"):
        good=hashlib.md5(blob).hexdigest()==checksum[4:]
        if not good:
            raise ValueError("NO_GO_DOWNLOAD_CHECKSUM_MISMATCH")
        return {"declared_checksum":checksum,"passed":True}
    return {"declared_checksum":checksum,"passed":None}


def _probe(record_id):
    api=f"https://zenodo.org/api/records/{record_id}"
    metadata=json.loads(_fetch(api).decode("utf-8"))
    profile=assess_api_metadata(metadata,record_id)
    profile["source_api_url"]=api
    profile["attempted_downloads"]=[]
    for filename,url,checksum,declared_size in profile["zip_candidates"]:
        try:
            blob=_fetch(url)
            if declared_size is not None and len(blob)!=int(declared_size):
                raise ValueError("NO_GO_DECLARED_SIZE_DIFFERENT")
            validation=_verify_md5_if_declared(blob,checksum)
            manifest=_safe_zip_inventory(blob)
            profile["selected_zip_filename"]=filename
            profile["selected_zip_sha256"]=_sha(blob)
            profile["zip_integrity"]=validation
            profile["zip_original_file_profiles"]=manifest
            profile["original_source_bytes_obtained"]=True
            profile["original_csv_count"]=sum(
                x.get("csv",{}).get("status")=="PARSED_ORIGINAL_CSV" for x in manifest)
            profile["csv_qa_failure_count"]=sum(
                x.get("csv",{}).get("status")=="CSV_SOURCE_QA_FAILURE" for x in manifest)
            profile["observed_effects_estimated"]=False
            profile["experimental_wind_by_scent_on_off_identified"]=False
            profile["single_visit_pollen_transfer_identified"]=False
            profile["raw_original_data_redistributed"]=False
            profile["status"]=(
                "VERIFIED_AUTHOR_ARCHIVE_SOURCE_GRAIN_WITH_CSV_QA_WARNINGS"
                if profile["csv_qa_failure_count"] else
                "VERIFIED_AUTHOR_ARCHIVE_SOURCE_GRAIN_ONLY")
            return profile
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,OSError,
                ValueError,zipfile.BadZipFile) as err:
            profile["attempted_downloads"].append({
               "file":filename,"error":type(err).__name__,
               "diagnostic":str(err)[:350],
               "http_status":getattr(err,"code",None)})
    profile["status"]="NO_GO_ZENODO_ARCHIVE_NOT_RETRIEVED"
    profile["original_source_bytes_obtained"]=False
    return profile


def run():
    outcomes=[]
    for record_id in DATASET_IDS:
        try:
            result=_probe(record_id)
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,OSError,
                ValueError,json.JSONDecodeError) as err:
            result={
              "record_id_requested":record_id,
              "status":"NO_GO_ZENODO_SOURCE_FETCH_OR_IDENTITY",
              "error":type(err).__name__,
              "http_status":getattr(err,"code",None),
              "original_source_bytes_obtained":False
            }
        outcomes.append(result)
    successes=[x for x in outcomes if x.get("status","").startswith("VERIFIED_AUTHOR_ARCHIVE_SOURCE_GRAIN")]
    return {
       "status":"VERIFIED_ONE_OR_MORE_AUTHOR_ARCHIVES" if successes else "NO_GO_NO_ORIGINAL_ZENODO_ARCHIVE",
       "source_article_doi":DOI_PAPER,
       "author_referenced_record_id":3743898,
       "alternate_indexed_record_id":3675327,
       "record_receipts":outcomes,
       "verified_record_count":len(successes),
       "ecological_effect_estimates_extracted":0,
       "no_invented_source_observations":True,
       "no_original_file_redistribution":True,
       "wind_by_odor_interaction_empirically_tested":False
    }


def main():
    receipt=run()
    directory=Path("stage35_source_receipts")
    directory.mkdir(parents=True,exist_ok=True)
    (directory/"stage35_zenodo_original_source_manifest.json").write_text(
       json.dumps(receipt,indent=2,ensure_ascii=False,allow_nan=False)+"\n")
    print(json.dumps({
       "status":receipt["status"],
       "verified_record_count":receipt["verified_record_count"],
       "source_details":[{
          "id":r["record_id_requested"],"status":r["status"],
          "archive":r.get("selected_zip_filename"),
          "available_zip_candidates":len(r.get("zip_candidates",[])),
          "download_failures":r.get("attempted_downloads",[]),
          "raw_csv_count":r.get("original_csv_count"),
          "qa_csv_failures":r.get("csv_qa_failure_count"),
          "files":[{
             "path":x["path"],"row_count":x.get("csv",{}).get("n_records"),
             "header":x.get("csv",{}).get("header")
          } for x in r.get("zip_original_file_profiles",[])]
       } for r in receipt["record_receipts"]]
    },sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
