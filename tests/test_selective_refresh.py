"""Independent exhaustive validation of the dynamic selective re-query bridge."""
from __future__ import annotations

import itertools
import math

import pytest

from adaptive_gain.selective_refresh import selective_refresh


def _bruteforce(alpha, beta, age, sampling, terminal, hazard, r0, r1, cost):
    """Enumerate 4 refresh maps, 2 skip actions and 4 new-signal action maps."""
    prior1 = alpha / (alpha + beta)
    prior = (1 - prior1, prior1)

    def transition(start, lag, destination):
        p1 = prior1 + (start - prior1) * math.exp(-(alpha + beta) * lag)
        return p1 if destination else 1 - p1

    def payoff(action, final_state):
        if action != final_state:
            return 0
        return r0 if final_state == 0 else r1

    branch = []
    for old in (0, 1):
        skip = max(
            math.exp(-hazard * terminal) * sum(
                transition(old, age + terminal, final) * payoff(action, final)
                for final in (0, 1)
            )
            for action in (0, 1)
        )
        refresh = max(
            -cost + math.exp(-hazard * (sampling + terminal)) * sum(
                transition(old, age + sampling, new)
                * transition(new, terminal, final)
                * payoff(actions[new], final)
                for new in (0, 1) for final in (0, 1)
            )
            for actions in itertools.product((0, 1), repeat=2)
        )
        branch.append((skip, refresh))
    all_schedules = [
        sum(prior[old] * branch[old][schedule[old]] for old in (0, 1))
        for schedule in itertools.product((0, 1), repeat=2)
    ]
    return branch, all_schedules


def test_reward_weighting_reverses_which_old_cue_triggers_refresh():
    common = dict(
        alpha=.8, beta=.2, cue_age=.1, sampling_delay=.15,
        terminal_delay=.15, opportunity_hazard=.25, query_cost=.015,
    )
    equal = selective_refresh(reward0=1, reward1=1, **common)
    rare_high = selective_refresh(reward0=4, reward1=1, **common)
    assert equal.selective_policy == ("refresh", "skip")
    assert rare_high.selective_policy == ("skip", "refresh")
    assert equal.strict_conditional_gain == pytest.approx(.00606686422009628)
    assert rare_high.strict_conditional_gain == pytest.approx(.057835106128382385)


def test_independent_policy_enumeration_grid():
    count = 0
    for alpha, beta, r0, r1, age, sampling, terminal, hazard, cost in itertools.product(
        (.2, .8), (.2, .8), (1, 4), (1, 4), (.1, .8),
        (.1, .5), (.1, .5), (.05, .5), (0, .015),
    ):
        actual = selective_refresh(
            alpha, beta, cue_age=age, sampling_delay=sampling,
            terminal_delay=terminal, opportunity_hazard=hazard,
            reward0=r0, reward1=r1, query_cost=cost,
        )
        branches, policies = _bruteforce(
            alpha, beta, age, sampling, terminal, hazard, r0, r1, cost
        )
        assert actual.skip_by_old_cue == pytest.approx(
            tuple(x[0] for x in branches)
        )
        assert actual.refresh_by_old_cue == pytest.approx(
            tuple(x[1] for x in branches)
        )
        assert actual.selective_expected_reward == pytest.approx(max(policies))
        assert actual.best_precommitted_reward == pytest.approx(
            max(policies[0], policies[3])
        )
        assert actual.strict_conditional_gain == pytest.approx(
            max(policies) - max(policies[0], policies[3]), abs=1e-11
        )
        count += 1
    assert count == 512


def test_costly_refresh_can_be_rejected_in_both_branches():
    result = selective_refresh(
        .8, .2, cue_age=.1, sampling_delay=.15,
        terminal_delay=.15, opportunity_hazard=.25,
        reward0=4, reward1=1, query_cost=100,
    )
    assert result.selective_policy == ("skip", "skip")
    assert result.strict_conditional_gain == pytest.approx(0)


