"""Inspect authentic Tunes et al 2021 UV floral pattern source Table S2.

A methodological schema check, not a new fitted UV/bee association.
Source: doi:10.3389/fpls.2021.618028, author public supplementary
Data_Sheet_2 PDF (Creative Commons Attribution paper).
"""
import hashlib
import json
from pathlib import Path
import urllib.request

URL="https://public-pages-files-2025.frontiersin.org/articles/618028/file/Data_Sheet_2.pdf/618028_supplementary-materials_datasheets_2_pdf/2"
MAX_BYTES=12_000_000

def inspect_source():
    import fitz
    req=urllib.request.Request(URL,headers={
        "User-Agent":"adaptive-gain-stage45-original-UV-supplement-audit/2026",
        "Accept":"application/pdf"
    })
    with urllib.request.urlopen(req,timeout=60) as response:
        blob=response.read(MAX_BYTES+1)
    if not blob.startswith(b"%PDF-") or len(blob)>MAX_BYTES:
        raise ValueError("NO_GO_UNEXPECTED_AUTHOR_PDF")
    with fitz.open(stream=blob,filetype="pdf") as pdf:
        result={"source_url":URL,"original_pdf_sha256":hashlib.sha256(blob).hexdigest(),
                "pdf_pages":len(pdf),"page_tables":[]}
        for pageno,p in enumerate(pdf):
            table_records=[]
            tables=p.find_tables(strategy="lines")
            for table in tables.tables:
                cells=table.extract()
                table_records.append({
                   "bbox":[round(float(x),2) for x in table.bbox],
                   "n_rows":len(cells),
                   "first_three_rows":[[(c or "")[:115] for c in row]
                                       for row in cells[:3]],
                   "max_columns":max((len(row) for row in cells),default=0)
                })
            result["page_tables"].append({
                "page_number_1based":pageno+1,
                "text_length":len(p.get_text("text")),
                "table_count":len(table_records),
                "tables":table_records
            })
    result["status"]="ORIGINAL_2021_UV_TABLE_EXTRACTION_PROBE_NOT_SPECIES_REGISTRY"
    return result

if __name__=="__main__":
    r=inspect_source()
    p=Path("stage45_uv_supplement_probe");p.mkdir(exist_ok=True)
    (p/"source_table_structure.json").write_text(
       json.dumps(r,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("UV_ORIGINAL_PDF_TABLE_PROBE",json.dumps(r,ensure_ascii=False))
