"""Fail-closed schema and zero-count source gate for UK PoMS 2017–2023 FIT.

No field ecology inference is permitted from this download-only step. We must
read the source schema and zero/effort semantics before specifying an estimator.
"""
from __future__ import annotations
import csv, hashlib, io, json, os, pathlib, sys, urllib.request, urllib.error, zipfile
from collections import Counter

DOI = "10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618"
UUID = "d706088c-9d48-4be5-b156-6ed6ad5e0618"
DATA_URL = "https://data-package.ceh.ac.uk/data/" + UUID + ".zip"
SUPPORT_URL = "https://data-package.ceh.ac.uk/sd/" + UUID + ".zip"
MAX_DOWNLOAD = 300_000_000
MAX_UNCOMPRESSED = 700_000_000

def read_download(url, name, directory):
    dest = directory / name
    request = urllib.request.Request(url, headers={
        "User-Agent": "adaptive-gain-poms-original-data-audit/1.0",
        "Accept": "application/zip,application/octet-stream,*/*"})
    entry = {"url":url, "file":name}
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            entry.update({"http_status":response.status, "final_url":response.geturl(),
                 "content_type":response.headers.get("Content-Type"),
                 "declared_size":response.headers.get("Content-Length")})
            length=0
            with dest.open("wb") as out:
                while True:
                    buf=response.read(1024*1024)
                    if not buf: break
                    length += len(buf)
                    if length > MAX_DOWNLOAD:
                        raise ValueError("DATASET_EXCEEDS_SAFETY_SIZE_LIMIT")
                    out.write(buf)
        raw=dest.read_bytes()
        entry.update({"bytes":len(raw), "sha256":hashlib.sha256(raw).hexdigest(),
            "first_bytes_hex":raw[:12].hex(), "is_zip":zipfile.is_zipfile(dest)})
        if not entry["is_zip"]:
            entry["status"]="NOT_ZIP_NO_ANALYSIS"
            entry["preview_ascii"]=raw[:120].decode("ascii", errors="replace")
        else: entry["status"]="ZIP_DOWNLOADED"
    except (OSError, ValueError, urllib.error.URLError) as exc:
        entry.update({"status":"ACCESS_BLOCKED","error_type":type(exc).__name__,
                      "error":str(exc)[:450]})
        if dest.exists(): dest.unlink()
    return entry

def csv_member_profile(z, member):
    """Only return header, row count, missing and numeric-zero rates; never rows."""
    # The original PoMS CSV can contain non-UTF8 Windows smart quotes beyond
    # the first few kB. Validate *the entire member* before selecting a codec.
    data=z.read(member)
    try:decoded=data.decode("utf-8");encoding="utf-8"
    except UnicodeDecodeError:decoded=data.decode("latin-1");encoding="latin-1"
    total=0;header=[];samples=[];missing=Counter()
    reader=csv.reader(io.StringIO(decoded,newline=""))
    try:header=next(reader)
    except StopIteration:return {"rows":0,"columns":[]}
    for record in reader:
        if len(record)!=len(header): raise ValueError("CSV_FIELD_COUNT_MISMATCH:"+member)
        total+=1
        for k,v in enumerate(record):
            if not v.strip():missing[header[k]]+=1
        if len(samples)<2000:samples.append(record)
    numeric={}
    for j,name in enumerate(header):
        good=0;zero=0;nonempty=0;negative=0
        for record in samples:
            value=record[j].strip()
            if not value:continue
            nonempty+=1
            try:
                v=float(value)
                if not (float("-inf")<v<float("inf")):continue
                good+=1
                if v==0:zero+=1
                if v<0:negative+=1
            except ValueError:pass
        if nonempty>0 and good/nonempty>.95:
            numeric[name]={"n_sample":nonempty,"zero_fraction_sample":zero/nonempty,
                           "negative_sample":negative,"numeric_fraction_sample":good/nonempty}
    return {"rows":total,"columns":header,"encoding":encoding,
            "missing_by_field":dict(missing),"sample_numeric_zero_summary":numeric}

def inventory_zip(path):
    with zipfile.ZipFile(path) as z:
        fileinfo=z.infolist()
        total=sum(x.file_size for x in fileinfo)
        if total>MAX_UNCOMPRESSED: raise ValueError("UNCOMPRESSED_SIZE_EXCEEDS_LIMIT")
        members=[]
        for info in fileinfo:
            entry={"name":info.filename,"uncompressed_bytes":info.file_size,
                   "compressed_bytes":info.compress_size,"crc32":format(info.CRC,"08x")}
            if info.filename.lower().endswith(".csv") and info.file_size<=90_000_000:
                entry["csv_profile"]=csv_member_profile(z,info.filename)
            members.append(entry)
        return {"files":members,"uncompressed_total":total}

def main():
    directory=pathlib.Path(os.environ.get("POMS_OUT","poms_source_gate"));directory.mkdir(exist_ok=True,parents=True)
    results={"doi":DOI,"scope":"Source acquisition/schema only; zero ecological inference",
             "source":"EIDC official data-package",
             "licence":"Open Government Licence; institutional data acknowledgement required",
             "permission_policy":"Do not bypass EIDC auth or licence acceptance"}
    for url,name,key in ((DATA_URL,"fit_original_data.zip","data"),(SUPPORT_URL,"supporting_information.zip","support")):
        entry=read_download(url,name,directory)
        if entry["status"]=="ZIP_DOWNLOADED":
            try:entry["inventory"]=inventory_zip(directory/name)
            except Exception as exc:entry["status"]="SCHEMA_ERROR";entry["error"]=str(exc)[:600]
        results[key]=entry
        print("ACCESS_GATE",key,entry["status"],entry.get("bytes"),entry.get("error",""),flush=True)
        for member in entry.get("inventory",{}).get("files",[]):
            cp=member.get("csv_profile",{})
            print("ZIP_MEMBER",json.dumps({"archive":key,"name":member["name"],
                "bytes":member["uncompressed_bytes"],"rows":cp.get("rows"),
                "columns":cp.get("columns"),"encoding":cp.get("encoding"),
                "numeric_zero_sample":cp.get("sample_numeric_zero_summary")},ensure_ascii=False),flush=True)
    (directory/"source_gate.json").write_text(json.dumps(results,indent=2,ensure_ascii=False))
    if results["data"]["status"]=="ZIP_DOWNLOADED":
        print("POMS_SOURCE_GATE_COMPLETE",flush=True)
    else:
        print("POMS_SOURCE_ACCESS_BLOCKED",flush=True)
        # Fail closed with a successfully archived diagnostic, not a fake result.
if __name__=="__main__":main()
