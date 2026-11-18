"""Probe ORIGINAL public DoPI v2 Zenodo archive: no fake rows, no bulk transfer.

DoPI (Balfour et al) 2026 Version 2 record doi 10.5281/zenodo.22876365.
Retrieve manifest, source file identity, and bounded beginning-of-file
content schema only; full downstream overlap requires actual verified bytes.

Each original source file can be hundreds of MB. This program deliberately
does not retain any third-party original raw content in GitHub/artifacts.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,urllib.request,urllib.parse
from pathlib import Path

URL="https://zenodo.org/api/records/22876365"
REC_ID=22876365
MAX_MANIFEST=4_000_000
PREVIEW_MAX=65536
ALLOWED={"zenodo.org","www.zenodo.org"}


def request(url,peek=None):
    u=urllib.parse.urlparse(url)
    if u.scheme!="https" or u.hostname not in ALLOWED:
        raise ValueError("SOURCE_HOST_NOT_ORIGINAL_ZENODO")
    headers={"Accept":"application/json,text/csv,application/octet-stream,*/*",
             "User-Agent":"university-independent-original-pollination-meta-reanalysis/1.0"}
    if peek:headers["Range"]=f"bytes=0-{peek-1}"
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=90) as r:
        data=r.read((peek if peek else MAX_MANIFEST)+1)
        headers=dict(r.headers.items())
        return data,r.status,headers,r.geturl()


def parse_manifest():
    data,code,head,redirect=request(URL)
    if code!=200 or len(data)>MAX_MANIFEST:
        raise ValueError("DOPI_ORIGINAL_MANIFEST_CANNOT_VERIFY")
    j=json.loads(data)
    if int(j.get("id",0))!=REC_ID:
        raise ValueError("NOT_AUTHENTIC_DOPI_V2_RELEASE")
    source_files=[]
    fs=j.get("files") or []
    if not isinstance(fs,list):raise ValueError("DOPI_FILES_MISSING")
    for f in fs:
        href=(f.get("links") or {}).get("self","")
        if not href and f.get("key"):
            href=URL+"/files/"+urllib.parse.quote(f["key"],safe="")+"/content"
        if not href:continue
        source_files.append({"file_key":f.get("key"),"size":f.get("size"),
             "checksum":f.get("checksum"),"content_url":href})
    if not source_files:raise ValueError("DOPI_NO_SOURCE_FILE_LINKS")
    return {"source_original_manifest_sha256":hashlib.sha256(data).hexdigest(),
            "original_record_id":int(j["id"]),
            "original_record_doi":j.get("doi"),
            "original_record_created":j.get("created"),
            "original_record_modified":j.get("updated"),
            "original_record_license":((j.get("metadata") or {}).get("license") or {}).get("id"),
            "source_release_files":source_files}


def probe():
    info=parse_manifest()
    result={"schema":"stage84_original_dopi_v2_zenodo_source_manifest_and_bounded_headers",
      "original_release_id":REC_ID,
      "original_2026_version_2_source_found":True,
      "original_manifest":info,
      "original_preview":[]}
    for f in info["source_release_files"]:
        size=f.get("size")
        entry={"source_file_key":f["file_key"],
               "source_manifest_bytes":size,
               "source_manifest_checksum":f["checksum"],
               "actual_first_bytes_access":"NOT_YET_READ"}
        try:
            b,status,headers,final=request(f["content_url"],PREVIEW_MAX)
            entry["source_http_status"]=status
            entry["source_http_content_range"]=headers.get("Content-Range")
            entry["source_returned_preview_bytes"]=min(len(b),PREVIEW_MAX)
            entry["first_16_original_magic_hex"]=b[:16].hex()
            entry["actual_first_bytes_access"]="VERIFIED_SOURCE_HTTP_BYTES"
            if b.startswith(b"PK\x03\x04"):entry["archive_format"]="ZIP_OR_XLSX"
            elif b.startswith(b"\x1f\x8b"):entry["archive_format"]="GZIP"
            elif b[:2048].lstrip().startswith((b"{",b"[")):
                entry["archive_format"]="JSON_PLAUSIBLE"
            else:
                for enc in ("utf-8-sig","cp1252"):
                    try:
                        s=b.decode(enc)
                        lines=[x for x in s.splitlines() if x.strip()]
                        if lines:
                            try:fields=next(csv.reader([lines[0]]))
                            except csv.Error:fields=[lines[0]]
                            entry["source_first_row_fields"]=[x[:80] for x in fields[:80]]
                            entry["source_first_3_line_lengths"]=[len(x) for x in lines[:3]]
                            entry["source_partial_text_charset"]=enc
                        entry["archive_format"]="TEXT_LIKE"
                        break
                    except UnicodeDecodeError:continue
        except Exception as e:
            entry["source_preview_failure"]=type(e).__name__+":"+str(e)[:160]
            entry["actual_first_bytes_access"]="UNVERIFIED_NOT_BIOLOGICAL_ABSENCE"
        result["original_preview"].append(entry)
    result["no_original_full_bulk_dataset_redistributed"]=True
    result["no_eupp_dopi_publication_independence_yet_estimated"]=True
    result["no_author_spectrometer_219_taxa_join_yet_estimated"]=True
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    obj=probe();a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE84_REAL_DOPI_V2_MANIFEST_PROBE",json.dumps(obj,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
