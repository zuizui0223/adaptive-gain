"""Native 2016 sequence/individual identity source semantics synthetic controls."""
import unittest
from sequence_grain import audit_rows, parse_positions

def fixture():
    return [
      {"colony":"A","id":"b1","cueType":"clay","group":"dummy_last",
       "landed":"2 6 8 5","cue":"2 6 7 10","reward":"2 6","firstLanding":"0.08","lastLanding":"1.30"},
      {"colony":"A","id":"b1","cueType":"clay","group":"test_diff",
       "landed":"2 6 5 2 3 6","cue":"2 6 7 10","reward":"NA NA","firstLanding":"0.10","lastLanding":"2.10"},
      {"colony":"B","id":"b2","cueType":"green","group":"dummy_last",
       "landed":"1 2 4","cue":"1 6 7 12","reward":"1 4","firstLanding":"0.12","lastLanding":"1.30"},
      {"colony":"B","id":"b2","cueType":"green","group":"test_easy",
       "landed":"1 2 1 4","cue":"1 6 7 12","reward":"NA NA","firstLanding":"0.30","lastLanding":"2.50"},
    ]

class SequenceGrainTests(unittest.TestCase):
    def test_original_numeric_visits_retain_repeated_flower_events(self):
        self.assertEqual(parse_positions("2 6 8 5 6 2"),[2,6,8,5,6,2])
    def test_57_bees_are_pairs_not_114_independent_animals(self):
        q=audit_rows(fixture(),expected_original=False)
        self.assertEqual(q["original_bees"],2)
        self.assertEqual(q["original_rows"],4)
        self.assertEqual(q["source_test_bees"],2)
        self.assertEqual(q["source_train_bees"],2)
        self.assertEqual(q["test_landing_events"],10)
        self.assertTrue(q["unique_one_train_one_test_per_bee"])
    def test_missing_test_animal_pair_is_no_go(self):
        rows=fixture();rows.pop()
        with self.assertRaisesRegex(ValueError,"PAIRED_TRAIN_TEST"):
            audit_rows(rows,expected_original=False)
    def test_nonphysical_flower_index_fails_closed(self):
        rows=fixture();rows[1]["landed"]="4 13"
        with self.assertRaisesRegex(ValueError,"ORIGINAL_FLOWER_INDEX"):
            audit_rows(rows,expected_original=False)

if __name__=="__main__":unittest.main()
