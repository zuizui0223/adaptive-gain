"""Finite decision policies under a JOINT binary sensory-error distribution.

A joint error pattern is sampled once per encounter, independently of the
latent world, and the j-th perceived bit equals declared bit XOR error[j].
This retains each cue's marginal accuracy while permitting correlated errors.

Only finite known-prior small tasks, unit-or-positive-integer acquisition costs,
free abstention and a hard acquisition budget are modeled. No ecological
fitness, evolution or generalized causal effect is inferred here.
"""
from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
from itertools import combinations, product
import math
from typing import Sequence

from .core import FiniteTask


def joint_bitflip_law(query_count: int, *, flip_probability: float,
                      common_mode_fraction: float) -> dict[tuple[int, ...], float]:
    """Shared-error mixture with fixed marginal P(flip_j)=epsilon.

    With probability rho, all error bits are the same Bernoulli(epsilon);
    otherwise bits flip independently with Bernoulli(epsilon). For m>=2
    pairwise error correlation equals rho (for 0<epsilon<1). Fractions are
    preserved when Fraction inputs are supplied.
    """
    if type(query_count) is not int or not 0 <= query_count <= 8:
        raise ValueError('query_count must be an integer in [0,8]')
    e, rho = flip_probability, common_mode_fraction
    if not math.isfinite(float(e)) or not 0 <= e <= .5:
        raise ValueError('flip_probability must be finite and in [0,1/2]')
    if not math.isfinite(float(rho)) or not 0 <= rho <= 1:
        raise ValueError('common_mode_fraction must be finite and in [0,1]')
    if query_count == 0:
        return {(): 1}  # the unique empty observation always has probability one
    return {
        bits: (1-rho) * e**sum(bits) * (1-e)**(query_count-sum(bits))
        + (rho * (1-e) if all(z == 0 for z in bits) else 0)
        + (rho * e if query_count > 0 and all(z == 1 for z in bits) else 0)
        for bits in product((0, 1), repeat=query_count)
    }


def _validate(task, probabilities, budget, law):
    if type(budget) is not int or budget < 0:
        raise ValueError('budget must be a nonnegative integer')
    if len(task.queries) > 8:
        raise ValueError('correlated readout audit permits at most eight binary queries')
    if any(type(outcome) is not int or outcome not in (0, 1)
           for query in task.queries for outcome in query.outcomes):
        raise ValueError('each query requires integer binary outcomes')
    if len(probabilities) != len(task.worlds):
        raise ValueError('one probability per represented world is required')
    p = tuple(float(q) for q in probabilities)
    if any(not math.isfinite(q) or q <= 0 for q in p):
        raise ValueError('world probabilities must be finite and strictly positive')
    if not math.isclose(math.fsum(p), 1., rel_tol=0., abs_tol=1e-9):
        raise ValueError('world probabilities must sum to one')
    if not isinstance(law, Mapping) or not law:
        raise ValueError('a nonempty error-pattern probability mapping is required')
    masses = []
    m = len(task.queries)
    for bits, probability in law.items():
        if not isinstance(bits, tuple) or len(bits) != m or any(
            type(b) is not int or b not in (0, 1) for b in bits
        ):
            raise ValueError('each pattern must contain one integer bit per query')
        w = float(probability)
        if not math.isfinite(w) or w < 0:
            raise ValueError('error-pattern weights must be finite and nonnegative')
        if w > 0:
            masses.append((bits, w))
    if not masses or not math.isclose(math.fsum(w for _, w in masses), 1., rel_tol=0., abs_tol=1e-9):
        raise ValueError('error-pattern probabilities must sum to one')
    # Guard against silent loss of a possible positive latent state.
    microstates = []
    for i, world in enumerate(task.worlds):
        for bits, w in masses:
            mass = p[i] * w
            if mass == 0:
                raise ArithmeticError('joint likelihood underflow; use exact arithmetic')
            response = tuple(task.queries[j].outcomes[i] ^ bits[j] for j in range(m))
            microstates.append((world.target, response, mass))
    return microstates


