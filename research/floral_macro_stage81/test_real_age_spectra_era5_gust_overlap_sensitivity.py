import tempfile,unittest
from pathlib import Path
import pandas as pd
import real_age_spectra_era5_gust_overlap_sensitivity as m

class ReconstructedSourceWindStageTests(unittest.TestCase):
    def test_paper_declared_site_split(self):
        self.assertEqual(m.publication_id("23_Holzschuh"),m.publication_id("25_Holzschuh"))
        self.assertNotEqual(m.publication_id("4_Marini"),m.publication_id("5_Marini"))
    def test_source_digest_guard(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"source.csv";p.write_text("Study_id,Year\nA,2023\n")
            with self.assertRaisesRegex(ValueError,"ORIGINAL_SOURCE_CSV_SHA_CHANGED"):
                m.source_frame(p,m.ORIGINAL_ERA5_151_SHA)
    def test_counterfactual_small_study_is_not_misreported_as_real_36(self):
        with self.assertRaisesRegex(ValueError,"INDEPENDENT_REAL_SOURCE_COHORT_COUNTS_CHANGED"):
            m.original_frozen_overlap(pd.DataFrame([]),pd.DataFrame([]))
    def test_source_gust_is_fraction_not_velocity(self):
        self.assertIn("fraction_days_10m_gust_ge_15_ms",m.WIND)
        self.assertEqual(m.ORIGINAL_INTERSECTION_PUBLICATIONS,16)
if __name__=="__main__":
    unittest.main()
