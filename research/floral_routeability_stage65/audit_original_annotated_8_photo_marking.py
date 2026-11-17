"""Stage65 authentic flowering-annotated photo visible-marking eligibility audit.

Previous Stage64 checked eight real licensed photos and validated original
source medium-pixel SHA256. Stage65 independently read eight pixels chosen
before inspection from a fresh annotated-flowering iNaturalist source query.
First cue 'Flowers' is *observation annotation*, not guaranteed that every
photo has an open flower or detectable petal marking.

Stage64 one-reviewer photo audit function validates all eight original
photo ID, observation ID, original image SHA, attribution/license and
missingness, not UV, guide function, VOC sample or pollinator data.
This Stage65 verifies *each manually inspected* source photo ID was in
the annotated original source records and identifies reused Stage64 photo
IDs. Counts remain photo-specific and single-rater unblinded pilot; no
phenology-filter causal effect or rate claim.
"""
from __future__ import annotations
import argparse,csv,json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_routeability_stage64"))
from audit_eight_original_CC_photo_one_reviewer_labels import audit

def source_csv(path):
    with Path(path).open(newline="",encoding="utf8") as f:
        return list(csv.DictReader(f))

def verified_stage65(source_credit,stage65_source,labels,prior_labels):
    result=audit(source_credit,labels)
    if len(stage65_source)!=27:
        raise ValueError("NO_GO_ORIGINAL_ANNOTATED_SOURCE_27_PHOTO_FRAME")
    newmap={}
    for r in stage65_source:
        key=str(r.get("fresh_2026_original_iNaturalist_photo_id","")).strip()
        if not key.isdigit() or key in newmap:
            raise ValueError("NO_GO_SOURCE_ANNOTATED_PHOTO_ID_NONUNIQUE")
        if (r.get("source_annotation_plant_phenology_flowers_server_filtered") not in (True,"True")
            or r.get("actual_individual_photo_visible_open_flower_status")!="NOT_YET_VERIFIED_FROM_PIXELS"):
            raise ValueError("NO_GO_ORIGINAL_FLOWERING_ANNOTATION_NOT_AUTHENTICATED")
        newmap[key]=r
    for r in labels:
        key=r["source_photo_id"]
        source=newmap.get(key)
        if source is None or (r["source_species"]!=source["source_original_iNat_species"]
                              or r["source_observation_id"]!=str(source["fresh_2026_original_iNaturalist_observation_id"])):
            raise ValueError("NO_GO_ORIGINAL_IMAGE_NOT_A_FLOWERING_ANNOTATED_SOURCE")
    if len(prior_labels)!=8:
        raise ValueError("NO_GO_ORIGINAL_STAGE64_PREVIOUS_8_PHOTO_FRAME")
    prior={r["source_photo_id"] for r in prior_labels}
    if len(prior)!=8:
        raise ValueError("NO_GO_STAGE64_ORIGINAL_REUSED_PHOTO_ID")
    current={r["source_photo_id"] for r in labels}
    overlap=current&prior
    positive={
        r["source_photo_id"] for r in labels
        if r["reviewed_visible_intrapetal_marking"]=="VISIBLE_COLOUR_PATTERN_PRESENT"
    }
    result.update({
        "status":"STAGE65_SOURCE_VERIFIED_FLOWERING_ANNOTATED_EIGHT_PHOTO_SINGLE_REVIEWER_PATTERN_QA",
        "n_annotated_CC_original_photo_source_records":len(stage65_source),
        "n_image_inspected_CC_licenced_original_photo_records":len(current),
        "n_stage65_images_reused_from_old_stage64_original_photo_sample":len(overlap),
        "n_stage65_images_not_in_old_stage64_eight_image_sample":len(current-prior),
        "n_source_positive_photo_IDs_already_in_stage64_manual_review":len(positive&prior),
        "n_source_positive_photo_IDs_not_in_stage64_image_sample":len(positive-prior),
        "flowering_annotation_is_observation_not_flower_image":True,
        "between_two_pilot_photographs_not_randomized_phenology_control":True,
        "positive_photo_records_not_evolutionarily_independent_species_fitness":True,
        "old_photo_source_not_external_data_source":True,
        "source_cue_routing_wind_VOC_mechanism_not_measured":True,
    })
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-CC8-image-credits",required=True)
    p.add_argument("--source-flowering-annotated-27",required=True)
    p.add_argument("--prior-unfiltered-8-annotations",
            default="research/floral_routeability_stage64/one_reviewer_actual_8_photo_flower_marking_quality_audit.csv")
    p.add_argument("--single-reviewer-8-annotations",
            default="research/floral_routeability_stage65/one_reviewer_actual_8_flower_annotated_photo_marking_audit.csv")
    x=p.parse_args()
    obs=verified_stage65(
        json.loads(Path(x.source_CC8_image_credits).read_text()),
        source_csv(x.source_flowering_annotated_27),
        source_csv(x.single_reviewer_8_annotations),
        source_csv(x.prior_unfiltered_8_annotations)
    )
    out=Path("stage65_original_flowering_CC_photo_real_marking_QA")
    out.mkdir(exist_ok=True)
    (out/"original_annotated_flowering_8_photo_review_eligibility_summary.json").write_text(
       json.dumps(obs,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("STAGE65_ACTUAL_ORIGINAL_FLOWERING_ANNOTATED_CC8_PHOTO_VISIBLE_MARKING_RESULTS",
          json.dumps(obs,ensure_ascii=False,sort_keys=True))
    print("NO_VISIBLE_NECTAR_GUIDE_FUNCTION_OR_GENUINE_UV_VOC_WIND_ASSOCIATION")
if __name__=="__main__":
    main()
