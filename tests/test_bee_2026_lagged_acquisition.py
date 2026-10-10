"""Offline semantic/sequence regression tests; no third-party raw CSV bundled."""
from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from scripts.analyze_bee_2026_lagged_acquisition import (
    parse_rows, lag_pairs, difference, summarize, xorshift32,
    next_regular_pairs, free_cue_carryover_difference,
    summarize_free_cue_carryover,
    git_blob_sha, verify_frozen_receipt,
)

HEADER = (
    "Bee_ID,Trial_Number,Difficulty,Trial_Type,"
    "Info_Requested,Actually_Landed_On_Platform,"
    "Is_Post_Request_Correct,Is_Post_Non_Request_Correct\n"
)


def _toy_bees():
    lines = [HEADER]
    for idx, diff in enumerate(("Easy", "Hard", "Impossible")):
        for j in range(4):
            bee = f"Bee_{idx*4+j+1:03d}"
            previous_correct = int(j < 2)
            next_landing = int(j in (1, 2, 3))
            lines.append(
                f"{bee},1,{diff},Regular,0,0,,{previous_correct}\n"
            )
            if next_landing:
                lines.append(f"{bee},2,{diff},Regular,1,1,1,\n")
            else:
                lines.append(f"{bee},2,{diff},Regular,0,0,,1\n")
            # Information delivery is not the same as requesting it.
            lines.append(
                f"{bee},3,{diff},Random_Free_Cue,1,0,1,\n"
            )
            lines.append(
                f"{bee},4,{diff},Regular,0,0,,1\n"
            )
    return parse_rows(io.StringIO("".join(lines)))


def test_lag_pairs_avoid_free_cue_and_other_task_ids():
    bees = _toy_bees()
    pairs = lag_pairs(bees)
    assert len(bees) == 12
    assert sum(len(group) for group in pairs.values()) == 12
    assert all(group[0]["prior_fail"] in (0, 1)
               for group in pairs.values())
    assert all(group[0]["prev_request"] == 0
               for group in pairs.values())
    assert all(group[0]["bin"] == 0 for group in pairs.values())


def test_balanced_toy_previous_error_effect_and_bootstrap():
    bees = _toy_bees()
    all_pairs = [item for group in lag_pairs(bees).values() for item in group]
    for d in ("Easy", "Hard", "Impossible"):
        crude = difference(all_pairs, d, adjusted=False)
        adjusted = difference(all_pairs, d, adjusted=True)
        assert crude["fail_minus_success"] == pytest.approx(0.5)
        assert adjusted["fail_minus_success"] == pytest.approx(0.5)
        assert adjusted["covered_trials"] == 4
        assert adjusted["included_strata"] == 1
    a = summarize(bees, bootstrap_reps=100, seed=0x5EEC23)
    b = summarize(bees, bootstrap_reps=100, seed=0x5EEC23)
    assert a == b
    assert a["regular_following_regular_pairs"] == 12
    assert a["status"] == "EXPLORATORY_SEQUENCE_ASSOCIATION_NO_CAUSAL_HISTORY_EFFECT"


def test_structural_outcome_and_delivery_rules_reject_invalid_rows():
    valid = (
        HEADER
        + "Bee_A,1,Easy,Regular,0,0,,1\n"
        + "Bee_A,2,Hard,Regular,1,1,0,\n"
        + "Bee_A,3,Impossible,Random_Free_Cue,1,0,1,\n"
    )
    assert len(parse_rows(io.StringIO(valid))["Bee_A"]) == 3

    invalid = [
        valid.replace("Regular,0,0,,1", "Regular,1,0,,1"),
        valid.replace("Regular,1,1,0,", "Regular,1,1,0,0"),
        valid.replace("Random_Free_Cue,1,0,1,", "Random_Free_Cue,0,0,1,"),
        valid.replace("Bee_A,3,Impossible", "Bee_A,2,Impossible"),
    ]
    for wrong in invalid:
        with pytest.raises(ValueError):
            parse_rows(io.StringIO(wrong))

    with pytest.raises(ValueError):
        difference([], "unknown", adjusted=True)
    with pytest.raises(ValueError):
        summarize(_toy_bees(), bootstrap_reps=0)
    with pytest.raises(ValueError):
        next(xorshift32(0))


