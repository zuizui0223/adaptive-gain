import pytest

from adaptive_gain.resource_overlap import resource_role_profile_collision
from adaptive_gain.structural_eco_evolution import (
    evolutionary_selection_activity,
    evolutionary_selection_retention,
    evolutionary_selection_retention_ratio,
    frequency_path,
    structural_selection_path,
)


def test_higher_order_cue_rearrangement_can_drive_reversible_evolution():
    """A repository collision yields activity without long-term retention.

    The two tasks have the same adaptive continuation root type and the same
    multiset of per-resource role profiles, but fixed costs 2 and 3.  At midpoint
    control cost their structural selection coefficients are exactly -1/2,+1/2.
    Alternating those community states therefore moves allele frequency every
    generation while returning it exactly after each two-generation cycle.
    """

    no_gain, strict = resource_role_profile_collision()
    selection = structural_selection_path(
        (strict, no_gain, strict, no_gain),
        lambda_cost=1.0,
        control_cost=0.5,
    )

    assert selection == pytest.approx((0.5, -0.5, 0.5, -0.5))
    assert evolutionary_selection_activity(selection) == pytest.approx(2.0)
    assert evolutionary_selection_retention(selection) == pytest.approx(0.0)
    assert evolutionary_selection_retention_ratio(selection) == pytest.approx(0.0)

    path = frequency_path(0.31, selection)
    assert path[1] != pytest.approx(path[0])
    assert path[2] == pytest.approx(path[0])
    assert path[3] != pytest.approx(path[2])
    assert path[4] == pytest.approx(path[0])
