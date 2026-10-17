"""Exact all-correlation maintenance threshold for the finite five-world example.

The proof enumerates *joint* endpoint reward lines of every deterministic
acquisition tree and terminal action, independently of the production solver.
A line is an (independent-channel value, shared-channel value) pair; mixing
channels with weight rho makes each fixed policy's reward affine in rho.
This small exact certificate is a benchmark result, not a universal theorem.
"""
from fractions import Fraction as F
from itertools import combinations, product
from functools import lru_cache

import pytest


TARGETS = (0, 1, 1, 0, 0)
CUES = (
    (0, 0, 1, 1, 0),
    (0, 1, 0, 0, 0),
    (0, 0, 0, 1, 0),
)
PRIOR = (F(1, 3),) + (F(1, 6),) * 4
EPS = F(1, 10)
LOSS = F(4)
K = F(1, 10)


@lru_cache(None)
def all_query_trees(remaining, budget):
    results = [None]
    if budget:
        for j in remaining:
            available = tuple(k for k in remaining if k != j)
            for left, right in product(all_query_trees(available, budget - 1), repeat=2):
                results.append((j, left, right))
    return tuple(results)


def path(tree, bits):
    out = []
    while tree is not None:
        j, left, right = tree
        out.append((j, bits[j]))
        tree = right if bits[j] else left
    return tuple(out)


def channel_mass(shared):
    if shared:
        error_law = {(0, 0, 0): 1 - EPS, (1, 1, 1): EPS}
    else:
        error_law = {
            err: EPS ** sum(err) * (1 - EPS) ** (3 - sum(err))
            for err in product((0, 1), repeat=3)
        }
    rows = []
    for i, target in enumerate(TARGETS):
        for err, p_err in error_law.items():
            perceived = tuple(CUES[j][i] ^ err[j] for j in range(3))
            rows.append((target, perceived, PRIOR[i] * p_err))
    assert sum((mass for _, _, mass in rows), F(0)) == 1
    return rows


INDEPENDENT_ROWS = channel_mass(False)
SHARED_ROWS = channel_mass(True)


def attainable_reward_lines(grouping):
    # Pool correct- and wrong-target masses separately in each noise channel.
    # Every terminal leaf allows choosing target 0, target 1, or abstaining.
    terminal_masses = {}
    for channel, data in enumerate((INDEPENDENT_ROWS, SHARED_ROWS)):
        for target, observed, mass in data:
            arr = terminal_masses.setdefault(grouping(observed), [[F(0), F(0)], [F(0), F(0)]])
            arr[channel][target] += mass
    all_lines = {(F(0), F(0))}
    for m in terminal_masses.values():
        terminal_rewards = [(F(0), F(0))]
        for action in (0, 1):
            terminal_rewards.append(tuple(m[ch][action] - LOSS * m[ch][1 - action] for ch in (0, 1)))
        all_lines = {
            (a + value_ind, b + value_shared)
            for a, b in all_lines
            for value_ind, value_shared in terminal_rewards
        }
    return all_lines


@lru_cache(None)
def all_lines(adaptive):
    out = set()
    if adaptive:
        for tree in all_query_trees((0, 1, 2), 2):
            out |= attainable_reward_lines(lambda observed, tr=tree: path(tr, observed))
    else:
        for k in range(3):
            for subset in combinations(range(3), k):
                out |= attainable_reward_lines(
                    lambda observed, ss=subset: tuple(observed[j] for j in ss)
                )
    return frozenset(out)


def value(line, rho):
    independent, shared = line
    return independent * (1 - rho) + shared * rho


A1 = (F(28, 75), F(7, 12))
AM = (F(97, 300), F(41, 60))
A2 = (F(7, 30), F(5, 6))
F1 = (F(3, 10), F(9, 20))
F2 = (F(1, 4), F(11, 20))
F3 = (F(3, 20), F(3, 5))


@pytest.mark.parametrize(
    ("adaptive", "hull", "count"),
    (
        (True, ((F(0), A1), (F(1, 3), AM), (F(3, 8), A2), (F(1), None)), 385),
        (False, ((F(0), F1), (F(1, 3), F2), (F(2, 3), F3), (F(1), None)), 208),
    ),
)
def test_every_affine_policy_is_bounded_on_all_rho(adaptive, hull, count):
    lines = all_lines(adaptive)
    assert len(lines) == count
    for (lo, active), (hi, _) in zip(hull, hull[1:]):
        assert active in lines
        # All policy values are affine in rho. At both endpoints dominance
        # proves it throughout the interval, including uncountably many rho.
        for rho in (lo, hi):
            best = value(active, rho)
            assert all(value(candidate, rho) <= best for candidate in lines)


