import unittest
from bout_transition_analysis import parse_bouts
from test_bout_transition_analysis import OriginalBoutTransitionTests
from within_bout_shuffle import (
    _last_day_shuffled,conditional_bout_order_test
)

class SourceBoutShuffleTests(unittest.TestCase):
    def fixture(self,bees=6):
        r,m=OriginalBoutTransitionTests().fixture(bee_count=bees)
        b,_=parse_bouts(r,m)
        return b
    def test_heldout_shuffles_do_not_change_training_or_flower_bag(self):
        import random
        b=self.fixture()
        moved=_last_day_shuffled(b,3,random.Random(42))
        self.assertEqual(len(moved),len(b))
        self.assertTrue(all(x is y for x,y in zip(b,moved) if x["day"]<3))
        for a,c in zip(b,moved):
            self.assertEqual(sorted(a["flowers"]),sorted(c["flowers"]))
            self.assertEqual(a["day"],c["day"])
            self.assertEqual(a["bout"],c["bout"])
        self.assertTrue(any(
            a["flowers"]!=c["flowers"]
            for a,c in zip(b,moved) if a["day"]==3))
    def test_true_alternating_order_exceeds_conditional_shuffle(self):
        a=conditional_bout_order_test(self.fixture(),permutations=39,seed=44)
        self.assertEqual(a["status"],"COMPUTED_DESCRIPTIVE_CONDITIONAL_BOUT_ORDER_TEST")
        self.assertGreater(a["observed_minus_null_mean_gain_nats"],0)
        self.assertLessEqual(a["positive_tail_monte_carlo_p"],.05)
        self.assertEqual(a["eligible_bees"],6)
    def test_scientific_no_go_not_recast_as_significance(self):
        a=conditional_bout_order_test(self.fixture(bees=3),permutations=39)
        self.assertEqual(a["status"],"NO_GO_PRIMARY_HOLDOUT_INSUFFICIENT")

if __name__=="__main__":
    unittest.main()
