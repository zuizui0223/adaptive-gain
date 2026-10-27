"""Inspect official UK PoMS 2017-2023 pan-trap flowering-community records.

Stage 3f SOURCE GATE ONLY. Never claim shared-square flowering plants are a
FIT insect's observed choice set. No raw microdata are committed to Git.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import time
import urllib.request
import zipfile

PAN_DOI = "10.5285/5841bfae-471b-498c-af89-c30e5140d6c5"
PAN_URL = "https://data-package.ceh.ac.uk/data/5841bfae-471b-498c-af89-c30e5140d6c5.zip"
FIT_URL = "https://data-package.ceh.ac.uk/data/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip"
FIT_1KM_NAME = "data/ukpoms_1kmfitcountdata_2017-2023.csv"
FIT_1KM_SHA256 = "29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52"

COMPRESSED_LIMIT = 300 * 1024 * 1024
TOTAL_EXPANDED_LIMIT = 1400 * 1024 * 1024
PREVIEW_LIMIT = 6000
COLUMN_HINT = re.compile(r"date|day|year|site|station|survey|sample|square|grid|loc|flower|plant|taxon|species|visit|record|event|occ|start|end|trap|habitat|status|type|name", re.I)
CATEGORY_HINT = re.compile(r"flowering|status|type|trap|visit|occurrence|survey", re.I)

def download(url:str, dest:Path):
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        last=None
        for attempt in range(3):
            try:
                req=urllib.request.Request(url,headers={
                    "User-Agent":"adaptive-gain-cross-source-scientific-audit/1.0",
                    "Accept":"application/zip,application/octet-stream,*/*"})
                with urllib.request.urlopen(req,timeout=120) as response, dest.open("wb") as out:
                    total=0
                    while True:
                        part=response.read(1024*1024)
                        if not part:break
                        total+=len(part)
                        if total>COMPRESSED_LIMIT:raise ValueError("compressed archive cap exceeded")
                        out.write(part)
                if not zipfile.is_zipfile(dest):raise ValueError("returned content is not a ZIP")
                last=None;break
            except Exception as exc:
                last=exc
                dest.unlink(missing_ok=True)
                time.sleep(2*(attempt+1))
        if last:raise RuntimeError(f"source retrieval failed: {last}") from last
    if dest.stat().st_size>COMPRESSED_LIMIT or not zipfile.is_zipfile(dest):
        raise ValueError("cached source failed archive guard")
    h=hashlib.sha256()
    with dest.open("rb") as inp:
        for chunk in iter(lambda:inp.read(1024*1024),b""):h.update(chunk)
    return {"source":url,"size":dest.stat().st_size,"zip_sha256_receipt":h.hexdigest(),
            "source_hash_policy":"uncompressed CSV member SHA256 is identity; dynamically regenerated ZIP wrapper is only a receipt"}

def zip_guard(z:zipfile.ZipFile):
    files=z.infolist()
    if sum(x.file_size for x in files)>TOTAL_EXPANDED_LIMIT:
        raise ValueError("expanded source cap exceeded")
    if len({f.filename for f in files})!=len(files):
        raise ValueError("archive has duplicate member names")

def sha_member(z, filename):
    h=hashlib.sha256()
    with z.open(filename) as data:
        for part in iter(lambda:data.read(1024*1024),b""):h.update(part)
    return h.hexdigest()

def decode_preview(z, filename:str, max_bytes=640_000):
    with z.open(filename) as raw:
        b=raw.read(max_bytes)
    for enc in ("utf-8","cp1252","latin-1"):
        try:
            t=b.decode(enc)
            return t,enc
        except UnicodeDecodeError:continue
    raise ValueError("cannot strictly decode first CSV bytes")

def csv_preview(z, filename:str):
    txt,encoding=decode_preview(z,filename)
    # May end in partial CSV row; drop partial physical final line.
    if not txt.endswith("\n"):
        txt=txt.rsplit("\n",1)[0]+"\n"
    sample=list(csv.reader(io.StringIO(txt)))
    if not sample:raise ValueError(f"no header in {filename}")
    header=sample[0]
    rows=[r for r in sample[1:] if len(r)==len(header)][:PREVIEW_LIMIT]
    if len(set(header))!=len(header):raise ValueError("duplicate CSV column names")
    focus=[c for c in header if COLUMN_HINT.search(c)]
    fields=[]
    for c in focus:
        idx=header.index(c)
        vals=[r[idx].strip() for r in rows]
        present=[v for v in vals if v not in ("","NA","nan","null","NULL")]
        counts=Counter(present)
        field={
            "column":c,"sample_nonempty":len(present),
            "sample_unique":len(counts),
            "sample_empty":len(vals)-len(present),
            "sample_count":len(vals)}
        if CATEGORY_HINT.search(c) and len(counts)<=24:
            # Only source categories, never sample IDs, grid refs or observer IDs.
            field["category_levels"]={k:v for k,v in counts.most_common(18)}
        if re.search(r"(^|_)date|day|year",c,re.I):
            field["time_format_sample"]=[x for x in sorted(set(present))[:3]]
        fields.append(field)
    return {"encoding_preview":encoding,"sample_rows":len(rows),
            "column_count":len(header),"columns":header,
            "key_field_profiles":fields}

def inspect_archive(path:Path):
    report={"package":str(path.name),"members":[]}
    with zipfile.ZipFile(path) as z:
        zip_guard(z)
        for f in z.infolist():
            if f.is_dir():continue
            meta={"filename":f.filename,"size":f.file_size,"crc32":f"{f.CRC:08x}",
                  "sha256_uncompressed_member":sha_member(z,f.filename)}
            if f.filename.lower().endswith(".csv"):
                meta["csv"]=csv_preview(z,f.filename)
            report["members"].append(meta)
    report["csv_members"]=sum("csv" in r for r in report["members"])
    return report

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="poms_pan_join_audit")
    args=p.parse_args(argv)
    root=Path(args.out)
    root.mkdir(parents=True,exist_ok=True)
    all_results={"stage":"source_schema_only",
                 "pan_source_doi":PAN_DOI,
                 "fit_source_doi":"10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618",
                 "fit_expected_original_csv_sha256":FIT_1KM_SHA256,
                 "not_insect_simultaneous_available_choices":True}
    for key,url in [("pan",PAN_URL),("fit",FIT_URL)]:
        source=root/(key+"_original_provider.zip")
        receipt=download(url,source)
        profile=inspect_archive(source)
        all_results[key]={"retrieval":receipt,"inventory":profile}
        print("POMS_PAN_PACKAGE "+json.dumps({
            "source":key,"receipt":receipt,
            "members":[{"file":r["filename"],"size":r["size"],"sha256":r["sha256_uncompressed_member"],
                        "columns":r.get("csv",{}).get("columns",[])} for r in profile["members"]]
        },ensure_ascii=False),flush=True)
    fit_members={r["filename"]:r["sha256_uncompressed_member"]
                 for r in all_results["fit"]["inventory"]["members"]}
    if fit_members.get(FIT_1KM_NAME)!=FIT_1KM_SHA256:
        raise ValueError("original structured FIT member no longer matches pinned bytes")
    if all_results["pan"]["inventory"]["csv_members"]==0:
        raise ValueError("no original pan survey CSV present")
    out=root/"pan_and_fit_source_inventory.json"
    out.write_text(json.dumps(all_results,ensure_ascii=False,indent=2,allow_nan=False))
    print("POMS_PAN_SCHEMA_AUDIT_COMPLETE",flush=True)

if __name__=="__main__":
    main()