def test_old_cue_with_lost_predictivity_has_no_routing_gain():
    result = selective_refresh(
        .8, .2, cue_age=1000, sampling_delay=.15,
        terminal_delay=.15, opportunity_hazard=.25,
        reward0=1, reward1=1, query_cost=.015,
    )
    assert result.strict_conditional_gain == pytest.approx(0)


def test_state_relabeling_with_payoff_relabeling():
    kw = dict(
        cue_age=.1, sampling_delay=.15, terminal_delay=.15,
        opportunity_hazard=.25, query_cost=.015,
    )
    a = selective_refresh(.8, .2, reward0=4, reward1=1, **kw)
    b = selective_refresh(.2, .8, reward0=1, reward1=4, **kw)
    assert a.strict_conditional_gain == pytest.approx(b.strict_conditional_gain)
    assert a.selective_policy == tuple(reversed(b.selective_policy))


def test_zero_direct_action_value_does_not_eliminate_routing_value():
    # Stationary 80:20 occupancy, identical reward for correct 0/1 action.
    # Old cue at age 1.2 is too old to change the optimal terminal action:
    # both conditional probabilities for state 1 are >0.5 at age 1.2.
    age = 1.2
    assert age > math.log(8/3)
    p1_after_old_zero = .8 * (1 - math.exp(-age))
    p1_after_old_one = .8 + .2 * math.exp(-age)
    assert p1_after_old_zero > .5 and p1_after_old_one > .5

    result = selective_refresh(
        .8, .2, cue_age=age, sampling_delay=.15,
        terminal_delay=.15, opportunity_hazard=.25,
        reward0=1, reward1=1, query_cost=.1,
    )
    assert result.selective_policy == ("refresh", "skip")
    assert result.uniform_skip_reward == pytest.approx(.7705555341766576)
    assert result.uniform_refresh_reward == pytest.approx(.7863907607064166)
    assert result.selective_expected_reward == pytest.approx(.8104582955764174)
    assert result.strict_conditional_gain == pytest.approx(.024067534870000795)
    _, all_policies = _bruteforce(.8, .2, age, .15, .15, .25, 1, 1, .1)
    assert result.selective_expected_reward == pytest.approx(max(all_policies))


def test_exact_mixed_sign_characterization():
    # For branch gains d0, d1 and pi0, pi1 >0, gain over the best
    # precommitted schedule equals the smaller positive/negative-side
    # gain, and is strictly positive exactly when d0*d1 <0.
    for age, r0, r1, cost in itertools.product(
        (.01, .1, .5, 1., 1.2, 2., 5.),
        (1, 2, 4), (1, 2, 4), (0, .015, .1, .4),
    ):
        x = selective_refresh(
            .8, .2, cue_age=age, sampling_delay=.15,
            terminal_delay=.15, opportunity_hazard=.25,
            reward0=r0, reward1=r1, query_cost=cost,
        )
        d0 = x.refresh_by_old_cue[0] - x.skip_by_old_cue[0]
        d1 = x.refresh_by_old_cue[1] - x.skip_by_old_cue[1]
        expected_gap = min(
            max(.2*d0, 0) + max(.8*d1, 0),
            max(-.2*d0, 0) + max(-.8*d1, 0),
        )
        assert x.strict_conditional_gain == pytest.approx(
            expected_gap, abs=1e-12
        )
        if d0*d1 < -1e-9:
            assert x.strict_conditional_gain > 0


def test_local_243_case_stability_of_policy_reversal():
    count = 0
    for age, sampling, terminal, hazard, cost in itertools.product(
        (.08, .1, .12), (.13, .15, .17), (.13, .15, .17),
        (.22, .25, .28), (.013, .015, .017),
    ):
        common = dict(
            cue_age=age, sampling_delay=sampling,
            terminal_delay=terminal, opportunity_hazard=hazard,
            query_cost=cost,
        )
        equal = selective_refresh(.8, .2, reward0=1, reward1=1, **common)
        rare_high = selective_refresh(.8, .2, reward0=4, reward1=1, **common)
        assert equal.selective_policy == ("refresh", "skip")
        assert rare_high.selective_policy == ("skip", "refresh")
        assert equal.strict_conditional_gain > 0
        assert rare_high.strict_conditional_gain > 0
        count += 1
    assert count == 243


