"""Independent test of information/timing separation in moving-state ecology."""
import itertools
import math

import pytest

from adaptive_gain.selective_refresh import selective_refresh
from adaptive_gain.waiting_control import (
    waiting_control_decomposition,
    timing_adjusted_precision_window,
    timing_adjusted_log_maintenance_ceiling,
)


def _independent_schedule_values(
    alpha, beta, age, sample, terminal, hazard, r0, r1, cost,
    error_old, error_new,
):
    """Explicitly integrate latent old state, old report, refreshed state,
    refreshed report and final state; brute force terminal action maps."""
    p1 = alpha / (alpha + beta)
    priors = (1 - p1, p1)

    def state_probability(initial, t, final):
        p = p1 + (initial - p1) * math.exp(-(alpha + beta) * t)
        return p if final else 1 - p

    def report_probability(true_state, report, noise):
        return 1 - noise if true_state == report else noise

    def success(action, final):
        if action != final:
            return 0.0
        return r1 if final else r0

    weights = []
    choices = []
    for old_report in (0, 1):
        w = sum(
            priors[initial] * report_probability(
                initial, old_report, error_old)
            for initial in (0, 1)
        )
        weights.append(w)

        def expected_no_query(action, delay):
            return sum(
                priors[initial] *
                report_probability(initial, old_report, error_old) *
                state_probability(initial, age + delay, final) *
                success(action, final)
                for initial in (0, 1) for final in (0, 1)
            ) / w

        skip = math.exp(-hazard * terminal) * max(
            expected_no_query(action, terminal) for action in (0, 1)
        )
        wait = math.exp(-hazard * (sample + terminal)) * max(
            expected_no_query(action, sample + terminal)
            for action in (0, 1)
        )
        query = math.exp(-hazard * (sample + terminal)) * max(
            sum(
                priors[initial] *
                report_probability(initial, old_report, error_old) *
                state_probability(initial, age + sample, updated) *
                report_probability(updated, new_report, error_new) *
                state_probability(updated, terminal, final) *
                success(actions[new_report], final)
                for initial in (0, 1)
                for updated in (0, 1)
                for new_report in (0, 1)
                for final in (0, 1)
            ) / w
            for actions in itertools.product((0, 1), repeat=2)
        ) - cost
        choices.append((skip, wait, query))
    return tuple(weights), tuple(choices)


def test_uninformative_query_can_fake_a_timing_gain():
    kwargs = dict(
        cue_age=.1, sampling_delay=.15, terminal_delay=.15,
        opportunity_hazard=.25, reward0=1, reward1=4,
        query_cost=.015, old_cue_error_rate=0,
        refresh_cue_error_rate=.5,
    )
    x = waiting_control_decomposition(.8, .2, **kwargs)
    assert x.original_two_schedule_premium == pytest.approx(
        .03419976772047084, abs=1e-12
    )
    assert x.no_query_timing_policy == ("wait", "skip")
    assert x.conditional_query_policy == ("wait", "skip")
    assert x.query_access_gain == pytest.approx(0, abs=1e-12)
    assert x.conditional_query_premium == pytest.approx(0, abs=1e-12)
    assert x.timing_only_conditional_premium == pytest.approx(
        x.conditional_three_vs_fixed_three_gain, abs=1e-12
    )
    assert x.wait_without_cue_by_old_report == pytest.approx(
        tuple(q + .015 for q in x.query_with_cue_by_old_report),
        abs=1e-12,
    )
    assert x.gross_fresh_information_value_by_old_report == pytest.approx(
        (0, 0), abs=1e-12
    )


def test_canonical_information_value_window_shrinks_with_wait_control():
    common = dict(
        cue_age=1.2, sampling_delay=.15, terminal_delay=.1,
        opportunity_hazard=.25, reward0=1, reward1=1,
        query_cost=.03, old_cue_error_rate=0,
    )
    x = waiting_control_decomposition(
        .8, .2, refresh_cue_error_rate=.11398573555617236,
        **common
    )
    assert x.best_no_query_timing_reward == pytest.approx(
        .7817755643571999, abs=1e-12
    )
    assert x.conditional_query_premium == pytest.approx(
        .03928316234197882, abs=2e-8
    )
    assert x.original_two_schedule_premium == pytest.approx(
        .04081084255824451, abs=2e-8
    )
    assert x.conditional_query_premium < x.original_two_schedule_premium
    for err in (0, .5):
        z = waiting_control_decomposition(
            .8, .2, refresh_cue_error_rate=err, **common
        )
        assert z.conditional_query_premium == pytest.approx(0, abs=1e-12)


