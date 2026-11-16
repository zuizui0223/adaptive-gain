"""Stage46: source-authenticate 13.2MB original equal-area bee hex shapefile ZIP.

Download in 3MB bounded HTTP 206 ranges; verify full original ZIP MD5 and
inspect shapefile DBF fields. Do not invent mapping of HEX id to lon/lat.
"""
from __future__ import annotations
import hashlib
import io
import json
from pathlib import Path
import struct
import zipfile

from discover_pollinator_sdm_sources import _get_json
from zip_range_catalog import get_range

ZENODO="https://zenodo.org/api/records/20525240"
HEX_FILE="Hexgon_shapefile.zip"
CHUNK=3_000_000


def _dbf_header(blob):
    if len(blob)<33:
        raise ValueError("NO_GO_SHAPE_DBF_SHORT_HEADER")
    version=blob[0]
    n=struct.unpack_from("<I",blob,4)[0]
    headerlen,recordlen=struct.unpack_from("<HH",blob,8)
    if headerlen>len(blob) or headerlen<33:
        raise ValueError("NO_GO_SHAPE_DBF_BAD_SCHEMA")
    fields=[]
    for pos in range(32,headerlen-1,32):
        h=blob[pos:pos+32]
        if h[0]==0x0D:break
        fields.append({"name":h[:11].split(b"\0",1)[0].decode("ascii",errors="replace"),
                       "type":chr(h[11]),"length":h[16],"decimals":h[17]})
    return {"records":n,"field_schema":fields,"source_record_len":recordlen}


def inspect_zip(archive,source_md5):
    if hashlib.md5(archive).hexdigest()!="".join(source_md5.split(":")[1:]):
        raise ValueError("NO_GO_ORIGINAL_HEX_SOURCE_MD5_FAIL")
    if not zipfile.is_zipfile(io.BytesIO(archive)):
        raise ValueError("NO_GO_HEX_ARCHIVE_NOT_ZIP")
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        names=[p for p in z.namelist() if not p.startswith("__MACOSX/")
               and not Path(p).name.startswith("._")]
        dbfs=[p for p in names if p.lower().endswith(".dbf")]
        shapefiles=[p for p in names if p.lower().endswith(".shp")]
        if len(dbfs)!=1 or len(shapefiles)!=1:
            raise ValueError("NO_GO_HEX_SOURCE_SHAPEFILE_AMBIGUOUS")
        dbf=_dbf_header(z.read(dbfs[0]))
        projection=[z.read(p).decode("latin1")[:1000]
                    for p in names if p.lower().endswith(".prj")]
        return {
          "status":"AUTHENTIC_ORIGINAL_BEE_HEX_POLYGON_GEOGRAPHY_SOURCE_SCHEMA",
          "original_hex_source_MD5":source_md5,
          "n_ZIP_source_members":len(names),
          "source_members":names[:90],
          "source_shapefile_member":shapefiles[0],
          "source_dbf_member":dbfs[0],
          "source_projection":projection,
          "dbf_original":dbf,
          "no_hex_species_join_yet":True
        }


def main():
    meta,_=_get_json(ZENODO)
    found=[x for x in meta.get("files") or [] if x.get("key")==HEX_FILE]
    if len(found)!=1:
        raise ValueError("NO_GO_ORIGINAL_EQUAL_AREA_HEX_SHAPEFILE_NOT_FOUND")
    entry=found[0];total=entry.get("size");url=(entry.get("links") or {}).get("self")
    if not isinstance(total,int) or total>15_000_000 or not isinstance(url,str):
        raise ValueError("NO_GO_UNEXPECTED_ORIGINAL_HEX_ARCHIVE_SIZE")
    chunks=[]
    for start in range(0,total,CHUNK):
        end=min(total,start+CHUNK)-1
        chunks.append(get_range(url,total,start,end))
    source=b"".join(chunks)
    if len(source)!=total:
        raise ValueError("NO_GO_ORIGINAL_HEX_ARCHIVE_PARTIAL")
    result=inspect_zip(source,entry.get("checksum") or "")
    result["original_zip_bytes"]=total
    result["original_Zenodo_file_url"]=url
    d=Path("stage46_hex_geography")
    d.mkdir(exist_ok=True)
    (d/"published_bee_hex_shapefile_schema.json").write_text(
        json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("STAGE46_ORIGINAL_BEE_HEX_GEOMETRY_SCHEMA",json.dumps(result,ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
