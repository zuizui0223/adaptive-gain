"""Exact small-policy invariants for weather & two source bit information."""
from fractions import Fraction as F
import pytest

from adaptive_gain.multispecies_wind_synergy import (
    optimal, fixed, perfect_formula, two_source_interaction,
    independent_of_target, showcase,
)


def test_32_world_noisy_10percent_exact_2cue_synergy():
    assert [optimal(4,5,bits,F(1,10)) for bits in
            ((),(0,),(1,),(0,1))] == [F(21,32),F(29,40),F(29,40),F(643,800)]
    assert two_source_interaction(4,5,F(1,10)) == F(1,100)
    assert fixed(4,5) == F(21,32)


def test_budget_six_yields_stronger_decision_value():
    assert [optimal(4,6,bits,F(1,10)) for bits in
            ((),(0,),(1,),(0,1))] == [F(11,16),F(25,32),F(25,32),F(181,200)]
    assert two_source_interaction(4,6,F(1,10)) == F(3,100)


@pytest.mark.parametrize("d", [2,3,4])
@pytest.mark.parametrize("budget", [0,1,2,3,4,5])
@pytest.mark.parametrize("r", [0,1,2])
def test_all_adaptive_policies_agree_with_perfect_bit_closed_formula(d,budget,r):
    assert optimal(d,budget,tuple(range(r)),F(0)) == perfect_formula(d,budget,r)


@pytest.mark.parametrize("error", [F(0),F(1,10),F(3,20),F(1,4),F(1,2)])
@pytest.mark.parametrize("joint_type", ["exclusive","independent","fully_shared"])
def test_species_signals_even_jointly_have_zero_marginal_target_information(error,joint_type):
    p={"exclusive":F(0),"independent":error*error,"fully_shared":error}[joint_type]
    assert independent_of_target(4,error,p)


@pytest.mark.parametrize("error", [F(0),F(1,10),F(1,4)])
def test_redundant_same_bit_is_not_distinct_species_information(error):
    assert optimal(4,5,(0,0),error) == optimal(4,5,(0,),error)
    assert optimal(4,5,(0,1),error) > optimal(4,5,(0,0),error)


@pytest.mark.parametrize("error, expected", [(F(0),F(1,32)), (F(1,10),F(1,100)),
                                              (F(1,6),F(0)),(F(1,4),F(-1,128)),
                                              (F(1,2),F(0))])
def test_synergy_is_budget_and_reliability_dependent(error,expected):
    assert two_source_interaction(4,5,error) == expected


def test_correlated_error_sign_change_at_fixed_single_source_quality():
    e=F(3,20)
    assert optimal(4,5,(0,1),e,F(0))==F(61,80)
    assert optimal(4,5,(0,1),e,e*e)==F(2467,3200)
    assert optimal(4,5,(0,1),e,e)==F(131,160)
    assert two_source_interaction(4,5,e,F(0))==F(-1,160)
    assert two_source_interaction(4,5,e,e*e)==F(7,3200)
    assert two_source_interaction(4,5,e,e)==F(1,20)


@pytest.mark.parametrize("budget, expected",[(3,F(-1,32)),(4,F(0)),(5,F(1,32)),(6,F(1,16))])
def test_perfect_joint_species_synergy_budget_threshold(budget,expected):
    assert two_source_interaction(4,budget,F(0))==expected


def test_shorter_hierarchy_cannot_show_positive_pair_interaction_any_budget():
    for d in (2,3):
        for budget in range(1,(1<<d)+2):
            v = perfect_formula(d,budget,2)-2*perfect_formula(d,budget,1)+perfect_formula(d,budget,0)
            assert v <= 0


def test_32_state_reproduction_receipt_and_separate_stochastic_vs_structural_claim():
    receipt=showcase()
    assert receipt["worlds"] == 32
    assert receipt["two_species_joint_target_information_zero"] is True
    assert receipt["budget_5_synergy"] == "1/100"
    assert receipt["scope"].startswith("constructed")


@pytest.mark.parametrize("kwargs", [
    {"d":0,"budget":5,"bits":(0,)},
    {"d":4,"budget":-1,"bits":(0,)},
    {"d":4,"budget":5,"bits":(8,)},
    {"d":4,"budget":5,"bits":(0,),"error":F(3,4)},
    {"d":4,"budget":5,"bits":(0,1),"error":F(1,10),"joint":F(1,5)},
])
def test_invalid_model_configuration_rejected(kwargs):
    with pytest.raises(ValueError):
        optimal(**kwargs)
