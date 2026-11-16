"""Stage49: original-paper species ledger with DISTINCT visual evidence types.

Rebuild from:
 (A) Tunes et al 2021 original UV photographs, 80 sampled Brazilian
     savanna taxa, Table S2 5-type UV pattern categories;
 (B) Koski/MacQueen/Ashman 2020 original PDF Supplemental Table S1,
     45 continent-by-binomial records and 1,238 herbarium specimens.
Treat article-reported 42 vs literal source 41 unique names as unresolved.
 (C) Two Koski Potentilleae datasets with 177 source taxa each share
     underlying source sample: source discovery only pending downloadable
     per-species scores. No fabrication of 177 named taxa.

Never infer spatial UV guides from UVP/year slope, or infer Bombus
visitation from a plant species name.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import csv
import hashlib
import json
from pathlib import Path
import urllib.request
import sys

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_visual_macro_stage45"))
from join_uv_with_global_traits import retrieve_original_uv,canonical_candidate
from extract_current_biology_table_s1 import (
    SOURCE_DOI as CB_DOI,SOURCE_URL as CB_URL,
    ORIGINAL_PDF_SHA256,MAX_BYTES,parse_table_s1_text,evaluate
)

SOURCE_A_DOI="10.3389/fpls.2021.618028"
SRC_A_N=80
SRC_B_PUBLISHED_N=42

def _canonical(original):
    # Never resolve aliases automatically; purely lexical matching.
    return canonical_candidate(original) or ""

def assemble(uv_original,cb_continent_rows):
    if len(uv_original)!=SRC_A_N:
        raise ValueError("NO_GO_ORIGINAL_UV_80_SOURCE_GRANULARITY")
    report=evaluate(cb_continent_rows)
    by_name=defaultdict(list)
    for r in cb_continent_rows:
        by_name[r["taxon_binomial_as_published"]].append(r)
    out=[]
    for r in uv_original:
        name=r["taxon_as_published"]
        if not isinstance(name,str) or not name.strip():
            raise ValueError("NO_GO_ORIGINAL_UV_TAXON_NAME_EMPTY")
        out.append({
           "published_taxon_string":name,
           "canonical_binomial_candidate_unreconciled":_canonical(name),
           "original_study_doi":SOURCE_A_DOI,
           "study_measurement_group":"Brazilian Cerrado study; per-species site assignment unavailable",
           "original_source_taxon_unit":"one_table_S2_taxon",
           "UV_spatial_guide_pattern_source_status":(
               "SOURCE_MEASURED_PATTERNED" if r["uv_pattern_present"] else
               "SOURCE_MEASURED_UNIFORM"),
           "UV_pattern_source_subtype":r["uv_pattern_type"],
           "UVP_temporal_slope_original_source":"",
           "UVP_temporal_slope_available":0,
           "published_sample_count":"",
           "source_pollination_status":"original_paper_syndrome_or_literature_not_observed_Bombus",
           "species_source_name_validation_status":(
               "LEXICAL_BINOMIAL_CANDIDATE_ONLY" if _canonical(name) else
               "NOT_VERIFIED_SPECIES_LEVEL_BINOMIAL"),
           "source_UV_modality":"direct_UV_photography_or_spectrophotometry",
           "model_Bombus_geographic_link_status":"NOT_YET_MATCHED_STUDY_SPECIES_TO_HEX",
        })
    for name,rs in sorted(by_name.items()):
        if len({x["continent"] for x in rs})!=len(rs):
            raise ValueError("NO_GO_DUPLICATE_SAME_CONTINENT_IN_CB_ORIGINAL")
        if len({x["floral_anther_position_code"] for x in rs})>1:
            raise ValueError("NO_GO_FLORAL_ANATOMY_CONFLICT_ACROSS_CONTINENTS")
        out.append({
           "published_taxon_string":name,
           "canonical_binomial_candidate_unreconciled":_canonical(name),
           "original_study_doi":CB_DOI,
           "study_measurement_group":"|".join(sorted({x["continent"] for x in rs})),
           "original_source_taxon_unit":"one_taxon_aggregated_from_continent_rows",
           "UV_spatial_guide_pattern_source_status":"NOT_CLASSIFIED_BY_TABLE_S1",
           "UV_pattern_source_subtype":"",
           "UVP_temporal_slope_original_source":"continent_specific_see_45_row_companion_file",
           "UVP_temporal_slope_available":1,
           "published_sample_count":sum(x["original_herbarium_samples"] for x in rs),
           "source_pollination_status":"NOT_DIRECTLY_MEASURED_IN_TABLE_S1",
           "species_source_name_validation_status":"LEXICAL_BINOMIAL_CANDIDATE_ONLY",
           "source_UV_modality":"UV_photo_measured_absorptive_proportion_over_time",
           "model_Bombus_geographic_link_status":"NOT_YET_MATCHED_STUDY_SPECIES_TO_HEX",
        })
    observed=Counter(x["original_study_doi"] for x in out)
    if observed[SOURCE_A_DOI]!=80 or observed[CB_DOI]!=len(by_name):
        raise ValueError("NO_GO_PUBLICATION_SPECIES_FRAME_LOST_OR_DUPLICATED")
    a={x["canonical_binomial_candidate_unreconciled"].casefold()
       for x in out if x["original_study_doi"]==SOURCE_A_DOI
          and x["canonical_binomial_candidate_unreconciled"]}
    b={x["canonical_binomial_candidate_unreconciled"].casefold()
       for x in out if x["original_study_doi"]==CB_DOI
          and x["canonical_binomial_candidate_unreconciled"]}
    return out,{
       "status":"TWO_AUTHENTIC_LITERATURE_VISUAL_SPECIES_FRAMES_WITH_DISTINCT_PHENOTYPE_MODALITIES",
       "published_source_rows_by_study":dict(sorted(observed.items())),
       "UV_photo_2021_original_80_rows":80,
       "original_2020_continent_taxon_rows":report["n_source_continent_by_taxon_rows"],
       "original_2020_unique_literal_binomial_names":report["n_unique_literal_published_binomials"],
       "article_reported_2020_number_of_species":SRC_B_PUBLISHED_N,
       "original_2020_herbarium_specimens":report["source_herbarium_samples_sum"],
       "reported_vs_literal_2020_n_unresolved":report["literal_source_table_species_count_may_differ_from_paper_n"],
       "original_2021_UV_patterned_taxon_rows":sum(
          int(r["uv_pattern_present"]) for r in uv_original),
       "original_2020_spatial_UV_pattern_labels_NOT_available":True,
       "literal_cross_paper_binomial_string_overlap_n":len(a&b),
       "combined_distinct_literal_source_binomial_candidates_n":len(a|b),
       "unresolved_generic_or_uncertain_2021_source_taxon_rows":sum(
          not _canonical(r["taxon_as_published"]) for r in uv_original),
       "distinct_independent_observational_2016_and_2020_Potentilleae_177_cohorts":False,
       "no_inference_that_2020_UVP_slope_means_guide_presence":True,
       "no_measured_Bombus_overlap_or_pollination_fitness":True,
    }


def fetch_original_cb_table():
    import fitz
    req=urllib.request.Request(CB_URL,headers={
        "User-Agent":"adaptive-gain-stage49-original-2020-UV-studies/2026",
        "Accept":"application/pdf,*/*",
    })
    with urllib.request.urlopen(req,timeout=50) as res:
        blob=res.read(MAX_BYTES+1)
    if len(blob)>MAX_BYTES or hashlib.sha256(blob).hexdigest()!=ORIGINAL_PDF_SHA256:
        raise ValueError("NO_GO_KOSKI_2020_PDF_DIGEST_CHANGED")
    with fitz.open(stream=blob,filetype="pdf") as pdf:
        if len(pdf)!=15:
            raise ValueError("NO_GO_ORIGINAL_CB_PDF_PAGE_COUNT")
        return parse_table_s1_text({i:pdf[i].get_text("text") for i in (13,14)})

def main():
    uv,uvreceipt=retrieve_original_uv()
    cb=fetch_original_cb_table()
    rows,receipt=assemble(uv,cb)
    receipt["author_UV_PDF_SHA256"]="d11b41a36d85d1b70c8d3d47c04f3e03e7d8f5f58ebaaa331a737e56ed4c2820"
    receipt["Current_Biology_original_PDF_SHA256"]=ORIGINAL_PDF_SHA256
    folder=Path("stage49_literature_species_registry")
    folder.mkdir(exist_ok=True)
    with (folder/"combined_original_papers_visual_trait_species_registry.csv").open(
        "w",encoding="utf8",newline="") as h:
        writer=csv.DictWriter(h,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (folder/"source_distinct_visual_modalities_receipt.json").write_text(
       json.dumps(receipt,indent=2,ensure_ascii=False,sort_keys=True)+"\n",
       encoding="utf8")
    print("STAGE49_SOURCE_VERIFIED_TWO_PAPER_SPECIES_REGISTRY",
          json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    print("NOT_A_COMPLETE_177_ROSACEAE_REGISTRY_YET")
    print("NO_CLAIM_OF_NEW_UV_BOMBUS_MACRO_ASSOCIATION")

if __name__=="__main__":
    main()
