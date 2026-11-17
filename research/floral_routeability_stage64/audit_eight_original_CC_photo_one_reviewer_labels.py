"""Stage64 audit independently viewed genuine CC-BY source flower photo pixels.

This is an **unblinded single-reviewer exploratory photograph eligibility**
audit of eight original iNaturalist medium images (two fixed by photo ID
per four source 2020 VOC/FCP study candidate species). Original-source
photo SHA256 & id already verified in immutable Github Actions artifact.
A visible petal spot is a **visual colour marking**, not proof of a
nectar guide, reward reliability, UV pattern, insect perception or fitness.

Every image without reviewable open corolla (vegetative, dried, too far)
is UNKNOWN for floral pattern, **not a biological negative**.
Only photo-level labels from this pilot, no species frequency estimates.
"""
from __future__ import annotations
import argparse,csv,json,hashlib,re
from collections import Counter
from pathlib import Path

TOTAL=8
ALLOWED_ELIGIBLE={
    "OPEN_COROLLA_DETAIL_PRESENT",
    "VEGETATIVE_NO_OPEN_FLOWER",
    "DRIED_INFLORESCENCE_NO_REVIEWABLE_COROLLA",
    "BLOOM_VISIBLE_DETAIL_UNRESOLVED",
}
MARKS={"VISIBLE_COLOUR_PATTERN_PRESENT","VISIBLE_COLOUR_PATTERN_VERIFIED_UNIFORM",
       "UNKNOWN_NOT_EVALUABLE"}
SOURCE_REVIEW="ONE_UNBLINDED_ASSISTANT_SOURCE_IMAGE_REVIEW"
SOURCE_IMAGE_STATUS="ORIGINAL_CC_LICENSED_PIXEL_DOWNLOADED_FOR_BOTANICAL_REVIEW"

