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
            rows.append({'study':st,'site':st+'_'+str(lag%2),'gap':lag,'imbalance':imbalance,'raw':y,'rarefied':y+0.04})
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


def test_site_fixed_effect_adjustment_runs_with_study_clustered_uncertainty():
    rows=[]
    for st in ['A','B','C','D']:
        for site in [st+'_1',st+'_2']:
            for gap in [1,5,12,20]:
                z=(gap%3)*.12
                y=.1+(.12 if site.endswith('_2') else 0)+.035*math.log1p(gap)+.04*z
                rows.append({'study':st,'site':site,'gap':gap,'imbalance':z,'raw':y,'rarefied':y+.01})
    r=m.study_fixed_effect_regression(rows,outcome='rarefied',fixed_effects='site')
    assert r['fixed_effects']=='site'
    assert r['n_pairs']==32 and r['n_studies']==4 and r['n_fixed_effect_groups']==8
    assert r['beta']==pytest.approx([.035,.04],abs=1e-10)


def test_reject_wrong_fixed_effect_layer():
    with pytest.raises(ValueError,match='fixed_effects'):
        m.study_fixed_effect_regression([],outcome='raw',fixed_effects='unknown')
