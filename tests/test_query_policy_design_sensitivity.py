"""Toy-only detection-sensitivity tests; no ecological power recommendation."""
import math
import pytest

from adaptive_gain.query_policy_design_sensitivity import (
    design_sensitivity,
    variance_balancing_old_zero_allocation,
)


TOY=dict(
    target_old_zero=.2,
    arm_probability_passive=1/3,
    arm_probability_query=1/3,
    success_passive_old_zero=.7,
    success_query_old_zero=.9,
    success_passive_old_one=.8,
    success_query_old_one=.75,
)


def test_rare_report_vs_common_report_contrast_bottleneck():
    out=design_sensitivity(laboratory_old_zero=.5,**TOY)
    assert out.conditional_minus_passive == pytest.approx(.04)
    assert out.conditional_minus_query == pytest.approx(.04)
    assert out.variance_coefficient_vs_passive == pytest.approx(.072)
    assert out.variance_coefficient_vs_query == pytest.approx(1.3344)
    assert out.approximate_total_trials_for_passive_contrast == 473
    assert out.approximate_total_trials_for_query_contrast == 8764
    assert out.approximate_total_trials_joint_bonferroni_bound == 8764
    assert out.binding_contrast == "query"


def test_oracle_nonuniform_old_report_design_is_only_toy_sensitivity():
    f0=variance_balancing_old_zero_allocation(**TOY)
    assert f0 == pytest.approx(.05119453924914674)
    balanced=design_sensitivity(laboratory_old_zero=f0,**TOY)
    assert balanced.approximate_total_trials_joint_bonferroni_bound == 4619
    assert abs(
        balanced.variance_coefficient_vs_passive/
        balanced.conditional_minus_passive**2 -
        balanced.variance_coefficient_vs_query/
        balanced.conditional_minus_query**2
    ) < 1e-9
    assert balanced.approximate_total_trials_joint_bonferroni_bound < 8764
    # These are still assumed true arm success rates, never empirical
    # estimates of required bees or colonies.


def test_variance_design_effect_doubles_illustrative_trial_burden():
    unclustered=design_sensitivity(laboratory_old_zero=.5,**TOY)
    inflated=design_sensitivity(
        laboratory_old_zero=.5,
        assumed_variance_design_effect=2,**TOY
    )
    assert inflated.approximate_total_trials_joint_bonferroni_bound == 17527
    assert inflated.approximate_total_trials_joint_bonferroni_bound > (
        unclustered.approximate_total_trials_joint_bonferroni_bound
    )


def test_invalid_probability_reward_and_wrong_policy_signs_are_rejected():
    with pytest.raises(ValueError,match="target_old_zero"):
        design_sensitivity(**dict(TOY,target_old_zero=0),laboratory_old_zero=.5)
    with pytest.raises(ValueError,match="SHAM"):
        design_sensitivity(**dict(
            TOY,arm_probability_passive=.6,arm_probability_query=.4
        ),laboratory_old_zero=.5)
    with pytest.raises(ValueError,match="does not beat both"):
        design_sensitivity(**dict(
            TOY,success_query_old_one=.95
        ),laboratory_old_zero=.5)
    with pytest.raises(ValueError,match="design_effect"):
        design_sensitivity(
            laboratory_old_zero=.5,
            assumed_variance_design_effect=.9,**TOY
        )
    with pytest.raises(ValueError,match="positive SHAM"):
        variance_balancing_old_zero_allocation(**dict(
            TOY,arm_probability_passive=.5,arm_probability_query=.5
        ))
