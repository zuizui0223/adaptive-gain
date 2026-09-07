from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    pair_packing_lower_bound,
    selected_policy_pair_packing_gain_certificate,
    selected_policy_private_pair_gain_certificate,
)
from adaptive_gain.witnesses import (
    mrod_routing_task,
    partial_external_bypass_gain_control,
    partial_internal_bypass_gain_control,
    payoff_routing_task,
    routing_bypass_control,
)


def _private_pair_incomplete_strict_gain_task():
    return FiniteTask(
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


def test_pair_packing_certifies_registered_mrod_and_payoff_strict_gain_without_fixed_optimization():
    for task in (mrod_routing_task(), payoff_routing_task()):
        certificate = selected_policy_pair_packing_gain_certificate(task)
        assert certificate.adaptive_cost == 2
        assert certificate.required_fixed_lower_bound == 3
        assert certificate.strict_adaptive_gain_certified_without_fixed_optimization
        assert certificate.pair_packing is not None
        assert certificate.pair_packing.achieved_lower_bound >= 3
        assert all(load <= capacity for (_, load), (_, capacity) in zip(
            certificate.pair_packing.query_loads,
            certificate.pair_packing.query_capacities,
        ))


def test_pair_packing_strictly_generalizes_private_pair_certificate_on_five_world_control():
    task = _private_pair_incomplete_strict_gain_task()
    assert adaptive_gain_receipt(task).strict_adaptive_gain
    assert not selected_policy_private_pair_gain_certificate(task).strict_adaptive_gain_certified_without_fixed_optimization
    packing = selected_policy_pair_packing_gain_certificate(task)
    assert packing.strict_adaptive_gain_certified_without_fixed_optimization
    assert packing.pair_packing is not None
    assert packing.pair_packing.achieved_lower_bound == 3


def test_pair_packing_certifies_partial_internal_and_external_bypass_gain_controls():
    for task in (partial_internal_bypass_gain_control(), partial_external_bypass_gain_control()):
        actual = adaptive_gain_receipt(task)
        assert (actual.adaptive_cost, actual.fixed_cost) == (3, 4)
        certificate = selected_policy_pair_packing_gain_certificate(task)
        assert certificate.required_fixed_lower_bound == 4
        assert certificate.strict_adaptive_gain_certified_without_fixed_optimization
        assert certificate.pair_packing is not None
        assert certificate.pair_packing.achieved_lower_bound >= 4


def test_pair_packing_does_not_false_certify_routing_bypass_control():
    task = routing_bypass_control()
    assert not adaptive_gain_receipt(task).strict_adaptive_gain
    certificate = selected_policy_pair_packing_gain_certificate(task)
    assert certificate.adaptive_cost == 2
    assert certificate.required_fixed_lower_bound == 3
    assert not certificate.strict_adaptive_gain_certified_without_fixed_optimization
    assert certificate.pair_packing is not None
    assert certificate.pair_packing.exact_maximum_certified
    assert certificate.pair_packing.achieved_lower_bound == 2


def test_integral_packing_respects_nonunit_query_cost_capacities():
    task = FiniteTask(
        (World("a", 0), World("b", 0), World("c", 1), World("d", 1)),
        (
            Query("wide_capacity", 2, (0, 1, 0, 1)),
            Query("other", 1, (0, 0, 1, 0)),
        ),
    )
    packing = pair_packing_lower_bound(task)
    loads = dict(packing.query_loads)
    capacities = dict(packing.query_capacities)
    assert all(loads[name] <= capacities[name] for name in loads)
    assert packing.exact_maximum_certified
