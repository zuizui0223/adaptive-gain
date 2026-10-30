"""Stage13 temporal cue-state null tested only on synthetic ordered flower IDs."""
import random
import unittest
from collections import Counter
from cue_sequence_null import score_switched, shuffle_after_first, test_source

def rows():
    seq=[
        ("a","b1","clay","test_easy","1 2 4 6 3 5 2","1 2 7 10"),
        ("a","b2","green","test_diff","3 5 3 7 8 9 5","1 2 7 10"),
        ("b","b3","clay","test_diff","1 3 5 1 7 10 6","1 2 7 10"),
        ("b","b4","green","test_easy","1 1 2 4 6 2","1 2 7 10"),
        ("c","b5","clay","test_easy","4 5 6 7 8","1 2 7 10"),
        ("c","b6","green","test_diff","1 2 1 2 1 2 3","1 2 7 10"),
    ]
    return [{"colony":c,"id":b,"cueType":typ,"group":g,"landed":visits,
             "cue":cue} for c,b,typ,g,visits,cue in seq]

class CueSequenceTests(unittest.TestCase):
    def test_consecutive_same_flower_never_counts_as_an_interflower_choice(self):
        score,events=score_switched([1,1,2,4,6],{1,2,7,10})
        self.assertEqual(events,3)
        self.assertAlmostEqual(score,2/3)
    def test_source_first_choice_and_flower_frequency_are_preserved(self):
        original=[1,3,3,8,4,5,1,2]
        shuffled=shuffle_after_first(original,random.Random(20261030))
        self.assertEqual(shuffled[0],original[0])
        self.assertEqual(Counter(shuffled),Counter(original))
        self.assertEqual(len(shuffled),len(original))
    def test_all_one_flower_is_technical_not_social_route(self):
        x,n=score_switched([3,3,3,3],{3,5,7,9})
        self.assertEqual(n,0)
        self.assertIsNone(x)
    def test_original_bees_weighted_equally_within_three_colonies(self):
        result=test_source(rows(),permutations=19,seed=20261030,expected_original=False)
        self.assertEqual(result["source_colonies"],3)
        self.assertEqual(result["source_eligible_bees"],6)
        self.assertEqual(result["source_test_landing_events"],39)
        self.assertEqual(result["permutations"],19)
        self.assertEqual(set(result["colony_actual_minus_null"]),{"a","b","c"})
        self.assertGreaterEqual(result["one_sided_source_conditional_p"],0.05)
        self.assertLessEqual(result["one_sided_source_conditional_p"],1)
    def test_duplicate_original_test_bee_is_no_go(self):
        items=rows()+[rows()[0]]
        with self.assertRaisesRegex(ValueError,"DUPLICATE_TEST_BEE"):
            test_source(items,permutations=3,expected_original=False)

if __name__=="__main__":unittest.main()
