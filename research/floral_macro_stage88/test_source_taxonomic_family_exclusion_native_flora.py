"""Explicit lineage removal is not an animal-versus-wind species label."""
from __future__ import annotations
import unittest
from source_taxonomic_family_exclusion_native_flora import SCOPES,GRAMINOID,OTHER_WIND_ENRICHED,mode_agnostic_summary

class FamilySpatialExclusionSemantics(unittest.TestCase):
    def test_primary_named_taxonomic_lineages_are_frozen(self):
        self.assertEqual(GRAMINOID,{"Poaceae","Cyperaceae","Juncaceae"})
        self.assertTrue(GRAMINOID<=SCOPES["exclude_three_graminoid_families"])
        self.assertTrue(SCOPES["exclude_three_graminoid_families"]<
                        SCOPES["exclude_graminoid_plus_nine_wind_enriched_families"])
        self.assertIn("Fagaceae",OTHER_WIND_ENRICHED)
    def test_no_false_pollination_mode_declared(self):
        src={"herba alba":{"colour_documented":True,"hues":("white",),
               "explicit_single_hue":"white","genus":"herba",
               "positive_spot_text":False,
               "petal_max_width_cm":None,"corolla_tube_max_length_cm":None}}
        one=mode_agnostic_summary("TST",set(src),src)
        self.assertEqual(one["hue_white_fraction_of_exclusive_documented"],1)
        self.assertEqual(one["source_family_exclusion_not_direct_anemophily_label"],"TRUE")
        self.assertEqual(one["n_source_native_NHM_species"],1)
    def test_unknown_reported_hues_are_not_negative_wind(self):
        src={"herba alba":{"colour_documented":False,"hues":(),
               "explicit_single_hue":None,"genus":"herba",
               "positive_spot_text":False,
               "petal_max_width_cm":None,"corolla_tube_max_length_cm":None}}
        one=mode_agnostic_summary("TST",set(src),src)
        self.assertEqual(one["n_source_single_explicit_hue"],0)
        self.assertEqual(one["hue_green_fraction_of_exclusive_documented"],"")
if __name__=="__main__":unittest.main()
