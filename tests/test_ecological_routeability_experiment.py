from adaptive_gain.ecological_routeability_experiment import (
    bypass_matched_control_task,
    ecological_routeability_experiment_contrast,
    experimental_stimulus_table,
)
from adaptive_gain.minimal_normal_form import minimal_strict_gain_standard_task


def test_experimental_contrast_is_exact_and_marginally_matched():
    receipt = ecological_routeability_experiment_contrast()

    assert receipt.routeable_adaptive_cost == 2
    assert receipt.routeable_fixed_cost == 3
    assert receipt.control_adaptive_cost == 2
    assert receipt.control_fixed_cost == 2
    assert receipt.same_world_count
    assert receipt.same_target_multiplicities
    assert receipt.same_query_outcome_multiplicities
    assert receipt.routeable_strict_gain
    assert not receipt.control_strict_gain
    assert receipt.routeable_fixed_terminal_accuracy == 0.75
    assert receipt.control_fixed_terminal_accuracy == 1.0
    assert receipt.routeable_adaptive_accuracy == 1.0
    assert receipt.control_adaptive_accuracy == 1.0
    assert receipt.exact_minimal_contrast


def test_routeable_stimulus_table_has_context_dependent_terminal_relevance():
    rows = experimental_stimulus_table(minimal_strict_gain_standard_task())
    by_state = {row["state"]: row for row in rows}

    assert by_state["w0"] == {
        "state": "w0",
        "target": 0,
        "q_left": 0,
        "q_route": 0,
        "q_right": 0,
    }
    assert by_state["w1"]["q_route"] == 1
    assert by_state["w2"]["q_route"] == 1
    assert by_state["w3"]["q_route"] == 0

    # route=0 branch: q_right separates the two targets.
    assert by_state["w0"]["q_right"] != by_state["w3"]["q_right"]
    assert by_state["w0"]["q_left"] == by_state["w3"]["q_left"]

    # route=1 branch: q_left separates the two targets.
    assert by_state["w1"]["q_left"] != by_state["w2"]["q_left"]
    assert by_state["w1"]["q_right"] == by_state["w2"]["q_right"]


def test_control_preserves_marginals_but_allows_route_bypass():
    routeable = experimental_stimulus_table(minimal_strict_gain_standard_task())
    control = experimental_stimulus_table(bypass_matched_control_task())

    for cue in ("q_left", "q_route", "q_right"):
        assert sorted(row[cue] for row in routeable) == sorted(
            row[cue] for row in control
        )

    # In the control, q_left + q_right already distinguish target classes.
    patterns = {}
    for row in control:
        pattern = (row["q_left"], row["q_right"])
        previous = patterns.setdefault(pattern, row["target"])
        assert previous == row["target"]