def test_exact_piecewise_adaptivity_premium_and_cost_crossing():
    # Follow the sorted union of adaptive and nonadaptive policy switches.
    rows = (
        (F(0), F(1, 3), A1, F1, F(11, 150), F(3, 50)),
        (F(1, 3), F(3, 8), AM, F2, F(11, 150), F(3, 50)),
        (F(3, 8), F(2, 3), A2, F2, -F(1, 60), F(3, 10)),
        (F(2, 3), F(1), A2, F3, F(1, 12), F(3, 20)),
    )
    for lo, hi, a, f, intercept, slope in rows:
        assert a in all_lines(True) and f in all_lines(False)
        for rho in (lo, (lo + hi) / 2, hi):
            premium = value(a, rho) - value(f, rho)
            assert premium == intercept + slope * rho
            assert premium == max(value(x, rho) for x in all_lines(True)) - max(
                value(x, rho) for x in all_lines(False)
            )
    # The previously overlooked intermediate adaptive policy at rho=1/3
    # exactly offsets the simultaneous nonadaptive switch: premium stays
    # strictly increasing, not locally nonmonotone.
    assert all(slope > 0 for _, _, _, _, _, slope in rows)
    assert (K + F(1, 60)) / F(3, 10) == F(7, 18)
    knots = [F(0), F(1, 3), F(3, 8), F(7, 18), F(2, 3), F(1)]
    for lo, hi in zip(knots, knots[1:]):
        rho = (lo + hi) / 2
        premium = max(value(x, rho) for x in all_lines(True)) - max(
            value(x, rho) for x in all_lines(False)
        )
        assert (premium - K > 0) == (rho > F(7, 18))
    assert max(value(x, F(7, 18)) for x in all_lines(True)) - max(
        value(x, F(7, 18)) for x in all_lines(False)
    ) == K


def test_what_joint_cue_calibration_must_observe():
    rho_star = F(7, 18)
    # Every cue's conditional error is EPS for every rho, hence single-cue
    # error rates cannot recover the dependence parameter.
    p_both = EPS * EPS + rho_star * EPS * (1 - EPS)
    p_disagree = 2 * EPS * (1 - EPS) * (1 - rho_star)
    assert p_both == F(9, 200)
    assert p_disagree == F(11, 100)
    for rho in (F(0), rho_star, F(1)):
        law = {
            errors: (1 - rho) * EPS**sum(errors) * (1 - EPS)**(3 - sum(errors))
            + (rho * (1 - EPS) if errors == (0, 0, 0) else F(0))
            + (rho * EPS if errors == (1, 1, 1) else F(0))
            for errors in product((0, 1), repeat=3)
        }
        for j in range(3):
            assert sum((p for errors, p in law.items() if errors[j]), F(0)) == EPS
        assert sum((p for errors, p in law.items() if errors[0] and errors[1]), F(0)) == (
            EPS * EPS + rho * EPS * (1 - EPS)
        )


def test_production_solver_matches_independent_all_policy_envelope_grid():
    from adaptive_gain.core import FiniteTask, Query, World
    from adaptive_gain.joint_bitflip_reward import joint_bitflip_law, optimal_joint_bitflip_reward

    task = FiniteTask(
        tuple(World(f"w{i}", target) for i, target in enumerate(TARGETS)),
        tuple(Query(f"q{j}", 1, cue) for j, cue in enumerate(CUES)),
    )
    for k in range(101):
        rho = F(k, 100)
        law = joint_bitflip_law(3, flip_probability=EPS, common_mode_fraction=rho)
        adaptive = optimal_joint_bitflip_reward(
            task, PRIOR, budget=2, error_pattern_probabilities=law,
            error_cost=LOSS, adaptive=True,
        )
        nonadaptive = optimal_joint_bitflip_reward(
            task, PRIOR, budget=2, error_pattern_probabilities=law,
            error_cost=LOSS, adaptive=False,
        )
        assert adaptive == pytest.approx(float(max(value(x, rho) for x in all_lines(True))), abs=1e-12)
        assert nonadaptive == pytest.approx(float(max(value(x, rho) for x in all_lines(False))), abs=1e-12)
