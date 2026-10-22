"""Exact census checks; generated four-world contexts are not empirical samples."""
from fractions import Fraction as F
import pytest

from adaptive_gain.core import World, Query, FiniteTask, adaptive_gain_receipt
from adaptive_gain.flower_cue_topology import (
    cue_matrix, adaptive_score, fixed_score, exact_policy_enumeration,
    catalog, summarize,
)

@pytest.fixture(scope="module")
def cases():
    return catalog(F(1,10))

def test_source_witness_and_strict_routing_original(cases):
    assert cue_matrix(2)==(0,1,0,0)
    assert cue_matrix(11)==(1,1,0,1)
    assert adaptive_score(cue_matrix(2),cue_matrix(11),F(1,10))==F(19,20)
    assert fixed_score(cue_matrix(2),cue_matrix(11),F(1,10))==F(3,4)
    assert adaptive_score(cue_matrix(2),cue_matrix(11),None)==F(3,4)

def test_flower_only_joint_sufficiency_kills_other_species_value():
    a,b=cue_matrix(2),cue_matrix(8)
    assert adaptive_score(a,b,None)==1
    assert adaptive_score(a,b,F(1,10))==1
    assert fixed_score(a,b,F(1,10))==1

def test_heterospecific_cue_can_be_helpful_without_any_adaptivity():
    a,b=cue_matrix(6),cue_matrix(9)
    assert adaptive_score(a,b,None)==F(1,2)
    assert adaptive_score(a,b,F(1,10))==F(9,10)
    assert fixed_score(a,b,F(1,10))==F(9,10)

def test_exact_census_categories(cases):
    s=summarize(cases)
    assert (s['all_pairs'],s['branch_specific_pairs'],s['canonical_oriented_pairs'])==(256,64,16)
    assert (s['all']['gain_none'],s['all']['source_helps_fixed_only'],
            s['all']['strict_adaptive_over_fixed'])==(196,12,48)
    assert (s['branch_specific']['gain_none'],s['branch_specific']['source_helps_fixed_only'],
            s['branch_specific']['strict_adaptive_over_fixed'])==(36,4,24)
    assert s['canonical']['strict_adaptive_over_fixed']==6

def test_all_256_adaptive_dp_equal_exhaustive_independent_policy_tree(cases):
    for row in cases:
        direct=exact_policy_enumeration(row['floral0'],row['floral1'],F(1,10))
        assert row['species_adaptive']==direct, (row['floral0_mask'],row['floral1_mask'])

@pytest.mark.parametrize('e',[F(0),F(1,20),F(1,10),F(1,4),F(2,5),F(1,2)])
def test_four_closed_form_noise_regimes_for_all_64_branch_specific_maps(cases,e):
    for r in cases:
        if not r['correct_branch_specific']:continue
        x,y=r['floral0'],r['floral1']
        if r['other_species_absolute_value']==0:
            pred_a,pred_f=F(1),F(1)
        elif r['strict_sequential_value']==0:
            pred_a=pred_f=1-e
        elif r['strict_sequential_value']==F(1,20):
            pred_a,pred_f=1-e/2,max(1-e,F(3,4))
        else:
            pred_a,pred_f=1-e/2,F(3,4)
        assert (adaptive_score(x,y,e),fixed_score(x,y,e))==(pred_a,pred_f)

def test_optimal_noisy_adaptivity_despite_zero_deterministic_guarantee_gap():
    f0,f1=cue_matrix(2),cue_matrix(9)
    assert (adaptive_score(f0,f1,F(0)),fixed_score(f0,f1,F(0)))==(1,1)
    assert (adaptive_score(f0,f1,F(1,4)),fixed_score(f0,f1,F(1,4)))==(F(7,8),F(3,4))
    assert adaptive_score(f0,f1,F(1,4))-fixed_score(f0,f1,F(1,4))==F(1,8)

def test_unchanged_core_exact_costs_on_all_64_valid_maps(cases):
    from collections import Counter
    counts=Counter()
    extra_noise_only=0
    targets=(0,1,0,1)
    for r in cases:
        if not r['correct_branch_specific']:continue
        t=FiniteTask(
          tuple(World(f'b{i//2}_t{i%2}',targets[i]) for i in range(4)),
          (
            Query('other_species',1,(0,0,1,1)),
            Query('flower0',1,r['floral0']),
            Query('flower1',1,r['floral1']),
            Query('direct_assay',3,targets),
          ))
        ret=adaptive_gain_receipt(t)
        counts[(ret.adaptive_cost,ret.fixed_cost)]+=1
        if ret.adaptive_cost==ret.fixed_cost and r['strict_sequential_value']>0:
            extra_noise_only+=1
    assert counts=={(1,1):28,(2,2):28,(2,3):8}
    assert extra_noise_only==16

def test_maximal_noise_is_no_more_useful_than_no_other_species(cases):
    for r in cases:
        assert adaptive_score(r['floral0'],r['floral1'],F(1,2))==r['baseline_without_species']

@pytest.mark.parametrize('mask',[-1,16,1.2,True])
def test_invalid_truth_table_masks(mask):
    with pytest.raises(ValueError):cue_matrix(mask)

def test_invalid_noise_and_wrong_world_shape():
    with pytest.raises(ValueError):adaptive_score(cue_matrix(2),cue_matrix(11),F(3,5))
    with pytest.raises(ValueError):fixed_score((0,1),cue_matrix(11),F(1,10))
