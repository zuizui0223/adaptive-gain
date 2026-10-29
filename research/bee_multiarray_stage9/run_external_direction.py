"""Run Stage 9 actually held-out 2017 independent three-array directions.

Reads original publisher Supplement S1/S2 and Figure 1 each verified by
byte-level SHA256 within transient CI. Source 20 nest-marker anomalies are
preserved in the provenance ledger but not used to construct physical routes.
Never re-fit the 2019 external dimensionless κ=1 turning rule.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from bout_grain import source_run
from external_turn_transfer import analyze

def run(root:Path):
    root.mkdir(parents=True,exist_ok=True)
    original,qa=source_run(root)
    if qa["status"]!="ORIGINAL_2017_BOUTS_AND_S1_S2_MATCHED_WITH_EXPLICIT_20_EXCLUSIONS":
        raise ValueError("NO_GO_ORIGINAL_2017_EXPERIMENT_NOT_RECONCILED")
    report=analyze(original,
                   image_path=root/"2017_original_source_figure1.jpg",
                   expected_original=True)
    report["original_publisher_source_sha256"]={
        "S1":qa["publisher_original_S1"]["original_sha256"],
        "S2":qa["publisher_original_S2"]["original_sha256"]}
    report["original_publisher_source_quality_gate"]=qa["status"]
    result_file=root/"2017_three_array_external_direction_results.json"
    result_file.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE9_SOURCE_TEST_RESULT "+json.dumps({
        "status":report["status"],
        "source_bouts":report["source_original_bout_accounting"],
        "lambda":report["train_only_lambda_by_original_array"],
        "tested_arrays":{
            k:{
                "status":x["status"],
                "tags":x["qualifying_original_individuals"],
                "real_triplets":x["original_source_test_genuine_triplets"],
                "source_colonies":x["original_colonies"],
                "geo_nll":x["bee_equal_Mgeo_nll"],
                "externally_fixed_turn_nll":x["bee_equal_Mexternalkappa1_nll"],
                "actual_gain":x["bee_equal_external_direction_gain_nats"],
                "positive_bees":x["bees_with_positive_gain"],
                "negative_bees":x["bees_with_negative_gain"],
                "colony_gains":x["independent_colony_mean_gain"]
            } for k,x in report["original_heldout_comparisons_by_array"].items()},
        "source_conditional_nulls":report["original_heldout_conditional_direction_null_by_array"],
        "source_figure_jitter":report["fixed_21_plot_digitization_perturbations"]
    },ensure_ascii=False,allow_nan=False),flush=True)
    print("STAGE9_EXTERNAL_LAYOUT_DIRECTION_COMPLETE",flush=True)
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage9_original")
    args=p.parse_args()
    run(Path(args.out))
