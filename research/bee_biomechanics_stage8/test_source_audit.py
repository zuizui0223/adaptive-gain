import hashlib
import unittest
from source_audit import (
    DOI, SOURCE_FOCUS,check_provider_checksum,_unpack_search_results,
    _is_target_item,safe_link,href,inspect_csv
)

class CambridgeSourceGateTests(unittest.TestCase):
    def test_only_item_with_original_cambridge_dataset_doi_accepted(self):
        target={
            "uuid":"1234",
            "name":"Research data supporting Bumblebees trade-off between nectar quality and floral biomechanics",
            "metadata":{"dc.identifier.doi":[{"value":"10.17863/CAM.100572"}]},
            "_links":{"self":{"href":"https://api.repository.cam.ac.uk/server/api/core/items/1234"}}
        }
        wrapper={"_embedded":{"searchResult":[
            {"_embedded":{"indexableObject":target}},
            {"_embedded":{"indexableObject":{"name":"Unrelated repository item"}}}
        ]}}
        options=_unpack_search_results(wrapper)
        self.assertEqual(len(options),2)
        self.assertTrue(_is_target_item(options[0]))
        self.assertFalse(_is_target_item(options[1]))
        self.assertIn("/items/1234",href(options[0],"self"))
    def test_provider_original_checksum_verification(self):
        src=b"bee,colony,time,flower\n1,A,4,down\n"
        rec={"checkSum":{"checkSumAlgorithm":"MD5",
                         "value":hashlib.md5(src).hexdigest()},
             "sizeBytes":len(src)}
        out=check_provider_checksum(src,rec,"test.csv")
        self.assertEqual(out["original_sha256"],hashlib.sha256(src).hexdigest())
        bad=dict(rec)
        bad["sizeBytes"]=len(src)+1
        with self.assertRaisesRegex(ValueError,"SIZE_MISMATCH"):
            check_provider_checksum(src,bad,"test.csv")
    def test_source_data_cannot_be_mirrored_to_unrelated_host(self):
        with self.assertRaisesRegex(ValueError,"INSTITUTIONAL"):
            safe_link("https://example.org/source-bees.csv")
    def test_source_unknown_behavior_is_not_labeled_a_specific_action(self):
        raw=(b"BeeID,Colony,Flower,TimeMs,Observation,Bout\n"
             b"AA,1,12,1234,visiting,2\n"
             b"AA,1,8,1789,resting,2\n"
             b"BB,2,12,2345,landing,3\n")
        schema=inspect_csv(raw)
        self.assertEqual(schema["original_csv_rows"],3)
        self.assertIn("BeeID",schema["fields_matching_original_roles"]["bee_or_colony"])
        self.assertIn("Observation",schema["fields_matching_original_roles"]["sequence_or_bout"])
        self.assertEqual(schema["source_fields"]["Observation"]["distinct"],3)
        self.assertFalse("AA" in str(schema))
    def test_missing_checksum_is_no_go(self):
        with self.assertRaisesRegex(ValueError,"CHECKSUM_ABSENT"):
            check_provider_checksum(b"some csv",{}, "test.csv")

if __name__=="__main__":
    unittest.main()