def _precommitted_subsets(task, budget):
    for k in range(len(task.queries)+1):
        for sub in combinations(range(len(task.queries)), k):
            if sum(task.queries[j].cost for j in sub) <= budget:
                yield sub


def _terminal_value(rows, indices, reward, loss):
    target_masses = {}
    for i in indices:
        y, _, m = rows[i]
        target_masses.setdefault(y, []).append(m)
    if not target_masses:
        return 0.
    return max(0., max(
        reward * math.fsum(ms) - loss * math.fsum(
            v for label, masses in target_masses.items() if label != y for v in masses
        )
        for y, ms in target_masses.items()
    ))


def optimal_joint_bitflip_reward(
    task: FiniteTask, world_probabilities: Sequence[float], *, budget: int,
    error_pattern_probabilities: Mapping[tuple[int, ...], float],
    correct_reward: float = 1., error_cost: float = 0., adaptive: bool = True,
) -> float:
    """Maximum expected decision reward for contingent versus fixed cue access.

    Joint readout errors are hidden, not observed by the policy. Both classes
    may stop, guess or abstain. Fixed access precommits any affordable subset;
    it is not forced to resolve every latent world. Intended for small audits.
    """
    rows = _validate(task, world_probabilities, budget, error_pattern_probabilities)
    v, L = float(correct_reward), float(error_cost)
    if not math.isfinite(v) or v <= 0:
        raise ValueError('correct_reward must be finite and positive')
    if not math.isfinite(L) or L < 0:
        raise ValueError('error_cost must be finite and nonnegative')
    if type(adaptive) is not bool:
        raise ValueError('adaptive must be boolean')

    if not adaptive:
        best = 0.
        for sub in _precommitted_subsets(task, budget):
            groups = {}
            for i, (_, response, _) in enumerate(rows):
                groups.setdefault(tuple(response[j] for j in sub), []).append(i)
            best = max(best, math.fsum(
                _terminal_value(rows, group, v, L) for group in groups.values()
            ))
        return best

    n = len(rows)
    obs_masks = tuple(
        tuple(sum(1 << i for i, (_, r, _) in enumerate(rows) if r[j] == bit)
              for bit in (0, 1))
        for j in range(len(task.queries))
    )

    @lru_cache(None)
    def search(mask: int, remaining: int, unused: int) -> float:
        indices = tuple(i for i in range(n) if mask & (1 << i))
        best = _terminal_value(rows, indices, v, L)
        for j, query in enumerate(task.queries):
            bit = 1 << j
            if not (unused & bit) or query.cost > remaining:
                continue
            left, right = mask & obs_masks[j][0], mask & obs_masks[j][1]
            if not left or not right:
                continue  # no information gained, but a query would cost budget
            candidate = math.fsum((
                search(left, remaining-query.cost, unused ^ bit),
                search(right, remaining-query.cost, unused ^ bit),
            ))
            best = max(best, candidate)
        return best

    return search((1 << n) - 1, budget, (1 << len(task.queries)) - 1)


def joint_bitflip_abstention_threshold(
    task: FiniteTask, world_probabilities: Sequence[float], *, budget: int,
    error_pattern_probabilities: Mapping[tuple[int, ...], float],
) -> float:
    """Exact structural criterion for the all-abstain (zero reward) cutoff.

    Max of posterior odds across all budget-feasible subset histories. Returns
    +inf when some attainable history excludes all other target labels. For a
    finite law and free abstention, adaptive and fixed access share this bound
    as a positivity criterion, not necessarily the same optimal value.
    """
    rows = _validate(task, world_probabilities, budget, error_pattern_probabilities)
    best = 0.
    for sub in _precommitted_subsets(task, budget):
        groups = {}
        for y, response, mass in rows:
            m = groups.setdefault(tuple(response[j] for j in sub), {})
            m.setdefault(y, []).append(mass)
        for by_target in groups.values():
            for y, ms in by_target.items():
                good = math.fsum(ms)
                bad = math.fsum(mass for label, z in by_target.items() if label != y for mass in z)
                if bad == 0:
                    return math.inf
                odds = good / bad
                if not math.isfinite(odds):
                    raise ArithmeticError('posterior odds overflow; use exact arithmetic')
                best = max(best, odds)
    return best
