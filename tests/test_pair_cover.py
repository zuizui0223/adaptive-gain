from itertools import product

from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    adaptive_minimum_resolution,
    optimal_policy_cost_decomposition,
    pair_cover_audit,
    private_pair_no_bypass_certificate,
    restricted_fixed_minimum_resolution,
    selected_policy_private_pair_gain_certificate,
)
from adaptive_gain.witnesses import (
    external_shortcut_control,
    internal_redundancy_control,
    mrod_routing_task,
    payoff_routing_task,
    routing_bypass_control,
)


def _selected_union(task):
    policy = adaptive_minimum_resolution(task).selected_policy
    assert policy is not None
    names = set()
    stack = [policy]
    while stack:
        node = stack.pop()
        if node.query is None:
            continue
        names.add(node.query)
        stack.extend(child for _, child in node.branches)
    order = {query.name: i for i, query in enumerate(task.queries)}
    return tuple(sorted(names, key=order.__getitem__))


def test_registered_positive_witnesses_have_global_private_pair_no_bypass_certificate():
    for task in (mrod_routing_task(), payoff_routing_task()):
        union = _selected_union(task)
        audit = pair_cover_audit(task)
        certificate = private_pair_no_bypass_certificate(task, union)
        gain_certificate = selected_policy_private_pair_gain_certificate(task)
        decomposition = optimal_policy_cost_decomposition(task)
        assert audit.all_cross_target_pairs_separable
        assert set(union) <= set(audit.globally_essential_queries)
        assert certificate.no_fixed_bypass_certified
        assert gain_certificate.strict_adaptive_gain_certified_without_fixed_optimization
        assert gain_certificate.branch_exclusive_overhead == 1
        assert decomposition.private_pair_no_bypass_certified
        assert decomposition.every_union_query_globally_mandatory
        assert decomposition.policy_union_restricted_fixed_cost == 3
        assert decomposition.internal_union_redundancy == 0
        assert decomposition.external_shortcut_discount == 0
        assert decomposition.realized_adaptive_gain == 1


def test_routing_bypass_control_is_internal_union_redundancy():
    task = routing_bypass_control()
    d = optimal_policy_cost_decomposition(task)
    assert (d.adaptive_cost, d.fixed_cost, d.policy_union_cost) == (2, 2, 3)
    assert d.policy_union_restricted_fixed_cost == 2
    assert d.internal_union_redundancy == 1
    assert d.external_shortcut_discount == 0
    assert d.fixed_bypass_discount == 1
    assert d.realized_adaptive_gain == 0
    assert d.three_way_identity_holds
    assert not d.private_pair_no_bypass_certified
    assert not selected_policy_private_pair_gain_certificate(task).strict_adaptive_gain_certified_without_fixed_optimization


def test_external_shortcut_control_separates_external_from_internal_bypass():
    task = external_shortcut_control()
    d = optimal_policy_cost_decomposition(task)
    assert (d.adaptive_cost, d.fixed_cost, d.policy_union_cost) == (2, 2, 3)
    assert d.policy_union_restricted_fixed_cost == 3
    assert d.internal_union_redundancy == 0
    assert d.external_shortcut_discount == 1
    assert d.fixed_bypass_discount == 1
    assert d.realized_adaptive_gain == 0
    assert d.three_way_identity_holds
    assert not d.private_pair_no_bypass_certified


def test_internal_redundancy_control_has_no_external_shortcut_discount():
    task = internal_redundancy_control()
    d = optimal_policy_cost_decomposition(task)
    assert (d.adaptive_cost, d.fixed_cost, d.policy_union_cost) == (2, 2, 3)
    assert d.policy_union_restricted_fixed_cost == 2
    assert d.internal_union_redundancy == 1
    assert d.external_shortcut_discount == 0
    assert d.realized_adaptive_gain == 0


def test_restricted_fixed_optimum_can_be_strictly_more_expensive_than_global_fixed_optimum():
    task = external_shortcut_control()
    union = _selected_union(task)
    restricted = restricted_fixed_minimum_resolution(task, union)
    assert restricted.minimum_cost == 3
    assert optimal_policy_cost_decomposition(task).fixed_cost == 2


def test_private_pair_certificate_is_sufficient_not_necessary_for_no_bypass():
    # Strict gain can have C_F=U without one union query owning a globally private
    # pair.  The fixed lower bound can be combinatorial rather than single-pair.
    task = FiniteTask(
        (
            World("w0", 0), World("w1", 0),
            World("w2", 1), World("w3", 1), World("w4", 1),
        ),
        (
            Query("q0", 1, (1, 0, 0, 0, 1)),
            Query("q1_alt", 1, (0, 1, 1, 1, 0)),
            Query("q2", 1, (0, 0, 1, 1, 0)),
            Query("q3", 1, (1, 0, 1, 0, 0)),
        ),
    )
    d = optimal_policy_cost_decomposition(task)
    cert = selected_policy_private_pair_gain_certificate(task)
    assert (d.adaptive_cost, d.fixed_cost, d.policy_union_cost) == (2, 3, 3)
    assert d.policy_union_restricted_fixed_cost == 3
    assert d.fixed_bypass_discount == 0
    assert not d.private_pair_no_bypass_certified
    assert not cert.strict_adaptive_gain_certified_without_fixed_optimization


def test_private_pair_gain_certificate_is_complete_in_minimal_balanced_four_world_three_query_universe():
    targets = (0, 0, 1, 1)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    patterns = tuple(product((0, 1), repeat=4))
    strict = certified = false_positive = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, outcomes) for j, outcomes in enumerate(maps)),
        )
        actual = adaptive_gain_receipt(task).strict_adaptive_gain
        certificate = selected_policy_private_pair_gain_certificate(task)
        predicted = certificate.strict_adaptive_gain_certified_without_fixed_optimization
        strict += int(actual)
        certified += int(predicted)
        false_positive += int(predicted and not actual)
    assert strict == 192
    assert certified == 192
    assert false_positive == 0
