"""Mock zip tests; no fake bees or botanical ranges appear as science."""
import hashlib
import io
from unittest.mock import patch
import unittest
import zipfile
from inspect_bee_matrix_bundle import (
    fetch_zip_to_temp,_xlsx_sheet_summary,inspect_compact_bee_matrix
)

class AuthenticArchiveGuards(unittest.TestCase):
    def test_untrusted_or_21GB_download_is_no_go(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_NOT_COMPACT"):
            fetch_zip_to_temp("https://zenodo.org/evil",21650768708)
        with self.assertRaisesRegex(ValueError,"NO_GO_UNTRUSTED"):
            fetch_zip_to_temp("https://evil.example.org/archive.zip",100)

    def test_xlsx_schema_only_no_imputed_guide(self):
        contents=io.BytesIO()
        with zipfile.ZipFile(contents,"w") as z:
            z.writestr("xl/workbook.xml",
              '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<sheets><sheet name="UVP" sheetId="1"/></sheets></workbook>')
            z.writestr("xl/worksheets/sheet1.xml",
              '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<dimension ref="A1:C2"/><sheetData><row r="1"><c r="A1"/></row>'
              '<row r="2"><c r="A2"/></row></sheetData></worksheet>')
        x=_xlsx_sheet_summary(contents.getvalue())
        self.assertEqual(x["sheet_names"],["UVP"])
        self.assertEqual(x["worksheets"][0]["row_count_xml"],2)
        self.assertTrue(x["no_original_trait_label_extracted"])

    def test_find_source_P_A_candidate_without_claiming_usable_Bombus(self):
        fake=io.BytesIO()
        with zipfile.ZipFile(fake,"w") as z:
            z.writestr("data/bee_presence_only_matrix_15deg.csv","cell,a\n1,0\n")
        source=fake.getvalue()
        sha="md5:"+hashlib.md5(source).hexdigest()
        meta={"files":[{"key":"data.zip","size":len(source),"checksum":sha,
               "links":{"self":"https://zenodo.org/api/files/mock/data.zip"}}]}
        with patch("inspect_bee_matrix_bundle._get_json",return_value=(meta,"a")),patch(
                   "inspect_bee_matrix_bundle.fetch_zip_to_temp",
                   return_value=(io.BytesIO(source),sha)):
            x=inspect_compact_bee_matrix()
        self.assertEqual(x["n_candidate_PA_matrix_members"],1)
        self.assertTrue(x["not_a_predicted_Bombus_richness_map_yet"])

    def test_missing_matrix_is_reported_not_faked(self):
        z=io.BytesIO()
        with zipfile.ZipFile(z,"w") as w:w.writestr("data/climate.tif","mock")
        v=z.getvalue()
        sha="md5:"+hashlib.md5(v).hexdigest()
        meta={"files":[{"key":"data.zip","size":len(v),"checksum":sha,
               "links":{"self":"https://zenodo.org/api/files/mock/data.zip"}}]}
        with patch("inspect_bee_matrix_bundle._get_json",return_value=(meta,"a")),patch(
                   "inspect_bee_matrix_bundle.fetch_zip_to_temp",
                   return_value=(io.BytesIO(v),sha)):
            x=inspect_compact_bee_matrix()
        self.assertEqual(x["status"],"NO_GO_COMPACT_ZIP_LACKS_READY_PREDICTION_MATRIX")

if __name__=="__main__":
    unittest.main()
