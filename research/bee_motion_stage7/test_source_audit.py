import json
import unittest
from source_audit import get_href,follow,ARCHIVE_NAME,README_NAME,MAX_ARCHIVE

class DryadOriginalSourceGateTests(unittest.TestCase):
    def test_native_hateoas_version_and_download_links(self):
        v={"_links":{"stash:version":{"href":"/api/v2/versions/12345"}}}
        self.assertEqual(get_href(v,"version"),"/api/v2/versions/12345")
        self.assertEqual(follow("https://datadryad.org/api/v2/datasets/a",
                                get_href(v,"version")),
                         "https://datadryad.org/api/v2/versions/12345")
        f={"_links":{"stash:download":{"href":"/api/v2/files/100/download"}}}
        self.assertEqual(get_href(f,"download"),"/api/v2/files/100/download")
    def test_reject_unsafe_provider_host(self):
        with self.assertRaisesRegex(ValueError,"NONDRYAD"):
            follow("https://datadryad.org/api/v2/versions/123",
                   "https://fake-dryad.example.org/original.7z")
    def test_data_files_are_exact_provider_names(self):
        self.assertTrue(ARCHIVE_NAME.endswith(".7z"))
        self.assertEqual(README_NAME,"README.md")
        self.assertGreater(MAX_ARCHIVE,17.31*1e6)
    def test_source_url_without_download_manifest_is_refused(self):
        obj={"_links":{"stash:files":{"href":"/api/v2/versions/123/files"}}}
        self.assertIsNone(get_href(obj,"download"))

if __name__=="__main__":unittest.main()
