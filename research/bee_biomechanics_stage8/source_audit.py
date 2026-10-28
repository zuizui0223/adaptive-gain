"""Stage 8: Cambridge DSpace original individual-bee behavioral data audit.

Look up source DOI through official institutional repository REST HAL,
identify ORIGINAL bundle and native bitstream metadata/checksum, download
only provider links. NO guessed file UUIDs or manually invented data.

Outputs metadata, digests, source quality receipts, not original rows.
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
import urllib.parse
import urllib.request

API="https://api.repository.cam.ac.uk/server/api"
REPOSITORY="https://www.repository.cam.ac.uk"
DOI="10.17863/CAM.100572"
HANDLE="1810/357732"
SOURCE_FOCUS=("TradeOffData.csv","BeeMasses.csv")
SOURCE_CSV_LIMIT=35*1024*1024
JSON_CAP=5*1024*1024
MAX_OBSERVATIONS=500000
MISSING={"","na","n/a","nan","null","#n/a","not recorded",".","none"}
FIELDS=re.compile(
    r"colony|bee|worker|individ|sucrose|concentra|treat|rough|orient|surfac|flower|bout|visit|drink|millisec|time|duration|activity|event|observ|nest|mass|flight|position|id",
    re.I)
EXAMPLES=re.compile(r"^$") # never print original individual bee identifiers as examples

def _request(url,limit=JSON_CAP):
    if not (url.startswith(API+"/") or url.startswith(REPOSITORY+"/")):
        raise ValueError("NO_GO_NON_CAMBRIDGE_INSTITUTIONAL_SOURCE_LINK "+url)
    req=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-cambridge-open-repository-source-audit/1.0",
        "Accept":"application/hal+json,application/json,text/csv,application/octet-stream,*/*"
    })
    with urllib.request.urlopen(req,timeout=60) as rsp:
        data=rsp.read(limit+1)
        typ=rsp.headers.get("Content-Type","")
        final=rsp.url
        code=getattr(rsp,"status",200)
    if len(data)>limit or not data:
        raise ValueError("NO_GO_SOURCE_BYTES_EMPTY_OR_OVERSIZE")
    if data[:200].lstrip().lower().startswith((b"<html",b"<!doctype")):
        raise ValueError("NO_GO_SOURCE_RETURNED_HTML")
    # external redirections not used for source identity: explicit provider
    # checksum still required for original dataset validation.
    return data,{"url":url,"http_status":code,"content_type":typ,
                 "final_host":urllib.parse.urlsplit(final).hostname}

def get_json(url):
    data,receipt=_request(url,JSON_CAP)
    try: obj=json.loads(data.decode("utf-8-sig"))
    except Exception as e:
        raise ValueError("NO_GO_DSPACE_JSON_ENDPOINT_NONJSON "+url) from e
    return obj,receipt

def href(obj,key):
    link=obj.get("_links",{}).get(key)
    if isinstance(link,dict):return link.get("href")
    return None

def safe_link(url,base=API):
    if not url:raise ValueError("NO_GO_MISSING_DSPACE_HATEOAS_LINK")
    candidate=urllib.parse.urljoin(base+"/",url)
    parts=urllib.parse.urlsplit(candidate)
    if parts.scheme!="https" or parts.netloc not in {
        "api.repository.cam.ac.uk","www.repository.cam.ac.uk"
    }:
        raise ValueError("NO_GO_DSPACE_INSTITUTIONAL_LINK_HOST "+candidate)
    return candidate

def _unpack_search_results(obj):
    # Search endpoint is a HAL page; result._embedded.indexableObject can
    # hold the actual item. Never take arbitrary first matching result.
    embedded=obj.get("_embedded",{})
    results=embedded.get("searchResult",embedded.get("searchResults",[]))
    # DSpace Discovery exposes a HAL "searchResult" collection wrapper.
    # Newer versions nest the actual entries below _embedded.objects.
    if isinstance(results,dict):
        results=results.get("_embedded",{}).get(
            "objects",results.get("_embedded",{}).get("searchResults",[]))
    if not isinstance(results,list):
        raise ValueError("NO_GO_DSPACE_SEARCH_HAL_SHAPE "+
                         json.dumps({"root":list(obj.keys()),
                                     "embedded":list(embedded.keys()),
                                     "wrapper_type":str(type(results))}))
    items=[]
    for result in results:
        payload=result.get("_embedded",{}).get("indexableObject") or result
        if not isinstance(payload,dict):continue
        candidate=payload.get("_embedded",{}).get("item",payload)
        items.append(candidate)
    return items

def _is_target_item(item):
    md=item.get("metadata",{})
    values=[]
    if isinstance(md,dict):
        for key,v in md.items():
            if "identifier" in key or "title" in key:
                if isinstance(v,list):values.extend(str(x.get("value","")) for x in v if isinstance(x,dict))
    title=str(item.get("name",""))
    joined=" ".join(values+[title]).lower()
    return ("10.17863/cam.100572" in joined or
            "1810/357732" in joined or
            ("nectar quality" in joined and "floral biomechanics" in joined) or
            ("nectar" in joined and "biomechanics" in joined and "trade" in joined))

def _read_json_candidates(urls):
    log=[]
    for url in urls:
        try:
            info,receipt=get_json(url)
            log.append({"url":url,"status":"200_SOURCE_JSON","http":receipt["http_status"]})
            return info,receipt,log
        except Exception as e:
            log.append({"url":url,"status":type(e).__name__,
                        "http":getattr(e,"code",None),"reason":str(e)[:170]})
    raise ValueError("NO_GO_ALL_DSPACE_SOURCE_METADATA_ROUTES "+json.dumps(log))

def discover_item():
    # No inferred UUIDs. These queries contain only the source DOI/title
    # and use DSpace public, documented discovery endpoints.
    queries=[
        API+"/discover/search/objects?"+urllib.parse.urlencode({"query":DOI,"size":20}),
        API+"/discover/search/objects?"+urllib.parse.urlencode({"query":"Bumblebees negotiate a trade-off between nectar quality and floral biomechanics","size":20}),
        API+"/discover/search/objects?"+urllib.parse.urlencode({"query":"TradeOffData.csv","size":20}),
    ]
    found=[];diagnostics=[]
    for url in queries:
        try:
            obj,rcpt=get_json(url)
            results=_unpack_search_results(obj)
            candidates=[r for r in results if _is_target_item(r)]
            diagnostics.append({"endpoint":url,"result_count":len(results),
                                "relevant_match_count":len(candidates)})
            for item in candidates:
                item_url=href(item,"self")
                if item_url:found.append((safe_link(item_url),item))
        except Exception as exc:
            diagnostics.append({"endpoint":url,"status":type(exc).__name__,
                                "http":getattr(exc,"code",None),
                                "reason":str(exc)[:240]})
    unique={url:item for url,item in found}
    if not unique:
        raise ValueError("NO_GO_CAMBRIDGE_ITEM_NOT_DISCOVERED "+
                         json.dumps(diagnostics))
    # A paper and the deposited source data can share the same title.
    # Resolve both native items and choose ONLY the record whose *own*
    # identifier/handle equals the source dataset DOI/handle; a related
    # article mentioning this DOI is not the original primary data.
    exact=[]
    candidate_info=[]
    for url,summary in unique.items():
        obj,http=get_json(url)
        meta=obj.get("metadata",{})
        identifiers=[]
        for key,values in meta.items():
            if not ("identifier" in key or key=="dc.identifier.uri"):
                continue
            if isinstance(values,list):
                identifiers.extend((key,str(v.get("value","")))
                                   for v in values if isinstance(v,dict))
        selected=[(k,v) for k,v in identifiers
                  if k in ("dc.identifier.doi","dc.identifier.uri",
                           "dc.identifier.handle","dc.identifier.other",
                           "dc.identifier") and
                  (DOI.lower() in v.lower() or HANDLE in v)]
        candidate_info.append({"url":url,"name":obj.get("name"),
                               "self_identifiers":identifiers[:12],
                               "strict_exact_identifier_matches":selected})
        if selected:
            exact.append((url,obj,http))
    if len(exact)!=1:
        raise ValueError("NO_GO_CAMBRIDGE_SOURCE_DATA_RECORD_ID_NOT_UNIQUE "+
                         json.dumps({"query_diagnostics":diagnostics,
                                     "same_title_items":candidate_info}))
    item_url,metadata,receipt=exact[0]
    if not _is_target_item(metadata):
        raise ValueError("NO_GO_DSPACE_ITEM_IDENTITY_NOT_SOURCE_DOI")
    audit={"item_url":item_url,"item_uuid":metadata.get("uuid"),
           "item_name":metadata.get("name"),
           "metadata_checks":diagnostics,
           "selected_item_http":receipt,
           "correct_doi":DOI,
           "reported_original_handle":HANDLE}
    return metadata,audit

def original_bitstreams(item):
    bundles_href=href(item,"bundles")
    if not bundles_href:
        # DSpace HAL sometimes requires linked conventional API path
        uid=item.get("uuid")
        if not uid:raise ValueError("NO_GO_DSPACE_ITEM_UUID_MISSING")
        bundles_href=API+"/core/items/"+uid+"/bundles"
    bundle_json,bundle_rcpt=get_json(safe_link(bundles_href))
    bundle_array=bundle_json.get("_embedded",{}).get("bundles",[])
    originals=[x for x in bundle_array if x.get("name")=="ORIGINAL"]
    if len(originals)!=1:raise ValueError("NO_GO_DSPACE_ORIGINAL_BUNDLE_AMBIGUOUS")
    bun=originals[0]
    child=href(bun,"bitstreams")
    if not child:
        uid=bun.get("uuid")
        if not uid:raise ValueError("NO_GO_DSPACE_BUNDLE_UUID_MISSING")
        child=API+"/core/bundles/"+uid+"/bitstreams"
    bits,bits_receipt=get_json(safe_link(child))
    original_records=bits.get("_embedded",{}).get("bitstreams",[])
    selected={}
    audit=[]
    for source in original_records:
        name=source.get("name")
        checksum=source.get("checkSum",source.get("checksum"))
        sha=source.get("sha256",None)
        audit.append({"original_filename":name,"size":source.get("sizeBytes"),
                      "provider_checksum":checksum,
                      "bitstream_uuid":source.get("uuid"),
                      "bundle":source.get("bundleName")})
        if name in SOURCE_FOCUS:
            content=href(source,"content")
            if not content:
                uuid=source.get("uuid")
                if not uuid:raise ValueError("NO_GO_REQUIRED_BITSTREAM_UUID "+name)
                content=API+"/core/bitstreams/"+uuid+"/content"
            selected[name]={"record":source,
                            "provider_bitstream_url":safe_link(content)}
    if set(selected)!=set(SOURCE_FOCUS):
        raise ValueError("NO_GO_CAMBRIDGE_ORIGINAL_DATA_FILES_NOT_PUBLISHED "+
                         json.dumps(audit))
    return selected,{"original_bundle_uuid":bun.get("uuid"),
                     "original_file_inventory":audit,
                     "original_bundle_json":bundle_rcpt,
                     "original_file_listing_http":bits_receipt}

def check_provider_checksum(data,record,source_name):
    source_hash=hashlib.sha256(data).hexdigest()
    checksum=record.get("checkSum",record.get("checksum"))
    if not checksum:
        raise ValueError("NO_GO_CAMBRIDGE_PROVIDER_ORIGINAL_CHECKSUM_ABSENT "+source_name)
    if isinstance(checksum,dict):
        algorithm=str(checksum.get("checkSumAlgorithm",checksum.get("algorithm",""))).lower()
        value=str(checksum.get("value","")).lower()
    else:
        raise ValueError("NO_GO_CAMBRIDGE_PROVIDER_ORIGINAL_CHECKSUM_SHAPE")
    observed={
        "md5":hashlib.md5(data).hexdigest(),
        "sha256":source_hash,
        "sha-256":source_hash,
    }.get(algorithm)
    if observed is None or observed!=value:
        raise ValueError("NO_GO_CAMBRIDGE_SOURCE_DIGEST_MISMATCH "+source_name)
    size=record.get("sizeBytes")
    if size is not None and int(size)!=len(data):
        raise ValueError("NO_GO_CAMBRIDGE_ORIGINAL_SIZE_MISMATCH "+source_name)
    return {"original_sha256":source_hash,"original_bytes":len(data),
            "original_provider_algorithm":algorithm,
            "original_provider_checksum":value}

def inspect_csv(raw):
    enc=None;content=None
    for candidate in ("utf-8-sig","cp1252","latin-1"):
        try:content=raw.decode(candidate,errors="strict");enc=candidate;break
        except UnicodeDecodeError:pass
    if content is None:raise ValueError("NO_GO_CAMBRIDGE_CSV_ENCODING")
    try:delim=csv.Sniffer().sniff(content[:6000],delimiters=",;\t").delimiter
    except csv.Error:delim=","
    reader=csv.DictReader(io.StringIO(content),delimiter=delim)
    header=reader.fieldnames
    if not header or len(header)<3 or len(set(header))!=len(header):
        raise ValueError("NO_GO_CAMBRIDGE_CSV_SOURCE_HEADER")
    counts={c:Counter() for c in header if FIELDS.search(c)}
    nonempty=Counter();bad_rows=0;sample=[];all_rows=0;seen=set();duplicates=0
    for row in reader:
        all_rows+=1
        if all_rows>MAX_OBSERVATIONS:raise ValueError("NO_GO_CAMBRIDGE_SOURCE_TOO_MANY_ROWS")
        if None in row or any(v is None for v in row.values()):
            bad_rows+=1;continue
        item=tuple(str(row[c]).strip() for c in header)
        if item in seen:duplicates+=1
        else:seen.add(item)
        for field,v in row.items():
            value=str(v).strip()
            if value.casefold() not in MISSING:
                nonempty[field]+=1
                if field in counts:counts[field][value]+=1
    if bad_rows:
        raise ValueError("NO_GO_CAMBRIDGE_SOURCE_RAGGED_CSV_ROWS "+str(bad_rows))
    return {
        "original_csv_rows":all_rows,
        "source_columns":header,
        "encoding":enc,"delimiter":repr(delim),
        "exact_duplicate_record_rows":duplicates,
        "source_fields":{
            c:{"nonempty":nonempty[c],"missing":all_rows-nonempty[c],
               "distinct":len(counts[c]),
               "native_values_if_le20":(
                   dict(counts[c].most_common(20)) if len(counts[c])<=20
                   and not re.search(r"bee|id|time|stamp|date|observation",c,re.I)
                   else None),
               "top_value_frequency":counts[c].most_common(1)[0][1]
                        if counts[c] else 0
            } for c in counts},
        "fields_matching_original_roles":{
            "bee_or_colony":[c for c in header if re.search(r"bee|colony",c,re.I)],
            "observed_time":[c for c in header if re.search(r"time|duration|millisec",c,re.I)],
            "physical_flower_or_handling":[c for c in header if re.search(r"flower|orient|surfac|rough",c,re.I)],
            "reward":[c for c in header if re.search(r"sucrose|nectar|concen",c,re.I)],
            "sequence_or_bout":[c for c in header if re.search(r"bout|visit|drink|observ",c,re.I)]
        },
        "original_source_identity_conditions":"colony,bee,original physical flower and timestamp must be justified before event train/test; no inferred animal cues"
    }

def run(folder):
    folder.mkdir(exist_ok=True,parents=True)
    metadata,audit=discover_item()
    selected,bundleaudit=original_bitstreams(metadata)
    report={"source":"University of Cambridge Apollo DSpace official",
            "dataset_doi":DOI,"item":audit,
            "files":bundleaudit,
            "source_fetch":"metadata_verified_data_pending"}
    p=folder/"original_cambridge_source_audit.json"
    p.write_text(json.dumps(report,indent=2,ensure_ascii=False))
    receipts={};schemas={}
    for name,info in selected.items():
        try:
            data,download_rcpt=_request(info["provider_bitstream_url"],SOURCE_CSV_LIMIT)
            checksum=check_provider_checksum(data,info["record"],name)
        except Exception as e:
            report["source_fetch"]="NO_GO_ORIGINAL_CAMBRIDGE_BYTES_UNAVAILABLE"
            report["error"]={"filename":name,"type":type(e).__name__,
                             "http":getattr(e,"code",None),"message":str(e)[:400]}
            p.write_text(json.dumps(report,indent=2,ensure_ascii=False))
            raise
        (folder/name).write_bytes(data)
        receipts[name]={"source_download":download_rcpt,**checksum}
        schemas[name]=inspect_csv(data)
        print("BEE_STAGE8_ORIGINAL_FILE "+json.dumps({
            "file":name,**receipts[name],
            "schema":schemas[name]
        },ensure_ascii=False),flush=True)
    report["source_fetch"]="SOURCE_ORIGINAL_BYTE_CHECKS_PASSED"
    report["original_file_receipts"]=receipts
    report["source_schemas"]=schemas
    p.write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print("BEE_STAGE8_ORIGINAL_AUDIT_COMPLETE",flush=True)
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage8_original")
    a=p.parse_args()
    run(Path(a.out))
