import json
import math
from pathlib import Path
import unittest

from turn_inertia_heldout import (
    COORD_PATH,PHYSICAL_FLOWERS,KAPPA_GRID,SHUFFLES,
    source_triplets,cosine_turn,turned,choose_kappa,fit_direction_models,
    incoming_heading_permutation
)
from geo_history_holdout import verify_geometry,geo_probs
from heldout_flower_history import static_probs

def mock_bouts(tags=6,perday=12):
    # Many repeated within-bout directional triplets; both variants reach
    # physical F4 from different incoming flowers (F1 or F2).
    arr=[]
    variants=[
        ["1","4","7","10","9","6","3","1"],
        ["2","4","7","10","9","6","3","2"],
        ["1","4","7","10","8","5","2","1"],
        ["2","4","7","10","8","5","2","1"]
    ]
    for bee in range(tags):
        for day in (1,2,3,4,5):
            for bout in range(perday):
                seq=list(variants[(bout+bee)%len(variants)])
                arr.append({"bee":f"bee{bee}","day":day,"bout":bout+1,
                            "start_time_seconds":day*100000+bout*500,
                            "end_time_seconds":day*100000+bout*500+300,
                            "recorded_duration_seconds":300,
                            "flowers":seq})
    return arr

class DirectionalInertiaTests(unittest.TestCase):
    def setUp(self):
        self.dist,self.receipt=verify_geometry(COORD_PATH)
        self.coords={k:tuple(v) for k,v in
                     self.receipt["ten_original_coordinate_labels"].items()}
    def test_actual_positions_identified_and_direction_not_numeric_id(self):
        self.assertAlmostEqual(cosine_turn(self.coords,"1","4","7"),1.0)
        self.assertAlmostEqual(cosine_turn(self.coords,"7","4","1"),1.0)
        self.assertAlmostEqual(cosine_turn(self.coords,"1","4","1"),-1.0)
        with self.assertRaisesRegex(ValueError,"ZERO_STEP"):
            cosine_turn(self.coords,"4","4","1")
    def test_direction_distribution_normalizes_and_zero_kappa_recovers_baseline(self):
        static=static_probs(["1"]*40,PHYSICAL_FLOWERS)
        g=geo_probs(static,"4",PHYSICAL_FLOWERS,self.dist,0.05)
        d={f:p/(1-g["4"]) for f,p in g.items() if f!="4"}
        q=turned(d,self.coords,"1","4",0.0)
        for f in d:self.assertAlmostEqual(q[f],d[f])
        h=turned(d,self.coords,"1","4",1.0)
        self.assertAlmostEqual(sum(h.values()),1.0)
        self.assertGreater(h["7"],q["7"])
        self.assertLess(h["1"],q["1"])
    def test_chord_triplets_only_within_true_bout(self):
        b=[{"bee":"bee0","day":1,"bout":1,"flowers":["1","1","4","7"]},
           {"bee":"bee0","day":1,"bout":2,"flowers":["7","4","7","10"]}]
        triples,audit=source_triplets(b)
        self.assertEqual(audit["visits"],8)
        self.assertEqual(audit["within_bout_adjacent_pairs"],6)
        self.assertEqual(audit["within_bout_total_triplets"],4)
        self.assertEqual(audit["eligible_distinct_step_triplets"],3)
        self.assertFalse(any(x["a"]=="1" and x["b"]=="7" for x in triples))
    def test_no_direction_if_zero_incoming_or_second_step(self):
        events,audit=source_triplets([
            {"bee":"a","day":1,"bout":1,"flowers":["1","1","1","4","4","7"]}
        ])
        self.assertEqual(audit["within_bout_total_triplets"],4)
        self.assertEqual(events,[])
    def test_expected_original_population_guard_before_result(self):
        b=mock_bouts()
        with self.assertRaisesRegex(ValueError,"NO_GO_STAGE5_ORIGINAL"):
            fit_direction_models(b,self.coords,self.dist)
    def test_train_only_lambda_audit_and_frozen_geometry_reference(self):
        b=mock_bouts()
        result,internal=fit_direction_models(
            b,self.coords,self.dist,expected_anchor=None,expected_lambda=None)
        self.assertEqual(result["status"],"FITTED_INDIVIDUAL_HELDOUT_DIRECTION_ANALYSIS")
        self.assertEqual(result["eligible_bee_tags"],6)
        self.assertEqual(result["final_day_heldout"],5)
        self.assertIn(result["selected_train_only_heading_kappa"],KAPPA_GRID)
        self.assertEqual(result["source_test_triplets"]["eligible_distinct_step_triplets"],
                         result["eligible_heldout_triplets"])
        self.assertEqual(len(result["per_bee"]),6)
        self.assertTrue(all(math.isfinite(x) for x in
            result["mean_bee_equal_heldout_nll"].values()))
        self.assertEqual(sum(result["primary_direction_to_direction_plus_history"]
                             ["per_bee_gains"].values())/6,
                         result["primary_direction_to_direction_plus_history"]
                             ["mean_bee_equal_nll_gain_nats_per_triplet"])
    def test_train_only_kappa_insensitive_to_last_day_destinations(self):
        b=mock_bouts()
        r1,_=fit_direction_models(b,self.coords,self.dist,
                                  expected_anchor=None,expected_lambda=None)
        changed=[{**x,"flowers":list(x["flowers"])} for x in b]
        for row in changed:
            if row["day"]==5:
                row["flowers"]=list(reversed(row["flowers"]))
        r2,_=fit_direction_models(changed,self.coords,self.dist,
                                  expected_anchor=None,expected_lambda=None)
        self.assertEqual(r1["selected_train_only_heading_kappa"],
                         r2["selected_train_only_heading_kappa"])
        self.assertEqual(r1["train_only_kappa_candidate_grid"],
                         r2["train_only_kappa_candidate_grid"])
    def test_conditional_shuffle_preserves_actual_current_to_next(self):
        b=mock_bouts(tags=6,perday=12)
        result,internal=fit_direction_models(
            b,self.coords,self.dist,expected_anchor=None,expected_lambda=None)
        test=incoming_heading_permutation(internal,n=19,seed=7)
        self.assertEqual(test["permutations"],19)
        self.assertIn(test["status"],[
            "NO_GO_UNSUPPORTED_PERMUTATION_CELLS",
            "COMPUTED_DIRECTION_SHUFFLE_NULL"])
        self.assertTrue(test["not_a_cue_perception_randomization"])

if __name__=="__main__":unittest.main()
