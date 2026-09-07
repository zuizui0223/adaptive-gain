from itertools import product

from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    selected_policy_integer_cover_gain_certificate,
)


def test_integer_budget_proof_matches_exact_strict_gain_on_all_4096_minimal_balanced_tasks():
    targets = (0, 0, 1, 1)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    patterns = tuple(product((0, 1), repeat=4))
    exact_strict = proof_strict = disagreements = 0

    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, outcomes) for j, outcomes in enumerate(maps)),
        )
        exact = adaptive_gain_receipt(task).strict_adaptive_gain
        proof = selected_policy_integer_cover_gain_certificate(
            task, max_states=1000
        ).strict_adaptive_gain_certified_without_fixed_optimum
        exact_strict += int(exact)
        proof_strict += int(proof)
        disagreements += int(exact != proof)

    assert exact_strict == 192
    assert proof_strict == 192
    assert disagreements == 0
