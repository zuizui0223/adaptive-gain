"""Stage49 mock-only spreadsheet source probe contracts."""
import io
import unittest
from unittest.mock import patch
import zipfile
from probe_original_published_uv_workbooks import _header_from_excel,_fetch,probe

def fixture():
    book=b'''<?xml version="1.0" encoding="UTF-8"?>
      <workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
      xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <sheets><sheet name="data" sheetId="1" r:id="rId1"/></sheets></workbook>'''
    shared=b'''<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <si><t>species</t></si><si><t>UV_pigment</t></si>
      <si><t>Mockus testii</t></si></sst>'''
    sheet=b'''<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <sheetData>
        <row r="1"><c r="A1" t="s"><v>0</v></c>
                   <c r="B1" t="s"><v>1</v></c></row>
        <row r="2"><c r="A2" t="s"><v>2</v></c>
                   <c r="B2"><v>0.71</v></c></row>
      </sheetData></worksheet>'''
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w") as z:
        z.writestr("xl/workbook.xml",book)
        z.writestr("xl/sharedStrings.xml",shared)
        z.writestr("xl/worksheets/sheet1.xml",sheet)
    return buf.getvalue()

class OriginalStudySourceAudit(unittest.TestCase):
    def test_xlsx_schema_is_inspected_without_biological_classification(self):
        d=_header_from_excel(fixture())
        self.assertEqual(d["sheet_manifest"][0]["name"],"data")
        cells=d["worksheet_first_rows"][0]["first_nine_source_row_cells"]
        self.assertEqual(cells[0][0]["preview"],"species")
        self.assertEqual(cells[1][0]["preview"],"Mockus testii")
        self.assertEqual(cells[1][1]["preview"],"0.71")
        self.assertTrue(d["never_infer_UV_pattern_from_unreviewed_sheet"])

    def test_no_xlsx_acceptance_of_html_source(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_FILE_NOT_GENUINE"):
            _header_from_excel(b"<html>Captcha</html>")

    def test_source_host_allowlist_no_insecure_aliases(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_HOST"):
            _fetch("https://somewhere-untrusted.example/not-a-source")
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_HOST"):
            _fetch("http://datadryad.org/downloads/file_stream/543161")

    def test_403_source_must_remain_unverified(self):
        from urllib.error import HTTPError
        def blocked(url,maxbytes=1_100_000):
            raise HTTPError(url,403,"Forbidden",{},None)
        with patch("probe_original_published_uv_workbooks._fetch",
                   side_effect=blocked):
            result=probe()
        self.assertTrue(result["no_independent_177_plus_177_double_count"])
        for r in result["sources"].values():
            self.assertIsNone(r["workbook"])
            self.assertEqual(
                 r["attempts"][0]["status"],
                 "SOURCE_NOT_RETRIEVED_OR_INVALID_NO_SPECIES_CLAIM"
            )

if __name__=="__main__":
    unittest.main()
