"""Check strict old-report mixture and control-maintenance inversion."""
import math

import pytest

from adaptive_gain.conditional_policy_transport import (
    conditional_frequency_gain, mixture_viability_window,
)


def test_exact_constructed_old_report_mixture_optimum_and_cost_window():
    a,b=.20,.05
    w=mixture_viability_window(
        query_advantage_given_old_zero=a,
        passive_advantage_given_old_one=b,
        additional_controller_cost=.01,
    )
    assert w.target_probability_at_maximum==pytest.approx(.20)
    assert w.maximum_gain==pytest.approx(.04)
    assert w.strictly_profitable_old_zero_frequency_interval == pytest.approx(
        (.05,.8)
    )
    for x, expected in ((.01,.002),(.05,.01),(.2,.04),
                        (.50,.025),(.8,.01),(.9,.005),(.95,.0025)):
        g=conditional_frequency_gain(
            old_zero_probability=x,
            query_advantage_given_old_zero=a,
            passive_advantage_given_old_one=b,
        )
        assert g.extra_reward_over_best_fixed==pytest.approx(expected)
        assert g.extra_reward_over_best_fixed==pytest.approx(
            min(g.extra_reward_over_always_passive,
                g.extra_reward_over_always_query)
        )
    assert conditional_frequency_gain(
        old_zero_probability=.2,
        query_advantage_given_old_zero=a,
        passive_advantage_given_old_one=b
    ).extra_reward_over_best_fixed == pytest.approx(w.maximum_gain)


def test_exact_global_frequency_peak_over_dense_grid():
    for a,b in ((.2,.05),(.05,.2),(1,1),(.001,.8),(.6,.3)):
        window=mixture_viability_window(
            query_advantage_given_old_zero=a,
            passive_advantage_given_old_one=b,
            additional_controller_cost=0,
        )
        grid=[
            conditional_frequency_gain(
                old_zero_probability=i/1000,
                query_advantage_given_old_zero=a,
                passive_advantage_given_old_one=b
            ).extra_reward_over_best_fixed
            for i in range(1001)
        ]
        assert max(grid)<=window.maximum_gain+1e-12
        assert grid[0]==pytest.approx(0)
        assert grid[-1]==pytest.approx(0)
        assert window.target_probability_at_maximum>0
        assert window.target_probability_at_maximum<1


def test_cost_equal_to_or_above_maximum_gives_no_viable_report_mixture():
    for cost in (.04,.041,.1):
        x=mixture_viability_window(
            query_advantage_given_old_zero=.2,
            passive_advantage_given_old_one=.05,
            additional_controller_cost=cost
        )
        assert x.strictly_profitable_old_zero_frequency_interval is None
    for k in (-.01,float("nan"),float("inf")):
        with pytest.raises(ValueError):
            mixture_viability_window(
                query_advantage_given_old_zero=.2,
                passive_advantage_given_old_one=.05,
                additional_controller_cost=k
            )


def test_reweighting_is_not_changing_markov_stationary_distribution():
    """At equal branch kernels, target report prevalence shifts the same
    conditional policy from viable to nonviable. Ecological state process
    itself is explicitly *not* held fixed by a natural-history change.
    """
    w=.2
    crit=mixture_viability_window(
        query_advantage_given_old_zero=.2,
        passive_advantage_given_old_one=.05,
        additional_controller_cost=.01)
    assert crit.strictly_profitable_old_zero_frequency_interval[0]<w
    assert w<crit.strictly_profitable_old_zero_frequency_interval[1]
    assert "old-REPORT" in crit.interpretation
    assert conditional_frequency_gain(
        old_zero_probability=.01,
        query_advantage_given_old_zero=.2,
        passive_advantage_given_old_one=.05,
    ).extra_reward_over_best_fixed < .01
    for bad in (-.1,1.1,float("nan")):
        with pytest.raises(ValueError,match="old_zero_probability"):
            conditional_frequency_gain(
                old_zero_probability=bad,
                query_advantage_given_old_zero=.2,
                passive_advantage_given_old_one=.05,
            )
    with pytest.raises(ValueError,match="strictly positive"):
        mixture_viability_window(
            query_advantage_given_old_zero=0,
            passive_advantage_given_old_one=.05,
            additional_controller_cost=0,
        )



def test_zero_controller_cost_retains_arbitrarily_small_positive_gain():
    very_small=mixture_viability_window(
        query_advantage_given_old_zero=1e-12,
        passive_advantage_given_old_one=1e-12,
        additional_controller_cost=0.,
    )
    assert very_small.maximum_gain==pytest.approx(5e-13,abs=1e-26)
    assert very_small.strictly_profitable_old_zero_frequency_interval == (0.,1.)
