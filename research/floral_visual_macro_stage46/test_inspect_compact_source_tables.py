"""No actual source files in mock unit tests."""
import unittest
from unittest.mock import patch
from inspect_compact_source_tables import (
    original_bytes,source_text_files,dryad_file_manifest
)

class CompactSourceTests(unittest.TestCase):
    def test_disallows_large_untrusted_urls(self):
        for x in ("http://zenodo.org/api/files/file",
                  "https://zenodo.org.example.org/evil"):
            with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_SOURCE_HOST"):
                original_bytes(x)

    def test_original_readme_sha_checked_and_scoped(self):
        import hashlib
        raw=b"data.zip and PA_mat and Bombus"
        declared="md5:"+hashlib.md5(raw).hexdigest()
        obj={"files":[{"key":"readme.txt",
            "links":{"self":"https://zenodo.org/api/files/x/readme.txt"},
            "checksum":declared}]}
        with patch("inspect_compact_source_tables._get_json",
                   return_value=(obj,"meta")),patch(
              "inspect_compact_source_tables.original_bytes",return_value=raw):
            x=source_text_files()
        self.assertIn("readme.txt",x)
        self.assertIn("Bombus",x["readme.txt"]["relevant_keywords"])

    def test_corrupt_original_text_checksum_fails(self):
        obj={"files":[{"key":"readme.txt",
            "links":{"self":"https://zenodo.org/api/files/x/readme.txt"},
            "checksum":"md5:0000"}]}
        with patch("inspect_compact_source_tables._get_json",
                   return_value=(obj,"meta")),patch(
              "inspect_compact_source_tables.original_bytes",return_value=b"fake"):
            with self.assertRaisesRegex(ValueError,"NO_GO_ZENODO_SOURCE_FILE_CHECKSUM"):
                source_text_files()

    def test_dryad_lists_dont_claim_species_measurements(self):
        obj={"_embedded":{"stash:files":[{
             "path":"Supplementary_Data_File.xlsx",
             "size":32768,"id":4112,
             "_links":{"stash:download":{"href":"/api/v2/files/4112/download"}}
        }]}}
        with patch("inspect_compact_source_tables._get_json",
                   return_value=(obj,"meta")):
            x=dryad_file_manifest()
        self.assertEqual(x["file_count_page"],1)
        self.assertEqual(x["source_files"][0]["file_id"],4112)
        self.assertTrue(x["no_source_traits_extracted_yet"])

if __name__=="__main__":
    unittest.main()
