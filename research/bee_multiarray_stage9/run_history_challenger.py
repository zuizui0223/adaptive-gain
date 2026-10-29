"""Run Stage9b first-order history challenger on original 2017 source only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from bout_grain import source_run
from external_turn_transfer import (
    verify_source_plot_coordinates, source_bout_events, split_bouts,
    choose_array_lambdas,
)
from history_challenger import analyze_history_challenge, EXPECTED_ARRAY_TRIPLETS


def run(root:Path):
    original, qa=source_run(root)
    if qa["status"] != "ORIGINAL_2017_BOUTS_AND_S1_S2_MATCHED_WITH_EXPLICIT_20_EXCLUSIONS":
        raise ValueError("NO_GO_ORIGINAL_SOURCE_IDENTITY_LOST")
    previous_path=root/"2017_three_array_external_direction_results.json"
    if not previous_path.exists():
        raise ValueError("NO_GO_PARENT_REAL_SOURCE_FIRST_REQUIRED")
    previous=json.loads(previous_path.read_text())
    if previous["status"]!="REAL_ORIGINAL_SOURCE_DIRECTION_RULE_TRANSPORT_EVALUATED":
        raise ValueError("NO_GO_PARENT_REAL_SOURCE_STATUS")
    coords, figure=verify_source_plot_coordinates(
        source_image=root/"2017_original_source_figure1.jpg")
    groups, source_grain=source_bout_events(original)
    if (source_grain["original_bouts"],source_grain["valid_bouts"],
        source_grain["excluded_nest_boundary_bouts"]) != (1740,1720,20):
        raise ValueError("NO_GO_FROZEN_ORIGINAL_SOURCE_GRAIN")
    population, exclusions=split_bouts(groups,expected_original=True)
    if exclusions!=previous["source_exclusions_prior_outcome"]:
        raise ValueError("NO_GO_PARENT_ORIGINAL_EXCLUSIONS_CHANGED")
    lambdas, early_audit=choose_array_lambdas(population,coords)
    for array in ("1","2","3"):
        expected=previous["train_only_lambda_by_original_array"][array]["selected_source_train_only_lambda_per_m"]
        if lambdas[array]!=expected:
            raise ValueError("NO_GO_PARENT_TRAIN_ONLY_LAMBDA_CHANGED")
    results=analyze_history_challenge(population,coords,lambdas,previous)
    results["original_source_original_SHA256"]={
        "S1":qa["publisher_original_S1"]["original_sha256"],
        "S2":qa["publisher_original_S2"]["original_sha256"]}
    results["original_source_image_SHA256"]=figure["original_publisher_jpeg_sha256"]
    results["parent_source_report_status"]=previous["status"]
    results["parent_original_lambda_reconciled"]=True
    out=root/"2017_three_array_history_conditioned_direction_stage9b.json"
    out.write_text(json.dumps(results,indent=2,ensure_ascii=False,allow_nan=False))
    detail={}
    for array,score in results["source_array_results"].items():
        null=results["source_conditioned_permutation_null"][array]
        detail[array]={
            "source_triplets":score["genuine_heldout_triplets"],
            "bees":score["qualifying_bees"],
            "history_gain_over_geo":score["bee_equal_history_over_geo_gain_nats"],
            "direction_gain_over_geo":score["bee_equal_direction_over_geo_gain_nats"],
            "direction_gain_over_history":score["bee_equal_direction_over_history_gain_nats"],
            "colony_equal_direction_over_history":score["colony_equal_direction_over_history_gain_nats"],
            "colony_gains":score["colony_direction_over_history_gains"],
            "positive_bees":score["bees_positive_direction_over_history"],
            "source_conditional_null_actual_minus_mean":null["actual_minus_null_mean_nats"],
            "source_conditional_null_p":null["one_sided_conditional_p"],
        }
    print("STAGE9B_ORIGINAL_SOURCE_HISTORY_CHALLENGE_RESULT "+json.dumps({
        "status":results["status"],
        "all_six_colony_arrays_positive":results[
            "history_conditioned_direction_descriptively_positive_in_all_six_colony_arrays"],
        "fixed_history_beta":results["fixed_history_beta"],
        "per_array":detail},ensure_ascii=False,allow_nan=False),flush=True)
    print("STAGE9B_HISTORY_CHALLENGE_COMPLETE",flush=True)
    return results


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage9_original")
    run(Path(p.parse_args().out))
