"""Stage49: audit machine-readable published floral UV taxa data before merging.

This obtains ORIGINAL published Dryad .xlsx study datasets when openly
accessible. It is a source/worksheet-content discovery, NOT an inferred
UV-pattern label, species occurrence model, or novel biological result.

Three independent study units:
  2016 Koski & Ashman, New Phytologist, 177 Potentilleae taxa, UV phenotype
  2020 Koski, Frontiers Plant Science, overlap of same 177 taxa PLUS visible
       floral pattern and size: not a second independent species sample.
  2020 Koski/MacQueen/Ashman, Current Biology, 42 taxa/1,238 herbarium
       specimens across three continents, UV pigment area across time.
Dryad file URLs are public identifiers; HTTP 403/429/406 is recorded as
unavailable, never reinterpreted as zero species.
"""
from __future__ import annotations
import hashlib
import io
import json
import urllib.error
import urllib.request
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

DOIS={
  "POTENTILLEAE_177":"10.5061/dryad.k98sf7m3z",
  "THREE_CONTINENT_42":"10.5061/dryad.ttdz08kw1",
}
DATASET_FILE_CANDIDATES={
  "POTENTILLEAE_177":[
    ("https://datadryad.org/downloads/file_stream/543161",
     "Supplementary_Data_File.xlsx"),
  ],
  "THREE_CONTINENT_42":[
    ("https://datadryad.org/downloads/file_stream/401217",
     "Koski_et_al._Current_Biology_Data.xlsx"),
  ]
}
MAX_BYTES=1_100_000
XML_MAIN="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
XML_REL="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS={"x":XML_MAIN}
BASE_API="https://datadryad.org/api/v2/datasets/"

def _fetch(url,maxbytes=MAX_BYTES):
    if not any(url.startswith(prefix) for prefix in (
        "https://datadryad.org/",
        "https://api.datadryad.org/",
    )):
        raise ValueError("NO_GO_SOURCE_HOST_NOT_ALLOWLISTED")
    req=urllib.request.Request(url,headers={
        "Accept":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/json,*/*",
        "User-Agent":"adaptive-gain-stage49-public-Dryad-original-data-audit/2026"
    })
    with urllib.request.urlopen(req,timeout=35) as result:
        content_type=result.headers.get("Content-Type","")
        data=result.read(maxbytes+1)
        status=result.status
    if len(data)>maxbytes:
        raise ValueError("NO_GO_SOURCE_FILE_SIZE_EXCEEDS_BOUNDED_LIMIT")
    return data,status,content_type

def _header_from_excel(blob):
    """Inspect xlsx via ZIP+XML schema, never interpret numeric UV data yet."""
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError("NO_GO_SOURCE_FILE_NOT_GENUINE_XLSX_ZIP")
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names=z.namelist()
        if "xl/workbook.xml" not in names:
            raise ValueError("NO_GO_SOURCE_XLSX_WORKBOOK_PART_ABSENT")
        book=ET.fromstring(z.read("xl/workbook.xml"))
        sheets=[
            {"name":tag.attrib.get("name"),
             "sheet_id":tag.attrib.get("sheetId"),
             "relationship_id":tag.attrib.get("{%s}id"%XML_REL)}
            for tag in book.findall("x:sheets/x:sheet",NS)
        ]
        shared=[]
        if "xl/sharedStrings.xml" in names:
            root=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("x:si",NS):
                shared.append("".join(t.text or "" for t in si.findall(".//x:t",NS)))
        probes=[]
        for fname in sorted(n for n in names if n.startswith("xl/worksheets/sheet")
                            and n.endswith(".xml"))[:8]:
            root=ET.fromstring(z.read(fname))
            rows=[]
            for row in root.findall(".//x:sheetData/x:row",NS)[:9]:
                values=[]
                for cell in row.findall("x:c",NS)[:20]:
                    kind=cell.attrib.get("t")
                    v=cell.find("x:v",NS)
                    inline=cell.find("x:is",NS)
                    raw=(v.text or "") if v is not None else ""
                    if kind=="s" and raw.isdigit():
                        idx=int(raw)
                        raw=shared[idx] if idx<len(shared) else "NO_GO_SHARED_STRING_INDEX_OUTSIDE_ARRAY"
                    elif kind=="inlineStr" and inline is not None:
                        raw="".join(x.text or "" for x in inline.findall(".//x:t",NS))
                    values.append({"cell":cell.attrib.get("r"),
                                   "kind":kind or "numeric_or_formula",
                                   "preview":raw[:120]})
                rows.append(values)
            probes.append({"worksheet_part":fname,
                           "first_nine_source_row_cells":rows})
    return {"sheet_manifest":sheets,"worksheet_first_rows":probes,
            "n_shared_strings":len(shared),
            "source_xlsx_bytes_sha256":hashlib.sha256(blob).hexdigest(),
            "never_infer_UV_pattern_from_unreviewed_sheet":True}

def probe():
    receipt={"status":"LITERATURE_ORIGINAL_UV_STUDY_WORKBOOK_SOURCE_PROBE",
             "sources":{},"no_independent_177_plus_177_double_count":True,
             "source_are_real_published_studies_not_image_derived":True}
    for key,doi in DOIS.items():
        entry={"dataset_doi":doi,"attempts":[],"workbook":None,
               "is_not_a_novel_uv_bombus_geographic_test":True}
        api=BASE_API+"doi%3A"+doi.replace("/","%2F")
        try:
            raw,status,ct=_fetch(api,100_000)
            j=json.loads(raw)
            entry["api"]={
               "http_status":status,
               "json_top_keys":list(j)[:25],
               "api_dataset_id":j.get("id"),
               "current_version":j.get("versionNumber"),
               "current_version_id":(j.get("_links") or {}).get("stash:version",{}),
            }
        except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
                TimeoutError,json.JSONDecodeError) as e:
            entry["api_error"]={"kind":type(e).__name__,
                                "detail":str(e)[:180]}
        for url,expected in DATASET_FILE_CANDIDATES[key]:
            attempt={"file_expected":expected,"original_public_url":url}
            try:
                raw,status,ct=_fetch(url)
                attempt.update({"status":"BYTES_RETRIEVED",
                                "http_status":status,"content_type":ct,
                                "size":len(raw)})
                entry["workbook"]=_header_from_excel(raw)
                attempt["status"]="GENUINE_XLSX_WORKBOOK_VERIFIED"
            except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
                    TimeoutError,ET.ParseError) as e:
                attempt["status"]="SOURCE_NOT_RETRIEVED_OR_INVALID_NO_SPECIES_CLAIM"
                attempt["error_kind"]=type(e).__name__
                attempt["error_detail"]=str(e)[:220]
            entry["attempts"].append(attempt)
            if attempt["status"]=="GENUINE_XLSX_WORKBOOK_VERIFIED":
                break
        receipt["sources"][key]=entry
    return receipt

def main():
    result=probe()
    p=Path("stage49_source_receipts")
    p.mkdir(exist_ok=True)
    (p/"published_uv_study_workbook_schema.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
        encoding="utf8")
    print("STAGE49_ORIGINAL_LITERATURE_XLSX_SOURCE_PROBE",
          json.dumps(result,ensure_ascii=False,sort_keys=True,allow_nan=False))
    # A negative source result MUST not be labeled a successful acquisition.
    for k,v in result["sources"].items():
        if v["workbook"] is None:
            print("NOT_VERIFIED_NO_SPECIES_EXTRACTED",k)

if __name__=="__main__":
    main()
