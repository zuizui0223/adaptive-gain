import hashlib
import unittest
from source_audit import (
    DOI,ORIGINAL_FILES,PROVIDER_HOSTS,official_urls,decode_and_audit_csv
)

class ThreeLayoutSourceTests(unittest.TestCase):
    def test_original_supplement_locator_from_actual_PMC_article(self):
        self.assertEqual(DOI,"10.1038/s41598-017-04919-8")
        self.assertEqual(len(ORIGINAL_FILES),2)
        self.assertTrue(ORIGINAL_FILES[0].endswith("MOESM2_ESM.csv"))
        self.assertTrue(ORIGINAL_FILES[1].endswith("MOESM3_ESM.csv"))
        self.assertEqual(len(official_urls(ORIGINAL_FILES[0])),2)
        self.assertTrue(all(url.startswith("https://") for url in official_urls(ORIGINAL_FILES[1])))
    def test_never_fetch_arbitrary_guessed_secondary_source(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_SUPPLEMENT_FILENAME"):
            official_urls("different-paper.csv")
        self.assertNotIn("random-mirror.org",PROVIDER_HOSTS)
    def test_source_csv_schema_is_audit_not_fabricated_bouts(self):
        b=b"colony,bee,layout,trip,flower,arrival\n1,bee1,1,1,2,10:00\n1,bee1,1,1,3,10:10\n2,bee2,1,1,4,11:03\n"
        out=decode_and_audit_csv(b)
        self.assertEqual(out["source_header_total_columns"],6)
        self.assertEqual(out["total_source_nonblank_rows"],3)
        self.assertEqual(out["row_width_histogram"],{6:3})
        self.assertEqual(out["source_grain_inference"],"NOT_YET_VALIDATED")
        self.assertTrue(out["one_bee_one_bout_one_row_NOT_ASSUMED"])
    def test_source_rows_duplicates_are_not_automatically_discarded(self):
        b=b"bee,flower\nA,2\nA,2\nB,1\n"
        out=decode_and_audit_csv(b)
        self.assertEqual(out["total_source_nonblank_rows"],3)
        self.assertEqual(out["original_identical_rows_count_not_removed"],1)
    def test_bad_source_row_shape_reported_not_coerced(self):
        b=b"bee;flower;trip\nA;2;1\nA;3\n"
        out=decode_and_audit_csv(b)
        self.assertEqual(out["row_width_histogram"],{2:1,3:1})
        self.assertEqual(len(out["row_width_mismatch_examples"]),1)
        self.assertEqual(out["source_grain_inference"],"NOT_YET_VALIDATED")

if __name__=="__main__":unittest.main()
