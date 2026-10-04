"""Independent audit of the temporal-routing formulas.

This file intentionally does not import adaptive_gain.temporal_routing or
adaptive_gain.noisy_temporal_routing. It reconstructs the latent-state model
directly with exact Fraction arithmetic.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import product


PAIRS = (("route", "left"), ("route", "right"), ("left", "right"))


def _left(target, context):
    return target if context == 1 else 0


def _right(target, context):
    return target if context == 0 else 1


def _outcome(query, target, context0, context1):
    if query == "route":
        return context0
    if query == "left":
        return _left(target, context1)
    if query == "right":
        return _right(target, context1)
    raise ValueError(query)


def _state_probability(context0, context1, rho):
    return Fraction(1, 4) * (rho if context1 == context0 else 1 - rho)


def _bayes_accuracy(joint):
    return sum(max(v) for v in joint.values())


def _fixed_accuracy(rho, pair):
    joint = defaultdict(lambda: [Fraction(0), Fraction(0)])
    for target, context0, context1 in product((0, 1), repeat=3):
        p = _state_probability(context0, context1, rho)
        obs = tuple(_outcome(q, target, context0, context1) for q in pair)
        joint[obs][target] += p
    return _bayes_accuracy(joint)


def _adaptive_accuracy(rho, rule):
    joint = defaultdict(lambda: [Fraction(0), Fraction(0)])
    for target, context0, context1 in product((0, 1), repeat=3):
        p = _state_probability(context0, context1, rho)
        if rule == "persistence":
            query = "right" if context0 == 0 else "left"
        else:
            query = "left" if context0 == 0 else "right"
        obs = (context0, query, _outcome(query, target, context0, context1))
        joint[obs][target] += p
    return _bayes_accuracy(joint)


def _bsc(bit, reliability):
    return ((bit, reliability), (1 - bit, 1 - reliability))


def _noisy_fixed_accuracy(rho, a, b, pair):
    joint = defaultdict(lambda: [Fraction(0), Fraction(0)])
    for target, context0, context1 in product((0, 1), repeat=3):
        p_state = _state_probability(context0, context1, rho)
        distribution = {(): Fraction(1)}
        for query in pair:
            latent = context0 if query == "route" else _outcome(
                query, target, context0, context1
            )
            reliability = a if query == "route" else b
            nxt = defaultdict(Fraction)
            for hist, p_hist in distribution.items():
                for obs, p_obs in _bsc(latent, reliability):
                    nxt[hist + (obs,)] += p_hist * p_obs
            distribution = dict(nxt)
        for obs, p_obs in distribution.items():
            joint[obs][target] += p_state * p_obs
    return _bayes_accuracy(joint)


def _noisy_adaptive_accuracy(rho, a, b, rule):
    joint = defaultdict(lambda: [Fraction(0), Fraction(0)])
    for target, context0, context1 in product((0, 1), repeat=3):
        p_state = _state_probability(context0, context1, rho)
        for observed_route, p_route in _bsc(context0, a):
            if rule == "persistence":
                query = "right" if observed_route == 0 else "left"
            else:
                query = "left" if observed_route == 0 else "right"
            latent = _outcome(query, target, context0, context1)
            for observed_specialist, p_specialist in _bsc(latent, b):
                joint[(observed_route, query, observed_specialist)][target] += (
                    p_state * p_route * p_specialist
                )
    return _bayes_accuracy(joint)


def test_independent_perfect_cue_temporal_formula():
    for rho in map(Fraction, (0, Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), 1)):
        fixed = [_fixed_accuracy(rho, pair) for pair in PAIRS]
        assert fixed == [Fraction(3, 4)] * 3

        adaptive = max(
            _adaptive_accuracy(rho, "persistence"),
            _adaptive_accuracy(rho, "alternation"),
        )
        expected = Fraction(3, 4) + abs(2 * rho - 1) / 4
        assert adaptive == expected
        assert adaptive - max(fixed) == abs(2 * rho - 1) / 4


def test_independent_noisy_factorization_grid():
    rhos = tuple(map(Fraction, (0, Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), 1)))
    reliabilities = (Fraction(1, 2), Fraction(3, 4), Fraction(1))
    for rho, a, b in product(rhos, reliabilities, reliabilities):
        fixed = max(_noisy_fixed_accuracy(rho, a, b, pair) for pair in PAIRS)
        expected_fixed = Fraction(1, 2) + (2 * b - 1) / 4
        assert fixed == expected_fixed

        adaptive = max(
            _noisy_adaptive_accuracy(rho, a, b, "persistence"),
            _noisy_adaptive_accuracy(rho, a, b, "alternation"),
        )
        expected_gain = abs((2 * rho - 1) * (2 * a - 1) * (2 * b - 1)) / 4
        assert adaptive - fixed == expected_gain
