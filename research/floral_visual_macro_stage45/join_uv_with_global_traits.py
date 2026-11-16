"""Stage45 exact taxon join: 80 measured UV source rows × official 59,369
NHM original botanical trait CSV. All source bytes are fetched in-memory and
verified at pinned immutable Git/PDF digests. Species names are candidate-only
until independent WFO/GBIF synonym resolution is performed.
"""
from __future__ import annotations
from collections import defaultdict,Counter
import csv
import hashlib
import io
import json
import re
from pathlib import Path
import urllib.request

from build_visual_trait_registry import _get_source_bytes,summarize_and_extract
from extract_original_uv_80 import (
  parse_table_pages,evaluate,URL,MAX_BYTES,PINNED_SOURCE_SHA256
)

BINOMIAL=re.compile(r"^([A-Z][A-Za-z-]+)\s+([a-z][a-z-]+)\b")
UNCERTAIN=re.compile(r"\b(sp\.|spp\.|cf\.|aff\.)",re.I)
SOURCE_80_DOI="10.3389/fpls.2021.618028"
SOURCE_59K_DOI="10.5519/p3dm31kc"


def canonical_candidate(name):
    if not isinstance(name,str) or UNCERTAIN.search(name):
        return None
    match=BINOMIAL.match(name.strip())
    return " ".join(match.groups()) if match else None


def join_sources(uv_rows,plant_rows):
    byname=defaultdict(list)
    for r in plant_rows:
        accepted=canonical_candidate(r["taxon"])
        if accepted:
            byname[accepted.casefold()].append(r)
    out=[]
    flags=Counter()
    for source in uv_rows:
        name=canonical_candidate(source["taxon_as_published"])
        matched=byname.get(name.casefold(),[]) if name else []
        if not name:
            status="NO_CANONICAL_BINOMIAL"
        elif not matched:
            status="NO_EXACT_TAXON_STRING_MATCH"
        elif len(matched)>1:
            status="AMBIGUOUS_EXACT_TAXON_STRING"
        else:
            status="EXACT_NAME_STRING_ONLY_NOT_TAXONOMIC_RECONCILIATION"
        row=matched[0] if len(matched)==1 else None
        out.append({
          "published_taxon":source["taxon_as_published"],
          "canonical_binomial_candidate":name or "",
          "uv_category_source_pdf":source["uv_category"],
          "uv_pattern_present_source_pdf":source["uv_pattern_present"],
          "nonuv_visible_pattern_present":source["non_uv_pattern_present"],
          "pollination_syndrome_source_pdf":source["pollination_system_reported"],
          "nhm_join_status":status,
          "nhm_taxon":row["taxon"] if row else "",
          "nhm_wfo_id_unverified":row["wfo"] if row else "",
          "nhm_colour_present":row["floral_colour_reported"] if row else "",
          "nhm_reported_flower_colour":row["flower_colour"] if row else "",
          "nhm_reported_corolla_colour":row["corolla_colour"] if row else "",
          "nhm_reported_flower_symmetry":row["flower_symmetry"] if row else "",
          "uv_source_doi":SOURCE_80_DOI,
          "nhm_source_doi":SOURCE_59K_DOI,
          "gbif_accepted_taxon_key":"",
          "gbif_taxonomic_acceptance":"not_checked",
          "species_occurrence_distribution":"not_estimated",
          "bombus_overlap_or_habitat_suitability":"not_estimated",
        })
        flags[status]+=1
    return out,dict(sorted(flags.items()))


def retrieve_original_uv():
    import fitz
    req=urllib.request.Request(URL,headers={
       "User-Agent":"adaptive-gain-stage45-UV-cross-DB-seed/2026",
       "Accept":"application/pdf"
    })
    with urllib.request.urlopen(req,timeout=60) as res:
        blob=res.read(MAX_BYTES+1)
    if len(blob)>MAX_BYTES or hashlib.sha256(blob).hexdigest()!=PINNED_SOURCE_SHA256:
        raise ValueError("NO_GO_TUNES_2021_ORIGINAL_PDF_DIGEST")
    with fitz.open(stream=blob,filetype="pdf") as pdf:
        rows=parse_table_pages(pdf)
    audit=evaluate(rows)
    if audit["n_original_taxon_rows"]!=80 or not audit["source_TableS2_vs_article_prose_R_CM_discrepancy"]:
        raise ValueError("NO_GO_80_UV_SOURCE_TABLE_NOT_VALIDATED")
    return rows,audit


def main():
    uv,uv_receipt=retrieve_original_uv()
    original,official=_get_source_bytes()
    plants,_,nhm_receipt=summarize_and_extract(original)
    out,counts=join_sources(uv,plants)
    if len(out)!=80:
        raise ValueError("NO_GO_JOIN_DROPPED_OR_DUPLICATED_UV_TAXA")
    folder=Path("stage45_crossdb_species")
    folder.mkdir(exist_ok=True)
    with (folder/"source_80_UV_taxa_x_NHM_59369_exact_name_join.csv").open(
        "w",encoding="utf8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    result={
      "status":"ORIGINAL_SOURCE_80_UV_TAXA_VS_59369_NHM_EXACT_NAME_JOIN",
      "source_uv_pdf_sha256":PINNED_SOURCE_SHA256,
      "source_nhm_git_blob":official["git_blob_sha1_verified"],
      "nhm_original_source_rows":len(plants),
      "uv_source_rows":len(uv),
      "uv_category_counts_TableS2":uv_receipt["source_uv_categories"],
      "uv_article_vs_table_discrepancy_preserved":uv_receipt["source_TableS2_vs_article_prose_R_CM_discrepancy"],
      "join_status_counts":counts,
      "taxon_name_match_does_not_resolve_synonyms":True,
      "no_false_uv_absence_from_NHM_colour_coverage":True,
      "no_gbif_occurrences_or_Bombus_SDM_have_been_estimated":True,
      "original_upstream_CSV_and_PDF_not_redistributed":True
    }
    (folder/"exact_name_join_provenance.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",
        encoding="utf8")
    print("STAGE45_UV_NHM_ORIGINAL_EXACT_NAME_JOIN",json.dumps(result,sort_keys=True))
    print("STAGE45_FIRST_20_UV_TAXON_JOIN_STATUSES",json.dumps([
       {"name":r["canonical_binomial_candidate"],"status":r["nhm_join_status"]}
       for r in out[:20]
    ],ensure_ascii=False))


if __name__=="__main__":
    main()
