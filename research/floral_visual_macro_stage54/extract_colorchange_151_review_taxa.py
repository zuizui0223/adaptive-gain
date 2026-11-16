"""Stage54: extract 2025 review's compiled floral colour-change species names.

Author original OA Supplemental Table S1 from Plants (2025) doi
10.3390/plants14142185, preserved source PDF SHA from prior source audit.
The table is ROTATED; rows are laid out with a given taxon at an
x-column and taxon text at approx y 560..685, colour transition y 470..530.
Use character/format rather than page plain-text order to reconstruct
taxon names, retain source page and X coordinate for independent audit.

This is an inherently POSITIVE-only LITERATURE REVIEW list of taxa
reported as showing developmental flower-colour change. It does not
contain 151 source measured nonchanging negative species. It does not
prove changed colour is a reward/bee informational cue or wind response.
All binomial mappings are provisional until original source review.
"""
from __future__ import annotations
import csv,json,hashlib,re,statistics
from collections import Counter
from pathlib import Path

from inspect_151_color_change_table_layout import get_original_pdf,PINNED_PDF

FONT_ITALIC="italic"
TABLE_PAGE_INDICES=range(1,18)
TAXON_Y_MIN,TAXON_Y_MAX=550,688
COLOUR_Y_MIN,COLOUR_Y_MAX=470,532
FIRST_COLUMN_X=77
MAX_CONTINUATION_INDENT=13.8
ABBREVIATED_RE=re.compile(r"(^| )(?:sp\.|spp\.|cf\.|aff\.)($| )",re.I)
BINOMIAL_RE=re.compile(r"\b([A-Z][A-Za-z-]+)\s+([a-z][a-z-]+)(?=\s|$)")


def normalized_spans(page):
    out=[]
    for block in page.get_text("dict").get("blocks",[]):
        for line in block.get("lines",[]):
            for span in line.get("spans",[]):
                value=" ".join(str(span.get("text","")).split())
                if not value:continue
                bbox=span.get("bbox",())
                if len(bbox)<4:continue
                out.append({
                    "value":value,
                    "x0":round(float(bbox[0]),3),
                    "y0":round(float(bbox[1]),3),
                    "font":span.get("font",""),
                    "size":float(span.get("size",0)),
                })
    return out


def group_italic_taxa(spans):
    italic=[x for x in spans
            if (TAXON_Y_MIN<=x["y0"]<=TAXON_Y_MAX
                and FONT_ITALIC in x["font"].lower()
                and 8.2<=x["size"]<=10.0
                and x["x0"]>=FIRST_COLUMN_X)]
    # The column direction is x, while text continues down a column
    # with a 12-pt x-offset. The next species column starts >=16pt away.
    italic.sort(key=lambda q:(q["x0"],-q["y0"]))
    groups=[]
    for span in italic:
        if groups and span["x0"]-groups[-1]["origin_x"]<=MAX_CONTINUATION_INDENT:
            groups[-1]["tokens"].append(span)
        else:
            groups.append({"origin_x":span["x0"],"tokens":[span]})
    rows=[]
    for g in groups:
        tokens=sorted(g["tokens"],key=lambda s:(-s["y0"],s["x0"]))
        assembled=" ".join(x["value"] for x in tokens)
        # Some original citations/author strings are italic: do not
        # manufacture a species when source has only a genus name.
        match=BINOMIAL_RE.search(assembled)
        rows.append({
            "column_x":g["origin_x"],
            "full_original_italic_taxon_text":assembled,
            "binomial_candidate":(match.group(1)+" "+match.group(2)) if match else "",
            "taxonomy_resolution":"ORIGINAL_REVIEW_BINOMIAL_UNRECONCILED" if match and not ABBREVIATED_RE.search(assembled)
                                  else "GENUS_ONLY_OR_UNRESOLVED_SOURCE_TABLE",
            "token_count":len(tokens),
        })
    return rows


