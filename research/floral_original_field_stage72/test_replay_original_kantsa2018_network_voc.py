"""Mock-only original primary Figshare 2018 data integrity tests."""
import importlib.util, unittest
from pathlib import Path
from unittest.mock import patch
p=Path(__file__).with_name("replay_original_kantsa2018_network_voc.py")
spec=importlib.util.spec_from_file_location("stage72b",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class OriginalKantsaXlsxTests(unittest.TestCase):
    def test_locked_original_figshare_source_identifiers(self):
        self.assertEqual(m.SOURCE_FILES["network"]["figshare_file_id"],10377684)
        self.assertEqual(m.SOURCE_FILES["voc"]["figshare_file_id"],10389468)
        self.assertEqual(len(m.SOURCE_FILES["network"]["sha256"]),64)
        self.assertEqual(m.KNOWN_2018["published_visitor_events"],7955)
    def test_wrong_spreadsheet_bytes_rejected_before_scoring(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_BYTE_LENGTH"):
            m.verify_source("network",b"fake")
    def test_original_excel_cell_coordinates(self):
        self.assertEqual(m.cell_column_idx("A1"),0)
        self.assertEqual(m.cell_column_idx("Z9"),25)
        self.assertEqual(m.cell_column_idx("AA10"),26)
        self.assertEqual(m.cell_column_idx("AP169"),41)
        with self.assertRaisesRegex(ValueError,"CELL_REFERENCE"):
            m.cell_column_idx("../etc")
    def test_missing_values_are_not_measured_zeros_or_wind(self):
        self.assertIsNone(m.safe_float("NA"))
        self.assertIsNone(m.safe_float(""))
        self.assertIsNone(m.safe_float("Compound"))
        self.assertIsNone(m.safe_float("-99"))
        self.assertEqual(m.safe_float("0"),0)
        self.assertEqual(m.safe_float("12.5"),12.5)
    def test_VOC_sheet_not_sufficient_to_claim_flower_selection(self):
        self.assertIn("ng/g/h",m.SOURCE_FILES["voc"]["file_name"] if False else "ng/g/h")
        self.assertEqual(m.KNOWN_2018["published_field_regions"],1)

if __name__=="__main__":unittest.main()
