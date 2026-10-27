"""Independent original-source F1-F10 geometry and foraging-history heldout test."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bee_behavior_stage4"))
from source_audit import download_source,parse_original_csv
from bout_transition_analysis import PUBLISHER_CSV_SHA256,parse_bouts,history_holdout_on_bouts
from geo_history_holdout import verify_geometry,analyze_geo

GEOMETRY_FILE=Path(__file__).resolve().with_name(
    "flower_positions_figure2_verified.json")

def analyze(out:Path):
    out.mkdir(exist_ok=True,parents=True)
    distance,geom_receipt=verify_geometry(GEOMETRY_FILE)
    raw,source_receipt=download_source(out)
    source_sha=hashlib.sha256(raw).hexdigest()
    if source_sha!=PUBLISHER_CSV_SHA256:
        raise ValueError("NO_GO_ORIGINAL_BEE_S1_FILE_SHA256_CHANGED")
    visits,shape=parse_original_csv(raw)
    bouts,bout_receipt=parse_bouts(visits,shape)
    original=history_holdout_on_bouts(bouts)
    if bout_receipt["original_recorded_total_visits"]!=6205 or (
       bout_receipt["original_recorded_within_bout_transitions"]!=5324 or
       original["heldout_within_bout_transitions_total"]!=1550 or
       abs(original["mean_per_bee_gain_nats"]-0.20652751831093835)>1e-9):
        raise ValueError("NO_GO_STAGE4_SOURCE_OR_MODEL_RECONCILIATION")
    spatial=analyze_geo(bouts,distance,geom_receipt)
    result={
        "stage":"5_GEOMETRY_VS_BEE_ROUTING_HELDOUT",
        "source_article_doi":"10.1186/s40462-019-0150-z",
        "source_original_s1_sha256":source_sha,
        "source_original_S1_bytes":len(raw),
        "source_study_one_colony":True,
        "no_individual_perceptual_cue_or_wind_treatment":True,
        "original_source_visits_and_bouts":{
            "visits":bout_receipt["original_recorded_total_visits"],
            "bouts":bout_receipt["source_original_bout_rows"],
            "within_bout_transitions":bout_receipt["original_recorded_within_bout_transitions"],
            "tagged_bees":bout_receipt["distinct_bee_tags"]},
        "stage4_on_exact_same_source_reconciliation":{
            "day5_transitions":original["heldout_within_bout_transitions_total"],
            "per_bee_mean_history_gain_nats":original["mean_per_bee_gain_nats"]},
        "geo_history_result":spatial,
    }
    (out/"original_geometry_history_heldout.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("BEE_STAGE5_GEOMETRY_RECEIPT "+
          json.dumps(geom_receipt,ensure_ascii=False),flush=True)
    print("BEE_STAGE5_HELDOUT_RESULT "+
          json.dumps(spatial,ensure_ascii=False),flush=True)
    print("BEE_STAGE5_GEOMETRY_ANALYSIS_COMPLETE",flush=True)
    if spatial["status"]!="FITTED_HELDOUT_SOURCE_GEOMETRY_DESCRIPTIVE":
        raise ValueError("NO_GO_STAGE5_PRIMARY_DATA_SUPPORT")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage5_geo_source")
    args=p.parse_args()
    analyze(Path(args.out))