def audit(metadata,annotations):
    original=metadata.get("source_image_credits_and_exceptions")
    if (metadata.get("status")!="LICENSED_ORIGINAL_INAT_FOUR_TAXON_SOURCE_PIXEL_REVIEW_GATE"
        or not isinstance(original,list)
        or len(original)!=TOTAL
        or metadata.get("n_licensed_actual_medium_photo_pixels_read")!=TOTAL):
        raise ValueError("NO_GO_ORIGINAL_EIGHT_CC_SOURCE_IMAGES_NOT_VERIFIED")
    if len(annotations)!=TOTAL:
        raise ValueError("NO_GO_SINGLE_REVIEWER_PHOTO_LABEL_COUNT")
    source={}
    for r in original:
        pid=str(r.get("source_original_photo_id",""))
        if r.get("status")!=SOURCE_IMAGE_STATUS or not pid.isdigit() or pid in source:
            raise ValueError("NO_GO_ORIGINAL_IMAGE_ID_OR_READ_STATUS")
        if not re.fullmatch(r"[0-9a-f]{64}",r.get("source_verified_medium_image_SHA256","")):
            raise ValueError("NO_GO_IMAGE_PIXEL_DIGEST_MISSING")
        if r.get("original_license") not in ("cc0","cc-by"):
            raise ValueError("NO_GO_ORIGINAL_LICENSE_NOT_ALLOWED")
        if not r.get("source_original_attribution",""):
            raise ValueError("NO_GO_ORIGINAL_AUTHOR_CREDIT_MISSING")
        source[pid]=r
    found={}
    for a in annotations:
        pid=a.get("source_photo_id","")
        src=source.get(pid)
        if not src or pid in found:
            raise ValueError("NO_GO_UNAUDITED_OR_DUPLICATED_ORIGINAL_IMAGE")
        if (a.get("original_medium_photo_SHA256")!=src["source_verified_medium_image_SHA256"]
            or a.get("source_species")!=src["source_species"]
            or str(a.get("source_observation_id"))!=str(src["source_original_observation_id"])):
            raise ValueError("NO_GO_IMAGE_PHOTO_ID_SPECIES_DIGEST_OR_OBS_MISMATCH")
        if a.get("photo_eligibility_photo_only") not in ALLOWED_ELIGIBLE:
            raise ValueError("NO_GO_UNSUPPORTED_PHOTO_ANTHESIS_STATUS")
        if a.get("reviewed_visible_intrapetal_marking") not in MARKS:
            raise ValueError("NO_GO_SOURCE_UNDERIVED_VISIBLE_PATTERN_LABEL")
        if a["photo_eligibility_photo_only"]!="OPEN_COROLLA_DETAIL_PRESENT" and (
            a["reviewed_visible_intrapetal_marking"]!="UNKNOWN_NOT_EVALUABLE"):
            raise ValueError("NO_GO_NONFLOWER_OR_UNREADABLE_PHOTO_CALLED_PATTERN_NEGATIVE")
        if (a.get("reviewer_status")!=SOURCE_REVIEW
            or a.get("source_RGB_UV_pattern_status")!="UNOBSERVABLE_IN_RGB"
            or a.get("source_VOC_same_plant_status")!="NOT_MEASURED_SAME_INDIVIDUAL"):
            raise ValueError("NO_GO_ONE_REVIEWER_UV_VOC_SAMPLE_PROVENANCE_ERASED")
        found[pid]=a
    counts=Counter(x["photo_eligibility_photo_only"] for x in annotations)
    traits=Counter(x["reviewed_visible_intrapetal_marking"] for x in annotations)
    reviewable=sum(x["photo_eligibility_photo_only"]=="OPEN_COROLLA_DETAIL_PRESENT"
                   for x in annotations)
    if reviewable!=sum(x["reviewed_visible_intrapetal_marking"]!="UNKNOWN_NOT_EVALUABLE"
                       for x in annotations):
        raise ValueError("NO_GO_PHOTO_REVIEWABLE_AND_CONFIRMED_TRAIT_COUNTS_DISAGREE")
    source_distinct=Counter(a["source_species"] for a in annotations
                            if a["reviewed_visible_intrapetal_marking"]=="VISIBLE_COLOUR_PATTERN_PRESENT")
    return {
      "status":"AUTHENTIC_EIGHT_INAT_CC_PHOTO_UNBLINDED_VISIBLE_MARKING_QA_NOT_SPECIES_TRAIT",
      "original_cc_photo_pixels_sha256_verified":TOTAL,
      "n_original_inat_source_taxa":len(set(a["source_species"] for a in annotations)),
      "n_source_photos_with_reviewable_open_corolla":reviewable,
      "n_source_photos_visible_colour_marking_positive":traits["VISIBLE_COLOUR_PATTERN_PRESENT"],
      "n_source_photos_verified_within_corolla_uniform":traits["VISIBLE_COLOUR_PATTERN_VERIFIED_UNIFORM"],
      "n_source_photos_flower_pattern_unknown_not_absent":traits["UNKNOWN_NOT_EVALUABLE"],
      "n_photo_ids_not_exposing_open_or_adequately_resolved_flower":TOTAL-reviewable,
      "by_photo_open_flower_eligibility":dict(sorted(counts.items())),
      "by_visible_pattern_state":dict(sorted(traits.items())),
      "distinct_species_with_source_positive_photo_records":dict(sorted(source_distinct.items())),
      "unblinded_assistant_one_reviewer_no_second_independent_verifier":True,
      "no_species_level_absence_or_frequency_inference":True,
      "photo_marks_not_nectar_guide_function":True,
      "RGB_is_not_UV_measured":True,
      "photo_not_same_original_VOC_specimen":True,
      "source_photo_selection_outcome_blind_before_pixel_review":True,
      "not_independent_plant_lineage_or_bumblebee_wind_effect":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-source-image-credits",required=True)
    p.add_argument("--original-one-reviewer-photo-labels",
                   default="research/floral_routeability_stage64/one_reviewer_actual_8_photo_flower_marking_quality_audit.csv")
    args=p.parse_args()
    original=json.loads(Path(args.original_source_image_credits).read_text())
    with Path(args.original_one_reviewer_photo_labels).open(
        newline="",encoding="utf8") as fp:
        annotations=list(csv.DictReader(fp))
    result=audit(original,annotations)
    out=Path("stage64_actual_image_visual_marking_quality_receipt")
    out.mkdir(exist_ok=True)
    (out/"source_original_8_CC_images_one_reviewer_open_flower_marking_summary.json").write_text(
       json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("STAGE64_ACTUAL_CC_SOURCE_FLORAL_PATTERN_ELIGIBILITY_AND_CONSERVATIVE_ANNOTATION",
          json.dumps(result,sort_keys=True,ensure_ascii=False))
    print("NO_ORIGINAL_4_SPECIES_NEGATIVE_OR_GENUINE_UV_NECTAR_GUIDE_OR_POLLEN_EFFECT")
if __name__=="__main__":
    main()
