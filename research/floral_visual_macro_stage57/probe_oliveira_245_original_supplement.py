"""Stage57: original 2025 Oliveira et al. 245-flower UV / bee-vs-bird table probe.

Source paper: DOI 10.1111/plb.70138, PMCID PMC12710832.
The paper states 245 analysed plant species and a supplementary DOCX Table S1
which includes source UV reflection, flower hue, botanical species and primary
pollination system (bee/bird). Be aware text elsewhere contains 292 colour
summary denominators: never silently merge 245 and 292.
Check original Europe PMC OA supplemental ZIP for the exact primary Table S1,
then read DOCX XML *table shape* and limited headers only. This is a source
identity/access/field audit, NOT 245 published biology records claimed to be
imported. Never assume raw 204 previously unpublished spectra are public
record-level files or that single average UV reflectance means a nectar guide.
"""
from __future__ import annotations
import hashlib,io,json,re,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
import urllib.error,urllib.request

SOURCE_DOI="10.1111/plb.70138"
SOURCE_PMID="PMC12710832"
SOURCE_API="https://www.ebi.ac.uk/europepmc/webservices/rest/"+SOURCE_PMID+"/supplementaryFiles"
TABLE_NAME="plb70138-sup-0003-TableS1-S8.docx"
MAX_EPMC_ZIP=17_000_000
MAX_DOCX=1_200_000
MAX_XML=5_000_000
NS="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

def fetch_original():
    req=urllib.request.Request(SOURCE_API,headers={
       "User-Agent":"adaptive-gain-stage57-author-2025-original-floral-UV245-supplement/2026",
       "Accept":"application/zip,application/octet-stream,*/*"})
    with urllib.request.urlopen(req,timeout=60) as r:
        body=r.read(MAX_EPMC_ZIP+1)
        mime=r.headers.get("Content-Type","")
    if len(body)>MAX_EPMC_ZIP:raise ValueError("NO_GO_SUPPLEMENT_SOURCE_TOO_LARGE")
    return body,mime

def inspect_docx_table(raw):
    if len(raw)>MAX_DOCX or not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("NO_GO_EXPECTED_PRIMARY_SOURCE_DOCX")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        if "word/document.xml" not in names:
            raise ValueError("NO_GO_NOT_AN_AUTHOR_ORIGINAL_DOCX")
        if z.getinfo("word/document.xml").file_size>MAX_XML:
            raise ValueError("NO_GO_AUTHOR_DOCX_XML_TOO_BIG")
        body=z.read("word/document.xml")
    doc=ET.fromstring(body)
    tables=[]
    for tbl in doc.iter(NS+"tbl"):
        rows=list(tbl.iter(NS+"tr"))
        cell_counts=[]
        previews=[]
        for i,row in enumerate(rows):
            cells=list(row.iter(NS+"tc"))
            cell_counts.append(len(cells))
            if i<3:
                previews.append([" ".join(
                    ("".join(x.itertext())).strip().split())[:105]
                    for x in cells[:10]])
        tables.append({
            "source_table_index":len(tables)+1,
            "n_docx_table_rows":len(rows),
            "cell_columns_min":min(cell_counts) if cell_counts else 0,
            "cell_columns_max":max(cell_counts) if cell_counts else 0,
            "first_3_row_schema_cell_snippets":previews,
            "not_certified_245_source_species":True,
        })
    return {"status":"ORIGINAL_2025_UV245_PRIMARY_DOCX_SUPPLEMENT_TABLE_SHAPE",
            "source_DOI":SOURCE_DOI,
            "source_table_member":TABLE_NAME,
            "docx_SHA256":hashlib.sha256(raw).hexdigest(),
            "n_tables_in_original_DOCX":len(tables),
            "first_15_original_tables":tables[:15],
            "n_possible_large_species_tables":sum(t["n_docx_table_rows"]>=200 for t in tables),
            "no_false_245_distinct_accepted_species_claim":True,
            "no_UV_spatial_guide_label_from_average_UV_fraction":True}

def inspect_public_archive(body,mime):
    if not zipfile.is_zipfile(io.BytesIO(body)):
        raise ValueError("NO_GO_ORIGINAL_EUROPE_PMC_SUPPLEMENT_NOT_ZIP")
    with zipfile.ZipFile(io.BytesIO(body)) as z:
        listings=[{"name":Path(q.filename).name,
                   "uncompressed_bytes":q.file_size}
                  for q in z.infolist() if not q.is_dir()]
        subset=[q for q in z.infolist()
                if Path(q.filename).name==TABLE_NAME and not q.is_dir()]
        if len(subset)!=1:
            return {
              "status":"AUTHOR_DOCX_TABLE_S1_NOT_FOUND_IN_OA_SUPPLEMENT_ARCHIVE",
              "archive_members":listings,
              "no_false_source_table_extraction":True
            }
        if subset[0].file_size>MAX_DOCX:
            raise ValueError("NO_GO_SOURCE_TABLE_DOCX_TOO_LARGE")
        member=z.read(subset[0])
    return {"status":"AUTHOR_ORIGINAL_TABLE_S1_DOCUMENT_SCHEMA_RETRIEVED",
            "archive_sha256":hashlib.sha256(body).hexdigest(),
            "zip_content_type":mime,
            "archive_members":listings,
            "original_primary_table":inspect_docx_table(member),
            "no_spectra_or_species_original_row_reconstruction":True}

def main():
    output=Path("stage57_Oliveira245_original_source_audit")
    output.mkdir(exist_ok=True)
    try:
        orig,mime=fetch_original()
        result=inspect_public_archive(orig,mime)
    except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
            TimeoutError,zipfile.BadZipFile,ET.ParseError) as e:
        result={"status":"ORIGINAL_2025_UV245_SOURCE_NOT_AVAILABLE_NO_FALSE_ROWS",
                "error_type":type(e).__name__,
                "error_summary":str(e)[:240]}
    result["source_paper_DOI"]=SOURCE_DOI
    result["source_original_PMCID"]=SOURCE_PMID
    result["source_official_supplement_API"]=SOURCE_API
    result["review_245_vs_text_292_denominator_must_be_reconciled_in_primary_table"]=True
    result["no_245_direct_UV_patterns_or_Bombus_native_effect_claimed"]=True
    (output/"2025_Oliveira_original_UV245_bee_bird_source_supplement_receipt.json").write_text(
       json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("STAGE57_2025_UV245_ORIGINAL_SOURCE_TABLE_S1_GATE",
          json.dumps(result,ensure_ascii=False,sort_keys=True))
    print("NO_NEW_245_SOURCE_ROWS_ADDED_TO_EXISTING_583_ORIGINAL_ATLAS")

if __name__=="__main__":
    main()
