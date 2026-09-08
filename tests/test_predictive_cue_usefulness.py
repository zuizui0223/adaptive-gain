import itertools

import pytest

from adaptive_gain.predictive_cue_usefulness import (
    adaptive_accuracy,
    best_adaptive_usefulness_probability,
    best_fixed_usefulness_probability,
    binary_jensen_gap_formula,
    common_optimal_specialists,
    fixed_accuracy,
    future_specialist_marginal,
    has_strict_routing_gain,
    optimal_adaptive_policy,
    optimal_fixed_specialist,
    routing_gain,
    summarize,
    symmetric_binary_gain,
)


def test_symmetric_binary_recovers_temporal_theorem():
    for rho in (0.0, 0.1, 0.25, 0.5, 0.8, 1.0):
        assert symmetric_binary_gain(rho) == pytest.approx(abs(2.0 * rho - 1.0) / 4.0)


def test_arbitrary_binary_kernel_matches_closed_form():
    prior = (0.7, 0.3)
    kernel = ((0.9, 0.1), (0.2, 0.8))
    assert routing_gain(prior, kernel) == pytest.approx(binary_jensen_gap_formula(prior, kernel))
    assert routing_gain(prior, kernel) > 0.0


def test_gain_zero_when_one_specialist_is_optimal_everywhere():
    prior = (0.4, 0.6)
    kernel = ((0.8, 0.2), (0.6, 0.4))
    assert common_optimal_specialists(prior, kernel) == (0,)
    assert routing_gain(prior, kernel) == pytest.approx(0.0)
    assert not has_strict_routing_gain(prior, kernel)


def test_zero_prior_rows_do_not_control_strictness():
    prior = (1.0, 0.0)
    kernel = ((0.8, 0.2), (0.1, 0.9))
    assert common_optimal_specialists(prior, kernel) == (0,)
    assert routing_gain(prior, kernel) == pytest.approx(0.0)


def test_three_specialist_jensen_gap_and_policy():
    prior = (0.2, 0.5, 0.3)
    kernel = (
        (0.8, 0.1, 0.1),
        (0.2, 0.7, 0.1),
        (0.1, 0.2, 0.7),
    )
    marginal = future_specialist_marginal(prior, kernel)
    assert marginal == pytest.approx((0.29, 0.43, 0.28))
    assert optimal_fixed_specialist(prior, kernel) == 1
    assert optimal_adaptive_policy(prior, kernel) == (0, 1, 2)
    assert best_fixed_usefulness_probability(prior, kernel) == pytest.approx(0.43)
    assert best_adaptive_usefulness_probability(prior, kernel) == pytest.approx(0.72)
    assert fixed_accuracy(prior, kernel) == pytest.approx(0.715)
    assert adaptive_accuracy(prior, kernel) == pytest.approx(0.86)
    assert routing_gain(prior, kernel) == pytest.approx(0.145)
    assert has_strict_routing_gain(prior, kernel)


def test_common_tied_specialist_is_exact_zero_gain_condition():
    prior = (0.5, 0.5)
    kernel = ((0.5, 0.5), (0.5, 0.5))
    assert common_optimal_specialists(prior, kernel) == (0, 1)
    assert routing_gain(prior, kernel) == pytest.approx(0.0)


def test_summary_is_self_consistent():
    prior = (0.55, 0.45)
    kernel = ((0.85, 0.15), (0.25, 0.75))
    s = summarize(prior, kernel)
    assert s.adaptive_accuracy - s.fixed_accuracy == pytest.approx(s.gain)
    assert s.gain == pytest.approx(binary_jensen_gap_formula(prior, kernel))
    assert s.adaptive_policy == (0, 1)
    assert s.common_optima == ()


def test_exhaustive_policy_search_matches_closed_form():
    prior = (0.2, 0.5, 0.3)
    kernel = (
        (0.6, 0.3, 0.1),
        (0.2, 0.7, 0.1),
        (0.15, 0.25, 0.60),
    )
    m = len(kernel[0])
    fixed_prob = max(sum(prior[i] * kernel[i][j] for i in range(len(prior))) for j in range(m))
    adaptive_prob = max(
        sum(prior[i] * kernel[i][policy[i]] for i in range(len(prior)))
        for policy in itertools.product(range(m), repeat=len(prior))
    )
    assert best_fixed_usefulness_probability(prior, kernel) == pytest.approx(fixed_prob)
    assert best_adaptive_usefulness_probability(prior, kernel) == pytest.approx(adaptive_prob)


@pytest.mark.parametrize(
    "prior,kernel",
    [
        ((), ((1.0,),)),
        ((0.4, 0.4), ((0.5, 0.5), (0.5, 0.5))),
        ((0.5, 0.5), ((0.5, 0.5),)),
        ((0.5, 0.5), ((0.6, 0.4), (0.2, 0.7))),
        ((0.5, 0.5), ((1.2, -0.2), (0.5, 0.5))),
    ],
)
def test_invalid_models_raise(prior, kernel):
    with pytest.raises(ValueError):
        routing_gain(prior, kernel)
