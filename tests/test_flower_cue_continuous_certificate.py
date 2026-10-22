"""Full-interval policy-envelope proof checks on 64 valid truth tables."""
from fractions import Fraction as F
from adaptive_gain.flower_cue_topology import cue_matrix
from research.wind_route_experiment.continuous_noise_certificate import (
    continuous_certificate,adaptive_policy_lines,fixed_policy_lines,
    formula,at,
)

def test_full_interval_certificate_all_64_has_attainable_segments():
    v=continuous_certificate()
    assert v["n_branch_valid"]==64
    assert v["regime_counts"]=={
        "no_source_value":36,"source_value_fixed_sufficient":4,
        "noise_only_adaptive_value":16,"structural_adaptive_value":8}
    for cls,w in v["examples_with_explicit_affine_policy_witnesses"].items():
        for typ in ("adaptive","fixed"):
            assert len(w[typ]["two_interval_witnesses"])==2

def test_noise_only_gain_exists_at_rationals_not_sampled_in_first_test_grid():
    x,y=cue_matrix(2),cue_matrix(9)
    a=adaptive_policy_lines(x,y)
    fixed=fixed_policy_lines(x,y)
    for e in (F(1,7),F(2,7),F(3,7)):
        assert max(at(line,e) for line in a)==formula("noise_only_adaptive_value","adaptive",e)
        assert max(at(line,e) for line in fixed)==formula("noise_only_adaptive_value","fixed",e)

def test_fixed_only_species_signal_cannot_be_mislabeled_as_order_gain():
    x,y=cue_matrix(6),cue_matrix(9)
    for e in (F(1,7),F(2,7),F(3,7)):
        a=max(at(line,e) for line in adaptive_policy_lines(x,y))
        b=max(at(line,e) for line in fixed_policy_lines(x,y))
        assert a==b==1-e
