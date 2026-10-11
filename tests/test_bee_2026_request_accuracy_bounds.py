"""Non-identification tests with exhaustive missing-potential-outcome assignments."""
from __future__ import annotations

import io
import itertools
import json
from pathlib import Path

import pytest

from adaptive_gain.partial_identification import binary_action_accuracy_bounds
from scripts.audit_bee_2026_request_accuracy_bounds import (
    analyze, source_outcome_counts, verify_against_receipt
)


def test_sharp_bounds_attained_by_all_counterfactual_completions():
    # Observed (A,Y) rows: action success, action failure,
    # no-action success, no-action failure. One missing potential
    # outcome per encounter.
    observed = [(1,1),(1,0),(0,1),(0,0)]
    outcomes = []
    for missing in itertools.product((0,1), repeat=len(observed)):
        total = 0
        for (a,y),m in zip(observed,missing):
            y1,y0 = (y,m) if a == 1 else (m,y)
            total += y1-y0
        outcomes.append(total/len(observed))
    r = binary_action_accuracy_bounds(1,1,1,1)
    assert r.n == 4
    assert r.naive_conditional_difference == pytest.approx(0)
    assert r.ate_lower == pytest.approx(min(outcomes))
    assert r.ate_upper == pytest.approx(max(outcomes))
    assert r.ate_lower == pytest.approx(-.5)
    assert r.ate_upper == pytest.approx(.5)


def test_no_randomization_implies_broad_bounds_even_after_high_correctness():
    for data in [
        (555,36,4163,1386,-.6838762214983712,.31612377850162876),
        (2662,204,1600,1642,-.2953503601833661,.704649639816634),
        (2073,156,183,700,-.10893316195372749,.8910668380462725),
    ]:
        ay,aw,ny,nw,low,high = data
        result = binary_action_accuracy_bounds(ay,aw,ny,nw)
        assert result.ate_lower == pytest.approx(low)
        assert result.ate_upper == pytest.approx(high)
        assert result.ate_lower < 0 < result.ate_upper
        assert result.observed_action_success_rate > .92
        assert result.naive_conditional_difference > .18
    with pytest.raises(ValueError):
        binary_action_accuracy_bounds(0,0,0,0)
    with pytest.raises(ValueError):
        binary_action_accuracy_bounds(1.5,0,0,1)
    with pytest.raises(ValueError):
        binary_action_accuracy_bounds(-1,1,1,1)


def test_source_parser_refuses_mix_of_delivery_and_purchase():
    hdr = (
        "Trial_ID,Bee_ID,Difficulty,Trial_Type,Info_Requested,"
        "Actually_Landed_On_Platform,Is_Post_Request_Correct,"
        "Is_Post_Non_Request_Correct\n"
    )
    source = hdr + (
        "1,Bee_1,Easy,Regular,1,1,1,\n"
        "2,Bee_1,Easy,Regular,0,0,,1\n"
        "3,Bee_1,Easy,Random_Free_Cue,1,0,1,\n"
        "4,Bee_1,Hard,Regular,1,1,1,\n"
        "5,Bee_1,Hard,Regular,0,0,,0\n"
        "6,Bee_1,Impossible,Regular,1,1,1,\n"
        "7,Bee_1,Impossible,Regular,0,0,,0\n"
    )
    groups = source_outcome_counts(io.StringIO(source))
    assert groups["Easy"]["request_correct"] == 1
    assert groups["Easy"]["no_request_correct"] == 1
    assert groups["Easy"]["n_free"] == 1
    assert groups["Easy"]["free_correct"] == 1
    assert analyze(groups)["regular_trials_by_difficulty"]["Easy"]["n_request"] == 1
    for wrong in (
        source.replace("Regular,1,1,1,", "Regular,1,0,1,"),
        source.replace("Random_Free_Cue,1,0,1,", "Random_Free_Cue,0,0,1,"),
        source.replace("Regular,0,0,,1", "Regular,0,0,1,1"),
        source + "7,Bee_2,Easy,Regular,0,0,,1\n",
    ):
        with pytest.raises(ValueError):
            source_outcome_counts(io.StringIO(wrong))


def test_frozen_public_outcome_counts_not_a_causal_point_estimate():
    root = Path(__file__).resolve().parents[1]
    frozen = json.loads(
        (root/"validation"/"bee_2026_request_ate_bounds_v1.json").read_text(
            encoding="utf-8"
        )
    )
    counts = {}
    for diff, g in frozen["regular_trials_by_difficulty"].items():
        counts[diff] = {
            k:g[k] for k in (
                "n_regular", "request_correct", "request_wrong",
                "no_request_correct", "no_request_wrong", "n_free", "free_correct"
            )
        }
    output = analyze(counts)
    verify_against_receipt(output,frozen)
    assert frozen["status"] == (
        "PARTIAL_IDENTIFICATION_SIGN_UNRESOLVED_IN_ALL_THREE_DIFFICULTIES"
    )
    for g in output["regular_trials_by_difficulty"].values():
        assert g["sharp_ate_lower"] < 0 < g["sharp_ate_upper"]
        assert g["observed_request_accuracy"] > .92
