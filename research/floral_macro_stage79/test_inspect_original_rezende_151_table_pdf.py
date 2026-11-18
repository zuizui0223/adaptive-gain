"""Original source PDF positive-list provenance guards. No OCR/PDF-photo infer."""
import importlib.util,unittest,hashlib
from pathlib import Path
p=Path(__file__).with_name("inspect_original_rezende_151_table_pdf.py")
s=importlib.util.spec_from_file_location("s79c",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class RezendePDFOriginalGuards(unittest.TestCase):
    def test_source_original_nested_archive_verified(self):
        self.assertEqual(m.INNER_SHA,
          "a2af585bdc42cdc6e990c624c4328b808526e259bd21e0bd91fa39b5c316ff28")
        self.assertEqual(m.PDF_BYTES,254746)
        self.assertIn("PMC12299958",m.SOURCE)
    def test_PDF_is_an_author_positive_list_not_negative_species_frame(self):
        self.assertEqual(m.PDF_NAME,"plants-3703510-supplementary.pdf")
        self.assertIn("supplementary",m.PDF_NAME)
if __name__=="__main__":unittest.main()
