import unittest
import numpy as np
from reward_species_null import fit_slope,evaluate_scores
class Tests(unittest.TestCase):
    def test_ridge_slope(self):
        x=np.arange(10.);y=2*x+3
        self.assertAlmostEqual(fit_slope(x,y),2/(1+5/10))
    def test_pair_skill_and_tau(self):
        x=np.arange(10.);y=(2*x+3)[None,:]
        s,t=evaluate_scores(x,y,np.arange(6),np.arange(6,10))
        self.assertAlmostEqual(s[0],1-(1-1/(1+5/6))**2)
        self.assertAlmostEqual(t[0],1.)
    def test_constant_outcome(self):
        x=np.arange(10.);y=np.ones((1,10))
        s,t=evaluate_scores(x,y,np.arange(6),np.arange(6,10))
        self.assertTrue(np.isnan(s[0]))
if __name__=='__main__':unittest.main()
