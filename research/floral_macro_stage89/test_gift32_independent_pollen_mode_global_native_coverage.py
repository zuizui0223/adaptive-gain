"""Stage89 source identity and absent-as-wind safeguards, source-free."""
import tempfile,unittest,zipfile
from pathlib import Path
from gift32_independent_pollen_mode_global_native_coverage import (
    original_gift_species,SOURCE_MODE,SOURCE_ARTIFACT_SHA,run
)
from global_native_pollination_mode_tdwg3 import summarize_one_region

class GenuineGIFTModeTests(unittest.TestCase):
    def test_source_refuses_fake_original_species_modes(self):
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/"fake.zip"
            with zipfile.ZipFile(f,"w") as z:z.writestr("source","data")
            with self.assertRaises(ValueError):original_gift_species(f)
    def test_gift_original_modes_never_infer_family_from_colour(self):
        self.assertEqual(SOURCE_MODE,{"biotic":"animal","abiotic_wind":"wind"})
        self.assertEqual(len(SOURCE_ARTIFACT_SHA),64)
        src={
           "plant alba":{"colour_documented":True,"hues":("yellow",),
             "explicit_single_hue":"yellow","genus":"plant",
             "positive_spot_text":False,"petal_max_width_cm":None,
             "corolla_tube_max_length_cm":None},
           "plant nigra":{"colour_documented":True,"hues":("brown",),
             "explicit_single_hue":"brown","genus":"plant",
             "positive_spot_text":False,"petal_max_width_cm":None,
             "corolla_tube_max_length_cm":None}}
        rows=summarize_one_region("AAA",set(src),
              {"plant alba":"animal"},src)
        self.assertEqual(rows["wind"]["source_WCVP_native_NHM_species_count"],0)
        self.assertEqual(rows["unknown"]["source_WCVP_native_NHM_species_count"],1)
        self.assertEqual(rows["animal"]["source_WCVP_native_NHM_species_count"],1)
        self.assertEqual(rows["unknown"]["hue_brown_fraction_of_exclusive_documented"],1)
if __name__=="__main__":unittest.main()
