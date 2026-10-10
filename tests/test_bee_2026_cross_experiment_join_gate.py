"""Test guardrails against false joining of public bee task CSVs.

Only synthetic trial examples are committed here. The original 2026
information-seeking and decision-latency data are kept at the authors'
repository, not duplicated in this test suite.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.audit_bee_2026_cross_experiment_join import (
    REQUIRED_ACTIVE, REQUIRED_LATENCY,
    audit, load_rows, pearson, xorshift32,
)


ACTIVE = (
    "Trial_ID,Bee_ID,Trial_Number,Difficulty,Trial_Type,"
    "Info_Requested,Actually_Landed_On_Platform\n"
)
LATENCY = (
    "Trial_ID,Bee_ID,Trial_Number,Difficulty,"
    "Decision_Latency_ms\n"
)


def _fixtures(tmp_path: Path, *, shuffle_task_difficulty: bool = True):
    source_info, source_latency = tmp_path/"active.csv", tmp_path/"latency.csv"
    data_a, data_l = [ACTIVE], [LATENCY]
    diff=("Easy", "Hard", "Impossible")
    ident=0
    for bee in ("Bee_001","Bee_002","Bee_003"):
        for trial in range(1,7):
            ident+=1
            original=diff[(trial-1)//2]
            other=diff[((trial-1)//2+1)%3] if shuffle_task_difficulty else original
            is_free=(trial%2==0)
            landed=int(trial%3==0)
            typ="Random_Free_Cue" if is_free else "Regular"
            delivered=1 if is_free else landed
            data_a.append(
                f"{ident},{bee},{trial},{original},{typ},"
                f"{delivered},{landed}\n"
            )
            data_l.append(
                f"{ident},{bee},{trial},{other},{1500+trial*50}\n"
            )
    source_info.write_text("".join(data_a),encoding="utf-8")
    source_latency.write_text("".join(data_l),encoding="utf-8")
    return source_info,source_latency


def test_recycled_triplet_keys_are_not_a_shared_trial_event(tmp_path):
    active_file,latency_file=_fixtures(tmp_path)
    out=audit(
        load_rows(active_file,REQUIRED_ACTIVE),
        load_rows(latency_file,REQUIRED_LATENCY),
        permutation_replicates=10,
    )
    assert out["active_trials"]==18
    assert out["latency_trials"]==18
    assert out["identical_numeric_triplet_keys"]==18
    assert out["mismatched_task_difficulty_at_identical_triplet_keys"]==18
    assert out["matching_task_difficulty_at_identical_triplet_keys"]==0
    assert out["mismatch_fraction"]==1
    assert out["free_cue_trials_per_bee_histogram"]=={"3":3}
    assert out["verdict"]=="HOLD_NO_CROSS_EXPERIMENT_TRIAL_LEVEL_LATENCY_JOIN"


def test_matched_difficulty_alone_does_not_authorize_cross_task_join(tmp_path):
    active_file,latency_file=_fixtures(
        tmp_path,shuffle_task_difficulty=False
    )
    out=audit(
        load_rows(active_file,REQUIRED_ACTIVE),
        load_rows(latency_file,REQUIRED_LATENCY),
        permutation_replicates=10,
    )
    assert out["mismatched_task_difficulty_at_identical_triplet_keys"]==0
    assert out["verdict"]=="HOLD_NO_CROSS_EXPERIMENT_TRIAL_LEVEL_LATENCY_JOIN"


def test_duplicate_composite_ids_and_bad_schema_are_rejected(tmp_path):
    a,l=_fixtures(tmp_path)
    records=a.read_text(encoding="utf-8").splitlines()
    a.write_text("\n".join([records[0],records[1],records[1]])+"\n")
    with pytest.raises(ValueError,match="duplicate composite key"):
        load_rows(a,REQUIRED_ACTIVE)
    l.write_text("Trial_ID,Bee_ID,Trial_Number\n1,Bee_001,1\n")
    with pytest.raises(ValueError,match="required columns"):
        load_rows(l,REQUIRED_LATENCY)


def test_permutation_and_pearson_edge_cases_are_deterministic():
    r1=xorshift32(0x229184)
    r2=xorshift32(0x229184)
    assert [next(r1) for _ in range(5)]==[next(r2) for _ in range(5)]
    assert pearson([1,2,3],[1,2,3])==pytest.approx(1)
    assert pearson([1,1,1],[1,2,3]) is None


def test_frozen_source_receipt_contains_blocked_join_and_no_causal_claim():
    path=Path(__file__).resolve().parents[1]/"validation"/(
        "bee_2026_cross_experiment_join_gate_v1.json"
    )
    obj=json.loads(path.read_text(encoding="utf-8"))
    assert obj["active_trials"]==19200
    assert obj["latency_trials"]==19200
    assert obj["identical_numeric_triplet_keys"]==19200
    assert obj["matching_task_difficulty_at_identical_triplet_keys"]==6801
    assert obj["mismatched_task_difficulty_at_identical_triplet_keys"]==12399
    assert obj["verdict"]=="HOLD_NO_CROSS_EXPERIMENT_TRIAL_LEVEL_LATENCY_JOIN"
    assert obj["source"]["active_blob_sha"]!=obj["source"]["latency_blob_sha"]
