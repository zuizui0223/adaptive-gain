from itertools import product
from math import comb

from adaptive_gain import FiniteTask, Query, World
from adaptive_gain.kernel_bounds import (
    is_inclusion_antichain,
    minimal_separator_antichain,
    task_pair_antichain_bound,
)
from adaptive_gain.minimal_normal_form import minimal_strict_gain_standard_task


def test_minimal_strict_gain_standard_form_saturates_three_query_sperner_bound():
    receipt = task_pair_antichain_bound(minimal_strict_gain_standard_task())
    assert receipt.query_count == 3
    assert receipt.raw_cross_target_pair_count == 4
    assert receipt.minimal_separator_antichain_size == 3
    assert receipt.sperner_upper_bound == comb(3, 1) == 3
    assert receipt.canonical_signatures == (1, 2, 4)
    assert receipt.strict_reduction_from_raw_pairs == 1


def test_middle_layer_of_boolean_lattice_is_tight_sperner_antichain():
    m = 4
    signatures = tuple(
        mask for mask in range(1 << m) if mask.bit_count() == m // 2
    )
    minimal = minimal_separator_antichain(signatures)
    assert len(minimal) == comb(4, 2) == 6
    assert is_inclusion_antichain(minimal)


def test_pair_dominance_keeps_only_inclusion_minimal_obligations():
    # 001 is harder than 011 and 111; 100 is harder than 110.  The supersets
    # are redundant obligations because covering each minimal signature covers
    # every containing signature too.
    signatures = (0b001, 0b011, 0b111, 0b100, 0b110, 0b001)
    assert minimal_separator_antichain(signatures) == (0b001, 0b100)


def test_sperner_bound_holds_across_complete_minimal_4096_universe():
    targets = (0, 0, 1, 1)
    worlds = tuple(World(f"w{i}", target) for i, target in enumerate(targets))
    patterns = tuple(product((0, 1), repeat=4))
    max_kernel = 0
    saturating = 0
    for maps in product(patterns, repeat=3):
        task = FiniteTask(
            worlds,
            tuple(Query(f"q{j}", 1, outcomes) for j, outcomes in enumerate(maps)),
        )
        receipt = task_pair_antichain_bound(task)
        assert receipt.antichain_bound_holds
        assert receipt.minimal_separator_antichain_size <= 3
        max_kernel = max(max_kernel, receipt.minimal_separator_antichain_size)
        saturating += int(receipt.minimal_separator_antichain_size == 3)
    assert max_kernel == 3
    assert saturating > 0


def test_empty_or_unseparable_signatures_do_not_falsify_nonempty_antichain_bound():
    task = FiniteTask(
        (World("a", 0), World("b", 1)),
        (Query("constant", 1, (0, 0)),),
    )
    receipt = task_pair_antichain_bound(task)
    assert receipt.raw_cross_target_pair_count == 1
    assert receipt.minimal_separator_antichain_size == 0
    assert receipt.antichain_bound_holds