def test_full_independent_state_action_enumeration_grid():
    cases = 0
    for alpha, beta, reward0, reward1, age, old_err, fresh_err in itertools.product(
        (.2, .8), (.2, .8), (1., 4.), (1., 4.), (.1, 1.2),
        (0., .08), (0., .12, .5)
    ):
        args = dict(
            cue_age=age, sampling_delay=.15, terminal_delay=.1,
            opportunity_hazard=.25, reward0=reward0, reward1=reward1,
            query_cost=.03, old_cue_error_rate=old_err,
            refresh_cue_error_rate=fresh_err,
        )
        x = waiting_control_decomposition(alpha, beta, **args)
        weights, branches = _independent_schedule_values(
            alpha, beta, age, .15, .1, .25, reward0, reward1,
            .03, old_err, fresh_err
        )
        assert x.old_report_weights == pytest.approx(weights, abs=1e-12)
        assert x.skip_by_old_report == pytest.approx(
            tuple(item[0] for item in branches), abs=1e-12)
        assert x.wait_without_cue_by_old_report == pytest.approx(
            tuple(item[1] for item in branches), abs=1e-12)
        assert x.query_with_cue_by_old_report == pytest.approx(
            tuple(item[2] for item in branches), abs=1e-12)
        conditional = sum(
            weights[j] * max(*branches[j]) for j in (0, 1)
        )
        no_sensor = sum(
            weights[j] * max(branches[j][0], branches[j][1])
            for j in (0, 1)
        )
        universal_query = sum(
            weights[j] * branches[j][2] for j in (0, 1)
        )
        fixed_three = max(
            sum(weights[j] * branches[j][c] for j in (0, 1))
            for c in (0, 1, 2)
        )
        assert x.conditional_query_reward == pytest.approx(
            conditional, abs=1e-12)
        assert x.best_no_query_timing_reward == pytest.approx(
            no_sensor, abs=1e-12)
        assert x.query_access_gain == pytest.approx(
            conditional - no_sensor, abs=1e-12)
        assert x.conditional_query_premium == pytest.approx(
            conditional - max(no_sensor, universal_query), abs=1e-12)
        assert x.conditional_three_vs_fixed_three_gain == pytest.approx(
            conditional - fixed_three, abs=1e-12)
        cases += 1
    assert cases == 192


def test_uninformative_new_cue_has_zero_fresh_information_but_not_zero_waiting():
    for old_err, r0, r1, age in itertools.product(
        (0, .03, .1, .5), (1, 4), (1, 4), (.1, 1.2)
    ):
        x = waiting_control_decomposition(
            .8, .2, cue_age=age, sampling_delay=.15,
            terminal_delay=.15, opportunity_hazard=.25,
            reward0=r0, reward1=r1,
            query_cost=.015, old_cue_error_rate=old_err,
            refresh_cue_error_rate=.5,
        )
        assert x.query_access_gain == pytest.approx(0, abs=1e-12)
        assert x.conditional_query_premium == pytest.approx(0, abs=1e-12)
        assert x.gross_fresh_information_value_by_old_report == pytest.approx(
            (0, 0), abs=1e-12
        )


def test_conditional_information_premium_degrades_monotonically_in_absolute_reward():
    params = dict(
        alpha=.8, beta=.2, cue_age=1.2, sampling_delay=.15,
        terminal_delay=.1, opportunity_hazard=.25,
        reward0=1, reward1=1, query_cost=.03
    )
    old = None
    gains = []
    for j in range(101):
        x = waiting_control_decomposition(
            refresh_cue_error_rate=j/200, **params
        )
        if old is not None:
            for b, a in zip(old.query_with_cue_by_old_report,
                            x.query_with_cue_by_old_report):
                assert b + 1e-12 >= a
            assert old.conditional_query_reward + 1e-12 >= (
                x.conditional_query_reward
            )
        gains.append(x.conditional_query_premium)
        old = x
    assert gains[0] == pytest.approx(0, abs=1e-12)
    assert gains[-1] == pytest.approx(0, abs=1e-12)
    assert max(gains) > .0395



