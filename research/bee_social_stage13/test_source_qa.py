"""Test provider integrity and native sequence representation, synthetic only."""
import unittest,hashlib
from source_qa import verify,original_table_schema

class Stage13SourceTests(unittest.TestCase):
    def test_sha256_only_exact_provider_bytes_pass(self):
        raw=b"a,b\n1,2\n"
        sha=hashlib.sha256(raw).hexdigest()
        self.assertEqual(verify(raw,sha,"sha-256"),sha)
        with self.assertRaisesRegex(ValueError,"DIGEST_MISMATCH"):
            verify(raw,"0"*64,"sha-256")
    def test_native_sequence_columns_are_not_inferred_from_paper(self):
        raw=b"group,bee,Landed,Cue,reward,firstLanding,lastLanding\ntest_easy,1,2-4-1,2-3,4,0.2,1.4\ntest_diff,2,1-4,1-3,1,0.3,1.0\n"
        qa=original_table_schema(raw)
        self.assertEqual(qa["original_source_rows"],2)
        self.assertEqual(qa["group_counts"],{"test_diff":1,"test_easy":1})
        self.assertEqual(qa["native_individual_id_candidate_counts"]["bee"],2)
        self.assertIn("Landed",qa["columns_might_contain_sequence_or_exposure"])
        self.assertTrue(qa["no_biological_hypothesis_scored"])
    def test_duplicate_header_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"REPEATED_CSV_COLUMN_NAMES"):
            original_table_schema(b"group,group\na,b\n")
    def test_blank_file_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"EMPTY_ORIGINAL"):
            original_table_schema(b"")

if __name__=="__main__":unittest.main()
