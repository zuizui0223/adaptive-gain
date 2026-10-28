"""Stage7b native Dataverse source-quality audit, 18-colony robot flowers.

Use exact KU Leuven RDR original published dataset API/MD5 records, never
guess numeric file IDs or conflate independent colony events with individual
tracked bee trajectories. Preserve source bytes in ephemeral CI only.
"""
from __future__ import annotations
from collections import Counter
import argparse,csv,hashlib,io,json,re
from pathlib import Path
import urllib.request
from urllib.parse import urlencode

HOST="https://rdr.kuleuven.be"
DOI="doi:10.48804/UIIVLP"
DATASET_API=HOST+"/api/datasets/:persistentId/?"+urlencode({"persistentId":DOI})
EXPECTED={
    "data_selfmed.csv":"3a3578d61d7633635615d43829df3f3c",
    "00_README.md":"b05dd7324c909f8f65d95ae938c68aca",
    "Data_analysis_selfmed.R":"ed741040397ea0979ce421937a42ebdd"}
MAX_FILE_BYTES=12*1024*1024
MAX_METADATA_BYTES=4*1024*1024
MAX_ROWS=250000
KEY_HINT=re.compile(r"col|hive|bee|individual|id|robot|flower|nectar|querc|treat|trial|date|day|clock|time|duration|reward|group|condition|hour|visit|event|tag",re.I)

def public_get(url,cap):
    if not url.startswith(HOST+"/api/"):
        raise ValueError("NO_GO_NON_NATIVE_RDR_URL")
    req=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-independent-multicolony-data-provenance/1.0",
        "Accept":"application/json,text/csv,text/plain,*/*"})
    with urllib.request.urlopen(req,timeout=85) as res:
        b=res.read(cap+1)
        actual=getattr(res,"status",200)
        typ=res.headers.get("Content-Type","")
    if len(b)>cap:
        raise ValueError("NO_GO_RDR_FILE_OVERSIZE")
    if not b or b[:100].lstrip().lower().startswith((b"<!doctype",b"<html")):
        raise ValueError("NO_GO_RDR_RETURNED_NONDATA_DOCUMENT")
    return b,{"http_status":actual,"type":typ}

def original_manifest():
    raw,transport=public_get(DATASET_API,MAX_METADATA_BYTES)
    try:metadata=json.loads(raw.decode("utf-8"))
    except Exception as exc:raise ValueError("NO_GO_RDR_DATASET_NONJSON") from exc
    if metadata.get("status")!="OK":raise ValueError("NO_GO_RDR_DATASET_STATUS_NOT_OK")
    data=metadata.get("data",{})
    latest=data.get("latestVersion",{})
    original_files=latest.get("files",[])
    if not original_files:raise ValueError("NO_GO_RDR_NO_PUBLISHED_FILE_RECORDS")
    ids=set()
    selected={}
    receipts=[]
    for f in original_files:
        datafile=f.get("dataFile",{})
        name=datafile.get("filename")
        rid=datafile.get("id")
        if rid in ids:
            raise ValueError("NO_GO_DUPLICATE_OFFICIAL_FILE_ID")
        ids.add(rid)
        checksum=datafile.get("checksum",{})
        md5=datafile.get("md5") or (
            checksum.get("value") if str(checksum.get("type","")).upper()=="MD5" else None)
        receipts.append({"file":name,"id":rid,"bytes":datafile.get("filesize"),
                         "source_md5":md5,"publisher_restricted":f.get("restricted")})
        if name not in EXPECTED:continue
        if f.get("restricted"):
            raise ValueError("NO_GO_RDR_FILE_RESTRICTED "+name)
        if not isinstance(rid,int) or rid<=0:
            raise ValueError("NO_GO_RDR_MISSING_ORIGINAL_FILE_ID "+str(name))
        if md5 and md5.lower()!=EXPECTED[name]:
            raise ValueError("NO_GO_RDR_FILE_DIGEST_CHANGED_FROM_PUBLICATION "+name)
        selected[name]={"original_id":rid,"original_expected_md5":EXPECTED[name],
                        "size":datafile.get("filesize"),"provider_recorded_md5":md5}
    if set(selected)!=set(EXPECTED):
        raise ValueError("NO_GO_RDR_REQUIRED_PUBLISHED_FILES_ABSENT")
    source={"dataset_doi":DOI,"dataset_id":data.get("id"),
            "persistent_id":data.get("persistentId"),
            "dataset_version":latest.get("versionNumber"),
            "dataset_minor_version":latest.get("versionMinorNumber"),
            "listed_files":receipts,"api":DATASET_API,
            "published_original_files":selected,
            "native_dataverse_metadata_request":transport}
    return selected,source

def download_real_sources(manifest,directory):
    files={}
    for name,item in manifest.items():
        url=HOST+"/api/access/datafile/"+str(item["original_id"])
        blob,transport=public_get(url,MAX_FILE_BYTES)
        source_md5=hashlib.md5(blob).hexdigest()
        if source_md5!=item["original_expected_md5"]:
            raise ValueError("NO_GO_ORIGINAL_RDR_MD5_MISMATCH "+name)
        if item["size"] is not None and len(blob)!=int(item["size"]):
            raise ValueError("NO_GO_ORIGINAL_RDR_FILE_SIZE_MISMATCH "+name)
        (directory/name).write_bytes(blob)
        files[name]={"source_download_api":url,"size":len(blob),
                     "original_md5":source_md5,
                     "source_sha256":hashlib.sha256(blob).hexdigest(),
                     "source_http":transport}
        print("BEE_STAGE7B_RDR_ORIGINAL_FILE "+json.dumps(
            {"name":name,**files[name]},ensure_ascii=False),flush=True)
    return files

