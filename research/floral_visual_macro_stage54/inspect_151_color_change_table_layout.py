"""Diagnostic layout only: official 2025 colour-change 151 review Table S1 PDF."""
import hashlib,io,json,zipfile
from pathlib import Path
from probe_multimodal_original_literature import _fetch,EUROPE_PMC
from inspect_nested_visual_trait_tables import PINNED_INNER_SHA,REVIEW_INNER
PDF_NAME="plants-3703510-supplementary.pdf"
PINNED_PDF="0c2ba82cd6eb554942fc3ac93014f7ecc9834686f695cf628f2873a2be213039"
def get_original_pdf():
    outer,_=_fetch(EUROPE_PMC)
    with zipfile.ZipFile(io.BytesIO(outer)) as z:
        inner=z.read(REVIEW_INNER)
    if hashlib.sha256(inner).hexdigest()!=PINNED_INNER_SHA:
        raise ValueError("NO_GO_SUPPLEMENT_NESTED_HASH")
    with zipfile.ZipFile(io.BytesIO(inner)) as z:
        b=z.read(PDF_NAME)
    if hashlib.sha256(b).hexdigest()!=PINNED_PDF:
        raise ValueError("NO_GO_SOURCE_151_TABLE_PDF_HASH")
    return b

def inspect_layout():
    import fitz
    b=get_original_pdf()
    out={"status":"SOURCE_ORIGINAL_151_TABLE_LAYOUT_DIAGNOSTIC",
         "paper_doi":"10.3390/plants14142185",
         "source_supplement_PDF_SHA256":PINNED_PDF,"pages":[]}
    with fitz.open(stream=b,filetype="pdf") as pdf:
        if len(pdf)!=23:
            raise ValueError("NO_GO_PDF_ORIGINAL_23_PAGES")
        for idx in range(1,18):
            page=pdf[idx]
            txt=page.get_text("text")
            lines=[line.strip() for line in txt.splitlines() if line.strip()]
            tables=[]
            for strategy in ("lines","text"):
                try:
                    found=page.find_tables(strategy=strategy)
                    for t in found.tables[:4]:
                        cells=t.extract()
                        tables.append({
                            "strategy":strategy,"rows":len(cells),
                            "columns_max":max((len(r) for r in cells),default=0),
                            "header_and_sample_cell_lengths":[
                                [len(s or "") for s in row[:9]] for row in cells[:2]],
                            "source_first_two_table_rows":[
                                [(s or "")[:90] for s in row[:9]] for row in cells[:2]]
                        })
                except Exception as err:
                    tables.append({"strategy":strategy,"error":type(err).__name__})
            out["pages"].append({
              "page":idx+1,"n_lines":len(lines),"tables":tables,
              "source_first_25_lines":lines[:25] if idx in (1,2,3) else [],
              "source_last_12_lines":lines[-12:] if idx in (16,17) else []
            })
    return out
if __name__=="__main__":
    q=inspect_layout()
    folder=Path("stage54_151_original_table_layout")
    folder.mkdir(exist_ok=True)
    (folder/"source_original_151_pages_2_to_18_table_layout.json").write_text(
        json.dumps(q,ensure_ascii=False,indent=2)+"\n")
    print("STAGE54_151_PUBLISHED_SOURCE_TABLE_LAYOUT",json.dumps(q,ensure_ascii=False))
