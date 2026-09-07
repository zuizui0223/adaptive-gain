from functools import lru_cache
from itertools import combinations, product

from adaptive_gain import (
    FiniteTask,
    Query,
    World,
    adaptive_gain_receipt,
    adaptive_minimum_resolution,
    bundle_information_bits,
)
from adaptive_gain.decomposition import optimal_policy_cost_decomposition
from adaptive_gain.exhaustive import enumerate_binary_universe
from adaptive_gain.witnesses import (
    direct_resolution_control,
    mrod_routing_task,
    payoff_routing_task,
    positive_root_information_gain_control,
    routing_bypass_control,
)


def _independent_oracle(targets, query_maps):
    n = len(targets)
    qn = len(query_maps)

    fixed = None
    for k in range(qn + 1):
        for bundle in combinations(range(qn), k):
            if all(
                targets[i] == targets[j]
                or any(query_maps[q][i] != query_maps[q][j] for q in bundle)
                for i, j in combinations(range(n), 2)
            ):
                fixed = k
                break
        if fixed is not None:
            break

    @lru_cache(None)
    def adaptive(mask, remaining):
        active = tuple(i for i in range(n) if mask & (1 << i))
        if len({targets[i] for i in active}) == 1:
            return 0
        best = None
        for q in range(qn):
            if not remaining & (1 << q):
                continue
            groups = {}
            for i in active:
                groups.setdefault(query_maps[q][i], 0)
                groups[query_maps[q][i]] |= 1 << i
            if len(groups) <= 1:
                continue
            costs = []
            for child_mask in groups.values():
                value = adaptive(child_mask, remaining ^ (1 << q))
                if value is None:
                    break
                costs.append(value)
            else:
                value = 1 + max(costs)
                best = value if best is None else min(best, value)
        return best

    return adaptive((1 << n) - 1, (1 << qn) - 1), fixed


def test_policy_union_decomposition_saturates_for_registered_positive_witnesses():
    for task in (mrod_routing_task(), payoff_routing_task()):
        d = optimal_policy_cost_decomposition(task)
        assert (d.adaptive_cost, d.fixed_cost, d.policy_union_cost) == (2, 3, 3)
        assert (d.branch_exclusive_overhead, d.realized_adaptive_gain, d.fixed_bypass_discount) == (1, 1, 0)
        assert d.identity_holds


def test_branch_exclusive_overhead_is_not_sufficient_because_fixed_can_bypass_route():
    task = routing_bypass_control()
    d = optimal_policy_cost_decomposition(task)
    assert (d.adaptive_cost, d.fixed_cost, d.policy_union_cost) == (2, 2, 3)
    assert (d.branch_exclusive_overhead, d.realized_adaptive_gain, d.fixed_bypass_discount) == (1, 0, 1)
    policy = adaptive_minimum_resolution(task).selected_policy
    assert policy is not None
    assert bundle_information_bits(task, (policy.query,)) == 0.0
    assert len({child.query for _, child in policy.branches}) == 2


def test_direct_control_has_zero_union_overhead_and_zero_gain():
    d = optimal_policy_cost_decomposition(direct_resolution_control())
    assert (d.adaptive_cost, d.fixed_cost, d.policy_union_cost) == (1, 1, 1)
    assert (d.branch_exclusive_overhead, d.realized_adaptive_gain, d.fixed_bypass_discount) == (0, 0, 0)


def test_zero_root_target_information_is_not_necessary_for_strict_gain():
    task = positive_root_information_gain_control()
    r = adaptive_gain_receipt(task)
    assert (r.adaptive_cost, r.fixed_cost) == (2, 3)
    roots = adaptive_minimum_resolution(task).optimal_first_queries
    assert "q_route" in roots
    assert bundle_information_bits(task, ("q_route",)) > 0.0


def test_exhaustive_four_world_balanced_binary_universe_has_exact_192_gain_tasks():
    summary = enumerate_binary_universe((0, 0, 1, 1), query_count=3)
    assert summary.total_tasks == 4096
    assert summary.strict_gain_tasks == 192
    assert summary.strict_gain_cost_pairs == ((2, 3),)
    assert summary.strict_tasks_all_optimal_roots_zero_direct_information
    assert dict(summary.cost_pair_counts) == {
        "1:1": 1352,
        "2:2": 864,
        "2:3": 192,
        "None:None": 1688,
    }


def test_exhaustive_small_universe_matches_independent_oracle_and_minimality_controls():
    cases = (
        ((0, 1), 3),
        ((0, 0, 1), 3),
        ((0, 0, 0, 1), 3),
    )
    for targets, qn in cases:
        patterns = tuple(product((0, 1), repeat=len(targets)))
        strict = 0
        for maps in product(patterns, repeat=qn):
            worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
            task = FiniteTask(worlds, tuple(Query(f"q{j}", 1, m) for j, m in enumerate(maps)))
            receipt = adaptive_gain_receipt(task)
            oracle = _independent_oracle(targets, maps)
            assert (receipt.adaptive_cost, receipt.fixed_cost) == oracle
            strict += int(receipt.strict_adaptive_gain)
        assert strict == 0
