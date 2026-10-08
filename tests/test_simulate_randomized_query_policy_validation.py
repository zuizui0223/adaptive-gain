"""Regression tests for clustered null/alternative policy-validation simulation."""
import json
from dataclasses import asdict

import pytest

from scripts.simulate_randomized_query_policy_validation import (
    MIXED_PROBABILITIES, NULL_PROBABILITIES, TARGET,
    _values, repeated_assay,
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
    assert c.nominal_no_cluster_contingent_gain == pytest.approx(.04)
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
