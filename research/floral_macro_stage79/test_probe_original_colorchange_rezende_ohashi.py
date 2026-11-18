"""Original non-image 151 vs 219 colour-change data provenance guards."""
import importlib.util,unittest,io,zipfile
from pathlib import Path
p=Path(__file__).with_name("probe_original_colorchange_rezende_ohashi.py")
s=importlib.util.spec_from_file_location("stage79a",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class ColourChangePositiveScreenedGuards(unittest.TestCase):
    def test_original_rezende_positive_list_not_other_species_absence(self):
        self.assertEqual(m.REZENDE_DOI,"10.3390/plants14142185")
        self.assertEqual(m.REZENDE_PMID,"PMC12299958")
        self.assertTrue(m.NO_PDF_AUTOPARSE)
    def test_ohashi_219_screened_not_all_219_true_Bee_usable_changes(self):
        self.assertEqual(m.OHASHI_DOI,"10.1111/1365-2435.12420")
        self.assertEqual(m.OHASHI_RECORD,"https://zenodo.org/api/records/4942515")
    def test_bare_text_html_as_author_supplement_not_spreadsheet(self):
        r=m.inventory_archive(b"<html>login</html>")
        self.assertEqual(r["status"],"NOT_AUTHENTIC_ZIP")
        with self.assertRaisesRegex(ValueError,"NOT_REAL_OOXML"):
            m.source_xlsx_schema(b"foo")
    def test_derived_archive_file_names_and_compression_not_guessed(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,"w",zipfile.ZIP_DEFLATED) as z:
            z.writestr("author README.txt","data from original source")
        r=m.inventory_archive(b.getvalue())
        self.assertEqual(r["member_count"],1)
        self.assertIn("original_member_sha256",r["original_source_members"][0])
        self.assertEqual(r["original_source_members"][0]["original_member_kind"],".txt")
    def test_original_api_must_be_authorized_origin(self):
        with self.assertRaisesRegex(ValueError,"NOT_ALLOWED_ORIGINAL"):
            m.request("http://www.ebi.ac.uk/pmc")
        with self.assertRaisesRegex(ValueError,"NOT_ALLOWED_ORIGINAL"):
            m.request("https://example.org/unknown.csv")
if __name__=="__main__":unittest.main()
