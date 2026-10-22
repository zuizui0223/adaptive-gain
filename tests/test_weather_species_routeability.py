"""Fraction-exact counterfactual tests, not field-data effect tests."""
from fractions import Fraction

import pytest

from adaptive_gain.core import adaptive_gain_receipt
from adaptive_gain.weather_species_routeability import (
    optimal_accuracy, fixed_accuracy, branch_target_independence,
    ecological_contexts, example_finite_task, analytic_route_success,
)


@pytest.mark.parametrize("error",[Fraction(i,20) for i in range(11)])
def test_branch_cue_zero_marginal_target_information(error):
    assert branch_target_independence(error)


@pytest.mark.parametrize("error",[Fraction(i,20) for i in range(11)])
def test_noisy_branch_adaptive_advantage_curve_is_exact(error):
    assert optimal_accuracy(2,native_error=error) == 1-error/2
    assert fixed_accuracy(2,native_error=error) == Fraction(3,4)
    assert analytic_route_success(error) == 1-error/2


@pytest.mark.parametrize("wind,species,expected",[
    (False,False,(2,3)),(True,False,(3,3)),
    (False,True,(2,3)),(True,True,(2,3)),
])
def test_deterministic_exact_costs_against_existing_repo_core(wind,species,expected):
    receipt=adaptive_gain_receipt(example_finite_task(wind,species))
    assert (receipt.adaptive_cost,receipt.fixed_cost)==expected
    assert receipt.fixed_cost-receipt.adaptive_cost == (1 if not wind or species else 0)


def test_budget_gate_specifically_two_units():
    for b in (0,1,2,3):
        a=optimal_accuracy(b)
        r=optimal_accuracy(b,heterospecific_error=Fraction(1,10))
        assert r-a == (Fraction(1,5) if b==2 else Fraction(0))


def test_weather_species_factorial_DID_requires_middle_budget():
    rows=ecological_contexts(Fraction(1,20),Fraction(1,10))
    assert {k:rows[k]["adaptive_at_2"] for k in (
        "calm_no_species","calm_species","wind_no_species","wind_species"
    )} == {
        "calm_no_species":Fraction(39,40),
        "calm_species":Fraction(39,40),
        "wind_no_species":Fraction(3,4),
        "wind_species":Fraction(19,20),
    }
    assert rows["species_x_wind_difference_in_differences"]==Fraction(1,5)
    assert all(rows[k]["fixed_at_2"]==Fraction(3,4) for k in (
        "calm_no_species","calm_species","wind_no_species","wind_species"))


def test_more_reliable_router_dominates_costwise():
    assert optimal_accuracy(2,native_error=Fraction(1,8),
                            heterospecific_error=Fraction(1,10))==Fraction(19,20)


@pytest.mark.parametrize("args",[
    (-1,None,None),(1, Fraction(-1,10),None),
    (2,None,Fraction(6,10)),
])
def test_invalid_budget_and_error_rejected(args):
    with pytest.raises(ValueError):
        optimal_accuracy(args[0],native_error=args[1],heterospecific_error=args[2])


def test_weather_may_mask_cue_without_changing_worlds_or_target_labels():
    tasks=[example_finite_task(w,s) for w in (False,True) for s in (False,True)]
    assert len({tuple(w.target for w in t.worlds) for t in tasks})==1
    assert len({tuple(w.name for w in t.worlds) for t in tasks})==1
    assert all(len(t.worlds)==4 and len(t.queries)==5 for t in tasks)


@pytest.mark.parametrize("native_error",[Fraction(i,20) for i in range(11)])
@pytest.mark.parametrize("other_error",[Fraction(j,20) for j in range(11)])
def test_two_branch_cues_use_better_accuracy_or_no_rescue(native_error,other_error):
    adaptive=optimal_accuracy(2,native_error=native_error,
                              heterospecific_error=other_error)
    assert adaptive == Fraction(1)-min(native_error,other_error)/2
    assert fixed_accuracy(2,native_error=native_error,
                          heterospecific_error=other_error)==Fraction(3,4)
    without=optimal_accuracy(2,native_error=native_error)
    assert adaptive-without == max(Fraction(0),(native_error-other_error)/2)
