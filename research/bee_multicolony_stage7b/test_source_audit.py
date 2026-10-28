import unittest
from source_audit import (
    original_csv_schema,EXPECTED,DOI,DATASET_API
)

class OriginalRoboticSourceTests(unittest.TestCase):
    def test_raw_colony_flower_record_not_individual_tag(self):
        raw=("hive,experiment_day,flower,quercetin,timestamp\n"
             "C1,1,F2,0,10:15\n"
             "C1,1,F1,1,10:20\n"
             "C2,1,F2,0,11:03\n").encode()
        result=original_csv_schema(raw)
        self.assertEqual(result["rows"],3)
        self.assertEqual(result["quality_profile"]["hive"]["unique_if_inspected"],2)
        self.assertEqual(result["quality_profile"]["flower"]["unique_if_inspected"],2)
        self.assertEqual(result["possible_source_roles_NOT_INFERRED"]["animal_tag_ids"],[])
        self.assertIn("hive",result["possible_source_roles_NOT_INFERRED"]["colony_ids"])
        self.assertEqual(result["exact_duplicate_rows"],0)
    def test_duplicates_reported_not_dropped(self):
        raw=b"colony,day,flower\nA,1,B\nA,1,B\nA,1,C\n"
        result=original_csv_schema(raw)
        self.assertEqual(result["rows"],3)
        self.assertEqual(result["exact_duplicate_rows"],1)
    def test_incomplete_csv_fails_closed(self):
        raw=b"colony,day,flower\nA,1,B,extra\nA,1,C\n"
        with self.assertRaisesRegex(ValueError,"NO_GO_CSV_RAGGED"):
            original_csv_schema(raw)
    def test_public_native_source_identity_fixed(self):
        self.assertIn("10.48804/UIIVLP",DOI)
        self.assertEqual(set(EXPECTED),{
            "00_README.md","data_selfmed.csv","Data_analysis_selfmed.R"})
        self.assertIn("persistentId",DATASET_API)

if __name__=="__main__":
    unittest.main()