def match_original_colour(italic_groups,allspans):
    color=[x for x in allspans if
           (COLOUR_Y_MIN<=x["y0"]<=COLOUR_Y_MAX
            and x["x0"]>=FIRST_COLUMN_X and
            not x["value"].startswith("("))]
    for group in italic_groups:
        origin=group["column_x"]
        tokens=[x for x in color if (abs(x["x0"]-origin)<=3.2 or
                                   (0<=x["x0"]-origin<=13 and len(x["value"])>8))]
        tokens=sorted(tokens,key=lambda s:-s["y0"])
        group["original_source_colour_transition_text"]=" ".join(x["value"] for x in tokens)[:230]
        group["source_colour_transition_nonempty"]=bool(tokens)
    return italic_groups


def parse_document(pdf):
    rows=[]
    pages=[]
    for idx in TABLE_PAGE_INDICES:
        page=pdf[idx]
        spans=normalized_spans(page)
        taxa=group_italic_taxa(spans)
        match_original_colour(taxa,spans)
        for row in taxa:
            row["source_pdf_page_1_based"]=idx+1
            row["source_paper_doi"]="10.3390/plants14142185"
            row["source_original_pdf_sha256"]=PINNED_PDF
            row["original_trait_kind"]="LITERATURE_REVIEW_REPORTED_FLORAL_COLOR_CHANGE"
            row["direct_measurement_in_this_2025_paper"]=False
            row["change_not_proven_pollinator_information_use"]=True
            row["visual_signal_negative_status"]="NOT_SAMPLED_IN_POSITIVE_ONLY_REVIEW"
        rows.extend(taxa)
        pages.append({"page_number_1_based":idx+1,
                      "n_original_italic_column_groups":len(taxa),
                      "n_binomial_candidate_groups":sum(bool(x["binomial_candidate"]) for x in taxa),
                      "n_colour_transition_nonempty":sum(x["source_colour_transition_nonempty"] for x in taxa),
                      "unresolved_groups":[x["full_original_italic_taxon_text"]
                                          for x in taxa if not x["binomial_candidate"]][:12]})
    summary={
       "status":"SOURCE_2025_FLORAL_COLOUR_CHANGE_REVIEW_TAXON_COLUMN_EXTRACTION",
       "original_supplement_pdf_sha256":PINNED_PDF,
       "n_review_original_taxon_column_groups":len(rows),
       "n_review_binomial_candidates":sum(bool(x["binomial_candidate"]) for x in rows),
       "n_source_group_colour_description_extracted":sum(x["source_colour_transition_nonempty"] for x in rows),
       "source_taxon_pages":pages,
       "n_unique_unreconciled_binomial_strings":len(set(
           x["binomial_candidate"] for x in rows if x["binomial_candidate"])),
       "review_claims_151_species_not_assumed_equal_to_extracted_taxa":True,
       "no_species_negative_controls_in_review_source":True,
       "not_direct_measured_receptor_information_or_wind":True,
    }
    return rows,summary


def main():
    import fitz
    source=get_original_pdf()
    if hashlib.sha256(source).hexdigest()!=PINNED_PDF:
        raise ValueError("NO_GO_REVIEW_SOURCE_PDF_HASH")
    with fitz.open(stream=source,filetype="pdf") as pdf:
        if len(pdf)!=23:
            raise ValueError("NO_GO_REVIEW_ORIGINAL_PDF_23_PAGE_SCHEMA")
        rows,report=parse_document(pdf)
    if not 90<=len(rows)<=230:
        raise ValueError("NO_GO_REVIEW_TAXON_COLUMNS_UNPLAUSIBLE_EXTRACTION")
    folder=Path("stage54_151_original_colour_change_taxon_candidates")
    folder.mkdir(exist_ok=True)
    with (folder/"2025_original_review_tableS1_colour_change_taxon_candidates.csv").open(
        "w",encoding="utf8",newline="") as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    (folder/"2025_original_review_taxon_extraction_receipt.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf8")
    print("STAGE54_ORIGINAL_COLOUR_CHANGE_2025_REVIEW_TAXON_CANDIDATES",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("STAGE54_UNRESOLVED_REVIEW_SOURCE_NAMES",
          json.dumps([x["full_original_italic_taxon_text"] for x in rows
                      if not x["binomial_candidate"]][:30],ensure_ascii=False))


if __name__=="__main__":
    main()
