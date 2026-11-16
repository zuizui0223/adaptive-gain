"""Stage49: primary-paper PDF Table S1 source schema for three-continent UV taxa.

Source is the CC BY-NC-ND Open-Access Koski, MacQueen & Ashman (2020)
Current Biology PDF containing Supplementary Table S1, DOI
10.1016/j.cub.2020.08.077. Only derived taxon/location categorical
data planned, not redistribution of original PDF or whole S1 page.

The original paper reports 42 species from 1,238 herbarium specimens.
Do not assert a numeric unique count from PDF page text without parsing
and source-gating it.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

SOURCE_URL=("https://mobot-biodiversity-jc.weebly.com/uploads/1/8/6/0/"
            "18603232/05-koski_et_al._2020_floral_pigmentation_has_"
            "responded_rapidly_to_global_change_in_ozone_and_temperature.pdf")
MAX_BYTES=15_000_000

def probe_original_pdf():
    import fitz
    req=urllib.request.Request(SOURCE_URL,headers={
       "User-Agent":"adaptive-gain-stage49-original-2020-Current-Biology-S1/2026",
       "Accept":"application/pdf,*/*"
    })
    with urllib.request.urlopen(req,timeout=45) as stream:
        blob=stream.read(MAX_BYTES+1)
        ct=stream.headers.get("Content-Type","")
    if len(blob)>MAX_BYTES or not blob.startswith(b"%PDF-"):
        raise ValueError("NO_GO_SOURCE_PDF_NOT_VALID")
    result={
      "status":"OPEN_ACCESS_CURRENT_BIOLOGY_SUPPLEMENT_PRIMARY_TABLE_S1_PROBE",
      "article_doi":"10.1016/j.cub.2020.08.077",
      "source_url":SOURCE_URL,
      "source_pdf_sha256":hashlib.sha256(blob).hexdigest(),
      "source_pdf_bytes":len(blob),
      "pdf_content_type":ct,
      "pages":[],
      "not_Dryad_original_xlsx":True,
      "no_UV_guide_absence_from_herbarium_species_list":True
    }
    with fitz.open(stream=blob,filetype="pdf") as pdf:
        result["pdf_pages"]=len(pdf)
        for i in range(max(0,len(pdf)-4),len(pdf)):
            p=pdf[i]
            txt=p.get_text("text")
            lines=[z.strip() for z in txt.splitlines() if z.strip()]
            detected=[q for q in lines if q in ("Australia","Eurasia","N. America")]
            result["pages"].append({
              "page_index":i,
              "text_length":len(txt),
              "reported_continent_row_starts_in_text":len(detected),
              "source_text_first_65_nonblank_lines":lines[:65],
              "source_text_last_65_nonblank_lines":lines[-65:],
            })
    return result

if __name__=="__main__":
    r=probe_original_pdf()
    out=Path("stage49_current_biology_source")
    out.mkdir(exist_ok=True)
    (out/"original_42_species_Table_S1_page_schema.json").write_text(
       json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("STAGE49_ORIGINAL_PAPER_TABLE_S1_PDF_PROBE",json.dumps(r,ensure_ascii=False))
