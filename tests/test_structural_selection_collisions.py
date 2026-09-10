import pytest

from adaptive_gain.resource_overlap import resource_role_profile_collision
from adaptive_gain.structural_eco_evolution import structural_selection_state


def test_same_continuation_and_role_profiles_can_reverse_structural_selection():
    """Existing information-loss collision becomes an evolutionary counterexample.

    resource_role_profile_collision() registers two tasks with the same adaptive
    continuation root type and the same multiset of complete per-resource role
    profiles, while exact fixed costs differ 2 versus 3.  Since both adaptive
    costs are 2, a midpoint constitutive control cost reverses selection on the
    contingent architecture despite those weaker structural summaries matching.
    """

    no_gain, strict = resource_role_profile_collision()
    no_gain_state = structural_selection_state(
        no_gain, lambda_cost=1.0, control_cost=0.5
    )
    strict_state = structural_selection_state(
        strict, lambda_cost=1.0, control_cost=0.5
    )

    assert no_gain_state.adaptive_cost == 2
    assert strict_state.adaptive_cost == 2
    assert no_gain_state.fixed_cost == 2
    assert strict_state.fixed_cost == 3
    assert no_gain_state.log_fitness_ratio == pytest.approx(-0.5)
    assert strict_state.log_fitness_ratio == pytest.approx(0.5)

    assert no_gain_state.log_fitness_ratio < 0 < strict_state.log_fitness_ratio
