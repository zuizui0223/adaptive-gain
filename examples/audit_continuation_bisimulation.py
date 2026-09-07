"""Reproduce structural quotient controls and optional exhaustive validation.

Run from an editable installation, or with PYTHONPATH=.
  python examples/audit_continuation_bisimulation.py --exhaustive --output validation/continuation_bisimulation.json
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
from itertools import product
import json
from pathlib import Path

from adaptive_gain.core import FiniteTask, Query, World, adaptive_gain_receipt
from adaptive_gain.continuation_bisimulation import (
    build_continuation_quotient, continuation_quotient_costs, verify_continuation_quotient,
)
from adaptive_gain.continuation_witnesses import continuation_fixed_cost_collision


def partitions(n):
    """Restricted-growth strings: one representative of every deterministic partition."""
    def extend(prefix):
        if len(prefix) == n:
            yield prefix
        else:
            for label in range(max(prefix, default=-1) + 2):
                yield from extend(prefix + (label,))
    return tuple(extend(()))


def audit_universe(targets, patterns):
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    tasks = tuple(FiniteTask(worlds, tuple(Query(f"q{j}", 1, col) for j, col in enumerate(cols)))
                  for cols in product(patterns, repeat=3))
    certificate = build_continuation_quotient(tasks, max_states=1_000_000)
    verified = verify_continuation_quotient(tasks, certificate)
    costs = continuation_quotient_costs(tasks, certificate)
    counts, class_pairs = Counter(), defaultdict(set)
    mismatches = strict = 0
    for i, task in enumerate(tasks):
        oracle = adaptive_gain_receipt(task)
        mismatches += costs[i] != oracle.adaptive_cost
        strict += oracle.strict_adaptive_gain
        pair = (oracle.adaptive_cost, oracle.fixed_cost)
        counts[str(pair)] += 1
        class_pairs[certificate.root_classes[i]].add(pair)
    result = {
        "targets": targets, "query_count": 3, "patterns_per_query": len(patterns),
        "task_count": len(tasks), "mixed_states_before_quotient": certificate.mixed_state_count,
        "mixed_continuation_classes": certificate.mixed_class_count,
        "distinct_root_classes": len(set(certificate.root_classes)),
        "structural_certificate_verified": verified, "adaptive_cost_mismatches": mismatches,
        "strict_gain_tasks_using_original_fixed_oracle": strict,
        "exact_cost_pair_counts": dict(sorted(counts.items())),
        "root_classes_with_multiple_fixed_costs": sum(len(pairs) > 1 for pairs in class_pairs.values()),
    }
    if not verified or mismatches:
        raise AssertionError(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exhaustive", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    tasks = continuation_fixed_cost_collision()
    cert = build_continuation_quotient(tasks)
    result = {
        "scope": "finite_synthetic_deterministic_worst_path_cost_not_empirical_data",
        "baseline_commit": "44c39b7b48ddd1452303b28150950339d44be732",
        "fixed_cost_collision": {
            "same_recursive_root_class": cert.root_classes[0] == cert.root_classes[1],
            "adaptive_costs": continuation_quotient_costs(tasks, cert),
            "original_cost_receipts": [asdict(adaptive_gain_receipt(task)) for task in tasks],
            "mixed_states": cert.mixed_state_count,
            "mixed_classes": cert.mixed_class_count,
            "structural_certificate_verified": verify_continuation_quotient(tasks, cert),
        },
        "universes": [],
        "limitations": [
            "State graph construction still visits all reachable mixed states.",
            "Class IDs are local to one certificate; cross-task sharing is a batch operation.",
            "Only declared positive query costs and deterministic worst-path resolution are preserved.",
            "Fixed bundle cost, target labels and probabilistic information need their original data.",
        ],
    }
    if args.exhaustive:
        for targets, patterns in (
            ((0, 0, 1, 1), tuple(product((0, 1), repeat=4))),
            ((0, 0, 1, 1, 1), tuple(product((0, 1), repeat=5))),
            ((0, 0, 1, 1), partitions(4)),
            ((0, 0, 1, 2), partitions(4)),
        ):
            row = audit_universe(targets, patterns)
            result["universes"].append(row)
        result["total_exhaustive_tasks"] = sum(row["task_count"] for row in result["universes"])
    text = json.dumps(result, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
