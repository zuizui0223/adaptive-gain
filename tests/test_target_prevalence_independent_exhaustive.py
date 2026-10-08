"""Independent exhaustive check of the minimal target-prevalence arity gap.

No adaptive-gain solver, target-prevalence helper, or private-pair constructor
is imported. Enumerate every four-world binary target labeling and every
unordered pair of deterministic unit-cost queries for b=2 and b=3.

For each pair requiring both queries as a universal fixed resolver, compute
which target classes can terminate in one query under either root choice.
At target prevalence 50/50, concentrating frequency on those pure classes
gives supremal early-termination mass 0, 1/2, or 1.
"""
from itertools import combinations, product


def _resolves(targets, queries):
    """Whether the selected queries distinguish every opposite-target pair."""
    for i, j in combinations(range(len(targets)), 2):
        if targets[i] == targets[j]:
            continue
        if all(query[i] == query[j] for query in queries):
            return False
    return True


def _root_pure_classes(targets, query):
    groups = {}
    for target, outcome in zip(targets, query):
        groups.setdefault(outcome, set()).add(target)
    return {
        next(iter(group))
        for group in groups.values()
        if len(group) == 1
    }


def _exhaustive_receipt(arity, world_count=4):
    queries = tuple(product(range(arity), repeat=world_count))
    count_fixed_two = 0
    count_one_pure_class = 0
    count_both_pure_classes = 0
    max_early_mass = 0.0
    witness = None

    for targets in product((0, 1), repeat=world_count):
        if len(set(targets)) != 2:
            continue

        for first, second in combinations(queries, 2):
            if _resolves(targets, (first,)):
                continue
            if _resolves(targets, (second,)):
                continue
            if not _resolves(targets, (first, second)):
                continue

            count_fixed_two += 1
            available_pure_classes = max(
                len(_root_pure_classes(targets, first)),
                len(_root_pure_classes(targets, second)),
            )
            if available_pure_classes == 1:
                count_one_pure_class += 1
            elif available_pure_classes == 2:
                count_both_pure_classes += 1

            early_mass = available_pure_classes / 2.0
            if early_mass > max_early_mass:
                max_early_mass = early_mass
                witness = (targets, first, second)

    return {
        "fixed_cost_two_pairs": count_fixed_two,
        "one_pure_target_class_pairs": count_one_pure_class,
        "both_pure_target_classes_pairs": count_both_pure_classes,
        "balanced_target_one_query_supremum": max_early_mass,
        "witness": witness,
    }


def test_four_world_two_query_exhaustion_binary():
    receipt = _exhaustive_receipt(2)
    assert receipt["fixed_cost_two_pairs"] == 264
    assert receipt["one_pure_target_class_pairs"] == 240
    assert receipt["both_pure_target_classes_pairs"] == 0
    assert receipt["balanced_target_one_query_supremum"] == 0.5


def test_four_world_two_query_exhaustion_ternary():
    receipt = _exhaustive_receipt(3)
    assert receipt["fixed_cost_two_pairs"] == 9720
    assert receipt["one_pure_target_class_pairs"] == 5616
    assert receipt["both_pure_target_classes_pairs"] == 3888
    assert receipt["balanced_target_one_query_supremum"] == 1.0


def test_three_worlds_cannot_support_two_pure_root_targets_plus_mixed_branch():
    receipt = _exhaustive_receipt(3, world_count=3)
    assert receipt["both_pure_target_classes_pairs"] == 0
