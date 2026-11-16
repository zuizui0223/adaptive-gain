"""Inspect late pages of the original 151-colour-changing species S1.

No original copyrighted page text is redistributed; only taxon-column
counts and provisional italic name tokens. Preserve PDF checksum gate.
"""
from inspect_151_color_change_table_layout import get_original_pdf,PINNED_PDF
from extract_colorchange_151_review_taxa import (
 normalized_spans,group_italic_taxa,match_original_colour
)
import hashlib,json
from pathlib import Path
import fitz
def diagnose():
    b=get_original_pdf()
    if hashlib.sha256(b).hexdigest()!=PINNED_PDF:
        raise ValueError("NO_GO_SOURCE_2025_REVIEW_PDF_SHA")
    with fitz.open(stream=b,filetype="pdf") as pdf:
        pages=[]
        for i in range(18,len(pdf)):
            p=pdf[i]
            spans=normalized_spans(p)
            taxa=group_italic_taxa(spans)
            pages.append({"page":i+1,
                          "n_italic_taxon_columns":len(taxa),
                          "n_binomial_candidates":sum(bool(x["binomial_candidate"]) for x in taxa),
                          "candidate_source_names":[x["full_original_italic_taxon_text"] for x in taxa[:19]],
                          "page_first_10_nonblank_tokens":p.get_text("text").splitlines()[:10]})
    return {"status":"PINNED_2025_SOURCE_REVIEW_LATE_PAGE_TAXON_DIAGNOSTIC",
            "source_pdf_sha256":PINNED_PDF,
            "pages":pages}
if __name__=="__main__":
    v=diagnose()
    output=Path("stage54_151_tail_diagnostic");output.mkdir(exist_ok=True)
    (output/"late_source_pages_19_to_23.json").write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
    print("STAGE54_SOURCE_REVIEW_151_LATE_PAGE_TAXA",json.dumps(v,ensure_ascii=False))
