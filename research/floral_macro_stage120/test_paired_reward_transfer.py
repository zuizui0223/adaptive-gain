import unittest
import pandas as pd, numpy as np
from paired_reward_transfer import paired_data,paired_evaluate,aggregate_compatible
class Tests(unittest.TestCase):
    def test_pair_scope(self):
        x=pd.DataFrame({"species":["a a","b b"],"genus":["a","b"],"family":["f","f"],"tube":[1.,2.],"symmetry":["radial","bilateral"],"target":[1.,2.]})
        p=x.copy();p.loc[1,"family"]="g"
        d,bad=paired_data({"nectar":x,"pollen":p})
        self.assertEqual(len(d),1);self.assertEqual(bad,1)
        self.assertEqual(paired_evaluate(d,"genus")["status"],"insufficient_paired_support")
    def test_zero_means(self):
        x=pd.DataFrame({"species":["a a","a a"],"genus":["a","a"],"family":["f","f"],"value":[0.,10.]})
        m=pd.DataFrame({"species":["a a"],"genus":["a"],"family":["f"],"tube":[1.],"symmetry":["radial"]})
        self.assertAlmostEqual(aggregate_compatible(x,m).target.iloc[0],1.)
        self.assertAlmostEqual(aggregate_compatible(x,m,True).target.iloc[0],np.log10(6.))
    def test_same_group_folds(self):
        rng=np.random.default_rng(7);n=80;t=rng.normal(size=n)
        d=pd.DataFrame({"species":[f"sp{i}" for i in range(n)],"genus":[f"g{i//2}" for i in range(n)],"family":[f"f{i//4}" for i in range(n)],"tube":t,"symmetry":np.where(np.arange(n)%2,"radial","bilateral"),"nectar":2*t+rng.normal(size=n)*.1,"pollen":rng.normal(size=n)})
        r=paired_evaluate(d,"family")
        self.assertGreater(r["paired_skill_contrasts"]["tube"]["observed_nectar_minus_pollen_skill"],.5)
if __name__=="__main__":unittest.main()
