"""Stage74B: official Zenodo original Finnell & Koski 2021 sensory-drive source.

DOI 10.5281/zenodo.5110165, publication 10.1111/nph.17631.
Research design: high vs low alpine populations of Argentina anserina;
actual 2 UV treatments (ambient/reduced), 2 guide sizes, bare/foliage
background and bee/fly first visitation. A PRIOR published field mechanism;
not an original adaptive-gain novel causal result or multi-species macro test.

Only source-identical Zenodo original file bytes, with original file MD5/SHA.
No user image-derived trait or fabricated 377-event rows.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import urllib.request
import urllib.error
import zipfile
from pathlib import Path

API="https://zenodo.org/api/records/5110165"
ZENODO="https://zenodo.org/"
REFERENCE_DOI="10.5281/zenodo.5110165"
PUBLICATION_DOI="10.1111/nph.17631"
MAX_FILE_BYTES=18_000_000
MAX_FILES=14
USER_AGENT="adaptive-gain-stage74-zenodo-original-2021-uv-guide-sensory-drive/2026-11-17"


def get(url,limit=MAX_FILE_BYTES):
    if not url.startswith(ZENODO):
        raise ValueError("STAGE74B_ONLY_OFFICIAL_PUBLIC_ZENODO_ORIGINAL_SOURCE")
    req=urllib.request.Request(url,headers={"User-Agent":USER_AGENT,
             "Accept":"application/json,application/octet-stream,*/*"})
    with urllib.request.urlopen(req,timeout=70) as response:
        raw=response.read(limit+1)
        final=response.geturl()
        mime=response.headers.get("Content-Type","")
    if len(raw)>limit:
        raise ValueError("STAGE74B_ORIGINAL_FILE_TOO_LARGE")
    return raw,final,mime

def errors(e):
    code=getattr(e,"code",None)
    return {"status":("HTTP_401_SOURCE_RESTRICTED" if code==401 else
                      "HTTP_403_SOURCE_DENIED" if code==403 else
                      "HTTP_404_SOURCE_NOT_FOUND" if code==404 else
                      "SOURCE_RETRIEVAL_UNRESOLVED"),
            "http_code":code,"exception_type":type(e).__name__,
            "no_biological_negative_inferred":True}


def verify_original_author_digest(source,digest):
    sha256=hashlib.sha256(source).hexdigest()
    md5=hashlib.md5(source).hexdigest()
    value=str(digest or "").strip()
    if value.startswith("md5:"):
        return md5==value.split(":",1)[1].lower(),"md5",sha256
    if value.startswith("sha256:"):
        return sha256==value.split(":",1)[1].lower(),"sha256",sha256
    if len(value)==32:
        return md5==value.lower(),"md5",sha256
    if len(value)==64:
        return sha256==value.lower(),"sha256",sha256
    return False,"NO_OFFICIAL_DIGEST",sha256


def source_members(raw,filename):
    info={}
    if filename.lower().endswith(".zip"):
        if not zipfile.is_zipfile(io.BytesIO(raw)):
            return {"status":"ORIGINAL_ARCHIVE_NOMINAL_ZIP_BUT_INVALID"}
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            members=[m for m in z.infolist() if not m.is_dir()]
            info["original_zip_members"]=[
              {"filename":m.filename,"size":m.file_size,"CRC32":m.CRC}
              for m in members[:70]]
            info["original_zip_non_directory_member_count"]=len(members)
            info["original_zip_member_metadata_only_not_extracted"]=True
    elif filename.lower().endswith((".csv",".txt",".md")):
        try:txt=raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            info["source_original_text_status"]="NOT_UTF8"
        else:
            if txt.lstrip().lower().startswith(("<html","<!doctype")):
                return {"status":"HTTP200_NOT_ORIGINAL_CSV"}
            lines=txt.splitlines()
            info["original_source_line_count"]=len(lines)
            if filename.lower().endswith(".csv"):
                reader=csv.reader(io.StringIO(txt))
                sample=[row[:20] for _,row in zip(range(4),reader)]
                info["original_csv_first_four_rows"]=sample
            else:
                info["original_text_first8lines"]=lines[:8]
    elif filename.lower().endswith((".xlsx",".xlsm")):
        if not zipfile.is_zipfile(io.BytesIO(raw)):
            return {"status":"HTTP200_NOT_XLSX"}
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            info["xlsx_original_verified"]="xl/workbook.xml" in z.namelist()
            info["original_workbook_entries"]=[x for x in z.namelist()
                if x.startswith("xl/worksheets/")][:30]
    else:
        info["source_original_format_class"]="BINARY_NOT_INTERPRETED_AS_SPECIES_EVENTS"
    return info


def record_files_metadata(meta):
    files=meta.get("files",[])
    if isinstance(files,dict):
        files=[dict(key=k,**v) if isinstance(v,dict) else {"key":k}
               for k,v in files.items()]
    return files


def manifest_meta():
    raw,final,mime=get(API,3_000_000)
    obj=json.loads(raw)
    if str(obj.get("id"))!="5110165":
        raise ValueError("STAGE74B_OFFICIAL_RECORD_DOES_NOT_MATCH_ORIGINAL_5110165")
    return obj,{"api_url":API,
                "actual_original_metadata_SHA256":hashlib.sha256(raw).hexdigest(),
                "original_metadata_bytes":len(raw)}


def pick_original_download_url(record):
    links=record.get("links") or {}
    for key in ("content","download","self"):
        uri=links.get(key)
        if isinstance(uri,str) and uri.startswith(ZENODO):
            return uri
    return None


def run():
    result={
      "schema":"stage74b_KoskiFinnell2021_Zenodo_original_UV_guide_sensory_field_source",
      "source_2021_publication_DOI":PUBLICATION_DOI,
      "source_original_data_DOI":REFERENCE_DOI,
      "source_published_design": {
        "manipulated_floral_UV_light":["ambient UV","reduced UV"],
        "guide_size_levels":["small","large"],
        "original_backgrounds":["bare substrate","foliage"],
        "elevation_strata":["low","high"],
        "reported_study_arrays":54,
        "reported_first_visits":377,
        "species_count":1,
      },
      "publication_prior_art_not_new_ecological_first":True,
      "source_original_file_metadata_retrieved":False,
      "source_original_file_receipts":[],
      "source_visitor_fitness_or_selection_effect_independently_fitted":False,
      "source_original_2021_data_not_same_replicate_as_Kent2025":True
    }
    try:meta,access=manifest_meta()
    except Exception as exc:
        result["original_metadata_access_error"]=errors(exc)
        return result
    result["source_original_file_metadata_retrieved"]=True
    result["original_API_metadata_receipt"]=access
    result["source_original_Zenodo_metadata_title"]=meta.get("metadata",{}).get("title")
    result["source_original_Zenodo_metadata_DOI"]=meta.get("doi")
    files=record_files_metadata(meta)
    result["original_Zenodo_files_count"]=len(files)
    to_pull=0
    for f in files:
        name=str(f.get("key") or f.get("filename") or "")
        size=int(f.get("size") or 0)
        checksum=str(f.get("checksum") or "")
        url=pick_original_download_url(f)
        r={"source_filename":name,"source_official_bytes":size,
            "source_original_checksum":checksum,
            "source_original_public_content_URL":url,
            "source_download_status":"NOT_ATTEMPTED"}
        if not url or size<=0 or size>MAX_FILE_BYTES or to_pull>=MAX_FILES:
            r["source_download_status"]="SOURCE_FILE_URL_OR_BUDGET_NOT_ADMITTED"
        else:
            to_pull+=1
            try:
                raw,final,mime=get(url)
                ok,algorithm,sha=verify_original_author_digest(raw,checksum)
                r.update({"source_download_status":("ORIGINAL_BYTES_CHECKSUM_AUTHENTIC"
                               if ok else "ORIGINAL_CHECKSUM_NOT_VALIDATED"),
                          "source_original_downloaded_sha256":sha,
                          "source_original_digest_algorithm":algorithm,
                          "source_actual_bytes":len(raw),
                          "source_download_content_type":mime})
                if ok:
                    r.update(source_members(raw,name))
            except Exception as exc:
                r.update(errors(exc))
                r["source_download_status"]=r["status"]
        result["source_original_file_receipts"].append(r)
    result["n_original_Zenodo_files_checksum_verified"]=sum(
        x["source_download_status"]=="ORIGINAL_BYTES_CHECKSUM_AUTHENTIC"
        for x in result["source_original_file_receipts"])
    result["source_reported_first_visits_are_author_background_until_parsed"]=True
    result["source_original_UV_treatment_does_not_identify_atmospheric_wind"]=True
    result["no_2021_manipulation_mislabeled_as_global_macro_effect"]=True
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    a.outdir.mkdir(exist_ok=True,parents=True)
    result=run()
    (a.outdir/"official_KoskiFinnell2021_original_Zenodo_UV_guide_source_receipt.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE74B_REAL_ZENODO_FOIL_UV_GUIDE_FIELD_SOURCE",
          json.dumps(result,sort_keys=True,ensure_ascii=False))
    print("NO_NEW_MULTISPECIES_CAUSAL_CLAIM_NO_IMPUTED_ECOLOGICAL_EVENTS")


if __name__=="__main__":
    main()
