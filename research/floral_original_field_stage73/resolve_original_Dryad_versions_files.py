"""Stage73 original-public Dryad files version + byte-integrity discovery.

Research sources:
Xie 2025 doi:10.5061/dryad.612jm64gq (China 41 islands+16 mainland sites),
Albor 2022 doi:10.5061/dryad.2ngf1vhrb (California field optics+pollinators).

Only original publisher-linked Dryad API v2/version-file listings, *source*
checksums/filenames and bytes. A Dryad public metadata entry is not a
downloaded file. HTTP 200 HTML is not XLSX. HTTP401 is ACCESS DENIAL, not
evidence that biological measurements are absent.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

BASE="https://datadryad.org"
DOI_FILES={
    "xie_island_2025":{
       "doi":"10.5061/dryad.612jm64gq",
       "expected":{
        "bee_visitation_frequency_to_each_floral_color_within_each_island.xlsx",
        "flower_color_reflectance_spectra.xlsx",
        "plant_bee_interactions_on_islands.zip",
        "README.md",
       },
    },
    "albor_california_2022":{
       "doi":"10.5061/dryad.2ngf1vhrb",
       "expected":{
        "Data_Albor_etal_2022.xlsx",
        "README_Albor_etal.2020_FuncEcol.txt",
       },
    }
}
MAX_DATA=18_000_000
MAX_JSON=1_500_000
UA="adaptive-gain-authentic-public-original-Dryad-stage73/2026-11-17"


def api_get(url, max_len=MAX_JSON):
    if not url.startswith(BASE+"/api/v2/"):
        raise ValueError("STAGE73_DRYAD_NON_ORIGINAL_API_ENDPOINT")
    request=urllib.request.Request(url,headers={"User-Agent":UA,
                     "Accept":"application/json,*/*"})
    with urllib.request.urlopen(request,timeout=40) as response:
        raw=response.read(max_len+1)
        final=response.geturl()
    if len(raw)>max_len:
        raise ValueError("STAGE73_DRYAD_SOURCE_EXCEEDS_SIZE_BOUND")
    return raw,final


def receipt(url, data, claimed_digest=""):
    sha=hashlib.sha256(data).hexdigest()
    state={"status":"ORIGINAL_BYTES_RETRIEVED",
      "source_endpoint":url, "actual_bytes":len(data),
      "downloaded_source_sha256":sha}
    if claimed_digest:
        state["official_metadata_digest"]=claimed_digest
        if len(claimed_digest)==64:
            state["official_metadata_sha256_matches"]=sha==claimed_digest
        elif len(claimed_digest)==32:
            state["official_metadata_md5_matches"]=hashlib.md5(data).hexdigest()==claimed_digest
        else:
            state["official_metadata_digest_format_unverified"]=True
    return state


def failure(url,e):
    code=getattr(e,"code",None)
    return {"status":("PUBLIC_FILE_ACCESS_401" if code==401 else
             "PUBLIC_FILE_ACCESS_403" if code==403 else
             "PUBLIC_FILE_NOT_FOUND_404" if code==404 else
             "ORIGINAL_SOURCE_FETCH_ERROR"),"source_endpoint":url,
             "error_class":type(e).__name__,
             "http_code":code, "no_biological_missingness_inferred":True}


def json_get(url):
    raw,_=api_get(url)
    o=json.loads(raw)
    if not isinstance(o,(dict,list)):
        raise ValueError("STAGE73_SOURCE_RESPONSE_NOT_JSON_CONTAINER")
    return o,receipt(url,raw)


def list_versions(doi):
    ident=urllib.parse.quote("doi:"+doi,safe="")
    url=BASE+"/api/v2/datasets/"+ident+"/versions"
    versions,rec=json_get(url)
    if not isinstance(versions,dict):
        raise ValueError("STAGE73_DRYAD_VERSIONS_UNEXPECTED_RESPONSE")
    # Raw schema retained in compact diagnostic metadata, not guessed.
    embedded=versions.get("_embedded") or {}
    candidates=[]
    for k,v in embedded.items():
        if "version" in k.lower() and isinstance(v,list):
            candidates+=v
    if isinstance(versions.get("versions"),list):
        candidates+=versions["versions"]
    version_ids=set()
    for d in candidates:
        if not isinstance(d,dict):continue
        for key in ("id","versionId"):
            if str(d.get(key,"")).isdecimal():
                version_ids.add(int(d[key]))
        for v in (d.get("_links") or {}).values():
            href=v.get("href") if isinstance(v,dict) else ""
            if "/api/v2/versions/" in str(href):
                suf=str(href).split("/api/v2/versions/",1)[1].split("/",1)[0]
                if suf.isdecimal():version_ids.add(int(suf))
    return sorted(version_ids),{"response_top_keys":sorted(versions),
        "response_embedded_keys":sorted(embedded),
        "version_candidate_count":len(candidates),
        "official_access_receipt":rec}


def list_file_metadata(version):
    url=BASE+f"/api/v2/versions/{version}/files?per_page=100"
    o,rec=json_get(url)
    embedded=o.get("_embedded") or {}
    candidates=[]
    for k,v in embedded.items():
        if "file" in k.lower() and isinstance(v,list):candidates+=v
    if isinstance(o.get("files"),list):candidates+=o["files"]
    files=[]
    for d in candidates:
        if not isinstance(d,dict):continue
        file_id=None
        for key in ("id","fileId"):
            if str(d.get(key,"")).isdecimal():
                file_id=int(d[key])
        links=d.get("_links") or {}
        self_link=links.get("self") or {}
        if file_id is None and isinstance(self_link,dict):
            href=str(self_link.get("href",""))
            suffix=href.rstrip("/").rsplit("/",1)[-1]
            if suffix.isdecimal():file_id=int(suffix)
        files.append({"file_id":file_id,
            "path":d.get("path") or d.get("fileName") or d.get("name"),
            "size":d.get("size"),"digest":d.get("digest"),
            "digest_type":d.get("digestType"),
            "status":d.get("status"),
            "source_download_link":str((links.get("stash:download") or {}).get("href","")),
            "source_metadata_keys":sorted(d)})
    return files,{"response_top_keys":sorted(o),
       "response_embedded_keys":sorted(embedded),
       "original_file_metadata_count":len(files),
       "original_file_metadata_receipt":rec}


def classify_file_bytes(raw, filename):
    filename=filename.lower()
    if filename.endswith(".xlsx"):
        if not zipfile.is_zipfile(io.BytesIO(raw)):
            return "HTTP_SUCCESS_NOT_EXCEL_BINARY"
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            return "ORIGINAL_XLSX_OOXML_CONFIRMED" if "xl/workbook.xml" in z.namelist() else "ZIP_NOT_XLSX"
    if filename.endswith(".zip"):
        if not zipfile.is_zipfile(io.BytesIO(raw)):
            return "HTTP_SUCCESS_NOT_ZIP"
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            return "ORIGINAL_ZIP_CONFIRMED_MEMBER_COUNT_"+str(len(z.namelist()))
    if filename.endswith((".txt",".md",".csv")):
        try:raw.decode("utf-8-sig")
        except UnicodeDecodeError:return "SOURCE_TEXT_NOT_UTF8_UNKNOWN"
        if raw[:10].lstrip().lower().startswith((b"<!doctype",b"<html")):
            return "HTTP_SUCCESS_HTML_NOT_ORIGINAL_TEXT"
        return "ORIGINAL_SOURCE_TEXT_UTF8"
    return "SOURCE_FORMAT_NOT_AUTOMATICALLY_CLASSIFIED"


def download_exact_file(fid,metadata):
    url=BASE+f"/api/v2/files/{fid}/download"
    raw,final=api_get(url,MAX_DATA)
    r=receipt(url,raw,str(metadata.get("digest") or ""))
    r["original_source_file_class"]=classify_file_bytes(raw,str(metadata.get("path") or ""))
    r["original_source_filename"]=metadata.get("path")
    # Do not count a nominal HTTP 200 as source admission if HTML.
    r["real_source_file_admitted"]=r["original_source_file_class"].startswith(
        ("ORIGINAL_XLSX","ORIGINAL_ZIP","ORIGINAL_SOURCE_TEXT"))
    r["official_checksum_comparison_failed"] = (
        r.get("official_metadata_sha256_matches") is False or
        r.get("official_metadata_md5_matches") is False
    )
    if r["official_checksum_comparison_failed"]:
        r["real_source_file_admitted"]=False
    return r,raw


def try_dataset_download(doi):
    ident=urllib.parse.quote("doi:"+doi,safe="")
    url=BASE+"/api/v2/datasets/"+ident+"/download"
    raw,final=api_get(url,MAX_DATA)
    r=receipt(url,raw)
    r["original_archive_kind"]=classify_file_bytes(raw,"dataset.zip")
    r["real_source_archive_admitted"]=r["original_archive_kind"].startswith("ORIGINAL_ZIP_CONFIRMED")
    if r["real_source_archive_admitted"]:
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            r["official_download_package_members"]=[
                 {"path":f.filename,"size":f.file_size}
                 for f in z.infolist() if not f.is_dir()][:30]
    return r


def run():
    out={}
    for name,source in DOI_FILES.items():
        doi=source["doi"]
        row={"original_dataset_DOI":doi,
             "expected_source_file_names":sorted(source["expected"]),
             "source_original_file_version_status":"NO_METADATA_YET",
             "file_source_bytes":[],
             "no_original_file_data_implies_no_biological_negative":True}
        try:
            mainmeta,rec=json_get(BASE+"/api/v2/datasets/"+urllib.parse.quote("doi:"+doi,safe=""))
            row["original_dataset_metadata_receipt"]=rec
            row["original_dataset_metadata_title"]=mainmeta.get("title")
            row["original_dataset_meta_top_keys"]=sorted(mainmeta)
            row["official_versionNumber"]=mainmeta.get("versionNumber")
            row["official_metadata_links"]=sorted((mainmeta.get("_links") or {}))
            embed=mainmeta.get("_embedded") or {}
            row["official_metadata_embedded_links"]=sorted(embed)
            version_ids,vmeta=list_versions(doi)
            row["original_versions_list"]=vmeta
            row["original_version_ids"]=version_ids
            if not version_ids:
                row["source_original_file_version_status"]="NO_RESOLVED_VERSION_ID"
            for version in version_ids[-3:]:
                f,info=list_file_metadata(version)
                row.setdefault("original_version_file_lists",[]).append({
                   "source_version_id":version,
                   "original_list_audit":info,
                   "original_metadata_files":f})
                names={str(d.get("path","")).rsplit("/",1)[-1] for d in f}
                row["original_source_expected_file_names_in_resolved_version"]=sorted(names&source["expected"])
                if names&source["expected"]:
                    row["source_original_file_version_status"]="OFFICIAL_VERSION_FILE_RECORDS_FOUND"
                for meta in f:
                    file_name=str(meta.get("path") or "").rsplit("/",1)[-1]
                    if file_name not in source["expected"]:continue
                    fid=meta.get("file_id")
                    if fid is None:
                        row["file_source_bytes"].append({"status":"NO_SOURCE_FILE_ID",
                            "original_source_filename":file_name})
                        continue
                    try:
                        r,_=download_exact_file(fid,meta)
                        r["file_id"]=fid
                    except Exception as e:
                        r=failure(BASE+f"/api/v2/files/{fid}/download",e)
                        r["original_source_filename"]=file_name
                        r["file_id"]=fid
                    row["file_source_bytes"].append(r)
        except Exception as exc:
            row["official_original_metadata_error"]=failure(
                BASE+"/api/v2/datasets/"+urllib.parse.quote("doi:"+doi,safe=""),exc)
        try:
            row["alternative_official_full_dataset_package"]=try_dataset_download(doi)
        except Exception as exc:
            row["alternative_official_full_dataset_package"]=failure(
                 BASE+"/api/v2/datasets/"+urllib.parse.quote("doi:"+doi,safe="")+"/download",exc)
        row["any_original_content_admitted"]=any(
             r.get("real_source_file_admitted") for r in row["file_source_bytes"]) or (
             row["alternative_official_full_dataset_package"].get("real_source_archive_admitted") is True)
        out[name]=row
    return {"schema":"stage73_original_dryad_v2_file_grain_and_binary_source_admission",
      "source_dataset_count":len(out),
      "source_public_metadata_not_binary":True,
      "source_401_does_not_prove_source_nonexistence":True,
      "no_source_photographs_or_inferred_traits":True,
      "no_biological_effect_or_false_pvalue_fitted":True,
      "source_results":out}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    a.outdir.mkdir(parents=True,exist_ok=True)
    d=run()
    (a.outdir/"original_Dryad_v2_Xie_Albor_source_manifest_and_binary_status.json").write_text(
        json.dumps(d,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE73_SOURCE_AUTHENTIC_DRYAD_API_VERSIONS_FILES_BINARY_PROBE",
          json.dumps(d,sort_keys=True,ensure_ascii=False))
    print("NO_SOURCE_METRICS_ASSUMED_FROM_ABSTRACT_NO_UNKNOWN_AS_ZERO")


if __name__=="__main__":
    main()
