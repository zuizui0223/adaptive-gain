"""Recover original public data from independent plant–predator–pollinator systems.

The script records byte digests, raw headers and all row counts before analysis.
Never replace a failed or non-CSV file with example data.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, time, urllib.request
from pathlib import Path

SOURCES={
 "rieken_2026":{
  "doi":"10.5061/dryad.1c59zw4bt",
  "files":{
   "data.csv":4965081,
   "code.R":4965082,
   "README.md":4965085}},
 "hulting_2024":{
  "doi":"10.5061/dryad.zpc866tg0",
  "files":{
   "CLE_crabspider.csv":2887401,
   "CLE_floral.csv":2887402,
   "CLE_pollinator.csv":2887403,
   "CLE_summarized.csv":2887396,
   "README.md":2887470}}}
MAX_SIZE=3_000_000

def fetch(file_id):
    url=f"https://datadryad.org/downloads/file_stream/{file_id}"
    last=None
    for i in range(3):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"adaptive-gain-original-data-research/1.0","Accept":"text/csv,text/plain,*/*"})
            with urllib.request.urlopen(req,timeout=80) as r:
                body=r.read(MAX_SIZE+1)
                if len(body)>MAX_SIZE:raise ValueError("SOURCE_EXCEEDS_LIMIT")
                return body,{"download_url":r.geturl(),"content_type":r.headers.get("Content-Type"),
                    "content_disposition":r.headers.get("Content-Disposition")}
        except Exception as ex:
            last=ex
            time.sleep((i+1)*2)
    raise RuntimeError(f"file_stream/{file_id}: {last}")

def csv_profile(raw):
    try:s=raw.decode("utf-8-sig");enc="utf-8-sig"
    except UnicodeDecodeError:s=raw.decode("latin-1");enc="latin-1"
    if s.lstrip().lower().startswith(("<!doctype","<html","<?xml")):
        raise ValueError("NOT_CSV_HTML_RESPONSE")
    dialect=csv.Sniffer().sniff(s[:5000],delimiters=",;\t")
    rows=list(csv.reader(io.StringIO(s),dialect))
    if not rows:raise ValueError("EMPTY_CSV")
    if len(rows[0])<3:raise ValueError("NOT_TABULAR_CSV")
    if any(len(x)!=len(rows[0]) for x in rows[1:]):
        raise ValueError("INCONSISTENT_CSV_WIDTH")
    return {"encoding":enc,"rows":len(rows)-1,"columns":rows[0],"width":len(rows[0])}

def main(argv=None):
    ap=argparse.ArgumentParser();ap.add_argument("--out",default="wind_indirect_original")
    args=ap.parse_args(argv)
    root=Path(args.out);root.mkdir(parents=True,exist_ok=True)
    receipt={"status":"RAW_SOURCE_QC_NO_INFERENCES","sources":{}}
    for source,cfg in SOURCES.items():
        out=root/source;out.mkdir(exist_ok=True)
        result={"doi":cfg["doi"],"files":{}}
        for filename,fid in cfg["files"].items():
            raw,headers=fetch(fid)
            if filename.endswith(".csv"):
                profile=csv_profile(raw)
            else:
                if raw.lstrip().lower().startswith(b"<!doctype html"):
                    raise ValueError(f"HTML_INSTEAD_OF_{filename}")
                profile={}
            dest=out/filename;dest.write_bytes(raw)
            details={"file_stream_id":fid,"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
                     "md5":hashlib.md5(raw).hexdigest(),**headers,**profile}
            result["files"][filename]=details
            print("SOURCE_FILE",source,filename,json.dumps(details,ensure_ascii=False),flush=True)
        receipt["sources"][source]=result
    (root/"receipt.json").write_text(json.dumps(receipt,indent=2,ensure_ascii=False))
    print("ALL_ORIGINAL_SOURCES_VERIFIED",flush=True)

if __name__=="__main__":main()
