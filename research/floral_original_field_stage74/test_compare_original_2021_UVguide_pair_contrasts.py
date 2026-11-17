"""Mock-only paired design tests before real 377 original visits analysis."""
import importlib.util,unittest
from pathlib import Path
p=Path(__file__).with_name("compare_original_2021_UVguide_pair_contrasts.py")
sp=importlib.util.spec_from_file_location("s74e",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class OriginalStudyArrayPairTests(unittest.TestCase):
    def test_original_first_visit_source_pinned(self):
        self.assertEqual(len(m.SOURCE_SHA),64)
        self.assertEqual(m.BOOTSTRAPS,5000)
    def test_bad_source_sha_fails(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_SHA"):
            m.source_verified_pair_frame({"source_workbook_sha256":"bad"})
    def test_fake_source_377_not_admitted(self):
        with self.assertRaisesRegex(ValueError,"NOT_377"):
            m.source_verified_pair_frame({
                "source_workbook_sha256":m.SOURCE_SHA,
                "original_UV_light_factor_source_grain":{
                  "source_raw_first_visit_counts_sum":0}})
    def test_pair_bootstrap_returns_deterministic_nonparametric_interval(self):
        first=m.bootstrap_ci([0.0,0.5,-0.25,1.0],nboot=250,seed=7)
        second=m.bootstrap_ci([0.0,0.5,-0.25,1.0],nboot=250,seed=7)
        self.assertEqual(first,second)
        self.assertLessEqual(first[0],first[1])
    def test_missing_all_pair_changes_has_no_invented_ci(self):
        self.assertIsNone(m.bootstrap_ci([],nboot=250))
    def test_original_arrays_not_replaced_with_648_source_rows(self):
        fake={
          "source_workbook_sha256":m.SOURCE_SHA,
          "original_UV_light_factor_source_grain":{
            "source_raw_first_visit_counts_sum":377,
            "original_distinct_randomized_array_ids":648},
        }
        with self.assertRaisesRegex(ValueError,"ARRAYS_NOT_54"):
            m.source_verified_pair_frame(fake)
if __name__=="__main__":
    unittest.main()
