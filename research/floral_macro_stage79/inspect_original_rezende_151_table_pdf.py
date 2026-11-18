"""Stage79C source Rezende 2025 original supplementary PDF table layout.

Public PMC12299958 original 9-member supplementary archive contains
plants-14-02185-s001.zip, inside plants-3703510-supplementary.pdf.
Publication's 151 positive colour-changers are NOT 151 measured negatives.
Read original PDF embedded text and render source page 1, no OCR or photos.
"""
from __future__ import annotations
import argparse,hashlib,io,json,subprocess,tempfile,urllib.request,zipfile,re
from pathlib import Path
SOURCE="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12299958/supplementaryFiles"
INNER_NAME="plants-14-02185-s001.zip"
INNER_SHA="a2af585bdc42cdc6e990c624c4328b808526e259bd21e0bd91fa39b5c316ff28"
PDF_NAME="plants-3703510-supplementary.pdf"
PDF_BYTES=254746

def original_pdf():
    req=urllib.request.Request(SOURCE,headers={
        "User-Agent":"adaptive-gain-2025-floral-change-supp-source/2026",
        "Accept":"application/zip"})
    with urllib.request.urlopen(req,timeout=75) as r:
        b=r.read(3_000_000)
    if not zipfile.is_zipfile(io.BytesIO(b)):
        raise ValueError("STAGE79C_EPMC_PUBLISHER_SUPPLEMENT_NOT_ZIP")
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        nested=z.read(INNER_NAME)
    if hashlib.sha256(nested).hexdigest()!=INNER_SHA:
        raise ValueError("STAGE79C_ORIGINAL_REZENDE_INNER_ZIP_SHA_CHANGED")
    with zipfile.ZipFile(io.BytesIO(nested)) as z:
        pdf=z.read(PDF_NAME)
    if len(pdf)!=PDF_BYTES or not pdf.startswith(b"%PDF"):
        raise ValueError("STAGE79C_SOURCE_ORIGINAL_PDF_NOT_AUTHENTIC")
    return pdf,hashlib.sha256(pdf).hexdigest()

def text_pages(b,out):
    with tempfile.TemporaryDirectory() as d:
        f=Path(d)/"original.pdf";f.write_bytes(b)
        meta=subprocess.run(["pdfinfo",str(f)],capture_output=True,text=True,check=True)
        s=subprocess.run(["pdftotext","-layout",str(f),"-"],
                         capture_output=True,text=True,check=True)
        if len(s.stdout)<400:
            raise ValueError("STAGE79C_PDF_EMBEDDED_TEXT_UNAVAILABLE")
        out.mkdir(exist_ok=True,parents=True)
        p=out/"original_page1"
        try:
            subprocess.run(["pdftoppm","-f","1","-l","1","-scale-to","1000","-png",
                            "-singlefile",str(f),str(p)],capture_output=True,check=True,timeout=50)
            rendered=p.with_suffix(".png").exists()
        except Exception:rendered=False
    return s.stdout,meta.stdout,rendered

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
    raw,sha=original_pdf()
    txt,meta,rendered=text_pages(raw,a.outdir/"renders")
    lines=txt.splitlines()
    species_re=re.compile(r"^[A-Z][a-zA-Z-]+ [a-z][a-z-]+$")
    naive=[line.strip() for line in lines if species_re.fullmatch(line.strip())]
    data={"schema":"stage79c_original_Rezende_2025_positive_only_colour_change_s1_PDF",
          "publication_DOI":"10.3390/plants14142185",
          "published_pos_151_species_NOT_CONFLATED_WITH_SCREENED_NEGATIVES":True,
          "original_pdf_sha256":sha,"source_pdf_bytes":len(raw),
          "source_nested_archive_sha256":INNER_SHA,
          "source_rendered_pdf_first_page":rendered,
          "source_pdf_info":meta[:2400],
          "source_pages_formfeed":txt.count("\f"),
          "source_text_characters":len(txt),
          "source_total_lines":len(lines),
          "source_first75_lines":[x[:180] for x in lines[:75]],
          "source_simple_binomial_lines_not_verified_as_table_taxon":naive[:40],
          "source_naive_binomial_line_count":len(naive),
          "actual_original_151_species_parsed_and_taxon_verified":False,
          "pdf_full_source_rows_NOT_automatically_extracted_as_species":True}
    (a.outdir/"rezende2025_original_pdf_table_schema_receipt.json").write_text(
        json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("STAGE79C_REAL_REZENDE_S1_PDF_TABLE_STRUCTURE",json.dumps(data,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
