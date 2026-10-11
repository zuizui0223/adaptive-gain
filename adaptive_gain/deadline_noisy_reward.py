"""Finite-budget cue acquisition with independent binary readout errors.

Underlying targets and query bits are fixed. Each distinct query is observed
at most once, independently conditional on the latent state, with a common
bit-flip probability in [0, 1/2]. Queries consume budget, not extra payoff.
Correct decisions pay v, errors -L, and abstention zero. Priors/channels are
known and each policy class is reoptimized. No empirical fitness is estimated.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product
import math
from typing import Sequence

from .core import FiniteTask


def _inputs(task: FiniteTask, probabilities: Sequence[float], budget: int,
            flip_probability: float) -> tuple[tuple[float, ...], float]:
    if type(budget) is not int or budget < 0:
        raise ValueError('budget must be a nonnegative integer')
    e = float(flip_probability)
    if not math.isfinite(e) or not 0 <= e <= .5:
        raise ValueError('flip_probability must be finite and in [0, 1/2]')
    if any(type(z) is not int or z not in (0,1)
           for q in task.queries for z in q.outcomes):
        raise ValueError('noisy model requires integer binary query outcomes')
    if len(probabilities) != len(task.worlds):
        raise ValueError('one probability is required per represented world')
    p = tuple(float(x) for x in probabilities)
    if any(not math.isfinite(x) or x <= 0 for x in p):
        raise ValueError('world probabilities must be finite and strictly positive')
    if not math.isclose(math.fsum(p), 1., rel_tol=0., abs_tol=1e-9):
        raise ValueError('world probabilities must sum to one')
    return p, e


def _observe(task, masses, query, response, error):
    result = tuple(m * ((1-error) if z == response else error)
                   for m,z in zip(masses, task.queries[query].outcomes))
    if error > 0 and any(before > 0 and after == 0
                         for before,after in zip(masses,result)):
        raise ArithmeticError('likelihood underflow; use exact arithmetic for this regime')
    return result


def _affordable_subsets(task, budget):
    for size in range(len(task.queries)+1):
        for subset in combinations(range(len(task.queries)), size):
            if sum(task.queries[j].cost for j in subset) <= budget:
                yield subset


def _response_masses(task, probabilities, subset, error):
    for response in product((0,1), repeat=len(subset)):
        masses = probabilities
        for j,z in zip(subset,response):
            masses = _observe(task,masses,j,z,error)
        if any(masses):
            yield masses


def optimal_noisy_deadline_reward(
    task: FiniteTask, world_probabilities: Sequence[float], *, budget: int,
    flip_probability: float, correct_reward: float = 1., error_cost: float = 0.,
    adaptive: bool = True,
) -> float:
    """Optimal expected reward; adaptive next-query choice or fixed subset.

    The fixed subset may be incomplete and terminal choices may depend on its
    observations. Both classes may abstain. This is not a universal-bundle
    comparison, and observed noisy cues must not be used to eliminate states.
    Enumeration is exponential in query count; intended for small audits.
    """
    p,e = _inputs(task,world_probabilities,budget,flip_probability)
    v,L = float(correct_reward),float(error_cost)
    if not math.isfinite(v) or v <= 0:
        raise ValueError('correct_reward must be finite and positive')
    if not math.isfinite(L) or L < 0:
        raise ValueError('error_cost must be finite and nonnegative')
    if type(adaptive) is not bool:
        raise ValueError('adaptive must be boolean')
    targets = tuple(w.target for w in task.worlds)
    labels = set(targets)

    @lru_cache(None)
    def terminal(masses):
        return max(0., max(v*math.fsum(m for m,y in zip(masses,targets) if y==label)
                           -L*math.fsum(m for m,y in zip(masses,targets) if y!=label)
                           for label in labels))

    if not adaptive:
        return max(math.fsum(terminal(masses) for masses in
                             _response_masses(task,p,subset,e))
                   for subset in _affordable_subsets(task,budget))

    @lru_cache(None)
    def search(masses,remaining,unused):
        best = terminal(masses)
        for j in unused:
            c = task.queries[j].cost
            if c > remaining:
                continue
            next_unused = tuple(k for k in unused if k!=j)
            value = math.fsum(search(child,remaining-c,next_unused)
                              for z in (0,1)
                              if any(child := _observe(task,masses,j,z,e)))
            best = max(best,value)
        return best
    return search(p,budget,tuple(range(len(task.queries))))


def noisy_deadline_abstention_threshold(
    task: FiniteTask, world_probabilities: Sequence[float], *, budget: int,
    flip_probability: float,
) -> float:
    """Largest attainable posterior odds of any target versus all others.

    Both policy classes have zero optimal gross reward iff L/v >= this
    threshold (zero-reward actions may tie at equality). Every adaptive
    history is attainable with its corresponding precommitted subset, so this
    *positivity boundary* is shared, though expected rewards need not agree.
    For strictly positive error and >=2 target labels the boundary is finite;
    zero error or a single target may give infinity. Finite binary channels,
    finite acquisition budget, free abstention and no per-query payoff debit
    are essential. This is not a bound for unbounded continuous evidence.
    """
    p,e = _inputs(task,world_probabilities,budget,flip_probability)
    targets = tuple(w.target for w in task.worlds)
    labels = set(targets)
    best = 0.
    for subset in _affordable_subsets(task,budget):
        for masses in _response_masses(task,p,subset,e):
            for label in labels:
                good=math.fsum(m for m,y in zip(masses,targets) if y==label)
                bad=math.fsum(m for m,y in zip(masses,targets) if y!=label)
                if good and bad == 0:
                    return math.inf
                if bad:
                    odds=good/bad
                    if not math.isfinite(odds):
                        raise ArithmeticError('posterior odds overflow; use exact arithmetic')
                    best=max(best,odds)
    return best
