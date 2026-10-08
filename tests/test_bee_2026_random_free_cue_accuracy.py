"""Tests for descriptive automatic-cue assignment contrasts.

Only synthetic trials and aggregate, pinned receipts are committed.
No raw 2026 bee data are copied into adaptive-gain.
"""
from __future__ import annotations

import copy
import io
import json
from pathlib import Path

import pytest

from scripts.audit_bee_2026_random_free_cue_accuracy import (
    analyze, contrasts, git_blob_sha, parse_trials, verify_receipt,
)

HEADER = (
    "Trial_ID,Bee_ID,Trial_Number,Difficulty,Trial_Type,"
    "Info_Requested,Actually_Landed_On_Platform,"
    "Is_Post_Request_Correct,Is_Post_Non_Request_Correct\n"
)


def _synthetic_trials():
    lines = [HEADER]
    trial_id = 0
    for bee_index in range(1, 5):
        bee = f"Bee_{bee_index:03d}"
        for t in range(1, 101):
            trial_id += 1
            j = (t - 1) % 20 + 1
            difficulty = ("Easy", "Hard", "Impossible")[j % 3]
            free = (j % 5 == 0)
            correctness = int(free or difficulty == "Easy")
            landed = int(bee_index % 2 == 0) if free else int(j % 7 == 0)
            info = 1 if free else landed
            post = str(correctness) if free or landed else ""
            non = str(correctness) if not free and not landed else ""
            lines.append(
                f"{trial_id},{bee},{t},{difficulty},"
                f"{'Random_Free_Cue' if free else 'Regular'},"
                f"{info},{landed},{post},{non}\n"
            )
    return parse_trials(io.StringIO("".join(lines)))


def test_one_hundred_trial_design_and_descriptive_offer_contrast():
    source = _synthetic_trials()
    assert len(source) == 4
    assert all(len(v) == 100 for v in source.values())
    z = analyze(source, bootstrap_repetitions=20)
    assert z["n_trials"] == 400
    assert z["free_cue_trials_per_bee_histogram"] == {"20": 4}
    assert z["accuracy_by_difficulty"]["Easy"]["free_minus_regular_accuracy"] == pytest.approx(0)
    for d in ("Hard", "Impossible"):
        assert z["accuracy_by_difficulty"][d]["free_minus_regular_accuracy"] == pytest.approx(1)
        assert z["accuracy_by_difficulty"][d]["paired_bee_signs"]["positive"] == 4
    assert len(z["trial_order_20_bins"]) == 5
    for d in ("Easy", "Hard", "Impossible"):
        control = z["free_arm_landing_accuracy_control"]["by_difficulty"][d]
        assert control["free_landed"]["n"] > 0
        assert control["free_not_landed"]["n"] > 0
        assert control["landing_minus_no_landing"] == pytest.approx(0)


def test_free_information_delivery_is_not_a_voluntary_request():
    example = HEADER + (
        "1,Bee_A,1,Easy,Random_Free_Cue,1,0,1,\n"
        "2,Bee_A,2,Easy,Regular,0,0,,1\n"
        "3,Bee_B,1,Hard,Random_Free_Cue,1,0,1,\n"
        "4,Bee_B,2,Hard,Regular,0,0,,1\n"
        "5,Bee_C,1,Impossible,Random_Free_Cue,1,0,1,\n"
        "6,Bee_C,2,Impossible,Regular,0,0,,1\n"
    )
    source = parse_trials(io.StringIO(example))
    pair = contrasts(sorted(source.items()))["Easy"]
    assert pair["free"]["n"] == 1
    assert pair["free"]["landing"] == 0
    assert pair["free"]["correct"] == 1
    assert pair["regular"]["landing"] == 0
    bad = [
        example.replace("Random_Free_Cue,1,0,1,", "Random_Free_Cue,0,0,1,"),
        example.replace("Regular,0,0,,1", "Regular,1,0,,1"),
        example.replace("Regular,0,0,,1", "Regular,0,0,1,1"),
        example + "2,Bee_B,3,Easy,Regular,0,0,,1\n",
    ]
    for text in bad:
        with pytest.raises(ValueError):
            parse_trials(io.StringIO(text))


def test_reproduction_and_mutation_guard():
    data = _synthetic_trials()
    a = analyze(data, bootstrap_repetitions=12, seed=0x7A4408)
    b = analyze(data, bootstrap_repetitions=12, seed=0x7A4408)
    assert a == b
    verify_receipt(a, copy.deepcopy(a))
    altered = copy.deepcopy(a)
    altered["accuracy_by_difficulty"]["Hard"]["free_minus_regular_accuracy"] += .1
    with pytest.raises(ValueError, match="frozen effect differs"):
        verify_receipt(a, altered)
    altered = copy.deepcopy(a)
    altered["source"]["commit"] = "other"
    with pytest.raises(ValueError, match="source pinned identity differs"):
        verify_receipt(a, altered)
    assert git_blob_sha(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a"


def test_pinned_source_receipt_has_positive_offered_cue_contrast_not_new_selection():
    path = (
        Path(__file__).resolve().parents[1]
        / "validation" / "bee_2026_random_free_cue_accuracy_v1.json"
    )
    frozen = json.loads(path.read_text(encoding="utf-8"))
    assert frozen["n_bees"] == 192
    assert frozen["n_trials"] == 19200
    assert frozen["source"]["blob_sha"] == (
        "26259c9071c6d73141d56b9bedd396cab1a04491"
    )
    assert frozen["free_cue_trials_per_bee_histogram"] == {"20": 192}
    for d in ("Easy", "Hard", "Impossible"):
        g = frozen["accuracy_by_difficulty"][d]
        assert g["paired_bees"] == 192
        assert g["free_minus_regular_accuracy"] > 0
        assert g["bee_cluster_bootstrap_95"][0] > 0
        assert g["bee_cluster_bootstrap_95"][1] > 0
    assert (
        frozen["status"]
        == "DESCRIPTIVE_RANDOM_FREE_CUE_POLICY_CONTRAST__CAUSAL_ITT_CONDITIONAL_ON_REPORTED_RANDOMIZATION"
    )
    assert "information-value" in frozen["claim_ceiling"]
    controls = frozen["free_arm_landing_accuracy_control"]["by_difficulty"]
    for d in ("Easy", "Hard", "Impossible"):
        ci = controls[d]["bee_cluster_bootstrap_95"]
        assert ci[0] < 0 < ci[1]
    assert frozen["free_arm_landing_accuracy_control"]["status"].endswith(
        "NOT_MOTOR_CAUSAL_EFFECT"
    )
