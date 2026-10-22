"""Independent synthetic tests for direct-wind original-data implementation."""
import unittest
import numpy as np
import pandas as pd
from direct_wind_analysis import paired_days,permute,holm,flower_subset

def sample():
    return pd.DataFrame([
      {"meadow":"A","SAMPLEDATE":"2015-06-01","PLOT_ID":"P1","WATCH":"1","wind":"ST","year":"2015","bee":2/15,"enemy":1/15},
      {"meadow":"A","SAMPLEDATE":"2015-06-01","PLOT_ID":"P2","WATCH":"1","wind":"BR","year":"2015","bee":3/15,"enemy":3/15},
      {"meadow":"A","SAMPLEDATE":"2015-06-01","PLOT_ID":"P3","WATCH":"1","wind":"ST","year":"2015","bee":1/15,"enemy":1/15},
      {"meadow":"A","SAMPLEDATE":"2015-06-01","PLOT_ID":"P4","WATCH":"1","wind":"BR","year":"2015","bee":2/15,"enemy":1/15},
      {"meadow":"A","SAMPLEDATE":"2015-06-02","PLOT_ID":"P5","WATCH":"1","wind":"ST","year":"2015","bee":0.,"enemy":0.}
    ])

class RoleWindSynthetic(unittest.TestCase):
    def test_mixed_wind_day_is_one_independent_block(self):
        d=paired_days(sample())
        self.assertEqual(len(d),1)
        self.assertAlmostEqual(d.iloc[0].bee_delta,(3+2-2-1)/30)
        self.assertAlmostEqual(d.iloc[0].enemy_delta,(3+1-1-1)/30)
        self.assertAlmostEqual(d.iloc[0].primary_delta,d.iloc[0].enemy_delta-d.iloc[0].bee_delta)

    def test_full_watch_wind_shuffle_retains_three_outcomes(self):
        v=permute(sample(),nrep=199,seed=12)
        self.assertEqual((v["days"],v["meadows"],v["watches"]),(1,1,4))
        self.assertEqual(set(v["outcomes"]),{"bee","enemy","primary"})
        self.assertTrue(all(.0<=d["p_two_sided"]<=1.0 for d in v["outcomes"].values()))

    def test_zero_activity_does_not_generate_false_effect(self):
        a=sample()
        a.loc[:,["bee","enemy"]]=0.
        v=permute(a,nrep=99)
        self.assertEqual(v["outcomes"]["primary"]["delta"],0.)
        self.assertEqual(v["outcomes"]["primary"]["p_two_sided"],1.)

    def test_only_exact_watch_flower_survey_matches(self):
        f=pd.DataFrame({"SAMPLEDATE":["2015-06-01","2015-06-02"],
           "PLOT_ID":["P1","P2"],"WATCH":["1","1"]})
        self.assertEqual(len(flower_subset(sample(),f)),1)

    def test_holm_three(self):
        np.testing.assert_allclose(holm([.02,.01,.5]),[.04,.03,.5])

    def test_one_wind_class_is_not_a_pair(self):
        self.assertTrue(paired_days(sample().query("wind=='ST'")).empty)

if __name__=="__main__":unittest.main()
