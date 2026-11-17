"""Stage72 source-free original archive provenance and XLSX parsing tests."""
import importlib.util
import io
import json
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
p=Path(__file__).with_name("audit_original_field_spectra_visits_sources.py")
s=importlib.util.spec_from_file_location("st72",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def fake_workbook():
    workbook=b'''<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <sheets><sheet name="Field Visitors" sheetId="1" r:id="rId1"/></sheets></workbook>'''
    rel=b'''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
      Target="worksheets/sheet1.xml"/></Relationships>'''
    sheet=b'''<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <dimension ref="A1:C3"/><sheetData>
      <row r="1"><c r="A1" t="inlineStr"><is><t>Plant</t></is></c><c r="B1" t="inlineStr"><is><t>Bee</t></is></c></row>
      <row r="2"><c r="A2" t="inlineStr"><is><t>Genus sp.</t></is></c><c r="B2"><v>2</v></c></row>
      <row r="3"><c r="A3"><v>4</v></c></row>
      </sheetData></worksheet>'''
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("xl/workbook.xml",workbook)
        z.writestr("xl/_rels/workbook.xml.rels",rel)
        z.writestr("xl/worksheets/sheet1.xml",sheet)
    return buf.getvalue()

class OriginalSourceTests(unittest.TestCase):
    def test_real_source_zip_workbook_structure_not_derived_photo(self):
        o=m.xlsx_workbook_metadata(fake_workbook())
        self.assertEqual(len(o),1)
        self.assertEqual(o[0]["sheet_name"],"Field Visitors")
        self.assertEqual(o[0]["source_nonempty_record_rows_in_sheet"],3)
        self.assertEqual(o[0]["preview_first_three_nonempty_rows_first9cells"][0],["Plant","Bee"])
    def test_corrupt_excel_is_not_original_extracted_sheet(self):
        with self.assertRaisesRegex(ValueError,"XLSX_CONTENT_NOT_ZIP"):
            m.xlsx_workbook_metadata(b"xlsx")
    def test_source_metadata_id_is_original_article_not_guessed(self):
        self.assertEqual(m.FIGSHARE_ARTICLE_ID,5663455)
        self.assertEqual(m.ATTRIBUTIONS["kantsa_2018"]["source_reported_visits"],7955)
        self.assertEqual(m.ATTRIBUTIONS["xie_2025"]["source_reported_mainland_sites"],16)
        self.assertEqual(m.ATTRIBUTIONS["albor_2022"]["source_reported_plants"],39)
    def test_only_HTTPS_retrieval_allowed(self):
        with self.assertRaisesRegex(ValueError,"ONLY_HTTPS"):
            m.download_bytes("http://example.org/raw.csv")
        with self.assertRaisesRegex(ValueError,"ONLY_HTTPS"):
            m.download_bytes("file:///etc/passwd")
    def test_403_and_401_do_not_become_trait_absence(self):
        import urllib.error
        e=urllib.error.HTTPError("https://example.org",401,"unauthorized",{},None)
        r=m.failed_receipt("original","https://example.org",e)
        self.assertEqual(r["status"],"SOURCE_OAUTH_REQUIRED_401")
        self.assertTrue(r["no_inferred_plant_species_or_visits"])
    def test_saved_source_hash_is_of_original_bytes(self):
        r=m.source_receipt("original","https://example.org",b"FOO")
        self.assertEqual(r["byte_count"],3)
        self.assertEqual(len(r["original_source_sha256"]),64)
    def test_only_real_handed_out_download_links(self):
        self.assertEqual(m.dataset_files({"files":[{"download_url":"https://a.org/f1"}]}),["https://a.org/f1"])
        self.assertEqual(m.dataset_files({"files":[{"file_id":10}]}),[])

if __name__=="__main__":
    unittest.main()
