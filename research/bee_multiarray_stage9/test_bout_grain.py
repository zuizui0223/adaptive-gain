import unittest
from bout_grain import (
    SHA_S1,SHA_S2,HEAD_S1,HEAD_S2,parse_quoted_sequence,validate_bouts,
    FLOWERS
)

def synthetic():
    records=[]
    for bee in range(29):
        for arr in range(1,4):
            for bout in range(1,21):
                seq="012343210" if bout%2 else "012121340"
                records.append(dict(zip(HEAD_S1,[
                    "b"+str(bee),"c"+str(bee//15),
                    "14","13",str(arr),str(bout),
                    "4","1","0","2.5","0",seq+'"'
                ])))
    return records

class KleinOriginalBoutsTests(unittest.TestCase):
    def test_original_pinned_hash_immutable_shape(self):
        self.assertEqual(len(SHA_S1),64)
        self.assertEqual(len(SHA_S2),64)
        self.assertEqual(len(HEAD_S1),12)
        self.assertEqual(len(HEAD_S2),15)
        self.assertIn("sqce_tot",HEAD_S1)
    def test_original_sequences_not_reinterpreted_as_string_labels(self):
        self.assertEqual(parse_quoted_sequence(' "01234210" '),"01234210")
        self.assertEqual(parse_quoted_sequence('01234210"'),"01234210")
        self.assertEqual(parse_quoted_sequence('01234210'),"01234210")
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_FLOWER_ID"):
            parse_quoted_sequence("01239210")
        with self.assertRaisesRegex(ValueError,"NO_GO_UNRECOGNIZED_SOURCE"):
            parse_quoted_sequence("0,1,2,3,4,0")
    def test_exact_real_design_required_in_source(self):
        data,receipt=validate_bouts(synthetic())
        self.assertEqual(receipt["source_S1_rows"],1740)
        self.assertEqual(receipt["source_distinct_experimental_bees"],29)
        self.assertEqual(receipt["original_unique_bee_array_cells"],87)
        self.assertEqual(receipt["source_independent_colonies"],2)
        self.assertEqual(receipt["source_bouts_per_bee_array_min"],20)
        self.assertEqual(receipt["source_bouts_per_bee_array_max"],20)
        self.assertEqual(receipt["original_grain_gate"],"PASS_FULLY_NEST_BOUNDED")
        self.assertEqual(receipt["source_original_bouts_eligible_for_direction"],1740)
        self.assertEqual(receipt["source_original_bouts_excluded_only_for_nest_quality"],0)
        self.assertEqual(receipt["source_duplicate_colony_bee_array_bout_keys"],0)
        self.assertEqual(receipt["source_bouts_with_extra_internal_nest_marker"],0)
        self.assertEqual(set(receipt["source_flower_id_visit_frequency"]),set(FLOWERS))
        self.assertEqual(len(data),1740)
        self.assertEqual(data[0]["flower_sequence"],"012343210")
    def test_duplicated_bout_invalid_not_independent(self):
        rows=synthetic()
        rows[-1]["bout"]="19"
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_BEE_SOURCE_GRAIN"):
            validate_bouts(rows)
    def test_missing_original_nest_start_end_not_silently_filled(self):
        rows=synthetic()
        rows[7]["sqce_tot"]="1234"
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_BEE_SOURCE_GRAIN"):
            validate_bouts(rows)
    def test_extra_nest_marker_within_bout_is_source_quality_risk(self):
        rows=synthetic()
        rows[9]["sqce_tot"]="0120340"
        with self.assertRaisesRegex(ValueError,"NO_GO_ORIGINAL_BEE_SOURCE_GRAIN"):
            validate_bouts(rows)

if __name__=="__main__":unittest.main()
