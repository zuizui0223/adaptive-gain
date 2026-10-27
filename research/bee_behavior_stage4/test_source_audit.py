import csv
import hashlib
import unittest
from source_audit import parse_original_csv, profile_original_table, ID_HINT

class PublisherSequenceAuditTests(unittest.TestCase):
    def original(self):
        return (
            b"BeeID,FlowerID,Day,Arrival,Departure,Encounter\n"
            b"B1,F1,2,10:00:05,10:00:13,no\n"
            b"B1,F3,2,10:01:05,10:01:13,yes\n"
            b"B2,F1,2,10:00:05,10:00:14,no\n"
        )
    def test_strict_source_roles_not_faked(self):
        rows,meta=parse_original_csv(self.original())
        self.assertEqual(meta["data_rows"],3)
        self.assertEqual(meta["delimiter"],"','")
        p=profile_original_table(rows,meta)
        self.assertEqual(p["original_row_count"],3)
        self.assertEqual(p["role_candidates_not_inferred_semantics"]["individual_id_columns"],["BeeID"])
        self.assertEqual(p["role_candidates_not_inferred_semantics"]["flower_id_columns"],["FlowerID"])
        self.assertEqual(set(p["role_candidates_not_inferred_semantics"]["time_columns"]),
                         {"Day","Arrival","Departure"})
        self.assertIn("Encounter",p["native_field_profile"])
        self.assertEqual(p["exact_source_row_duplicates"],0)
    def test_exact_duplicates_only_not_distinct_landing(self):
        rows,meta=parse_original_csv(self.original()+self.original().splitlines()[1]+b"\n")
        p=profile_original_table(rows,meta)
        self.assertEqual(p["exact_source_row_duplicates"],1)
        # Count all original records: do not silently discard duplicates
        self.assertEqual(p["original_row_count"],4)
    def test_ragged_csv_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_RAGGED_SOURCE"):
            parse_original_csv(self.original()+b"B1,F1\n")
    def test_header_duplicate_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_HEADER_DUPLICATE"):
            parse_original_csv(b"bee,bee\nA,1\nA,2\n")
    def test_semicolon_and_native_bee_tags(self):
        data="bee;flower;day\nA;F1;1\nB;F2;1\n".encode()
        rows,meta=parse_original_csv(data)
        self.assertEqual(len(rows),2)
        self.assertEqual(meta["delimiter"],"';'")
        self.assertEqual(meta["columns"],["bee","flower","day"])
    def test_source_has_no_implicit_visually_available_set(self):
        rows,meta=parse_original_csv(self.original())
        p=profile_original_table(rows,meta)
        self.assertTrue(p["cue_sequence_and_wind_not_inferred_from_visit_counts"])
        self.assertTrue(p["published_visits_6205_not_automatically_equal_source_rows"])

if __name__=="__main__":
    unittest.main()
