"""Stage46: extract only the 1.3MB compressed original modeled bee P/A matrix.

Published Laborieux et al 2026 source Zenodo 20525240, inner member of
data.zip. ZIP local header + compressed data fetched by HTTP 206 byte ranges;
verify original ZIP central directory metadata, exact decompressed bytes
and CRC32. Do not download the 126MB full data ZIP or the 21GB SDM ZIP.

First produce SCHEMA ONLY. Presence matrix is a modelled source product,
not observed individuals or a newly fitted Bombus suitability model.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from pathlib import Path
import struct
import zlib

from zip_range_catalog import get_range,parse_central_directory,central_directory_location
from discover_pollinator_sdm_sources import _get_json

ZENODO="https://zenodo.org/api/records/20525240"
SOURCE_NAME="data/bee_presence_only_matrix_15deg.csv"
MAX_CSV=25_000_000


def decompress_original_member(url,total,entry):
    off=entry["local_header_offset"]
    raw=get_range(url,total,off,off+29)
    if len(raw)!=30:
        raise ValueError("NO_GO_ORIGINAL_LOCAL_HEADER_SHORT")
    parts=struct.unpack("<4s5H3I2H",raw)
    sig,version,flags,method,mtime,mdate,crc_hdr,comp_hdr,uncomp_hdr,name_len,extra_len=parts
    if sig!=b"PK\x03\x04" or flags&1 or method!=8 or (
        entry["encrypted"] or entry["compression_method"]!=8):
        raise ValueError("NO_GO_SOURCE_MEMBER_ENCRYPTED_OR_BAD_COMPRESSOR")
    first=off+30
    name_bytes=get_range(url,total,first,first+name_len-1) if name_len else b""
    original_name=name_bytes.decode("utf8" if flags&0x800 else "cp437")
    if original_name!=entry["filename"]:
        raise ValueError("NO_GO_LOCAL_ZIP_NAME_CONFLICT")
    data_start=off+30+name_len+extra_len
    compressed=entry["compressed_bytes"]
    if compressed>3_500_000 or entry["uncompressed_bytes"]>MAX_CSV:
        raise ValueError("NO_GO_SOURCE_MATRIX_TOO_LARGE")
    data=get_range(url,total,data_start,data_start+compressed-1)
    uncompressed=zlib.decompress(data,-15)
    if len(uncompressed)!=entry["uncompressed_bytes"] or (
        zlib.crc32(uncompressed)&0xFFFFFFFF)!=entry["crc32"]:
        raise ValueError("NO_GO_SOURCE_MATRIX_CRC32_OR_SIZE_FAIL")
    return uncompressed


def source_matrix_schema(data):
    if not isinstance(data,bytes) or len(data)<10:
        raise ValueError("NO_GO_SOURCE_MATRIX_BYTES_ABSENT")
    reader=csv.reader(io.StringIO(data.decode("utf-8-sig"),newline=""))
    head=next(reader,None)
    if not head or len(head)<2:
        raise ValueError("NO_GO_SOURCE_MATRIX_HEADER")
    rows=0
    first_rows=[]
    suspect=0
    label_Bombus_rows=0
    for row in reader:
        if not row:continue
        if len(row)!=len(head):
            suspect+=1
        rows+=1
        if rows<=6:
            first_rows.append({
                "first_12_values":row[:12],
                "row_width":len(row)
            })
        if row[0].casefold().startswith("bombus "):
            label_Bombus_rows+=1
        if rows>2000000:
            raise ValueError("NO_GO_TOO_MANY_MATRIX_ROWS")
    head_Bombus=[h for h in head if (
        h.casefold().startswith("bombus ") or h.casefold().startswith("bombus_")
        or h.casefold().startswith("bombus."))]
    if suspect:
        raise ValueError("NO_GO_SOURCE_MATRIX_NONRECTANGULAR")
    return {
       "status":"SOURCE_VERIFIED_2026_MODELED_BEE_PA_MATRIX_CSV_SCHEMA",
       "data_bytes":len(data),
       "n_header_columns":len(head),
       "n_data_rows":rows,
       "first_30_columns":head[:30],
       "first_6_original_rows_12_values":first_rows,
       "Bombus_named_columns":len(head_Bombus),
       "first_25_Bombus_column_names":head_Bombus[:25],
       "Bombus_named_first_column_rows":label_Bombus_rows,
       "source_matrix_member_SHA256":hashlib.sha256(data).hexdigest(),
       "no_Bombus_richness_or_species_distributions_calculated_yet":True
    }


def main():
    meta,_=_get_json(ZENODO)
    files=[f for f in meta.get("files") or [] if f.get("key")=="data.zip"]
    if len(files)!=1:
        raise ValueError("NO_GO_SOURCE_DATA_ZIP_METADATA_MISSING")
    f=files[0];url=(f.get("links") or {}).get("self")
    total=f.get("size")
    tail_start=max(0,total-262144)
    tail=get_range(url,total,tail_start,total-1)
    pos,length,count=central_directory_location(tail,total)
    entries=parse_central_directory(get_range(url,total,pos,pos+length-1),count)
    selected=[x for x in entries if x["filename"]==SOURCE_NAME]
    if len(selected)!=1:
        raise ValueError("NO_GO_NO_UNAMBIGUOUS_SOURCE_BEE_PA_MATRIX")
    content=decompress_original_member(url,total,selected[0])
    schema=source_matrix_schema(content)
    schema["source_zip_url"]=url
    schema["original_zip_MD5_claim_from_Zenodo"]=f.get("checksum")
    schema["original_inner_source_member"]=SOURCE_NAME
    schema["original_member_crc32_verified"]=selected[0]["crc32"]
    schema["original_inner_file_not_redistributed"]=True
    folder=Path("stage46_PA_matrix_schema");folder.mkdir(exist_ok=True)
    (folder/"global_modelled_bee_presence_matrix_source_schema.json").write_text(
       json.dumps(schema,indent=2,ensure_ascii=False,sort_keys=True,allow_nan=False)+"\n",
       encoding="utf8")
    print("STAGE46_MODELED_BEE_MATRIX_AUTHENTIC_SCHEMA",json.dumps(schema,ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
