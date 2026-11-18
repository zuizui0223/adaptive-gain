import io,unittest,zipfile
import numpy as np
import extract_real_ohashi_age_spectral_28 as m
from unittest.mock import patch

class SourceAgeSpectrumTests(unittest.TestCase):
    def test_ignore_mac_appledouble_ghosts(self):
        self.assertTrue(m.valid_source_workbook("Ohashi/Reflectance/A/A-e1o.xls"))
        self.assertFalse(m.valid_source_workbook("Ohashi/Reflectance/A/._A-e1o.xls"))
        self.assertFalse(m.valid_source_workbook("__MACOSX/Reflectance/A/A-e1o.xls"))
    def test_author_age_replicate_and_part_semantics(self):
        self.assertEqual(m.parse_filename("Wisteria_floribunda-l10sc.xls"),("l",10,"sc"))
        self.assertEqual(m.parse_filename("Abelia_spathulata-e1.xls"),("e",1,"principal"))
        self.assertEqual(m.parse_filename("foo-e15.xls"),None)
        self.assertEqual(m.parse_filename("._foo-e2c.xls"),("e",2,"c"))
        # Above last filename is rejected by valid_source_workbook, not parse_filename.
    def test_identical_early_late_means_are_not_color_change(self):
        e=np.tile(np.linspace(4.,35.,401),(10,1))
        l=e.copy()
        r=m.measured_early_late_metrics(e,l,permutations=39)
        self.assertAlmostEqual(r["raw_reflectance_early_late_RMS_percent_points"],0)
        self.assertEqual(r["raw_spectrum_permutation_p_999_not_bee_colour"],1)
    def test_signed_band_early_to_late(self):
        e=np.full((10,401),12.);l=np.full((10,401),23.)
        r=m.measured_early_late_metrics(e,l,seed=1,permutations=99)
        self.assertAlmostEqual(r["raw_reflectance_early_late_RMS_percent_points"],11)
        self.assertAlmostEqual(r["raw_early_late_signed_delta_UV300_399_percent_points"],11)
        self.assertAlmostEqual(r["raw_early_late_signed_delta_green500_599_percent_points"],11)
    def test_stage_is_independent_samples_not_paired(self):
        e=np.zeros((4,401))
        l=np.ones((5,401))*10
        r=m.measured_early_late_metrics(e,l,permutations=99)
        self.assertEqual(r["n_early_independent_original_plant_samples"],4)
        self.assertEqual(r["n_late_independent_original_plant_samples"],5)

if __name__=="__main__":unittest.main()
