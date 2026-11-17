"""Source-free original Dryad version/file source admission tests."""
import hashlib
import importlib.util
import io
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

p=Path(__file__).with_name("resolve_original_Dryad_versions_files.py")
spec=importlib.util.spec_from_file_location("stage73_source",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)


def mock_xlsx():
    with io.BytesIO() as b:
        with zipfile.ZipFile(b,"w",zipfile.ZIP_DEFLATED) as z:
            z.writestr("xl/workbook.xml","<workbook/>")
        return b.getvalue()


class DryadOriginalSourceAdmissionTests(unittest.TestCase):
    def test_original_dataset_and_file_names(self):
        self.assertEqual(len(mod.DOI_FILES),2)
        self.assertIn("flower_color_reflectance_spectra.xlsx",
                      mod.DOI_FILES["xie_island_2025"]["expected"])
        self.assertIn("Data_Albor_etal_2022.xlsx",
                      mod.DOI_FILES["albor_california_2022"]["expected"])

    def test_true_original_workbook_not_spoofed_html(self):
        self.assertEqual(mod.classify_file_bytes(mock_xlsx(),"source.xlsx"),
                         "ORIGINAL_XLSX_OOXML_CONFIRMED")
        self.assertEqual(mod.classify_file_bytes(b"<html>Access</html>","source.xlsx"),
                         "HTTP_SUCCESS_NOT_EXCEL_BINARY")

    def test_wrong_zip_or_html_not_original_spatial_interactions(self):
        self.assertEqual(mod.classify_file_bytes(b"<html>access</html>","plant_bee_interactions_on_islands.zip"),
                         "HTTP_SUCCESS_NOT_ZIP")
        with io.BytesIO() as b:
            with zipfile.ZipFile(b,"w") as z:z.writestr("first.xlsx",mock_xlsx())
            self.assertEqual(mod.classify_file_bytes(b.getvalue(),"plant_bee_interactions_on_islands.zip"),
                             "ORIGINAL_ZIP_CONFIRMED_MEMBER_COUNT_1")

    def test_source_metadata_strong_checksums_match_bytes(self):
        raw=b"Test data"
        d=hashlib.sha256(raw).hexdigest()
        v=mod.receipt("https://datadryad.org/api/v2/files/99/download",raw,d)
        self.assertTrue(v["official_metadata_sha256_matches"])
        self.assertEqual(v["downloaded_source_sha256"],d)
        wrong=mod.receipt("https://datadryad.org/api/v2/files/99/download",raw,"0"*64)
        self.assertFalse(wrong["official_metadata_sha256_matches"])

    def test_no_arbitrary_malicious_URLs(self):
        with self.assertRaisesRegex(ValueError,"NON_ORIGINAL"):
            mod.api_get("https://example.org/myfile.xlsx")
        with self.assertRaisesRegex(ValueError,"NON_ORIGINAL"):
            mod.api_get("file:///etc/passwd")
        with self.assertRaisesRegex(ValueError,"NON_ORIGINAL"):
            mod.api_get("https://datadryad.org/other/file")

    def test_error_cannot_mean_missing_source_ecology(self):
        import urllib.error
        err=urllib.error.HTTPError("https://datadryad.org/api/v2/files/1/download",401,"auth",{},None)
        val=mod.failure(err.url,err)
        self.assertEqual(val["status"],"PUBLIC_FILE_ACCESS_401")
        self.assertTrue(val["no_biological_missingness_inferred"])

    def test_versions_derived_only_from_actual_official_response(self):
        original={
            "_embedded":{"stash:versions":[
                {"id":111,"_links":{"self":{"href":"/api/v2/versions/111"}}},
                {"_links":{"self":{"href":"/api/v2/versions/112"}}}
            ]}
        }
        with patch.object(mod,"json_get",return_value=(original,{"sha":"fake"})):
            found,diag=mod.list_versions("10.5061/dryad.612jm64gq")
        self.assertEqual(found,[111,112])
        self.assertEqual(diag["version_candidate_count"],2)

    def test_file_metadata_source_id_and_source_digest_cannot_be_invented(self):
        original={
          "_embedded":{"stash:files":[
            {"_links":{
              "self":{"href":"/api/v2/files/198"},
              "stash:download":{"href":"/api/v2/files/198/download"}},
             "path":"flower_color_reflectance_spectra.xlsx",
             "size":500,"digestType":"sha-256","digest":"a"*64}
          ]}
        }
        with patch.object(mod,"json_get",return_value=(original,{"sha":"fake"})):
            found,diag=mod.list_file_metadata(332)
        self.assertEqual(found[0]["file_id"],198)
        self.assertEqual(found[0]["digest"],"a"*64)
        self.assertEqual(diag["original_file_metadata_count"],1)

if __name__=="__main__":
    unittest.main()
