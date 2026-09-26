import pytest

from adaptive_gain.aedes_context_semantics import (
    aedes_context_semantics_receipt,
    aedes_preindexed_host_task,
    aedes_preindexed_oviposition_task,
)
from adaptive_gain.core import adaptive_gain_receipt


def test_preindexed_context_branches_have_zero_gap():
    host = adaptive_gain_receipt(aedes_preindexed_host_task(3))
    oviposition = adaptive_gain_receipt(aedes_preindexed_oviposition_task(5))
    assert host.adaptive_cost == host.fixed_cost == 3
    assert oviposition.adaptive_cost == oviposition.fixed_cost == 5
    assert host.strict_adaptive_gain is False
    assert oviposition.strict_adaptive_gain is False


def test_integrated_and_preindexed_context_semantics_diverge():
    receipt = aedes_context_semantics_receipt(2, 3, 5)
    assert receipt.integrated_adaptive_cost == 7
    assert receipt.integrated_fixed_cost == 10
    assert receipt.integrated_gap == 3
    assert receipt.host_branch_gap == 0
    assert receipt.oviposition_branch_gap == 0
    assert receipt.positive_gain_requires_within_architecture_state_use is True


def test_context_semantics_control_holds_over_positive_cost_grid():
    for state_cost in range(1, 5):
        for host_cost in range(1, 5):
            for oviposition_cost in range(1, 5):
                receipt = aedes_context_semantics_receipt(
                    state_cost,
                    host_cost,
                    oviposition_cost,
                )
                assert receipt.integrated_gap == min(host_cost, oviposition_cost)
                assert receipt.integrated_gap > 0
                assert receipt.host_branch_gap == 0
                assert receipt.oviposition_branch_gap == 0
                assert receipt.prospective_only is True


@pytest.mark.parametrize(
    "args",
    [
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (1.0, 1, 1),
    ],
)
def test_context_semantics_reject_invalid_costs(args):
    with pytest.raises(ValueError):
        aedes_context_semantics_receipt(*args)
