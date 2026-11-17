"""Stage65: original iNaturalist flower-ANNOTATED fresh-photo acquisition pilot.

Official iNaturalist API observation search supports Flowers/Fruits term_id=12,
Flowers term_value_id=13 (https://help.inaturalist.org/ ... search URL guide).
This means a community source observation was annotated as flowering,
NOT that its selected photo necessarily shows a reviewable OPEN corolla.

Scope: four ORIGINAL Stage60 VOC x FCP source selected taxa, no
selection based on the image outcome. Compare source metadata opportunity
to the earlier original *unfiltered* Stage64 audit of 17 separate iNat photo
IDs (same provider, not independent biological sources/random samples).
Only official original CC-licensed photo metadata; pixel/visible morphology
will be checked separately, never inferred from phenology.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,urllib.error,urllib.parse,urllib.request
from pathlib import Path
from collections import Counter
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_routeability_stage64"))
from probe_original_iNat_flower_photo_source import (
    FCP_TARGETS,API,original_url,source_sample,validate_source_candidates,MAX_BYTES)

ANNOTATION_ID=12
FLOWERS_VALUE_ID=13
MAX_BYTES_ANNO=MAX_BYTES

def annotated_url(taxon_id):
    # The only difference from Stage64 original source query is the
    # documented iNaturalist flowering annotation filter.
    return original_url(taxon_id)+"&term_id=12&term_value_id=13"

def get_annotated_source(taxon_id,opener=urllib.request.urlopen):
    url=annotated_url(taxon_id)
    if not url.startswith(API+"?") or "term_id=12&term_value_id=13" not in url:
        raise ValueError("NO_GO_NOT_ORIGINAL_INAT_FLOWER_ANNOTATION_QUERY")
    req=urllib.request.Request(url,headers={
        "Accept":"application/json",
        "User-Agent":"adaptive-gain-stage65-original-iNat-annotated-flowering-CC-source/2026"})
    with opener(req,timeout=55) as res:
        if urllib.parse.urlparse(res.geturl()).hostname!="api.inaturalist.org":
            raise ValueError("NO_GO_INAT_ANNOTATION_API_EXTERNAL_REDIRECT")
        raw=res.read(MAX_BYTES_ANNO+1)
    if len(raw)>MAX_BYTES_ANNO:
        raise ValueError("NO_GO_SOURCE_ANNOTATED_I_NAT_JSON_TOO_LARGE")
    return json.loads(raw),hashlib.sha256(raw).hexdigest()

def compare_prior(current,prior):
    prior_ids={r.get("fresh_2026_original_iNaturalist_photo_id","") for r in prior}
    current_ids={r.get("fresh_2026_original_iNaturalist_photo_id","") for r in current}
    if "" in current_ids:
        raise ValueError("NO_GO_SOURCE_FLOWER_ANNOTATED_UNKNOWN_PHOTO_ID")
    return {
        "n_new_flower_annotated_CC_photo_metadata":len(current_ids),
        "n_old_unfiltered_CC_source_photo_metadata":len(prior_ids),
        "n_selected_photo_IDs_in_both_queries":len(current_ids&prior_ids),
        "n_new_annotated_photo_IDs_not_in_old_filtered_source_list":
            len(current_ids-prior_ids),
        "different_query_populations_cannot_infer_phenology_causal_gain":True,
        "flower_annotation_not_equivalent_to_photo_open_corolla":True,
        "both_pilots_same_iNaturalist_source_not_independent_provider":True,
    }

def source_csv(path):
    with Path(path).open(encoding="utf8",newline="") as h:
        return list(csv.DictReader(h))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--original-stage60-voc-fcp80",required=True)
    parser.add_argument("--original-stage64-unfiltered-CC-metadata",required=True)
    args=parser.parse_args()
    validate_source_candidates(source_csv(args.original_stage60_voc_fcp80))
    prior=source_csv(args.original_stage64_unfiltered_CC_metadata)
    source_name_pairs={(r["source_original_iNat_species"],r["fresh_2026_original_iNaturalist_photo_id"])
                       for r in prior}
    if len(prior)!=17 or len(source_name_pairs)!=17:
        raise ValueError("NO_GO_STAGE64_ORIGINAL_PREVIOUS_17_SOURCE_ID_REGISTRY")
    allrows=[]
    receipt={}
    for name,tid,n,tier in FCP_TARGETS:
        try:
            data,sha=get_annotated_source(tid)
            selected,meta=source_sample(data,tid,name,tier)
            for row in selected:
                row["source_annotation_plant_phenology_flowers_server_filtered"]=True
                row["actual_individual_photo_visible_open_flower_status"]="NOT_YET_VERIFIED_FROM_PIXELS"
                row["source_plant_phenology_not_per_photo_flowering_verification"]=True
                row["old_unfiltered_source_ID_overlap"]=(
                    (row["source_original_iNat_species"],str(row["fresh_2026_original_iNaturalist_photo_id"]))
                    in source_name_pairs)
            allrows.extend(selected)
            receipt[name]={"status":"ORIGINAL_INAT_FLOWER_ANNOTATED_SOURCE_METADATA_AVAILABLE",
                           "original_source_response_SHA256":sha,
                           "official_flower_annotated_query_url":annotated_url(tid),**meta}
        except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
                TimeoutError,json.JSONDecodeError) as e:
            receipt[name]={"status":"ANNOTATED_FLOWER_SOURCE_QUERY_UNAVAILABLE_NOT_NO_FLOWERS",
                           "error_type":type(e).__name__,
                           "error_summary":str(e)[:160],
                           "official_flower_annotated_query_url":annotated_url(tid)}
    out=Path("stage65_original_iNat_flower_annotated_photo_metadata")
    out.mkdir(exist_ok=True)
    out_csv=out/"four_source_taxa_original_iNat_annotated_flowering_CC_photo_review.csv"
    if allrows:
        with out_csv.open("w",encoding="utf8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(allrows[0]))
            writer.writeheader();writer.writerows(allrows)
    else:
        with out_csv.open("w",encoding="utf8",newline="") as f:
            f.write("source_original_iNat_species,fresh_2026_original_iNaturalist_photo_id\n")
    summary={
        "status":"ORIGINAL_I_NAT_ANNOTATED_FLOWERS_VS_UNFILTERED_CC_PHOTO_METADATA_QA",
        "source_4_FCP_VOC_taxa_frozen_before_source_photo_viewing":True,
        "source_original_iNat_phenology_attribute_id":ANNOTATION_ID,
        "source_original_iNat_phenology_flowering_value_id":FLOWERS_VALUE_ID,
        "source_query_results":receipt,
        "source_overlapping_and_new_photo_identifiers":compare_prior(allrows,prior),
        "not_a_photo_level_flower_organ_state_yet":True,
        "source_original_FCP_100_metadata_NOT_recreated":True,
        "no_UV_measurement_or_olfactory_evolution_fitted":True,
        "no_atmospheric_wind_from_wind_pollination_column":True,
        "source_flower_phenology_annotation_is_not_an_independently_double_scored_guide":True,
    }
    (out/"source_annotated_flower_photo_4taxa_vs_unfiltered17_receipt.json").write_text(
       json.dumps(summary,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
       encoding="utf8")
    print("STAGE65_GENUINE_ORIGINAL_I_NAT_FLOWERING_ANNOTATION_SOURCE_FILTER",
          json.dumps(summary,sort_keys=True,ensure_ascii=False))
    print("NO_SOURCE_PHOTO_MARKING_LABEL_ORIGINAL_IMAGE_NOT_YET_REVIEWED")
if __name__=="__main__":
    main()
