import unittest
import numpy as np,pandas as pd
from budgeted_reward import species,read_table,evaluate,routed,inner_select
class TestBudget(unittest.TestCase):
    def test_exact_names(self):
        self.assertEqual(species("Abutilon_regnelli"),"abutilon regnelli")
        self.assertIsNone(species("Abelia_x_grandiflora"))
    def test_synthetic_cv_and_cost(self):
        rng=np.random.default_rng(3);n=120
        s=np.where(np.arange(n)%2==0,"radial","bilateral")
        t=rng.normal(size=n);h=np.where(rng.random(n)>.5,"A","B")
        y=np.where(s=="radial",2*t,(h=="A")*3)+rng.normal(size=n)*.15
        d=pd.DataFrame({"symmetry":s,"tube":t,"shape":h,"target":y,"genus":[f"g{i//4}" for i in range(n)],"family":[f"f{i//8}" for i in range(n)]})
        r=evaluate(d,"genus",("tube","shape"))
        self.assertEqual(r["status"],"estimated_exploratory")
        self.assertEqual(sum(x["n_test"] for x in r["folds"]),n)
        self.assertGreater(r["adaptive_relative_mse_gain_vs_routed_fixed"],0)
        self.assertTrue(all(set(x["adaptive_second"])=={"radial","bilateral"} for x in r["folds"]))
    def test_sparse_cohort_gate(self):
        d=pd.DataFrame({"symmetry":["radial"]*10,"genus":["g"]*10})
        self.assertEqual(evaluate(d,"genus",("tube","shape"))["status"],"insufficient_support")
if __name__=="__main__":unittest.main()
