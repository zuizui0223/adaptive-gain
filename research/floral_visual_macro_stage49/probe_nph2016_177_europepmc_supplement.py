"""Stage49 add-on: source probe for the 2016 Potentilleae original 177-species S2.

Official openly published supplemental title:
nph13921-sup-0001-FigS1-TablesS1-S2.pdf
DOI 10.1111/nph.13921, PMCID PMC6681094.
The publisher supplement URL returns HTTP 403 in this environment.
Instead test Europe PMC's public OA supplementary ZIP API. Do not
invent source names/UV pattern labels if supplementary file is unavailable.
Only report metadata, page count and bounded table headers, not an effect.
"""
from __future__ import annotations
import hashlib
import io
import json
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

PMC_ID="PMC6681094"
API="https://www.ebi.ac.uk/europepmc/webservices/rest/"+PMC_ID+"/supplementaryFiles"
NAME="nph13921-sup-0001-FigS1-TablesS1-S2.pdf"
SOURCE_DOI="10.1111/nph.13921"
MAX_BYTES=12_000_000
MAX_PDF_BYTES=5_000_000

def _fetch(url):
    if url!=API:
        raise ValueError("NO_GO_UNKNOWN_2016_SUPPLEMENT_SOURCE")
    req=urllib.request.Request(url,headers={
        "Accept":"application/zip,application/octet-stream,*/*",
        "User-Agent":"adaptive-gain-stage49-2016-nph177-published-supplement/2026"
    })
    with urllib.request.urlopen(req,timeout=55) as response:
        data=response.read(MAX_BYTES+1)
        content_type=response.headers.get("Content-Type","")
    if len(data)>MAX_BYTES:
        raise ValueError("NO_GO_SUPPLEMENT_TOO_LARGE")
    return data,content_type

def inspect(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError("NO_GO_NOT_EUROPEPMC_SUPPLEMENT_ZIP")
    files=[]
    pdf_records=[]
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for item in z.infolist():
            if item.is_dir() or len(item.filename)>250 or ".." in Path(item.filename).parts:
                continue
            info={"name":item.filename,"uncompressed_bytes":item.file_size}
            files.append(info)
            if item.filename.endswith(".pdf") and item.file_size<MAX_PDF_BYTES:
                original=z.read(item)
                if original.startswith(b"%PDF"):
                    try:
                        import fitz
                        with fitz.open(stream=original,filetype="pdf") as pdf:
                            text_pages=[{
                                "p":i+1,"text_length":len(p.get_text("text")),
                                "table_s2_references":p.get_text("text").lower().count("table s2"),
                                "first_lines":p.get_text("text").splitlines()[:25]
                            } for i,p in enumerate(pdf)]
                        pdf_records.append({
                            "name":item.filename,
                            "sha256":hashlib.sha256(original).hexdigest(),
                            "pages":len(text_pages),
                            "page_text_schema":text_pages
                        })
                    except (ValueError,RuntimeError) as e:
                        pdf_records.append({"name":item.filename,"error":type(e).__name__})
    return {
        "status":"ORIGINAL_NPH2016_177_SPECIES_SUPPLEMENT_INDEX_ONLY",
        "article_doi":SOURCE_DOI,
        "pmcid":PMC_ID,
        "source_names":files,
        "pdf_source_manifest":pdf_records,
        "no_new_verified_177_taxon_rows_yet":True,
        "not_a_visual_Bombus_geographic_effect":True,
    }

def main():
    output=Path("stage49_original_nph177")
    output.mkdir(exist_ok=True)
    receipt={"article_doi":SOURCE_DOI,"source_url":API}
    try:
        raw,content_type=_fetch(API)
        receipt.update(inspect(raw))
        receipt["original_zip_sha256"]=hashlib.sha256(raw).hexdigest()
        receipt["api_content_type"]=content_type
    except (ValueError,urllib.error.URLError,urllib.error.HTTPError,TimeoutError) as e:
        receipt["status"]="UNAVAILABLE_NO_177_SPECIES_PER_ROW_EXTRACTION"
        receipt["error_type"]=type(e).__name__
        receipt["error_summary"]=str(e)[:170]
    (output/"europe_pmc_nph177_original_supplement_index.json").write_text(
        json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8"
    )
    print("STAGE49_NPH_2016_ORIGINAL_177_SOURCE_PROBE",
          json.dumps(receipt,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()
