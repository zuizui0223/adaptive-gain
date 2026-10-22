"""Weather × heterospecific routing: exact finite task and Bayes-budget extension.

This is a synthetic model, not a fitted ecological effect. Four EQUALLY likely
resource states share two independent bits (branch, target). A different-species
cue reports the branch, never the target; flower cues are branch-specific.
Weather can mask a native branch cue; a heterospecific cue can restore it.

The deterministic analogue uses the established adaptive_gain.core exact solver.
For imperfect routing observations a separate Fraction-valued finite Bayesian
DP computes maximum success at a hard budget, not guaranteed resolution C_A.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
from itertools import combinations, product

_STATES = ((0, 0), (0, 1), (1, 0), (1, 1))  # (branch, correct target)
_COSTS = {"native": 1, "heterospecific": 1, "flower_0": 1,
          "flower_1": 1, "direct_assay": 3}
_QUARTER = Fraction(1, 4)


def _error(x: Fraction | None) -> Fraction | None:
    if x is None:
        return None
    e = Fraction(x)
    if not Fraction(0) <= e <= Fraction(1, 2):
        raise ValueError("observed binary branch cue error must be in [0,1/2]")
    return e


def _likelihood(name: str, observed: int, state: tuple[int, int],
                native_error: Fraction | None,
                heterospecific_error: Fraction | None) -> Fraction:
    branch, target = state
    if name == "native":
        err = native_error
    elif name == "heterospecific":
        err = heterospecific_error
    elif name == "flower_0":
        return int(observed == (target if branch == 0 else 0))
    elif name == "flower_1":
        return int(observed == (target if branch == 1 else 1))
    elif name == "direct_assay":
        return int(observed == target)
    else:
        raise ValueError("unknown cue")
    if err is None:
        raise ValueError("unavailable cue cannot be queried")
    return 1 - err if observed == branch else err


def _vocabulary(e_native, e_hetero):
    out = ["flower_0", "flower_1", "direct_assay"]
    if e_native is not None:
        out.insert(0, "native")
    if e_hetero is not None:
        out.insert(0, "heterospecific")
    return tuple(sorted(out))


def _validation(budget, native_error, heterospecific_error):
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")
    n, h = _error(native_error), _error(heterospecific_error)
    return n, h, _vocabulary(n, h)


def _terminal_score(weights: tuple[Fraction, ...]) -> Fraction:
    """Unnormalized correct-decision probability at a Bayesian tree leaf."""
    return max(weights[0] + weights[2], weights[1] + weights[3])


def optimal_accuracy(budget: int, *, native_error: Fraction | None = None,
                     heterospecific_error: Fraction | None = None) -> Fraction:
    """Optimal conditional query policy success probability, uniform prior.

    This is not deterministic guaranteed-resolution cost; errors are permitted.
    A leaf may stop and guess at any remaining budget. Query outcomes are
    conditionally independent GIVEN the four ecological worlds by assumption.
    """
    en, eh, names = _validation(budget, native_error, heterospecific_error)

    @lru_cache(None)
    def solve(mass: tuple[Fraction, ...], available: tuple[str, ...], left: int):
        best = _terminal_score(mass)
        for name in available:
            price = _COSTS[name]
            if price > left:
                continue
            reduced = tuple(x for x in available if x != name)
            total = Fraction(0)
            for outcome in (0, 1):
                branch = tuple(
                    mass[i] * _likelihood(name, outcome, world, en, eh)
                    for i, world in enumerate(_STATES)
                )
                if any(branch):
                    total += solve(branch, reduced, left - price)
            if total > best:
                best = total
        return best

    return solve((_QUARTER,) * 4, names, budget)


def fixed_accuracy(budget: int, *, native_error: Fraction | None = None,
                   heterospecific_error: Fraction | None = None) -> Fraction:
    """Best precommitted acquisition subset at fixed budget; Bayes decision after.

    This independently enumerates subset signatures, not the adaptive solver
    with decision branching disabled.
    """
    en, eh, names = _validation(budget, native_error, heterospecific_error)
    best = Fraction(1, 2)
    for n in range(len(names) + 1):
        for chosen in combinations(names, n):
            if sum(_COSTS[x] for x in chosen) > budget:
                continue
            score = Fraction(0)
            for outcomes in product((0, 1), repeat=n):
                target_probs = [Fraction(0), Fraction(0)]
                for branch, target in _STATES:
                    weight = _QUARTER
                    for cue, observation in zip(chosen, outcomes):
                        weight *= _likelihood(cue, observation, (branch, target), en, eh)
                    target_probs[target] += weight
                score += max(target_probs)
            best = max(best, score)
    return best


def branch_target_independence(error: Fraction) -> bool:
    """Verify a possibly inaccurate species-branch cue has NO marginal target MI.

    Exactly tests P(cue=o,target=t)=P(cue=o)P(target=t); no logarithms.
    """
    e = _error(error)
    cells = {
        (o, t): sum((
            _QUARTER * (1-e if o == b else e)
            for b, goal in _STATES if goal == t
        ), Fraction(0))
        for o in (0, 1) for t in (0, 1)
    }
    return all(
        cells[o, t] ==
        sum(cells[o, x] for x in (0, 1)) * sum(cells[x, t] for x in (0, 1))
        for o, t in cells
    )


def analytic_route_success(error: Fraction) -> Fraction:
    """Constructive cue→branch-specific flower policy; optimal on 0<=e<=1/2."""
    return Fraction(1) - _error(error) / 2


def ecological_contexts(calm_native_error: Fraction = Fraction(1, 20),
                        windy_heterospecific_error: Fraction = Fraction(1, 10)
                        ) -> dict[str, object]:
    """Factorial wind×species cue intervention under the SAME four worlds.

    These assumed error rates are illustrative, NOT inferred from field data.
    The experiment's hard information budget is precisely TWO unit cues.
    """
    calm = _error(calm_native_error)
    species = _error(windy_heterospecific_error)
    no = {"native_error": calm}
    yes = {"native_error": calm, "heterospecific_error": species}
    contexts = {
        "calm_no_species": no,
        "calm_species": yes,
        "wind_no_species": {},
        "wind_species": {"heterospecific_error": species},
    }
    rows: dict[str, object] = {}
    for name, params in contexts.items():
        rows[name] = {
            "adaptive_at_2": optimal_accuracy(2, **params),
            "fixed_at_2": fixed_accuracy(2, **params),
            "native_error": params.get("native_error"),
            "heterospecific_error": params.get("heterospecific_error"),
        }
    rows["species_x_wind_difference_in_differences"] = (
        rows["wind_species"]["adaptive_at_2"]
        - rows["calm_species"]["adaptive_at_2"]
        - rows["wind_no_species"]["adaptive_at_2"]
        + rows["calm_no_species"]["adaptive_at_2"]
    )
    return rows


def example_finite_task(windy: bool, heterospecific_present: bool, *,\n                        offbranch_floral_1: int = 1):
    """Construct repo's exact deterministic finite task, conditional on context.

    Wind and species-cue presence are EXTERNAL experimentally set contexts,
    not hidden ecological worlds. Cost units are hypothetical and not
    estimated from measured flight durations.
    """
    from adaptive_gain.core import World, Query, FiniteTask
    worlds = tuple(World(f"b{b}_t{t}", t) for b, t in _STATES)
    def native(s, t): return s if not windy else 0
    def other(s, t): return s if heterospecific_present else 0
    def flower0(s, t): return t if s == 0 else 0
    def flower1(s, t): return t if s == 1 else offbranch_floral_1
    queries = tuple(Query(name, cost, tuple(fn(*x) for x in _STATES))
                    for name, cost, fn in (
                        ("native_branch", 1, native),
                        ("other_species_branch", 1, other),
                        ("floral_cue_0", 1, flower0),
                        ("floral_cue_1", 1, flower1),
                        ("direct_assay", 3, lambda b, t: t),
                    ))
    return FiniteTask(worlds, queries)


def full_receipt():
    """Machine-readable computations, including the repository's exact solver."""
    from adaptive_gain.core import adaptive_gain_receipt
    context = ecological_contexts()
    exact = {}
    for w, s in product((False, True), repeat=2):
        result = adaptive_gain_receipt(example_finite_task(w, s))
        exact[f"wind_{int(w)}_species_{int(s)}"] = {
            "adaptive_cost": result.adaptive_cost,
            "fixed_cost": result.fixed_cost,
            "structural_gap": result.fixed_cost - result.adaptive_cost,
        }
    return {"context_bayes": context, "exact_deterministic": exact,
            "uncertainty_curve": [
                {"error": Fraction(i, 20),
                 "adaptive": optimal_accuracy(2, native_error=Fraction(i, 20)),
                 "fixed": fixed_accuracy(2, native_error=Fraction(i, 20))}
                for i in range(11)],
            "scope": "synthetic_four_world_bayesian_cue_task_not_fitted_field_prediction"}


if __name__ == "__main__":
    import json
    def fraction_json(value):
        if isinstance(value, Fraction):
            return {"num": value.numerator, "den": value.denominator,
                    "decimal": float(value)}
        raise TypeError(type(value).__name__)
    print(json.dumps(full_receipt(), default=fraction_json, indent=2))