def test_noisy_old_cue_reversal_and_identifiability_limit():
    """Direction reversal survives modest noise, but is not universal."""
    baseline = dict(
        alpha=.8, beta=.2, cue_age=.1, sampling_delay=.15,
        terminal_delay=.15, opportunity_hazard=.25, query_cost=.015,
    )
    for error in (0, .01, .03, .05, .08):
        equal = selective_refresh(
            reward0=1, reward1=1, old_cue_error_rate=error, **baseline
        )
        rare_high = selective_refresh(
            reward0=4, reward1=1, old_cue_error_rate=error, **baseline
        )
        assert equal.selective_policy == ("refresh", "skip")
        assert rare_high.selective_policy == ("skip", "refresh")
        assert equal.strict_conditional_gain > 0
        assert rare_high.strict_conditional_gain > 0

    at_ten_percent = selective_refresh(
        reward0=4, reward1=1, old_cue_error_rate=.1, **baseline
    )
    assert at_ten_percent.selective_policy == ("refresh", "refresh")
    assert at_ten_percent.strict_conditional_gain == pytest.approx(0)

    for r0, r1 in ((1, 1), (4, 1)):
        uninformative = selective_refresh(
            reward0=r0, reward1=r1, old_cue_error_rate=.5, **baseline
        )
        assert uninformative.strict_conditional_gain == pytest.approx(0)
    with pytest.raises(ValueError):
        selective_refresh(
            reward0=1, reward1=1, old_cue_error_rate=.6, **baseline
        )


def test_independent_noisy_old_observation_and_state_path_enumeration():
    """Enumerate latent initial state, noisy report, refresh and final state."""
    up, down = .8, .2
    prior = (.2, .8)
    sampling, terminal, hazard, cost, age = .15, .15, .25, .015, .1
    r0, r1 = 4, 1

    def transition(start, elapsed, destination):
        p1 = .8 + (start - .8) * math.exp(-elapsed)
        return p1 if destination else 1 - p1

    for error in (0, .01, .05, .08, .1, .3, .5):
        def emit(observation, initial):
            return 1 - error if observation == initial else error

        branches, weights = [], []
        for observation in (0, 1):
            weight = sum(
                prior[z] * emit(observation, z) for z in (0, 1)
            )
            weights.append(weight)

            skip = max(
                math.exp(-hazard * terminal) * sum(
                    prior[z] * emit(observation, z)
                    * transition(z, age + terminal, final)
                    * ((r0 if final == 0 else r1) if action == final else 0)
                    for z in (0, 1) for final in (0, 1)
                ) / weight
                for action in (0, 1)
            )

            refresh = max(
                math.exp(-hazard * (sampling + terminal)) * sum(
                    prior[z] * emit(observation, z)
                    * transition(z, age + sampling, new)
                    * transition(new, terminal, final)
                    * ((r0 if final == 0 else r1)
                       if policy[new] == final else 0)
                    for z in (0, 1)
                    for new in (0, 1)
                    for final in (0, 1)
                ) / weight - cost
                for policy in itertools.product((0, 1), repeat=2)
            )
            branches.append((skip, refresh))

        values = [
            sum(
                weights[old] * branches[old][schedule[old]]
                for old in (0, 1)
            )
            for schedule in itertools.product((0, 1), repeat=2)
        ]
        actual = selective_refresh(
            up, down, cue_age=age, sampling_delay=sampling,
            terminal_delay=terminal, opportunity_hazard=hazard,
            reward0=r0, reward1=r1, query_cost=cost,
            old_cue_error_rate=error,
        )
        assert actual.selective_expected_reward == pytest.approx(max(values))
        assert actual.best_precommitted_reward == pytest.approx(
            max(values[0], values[3])
        )
