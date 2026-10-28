"""Original Cambridge Stage8b read-only source-run entrypoint."""
from __future__ import annotations
import argparse
from pathlib import Path
from within_trip_conditional_lag import run

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="bee_stage8b_source")
    args=parser.parse_args()
    report=run(Path(args.out))
    if report.get("status")!="STAGE8B_CONDITIONAL_NULLS_COMPLETED_OR_EXPLICIT_NO_GO":
        raise ValueError("NO_GO_STAGE8B_COMPLETE_RESULT_NOT_REACHED")
