"""Source-free original 2021 file ID and study-design provenance tests."""
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

p=Path(__file__).with_name("inspect_original_2021_UVguide_field_workbook.py")
sp=importlib.util.spec_from_file_location("st74c",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)


class UVGuideOriginalWorkbookTests(unittest.TestCase):
    def test_three_original_author_original_source_files_digest_pinned(self):
        self.assertEqual(len(m.PIN),3)
        self.assertEqual(m.PIN["FinnKosk_PollData_Final.xlsx"]["size"],67593)
        self.assertEqual(len(m.PIN["ColorContrastData.xlsx"]["sha256"]),64)
        self.assertEqual(len(m.PIN["Spectra Used for Vismodels.zip"]["sha256"]),64)
    def test_original_missing_zenodo_file_fails_closed(self):
        with (patch.object(m,"manifest_meta",return_value=({"files":[]} ,{})),
              patch.object(m,"record_files_metadata",return_value=[])):
            with self.assertRaisesRegex(ValueError,"LISTING_MISSING"):
                m.run()
    def test_original_file_not_replaced_by_abstract_claim(self):
        with patch.object(m,"pick_original_download_url",return_value=None):
            with self.assertRaisesRegex(ValueError,"NO_ORIGINAL_DOWNLOAD_LINK"):
                m.safe_source_download({"key":"FinnKosk_PollData_Final.xlsx"})
    def test_source_original_archive_not_guessed_to_have_visitor_records(self):
        self.assertEqual(m.REFERENCE_DOI,"10.5281/zenodo.5110165")
        self.assertEqual(m.PUBLICATION_DOI,"10.1111/nph.17631")
    def test_source_original_byte_authentication_rejects_corrupt(self):
        fake={"key":"FinnKosk_PollData_Final.xlsx",
              "checksum":"md5:2cd6ee2c70b0bde53fbe6cac3c8b8bb1"}
        with (patch.object(m,"pick_original_download_url",return_value="https://zenodo.org/f"),
              patch.object(m,"get",return_value=(b"bad","https://zenodo.org/f","octet"))):
            with self.assertRaisesRegex(ValueError,"SOURCE_BYTES_CHANGED"):
                m.safe_source_download(fake)
if __name__=="__main__":
    unittest.main()
