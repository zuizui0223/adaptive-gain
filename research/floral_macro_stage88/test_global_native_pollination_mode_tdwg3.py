"""Source-free species-level mode attribution, no biological zero imputation."""
import unittest
from global_native_pollination_mode_tdwg3 import norm_mode,recompute_global,summarize_one_region

class Stage88ModeGuards(unittest.TestCase):
    def test_unreported_mode_cannot_be_wind_or_animal(self):
        self.assertEqual(norm_mode(""),"unknown")
        self.assertEqual(norm_mode("unknown"),"unknown")
        self.assertEqual(norm_mode("animal"),"animal")
        self.assertEqual(norm_mode("wind"),"wind")
        with self.assertRaises(ValueError):norm_mode("0")
        with self.assertRaises(ValueError):norm_mode("2")
    def test_author_numeric_mapping_requires_prior_verified_codes(self):
        self.assertEqual(norm_mode("1",{"1":"animal","0":"wind"}),"animal")
        self.assertEqual(norm_mode("0",{"1":"animal","0":"wind"}),"wind")
        with self.assertRaises(ValueError):norm_mode("3",{"1":"animal","0":"wind"})
    @staticmethod
    def fake_traits():
        return {"flora alba":{"colour_documented":True,"hues":("white",),
                     "explicit_single_hue":"white","positive_spot_text":False,
                     "petal_max_width_cm":None,"corolla_tube_max_length_cm":None,
                     "genus":"flora"},
                "flora rubra":{"colour_documented":True,"hues":("red",),
                     "explicit_single_hue":"red","positive_spot_text":True,
                     "petal_max_width_cm":None,"corolla_tube_max_length_cm":None,
                     "genus":"flora"},
                "herba viridis":{"colour_documented":True,"hues":("green",),
                     "explicit_single_hue":"green","positive_spot_text":False,
                     "petal_max_width_cm":None,"corolla_tube_max_length_cm":None,
                     "genus":"herba"}}
    def test_one_region_unknown_separate_mode(self):
        t=self.fake_traits()
        d=summarize_one_region("AAA",set(t),{
            "flora alba":"animal","herba viridis":"wind"},t)
        self.assertEqual(d["animal"]["source_WCVP_native_NHM_species_count"],1)
        self.assertEqual(d["wind"]["source_WCVP_native_NHM_species_count"],1)
        self.assertEqual(d["unknown"]["source_WCVP_native_NHM_species_count"],1)
        self.assertEqual(d["unknown"]["hue_red_fraction_of_exclusive_documented"],1)
        self.assertEqual(d["animal"]["hue_red_fraction_of_exclusive_documented"],0)
        self.assertTrue(d["wind"]["source_unknown_mode_is_missing_NOT_wind"])
    def test_globally_limited_fixture_triggers_source_requirements(self):
        with self.assertRaises(ValueError):
            recompute_global(self.fake_traits(),
                             {"AAA":set(self.fake_traits())},
                             {"flora alba":"animal"}, {})

if __name__=="__main__":unittest.main()
