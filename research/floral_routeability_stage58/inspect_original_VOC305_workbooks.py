"""Stage58: original 2020 floral VOC supplementary workbook row/column schema.

Farré-Armengol et al 2020 DOI 10.3389/fpls.2020.01154 source OA
EuropePMC source read (one ZIP, 24 members verified Stage58), original
DataSheet_1/2/3 XLSX SHA-256 identifiers pinned from live source.
The goal is to determine which original sheet encodes plant-species
identity × volatile compound × geography × guild, not to assume all
305 named plants have measured plant-specific scent loss/presence.

No raw original workbook, commercial VOC identities, or licensed metadata
rehosted: outputs only bounded rows/headers and numeric matrix shape.
"""
from __future__ import annotations
import hashlib,io,json,zipfile,urllib.error,urllib.request
from pathlib import Path

URL="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7412988/supplementaryFiles"
MEMBERS={
 "DataSheet_1.xlsx":"918ebcf51db693eb14ae8dec5eca1cb19fd48513cc345af050070d24e88ffe45",
 "DataSheet_2.xlsx":"bc3c788793dfd6c26f489d240328882a0adb3025d1afd5ddfe49d2ec1b221e79",
 "DataSheet_3.xlsx":"1b25abdad31a2ede3032b654eac7b452ccfa60784cc3e44cc41a626f2e16a17a",
}
MAX_ZIP_BYTES=20_000_000

def download_source():
    req=urllib.request.Request(URL,headers={"Accept":"application/zip",
       "User-Agent":"adaptive-gain-stage58-original-305-floral-VOC-source-xlsx/2026"})
    with urllib.request.urlopen(req,timeout=75) as r:
        b=r.read(MAX_ZIP_BYTES+1)
    if len(b)>MAX_ZIP_BYTES or not zipfile.is_zipfile(io.BytesIO(b)):
        raise ValueError("NO_GO_AUTHORED_FARRE_SOURCE_ZIP_BOUNDS")
    return b

def bounded_text(value):
    s=" ".join(str(value if value is not None else "").split())
    return s[:120]

def inspect_source_workbooks(b):
    from openpyxl import load_workbook
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        out={}
        for name,pin in MEMBERS.items():
            matches=[f for f in z.infolist() if not f.is_dir() and Path(f.filename).name==name]
            if len(matches)!=1:
                raise ValueError("NO_GO_ORIGINAL_VOC_SOURCE_WORKBOOK_ID_NOT_UNIQUE")
            raw=z.read(matches[0])
            if hashlib.sha256(raw).hexdigest()!=pin:
                raise ValueError("NO_GO_ORIGINAL_VOC_WORKBOOK_INNER_SHA_CHANGED")
            wb=load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
            tables=[]
            for ws in wb.worksheets:
                first=[]
                for j,row in enumerate(ws.iter_rows(values_only=True)):
                    if j>=5:break
                    first.append([bounded_text(v) for v in row[:18]])
                tables.append({
                  "sheet_name":ws.title[:80],
                  "max_row_reported":ws.max_row,
                  "max_col_reported":ws.max_column,
                  "first_5_rows_source_schema_only":first,
                  "no_species_trait_labels_inferred_from_source_schema":True
                })
            wb.close()
            out[name]={"source_original_inner_sha256":pin,
                       "source_original_workbook_bytes":len(raw),
                       "worksheets":tables}
    return {"status":"SOURCE_AUTHENTIC_FARRE_2020_3_VOC_WORKBOOKS_SCHEMA",
            "original_supplement_url":URL,
            "source_paper_doi":"10.3389/fpls.2020.01154",
            "source_authored_workbooks":out,
            "no_305_row_species_mapping_or_817_union_claim":True,
            "no_absent_VOC_phenotype_inferred_from_empty_XLSX_cell":True}

def main():
    out=Path("stage58_original_305_voc_workbook_schemas")
    out.mkdir(exist_ok=True)
    try:
        report=inspect_source_workbooks(download_source())
    except (ValueError,urllib.error.HTTPError,urllib.error.URLError,TimeoutError,
            zipfile.BadZipFile) as exc:
        report={"status":"SOURCE_VOC_ORIGINAL_WORKBOOKS_UNAVAILABLE_NOT_SCENT_NEGATIVE",
                "source_paper_doi":"10.3389/fpls.2020.01154",
                "error_type":type(exc).__name__,"error_summary":str(exc)[:190]}
    (out/"original_Farre_305_851_VOC_tables_source_columns.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("STAGE58_SOURCE_305_VOC_ORIGINAL_WORKBOOK_SCHEMA",
          json.dumps(report,ensure_ascii=False,sort_keys=True))
    print("NO_VOC_EMISSION_ABSENCE_FOR_UNMEASURED_SPECIES_OR_MODALITY_POOL")
if __name__=="__main__":
    main()
