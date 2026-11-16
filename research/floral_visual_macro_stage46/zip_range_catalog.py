"""Stage46: source remote ZIP central-directory probe using HTTP 206 only.

Do not download 126 MB data.zip or 21.65 GB rasters. Read tail + central
directory for true original compressed-member names, CRC32 and byte offsets.
The output is original-file evidence, not a Bombus suitability prediction.
"""
from __future__ import annotations
import json
from pathlib import Path
import struct
import urllib.request
import urllib.error

from discover_pollinator_sdm_sources import _get_json

RECORD_URL="https://zenodo.org/api/records/20525240"
TAIL_SIZE=262144
MAX_RANGE=4_000_000


def get_range(url,total,start,end):
    if not url.startswith("https://zenodo.org/") or not (
        isinstance(total,int) and 0<=start<=end<total and end-start+1<=MAX_RANGE):
        raise ValueError("NO_GO_ZENODO_RANGE_INVALID")
    req=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-stage46-zenodo-selective-ZIP/2026",
        "Range":f"bytes={start}-{end}"
    })
    with urllib.request.urlopen(req,timeout=90) as res:
        if res.status!=206:
            raise ValueError("NO_GO_ZENODO_DID_NOT_HONOR_RANGE")
        cr=res.headers.get("Content-Range","")
        if cr!=f"bytes {start}-{end}/{total}":
            raise ValueError("NO_GO_ZENODO_INVALID_CONTENT_RANGE")
        blob=res.read(MAX_RANGE+1)
    if len(blob)!=end-start+1:
        raise ValueError("NO_GO_ZENODO_RANGE_SIZE_MISMATCH")
    return blob


def central_directory_location(tail,total):
    idx=tail.rfind(b"PK\x05\x06")
    if idx<0 or len(tail)-idx<22:
        raise ValueError("NO_GO_ZIP_END_OF_CENTRAL_DIRECTORY_MISSING")
    fields=struct.unpack_from("<4s4HIIH",tail,idx)
    _,disk,cd_disk,num_disk,num_total,size,offset,comment_len=fields
    if disk!=0 or cd_disk!=0 or num_disk!=num_total or (
        size==0xFFFFFFFF or offset==0xFFFFFFFF):
        raise ValueError("NO_GO_UNSUPPORTED_ZIP_MULTIDISK_OR_ZIP64")
    if offset+size>total or num_total>10000:
        raise ValueError("NO_GO_ZIP_CD_INVALID_BOUNDS")
    return offset,size,num_total


def parse_central_directory(raw,expected_entries):
    pos=0
    items=[]
    while pos<len(raw):
        if len(raw)-pos<46 or raw[pos:pos+4]!=b"PK\x01\x02":
            raise ValueError("NO_GO_ZIP_CENTRAL_DIRECTORY_FILE_HEADER")
        f=struct.unpack_from("<4s6H3I5H2I",raw,pos)
        flags=f[3];method=f[4];crc=f[7];comp=f[8];size=f[9]
        fn_len=f[10];extra_len=f[11];comment_len=f[12];local=f[16]
        end=pos+46+fn_len+extra_len+comment_len
        if end>len(raw) or comp==0xFFFFFFFF or local==0xFFFFFFFF:
            raise ValueError("NO_GO_INVALID_ZIP_CD_MEMBER")
        namebytes=raw[pos+46:pos+46+fn_len]
        name=namebytes.decode("utf8" if flags&0x800 else "cp437")
        items.append({
            "filename":name,"compressed_bytes":comp,"uncompressed_bytes":size,
            "compression_method":method,"crc32":crc,"local_header_offset":local,
            "encrypted":bool(flags&1),
        })
        pos=end
    if len(items)!=expected_entries:
        raise ValueError("NO_GO_ZIP_CD_MEMBER_COUNT_MISMATCH")
    return items


def probe():
    meta,_=_get_json(RECORD_URL)
    candidates=[x for x in (meta.get("files") or []) if x.get("key")=="data.zip"]
    if len(candidates)!=1:
        raise ValueError("NO_GO_ZENODO_COMPACT_DATA_ZIP_UNIDENTIFIED")
    entry=candidates[0]
    total=entry.get("size")
    url=(entry.get("links") or {}).get("self")
    if not isinstance(total,int) or total>135_000_000 or not isinstance(url,str):
        raise ValueError("NO_GO_ZIP_SIZE_OR_SOURCE_ID")
    tail_start=max(0,total-TAIL_SIZE)
    tail=get_range(url,total,tail_start,total-1)
    offset,length,n=central_directory_location(tail,total)
    cd=get_range(url,total,offset,offset+length-1)
    members=parse_central_directory(cd,n)
    match=[x for x in members if any(tag in x["filename"].lower()
      for tag in ("bee_presence_only_matrix","pa_matrix","pa_mat","bombus","species_presence"))]
    return {
       "status":"AUTHENTIC_ORIGINAL_GLOBAL_BEE_MODEL_ZIP_RANGE_DIRECTORY_READ",
       "source_zenodo_record":meta.get("id"),
       "original_zip_file_url":url,
       "original_zip_length_bytes":total,
       "original_zip_deposit_checksum":entry.get("checksum"),
       "n_members":len(members),
       "central_directory_bytes":length,
       "bytes_read_source_index":len(tail)+len(cd),
       "candidate_modelled_species_grid_entries":match[:80],
       "candidate_count":len(match),
       "first_50_member_names":[x["filename"] for x in members[:50]],
       "raw_global_Bombus_occurrences_not_used":True,
       "no_full_zip_or_21GB_raster_download":True,
       "no_Bombus_prediction_values_extracted_yet":True
    }


if __name__=="__main__":
    a=probe()
    folder=Path("stage46_range_zip_index")
    folder.mkdir(exist_ok=True)
    (folder/"bee_model_data_zip_central_directory.json").write_text(
       json.dumps(a,indent=2,ensure_ascii=False,sort_keys=True,allow_nan=False)+"\n")
    print("STAGE46_AUTHENTIC_BEE_SDM_CENTRAL_DIRECTORY",json.dumps(a,sort_keys=True))