def test_matched_wait_precision_window_is_not_naive_two_schedule_window():
    kwargs = dict(
        alpha=.8, beta=.2, cue_age=1.2,
        sampling_delay=.15, terminal_delay=.1,
        opportunity_hazard=.25, reward0=1, reward1=1,
        query_cost=.03,
    )
    result = timing_adjusted_precision_window(**kwargs)
    assert result.lower_error == pytest.approx(
        .05652257923804355, abs=2e-8)
    assert result.upper_error == pytest.approx(
        .34238956740911564, abs=2e-8)
    assert result.peak_error == pytest.approx(
        .11225411408084168, abs=2e-8)
    assert result.peak_query_control_premium == pytest.approx(
        .039581029649796484, abs=2e-8)
    assert result.no_query_timing_reward_at_peak == pytest.approx(
        .7817755643571999, abs=2e-8)
    assert result.query_fixed_tie_at_peak
    assert not result.peak_on_boundary

    for error, has_information_schedule_premium in (
        (0, False), (.05, False), (.07, True), (.12, True),
        (.34, True), (.35, False), (.5, False)
    ):
        x = waiting_control_decomposition(
            refresh_cue_error_rate=error, **kwargs
        )
        assert (
            x.conditional_query_premium > 1e-10
        ) == has_information_schedule_premium

    cost = timing_adjusted_log_maintenance_ceiling(
        baseline_fitness=1, **kwargs
    )
    assert cost == pytest.approx(.021971229563271327, abs=1e-9)


def test_timing_adjusted_root_beats_finite_independent_grid():
    count = 0
    for alpha, beta, r0, r1, age, olderr in itertools.product(
        (.2, .8), (.2, .8), (1., 4.), (1., 4.),
        (.1, 1.2), (0., .08)
    ):
        kwargs = dict(
            alpha=alpha, beta=beta, cue_age=age,
            sampling_delay=.15, terminal_delay=.1,
            opportunity_hazard=.25, reward0=r0, reward1=r1,
            query_cost=.03, old_cue_error_rate=olderr,
        )
        optimum = timing_adjusted_precision_window(**kwargs)
        grid = [
            waiting_control_decomposition(
                refresh_cue_error_rate=j/100, **kwargs
            ).conditional_query_premium
            for j in range(51)
        ]
        if optimum.peak_error is None:
            assert max(grid) == pytest.approx(0, abs=1e-10)
        else:
            assert optimum.peak_query_control_premium + 1e-10 >= max(grid)
            assert (0 <= optimum.lower_error <= optimum.peak_error
                    <= optimum.upper_error <= .5)
        count += 1
    assert count == 64


def test_neither_query_nor_controller_can_be_preferred_when_old_cue_uninformative():
    kwargs = dict(
        alpha=.8, beta=.2, cue_age=.1,
        sampling_delay=.15, terminal_delay=.15,
        opportunity_hazard=.25, reward0=4,
        reward1=1, query_cost=.015,
        old_cue_error_rate=.5
    )
    cert = timing_adjusted_precision_window(**kwargs)
    assert cert.peak_error is None
    assert timing_adjusted_log_maintenance_ceiling(
        baseline_fitness=1, **kwargs
    ) == 0
    for eps in (0, .01, .2, .5):
        x = waiting_control_decomposition(
            refresh_cue_error_rate=eps, **kwargs
        )
        assert x.conditional_query_premium == pytest.approx(0, abs=1e-12)

    with pytest.raises(ValueError):
        timing_adjusted_precision_window(
            iterations=0, **kwargs
        )
    with pytest.raises(ValueError):
        timing_adjusted_precision_window(
            refresh_cue_error_rate=.1, **kwargs
        )
    with pytest.raises(ValueError):
        timing_adjusted_log_maintenance_ceiling(
            baseline_fitness=0, **kwargs
        )
