"""Stage104 original WFO size bounds and AusTraits measured-source grades."""
import tempfile,unittest,zipfile
from pathlib import Path
from graded_Austraits_and_WFO_interval_mainland_source import (
    original_interval_species,geographic_groups,describe_floral_size_sources)

def wfo_samples():
    return {
      "flora alba":{"status":"bounded_source_range_or_mixed","lower_mm":5.,"upper_mm":7.,
             "contains_bounded_range":True,"contains_original_single_number":False,
             "contains_upper_limit":False,"wide_source_span_needs_review":False},
      "flora rubra":{"status":"upper_limit_only_source_NO_lower_bound","lower_mm":None,"upper_mm":10.,
             "contains_bounded_range":False,"contains_original_single_number":False,
             "contains_upper_limit":True,"wide_source_span_needs_review":False},
      "sylva rubra":{"status":"exact_source_singletons","lower_mm":20.,"upper_mm":20.,
             "contains_bounded_range":False,"contains_original_single_number":True,
             "contains_upper_limit":False,"wide_source_span_needs_review":False},
      "sylva nigra":{"status":"no_eligible_size_evidence","lower_mm":None,"upper_mm":None,
             "contains_bounded_range":False,"contains_original_single_number":False,
             "contains_upper_limit":False,"wide_source_span_needs_review":False},
      "sylva alba":{"status":"bounded_source_range_or_mixed","lower_mm":3.,"upper_mm":30.,
             "contains_bounded_range":True,"contains_original_single_number":False,
             "contains_upper_limit":False,"wide_source_span_needs_review":True},
    }
class SourceGradeGuards(unittest.TestCase):
    def demo(self):
        flora={"AAA":{"flora alba","flora rubra","sylva alba"},
               "BBB":{"flora alba","sylva rubra","sylva nigra"}}
        aus={"flora alba":6.,"sylva alba":12.}
        return flora,aus,wfo_samples(),{"AAA"},{"BBB"}
    def test_union_no_double_species(self):
        flora,aus,wfo,t,h=self.demo()
        groups,rows,cohorts,paired=describe_floral_size_sources(flora,aus,wfo,t,h)
        self.assertEqual(groups["A_original_AusTraits_measured_source"]["global_distinct_accepted_source_species"],2)
        self.assertEqual(groups["B_original_WFO_all_source_bound_evidence_NOT_manual"]["global_distinct_accepted_source_species"],4)
        self.assertEqual(groups["A_and_B_exact_species_overlap"]["global_distinct_accepted_source_species"],2)
        self.assertEqual(groups["A_or_B_total_source_available_NOT_all_measured"]["global_distinct_accepted_source_species"],4)
        self.assertEqual(groups["B_only_not_independent_measurement"]["global_distinct_accepted_source_species"],2)
    def test_upper_only_not_exact_midpoint_or_lower(self):
        flora,aus,wfo,t,h=self.demo()
        groups,rows,cohorts,paired=describe_floral_size_sources(flora,aus,wfo,t,h)
        self.assertEqual(groups["B3_WFO_upper_only_no_lower_bound"]["global_distinct_accepted_source_species"],1)
        self.assertEqual(groups["B4_WFO_original_single_number_lexical"]["global_distinct_accepted_source_species"],1)
    def test_explicit_interval_contains_separate_Austraits_value(self):
        flora,aus,wfo,t,h=self.demo()
        _,_,_,paired=describe_floral_size_sources(flora,aus,wfo,t,h)
        within={r["source_species"]:r["AusTraits_value_within_WFO_reported_size_envelope"] for r in paired}
        self.assertEqual(within,{"flora alba":True,"sylva alba":True})
    def test_holdout_new_source_species_not_same_taxon(self):
        flora,aus,wfo,t,h=self.demo()
        groups,rows,cohorts,paired=describe_floral_size_sources(flora,aus,wfo,t,h)
        v=groups["A_or_B_total_source_available_NOT_all_measured"]
        self.assertEqual(v["source_holdout_37_distinct_species"],2)
        self.assertEqual(v["source_holdout_37_distinct_species_UNSEEN_train"],1)
        self.assertEqual(v["source_holdout_37_exact_species_SHARED_with_train"],1)
    def test_corrupt_stage103_source_ZIP_must_be_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake.csv","untrusted")
            with self.assertRaisesRegex(ValueError,"SOURCE_ARTIFACT_SHA_MISMATCH"):
                original_interval_species(p,{"flora alba"})
    def test_wrong_stage98B_geography_sha_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake.csv","untrusted")
            with self.assertRaisesRegex(ValueError,"SOURCE_ARTIFACT_SHA_MISMATCH"):
                geographic_groups(p,{"AAA":set()})
    def test_measured_Austraits_not_deleted_by_suspect_WFO_span(self):
        flora,aus,wfo,t,h=self.demo()
        _,rows,cohorts,_=describe_floral_size_sources(flora,aus,wfo,t,h)
        train=next(x for x in rows if x["TDWG_L3"]=="AAA")
        self.assertEqual(train["n_WFO_wide_span_flagged_source_species"],1)
        self.assertEqual(train["n_A_original_AusTraits_measured_source"],2)
        self.assertEqual(cohorts["exploration"]["regions_with_10plus_AB_after_removing_wide_source_span"],0)
    def test_only_two_mainland_folds(self):
        flora,aus,wfo,t,h=self.demo()
        _,rows,cohorts,_=describe_floral_size_sources(flora,aus,wfo,t,h)
        self.assertEqual([r["original_source_fixed_fold"] for r in rows],["exploration","holdout"])
        self.assertEqual(cohorts["holdout"]["source_mainland_regions"],1)
if __name__=="__main__":unittest.main()
