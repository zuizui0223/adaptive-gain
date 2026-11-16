"""Source-verified 80-species UV-pattern atlas seed from Tunes et al. 2021.

Original supplementary Table 2 PDF: DOI 10.3389/fpls.2021.618028,
CC-BY. The original study uses UV photography/spectrophotometry for UV
category and heterogeneous non-UV color pattern; literature and floral
syndromes for pollination labels. These ARE NOT observed Bombus visits.
Only source-derived categorical rows are output; no original PDF copied.
"""
from __future__ import annotations
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request

from probe_uv_supplement import URL,MAX_BYTES

PINNED_SOURCE_SHA256="d11b41a36d85d1b70c8d3d47c04f3e03e7d8f5f58ebaaa331a737e56ed4c2820"
CATEGORIES={"A","R","BE","CM","CR"}
EXPECTED_COUNTS={"A":47,"R":6,"BE":7,"CM":5,"CR":15}
SOURCE_DOI="10.3389/fpls.2021.618028"


def parse_table_pages(pdf):
    """Independent categorical table parser, accepts fitz.Document-like."""
    records=[]
    family=None
    for idx in range(1,min(len(pdf),6)): # printed Table S2 on physical PDF pages 2–6
        page=pdf[idx]
        found=page.find_tables(strategy="lines")
        for table in found.tables:
            data=table.extract()
            if not data or max(len(x) for x in data)!=7:
                continue
            for cells in data:
                if len(cells)!=7:
                    continue
                entry=[re.sub(r"\s+"," ",(x or "")).strip() for x in cells]
                fam,name,uv,pollination,reward,unit,nonuv=entry
                if fam and not name and not uv:
                    family=fam
                    continue
                if name.lower() in ("species",""):
                    continue
                if uv not in CATEGORIES:
                    raise ValueError("NO_GO_UV_CATEGORY_NOT_ONE_OF_FIVE_"+uv[:30])
                species_level=bool(re.match(r"^[A-Z][a-zA-Z-]+\s+[a-z][a-z-]+\b",name)) and not bool(
                    re.search(r"\b(sp\.|spp\.|cf\.|aff\.)",name,re.I))
                if nonuv not in ("Present","Absent"):
                    raise ValueError("NO_GO_UNKNOWN_VISIBLE_PATTERN_STATUS")
                records.append({
                    "taxon_as_published":name,
                    "source_family_name":family or "",
                    "uv_category":uv,
                    "uv_pattern_present":int(uv in ("BE","CM","CR")),
                    "uv_pattern_type":({"BE":"bullseye",
                                        "CM":"corolla_markings",
                                        "CR":"contrasting_reproductive_structures",
                                        "A":"uniform_uv_absorbing",
                                        "R":"uniform_uv_reflecting"}[uv]),
                    "non_uv_pattern_present":int(nonuv=="Present"),
                    "pollination_system_reported":pollination,
                    "floral_resource_reported":reward,
                    "attraction_unit_reported":unit,
                    "species_level_binomial_candidate":int(species_level),
                    "pollination_evidence_basis":"source_literature_or_syndrome_inference_mixed",
                    "source_doi":SOURCE_DOI
                })
    return records


def evaluate(records):
    counts=Counter(r["uv_category"] for r in records)
    n=len(records)
    if n!=80 or dict(sorted(counts.items()))!=dict(sorted(EXPECTED_COUNTS.items())):
        raise ValueError("NO_GO_NOT_SOURCE_VERIFIED_EIGHTY_UV_CATEGORIES")
    keys=[r["taxon_as_published"] for r in records]
    if len(set(keys))!=len(keys):
        raise ValueError("NO_GO_SOURCE_PDF_DUPLICATED_SPECIES_ROWS")
    return {
        "status":"ORIGINAL_TUNES_2021_80_SPECIES_UV_CATEGORY_REGISTRY",
        "source_doi":SOURCE_DOI,
        "source_uv_categories":dict(sorted(counts.items())),
        "n_original_taxon_rows":n,
        "n_patterned_author_categories":sum(r["uv_pattern_present"] for r in records),
        "n_uniform_A_R_author_categories":sum(1-r["uv_pattern_present"] for r in records),
        "n_species_binomial_candidates":sum(r["species_level_binomial_candidate"] for r in records),
        "n_genus_or_uncertain_name_rows":sum(1-r["species_level_binomial_candidate"] for r in records),
        "n_source_visible_non_uv_pattern_present":sum(r["non_uv_pattern_present"] for r in records),
        "source_original_UV_phenotype_measured":True,
        "source_pollination_labels_NOT_direct_Bombus_observations":True,
        "no_new_pollinator_trait_correlation_test":True,
        "no_species_level_NHM_or_GBIF_range_overlap_yet":True,
    }


def main():
    import fitz
    req=urllib.request.Request(URL,headers={"User-Agent":
        "adaptive-gain-stage45-original-UV-80-species-source-reader/2026",
        "Accept":"application/pdf"})
    with urllib.request.urlopen(req,timeout=60) as stream:
        original=stream.read(MAX_BYTES+1)
    if not original.startswith(b"%PDF-") or len(original)>MAX_BYTES or (
        hashlib.sha256(original).hexdigest()!=PINNED_SOURCE_SHA256):
        raise ValueError("NO_GO_UNAUTHENTICATED_AUTHOR_SUPPLEMENT_PDF")
    with fitz.open(stream=original,filetype="pdf") as pdf:
        records=parse_table_pages(pdf)
    result=evaluate(records)
    result["original_source_pdf_sha256"]=PINNED_SOURCE_SHA256
    output=Path("stage45_verified_uv_species")
    output.mkdir(exist_ok=True)
    with (output/"tunescamargoguimaraes2021_uv_80_taxa.csv").open(
        "w",encoding="utf8",newline="") as handle:
        w=csv.DictWriter(handle,fieldnames=list(records[0]))
        w.writeheader()
        w.writerows(records)
    (output/"uv_80_species_source_receipt.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("ORIGINAL_UV_80_SPECIES_DATASET",json.dumps(result,sort_keys=True))
    print("UV_PATTERNED_TAXON_NAMES",json.dumps(
       [r["taxon_as_published"] for r in records if r["uv_pattern_present"]],
       ensure_ascii=False))
    print("NO_NEW_MACRO_FIT_OR_BOMBUS_SUITABILITY")

if __name__=="__main__":
    main()
