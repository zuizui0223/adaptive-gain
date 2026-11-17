"""Synthetic checks of the original 2021 array-pair as inference grain."""
import importlib.util
import unittest
from collections import defaultdict,Counter
from pathlib import Path
from unittest.mock import patch

p=Path(__file__).with_name("recount_original_UVguide_first_choice_by_array_pair.py")
sp=importlib.util.spec_from_file_location("st74d",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class OriginalPairedFirstVisitTests(unittest.TestCase):
    def test_original_visit_count_validation(self):
        self.assertEqual(m.numeric_visitor_count("2"),2)
        self.assertEqual(m.numeric_visitor_count("0"),0)
        self.assertIsNone(m.numeric_visitor_count(""))
        self.assertIsNone(m.numeric_visitor_count("-3"))
        self.assertIsNone(m.numeric_visitor_count("2.2"))
    def test_different_pollinator_rows_not_independent_arrays(self):
        pair={
            ("high","POP","44015","1"): {
                "ambient_uv":{"bee":Counter({"l":8,"s":2}),"fly":Counter({"l":2,"s":0})},
                "reduced_uv":{"bee":Counter({"l":1,"s":5}),"fly":Counter({"l":1,"s":1})},
            },
            ("low","POP","44016","2"): {
                "ambient_uv":{"bee":Counter({"l":1,"s":3})},
                "reduced_uv":{"bee":Counter({"l":2,"s":2})},
            },
        }
        arms=m.normalized_guide_arms(pair)
        self.assertEqual(len(arms),4)
        data=m.paired_treatment_summary(arms)
        self.assertEqual(data["source_original_n_two_arm_pair_keys"],2)
        self.assertEqual(data["source_by_elevation_within_pair_UV_treatment_large_choice"]["high"]["n_positive_diff_pairs"],1)
        self.assertEqual(data["source_by_elevation_within_pair_UV_treatment_large_choice"]["low"]["n_negative_diff_pairs"],1)
    def test_single_guild_or_zero_visits_does_not_impute_preference(self):
        pair={("high","P","10","1"):{
           "ambient_uv":{"bee":Counter({"l":0,"s":0})},
           "reduced_uv":{"fly":Counter({"l":3,"s":1})}}}
        arms=m.normalized_guide_arms(pair)
        d=m.paired_treatment_summary(arms)
        self.assertEqual(d["original_pair_diagnostic_counts"]["source_pairs_with_zero_total_first_visits_in_one_arm"],1)
        self.assertEqual(d["source_by_elevation_within_pair_UV_treatment_large_choice"]["high"]["n_pairs_both_arms_with_known_visits"],0)
    def test_original_source_requires_648_array_flower_guild_rows(self):
        books={"UVLightArrays":{1:{0:"Elevation",1:"FirstVisits"}}}
        with self.assertRaisesRegex(ValueError,"MISSING_CRITICAL"):
            m.summarize_factor_sheet(books,"UVLightArrays")
if __name__=="__main__":
    unittest.main()
