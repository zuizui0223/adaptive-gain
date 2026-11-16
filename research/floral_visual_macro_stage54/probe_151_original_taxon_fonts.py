"""Minimal font/position audit of source-authenticated 2025 S1 visual-change taxa."""
import json
from pathlib import Path
import fitz
from inspect_151_color_change_table_layout import get_original_pdf,PINNED_PDF

def inspect():
    d={"status":"REAL_SOURCE_151_TAXON_COLUMN_FONT_GEOMETRY",
       "source_PDF_sha256":PINNED_PDF,"pages":[]}
    original=get_original_pdf()
    with fitz.open(stream=original,filetype="pdf") as pdf:
        for i in (1,2,4,7,12,17):
            p=pdf[i]
            spans=[]
            for block in p.get_text("dict")["blocks"]:
                for line in block.get("lines",[]):
                    for span in line["spans"]:
                        if span["text"].strip() and span["bbox"][1]>60:
                            spans.append({
                                "text":span["text"].strip()[:85],
                                "x0":round(span["bbox"][0],1),
                                "y0":round(span["bbox"][1],1),
                                "font":span["font"],
                                "flags":span["flags"],
                                "size":round(span["size"],1)
                            })
            d["pages"].append({"page":i+1,
                               "n_source_spans":len(spans),
                               "first_42_spans":spans[:42]})
    return d
if __name__=="__main__":
    r=inspect()
    p=Path("stage54_151_taxon_fonts");p.mkdir(exist_ok=True)
    (p/"source_original_151_taxon_column_fonts.json").write_text(
        json.dumps(r,indent=2,ensure_ascii=False)+"\n")
    print("STAGE54_151_REAL_TAXON_FONT_COORDINATES",json.dumps(r,ensure_ascii=False))
