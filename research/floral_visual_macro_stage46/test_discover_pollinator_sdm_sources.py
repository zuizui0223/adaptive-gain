"""Source-only archive access contract, all synthetic mock JSON."""
import unittest
from unittest.mock import patch
from discover_pollinator_sdm_sources import (
    SOURCE_LIST,_get_json,_zenodo_summary,_dryad_summary,discover
)
class ArchiveSourceIdentityTests(unittest.TestCase):
    def test_only_pinned_archive_hosts_accepted(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_ARCHIVE_METADATA_UNTRUSTED_HOST"):
            _get_json("https://external.example.org/fake")
        with self.assertRaisesRegex(ValueError,"NO_GO_ARCHIVE_METADATA_UNTRUSTED_HOST"):
            _get_json("http://zenodo.org/api/records/123")

    def test_zenodo_file_name_and_bytes_not_measurement(self):
        payload={"doi":"10.5281/zenodo.20525239",
          "metadata":{"title":"Mock global bee ranges",
                      "license":{"id":"cc-by-4.0"}},
          "files":[{"key":"bee_sdm_grid.csv","size":82410,
                    "checksum":"md5:1234",
                    "links":{"self":"https://zenodo.org/api/files/x/file"}}]}
        r=_zenodo_summary(payload)
        self.assertEqual(r["file_count"],1)
        self.assertEqual(r["files"][0]["extension"],".csv")
        self.assertEqual(r["files"][0]["size_bytes"],82410)
        self.assertEqual(r["record_doi"],"10.5281/zenodo.20525239")

    def test_dryad_metadata_not_a_species_trait_count(self):
        x={"title":"Mock uv Potentilleae",
           "identifier":"doi:10.5061/dryad.k98sf7m3z",
           "_links":{"stash:version":{"href":"/api/v2/versions/xyz"}}}
        r=_dryad_summary(x)
        self.assertEqual(r["record_doi"],"doi:10.5061/dryad.k98sf7m3z")
        self.assertEqual(r["embedded_file_count"],0)
        self.assertNotIn("species_count",r)

    def test_partial_failures_keep_no_negative_evidence(self):
        def mock_get(url):
            if "20525239" in url:
                return ({"doi":"10.5281/zenodo.20525239",
                         "metadata":{"title":"Source"},
                         "files":[]},"sha")
            raise ValueError("UNAVAILABLE")
        with patch("discover_pollinator_sdm_sources._get_json",side_effect=mock_get):
            r=discover()
        self.assertEqual(len(r["sources"]),1)
        self.assertEqual(len(r["unavailable"]),len(SOURCE_LIST)-1)
        self.assertTrue(all(v["missing_is_not_negative_evidence"]
                            for v in r["unavailable"].values()))
        self.assertTrue(r["sources"]["global_bee_range_model_2026"]
                         ["original_spatial_raster_data_downloaded"] is False)

if __name__=="__main__":
    unittest.main()
