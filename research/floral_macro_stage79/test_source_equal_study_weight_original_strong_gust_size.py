"""Original-study equal-weight size–gust source support guard tests."""
import importlib.util,unittest
from pathlib import Path
import numpy as np,pandas as pd
sp=importlib.util.spec_from_file_location("stage79k",Path(__file__).with_name("source_equal_study_weight_original_strong_gust_size.py"))
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class StudyEqualWeightTests(unittest.TestCase):
    def test_original_study_information_must_sum_one_each(self):
        d=pd.DataFrame({"Study_id":["A","A","B","B","B"],
            "original_source_width_local_null_information":[100.,2.,3.,3.,3.]})
        result=m.normalize_original_studies(d)
        t=result.groupby("Study_id")["source_equal_study_information_weight"].sum()
        self.assertAlmostEqual(t["A"],1.)
        self.assertAlmostEqual(t["B"],1.)
        self.assertAlmostEqual(result.loc[0,"source_equal_study_information_weight"],100/102)
    def test_study_with_zero_information_rejected(self):
        d=pd.DataFrame({"Study_id":["A"],"original_source_width_local_null_information":[0.]})
        with self.assertRaisesRegex(ValueError,"ZERO_SOURCE_INFORMATION"):
            m.normalize_original_studies(d)
    def test_within_study_simple_wind_slope_not_a_causal_path(self):
        d=pd.DataFrame({
            "Study_id":["A","A","B","B"],
            m.MAIN:[0.,2.,1.,3.],
            "original_source_width_null_score_ratio":[0.,1.,1.,0.],
            "original_source_width_local_null_information":[1.,1.,1.,1.]})
        source=m.within_study_simple_slopes(d)
        self.assertEqual(len(source),2)
        self.assertAlmostEqual(source[0]["source_simple_original_within_study_null_score_gust_slope"],.5)
        self.assertAlmostEqual(source[1]["source_simple_original_within_study_null_score_gust_slope"],-.5)
        self.assertTrue(all(x["source_not_adjusted_for_network_TP_climate_or_taxon"] for x in source))
    def test_study_equal_weight_scientific_no_confirmatory_prior(self):
        self.assertEqual(m.MIN_STUDIES,10)
        self.assertEqual(m.MIN_WIND_VARYING,5)
        self.assertIn("not a new primary",m.__doc__.lower())

if __name__=="__main__":unittest.main()
