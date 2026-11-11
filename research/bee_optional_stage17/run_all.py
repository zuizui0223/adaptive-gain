"""Stage17 original-source-free synthetic test receipts — NO real animal inference."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from allocation import generate,receipt as allocation_receipt
from source_gate import make_mock_source,validate_mock_source
from estimator import estimate_mock_ITT

MOCK_PILOT_DELAY_BOUNDS={"low":(.19,.21),"medium":(.99,1.01),"high":(2.99,3.01)}

def run(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    assignments=generate(24,12)
    fake=make_mock_source(assignments,inject_middle_only_mg=2.0)
    qa,valid=validate_mock_source(assignments,fake,MOCK_PILOT_DELAY_BOUNDS)
    if valid is None:raise RuntimeError("NO_GO_SYNTHETIC_SOURCE_GATE")
    result=estimate_mock_ITT(assignments,valid)
    if result["status"]!="SYNTHETIC_ONLY_COLONY_ESTIMATOR_QA":
        raise RuntimeError("NO_GO_COLONY_MOCK_ESTIMATOR")
    if not abs(result["middle_vs_extremes_curvature_mg"]-2.0)<.1:
        raise ValueError("NO_GO_INJECTED_MOCK_MIDDLE_EFFECT_NOT_RECOVERED")
    # Do not save per-trial fake event streams, source animal IDs, and
    # individual source assignments; the public receipt is aggregate only.
    document={
      "status":"STAGE17_SYNTHETIC_OPTIONAL_FIRST_QUERY_QA_VERIFIED",
      "source_data_date":"2026-11-11",
      "real_bee_trials":0,
      "synthetic_original_assignments":len(assignments),
      "source_allocation_digest":allocation_receipt()["public_mock_schedule_sha256"],
      "source_allocation_arm_counts":allocation_receipt()["arm_counts"],
      "source_record_contract":qa,
      "colony_equal_mock_estimate":{
          k:v for k,v in result.items() if k not in
          ("synthetic_two_sided_p_NOT_EMPIRICAL","synthetic_CI95_NOT_EMPIRICAL","synthetic_colony_df")
      },
      "original_pilot_delay_ranges_are_FAKE_seconds":MOCK_PILOT_DELAY_BOUNDS,
      "synthetic_mid_only_treatment_addition_not_empirical_mg":2.0,
      "does_not_estimate_root_learning_or_real_cost_curve":True,
      "real_colony_based_variance_not_calibrated":True,
      "no_preregistered_animal_work_has_occurred":True,
      "scientific_claim_ceiling":"source-free design and code validation only"
    }
    p=root/"stage17_synthetic_design_receipt.json"
    p.write_text(json.dumps(document,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE17_SYNTHETIC_NO_BEES_RESULT "+json.dumps({
        "status":document["status"],
        "source_original_real_bees":document["real_bee_trials"],
        "fake_trials":document["synthetic_original_assignments"],
        "fake_arms":document["source_allocation_arm_counts"],
        "fake_explicit_skips":qa["source_explicit_skip_trials"],
        "fake_source_leaf_events":qa["physical_first_and_second_leaf_events"],
        "mock_injected_K_mg_not_empirical":result["middle_vs_extremes_curvature_mg"],
        "mean_leaf_requests_by_cost":result["mean_leaf_requests_by_tier"],
        "mean_skip_fraction_by_cost":result["mean_skip_fraction_by_tier"]
    },ensure_ascii=False,allow_nan=False),flush=True)
    return document

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage17_outputs")
    run(p.parse_args().out)
