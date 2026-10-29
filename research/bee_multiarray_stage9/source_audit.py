"""Stage 9: verify original Klein et al. 2017 three-array bee flower sequences.

Source is original Springer Nature Scientific Reports Supplementary Dataset S1.
PMCID PMC5496863 provides publisher-original supplementary mirror. No
invented animal IDs, source flight bearings, array coordinates or source rows.
All raw microdata transient in CI only. Keep non-identifying source receipts.
"""
from __future__ import annotations
from collections import Counter
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request
from urllib.parse import urlsplit

DOI="10.1038/s41598-017-04919-8"
PMCID="PMC5496863"
ORIGINAL_FILES=("41598_2017_4919_MOESM2_ESM.csv",
                "41598_2017_4919_MOESM3_ESM.csv")
MAX_FILE=35*1024*1024
MAX_ROWS=350000
PROVIDER_HOSTS={"static-content.springer.com","pmc.ncbi.nlm.nih.gov",
                "www.ncbi.nlm.nih.gov","cdn.ncbi.nlm.nih.gov",
                "www.ebi.ac.uk","europepmc.org"}

def official_urls(filename):
    if filename not in ORIGINAL_FILES:
        raise ValueError("NO_GO_ORIGINAL_SUPPLEMENT_FILENAME_NOT_ON_PUBLISHED_RECORD")
    return [
        "https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-017-04919-8/MediaObjects/"+filename,
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC5496863/bin/"+filename
    ]

def fetch_exact_provider_file(filename,folder):
    attempts=[]
    for url in official_urls(filename):
        try:
            request=urllib.request.Request(url,headers={
                "User-Agent":"adaptive-gain-original-scientific-reports-sequence-source/1.0",
                "Accept":"text/csv,text/plain,application/octet-stream,*/*"})
            with urllib.request.urlopen(request,timeout=65) as result:
                data=result.read(MAX_FILE+1)
                actual_url=result.url
                status=getattr(result,"status",200)
                typ=result.headers.get("Content-Type","")
            final_host=urlsplit(actual_url).hostname
            if final_host not in PROVIDER_HOSTS:
                raise ValueError("NO_GO_REDIRECT_OUTSIDE_ORIGINAL_PUBLISHER_OR_PMC")
            if not 80<=len(data)<=MAX_FILE:
                raise ValueError("NO_GO_SOURCE_FILE_ABNORMAL_SIZE")
            prefix=data[:100].lstrip().lower()
            if prefix.startswith((b"<html",b"<!doctype html",b"<?xml",b"<!doctype")):
                raise ValueError("NO_GO_PROVIDER_RETURNED_LANDING_HTML_NOT_DATA")
            if b"\0" in data[:600]:
                raise ValueError("NO_GO_ORIGINAL_SOURCE_CONTAINS_NUL_BYTES")
            destination=folder/filename
            destination.write_bytes(data)
            receipt={
                "publisher_source":url,
                "final_publisher_host":final_host,
                "http_status":status,
                "content_type":typ,
                "source_bytes":len(data),
                "source_sha256":hashlib.sha256(data).hexdigest(),
                "source_file":filename,
                "original_paper_doi":DOI,
                "original_PMC_id":PMCID,
                "is_publisher_original_source":True,
                "prior_provider_route_failures":attempts
            }
            return data,receipt
        except Exception as error:
            attempts.append({"provider_url":url,
                             "exception":type(error).__name__,
                             "http_status":getattr(error,"code",None),
                             "why":str(error)[:220]})
    raise ValueError("NO_GO_ORIGINAL_SUPPLEMENT_UNAVAILABLE "+
                     json.dumps({"file":filename,"attempts":attempts}))

