"""Reproducible original bee-bout empirical history prediction and source receipt.

Runs only after source publisher CSV was downloaded and SHA-256 validated.
Does not distribute raw experimental bee tags or observations.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from source_audit import parse_original_csv
from bout_transition_analysis import (
    PUBLISHER_CSV_SHA256, parse_bouts,history_holdout_on_bouts,PHYSICAL_FLOWERS
)

def analyze(original:Path,out:Path):
    raw=original.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=PUBLISHER_CSV_SHA256:
        raise ValueError("NO_GO_PUBLISHER_SOURCE_SHA256_MISMATCH")
    rows,meta=parse_original_csv(raw)
    bouts,structure=parse_bouts(rows,meta)
    estimate=history_holdout_on_bouts(bouts,PHYSICAL_FLOWERS)
    result={
        "source_doi":"10.1186/s40462-019-0150-z",
        "source_file":"40462_2019_150_MOESM2_ESM.csv",
        "exact_sha256":digest,
        "source_original_csv_rows":len(rows),
        "original_bout_observation_structure":structure,
        "heldout_prediction":estimate,
        "source_p2_displacement_gate":"NO_GO_NO_PUBLISHER_DATASET_S1_ENCOUNTER_OUTCOME_FIELD",
        "do_not_claim":"direct ecological wind measurement, perceptual cue order, reproductive fitness, experimental cue routing or independent colonies"
    }
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    print("BEE_STAGE4_BOUT_STRUCTURE "+json.dumps(structure,ensure_ascii=False),flush=True)
    print("BEE_STAGE4_HELDOUT_MODEL "+json.dumps(estimate,ensure_ascii=False),flush=True)
    print("BEE_STAGE4_BOUT_ANALYSIS_COMPLETE",flush=True)
    return result

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="bee_stage4_source")
    args=parser.parse_args(argv)
    root=Path(args.out)
    analyze(root/"original_publisher_dataset_s1.csv",
            root/"bee_bout_history_heldout_result.json")

if __name__=="__main__":
    main()
