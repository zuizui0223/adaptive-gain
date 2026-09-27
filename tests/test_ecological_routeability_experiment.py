from adaptive_gain.ecological_routeability_experiment import (
    bypass_matched_control_task,
    ecological_routeability_experiment_contrast,
    experimental_stimulus_table,
    pairwise_information_signature,
    uniform_target_conditional_information_for_query,
    uniform_target_information_for_query_bundle,
    routeability_budget_information_ceilings,
    uniform_target_accuracy_for_context_policy,
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
    assert receipt.same_pairwise_information_signatures
    assert receipt.routeable_terminal_pair_target_information_bits == 0.5
    assert receipt.control_terminal_pair_target_information_bits == 1.0
    assert receipt.routeable_context_given_terminals_information_bits == 0.5
    assert receipt.control_context_given_terminals_information_bits == 0.0
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


def test_budget_ladder_localizes_architecture_by_access_interaction_to_b2():
    rows = {
        row.budget: row
        for row in routeability_budget_information_ceilings()
    }
    assert set(rows) == {1, 2, 3}

    b1 = rows[1]
    assert b1.routeable_adaptive_policy == 0.5
    assert b1.routeable_fixed_policy == 0.75
    assert b1.control_adaptive_policy == 0.5
    assert b1.control_fixed_policy == 0.75
    assert b1.architecture_by_access_interaction == 0.0

    b2 = rows[2]
    assert b2.routeable_adaptive_policy == 1.0
    assert b2.routeable_fixed_policy == 0.75
    assert b2.control_adaptive_policy == 1.0
    assert b2.control_fixed_policy == 1.0
    assert b2.architecture_by_access_interaction == 0.25

    b3 = rows[3]
    assert b3.routeable_adaptive_policy == 1.0
    assert b3.routeable_fixed_policy == 1.0
    assert b3.control_adaptive_policy == 1.0
    assert b3.control_fixed_policy == 1.0
    assert b3.architecture_by_access_interaction == 0.0


def test_same_context_routing_policy_solves_both_architectures():
    routeable = minimal_strict_gain_standard_task()
    control = bypass_matched_control_task()

    assert uniform_target_accuracy_for_context_policy(routeable) == 1.0
    assert uniform_target_accuracy_for_context_policy(control) == 1.0

    reverse_policy = {0: "q_left", 1: "q_right"}
    assert uniform_target_accuracy_for_context_policy(
        routeable,
        branch_queries=reverse_policy,
    ) < 1.0
    assert uniform_target_accuracy_for_context_policy(
        control,
        branch_queries=reverse_policy,
    ) < 1.0


def test_routeable_and_control_match_the_named_pairwise_information_surface():
    routeable = minimal_strict_gain_standard_task()
    control = bypass_matched_control_task()

    route_signature = pairwise_information_signature(routeable)
    control_signature = pairwise_information_signature(control)

    assert route_signature == control_signature
    assert len(route_signature) == 6

    by_pair = {
        (left, right): signature
        for left, right, signature in route_signature
    }
    assert by_pair[("target", "q_route")] == (1, 1, 1, 1)
    assert by_pair[("target", "q_left")] == (0, 2, 1, 1)
    assert by_pair[("target", "q_right")] == (0, 2, 1, 1)


def test_pairwise_information_matching_does_not_imply_equal_routeability():
    receipt = ecological_routeability_experiment_contrast()

    assert receipt.same_pairwise_information_signatures
    assert receipt.routeable_adaptive_cost == receipt.control_adaptive_cost == 2
    assert receipt.routeable_fixed_cost == 3
    assert receipt.control_fixed_cost == 2


def test_higher_order_information_pinpoints_the_bypass_difference():
    routeable = minimal_strict_gain_standard_task()
    control = bypass_matched_control_task()

    assert uniform_target_information_for_query_bundle(
        routeable, ("q_left", "q_right")
    ) == 0.5
    assert uniform_target_information_for_query_bundle(
        control, ("q_left", "q_right")
    ) == 1.0

    assert uniform_target_conditional_information_for_query(
        routeable,
        "q_route",
        given_query_names=("q_left", "q_right"),
    ) == 0.5
    assert uniform_target_conditional_information_for_query(
        control,
        "q_route",
        given_query_names=("q_left", "q_right"),
    ) == 0.0
