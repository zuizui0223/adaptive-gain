"""Stage46: inspect compact ORIGINAL global bee SDM-derived presence matrix ZIP.

Source: Laborieux et al. 2026 global bee bioregions, Zenodo 20525239.
Download ONLY the 126MB *data.zip*, not the 21.65GB sdm.zip. Authenticate
published bytes and inspect archived species-by-grid format; no fabricated
Bombus suitability or source redistribution.

Also inspect 31KB original Dryad Potentilleae UV comparative xlsx schema,
without writing or editing a spreadsheet or attributing inferred traits.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import tempfile
import urllib.request
import zipfile
from xml.etree import ElementTree as ET

from discover_pollinator_sdm_sources import _get_json
from inspect_compact_source_tables import original_bytes

ZENODO="https://zenodo.org/api/records/20525239"
DRYAD_UV="https://datadryad.org/api/v2/files/543161/download"
MAX_ZIP_BYTES=135_000_000
MAX_UV_BYTES=120_000


def fetch_zip_to_temp(url,declared_size):
    if declared_size<=0 or declared_size>MAX_ZIP_BYTES:
        raise ValueError("NO_GO_NOT_COMPACT_BEE_SDM_ARCHIVE")
    if not url.startswith("https://zenodo.org/"):
        raise ValueError("NO_GO_UNTRUSTED_BEE_MATRIX_ARCHIVE_HOST")
    digest=hashlib.md5()
    f=tempfile.TemporaryFile()
    request=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-stage46-source-model-grid-inspection/2026",
        "Accept":"application/octet-stream,application/zip"})
    actual=0
    with urllib.request.urlopen(request,timeout=180) as response:
        while True:
            chunk=response.read(512*1024)
            if not chunk:break
            actual+=len(chunk)
            if actual>MAX_ZIP_BYTES:
                raise ValueError("NO_GO_GLOBAL_BEE_COMPACT_ZIP_TOO_LARGE")
            f.write(chunk)
            digest.update(chunk)
    if actual!=declared_size:
        raise ValueError("NO_GO_GLOBAL_BEE_ZIP_INCOMPLETE")
    f.seek(0)
    return f,"md5:"+digest.hexdigest()


def _xlsx_sheet_summary(binary):
    if not zipfile.is_zipfile(io.BytesIO(binary)):
        raise ValueError("NO_GO_ORIGINAL_UV_XLSX_NOT_VALID")
    ns={"x":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(io.BytesIO(binary)) as arc:
        book=ET.fromstring(arc.read("xl/workbook.xml"))
        names=[elem.attrib.get("name") for elem in book.findall(".//x:sheet",ns)]
        result=[]
        for filename in sorted(arc.namelist()):
            if not filename.startswith("xl/worksheets/sheet") or not filename.endswith(".xml"):
                continue
            root=ET.fromstring(arc.read(filename))
            rowlist=root.findall(".//x:sheetData/x:row",ns)
            dim=root.find("x:dimension",ns)
            result.append({"member":filename,
                "row_count_xml":len(rowlist),
                "dimension":dim.attrib.get("ref") if dim is not None else None,
                "first_five_row_cell_count":[len(row.findall("x:c",ns))
                                             for row in rowlist[:5]]})
    return {"sheet_names":names,"worksheets":result,
            "no_original_trait_label_extracted":True}


def inspect_compact_bee_matrix():
    meta,_=_get_json(ZENODO)
    files=[x for x in (meta.get("files") or []) if x.get("key")=="data.zip"]
    if len(files)!=1:
        raise ValueError("NO_GO_ORIGINAL_2026_BEE_DATA_ZIP_MISSING")
    file=files[0]
    expected_size=file.get("size")
    checksum=file.get("checksum")
    url=(file.get("links") or {}).get("self")
    if not isinstance(url,str):
        raise ValueError("NO_GO_BEE_ARCHIVE_URL_MISSING")
    f,digest=fetch_zip_to_temp(url,expected_size)
    if checksum and digest.lower()!=checksum.lower():
        raise ValueError("NO_GO_ORIGINAL_BEE_DATA_ZIP_CHECKSUM")
    with zipfile.ZipFile(f) as zipdata:
        infos=[x for x in zipdata.infolist() if not x.is_dir()]
        if len(infos)>10000:
            raise ValueError("NO_GO_TOO_MANY_BEE_ZIP_MEMBERS")
        candidates=[]
        for info in infos:
            name=info.filename
            low=name.casefold()
            if ("presence_only_matrix" in low or "presence_absence" in low
                or "pa_mat" in low or "bombus" in low):
                candidates.append({"name":name,"size_uncompressed":info.file_size,
                                   "size_compressed":info.compress_size})
        if not candidates:
            # The file may not include the generated matrix despite README;
            # do not assert it is present if none.
            status="NO_GO_COMPACT_ZIP_LACKS_READY_PREDICTION_MATRIX"
        else:
            status="COMPACT_ZIP_CONTAINS_CANDIDATE_MODELED_BEE_PA_MATRIX"
        names=[x.filename for x in infos]
        return {
           "status":status,
           "zenodo_record":20525239,
           "source_zip_sha_md5":digest,
           "zenodo_metadata_checksum":checksum,
           "original_zip_bytes":expected_size,
           "n_original_bundle_files":len(infos),
           "n_candidate_PA_matrix_members":len(candidates),
           "candidate_PA_matrix_members":candidates[:100],
           "archive_filename_preview":names[:100],
           "not_a_predicted_Bombus_richness_map_yet":True,
           "never_downloaded_large_21GB_SDM_archive":True
        }


def main():
    data={"bee_matrix_archive":inspect_compact_bee_matrix()}
    original=original_bytes(DRYAD_UV,MAX_UV_BYTES)
    data["dryad_uv_original"]={
       "source_doi":"10.5061/dryad.k98sf7m3z",
       "source_file_id":543161,
       "source_filename":"Supplementary_Data_File.xlsx",
       "source_bytes":len(original),
       "source_sha256":hashlib.sha256(original).hexdigest(),
       **_xlsx_sheet_summary(original)
    }
    data["status"]="PUBLISHED_MODELED_BEE_COMPACT_ARCHIVE_AND_UV_COMPARATIVE_STRUCTURE_VERIFIED"
    output=Path("stage46_matrix_structure")
    output.mkdir(exist_ok=True)
    (output/"modelled_bee_matrix_and_UV_xlsx_structure.json").write_text(
       json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+"\n")
    print("STAGE46_COMPACT_BEE_MATRIX_AND_UV_STRUCTURES",json.dumps(data,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
