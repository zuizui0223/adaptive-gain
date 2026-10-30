import unittest
import numpy as np
import pandas as pd
import statsmodels.api as sm
from association import within_plant, design, clustered_ols, contrast

class AssociationTests(unittest.TestCase):
    def test_within_plant_not_between_species_reward(self):
        d=pd.DataFrame({'plant':['A','A','B','B'],'wind':[0.,2.,3.,5.],'energy_j':[1.,3.,10.,20.]})
        z,scale=within_plant(d)
        np.testing.assert_allclose(z.groupby('plant')[['w','r']].mean(),0.,atol=1e-12)
        self.assertGreater(scale,0)
    def test_cr1_matches_independent_statsmodels(self):
        rng=np.random.default_rng(771)
        X=np.c_[np.ones(200),rng.normal(size=(200,4))]
        group=np.repeat(np.arange(40),5)
        y=X@np.array([1.,.2,-.4,.3,.6])+rng.normal(size=200)+rng.normal(size=40)[group]
        ours=clustered_ols(X,y,group)
        ref=sm.OLS(y,X).fit(cov_type='cluster',cov_kwds={'groups':group,'use_correction':True},use_t=True)
        np.testing.assert_allclose(ours['beta'],ref.params,rtol=1e-10,atol=1e-10)
        np.testing.assert_allclose(ours['cov'],ref.cov_params(),rtol=1e-9,atol=1e-10)
        c=contrast(ours,np.array([0,1,0,0,0]))
        self.assertAlmostEqual(c['coefficient'],ref.params[1])
        self.assertAlmostEqual(c['p_two_sided'],ref.pvalues[1],places=10)
    def test_rank_failure_is_not_silent_column_deletion(self):
        X=np.ones((10,2))
        with self.assertRaisesRegex(ValueError,'RANK'): clustered_ols(X,np.arange(10.),np.arange(10))
    def test_design_contains_only_one_primary_interaction(self):
        d=pd.DataFrame({'plant':['A','A','B','B'],'site':['X','Y','X','Y'],'w':[0.,1.,0.,1.],'r':[1.,-1.,1.,-1.],
          'temperature':[20]*4,'blue_sky':[50]*4,'date':['2024-04-01']*4,'flower_density':[100]*4})
        X,names=design(d)
        self.assertEqual(names.count('w:r'),1)
        np.testing.assert_allclose(X[:,names.index('w:r')],d.w*d.r)
        self.assertNotIn('probes',names)
    def test_interaction_recovery_without_noise(self):
        rng=np.random.default_rng(37);n=120
        w=rng.normal(size=n);r=rng.normal(size=n)
        X=np.c_[np.ones(n),w,r,w*r]
        fit=clustered_ols(X,X@np.array([2.,-.1,.2,.3]),np.repeat(np.arange(40),3))
        self.assertAlmostEqual(fit['beta'][-1],.3,places=12)

if __name__=='__main__':unittest.main()
