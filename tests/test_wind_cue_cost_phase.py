"""Finite cost×noise phase tests. Constructed decision model, not field biology."""
from fractions import Fraction as F
import pytest

from adaptive_gain.multispecies_wind_synergy import (
    optimal, fixed, perfect_cost_formula, costly_two_source_interaction,
)

COSTS=((1,1),(1,2),(2,2),(1,3),(2,3),(3,3))


@pytest.mark.parametrize("d",(2,3,4))
@pytest.mark.parametrize("budget",range(9))
@pytest.mark.parametrize("costs",COSTS)
def test_162_perfect_cost_formula_checks(d,budget,costs):
    assert optimal(d,budget,(0,1),F(0),costs=costs) == perfect_cost_formula(
        d,budget,(0,1),costs)


def test_recover_baseline_32_world_original_accuracy():
    original=optimal(4,5,(0,1),F(1,10))
    assert original==F(643,800)
    assert optimal(4,5,(0,1),F(1,10),costs=(1,1))==original


def test_unequal_query_cost_reverses_source_complementarity():
    low=costly_two_source_interaction(4,5,F(1,10),costs=(1,1))
    high=costly_two_source_interaction(4,5,F(1,10),costs=(1,2))
    assert low["AB"]==F(643,800)
    assert high["AB"]==F(29,40)
    assert low["synergy"]==F(1,100)
    assert high["synergy"]==-F(1,80)
    assert low["AB"]-high["AB"]==F(63,800)
    assert low["synergy"]-high["synergy"]==F(9,400)
    assert high["AB"]==high["A"]
    assert high["AB"]>=high["B"]


def test_both_expensive_is_still_nonharmful_but_subadditive():
    x=costly_two_source_interaction(4,5,F(1,10),costs=(2,2))
    assert x["AB"]==F(107,160)  # .66875
    assert x["synergy"]==-F(1,80)
    assert x["AB"]>=max(x["none"],x["A"],x["B"])


def test_perfect_cost_falsifier():
    cheap=costly_two_source_interaction(4,5,F(0),costs=(1,1))
    costly=costly_two_source_interaction(4,5,F(0),costs=(1,2))
    assert cheap["AB"]==F(7,8) and cheap["synergy"]==F(1,32)
    assert costly["AB"]==F(3,4) and costly["synergy"]==-F(1,32)


@pytest.mark.parametrize("budget",(3,4,5,6,7,8))
@pytest.mark.parametrize("error",(F(0),F(1,10),F(3,20)))
def test_observation_cost_monotonicity_and_optional_species_nonharm(budget,error):
    x=[costly_two_source_interaction(4,budget,error,costs=p)
       for p in ((1,1),(1,2),(2,2))]
    assert x[0]["AB"]>=x[1]["AB"]>=x[2]["AB"]
    for v in x:
        assert v["AB"]>=max(v["A"],v["B"],v["none"])
        assert v["adaptive_vs_fixed"]>=0
        assert fixed(4,budget)==v["none"]


def test_a_second_source_can_become_valuable_again_with_more_time():
    short=costly_two_source_interaction(4,5,F(1,10),costs=(1,2))
    long=costly_two_source_interaction(4,7,F(1,10),costs=(1,2))
    assert short["synergy"]==-F(1,80)
    assert long["synergy"]==F(1,200)


def test_noise_dependence_retained_under_cost_extension():
    error=F(3,20)
    x=[costly_two_source_interaction(4,5,error,q,costs=(1,1))
       for q in (F(0),error**2,error)]
    assert x[0]["synergy"] < 0 < x[1]["synergy"] < x[2]["synergy"]


@pytest.mark.parametrize("bad",((0,1),(1,),(1,-2),(1.5,1)))
def test_invalid_query_costs_are_rejected(bad):
    with pytest.raises(ValueError):
        optimal(4,5,(0,1),F(1,10),costs=bad)
