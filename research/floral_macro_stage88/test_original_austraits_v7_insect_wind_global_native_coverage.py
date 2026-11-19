"""Mock source-free test; field conclusions only from SHA-matched AusTraits."""
from __future__ import annotations
import unittest,tempfile,zipfile
from pathlib import Path
from original_austraits_v7_insect_wind_global_native_coverage import (
    original_long_source_table,pollination_source,ARCHIVE_SHA,ARCHIVE_MD5
)

class AusTraitsSourceAndMeaning(unittest.TestCase):
    def test_known_source_digest_frozen_independent_prior_audit(self):
        self.assertEqual(len(ARCHIVE_SHA),64)
        self.assertEqual(len(ARCHIVE_MD5),32)
    def test_fake_source_not_accepted_as_original_global_mode_panel(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("a.csv","taxon_name,trait_name,value,dataset_id\nRose a,pollination_syndrome,insect,Demo\n")
            with zipfile.ZipFile(p) as z:
                with self.assertRaises(ValueError):original_long_source_table(z)
    def test_missing_original_checksum_not_inferred_from_filename(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"source.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("source","not authenticated")
            with zipfile.ZipFile(p) as z:
                with self.assertRaises(ValueError):pollination_source(z)

if __name__=="__main__":unittest.main()
