"""Exact 2-source environmental information synergy with budgeted floral queries.

Synthetic 2^d branch (B), binary profitable choice (T) independent uniform.
A branch-specific flower query F_j=1 iff (B=j,T=1), otherwise 0.
Two unrelated species observations report distinct bits of B, with correlated
binary errors whose joint mass P(E0=1,E1=1) is q. No source observation, singly
or jointly, conveys any MARGINAL information about T. They can nevertheless
determine which flower query is productive under an intermediate budget.

This models Bayesian decision correctness, NOT empirical species interactions,
pollen transfer, evolution, wind exposure, or biological fitness.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import lcm


def _check(d, budget, bits, error, joint):
    if type(d) is not int or not 1 <= d <= 5:
        raise ValueError("d must be an integer from 1 to 5")
    if type(budget) is not int or not 0 <= budget <= 16:
        raise ValueError("budget must be integer 0..16")
    bits = tuple(bits)
    if len(bits) > 2 or any(type(x) is not int or not 0 <= x < d for x in bits):
        raise ValueError("at most two declared binary habitat bits")
    e = Fraction(error)
    q = e*e if joint is None else Fraction(joint)
    if not 0 <= e <= Fraction(1, 2) or not 0 <= q <= e:
        raise ValueError("invalid marginal error or both-wrong probability")
    return bits, e, q


def optimal(d, budget, bits=(), error=Fraction(0), joint=None):
    """Bayes-optimal success across ALL adaptive cue orders and stop decisions.

    Dynamic programming uses integer likelihood masses. Both-other-source error
    indicators are latent worlds; bit readings can be correlated. Flower queries
    return 1 only when T=1 and the corresponding branch is true. After zero
    flower outcomes, guessing T=0 is always weakly Bayes-optimal, since T=0
    posterior mass dominates the remaining T=1 mass pointwise in B.
    """
    bits, e, q = _check(d, budget, bits, error, joint)
    n = 1 << d
    probabilities = (1-2*e+q, e-q, e-q, q)  # E0 + 2*E1
    denom = lcm(*(x.denominator for x in probabilities))
    masses = tuple(int(x*denom) for x in probabilities)

    @lru_cache(None)
    def weights(read, observations):
        rows = []
        for b in range(n):
            w = 0
            for noise, probability in enumerate(masses):
                good = True
                for sensor, habitat_bit in enumerate(bits):
                    if read & (1 << sensor):
                        seen = ((b >> habitat_bit) & 1) ^ ((noise >> sensor) & 1)
                        if seen != ((observations >> sensor) & 1):
                            good = False
                            break
                if good:
                    w += probability
            rows.append(w)
        return tuple(rows)

    @lru_cache(None)
    def best(tested_flowers, seen_sources, outcomes, left):
        if left == 0:
            return 0
        w = weights(seen_sources, outcomes)
        answer = 0
        for b in range(n):
            flag = 1 << b
            if tested_flowers & flag:
                continue
            candidate = w[b] + best(tested_flowers | flag, seen_sources, outcomes, left-1)
            answer = max(answer, candidate)
        for s in range(len(bits)):
            flag = 1 << s
            if seen_sources & flag:
                continue
            nxt = seen_sources | flag
            candidate = (best(tested_flowers, nxt, outcomes & ~flag, left-1)
                         + best(tested_flowers, nxt, outcomes | flag, left-1))
            answer = max(answer, candidate)
        return answer

    return Fraction(1, 2) + Fraction(best(0, 0, 0, budget), 2*n*denom)


def fixed(d, budget):
    """Bayesian optimum for precommitted cue sets: measure up to K florals."""
    _check(d, budget, (), Fraction(0), None)
    n = 1 << d
    return Fraction(1, 2) + Fraction(min(n, budget), 2*n)


def perfect_formula(d, budget, r):
    """Closed form for r distinct fully accurate branch bits, equal cue costs."""
    if type(d) is not int or d < 1 or type(budget) is not int or budget < 0:
        raise ValueError("invalid perfect hierarchy")
    if type(r) is not int or not 0 <= r <= d:
        raise ValueError("number of distinct source bits out of range")
    n = 1 << d
    covered = max(min(n, (1 << k) * max(0, budget-k))
                  for k in range(min(r, budget)+1))
    return Fraction(1, 2) + Fraction(covered, 2*n)


def two_source_interaction(d, budget, error=Fraction(0), joint=None):
    """P(A,B)-P(A)-P(B)+P(no cues), NOT PID mutual-information synergy."""
    base = optimal(d, budget, (), error, joint)
    a = optimal(d, budget, (0,), error, joint)
    b = optimal(d, budget, (1,), error, joint)
    both = optimal(d, budget, (0, 1), error, joint)
    return both - a - b + base


def independent_of_target(d, error=Fraction(0), joint=None):
    """Verify I((S_A,S_B);T)=0 using exact factorization of their joint law."""
    _, e, q = _check(d, 2, (0, 1), error, joint)
    n = 1 << d
    probabilities = (1-2*e+q, e-q, e-q, q)
    for o1, o2 in product((0, 1), repeat=2):
        ps = sum((Fraction(1, n)*p for b in range(n)
                  for noise, p in enumerate(probabilities)
                  if (((b & 1) ^ (noise & 1)) == o1
                      and ((((b >> 1) & 1) ^ ((noise >> 1) & 1)) == o2))),
                 Fraction(0))
        for t in (0, 1):
            joint_prob = sum((Fraction(1, 2*n)*p for b in range(n)
                              for noise, p in enumerate(probabilities)
                              if (((b & 1) ^ (noise & 1)) == o1
                                  and ((((b >> 1) & 1) ^ ((noise >> 1) & 1)) == o2))),
                             Fraction(0))
            if joint_prob != ps / 2:
                return False
    return True


def showcase():
    e = Fraction(1, 10)
    def stringify(x):
        return str(x) if isinstance(x, Fraction) else x
    main = [optimal(4, 5, bits, e) for bits in ((), (0,), (1,), (0, 1))]
    alternative = [optimal(4, 6, bits, e) for bits in ((), (0,), (1,), (0, 1))]
    cases = []
    for error in (Fraction(1, 10), Fraction(3, 20)):
        for dependence, q in (("exclusive", Fraction(0)), ("independent", error*error), ("fully_shared", error)):
            cases.append({"error": str(error), "dependence": dependence,
                          "both_wrong": str(q),
                          "both_accuracy": str(optimal(4, 5, (0, 1), error, q)),
                          "interaction": str(two_source_interaction(4, 5, error, q))})
    return {"scope": "constructed decision model only, not a field fit",
            "worlds": 32, "branches": 16, "budget_5_accuracy": [str(x) for x in main],
            "budget_5_synergy": str(main[3]-main[1]-main[2]+main[0]),
            "budget_6_accuracy": [str(x) for x in alternative],
            "budget_6_synergy": str(alternative[3]-alternative[1]-alternative[2]+alternative[0]),
            "fixed_budget_5": str(fixed(4,5)),
            "two_species_joint_target_information_zero": independent_of_target(4,e),
            "correlated_error_cases": cases}


if __name__ == "__main__":
    import json
    print(json.dumps(showcase(), indent=2, ensure_ascii=False))
