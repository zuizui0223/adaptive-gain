"""Independent tests of the Blackwell-ordered adaptive-premium envelope."""
import itertools
import math

import pytest

from adaptive_gain.ordered_accuracy_window import precision_window
from adaptive_gain.selective_refresh import selective_refresh


def test_exact_witness_window_peak_and_comparator_indifference():
    params = dict(
        alpha=.8, beta=.2, cue_age=1.2, sampling_delay=.15,
        terminal_delay=.1, opportunity_hazard=.25,
        reward0=1, reward1=1, query_cost=.03,
    )
    cert = precision_window(**params)
    assert cert.lower_error == pytest.approx(.05652257923804, abs=2e-8)
    assert cert.upper_error == pytest.approx(.35127167369242, abs=2e-8)
    assert cert.peak_error == pytest.approx(.114, abs=.002)
    assert cert.peak_conditional_premium > .0408
    assert cert.comparator_tie_at_peak
    assert not cert.peak_on_boundary

    at_peak = selective_refresh(
        refresh_cue_error_rate=cert.peak_error, **params
    )
    assert at_peak.uniform_skip_reward == pytest.approx(
        at_peak.uniform_refresh_reward, abs=1e-9
    )
    assert cert.peak_conditional_premium == pytest.approx(
        at_peak.strict_conditional_gain
    )
    assert at_peak.selective_policy == ("refresh", "skip")


def test_noisy_old_cue_error_fifty_per_cent_has_no_conditional_premium():
    cert = precision_window(
        alpha=.8, beta=.2, cue_age=.1,
        sampling_delay=.15, terminal_delay=.15,
        opportunity_hazard=.25, reward0=4, reward1=1,
        query_cost=.015, old_cue_error_rate=.5,
    )
    assert cert.lower_error is None
    assert cert.upper_error is None
    assert cert.peak_error is None
    assert cert.peak_conditional_premium == 0


def test_phase_window_optimum_dominates_independent_dense_grid():
    """Exhaustive numeric grid versus bisection in varied ecological scopes."""
    case_count = 0
    for alpha, beta, reward0, reward1, age, old_err in itertools.product(
        (.2, .8), (.2, .8), (1, 4), (1, 4), (.1, 1.2), (0, .08)
    ):
        params = dict(
            alpha=alpha, beta=beta, cue_age=age,
            sampling_delay=.15, terminal_delay=.1,
            opportunity_hazard=.25,
            reward0=reward0, reward1=reward1,
            query_cost=.03, old_cue_error_rate=old_err,
        )
        cert = precision_window(**params)
        grid = [
            selective_refresh(refresh_cue_error_rate=j/200, **params)
            for j in range(101)
        ]
        values = [z.strict_conditional_gain for z in grid]
        if cert.peak_error is None:
            assert max(values) < 1e-10
        else:
            assert cert.peak_conditional_premium + 1e-9 >= max(values)
            assert 0 <= cert.lower_error <= cert.peak_error <= cert.upper_error <= .5
        case_count += 1
    assert case_count == 64


def test_direct_branch_ordering_implies_single_peak_for_multiple_reports():
    """Test general theorem with 3+ old reports, not only binary ecology."""
    for offsets in itertools.product((-.4, -.1, .1, .3), repeat=3):
        weights = (.2, .3, .5)
        # Each branch advantage d_i is nonincreasing in sensor imprecision.
        curves = [
            [offset - (0.2 + i*.3)*j/100 for j in range(101)]
            for i, offset in enumerate(offsets)
        ]
        premiums = []
        for j in range(101):
            positive = sum(
                weights[i] * max(curves[i][j], 0) for i in range(3)
            )
            negative = sum(
                weights[i] * max(-curves[i][j], 0) for i in range(3)
            )
            premiums.append(min(positive, negative))
        # no decrease followed by an increase (flat plateaus allowed)
        seen_decline = False
        for previous, now in zip(premiums, premiums[1:]):
            if now < previous - 1e-10:
                seen_decline = True
            if seen_decline:
                assert now <= previous + 1e-10


def test_interval_and_root_validation():
    baseline = dict(
        alpha=.8, beta=.2, cue_age=1.2,
        sampling_delay=.15, terminal_delay=.1,
        opportunity_hazard=.25, reward0=1, reward1=1, query_cost=.03,
    )
    with pytest.raises(ValueError):
        precision_window(iterations=0, **baseline)
    with pytest.raises(ValueError):
        precision_window(refresh_cue_error_rate=.1, **baseline)

    cert = precision_window(**baseline)
    for eps, positive in (
        (cert.lower_error - .001, False),
        (cert.lower_error + .001, True),
        (cert.upper_error - .001, True),
        (cert.upper_error + .001, False),
    ):
        assert (selective_refresh(
            refresh_cue_error_rate=eps, **baseline
        ).strict_conditional_gain > 1e-12) == positive
