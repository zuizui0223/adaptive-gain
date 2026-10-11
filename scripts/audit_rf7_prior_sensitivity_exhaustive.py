"""Independent exhaustive RF7 prior-sensitivity audit on four binary worlds.

Enumerates all ordered triples of nonconstant binary queries and every
nontrivial binary target labeling.  Uses a small, standalone fixed-coverage
check and a memoized contingent-decision recursion; does not import
adaptive_gain's production solver.

Run:
    python scripts/audit_rf7_prior_sensitivity_exhaustive.py
    python scripts/audit_rf7_prior_sensitivity_exhaustive.py --output-json result.json
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import product
import json
import math
from pathlib import Path


N = 4
M = 3
MU = 0.3
QUERY_MASKS = tuple(range(1, (1 << N) - 1))
PROBABILITIES = {
    "uniform": (0.25, 0.25, 0.25, 0.25),
    "dominant_world": (0.999, 0.001 / 3, 0.001 / 3, 0.001 / 3),
}


def smallest_fixed_resolver(target: int, queries: tuple[int, ...]) -> int | None:
    """Return minimum number of jointly acquired queries separating all targets."""
    different_pairs = tuple(
        (i, j)
        for i in range(N)
        for j in range(i + 1, N)
        if ((target >> i) & 1) != ((target >> j) & 1)
    )
    for size in range(1, M + 1):
        for chosen in range(1, (1 << M)):
            if chosen.bit_count() != size:
                continue
            if all(
                any(
                    ((chosen >> k) & 1)
                    and (((queries[k] >> i) & 1) != ((queries[k] >> j) & 1))
                    for k in range(M)
                )
                for i, j in different_pairs
            ):
                return size
    return None


def best_adaptive_discounted_value(
    target: int,
    queries: tuple[int, ...],
    weights: tuple[float, ...],
) -> float:
    """Optimize the exact discounted value over all resolving contingent trees."""
    discount = math.exp(-MU)

    @lru_cache(maxsize=None)
    def solve(world_mask: int, remaining_queries: int) -> float:
        target_ones = target & world_mask
        if target_ones == 0 or target_ones == world_mask:
            return sum(
                weights[i] for i in range(N) if (world_mask >> i) & 1
            )

        best = -math.inf
        for k, query in enumerate(queries):
            if not ((remaining_queries >> k) & 1):
                continue
            branch_one = world_mask & query
            branch_zero = world_mask & ~query
            if not branch_one or not branch_zero:
                continue
            after = remaining_queries & ~(1 << k)
            left = solve(branch_zero, after)
            right = solve(branch_one, after)
            if math.isfinite(left) and math.isfinite(right):
                best = max(best, discount * (left + right))
        return best

    return solve((1 << N) - 1, (1 << M) - 1)


def audit() -> dict:
    maxima = {name: {"advantage": -math.inf} for name in PROBABILITIES}
    evaluated = 0
    solvable = 0
    for target in range(1, (1 << N) - 1):
        for queries in product(QUERY_MASKS, repeat=M):
            evaluated += 1
            fixed = smallest_fixed_resolver(target, queries)
            if fixed is None:
                continue
            solvable += 1
            for name, weights in PROBABILITIES.items():
                adaptive = best_adaptive_discounted_value(
                    target, queries, weights
                )
                if not math.isfinite(adaptive):
                    continue
                gain = adaptive - math.exp(-MU * fixed)
                if gain > maxima[name]["advantage"] + 1e-12:
                    maxima[name] = {
                        "advantage": gain,
                        "adaptive_performance": adaptive,
                        "fixed_cost": fixed,
                        "target_bits": target,
                        "query_outcome_masks": list(queries),
                    }

    ceiling = math.exp(-MU) - math.exp(-MU * min(M, N - 1))
    result = {
        "status": "EXHAUSTIVE_INDEPENDENT_ENUMERATION",
        "worlds": N,
        "queries": M,
        "query_arity": 2,
        "discount_rate": MU,
        "ordered_query_tuples_and_targets_evaluated": evaluated,
        "solvable_tasks": solvable,
        "expected_value_supremum": ceiling,
        "maxima": maxima,
        "relative_to_supremum": {
            name: row["advantage"] / ceiling
            for name, row in maxima.items()
        },
        "scope": (
            "These maxima are exact for the two declared world-frequency "
            "distributions, across all ordered binary 3-query tasks on 4 worlds. "
            "The theoretical supremum instead permits arbitrary positive priors."
        ),
    }
    assert evaluated == 38_416
    assert solvable == 28_528
    assert math.isclose(
        maxima["uniform"]["advantage"],
        0.14224197635342734,
        rel_tol=0.0,
        abs_tol=1e-10,
    )
    assert math.isclose(
        maxima["dominant_world"]["advantage"],
        0.33396172637229543,
        rel_tol=0.0,
        abs_tol=1e-10,
    )
    assert maxima["uniform"]["advantage"] < ceiling
    assert maxima["dominant_world"]["advantage"] < ceiling
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    print(payload)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