def test_frozen_public_source_result_is_not_interpreted_causally():
    source = (
        Path(__file__).resolve().parents[1]
        / "validation" / "bee_2026_lagged_request_exploratory_v1.json"
    )
    record = json.loads(source.read_text(encoding="utf-8"))
    assert record["source"]["blob_sha"] == (
        "26259c9071c6d73141d56b9bedd396cab1a04491"
    )
    assert record["n_bees"] == 192
    assert record["n_total_trials"] == 19200
    assert record["regular_following_regular_pairs"] == 12132
    assert record["status"] == (
        "EXPLORATORY_SEQUENCE_ASSOCIATION_NO_CAUSAL_HISTORY_EFFECT"
    )
    for d in ("Easy", "Hard", "Impossible"):
        estimate = record["difficulty"][d]
        assert estimate["covered_trials"] <= record["regular_following_regular_pairs"]
        ci = estimate["bee_cluster_bootstrap_95"]
        assert ci[0] < 0 < ci[1]
        assert estimate["bootstrap_valid_repetitions"] == 1500



def test_previous_free_cue_exposure_is_not_previous_voluntary_request():
    bees = _toy_bees()
    pairs = next_regular_pairs(bees)
    assert len(pairs) == 12
    assert sum(len(records) for records in pairs.values()) == 24
    # Every bee contributes one Regular->Regular and one Free->Regular pair.
    assert all(sum(x["prev_free"] for x in records) == 1
               for records in pairs.values())
    assert all(sum(1 for x in records if x["prev_free"] == 0) == 1
               for records in pairs.values())

    all_rows = [x for record in pairs.values() for x in record]
    raw = free_cue_carryover_difference(
        all_rows, "Hard", adjusted=False
    )
    assert raw["covered_trials"] == 8
    assert raw["free_minus_regular_previous_trial"] == pytest.approx(-.75)
    for d in ("Easy", "Hard", "Impossible"):
        x = free_cue_carryover_difference(
            all_rows, d, adjusted=True
        )
        assert x["covered_trials"] > 0
        assert x["included_strata"] >= 1


def test_previous_free_exposure_bootstrap_and_frozen_source():
    bees = _toy_bees()
    a = summarize_free_cue_carryover(bees, bootstrap_reps=50)
    b = summarize_free_cue_carryover(bees, bootstrap_reps=50)
    assert a == b
    assert a["next_regular_after_any_previous_type"] == 24
    assert a["status"] == (
        "EXPLORATORY_LAGGED_EXPOSURE_ASSOCIATION_NOT_INFORMATION_CAUSAL_EFFECT"
    )
    receipt = json.loads(
        (Path(__file__).resolve().parents[1] / "validation"
         / "bee_2026_lagged_request_exploratory_v1.json").read_text(
             encoding="utf-8"
         )
    )["previous_free_cue_exposure"]
    assert receipt["next_regular_after_any_previous_type"] == 15205
    for d in ("Easy", "Hard", "Impossible"):
        x = receipt["by_current_difficulty"][d]
        assert x["strata"] == 30
        assert x["bee_cluster_bootstrap_95"][0] < 0 < (
            x["bee_cluster_bootstrap_95"][1]
        )
        assert x["bootstrap_valid_repetitions"] == 1500



def test_git_blob_pin_algorithm_and_receipt_checker():
    assert git_blob_sha(b"hello\n") == (
        "ce013625030ba8dba906f756967f9e9ca394464a"
    )
    bees = _toy_bees()
    current = summarize(bees, bootstrap_reps=50, seed=0x5EEC23)
    current["previous_free_cue_exposure"] = summarize_free_cue_carryover(
        bees, bootstrap_reps=50
    )
    import copy
    frozen = copy.deepcopy(current)
    verify_frozen_receipt(current, frozen)
    bad = copy.deepcopy(frozen)
    bad["difficulty"]["Hard"]["stratified_fail_minus_success"] += .1
    with pytest.raises(ValueError, match="frozen result differs"):
        verify_frozen_receipt(current,bad)
    bad = copy.deepcopy(frozen)
    bad["source"]["blob_sha"] = "wrong"
    with pytest.raises(ValueError, match="source blob metadata differs"):
        verify_frozen_receipt(current,bad)
    bad = copy.deepcopy(frozen)
    bad["previous_free_cue_exposure"]["by_current_difficulty"]["Easy"][
        "bee_cluster_bootstrap_95"][0] += .01
    with pytest.raises(ValueError, match="frozen result differs"):
        verify_frozen_receipt(current,bad)
