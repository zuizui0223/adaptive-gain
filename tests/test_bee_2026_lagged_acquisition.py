"""Offline semantic/sequence regression tests; no third-party raw CSV bundled."""
from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from scripts.analyze_bee_2026_lagged_acquisition import (
    parse_rows, lag_pairs, difference, summarize, xorshift32,
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
