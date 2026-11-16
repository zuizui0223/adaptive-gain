"""Stage54 all fabricated API replies; no false floral labels."""
import io,json,unittest,zipfile
from unittest.mock import patch
from probe_multimodal_original_literature import (
    _fetch,_supplement_entry,_summarize_json_source,probe
)
class SourceFirstAudits(unittest.TestCase):
    def test_zip_manifest_is_not_positive_or_negative_species_list(self):
        b=io.BytesIO()
        with zipfile.ZipFile(b,"w") as z:
            z.writestr("plants-14-02185-s001.csv","species,flower_color_change\nMockus alba,yes\n")
        q=_supplement_entry(b.getvalue())
        self.assertTrue(q["any_species_table_supplement"])
        self.assertEqual(q["source_supplement_members"][0]["table_schema"]["total_lines"],2)
        self.assertIn("member_sha256",q["source_supplement_members"][0])

    def test_invalid_zip_cannot_be_read_as_151_species(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_EUROPEPMC_SUPPLEMENT"):
            _supplement_entry(b"not zip")

    def test_zenodo_219_metadata_not_measured_negative_list(self):
        raw=json.dumps({"id":4942515,"files":[
          {"key":"Ohashi_etal.zip","size":285930000,
           "checksum":"md5:fake","links":{"self":"https://zenodo.org/file"}}
        ]}).encode()
        out=_summarize_json_source(raw,"2015_Ohashi_219_Zenodo_metadata")
        self.assertTrue(out["no_285MB_zip_download_here"])
        self.assertEqual(out["files"][0]["name"],"Ohashi_etal.zip")

    def test_all_denied_sources_are_not_plant_absences(self):
        from urllib.error import URLError
        with patch("probe_multimodal_original_literature._fetch",
                   side_effect=URLError("source unavailable")):
            result=probe()
        self.assertTrue(result["unverified_signals_never_marked_absent"])
        self.assertTrue(all(x["access"]=="UNAVAILABLE_NOT_NEGATIVE_TRAIT"
                            for x in result["sources"].values()))

    def test_disallow_untrusted_source_host(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_UNTRUSTED"):
            _fetch("https://somehost.invalid/maybe.csv")


if __name__=="__main__":unittest.main()
