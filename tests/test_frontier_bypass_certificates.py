from dataclasses import replace
from itertools import product

from adaptive_gain.core import FiniteTask, Query, World, adaptive_minimum_resolution
from adaptive_gain.frontier_bypass_certificates import (
    frontier_replacement_certificate,
    selected_policy_no_external_shortcut_certificate,
    verify_frontier_replacement_certificate,
)
from adaptive_gain.frontier_decomposition import productive_frontier_policy_decomposition
from adaptive_gain.productive_frontier import ProductiveFrontierCertificate
from adaptive_gain.witnesses import (
    external_shortcut_control,
    internal_redundancy_control,
    mrod_routing_task,
    partial_external_bypass_gain_control,
    partial_internal_bypass_gain_control,
    payoff_routing_task,
    routing_bypass_control,
)


def test_set_valued_replacement_is_strictly_stronger_than_pairwise_replacement():
    # Edges are {a,x} and {b,x}; outside x costs 2.  Neither a nor b alone
    # replaces x, but the inside set {a,b} does at equal cost.
    frontier = ProductiveFrontierCertificate(
        ("a", "b", "x"),
        (1, 1, 2),
        (0b101, 0b110),
        (0b101, 0b110),
    )
    certificate = frontier_replacement_certificate(frontier, ("a", "b"))
    assert certificate.certified
    assert verify_frontier_replacement_certificate(frontier, certificate)
    assert len(certificate.replacements) == 1
    replacement = certificate.replacements[0]
    assert replacement.outside_query == "x"
    assert replacement.replacement_queries == ("a", "b")
    assert replacement.replacement_cost == replacement.outside_cost == 2

    tampered = replace(
        certificate,
        replacements=(replace(replacement, replacement_queries=("a",)),),
    )
    assert not verify_frontier_replacement_certificate(frontier, tampered)


def test_registered_no_external_controls_are_certified():
    for task in (
        mrod_routing_task(),
        payoff_routing_task(),
        routing_bypass_control(),
        internal_redundancy_control(),
        partial_internal_bypass_gain_control(),
    ):
        certificate = selected_policy_no_external_shortcut_certificate(task)
        assert certificate.certified
        decomposition = productive_frontier_policy_decomposition(task)
        assert decomposition.external_shortcut_discount == 0


def test_registered_external_shortcuts_are_not_falsely_certified():
    for task in (external_shortcut_control(), partial_external_bypass_gain_control()):
        certificate = selected_policy_no_external_shortcut_certificate(task)
        assert not certificate.certified
        decomposition = productive_frontier_policy_decomposition(task)
        assert decomposition.external_shortcut_discount == 1


def test_complete_balanced_four_world_three_query_universe_has_no_false_positive_certificate():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    patterns = tuple(product((0, 1), repeat=4))
    checked = resolved = certified = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        adaptive = adaptive_minimum_resolution(task)
        checked += 1
        if adaptive.minimum_worst_path_cost is None or adaptive.selected_policy is None:
            continue
        resolved += 1
        certificate = selected_policy_no_external_shortcut_certificate(task)
        if certificate.certified:
            certified += 1
            decomposition = productive_frontier_policy_decomposition(task)
            assert decomposition.external_shortcut_discount == 0
    assert checked == 16 ** 3 == 4_096
    assert resolved > 0
    assert certified > 0
