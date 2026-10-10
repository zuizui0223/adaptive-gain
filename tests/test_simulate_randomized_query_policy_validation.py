"""Regression tests for clustered null/alternative policy-validation simulation."""
import json
from dataclasses import asdict

import pytest

from scripts.simulate_randomized_query_policy_validation import (
    MIXED_PROBABILITIES, NULL_PROBABILITIES, TARGET,
    _values, repeated_assay, _marginal_probabilities,
)


def test_true_table_can_have_zero_unconditional_query_effect_but_positive_policy_gain():
    assert TARGET == (.2, .8)
    assert _values(NULL_PROBABILITIES,(2,0)) == pytest.approx((0,0,0))
    assert _values(MIXED_PROBABILITIES,(2,0)) == pytest.approx((.04,.04,.04))
    # If both regimes are equal within both old-report branches, the
    # apparent adaptive gain is a train-set optimization artifact.
    for policy in ((0,0),(2,2),(0,2),(2,0)):
        assert _values(NULL_PROBABILITIES,policy)[2] == pytest.approx(0)


def test_monte_carlo_deterministic_and_heldout_split_respected():
    args=dict(repetitions=12,bootstrap_draws=25,clusters_train=8,
              clusters_heldout=8,trials_per_cell=4,colony_logit_sd=.55,seed=521)
    a=repeated_assay(scenario="null",**args)
    b=repeated_assay(scenario="null",**args)
    c=repeated_assay(scenario="mixed",**args)
    assert a == b
    assert a.nominal_no_cluster_contingent_gain == pytest.approx(0)
    assert a.marginal_cluster_contingent_gain == pytest.approx(0,abs=1e-12)
    assert not a.marginal_cluster_policy_is_mixed
    assert c.nominal_no_cluster_contingent_gain == pytest.approx(.04)
    assert c.marginal_cluster_contingent_gain > .035
    assert c.marginal_cluster_policy_is_mixed
    assert a.clusters_train==8
    assert a.clusters_heldout==8
    assert a.trials_per_cluster==24
    assert a.repetitions==12
    assert a.bootstrap_draws_per_repetition==25
    for x in (a,c):
        for p in (
            x.fraction_naive_training_gain_positive,
            x.fraction_heldout_gain_positive,
            x.fraction_joint_lower_bounds_both_positive,
            x.fraction_training_learned_mixed_policy,
            x.fraction_training_learned_correct_mixed_policy,
        ):
            assert 0<=p<=1
        assert x.mean_heldout_gain <= min(
            x.mean_heldout_conditional_minus_passive,
            x.mean_heldout_conditional_minus_query
        ) + 1e-12
        payload=json.dumps(asdict(x),allow_nan=False)
        assert "SYNTHETIC_POLICY_VALIDATION_CALIBRATION" in payload


def test_one_report_missing_values_and_invalid_sampling_design_rejected():
    with pytest.raises(ValueError,match="scenario"):
        repeated_assay(scenario="unknown",repetitions=1,bootstrap_draws=20)
    with pytest.raises(ValueError,match=">=4"):
        repeated_assay(scenario="null",clusters_heldout=2,repetitions=1)
    with pytest.raises(ValueError,match="nonnegative"):
        repeated_assay(scenario="null",colony_logit_sd=-.1,repetitions=1)
    with pytest.raises(ValueError,match="positive integers"):
        repeated_assay(scenario="null",trials_per_cell=0,repetitions=1)



def test_marginal_colony_mixture_reduces_but_does_not_erase_toy_value():
    assert _marginal_probabilities(MIXED_PROBABILITIES, 0)==MIXED_PROBABILITIES
    marginal=_marginal_probabilities(MIXED_PROBABILITIES, .55)
    assert marginal[0][0] == pytest.approx(.6885752044439802,abs=2e-6)
    assert marginal[0][2] == pytest.approx(.8892301228380588,abs=2e-6)
    assert marginal[1][0] == pytest.approx(.7864460434604592,abs=2e-6)
    assert marginal[1][2] == pytest.approx(.7370374490766479,abs=2e-6)
    assert _values(marginal,(2,0))[2] == pytest.approx(
        .03952687550704903,abs=2e-6
    )
    # TRUE population-marginal gain under the assumed colony mixture
    # differs from the nominal 0.04 at zero random intercept.
