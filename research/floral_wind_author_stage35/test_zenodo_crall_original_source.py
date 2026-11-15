"""Stage35 tests: invented in-memory archives only; no research observations."""
import io
import json
import unittest
from unittest.mock import patch
import zipfile

from zenodo_crall_original_source import (
    _csv_profile, _safe_zip_inventory, _candidate_download_urls,
    _verify_md5_if_declared, assess_api_metadata, run, _fetch
)


def fake_zip():
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("fake/session.csv",
                   "site,wind,bees\nMOCK_A,0.1,2\nMOCK_B,0.2,3\n")
        z.writestr("fake/author_code.R","# fake no data\n")
    return buffer.getvalue()


def fake_meta():
    return {
       "id":3743898,
       "doi":"10.5281/zenodo.3743898",
       "metadata":{
          "title":"Wind drives temporal variation in pollinator visitation in a fragmented tropical forest",
          "creators":[{"name":"Crall, James D."}]
       },
       "files":[{"key":"MOCK_Crall.zip",
                 "size":len(fake_zip()),
                 "checksum":None,
                 "links":{"self":"https://zenodo.org/api/records/3743898/files/MOCK_Crall.zip/content"}}]
    }


class ZenodoSourceGrainTests(unittest.TestCase):
    def test_fake_metadata_valid_but_not_original(self):
        x=assess_api_metadata(fake_meta(),3743898)
        self.assertEqual(x["record_id_metadata"],3743898)
        self.assertEqual(x["zip_candidates"][0][0],"MOCK_Crall.zip")
        self.assertTrue(x["cannot_conflate_versions"])

    def test_no_silent_version_substitution(self):
        x=assess_api_metadata(fake_meta(),3675327)
        self.assertEqual(x["record_id_requested"],3675327)
        self.assertEqual(x["record_id_metadata"],3743898)

    def test_fake_two_csv_rows_and_grain(self):
        x=_safe_zip_inventory(fake_zip())
        self.assertEqual(len(x),2)
        t=x[0]["csv"]
        self.assertEqual(t["n_records"],2)
        self.assertEqual(t["header"],["site","wind","bees"])
        self.assertEqual(t["column_profiles"][1]["numeric_min"],.1)
        self.assertEqual(t["column_profiles"][1]["numeric_max"],.2)
        self.assertTrue(t["no_individual_original_rows_redistributed"])

    def test_zip_traversal_rejected(self):
        z=io.BytesIO()
        with zipfile.ZipFile(z,"w") as archive:
            archive.writestr("../source.csv","a,b\n1,2\n")
        with self.assertRaisesRegex(ValueError,"UNSAFE_ZIP_PATH"):
            _safe_zip_inventory(z.getvalue())

    def test_csv_arity_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError,"FIELD_ARITY_MISMATCH"):
            _csv_profile(b"a,b\n1\n")

    def test_wrong_original_title_and_author_rejected(self):
        wrong=fake_meta()
        wrong["metadata"]["title"]="Something unrelated"
        with self.assertRaisesRegex(ValueError,"UNRELATED_ZENODO_RECORD"):
            assess_api_metadata(wrong,3743898)
        wrong=fake_meta()
        wrong["metadata"]["creators"]=[{"name":"Someone else"}]
        with self.assertRaisesRegex(ValueError,"NOT_CRALL_AUTHOR"):
            assess_api_metadata(wrong,3743898)

    def test_wrong_checksum_rejected(self):
        import hashlib
        y=fake_zip()
        ok="md5:"+hashlib.md5(y).hexdigest()
        self.assertTrue(_verify_md5_if_declared(y,ok)["passed"])
        with self.assertRaisesRegex(ValueError,"DOWNLOAD_CHECKSUM_MISMATCH"):
            _verify_md5_if_declared(y,"md5:"+"0"*32)

    def test_non_zenodo_host_rejected_before_network(self):
        with self.assertRaisesRegex(ValueError,"HOST_UNAUTHORIZED"):
            _fetch("https://invalid.example/api/records/1")

    def test_fail_closed_when_both_records_unavailable(self):
        from urllib.error import HTTPError
        def deny(_):
            raise HTTPError("https://zenodo.org",429,"Too Many Requests",None,None)
        with patch("zenodo_crall_original_source._fetch",side_effect=deny):
            x=run()
        self.assertEqual(x["verified_record_count"],0)
        self.assertEqual(x["status"],"NO_GO_NO_ORIGINAL_ZENODO_ARCHIVE")
        self.assertEqual(len(x["record_receipts"]),2)
        self.assertTrue(all(r["http_status"]==429 for r in x["record_receipts"]))
        self.assertEqual(x["ecological_effect_estimates_extracted"],0)
        self.assertFalse(x["wind_by_odor_interaction_empirically_tested"])


if __name__=="__main__":
    unittest.main()