def decode_and_audit_csv(data):
    txt=None
    encoding=None
    for enc in ("utf-8-sig","cp1252","latin-1"):
        try:
            txt=data.decode(enc,"strict")
            encoding=enc
            break
        except UnicodeDecodeError:
            pass
    if txt is None:raise ValueError("NO_GO_ORIGINAL_SOURCE_DECODING")
    try:
        delim=csv.Sniffer().sniff(txt[:12000],delimiters=",;\t").delimiter
    except csv.Error:
        delim=","
    reader=csv.reader(io.StringIO(txt,newline=""),delimiter=delim)
    head=next(reader,None)
    if not head:raise ValueError("NO_GO_ORIGINAL_SOURCE_HAS_NO_HEADER")
    columns=[x.strip() for x in head]
    row_width=Counter()
    head_preview=[]
    rows=0
    nonempty=[0]*len(columns)
    exact_duplicate_rows=0
    seen=set()
    first_values=[]
    for row in reader:
        if not row or (len(row)==1 and not row[0].strip()):
            continue
        rows+=1
        if rows>MAX_ROWS:raise ValueError("NO_GO_TOO_MANY_ORIGINAL_VISIT_ROWS")
        row_width[len(row)]+=1
        if len(row)!=len(columns):
            if len(head_preview)<5:
                head_preview.append({"source_line":rows+1,"width":len(row),
                                     "header_width":len(columns)})
            continue
        key=tuple(x.strip() for x in row)
        if key in seen:exact_duplicate_rows+=1
        else:seen.add(key)
        for i,value in enumerate(key):
            if value.casefold() not in ("","na","nan","n/a","null","none"):
                nonempty[i]+=1
        if rows<=3:
            first_values.append([x[:45] for x in key[:12]])
    # This is a schema/grain audit only: do NOT infer 29 bees or true
    # visits from the observed first source column until source semantics
    # and actual row/column role have been checked explicitly.
    return {
        "status":"ORIGINAL_SOURCE_STRUCTURE_INSPECTED",
        "source_encoding":encoding,
        "source_delimiter":repr(delim),
        "source_header":columns[:120],
        "source_header_total_columns":len(columns),
        "total_source_nonblank_rows":rows,
        "row_width_histogram":dict(sorted(row_width.items())),
        "original_identical_rows_count_not_removed":exact_duplicate_rows,
        "nonmissing_per_source_column_first120":{
            str(c or f"__unnamed_{i}"):nonempty[i]
            for i,c in enumerate(columns[:120])},
        "bounded_first_values_not_interpreted_as_bee_ids":first_values,
        "row_width_mismatch_examples":head_preview,
        "source_grain_inference":"NOT_YET_VALIDATED",
        "unparsed_original_flower_array_positions":"NOT_INCLUDED",
        "one_bee_one_bout_one_row_NOT_ASSUMED":True
    }

def run(folder):
    folder.mkdir(exist_ok=True,parents=True)
    report={"status":"SOURCE_FETCH_STARTED",
            "study_doi":DOI,"source_original_datasets":{},
            "no_spatial_or_behavioral_result_fitted":True}
    outfile=folder/"klein2017_source_gate.json"
    outfile.write_text(json.dumps(report,indent=2,ensure_ascii=False))
    try:
        for name in ORIGINAL_FILES:
            data,receipt=fetch_exact_provider_file(name,folder)
            schema=decode_and_audit_csv(data)
            report["source_original_datasets"][name]={
                "byte_provenance":receipt,"source_schema":schema}
            outfile.write_text(json.dumps(report,indent=2,ensure_ascii=False))
            print("STAGE9_ORIGINAL_SUPPLEMENT "+
                  json.dumps({"name":name,"receipt":receipt,
                              "source_schema":schema},ensure_ascii=False),flush=True)
        report["status"]="SOURCE_ORIGINAL_2017_S1_S2_VERIFIED"
    except Exception as error:
        report["status"]="NO_GO_ORIGINAL_SOURCE_RETRIEVAL_OR_SCHEMA"
        report["failed_gate_reason"]=str(error)[:3500]
        outfile.write_text(json.dumps(report,indent=2,ensure_ascii=False))
        print("STAGE9_ORIGINAL_SOURCE_NO_GO "+str(error),flush=True)
        raise
    outfile.write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print("STAGE9_ORIGINAL_SOURCE_GATE_COMPLETE",flush=True)
    return report

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="bee_stage9_original")
    args=parser.parse_args()
    run(Path(args.out))
