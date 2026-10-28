"""Run original publisher-bee figure/S1 verified directional inertia vs history.

The artifact is a non-identifying summary; original raw individual visitor
records are not committed to the GitHub repository.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bee_behavior_stage4"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bee_behavior_stage5"))
from source_audit import download_source,parse_original_csv
from bout_transition_analysis import (
    parse_bouts,PUBLISHER_CSV_SHA256
)
from geo_history_holdout import verify_geometry
from turn_inertia_heldout import (
    COORD_PATH,fit_direction_models,incoming_heading_permutation
)

def run(outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    dist,geometry=verify_geometry(COORD_PATH)
    coords={k:tuple(v) for k,v in
            geometry["ten_original_coordinate_labels"].items()}
    raw,receipt=download_source(outdir)
    original_sha=hashlib.sha256(raw).hexdigest()
    if original_sha!=PUBLISHER_CSV_SHA256:
        raise ValueError("NO_GO_STAGE6_EXACT_PUBLISHER_SUPPLEMENT_HASH_CHANGED")
    records,schema=parse_original_csv(raw)
    bouts,source=parse_bouts(records,schema)
    if (source["source_original_bout_rows"],
        source["original_recorded_total_visits"],
        source["original_recorded_within_bout_transitions"],
        source["distinct_bee_tags"])!=(881,6205,5324,10):
        raise ValueError("NO_GO_STAGE6_SOURCE_2019_STUDY_ROW_RECONCILIATION")
    main,cache=fit_direction_models(bouts,coords,dist)
    if main["status"]!="FITTED_INDIVIDUAL_HELDOUT_DIRECTION_ANALYSIS":
        result={
            "status":"NO_GO_STAGE6_DIRECTION_ADMISSION",
            "source_original_sha256":original_sha,
            "source_bout_grain":source,
            "directional_model":main
        }
        (outdir/"bee_stage6_heldout_turn_inertia.json").write_text(
            json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
        print("BEE_STAGE6_ADMISSION_NO_GO "+json.dumps(result,ensure_ascii=False),flush=True)
        raise ValueError("NO_GO_STAGE6_DIRECTION_ADMISSION")
    placebo=incoming_heading_permutation(cache)
    result={
        "status":"ORIGINAL_SOURCE_CONFIRMED",
        "original_supplement_sha256":original_sha,
        "source_doi":"10.1186/s40462-019-0150-z",
        "source_figure_pdf_sha256":geometry["original_figure_sha256"],
        "source_byte_size":len(raw),
        "source_bouts_original":source["source_original_bout_rows"],
        "source_flower_visits_original":source["original_recorded_total_visits"],
        "source_within_bout_pairs_original":source["original_recorded_within_bout_transitions"],
        "source_unique_bee_tags":source["distinct_bee_tags"],
        "directional_model":main,
        "heading_permutation_control":placebo,
        "claim_ceiling":"Source flower-to-flower endpoint geometry, not directly measured animal heading, cognition, wind, controlled social interaction or fitness"
    }
    (outdir/"bee_stage6_heldout_turn_inertia.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("BEE_STAGE6_SOURCE_RECEIPT "+json.dumps({
        "source_sha256":original_sha,"source_fig2_pdf_sha256":geometry["original_figure_sha256"],
        "source_bouts":source["source_original_bout_rows"],
        "source_visits":source["original_recorded_total_visits"],
        "original_source_pairs":source["original_recorded_within_bout_transitions"],
        "bees":source["distinct_bee_tags"]},ensure_ascii=False),flush=True)
    print("BEE_STAGE6_DIRECTION_MODEL "+
          json.dumps(main,ensure_ascii=False,allow_nan=False),flush=True)
    print("BEE_STAGE6_HEADINGS_SHUFFLE "+
          json.dumps(placebo,ensure_ascii=False,allow_nan=False),flush=True)
    print("BEE_STAGE6_DIRECTION_ANALYSIS_COMPLETE",flush=True)
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="bee_stage6_result")
    args=parser.parse_args()
    run(Path(args.out))
