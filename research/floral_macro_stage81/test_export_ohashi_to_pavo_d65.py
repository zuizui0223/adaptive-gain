import unittest
from pathlib import Path
import tempfile
from unittest.mock import patch
import export_ohashi_to_pavo_d65 as module

class ReceptorSourceExportGuards(unittest.TestCase):
    def test_author_source_sha_is_locked(self):
        self.assertEqual(module.AUTHOR_SHA, "860ad9ef71d99efdda441fae00090ddb1dad0145f5c54a04b581b09490e718b7")
    def test_no_source_original_spectra_persist_in_repo(self):
        self.assertFalse(Path(__file__).with_name("temp_original_28_spectra_wide.csv").exists())
        self.assertFalse(Path(__file__).with_name("temp_original_28_spectra_manifest.csv").exists())
    def test_invalid_source_crosswalk_fails_before_slow_download(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad=Path(tmp)/"crosswalk.json"
            bad.write_text('{"original_full_source_SHA256":"wrong","exact_measured_species_with_2025_EuPP_visit_names":[]}')
            with self.assertRaisesRegex(ValueError, "SOURCE_ZIP_DIGEST_PRIOR_CHANGED"):
                module.build(bad,Path(tmp)/"result")

if __name__=="__main__":
    unittest.main()
