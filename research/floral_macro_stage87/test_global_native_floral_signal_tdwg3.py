"""Source-free Stage87 guards; numerical findings require actual SHA-verified data."""
import unittest
from global_native_floral_signal_tdwg3 import strict_name,source_hues,numeric_cm,summarize

class GlobalNativeVisualGuards(unittest.TestCase):
    def test_strict_binomial_requires_species(self):
        self.assertEqual(strict_name("Campanula punctata"),"campanula punctata")
        self.assertEqual(strict_name("Cirsium_sieboldii"),"cirsium sieboldii")
        self.assertIsNone(strict_name("Campanula punctata var. punctata"))
        self.assertIsNone(strict_name("Campanula sp."))
    def test_multi_hues_not_absent_other_colors(self):
        a,b=source_hues({"flower colour":"Yellow, occasionally white",
                         "petal colour":"","corolla colour":""})
        self.assertTrue(a)
        self.assertEqual(b,("white","yellow"))
    def test_missing_spot_or_colour_not_negative(self):
        d,h=source_hues({"flower colour":"","corolla colour":"","petal colour":""})
        self.assertFalse(d);self.assertEqual(h,())
        d,h=source_hues({"flower colour":"pale pink with spotted edges"})
        self.assertTrue(d);self.assertEqual(h,("pink",))
    def test_source_typed_max_petal_width(self):
        self.assertAlmostEqual(numeric_cm("4.0 cm"),4.)
        self.assertIsNone(numeric_cm("3 - 4 cm"))
        self.assertIsNone(numeric_cm("not recorded"))
    def test_region_denominator_prose_only_and_genus_balancing(self):
        traits={
          "plant a":{"colour_documented":True,"hues":("yellow",),"explicit_single_hue":"yellow","genus":"plant","positive_spot_text":True,"petal_max_width_cm":2,"corolla_tube_max_length_cm":3},
          "plant b":{"colour_documented":True,"hues":("yellow",),"explicit_single_hue":"yellow","genus":"plant","positive_spot_text":False,"petal_max_width_cm":3,"corolla_tube_max_length_cm":2},
          "shrub c":{"colour_documented":True,"hues":("purple",),"explicit_single_hue":"purple","genus":"shrub","positive_spot_text":False,"petal_max_width_cm":None,"corolla_tube_max_length_cm":None},
        }
        rows,_=summarize({"AAA":set(traits)},traits);r=rows[0]
        self.assertEqual(r["n_source_single_explicit_hue"],3)
        self.assertAlmostEqual(r["hue_yellow_fraction_of_exclusive_documented"],2/3)
        self.assertAlmostEqual(r["hue_yellow_mean_of_genus_fractions"],.5)
        self.assertEqual(r["n_source_positive_spot_word"],1)
        self.assertEqual(r["n_unique_source_native_genera"],2)

if __name__=="__main__":unittest.main()
