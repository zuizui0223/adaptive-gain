from fractions import Fraction

import pytest

from adaptive_gain.routing_mutation_bias_nonidentifiability import (
    neutral_measure_for_target_selected_distribution,
    normalize_positive_distribution,
)
from adaptive_gain.routing_origin_fixation import (
    full_phase_is_modal_layer,
    full_phase_stationary_mass_from_tilt,
    moran_fixation_probability,
    routing_fitness,
)
from adaptive_gain.routing_representation_dependence import compressed_full_phase_mass_from_tilt
from adaptive_gain.routing_reversible_certificate import (
    ReversibleMutationCertificate,
    selected_layer_distribution_from_tilt,
)


def _simple_certificate() -> ReversibleMutationCertificate:
    return ReversibleMutationCertificate(
        gains=(0, 1),
        proposal=((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 2), Fraction(1, 2))),
        neutral_measure=(Fraction(1, 2), Fraction(1, 2)),
        start_state=0,
    )


@pytest.mark.parametrize(
    "call",
    [
        lambda: routing_fitness(1, (0, 0), 1.5),
        lambda: moran_fixation_probability(1.5, 4),
        lambda: full_phase_is_modal_layer(3, 1.5),
        lambda: full_phase_stationary_mass_from_tilt(3, 1.5),
        lambda: compressed_full_phase_mass_from_tilt(2, 1.5),
        lambda: selected_layer_distribution_from_tilt(_simple_certificate(), 1.5),
        lambda: neutral_measure_for_target_selected_distribution((1, 1), 1.5),
        lambda: normalize_positive_distribution((1, 0.5)),
    ],
)
def test_float_inputs_fail_with_explicit_exact_arithmetic_message(call):
    with pytest.raises(TypeError, match=r"Fraction or int; float breaks exact rational arithmetic"):
        call()


def test_bool_is_not_silently_accepted_as_integer():
    with pytest.raises(TypeError, match=r"theta must be Fraction or int"):
        full_phase_is_modal_layer(2, True)


def test_fraction_and_int_inputs_remain_exact_and_supported():
    assert full_phase_is_modal_layer(1, 3) is True
    assert full_phase_stationary_mass_from_tilt(1, Fraction(3, 2)) == Fraction(1, 3)
    assert moran_fixation_probability(Fraction(3, 2), 4) == Fraction(27, 65)
