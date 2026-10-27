import math
import random
import unittest
from heldout_flower_history import (
    ALPHA,BETA,MIN_ELIGIBLE_BEES,
    validate_events,static_probs,transition_probs,paired_predict
)

class HeldoutIndividualBeeTests(unittest.TestCase):
    def fixture(self, perday=24):
        bees=[f"bee{i}" for i in range(6)]
        records=[]
        for bee in bees:
            for day in (1,2,3):
                for visit in range(perday):
                    records.append({"bee":bee,"flower":"F1" if visit%2==0 else "F2",
                                    "day":day,"timestamp":visit+3})
        return records
    def test_static_distribution_smoothed_and_normalized(self):
        v=static_probs(["F1"]*8,["F1","F2","F3"])
        self.assertAlmostEqual(sum(v.values()),1)
        self.assertGreater(v["F3"],0)
    def test_transition_smoothing_preserves_full_physically_present_array(self):
        static=static_probs(["F1"]*30,["F1","F2","F3"])
        p=transition_probs("F1",{("F1","F2"):10},static,["F1","F2","F3"])
        self.assertAlmostEqual(sum(p.values()),1)
        self.assertGreater(p["F3"],0)
    def test_history_signal_in_final_day_beyond_margins(self):
        a=paired_predict(self.fixture(),["F1","F2","F3"])
        self.assertEqual(a["status"],"source_event_gate_passed")
        self.assertEqual(len(a["per_bee"]),6)
        self.assertEqual(a["holdout_day"],"3")
        self.assertGreater(a["bee_mean_M1_gain_nats_per_transition"],0.1)
        self.assertEqual(a["total_heldout_transitions"],6*23)
        self.assertEqual(a["gain_positive_bees"],6)
        self.assertLessEqual(a["within_colony_bee_sign_flip_p_descriptive"],0.05)
    def test_holdout_order_is_globally_final_day_not_last_rows(self):
        events=list(reversed(self.fixture()))
        result=paired_predict(events,["F1","F2"])
        self.assertEqual(result["holdout_day"],"3")
    def test_same_bee_same_time_fails_closed(self):
        r=self.fixture()
        r.append({"bee":"bee1","flower":"F3","day":2,"timestamp":3})
        with self.assertRaisesRegex(ValueError,"NO_GO_SEQUENCE_TIE"):
            paired_predict(r,["F1","F2","F3"])
    def test_no_training_data_future_leakage(self):
        with self.assertRaisesRegex(ValueError,"future data"):
            paired_predict(self.fixture(),["F1","F2"],last_day=2)
    def test_unknown_flower_does_not_get_invented(self):
        with self.assertRaisesRegex(ValueError,"absent from physical array"):
            paired_predict(self.fixture(),["F1"])
    def test_no_go_fewer_five_bees_even_with_many_visits(self):
        base=[x for x in self.fixture() if x["bee"] in {f"bee{i}" for i in range(4)}]
        got=paired_predict(base,["F1","F2"])
        self.assertEqual(got["status"],"NO_GO_TOO_FEW_INDEPENDENT_BEE_TAGS_FOR_HOLDOUT")
    def test_training_marginal_is_frozen_across_holdout(self):
        data=self.fixture()
        got=paired_predict(data,["F1","F2"])
        mutated=[dict(row) for row in data]
        # The baseline should have unchanged M0 regardless of what future
        # heldout observations occur. All bee-day train events identical.
        for x in mutated:
            if x["day"]==3:
                x["flower"]="F2"
        changed=paired_predict(mutated,["F1","F2"])
        self.assertEqual(
            [v["training_visits"] for v in got["per_bee"]],
            [v["training_visits"] for v in changed["per_bee"]])
        # An altered test sequence can change the score; no train refit occurs.
        self.assertTrue(all(v["loss_M0_static_nats_per_transition"]>0 for v in changed["per_bee"]))

if __name__=="__main__":
    unittest.main()
