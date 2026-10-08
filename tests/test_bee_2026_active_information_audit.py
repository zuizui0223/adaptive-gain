"""Offline regression checks for the published 2026 bumblebee source schema.

Unit tests use miniature synthetic records. No third-party raw data are
embedded in or downloaded by the CI suite. A frozen aggregate receipt is
checked for internal accounting consistency.
"""
import csv
import io
import json
from pathlib import Path

import pytest

from scripts.audit_bee_2026_active_information import (
    parse_trials, summarize_trials, xorshift32,
)


CSV_HEADER = (
    "Trial_ID,Bee_ID,Trial_Number,Difficulty,Trial_Type,"
    "Info_Requested,Actually_Landed_On_Platform,"
    "Post_Request_Accuracy,Is_Post_Request_Correct,"
    "Non_Request_Accuracy,Is_Post_Non_Request_Correct\n"
)


def _example():
    lines=[CSV_HEADER]
    idn=0
    for bee in ("Bee_001","Bee_002","Bee_003"):
        for difficulty in ("Easy","Hard","Impossible"):
            for trial_type in ("Regular","Random_Free_Cue"):
                idn+=1
                active=int(difficulty=="Impossible" if trial_type=="Regular"
                           else bee!="Bee_002")
                received=active if trial_type=="Regular" else 1
                lines.append(
                    f"{idn},{bee},{idn},{difficulty},{trial_type},"
                    f"{received},{active},,,,\n"
                )
    return io.StringIO("".join(lines))


def test_free_cue_delivery_is_not_platform_landing():
    rows=parse_trials(_example())
    out=summarize_trials(rows,bootstrap_repetitions=25)
    assert out["n_trials"]==18
    assert out["n_bees"]==3
    assert out["per_bee_trial_count_min"]==6
    assert out["per_bee_trial_count_max"]==6
    assert out["request_landing_disagreements"]["Regular"]==0
    assert out["request_landing_disagreements"]["Random_Free_Cue"]==3
    assert out["groups"]["Random_Free_Cue|Easy"]["info"]==3
    assert out["groups"]["Random_Free_Cue|Easy"]["land"]==2
    assert out["groups"]["Regular|Easy"]["info"]==0
    assert out["within_bee_differences"]["Easy"]["n_paired"]==3
    assert out["within_bee_differences"]["Easy"]["positive"]==2
    assert out["within_bee_differences"]["Easy"]["negative"]==0


def test_all_trial_ids_are_unique_and_binary_flags_required():
    raw=_example().getvalue()
    rows=raw.splitlines()
    repeated="\n".join([rows[0],rows[1],rows[1]])+"\n"
    with pytest.raises(ValueError,match="duplicate Trial_ID"):
        parse_trials(io.StringIO(repeated))
    corrupt=raw.replace(",0,0,,,,",",2,0,,,,",1)
    with pytest.raises(ValueError,match="Info_Requested"):
        parse_trials(io.StringIO(corrupt))


def test_bootstrap_reproducible_under_same_seed():
    rows=parse_trials(_example())
    first=summarize_trials(rows,bootstrap_repetitions=75,seed=0x8E4C19)
    second=summarize_trials(rows,bootstrap_repetitions=75,seed=0x8E4C19)
    assert first["landing_comparisons"]==second["landing_comparisons"]
    with pytest.raises(ValueError):
        summarize_trials(rows,bootstrap_repetitions=0)
    g=xorshift32(0x8E4C19)
    assert all(0<=next(g)<1 for _ in range(100))


def test_frozen_third_party_trial_receipt_is_internally_consistent():
    receipt=json.loads(
        Path("validation/bee_2026_active_information_schema_audit_v1.json")
        .read_text(encoding="utf-8")
    )
    groups=receipt["groups"]
    c=receipt["contract"]
    assert c["n_trials"]==19200
    assert c["n_bees"]==192
    assert sum(x["n"] for x in groups.values())==c["n_trials"]
    assert sum(x["land"] for k,x in groups.items() if k.startswith("Regular|"))==5686
    assert sum(x["info"] for k,x in groups.items() if k.startswith("Random_Free_Cue|"))==3840
    assert sum(x["n"]-x["land"] for k,x in groups.items()
               if k.startswith("Random_Free_Cue|"))==1812
    assert sum(x["n"] for k,x in groups.items()
               if k.startswith("Random_Free_Cue|"))==3840
    assert sum(x["n"] for k,x in groups.items()
               if k.startswith("Regular|"))==15360
    assert all(groups["Regular|"+d]["info"]==groups["Regular|"+d]["land"]
               for d in ("Easy","Hard","Impossible"))
    for difficulty,stats in receipt["comparison"].items():
        if difficulty=="method":
            continue
        regular=groups["Regular|"+difficulty]
        free=groups["Random_Free_Cue|"+difficulty]
        expected=free["land"]/free["n"]-regular["land"]/regular["n"]
        assert stats["difference"]==pytest.approx(expected,abs=1e-12)
        assert stats["bootstrap95"][0]<expected<stats["bootstrap95"][1]
    paired = receipt["within_bee_paired_landing_differences"]
    for diff in ("Easy", "Hard", "Impossible"):
        assert paired[diff]["n_paired"] == 192
        assert paired[diff]["n_missing"] == 0
        assert (
            paired[diff]["positive"]
            + paired[diff]["negative"]
            + paired[diff]["zero"]
        ) == 192
    assert paired["Easy"]["positive"] == 190
    assert paired["Impossible"]["negative"] == 178
    assert receipt["source"]["blob_sha"] == (
        "26259c9071c6d73141d56b9bedd396cab1a04491"
    )
