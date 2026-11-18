"""Source-free safeguards; real data and checksum are verified separately in CI."""
from __future__ import annotations
import json,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
from export_original_50_stage_spectra import (
    read_verified_stage84,parse_source_spectra
)
from extract_real_ohashi_age_spectral_28 import (
    parse_filename,valid_source_workbook
)

class Stage85Guards(unittest.TestCase):
    def test_non_genuine_source_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"not-authentic.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake","fake")
            with self.assertRaises(ValueError):read_verified_stage84(p)
    def test_author_age_part_replicate_not_plant_species_count(self):
        self.assertEqual(parse_filename("Ohashi-e10o.xls"),("e",10,"o"))
        self.assertEqual(parse_filename("Ohashi-m9c.xls"),("m",9,"c"))
        self.assertEqual(parse_filename("Ohashi-l3.xls"),("l",3,"principal"))
        self.assertIsNone(parse_filename("Ohashi-unknown.xls"))
        self.assertIsNone(parse_filename("Ohashi-e11.xls"))
    def test_mac_appledouble_not_a_source_spectrum(self):
        self.assertTrue(valid_source_workbook("Reflectance/Flower/Flower-e1o.xls"))
        self.assertFalse(valid_source_workbook("__MACOSX/._Flower-e1o.xls"))
        self.assertFalse(valid_source_workbook("Reflectance/Flower/._Flower-e1o.xls"))
    def test_wrong_spectrometer_archive_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("Reflectance/Foo_bar/Foo-e1.xls","FAKE")
            with zipfile.ZipFile(p) as z:
                with self.assertRaises(ValueError):parse_source_spectra(z,["foo bar"])

if __name__=="__main__":unittest.main()
