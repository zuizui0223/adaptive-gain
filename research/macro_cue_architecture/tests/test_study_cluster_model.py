"""Test a pure fixed-effects cluster model on synthetic panel data."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'stage0'))
import study_cluster_model as m
import pytest
import math


def test_within_study_slopes_do_not_depend_on_baseline_study_differences():
    rows=[]
    for st,offset in [('A',0.2),('B',0.6),('C',0.1),('D',0.4)]:
        for lag in [1,2,4,8,16,27]:
            imbalance=(lag%3)*0.1+0.04*(lag//4)
            y=offset+0.06*math.log1p(lag)+0.14*imbalance+(ord(st)-65)*.0001*(lag%2)
            rows.append({'study':st,'gap':lag,'imbalance':imbalance,'raw':y,'rarefied':y+0.04})
    r=m.study_fixed_effect_regression(rows,outcome='raw')
    assert r['n_pairs']==24 and r['n_studies']==4
    assert r['beta'][0]==pytest.approx(.06,rel=.2)
    assert r['beta'][1]==pytest.approx(.14,rel=.2)
    assert r['df']==3
    for b,ci in zip(r['beta'],r['ci95_t_cluster_df']):assert ci[0]<=b<=ci[1]
    q=m.study_fixed_effect_regression(rows,outcome='rarefied')
    assert q['beta']==pytest.approx(r['beta'])


def test_refuse_small_number_of_independent_studies():
    with pytest.raises(ValueError,match='3 study'):
        m.study_fixed_effect_regression([{'study':'A','gap':1,'imbalance':.4,'raw':.5,'rarefied':.6}],outcome='raw')
