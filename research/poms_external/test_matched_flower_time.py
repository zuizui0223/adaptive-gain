"""Independent exact-kernel and matching checks; no source download needed."""
import unittest
import numpy as np
import pandas as pd
from matched_flower_time import exact_conditional_2x2, bh, select_strata, analyze_panel, GUILDS

class ExactMatchedTests(unittest.TestCase):
    def test_no_visitors_cannot_test_plant_month_interaction(self):
        self.assertIsNone(exact_conditional_2x2(np.zeros((2,2),dtype=int),np.ones((2,2))))

    def test_uniform_exposure_strong_association(self):
        obs=exact_conditional_2x2(np.array([[9,1],[1,9]]),np.ones((2,2)))
        self.assertLess(obs["p"],.01)
        self.assertGreater(obs["log_interaction_or"],0)

    def test_exposure_odds_compensates_raw_counts(self):
        r=exact_conditional_2x2(np.array([[8,4],[4,8]]),np.array([[2,1],[1,2]],float))
        self.assertGreater(r["p"],.15)
        self.assertLess(abs(r["log_interaction_or"]),.06)

    def test_invalid_exposure_fails_closed(self):
        with self.assertRaises(ValueError):
            exact_conditional_2x2(np.array([[2,3],[4,5]]),np.array([[1,0],[1,1]]))

    def test_bh_is_conservative(self):
        q=bh([.05,.001,.4])
        self.assertAlmostEqual(q[1],.003)
        self.assertGreaterEqual(q[0],.05)
        self.assertGreaterEqual(q[2],.4)

    def test_crossed_support_needs_same_two_plants_in_two_months(self):
        d=pd.to_datetime(["2022-05-01","2022-05-01","2022-07-01","2022-07-01"])
        df=pd.DataFrame({"site":["A"]*4,"year":[2022]*4,"month":[5,5,7,7],
            "plant":["Aster","Buddleja","Aster","Buddleja"],"date":d,
            "units":["flower head"]*4,"flowers":[10.,10.,12.,12.]})
        for g in GUILDS:df[g]=[1,2,3,4]
        r=select_strata(df)
        self.assertEqual(len(r),1)
        self.assertEqual(r[0]["cell_survey_counts"],[1,1,1,1])
        self.assertTrue(r[0]["within_7_days_both_months"])
        self.assertEqual(r[0]["cell_values"]["bumblebees"],[[1,2],[3,4]])

    def test_no_common_months_is_not_crossed(self):
        d=pd.to_datetime(["2022-05-01","2022-06-01","2022-07-01","2022-08-01"])
        df=pd.DataFrame({"site":["A"]*4,"year":[2022]*4,"month":[5,6,7,8],
            "plant":["Aster","Aster","Buddleja","Buddleja"],"date":d,
            "units":["flower head"]*4,"flowers":[10.]*4})
        for g in GUILDS:df[g]=[1,2,3,4]
        self.assertEqual(len(select_strata(df)),0)

    def test_one_independent_site_year_selection(self):
        a={"site":"A","year":2022,"surveys":4,"cell_survey_counts":[1]*4,
           "within_7_days_both_months":True,"flower_unit_exposures":[[2,2],[2,2]],
           "survey_exposures":[[1,1],[1,1]],
           "cell_values":{g:[[1,1],[1,1]] for g in GUILDS}}
        b={**a,"year":2023,"surveys":8,"cell_survey_counts":[2]*4}
        r=analyze_panel([a,b],"surveys",only_one_site_year=True)
        self.assertEqual(r["independent_sites"],1)
        self.assertEqual(r["sampled_site_years"],1)
        self.assertEqual(r["survey_rows_in_selected_2x2"],8)

if __name__=="__main__":unittest.main()
