from __future__ import annotations

from fractions import Fraction
from itertools import product

import pytest

from adaptive_gain.routing_origin_fixation import (
    RoutingStationaryStateLimitError,
    degeneracy_chain_bound_holds,
    detailed_balance_holds,
    full_phase_half_mass_bounds,
    full_phase_is_modal_layer,
    full_phase_modal_tilt_threshold,
    full_phase_stationary_mass_from_tilt,
    gain_layer_degeneracies,
    gain_layer_degeneracy,
    minimum_population_size_for_modal_full_phase,
    moran_fixation_probability,
    moran_fixation_ratio,
    origin_fixation_selection_receipt,
    origin_fixation_transition_row,
    routing_genotype_count,
    routing_genotypes,
    routing_realized_gain,
    stationary_flow_distribution,
    stationary_genotype_distribution,
    stationary_layer_distribution,
    stationary_tilt,
    steps_below_full_layer_degeneracy,
)


def _solve_stationary_exact_q1(population_size: int, fitness_step: Fraction):
    """Independent exact 4-state stationary solve by Gauss-Jordan elimination."""
    q = 1
    states = tuple(routing_genotypes(q))
    n = len(states)
    index = {state: i for i, state in enumerate(states)}
    p = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]
    for i, state in enumerate(states):
        for target, prob in origin_fixation_transition_row(q, state, population_size, fitness_step).items():
            p[i][index[target]] += prob

    # Solve (P^T-I) pi=0 with the last equation replaced by sum pi=1.
    a = [[p[col][row] - (1 if row == col else 0) for col in range(n)] + [Fraction(0, 1)] for row in range(n)]
    a[-1] = [Fraction(1, 1) for _ in range(n)] + [Fraction(1, 1)]

    pivot_row = 0
    for col in range(n):
        pivot = next((r for r in range(pivot_row, n) if a[r][col] != 0), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [value / scale for value in a[pivot_row]]
        for r in range(n):
            if r == pivot_row or a[r][col] == 0:
                continue
            factor = a[r][col]
            a[r] = [left - factor * right for left, right in zip(a[r], a[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == n:
            break

    solution = [Fraction(0, 1) for _ in range(n)]
    for row in a:
        pivot = next((c for c in range(n) if row[c] == 1 and all(row[d] == 0 for d in range(c))), None)
        if pivot is not None:
            solution[pivot] = row[-1]
    return {state: solution[index[state]] for state in states}


def test_moran_fixation_ratio_is_exact_power_law() -> None:
    for n in range(2, 8):
        for r in (Fraction(2, 1), Fraction(3, 2), Fraction(5, 3), Fraction(2, 3)):
            assert moran_fixation_ratio(r, n) == r ** (n - 1)
            rho = moran_fixation_probability(r, n)
            assert 0 < rho < 1
        assert moran_fixation_probability(Fraction(1, 1), n) == Fraction(1, n)


def test_origin_fixation_rows_are_exactly_stochastic() -> None:
    for q in (1, 2):
        for state in routing_genotypes(q):
            row = origin_fixation_transition_row(q, state, 4, Fraction(3, 2))
            assert sum(row.values(), Fraction(0, 1)) == 1
            assert all(probability >= 0 for probability in row.values())


def test_exact_stationary_law_satisfies_detailed_balance_and_pi_p_equals_pi() -> None:
    for q in (1, 2):
        pi = stationary_genotype_distribution(q, 4, Fraction(3, 2))
        assert detailed_balance_holds(q, 4, Fraction(3, 2)) is True
        assert stationary_flow_distribution(q, 4, Fraction(3, 2)) == pi


def test_q1_stationary_law_matches_independent_linear_solve() -> None:
    exact = stationary_genotype_distribution(1, 5, Fraction(4, 3))
    solved = _solve_stationary_exact_q1(5, Fraction(4, 3))
    assert solved == exact


def test_gain_layer_degeneracy_matches_direct_enumeration() -> None:
    for q in range(1, 5):
        observed = [0] * (q + 1)
        for state in routing_genotypes(q):
            observed[routing_realized_gain(q, state)] += 1
        expected = gain_layer_degeneracies(q)
        assert tuple(observed) == expected
        assert sum(expected) == routing_genotype_count(q)
        for r in range(q + 1):
            assert expected[r] == gain_layer_degeneracy(q, r)


def test_stationary_layer_distribution_matches_aggregated_genotype_law() -> None:
    q = 2
    n = 4
    a = Fraction(2, 1)
    pi = stationary_genotype_distribution(q, n, a)
    aggregated = [Fraction(0, 1) for _ in range(q + 1)]
    for state, mass in pi.items():
        aggregated[routing_realized_gain(q, state)] += mass
    assert tuple(aggregated) == stationary_layer_distribution(q, n, a)
    assert stationary_tilt(n, a) == 8
    assert gain_layer_degeneracies(q) == (19, 7, 1)
    assert tuple(aggregated) == (Fraction(19, 139), Fraction(56, 139), Fraction(64, 139))


def test_chain_degeneracy_bound_is_sharp_at_nearest_layer() -> None:
    for q in range(1, 9):
        k = q + 1
        a = 2**k - 1
        assert steps_below_full_layer_degeneracy(q, 1) == a
        for s in range(1, q + 1):
            assert degeneracy_chain_bound_holds(q, s) is True
            assert steps_below_full_layer_degeneracy(q, s) <= a**s


def test_full_phase_modal_layer_threshold_is_exact() -> None:
    for q in range(1, 9):
        threshold = full_phase_modal_tilt_threshold(q)
        assert full_phase_is_modal_layer(q, threshold) is True
        assert full_phase_is_modal_layer(q, threshold - 1) is False
        assert full_phase_is_modal_layer(q, threshold + 1) is True


def test_half_mass_window_is_valid() -> None:
    for q in range(1, 8):
        necessary, sufficient = full_phase_half_mass_bounds(q)
        assert necessary == full_phase_modal_tilt_threshold(q)
        assert sufficient == 2 * necessary
        if necessary > 1:
            assert full_phase_stationary_mass_from_tilt(q, necessary - 1) < Fraction(1, 2)
        assert full_phase_stationary_mass_from_tilt(q, sufficient) >= Fraction(1, 2)


def test_canonical_q2_entropy_selection_competition() -> None:
    q = 2
    assert gain_layer_degeneracies(q) == (19, 7, 1)
    assert full_phase_modal_tilt_threshold(q) == 7
    assert full_phase_stationary_mass_from_tilt(q, 7) == Fraction(49, 117)
    assert full_phase_stationary_mass_from_tilt(q, 9) == Fraction(81, 163)
    assert full_phase_stationary_mass_from_tilt(q, 10) == Fraction(100, 189)
    assert full_phase_stationary_mass_from_tilt(q, 9) < Fraction(1, 2)
    assert full_phase_stationary_mass_from_tilt(q, 10) > Fraction(1, 2)
    # Exact half-mass boundary is z^2 = 7z+19, z=e^beta.
    assert 9**2 < 7 * 9 + 19
    assert 10**2 > 7 * 10 + 19


def test_population_size_threshold_for_twofold_fitness_step_is_q_plus_two() -> None:
    for q in range(1, 10):
        assert minimum_population_size_for_modal_full_phase(q, 2) == q + 2
    assert minimum_population_size_for_modal_full_phase(3, 1) is None


def test_receipt_canonical_q2_population_threshold() -> None:
    below = origin_fixation_selection_receipt(2, 3, 2)
    above = origin_fixation_selection_receipt(2, 4, 2)
    assert below.stationary_tilt == 4
    assert below.full_phase_is_modal is False
    assert above.stationary_tilt == 8
    assert above.full_phase_is_modal is True
    assert above.layer_degeneracies == (19, 7, 1)
    assert above.full_phase_stationary_mass == Fraction(64, 139)
    assert above.detailed_balance_verified is True


def test_state_limit_and_validation() -> None:
    with pytest.raises(RoutingStationaryStateLimitError, match="routing genotypes"):
        stationary_genotype_distribution(4, 4, 2, state_limit=100)
    with pytest.raises(ValueError, match="at least 2"):
        moran_fixation_probability(2, 1)
    with pytest.raises(ValueError, match="positive"):
        moran_fixation_probability(0, 4)
    with pytest.raises(ValueError, match="at least one"):
        stationary_tilt(4, Fraction(1, 2))
    with pytest.raises(ValueError, match=r"\[0,q\]"):
        gain_layer_degeneracy(2, 3)
