#!/usr/bin/env python3
"""Exact original WFO floral text × Farré-Armengol 2020 VOC-305 overlap.

Source-only cross-study evidence feasibility and diagnostic, NOT a test of
true fragrance absence or a comparable total-VOC EMISSION-RATE effect. Original
VOC columns count compounds with reported positive presence; unmentioned
botanical prose is NOT a flower negative and absence of measured compounds
in a source workbook does not mean scentless.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,statistics,zipfile
from pathlib import Path
from collections import Counter,defaultdict

WFO_SOURCE_SHA="eb32786c6464a6edecd7ff0d12e61762cdb107f3082124066aadcc03292dd88e"
VOC_SOURCE_SHA="9522821741ad3054345235f6a3711a709144cc86cc13c0cc6e06cd278b2f6552"
WFO_MEMBER="stage93_derived/stage93_original_WFO_species_fragrance_lexical_states_NOT_VOC.csv"
VOC_MEMBER="original_VOC305_accepted_source_and_visual817_evidence_bridge.csv"
WFO_RECEIPT="stage93_derived/stage93_WFO_original_flora_source_scent_coverage.json"

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def get(path,expected,member):
    if sha(path)!=expected:raise ValueError("STAGE96_VOC_WFO_SOURCE_ARTIFACT_SHA_CHANGED")
    with zipfile.ZipFile(path) as z:
        if member not in z.namelist():raise ValueError("STAGE96_VOC_WFO_REQUIRED_MEMBER_MISSING")
        data=list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig"))))
    return data

def overlap(wfo,voc):
    if len(wfo)!=27899 or len(voc)!=305:
        raise ValueError("STAGE96_VOC_WFO_ORIGINAL_SPECIES_UNIVERSE_CHANGED")
    flora={}
    for r in wfo:
        k=str(r.get("accepted_species") or "").casefold().strip()
        if not k or k in flora:raise ValueError("STAGE96_WFO_DUPLICATE_NATIVE_ACCEPTED_SPECIES")
        flora[k]=r
    rows=[]
    for source in voc:
        if source.get("GBIF_strict_taxonomy_status")!="EXACT_CONFIDENT_SPECIES_MAPPED":
            continue
        original=str(source.get("source_species_canonical_binomial_if_valid") or "").casefold().strip()
        if original not in flora:continue
        w=flora[original]
        state=w["source_flora_lexical_fragrance_state"]
        if state not in ("positive_candidate","explicit_negative_candidate","unmentioned_or_uncertain","conflicting_prose"):
            raise ValueError("STAGE96_WFO_UNRECOGNIZED_SCENT_SOURCE_REPORT")
        try:positive=int(source["source_VOC_positive_presence_columns_in_original_full_bouquet"])
        except (TypeError,ValueError):raise ValueError("STAGE96_ORIGINAL_VOC_SOURCE_COMPOUND_COUNT_UNRECOVERABLE")
        if positive<0:raise ValueError("STAGE96_NEGATIVE_ORIGINAL_VOC_COMPOUND_COUNT")
        rows.append({"accepted_species_exact_literal":original,
          "WFO_flower_fragrance_text_lexical_state":state,
          "WFO_original_flora_provider":w["original_flora_provider"],
          "WFO_original_description_characters_median":w["botanical_description_length_characters_median"],
          "original_VOC_author_source_article":source["source_article_abbrev"],
          "original_VOC_positive_presence_compound_columns_not_emission_flux":positive,
          "source_GBIF_strict_accepted_verified":True,
          "original_scent_report_not_verified_same_population_with_VOC":True,
          "original_VOC_compound_detected_not_human_fragrance_perception":True})
    if len({r["accepted_species_exact_literal"] for r in rows})!=len(rows):
        raise ValueError("STAGE96_VOC_DUPLICATE_MATCHED_SPECIES")
    return rows

def describe(rows):
    groups=defaultdict(list)
    for r in rows:groups[r["original_VOC_author_source_article"]].append(r)
    states=Counter(r["WFO_flower_fragrance_text_lexical_state"] for r in rows)
    med={}
    for st in ("positive_candidate","explicit_negative_candidate","unmentioned_or_uncertain","conflicting_prose"):
        x=[int(r["original_VOC_positive_presence_compound_columns_not_emission_flux"])
           for r in rows if r["WFO_flower_fragrance_text_lexical_state"]==st]
        med[st]=statistics.median(x) if x else None
    within=[]
    for study,data in sorted(groups.items()):
        a=[int(r["original_VOC_positive_presence_compound_columns_not_emission_flux"])
            for r in data if r["WFO_flower_fragrance_text_lexical_state"]=="positive_candidate"]
        b=[int(r["original_VOC_positive_presence_compound_columns_not_emission_flux"])
            for r in data if r["WFO_flower_fragrance_text_lexical_state"]=="unmentioned_or_uncertain"]
        if a and b:
            within.append({"source_article":study,
              "source_positive_flower_scent_n":len(a),
              "source_unmentioned_or_uncertain_flower_scent_n":len(b),
              "median_difference_compound_columns_positive_minus_unmentioned":
                   statistics.median(a)-statistics.median(b)})
    n_neg=states["explicit_negative_candidate"]
    return {"original_source_taxa_exact_matched":len(rows),
       "source_WFO_lexical_state_counts":dict(states),
       "original_distinct_VOC_source_article_text_keys":len(groups),
       "source_median_detected_compound_columns_NOT_emission_flux":med,
       "within_original_source_article_positive_vs_unmentioned_both_groups":len(within),
       "within_source_article_positive_minus_unmentioned_difference_positive":sum(
           v["median_difference_compound_columns_positive_minus_unmentioned"]>0 for v in within),
       "within_source_article_positive_minus_unmentioned_difference_negative":sum(
           v["median_difference_compound_columns_positive_minus_unmentioned"]<0 for v in within),
       "within_study_source_only_diagnostics":within,
       "explicit_verified_scentless_source_matches_missing":n_neg==0,
       "fragrance_absence_proxy_validation_identifiable":False,
       "no_same_site_temporal_or_direct_fitness_evidence":True,
       "cannot_compare_orig_emission_units_from_this_presence_workbook":True,
       "no_statistical_phenotypic_source_negative_vs_positive_contrast":True}

def run(wfo_zip,voc_zip,outdir):
    wfo=get(wfo_zip,WFO_SOURCE_SHA,WFO_MEMBER)
    voc=get(voc_zip,VOC_SOURCE_SHA,VOC_MEMBER)
    with zipfile.ZipFile(wfo_zip) as z:receipt=json.loads(z.read(WFO_RECEIPT))
    if receipt["scent_lexical_species_states"]!={"positive_candidate":420,
       "explicit_negative_candidate":105,"unmentioned_or_uncertain":27374}:
        raise ValueError("STAGE96_WFO_ORIGINAL_TEXT_STATE_MARGINS_DRIFTED")
    rows=overlap(wfo,voc)
    summary=describe(rows)
    source={"schema":"stage96V_WFO_lexical_flower_fragrance_x_original_VOC_305_source_bound_overlap",
        "source_SHA256":{"original_WFO_202606":WFO_SOURCE_SHA,"original_2020_VOC305":VOC_SOURCE_SHA},
        "original_WFO_native_species":len(wfo),"original_author_VOC_species":len(voc),
        "no_abstract_only_species_count":True,
        **summary}
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage96V_original_WFO_flora_VOC305_exact_matched_source_species.csv").open("w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    (outdir/"stage96V_original_flora_scent_VOC305_proxy_feasibility.json").write_text(
        json.dumps(source,indent=2,sort_keys=True)+"\n")
    print("STAGE96V_REAL_ORIGINAL_WFO_X_VOC305",json.dumps({
      "exact_species":source["original_source_taxa_exact_matched"],
      "lexical_states":source["source_WFO_lexical_state_counts"],
      "original_within_study_compound_presence_diagnostics":
           source["within_original_source_article_positive_vs_unmentioned_both_groups"],
      "valid_absence_proxy_test":source["fragrance_absence_proxy_validation_identifiable"]},
      sort_keys=True),flush=True)
    return source

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--wfo-species-zip",type=Path,required=True)
    p.add_argument("--voc305-species-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.wfo_species_zip,a.voc305_species_zip,a.outdir)
