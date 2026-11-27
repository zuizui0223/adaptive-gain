import unittest
import numpy as np,pandas as pd
from regional_reward_transfer import skill,region_test,macro_fit
class Tests(unittest.TestCase):
    def test_pair_contrast_removes_intercept_shift(self):
        y=np.array([1.,2.,3.,4.]);p=y+20
        r=skill(y,p,np.repeat(2.,4))
        self.assertAlmostEqual(r["within_assemblage_pair_contrast_skill"],1)
        self.assertLess(r["transfer_skill_vs_training_mean"],0)
        self.assertAlmostEqual(r["kendall_tau_b"],1)
    def test_constant_target_abstention(self):
        self.assertIsNone(skill([2.,2.],[1.,2.],[2.,2.])["within_assemblage_pair_contrast_skill"])
    def test_all_local_genera_are_excluded(self):
        rng=np.random.default_rng(11);n=120;t=rng.normal(size=n)
        d=pd.DataFrame({"species":[f"s{i}" for i in range(n)],"genus":[f"g{i//2}" for i in range(n)],"family":[f"f{i//4}" for i in range(n)],"tube":t,"nectar":2*t,"pollen":rng.normal(size=n)})
        local=set(d.iloc[:40:2].species)
        r,_=region_test(d,local,"genus",("nectar","pollen"))
        self.assertEqual(r["status"],"estimated_exploratory")
        self.assertEqual(r["n_train"],80)
        self.assertGreater(r["outcomes"]["nectar"]["within_assemblage_pair_contrast_skill"],.9)
    def test_insufficient_support(self):
        d=pd.DataFrame({"species":["s1"],"genus":["g1"],"family":["f1"]})
        self.assertEqual(region_test(d,{"s1"},"genus",("nectar",))[0]["status"],"insufficient_local_cohort")
if __name__=="__main__":unittest.main()