def original_csv_schema(source):
    text=None;enc=None
    for codec in ["utf-8-sig","cp1252","latin1"]:
        try:text=source.decode(codec,errors="strict");enc=codec;break
        except UnicodeDecodeError:pass
    if text is None:raise ValueError("NO_GO_CSV_TEXT_ENCODING")
    try:delim=csv.Sniffer().sniff(text[:8192],delimiters=",;\t").delimiter
    except csv.Error:delim=","
    read=csv.DictReader(io.StringIO(text),delimiter=delim)
    columns=read.fieldnames
    if not columns or len(columns)<2 or len(set(columns))!=len(columns):
        raise ValueError("NO_GO_CSV_HEADER_DUPLICATION_OR_MISSING")
    source_rows=0
    exact_duplicates=0
    seen=set()
    nonempty=Counter()
    counters={c:Counter() for c in columns if KEY_HINT.search(c)}
    all_example_rows=[]
    for row in read:
        source_rows+=1
        if source_rows>MAX_ROWS:raise ValueError("NO_GO_CSV_TOO_MANY_ROWS")
        if None in row:raise ValueError("NO_GO_CSV_RAGGED_ROW")
        vals=tuple((row[c] or "").strip() for c in columns)
        if vals in seen:exact_duplicates+=1
        else:seen.add(vals)
        for c in columns:
            v=(row[c] or "").strip()
            if v not in ("","NA","N/A","nan","null"):
                nonempty[c]+=1
                if c in counters:
                    counters[c][v]+=1
        if len(all_example_rows)<3:
            # Only likely source categories/patterns; no untrusted names from
            # internal human participant records. Automatic robotic events
            # are insect visits; avoid exposing exact timestamps/locations.
            all_example_rows.append({c:str(row[c])[:70] for c in columns if KEY_HINT.search(c)})
    profile={}
    for c in columns:
        values=counters.get(c)
        profile[c]={
            "nonempty":nonempty[c],
            "null":source_rows-nonempty[c],
            "unique_if_inspected":len(values) if values is not None else None,
        }
        if values is not None and len(values)<=22 and not re.search(r"time|date|bee.*id|^id$|stamp|event",c,re.I):
            profile[c]["source_levels"]={k:v for k,v in values.most_common(22)}
        elif values is not None:
            profile[c]["source_level_count_only"]=len(values)
    role_candidates={
        "animal_tag_ids":[c for c in columns if re.search(r"bee.?id|beetag|rfid|individual.?id|worker.?id|forager.?id",c,re.I)],
        "colony_ids":[c for c in columns if re.search(r"colony|hive",c,re.I)],
        "flower_ids":[c for c in columns if re.search(r"flower|device|robot|feeder",c,re.I)],
        "timing":[c for c in columns if re.search(r"time|date|day|hour|stamp",c,re.I)],
        "reward_or_treatment":[c for c in columns if re.search(r"querc|nectar|treat|reward|group|status|condition",c,re.I)],
    }
    return {"rows":source_rows,"columns":columns,"source_encoding":enc,
            "delimiter":repr(delim),"exact_duplicate_rows":exact_duplicates,
            "quality_profile":profile,
            "possible_source_roles_NOT_INFERRED":role_candidates,
            "schema_small_source_examples":all_example_rows,
            "no_individual_identity_may_be_inferred_from_colony":True,
            "not_physical_flight_trajectories":True}

def run(root):
    root.mkdir(parents=True,exist_ok=True)
    items,manifest=original_manifest()
    result={"dataset_source":manifest,
            "stage":"original_RDR_dataverse_source_schema_and_quality",
            "source_retrieval_status":"NOT_DOWNLOADED"}
    (root/"rdr_multicolony_source_audit.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False))
    print("BEE_STAGE7B_SOURCE_MANIFEST "+json.dumps(manifest,ensure_ascii=False),flush=True)
    try:
        hashes=download_real_sources(items,root)
    except Exception as exc:
        result["source_retrieval_status"]="NO_GO_FILE_DOWNLOAD"
        result["blocker"]={"type":type(exc).__name__,"http":getattr(exc,"code",None),
                           "error":str(exc)[:550]}
        (root/"rdr_multicolony_source_audit.json").write_text(
            json.dumps(result,indent=2,ensure_ascii=False))
        raise
    csvpath=root/"data_selfmed.csv"
    schema=original_csv_schema(csvpath.read_bytes())
    readme=(root/"00_README.md").read_text(encoding="utf-8-sig",errors="strict")
    result.update({"source_retrieval_status":"SOURCE_VERIFIED",
                   "verified_source_file_receipts":hashes,
                   "original_event_csv_schema":schema,
                   "original_source_readme":readme[:25000],
                   "not_a_single_bee_behavior_sequence_without_explicit_animal_id":True})
    (root/"rdr_multicolony_source_audit.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False))
    print("BEE_STAGE7B_ORIGINAL_SCHEMA "+json.dumps(schema,ensure_ascii=False),flush=True)
    print("BEE_STAGE7B_README "+readme[:12000],flush=True)
    print("BEE_STAGE7B_SOURCE_AUDIT_COMPLETE",flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="rdr_multicolony_source")
    a=p.parse_args()
    run(Path(a.out))
