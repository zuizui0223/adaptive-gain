from collections import Counter
from itertools import product

from adaptive_gain.continuation_witnesses import continuation_fixed_cost_collision
from adaptive_gain.core import FiniteTask, Query, World, adaptive_gain_receipt
from adaptive_gain.five_world_normal_form import five_world_irreducible_standard_task
from adaptive_gain.resource_orbit_quotient import (
    canonical_fixed_replay_state,
    resource_orbit_cost_audit,
    task_automorphism_group,
    verify_task_automorphism_group,
)


def test_five_world_strict_core_keeps_capacity_under_genuine_task_automorphism():
    task = five_world_irreducible_standard_task()
    group = task_automorphism_group(task)
    assert verify_task_automorphism_group(task, group)
    assert group.automorphism_count == 2
    assert any(auto.query_mapping == (0, 2, 1) for auto in group.automorphisms)

    all_worlds = (1 << len(task.worlds)) - 1
    all_queries = (1 << len(task.queries)) - 1
    canonical = canonical_fixed_replay_state(
        all_worlds, all_queries, all_queries, group
    )
    assert canonical[1].bit_count() == 3
    assert canonical[2].bit_count() == 3

    audit = resource_orbit_cost_audit(task)
    assert audit.exact_costs_agree
    assert (audit.adaptive_cost, audit.fixed_cost) == (2, 3)
    assert audit.automorphism_count == 2
    assert audit.adaptive_orbit_states <= audit.adaptive_state_occurrences
    assert audit.fixed_orbit_states <= audit.fixed_state_occurrences


def test_capacity_aware_orbit_quotient_keeps_previous_fixed_cost_collision_separate():
    strict, bypass = continuation_fixed_cost_collision()
    strict_audit = resource_orbit_cost_audit(strict)
    bypass_audit = resource_orbit_cost_audit(bypass)
    assert strict_audit.exact_costs_agree
    assert bypass_audit.exact_costs_agree
    assert (strict_audit.adaptive_cost, strict_audit.fixed_cost) == (2, 3)
    assert (bypass_audit.adaptive_cost, bypass_audit.fixed_cost) == (2, 2)


def test_complete_balanced_four_world_binary_universe_preserves_joint_costs():
    worlds = (
        World("w0", 0), World("w1", 0),
        World("w2", 1), World("w3", 1),
    )
    patterns = tuple(product((0, 1), repeat=4))
    checked = strict = symmetric = 0
    automorphism_counts = Counter()
    adaptive_occurrences = adaptive_orbits = 0
    fixed_occurrences = fixed_orbits = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{i}", 1, outcomes) for i, outcomes in enumerate(maps)),
        )
        audit = resource_orbit_cost_audit(task)
        direct = adaptive_gain_receipt(task)
        assert audit.exact_costs_agree
        assert audit.adaptive_cost == direct.adaptive_cost
        assert audit.fixed_cost == direct.fixed_cost
        assert (audit.adaptive_cost is not None and audit.fixed_cost is not None and audit.adaptive_cost < audit.fixed_cost) == direct.strict_adaptive_gain
        strict += int(direct.strict_adaptive_gain)
        symmetric += int(audit.automorphism_count > 1)
        automorphism_counts[audit.automorphism_count] += 1
        adaptive_occurrences += audit.adaptive_state_occurrences
        adaptive_orbits += audit.adaptive_orbit_states
        fixed_occurrences += audit.fixed_state_occurrences
        fixed_orbits += audit.fixed_orbit_states
        checked += 1
    assert checked == 16 ** 3 == 4_096
    assert strict == 192
    assert symmetric == 2_560
    assert automorphism_counts == Counter({1: 1536, 2: 1440, 4: 1008, 8: 48, 12: 48, 24: 16})
    # Registered complete-universe computational benchmark, not a prevalence or
    # asymptotic speed claim.  Occurrences include repeated recursive calls;
    # orbit states are distinct canonical cache entries after exact symmetry.
    assert (adaptive_occurrences, adaptive_orbits) == (20_992, 16_048)
    assert (fixed_occurrences, fixed_orbits) == (50_576, 47_304)
