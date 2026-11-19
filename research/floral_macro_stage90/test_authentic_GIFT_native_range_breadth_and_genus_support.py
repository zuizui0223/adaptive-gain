"""No synthetic source claims: source-free tests of range weighting and unknowns."""
import tempfile,unittest,zipfile
from pathlib import Path
from authentic_GIFT_native_range_breadth_and_genus_support import (
  frozen_stage89_reference,within_region_weighted,REFERENCE_ZIP_SHA
)

class Stage90SourceAndWeightGuards(unittest.TestCase):
    def test_fake_source_accepted_cohort_not_loaded(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"fake.zip"
            with zipfile.ZipFile(path,"w") as z:z.writestr("fake","no source")
            with self.assertRaises(ValueError):frozen_stage89_reference(path)
    def test_inverse_breadth_weight_not_count_as_repeated_evolution(self):
        trait={
          "planta alba":{"explicit_single_hue":"brown"},
          "planta rubra":{"explicit_single_hue":"green"},
          "herba alba":{"explicit_single_hue":"brown"},
          "planta incerta":{"explicit_single_hue":None}}
        weights={"planta alba":10,"planta rubra":1,"herba alba":2,
                 "planta incerta":3}
        family={k:"Dummyaceae" for k in trait}
        d=within_region_weighted(set(trait),trait,weights,family)
        # Among documented three plants, inverse breadth total 0.1+1+0.5=1.6.
        self.assertEqual(d["source_documented_one_hue_species"],3)
        self.assertAlmostEqual(d["source_one_hue_inverse_range_weight_sum"],1.6)
        self.assertAlmostEqual(d["hue_brown_pooled_inverse_native_range"],.6/1.6)
        self.assertAlmostEqual(d["hue_green_pooled_inverse_native_range"],1./1.6)
        # Genus Planta has 0.1 brown, 1 green; Herba all brown.
        self.assertAlmostEqual(d["hue_brown_genus_equal_inverse_native_range"],(.1/1.1+1)/2)
    def test_missing_colour_documentation_never_negative_or_weighted_hue(self):
        traits={"planta alba":{"explicit_single_hue":None}}
        d=within_region_weighted(set(traits),traits,{"planta alba":2},{"planta alba":"Dummyaceae"})
        self.assertEqual(d["source_documented_one_hue_species"],0)
        self.assertIsNone(d["hue_green_pooled_inverse_native_range"])
        self.assertIsNone(d["hue_brown_genus_equal_inverse_native_range"])
    def test_breadth_zero_is_invalid(self):
        with self.assertRaises(ZeroDivisionError):
            within_region_weighted({"planta alba"},{"planta alba":{"explicit_single_hue":"green"}},
                {"planta alba":0},{"planta alba":"Dummyaceae"})

if __name__=="__main__":unittest.main()
