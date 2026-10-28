import math
import random
import unittest
from collections import Counter
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"bee_biomechanics_stage8"))

from episode_audit import source_episode_audit
from heldout_experience_choice import (
    evaluate,true_visited_pairs,split_bee_source_trips,fit_probabilities,score_edges
)
from test_heldout_experience_choice import fixture
from within_trip_conditional_lag import (
    contiguous_segments,permuted_test_edges,eligibility,analyze,
    _signed_effect
)

def source_test_cases(trips=12,episodes_per_trip=12):
    rows=fixture(colonies=3,bees_per_colony=4,trips=trips,
                 episodes_per_trip=episodes_per_trip)
    episodes,qa=source_episode_audit(rows,source_expected=None)
    pairs,first,info=true_visited_pairs(episodes,rows)
    bees,excluded=split_bee_source_trips(pairs,first)
    return rows,episodes,qa,bees

class WithinTripSourceConditionalLagTests(unittest.TestCase):
    def test_uninterrupted_edges_segmented_without_crossing_bout(self):
        rows,episodes,qa,bees=source_test_cases()
        all_original=sum(len(b["test_pairs"]) for b in bees)
        all_segments=sum(len(contiguous_segments(b["test_pairs"])) for b in bees)
        self.assertEqual(all_original,sum(
            len(s) for b in bees for s in contiguous_segments(b["test_pairs"])))
        self.assertEqual(all_segments,sum(b["heldout_later_trips"] for b in bees))
        self.assertEqual(all_original,12*3*11)
        self.assertTrue(all(
            len({e["trip"] for e in segment})==1
            for b in bees for segment in contiguous_segments(b["test_pairs"])))
    def test_split_rest_marker_and_no_cross_gap(self):
        rows=fixture(colonies=3,bees_per_colony=4,trips=10,
                     episodes_per_trip=8,rest_between=True)
        eps,qa=source_episode_audit(rows,source_expected=None)
        pair,first,extra=true_visited_pairs(eps,rows)
        bees,_=split_bee_source_trips(pair,first)
        self.assertGreater(extra["source_true_pair_exclusions"]
                           ["genuine_rest_or_bout_marker_in_between"],0)
        for bee in bees:
            for seg in contiguous_segments(bee["test_pairs"]):
                for a,b in zip(seg,seg[1:]):
                    self.assertEqual(a["source_next_first"],b["source_prev_first"])
                    self.assertEqual(a["trip"],b["trip"])
    def test_main_shuffle_preserves_actual_future_choices_and_segment_bags(self):
        rows,eps,qa,bees=source_test_cases()
        b=bees[0]
        original=b["test_pairs"]
        moved,changed=permuted_test_edges(original,random.Random(42),
                                          "orientation_and_drink")
        self.assertGreater(changed,0)
        self.assertEqual([v["next_horizontal"] for v in moved],
                         [v["next_horizontal"] for v in original])
        self.assertEqual([v["source_next_first"] for v in moved],
                         [v["source_next_first"] for v in original])
        before=contiguous_segments(original)
        after=contiguous_segments(moved)
        for x,y in zip(before,after):
            self.assertCountEqual(
                [(e["previous_orientation"],e["previous_recorded_drink"])
                 for e in x],
                [(e["previous_orientation"],e["previous_recorded_drink"])
                 for e in y])
    def test_secondary_shuffle_keeps_previous_orientation_and_next_outcome(self):
        rows,eps,qa,bees=source_test_cases()
        a=bees[0]["test_pairs"]
        b,changed=permuted_test_edges(a,random.Random(42),
                                     "drink_given_orientation")
        self.assertEqual([x["previous_orientation"] for x in a],
                         [x["previous_orientation"] for x in b])
        self.assertEqual([x["next_horizontal"] for x in a],
                         [x["next_horizontal"] for x in b])
        for before,after in zip(contiguous_segments(a),contiguous_segments(b)):
            for orientation in ("horizontal","vertical"):
                self.assertCountEqual(
                    [x["previous_recorded_drink"] for x in before
                     if x["previous_orientation"]==orientation],
                    [x["previous_recorded_drink"] for x in after
                     if x["previous_orientation"]==orientation])
    def test_eligible_synthetic_original_source_and_frozen_19_shuffle_models(self):
        rows,eps,qa,bees=source_test_cases()
        info=eligibility(bees)
        self.assertEqual(info["heldout_original_bees"],12)
        self.assertEqual(info["all_source_heldout_test_pairs"],396)
        self.assertEqual(info["primary_gate"],"PASS",info)
        self.assertEqual(info["secondary_gate"],"PASS",info)
        fit=analyze(eps,qa,rows,permutations=19,seed=9,
                    expected_source=False)
        self.assertEqual(fit["status"],"STAGE8B_CONDITIONAL_NULLS_COMPLETED_OR_EXPLICIT_NO_GO")
        self.assertEqual(fit["orientation_given_original_segment_null"]["status"],
                         "COMPUTED_SOURCE_SEGMENT_CONDITIONAL_LAG_NULL")
        self.assertEqual(fit["drink_given_source_orientation_and_segment_null"]["status"],
                         "COMPUTED_SOURCE_SEGMENT_CONDITIONAL_LAG_NULL")
        self.assertEqual(fit["observed_lag_scores"]["source_test_pairs"],396)
        self.assertTrue(0<fit["orientation_given_original_segment_null"]
                          ["one_tailed_positive_association_p"]<=1)
        self.assertGreater(fit["drink_given_source_orientation_and_segment_null"]
                           ["actual_minus_null_mean_nats"],0)
    def test_fewer_bees_no_go_no_invented_extra_colonies(self):
        rows=fixture(colonies=1,bees_per_colony=4,trips=12,episodes_per_trip=12)
        eps,qa=source_episode_audit(rows,source_expected=None)
        o=analyze(eps,qa,rows,permutations=9,expected_source=False)
        self.assertEqual(o["status"],"NO_GO_PREVIOUS_SOURCE_HELDOUT_SUPPORT")
        self.assertNotIn("orientation_given_original_segment_null",o)
    def test_baseline_prediction_probabilities_never_retrained_on_test(self):
        rows,eps,qa,bees=source_test_cases()
        b=bees[0]
        original_fit=fit_probabilities(b["train_pairs"])
        baseline,_=score_edges(b["test_pairs"],original_fit)
        reshuffled,_=permuted_test_edges(
            b["test_pairs"],random.Random(5),"orientation_and_drink")
        shuffled,_=score_edges(reshuffled,original_fit)
        self.assertAlmostEqual(baseline["M0"],shuffled["M0"],places=12)
        self.assertEqual(original_fit,
                         fit_probabilities(b["train_pairs"]))
        conditional,_=permuted_test_edges(
            b["test_pairs"],random.Random(5),"drink_given_orientation")
        m1,_=score_edges(conditional,original_fit)
        self.assertAlmostEqual(baseline["M1"],m1["M1"],places=12)

if __name__=="__main__":
    unittest.main()
