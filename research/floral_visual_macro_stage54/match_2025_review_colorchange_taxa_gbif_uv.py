"""Stage54: 2025 literature-reviewed floral colour-change source taxa × UV262.

Original positive-only 2025 review Table S1 source PDF (pinned SHA):
doi:10.3390/plants14142185. The audited font-column extraction recovers
136 provisional source taxon groups, 128 provisional binomial strings.
This is NOT the whole published 151-plant roster. Strict GBIF accepted
speciesName reconciliation identifies confident cases; unresolved source
rows stay unknown, never biological no-change species.

Review text says an original colour transition was REPORTED IN LITERATURE,
but data are NOT all original measured spectra or reward information.
No bee perceptual colour-change trait or wind interaction inferred.
"""
from __future__ import annotations
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import argparse,csv,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage49"))
from match_literature_visual_taxa_gbif import lookup

PDF_SHA="0c2ba82cd6eb554942fc3ac93014f7ecc9834686f695cf628f2873a2be213039"
SOURCE_REVIEW_GROUPS=136
SOURCE_BINOMIAL_CANDIDATES=128
BASE_UV262=262
REVIEW_DOI="10.3390/plants14142185"


def validate(source,uv262):
    if len(source)!=SOURCE_REVIEW_GROUPS:
        raise ValueError("NO_GO_SOURCE_REVIEW_136_COLS_CHANGED")
    if sum(bool(r.get("binomial_candidate")) for r in source)!=SOURCE_BINOMIAL_CANDIDATES:
        raise ValueError("NO_GO_SOURCE_REVIEW_128_BINOMIAL_CANDIDATE_CHANGED")
    if any(r.get("source_original_pdf_sha256")!=PDF_SHA for r in source):
        raise ValueError("NO_GO_SOURCE_REVIEW_ORIGINAL_PDF_SHA_MISMATCH")
    if any(r.get("source_paper_doi")!=REVIEW_DOI for r in source):
        raise ValueError("NO_GO_SOURCE_REVIEW_STUDY_DOI_MISMATCH")
    if len(uv262)!=BASE_UV262:
        raise ValueError("NO_GO_ACCEPTED_UV_SOURCE_262_DENOMINATOR")
    names={r.get("gbif_accepted_species_key") for r in uv262}
    if len(names)!=BASE_UV262 or not all(x and x.isdigit() for x in names):
        raise ValueError("NO_GO_UV262_ACCEPTED_KEYS_NOT_UNIQUE")
    return {r["gbif_accepted_species_key"]:r for r in uv262}


def merge(review,gbif,uv):
    rows=[]
    for r in review:
        name=r["binomial_candidate"]
        match=gbif.get(name,{"taxonomy_status":"SOURCE_REVIEW_NAME_NOT_RESOLVED"})
        key=match.get("gbif_accepted_usage_key")
        other=uv.get(str(key)) if isinstance(key,int) else None
        rows.append({
          "source_original_review_column_x":r["column_x"],
          "source_original_pdf_page":r["source_pdf_page_1_based"],
          "review_source_italic_taxon_text":r["full_original_italic_taxon_text"],
          "review_source_binomial_candidate":name,
          "review_source_colour_transition_as_printed":r["original_source_colour_transition_text"],
          "gbif_exact_species_match_status":match["taxonomy_status"],
          "gbif_accepted_key_or_unresolved":key or "",
          "review_original_trait_report":"COLOUR_CHANGE_REPORTED_IN_LITERATURE",
          "source_2025_review_is_not_all_original_direct_measurement":True,
          "bee_perceptible_colour_change_status":"NOT_MEASURED_FROM_REVIEW_TEXT",
          "butterfly_perceptible_change_status":"NOT_MEASURED_FROM_REVIEW_TEXT",
          "nectar_reward_information_status":"NOT_MEASURED_FROM_REVIEW_TEXT",
          "UV_direct_study_crossmatch_status":(
              "HAS_INDEPENDENT_UV262_STUDY" if other is not None else
              "NOT_IN_UV262_ACCEPTED_SOURCE_OR_UNMATCHED"),
          "UV_source_measured_pattern_or_missing":(
              other["source_measured_UV_spatial_pattern_or_missing"] if other else ""),
          "source_original_review_doi":REVIEW_DOI,
          "review_negative_species_comparator":"NOT_SAMPLED_IN_POSITIVE_ONLY_REVIEW",
          "no_wind_or_Bombus_exposure_study_join":True,
        })
    mapped=[x for x in rows if x["gbif_exact_species_match_status"]=="EXACT_CONFIDENT_SPECIES_MAPPED"]
    accepted={x["gbif_accepted_key_or_unresolved"] for x in mapped}
    overlap={x["gbif_accepted_key_or_unresolved"] for x in mapped
             if x["UV_direct_study_crossmatch_status"]=="HAS_INDEPENDENT_UV262_STUDY"}
    return rows,{
       "status":"SOURCE_2025_REVIEW_136_PARTIAL_COLOUR_CHANGE_TAXA_GBIF_AND_UV262",
       "n_recovered_original_pdf_taxon_column_groups":len(rows),
       "source_paper_reports_151_colour_change_species":True,
       "n_verified_source_binomial_candidates":sum(bool(r["review_source_binomial_candidate"]) for r in rows),
       "n_original_review_high_confidence_GBIF_mapped_columns":len(mapped),
       "n_distinct_GBIF_accepted_reviewed_colour_changers":len(accepted),
       "n_accepted_review_taxa_also_in_original_UV262":len(overlap),
       "n_new_accepted_review_taxa_not_in_UV262":len(accepted-overlap),
       "n_total_distinct_UV262_and_2025_review_accepted_species":len(uv)+len(accepted-overlap),
       "n_review_taxon_column_groups_unresolved":len(rows)-len(mapped),
       "positive_only_secondary_literature_source_no_measured_negative":True,
       "source_2025_151_claim_not_falsely_reproduced_by_136_column_extraction":True,
       "no_functional_Bombus_sense_or_wind_model_estimated":True
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--review-source",required=True)
    p.add_argument("--UV262-source",required=True)
    args=p.parse_args()
    with Path(args.review_source).open(encoding="utf8",newline="") as f:
        review=list(csv.DictReader(f))
    with Path(args.UV262_source).open(encoding="utf8",newline="") as f:
        uvrows=list(csv.DictReader(f))
    uv=validate(review,uvrows)
    names=sorted({x["binomial_candidate"] for x in review if x["binomial_candidate"]})
    with ThreadPoolExecutor(max_workers=4) as pool:
        response=list(pool.map(lookup,names))
    rows,summary=merge(review,dict(zip(names,response)),uv)
    output=Path("stage54_151_review_GBIF_UV262_crosswalk")
    output.mkdir(exist_ok=True)
    with (output/"2025_review_136_taxon_columns_GBIF_species_UV262_overlap.csv").open(
        "w",encoding="utf8",newline="") as h:
        writer=csv.DictWriter(h,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    (output/"source_2025_review_GBIF_species_UV262_receipt.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf8")
    print("STAGE54_ORIGINAL_2025_REVIEW_COLOUR_CHANGE_ACCEPTED_UV_OVERLAP",
          json.dumps(summary,ensure_ascii=False,sort_keys=True))
    if summary["n_original_review_high_confidence_GBIF_mapped_columns"]<80:
        raise SystemExit("NO_GO_TOO_FEW_CONFIDENT_REVIEW_SOURCE_GBIF_MATCHES")

if __name__=="__main__":
    main()
