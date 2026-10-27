"""Original publisher-source ingest and source-grain audit for individual bee routes.

No guessed bee IDs, floral labels, interaction semantics or cue order.
All datasets live in ephemeral CI run; Git stores only code/protocol.
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

SOURCE_DOI = "10.1186/s40462-019-0150-z"
FILE_NAME = "40462_2019_150_MOESM2_ESM.csv"
SOURCE_URLS = [
    "https://static-content.springer.com/esm/art%3A10.1186%2Fs40462-019-0150-z/MediaObjects/40462_2019_150_MOESM2_ESM.csv",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC6383269/bin/40462_2019_150_MOESM2_ESM.csv",
]
MAX_DOWNLOAD_BYTES=3*1024*1024
MISSING={"", "na", "n/a", "nan", "null", "none", ".", "not recorded"}
ID_HINT=re.compile(r"bee|forag|individ|tag|visitor|flower|plant|event|bout|interaction|date|day|time|hour|start|end|arrival|depart|resident|duration|position|status|outcome|visit|nest", re.I)
SENSITIVE_VALUES=re.compile(r"bee|individ|tag|visitor|flower|date|day|time|start|end|arriv|depart|bout|type|status|interaction|outcome", re.I)
MAX_DATA_ROWS=100_000

def download_source(out:Path,urls=SOURCE_URLS):
    """Try original public supplementary file mirrors with immutable-byte receipt."""
    out.mkdir(parents=True,exist_ok=True)
    errors=[]
    for url in urls:
        for attempt in range(2):
            try:
                req=urllib.request.Request(url,headers={
                    "User-Agent":"adaptive-gain-independent-bee-trajectory-source-check/1.0",
                    "Accept":"text/csv,text/plain,application/octet-stream,*/*"})
                with urllib.request.urlopen(req,timeout=45) as res:
                    typ=res.headers.get("Content-Type","")
                    raw=res.read(MAX_DOWNLOAD_BYTES+1)
                    code=getattr(res,"status",200)
                if len(raw)>MAX_DOWNLOAD_BYTES or len(raw)<200:
                    raise ValueError(f"publisher file size outside 200–{MAX_DOWNLOAD_BYTES} bytes: {len(raw)}")
                if b"\0" in raw[:500]:
                    raise ValueError("source contains NULs; not an ordinary CSV")
                prefix=raw[:500].lstrip().lower()
                if prefix.startswith((b"<html",b"<!doctype html",b"<?xml")):
                    raise ValueError("publisher returned an HTML/XML landing page")
                # Do not silently accept an error page that happens to have 200 status.
                if raw[:100].count(b",")==0 and raw[:100].count(b";")==0 and b"\t" not in raw[:100]:
                    raise ValueError("source has no plausible separated header")
                dest=out/"original_publisher_dataset_s1.csv"
                dest.write_bytes(raw)
                receipt={"status":"original_publisher_bytes_obtained",
                         "source_url":url,"http_status":code,
                         "content_type":typ,
                         "file":FILE_NAME,
                         "bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
                         "license":"Springer Movement Ecology article CC BY 4.0; data CC0 waiver unless indicated",
                         "doi":SOURCE_DOI,
                         "requested_url_count":len(urls)}
                return raw,receipt
            except Exception as exc:
                errors.append({"url":url,"attempt":attempt+1,
                               "failure_type":type(exc).__name__,
                               "reason":str(exc)[:350]})
                time.sleep(0.25)
    raise RuntimeError("NO_GO_SOURCE_FETCH "+json.dumps(errors,ensure_ascii=False))

def parse_original_csv(raw:bytes):
    candidates=[]
    for enc in ("utf-8-sig","cp1252","latin-1"):
        try:
            text=raw.decode(enc,"strict")
            candidates.append((text,enc))
            break
        except UnicodeDecodeError:
            pass
    if not candidates:
        raise ValueError("NO_GO_ORIGINAL_ENCODING")
    text,enc=candidates[0]
    sample=text[:8192]
    try:
        dialect=csv.Sniffer().sniff(sample,delimiters=",;\t")
        delim=dialect.delimiter
    except csv.Error:
        delim=","
    reader=csv.reader(io.StringIO(text,newline=""),delimiter=delim)
    rows=list(reader)
    if len(rows)<3 or len(rows)>MAX_DATA_ROWS:
        raise ValueError(f"NO_GO_SOURCE_ROW_GRAIN, lines={len(rows)}")
    header=[x.strip() for x in rows[0]]
    if len(header)<2 or len(set(header))!=len(header):
        raise ValueError("NO_GO_HEADER_DUPLICATE_OR_INSUFFICIENT")
    if any(not h for h in header):
        raise ValueError("NO_GO_HEADER_EMPTY_NAME")
    sizes=Counter(len(row) for row in rows[1:])
    bad=sum(n for s,n in sizes.items() if s!=len(header))
    if bad:
        raise ValueError(f"NO_GO_RAGGED_SOURCE: {bad} rows incorrect length: {dict(sizes)}")
    table=[dict(zip(header,r)) for r in rows[1:]]
    return table,{"encoding":enc,"delimiter":repr(delim),
                  "columns":header,"data_rows":len(table),
                  "row_width_histogram":dict(sorted(sizes.items()))}

def profile_original_table(records:list[dict],meta:dict):
    fields={}
    for c in meta["columns"]:
        values=[row.get(c,"").strip() for row in records]
        good=[v for v in values if v.casefold() not in MISSING]
        counter=Counter(good)
        item={"not_missing":len(good),
              "missing":len(values)-len(good),
              "distinct_nonmissing":len(counter),
              "max_frequency":max(counter.values()) if counter else 0}
        if ID_HINT.search(c):
            # A few original categorical examples are used solely to detect
            # the native source representation. We never expose human identities.
            # Tagged experimental bee codes are animal-only identifiers.
            item["short_native_examples"]=[x[:50] for x,_ in counter.most_common(5)]
        item["numeric_fraction"]=(
            sum(bool(re.fullmatch(r"[-+]?\d+(?:\.\d+)?",s)) for s in good)/len(good)
            if good else 0.0)
        fields[c]=item
    total_rows=len(records)
    duplicate_rows=total_rows-len({
        tuple(row.get(c,"") for c in meta["columns"]) for row in records
    })
    likely={
        "individual_id_columns":[c for c in meta["columns"]
                                 if re.search("bee|individ|tag|forager|visitor",c,re.I)],
        "flower_id_columns":[c for c in meta["columns"]
                             if re.search("flower|plant",c,re.I)],
        "time_columns":[c for c in meta["columns"]
                        if re.search("date|day|time|arriv|depart|hour|start|end",c,re.I)],
        "interaction_columns":[c for c in meta["columns"]
                               if re.search("interaction|resident|push|outcome|social|displace",c,re.I)],
        "bout_columns":[c for c in meta["columns"]
                        if re.search("bout|trip|nest",c,re.I)]
    }
    return {"original_row_count":total_rows,
            "exact_source_row_duplicates":duplicate_rows,
            "source_schema":meta,"native_field_profile":fields,
            "role_candidates_not_inferred_semantics":likely,
            "published_visits_6205_not_automatically_equal_source_rows":True,
            "cue_sequence_and_wind_not_inferred_from_visit_counts":True}

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="bee_stage4_source")
    args=parser.parse_args(argv)
    out=Path(args.out)
    raw,receipt=download_source(out)
    print("BEE_STAGE4_SOURCE_RECEIPT "+json.dumps(receipt,ensure_ascii=False),flush=True)
    try:
        records,meta=parse_original_csv(raw)
    except Exception as exc:
        # Emit bounded original *format* diagnostics before rejecting the
        # manuscript claim; never turn arbitrary first rows into invented
        # event fields. This diagnostic lives only in CI logs/artifact.
        prefix=raw[:450]
        diag={
            "status":"NO_GO_SCHEMA_FORMAT",
            "reason":str(exc),
            "source_url":receipt["source_url"],
            "bytes":len(raw),"sha256":receipt["sha256"],
            "first_450_bytes_repr":repr(prefix),
            "first_line_len":len(raw.splitlines()[0]) if raw.splitlines() else 0,
            "first_line_delimiter_counts":{
                "comma":raw.splitlines()[0].count(b",") if raw.splitlines() else 0,
                "semicolon":raw.splitlines()[0].count(b";") if raw.splitlines() else 0,
                "tab":raw.splitlines()[0].count(b"\t") if raw.splitlines() else 0,
            }
        }
        (out/"original_publisher_source_audit.json").write_text(
            json.dumps({"publisher_receipt":receipt,
                        "schema_audit_diagnostic":diag},
                       indent=2,ensure_ascii=False))
        print("BEE_STAGE4_SOURCE_DIAGNOSTIC "+
              json.dumps(diag,ensure_ascii=False),flush=True)
        raise
    audit=profile_original_table(records,meta)
    report={"publisher_receipt":receipt,"schema_audit":audit,
            "outcome_gate":"SCHEMA_INSPECTION_ONLY",
            "notice":"Ten flowers physically presented; no assertion that all ten simultaneously perceptible, and no reported wind manipulation"}
    (out/"original_publisher_source_audit.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))
    print("BEE_STAGE4_SOURCE_RECEIPT "+json.dumps(receipt,ensure_ascii=False),flush=True)
    print("BEE_STAGE4_SCHEMA "+json.dumps(audit,ensure_ascii=False),flush=True)
    print("BEE_STAGE4_SOURCE_AUDIT_COMPLETE",flush=True)
    return report

if __name__=="__main__":
    main()
