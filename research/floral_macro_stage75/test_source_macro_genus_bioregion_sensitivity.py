"""Source-free genus and bioregion macro evidence and no false causal claims."""
import importlib.util,unittest
from pathlib import Path
from collections import Counter
p=Path(__file__).with_name("source_macro_genus_bioregion_sensitivity.py")
s=importlib.util.spec_from_file_location("stage75b",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class OriginalMacroGenusStudyTests(unittest.TestCase):
    def test_source_precomputed_macro_shas_are_immutable(self):
        self.assertEqual(len(m.SOURCE_UNIT_SHA),64)
        self.assertEqual(len(m.SOURCE_ORIGINAL_SITE_SCORE_SHA),64)
        self.assertEqual(len(m.SOURCE_ORIGINAL_MACRO_RECEIPT_SHA),64)
        with self.assertRaisesRegex(ValueError,"SHA_CHANGED"):
            m.pinned_csv(p,m.SOURCE_UNIT_SHA)

    def test_group_species_network_retains_pre_outcome_frame(self):
        row={
          "color_contrast":"yellow_vs_white",
          "Study_id":"X1","Network_id":"A","Year":"2021",
          "species":"linum perenne","genus":"linum","hue":"white",
          "original_strict_Bombus_species_visit_records":"1",
          "original_strict_other_bee_species_visit_records":"3"}
        f,bee=m.original_data_frame([row])
        self.assertEqual(len(f),1)
        self.assertEqual(bee[(("X1","A","2021"),"linum perenne")]["B"],1)

    def test_duplicate_contrast_plant_source_bee_count_disagreement_is_rejected(self):
        a={"color_contrast":"yellow_vs_white","Study_id":"S",
          "Network_id":"A","Year":"2021","species":"gentiana lutea",
          "genus":"gentiana","hue":"yellow",
          "original_strict_Bombus_species_visit_records":"1",
          "original_strict_other_bee_species_visit_records":"4"}
        b=dict(a,color_contrast="yellow_vs_purple",
               original_strict_Bombus_species_visit_records="2")
        with self.assertRaisesRegex(ValueError,"BEE_COUNTS_INCONSISTENT"):
            m.original_data_frame([a,b])

    def test_original_bioregion_sums_are_descriptive_only(self):
        row={
          "original_hue_source_comparison":"yellow_vs_white",
          "Bioregion":"Atlantic","Country":"Ireland",
          "EuPPollNet_habitat":"Agricultural margins",
          "Study_id":"X1","Network_id":"A","Year":"2021",
          "original_null_score":"2",
          "original_null_information":"5",
        }
        result=m.context_summary([row,row])
        bio=[x for x in result if x["original_field_context_dimension"]=="Bioregion"][0]
        self.assertEqual(bio["original_informative_networks"],2)
        self.assertEqual(bio["original_distinct_study_ids"],1)
        self.assertAlmostEqual(bio["source_null_local_score_ratio_if_information"],0.4)
        self.assertEqual(bio["source_field_context_not_direct_wind_or_climate_Bombus_model"],1)

    def test_genus_is_not_phylogenetic_tree(self):
        self.assertEqual(len(m.CONTRASTS),2)

if __name__=="__main__":
    unittest.main()
