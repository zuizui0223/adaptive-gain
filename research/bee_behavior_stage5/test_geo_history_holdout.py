import math
import sys
import tempfile
import unittest
from pathlib import Path

from geo_history_holdout import (
    verify_geometry,geo_probs,geo_history_probs,choose_global_lambda,
    split_bouts,analyze_geo,PHYSICAL_FLOWERS,LAMBDA_CANDIDATES,
    conditional_switch_probability,
)
from heldout_flower_history import static_probs
from bout_transition_analysis import parse_bouts

GEO_PATH=Path(__file__).with_name("flower_positions_figure2_verified.json")

def synthetic_bouts(n_bees=6):
    import itertools
    sequence=["1","2","5","7","9","10","8","5","4","3","1","2"]
    bouts=[]
    for bee in range(n_bees):
        for day in (1,2,3):
            for j in range(10):
                start=39000+j*300+day*18000
                bouts.append({"bee":f"bee{bee}","day":day,"bout":j+1,
                    "start_time_seconds":start,"end_time_seconds":start+160,
                    "recorded_duration_seconds":160,
                    "flowers":sequence[bee%3:]+sequence[:bee%3]})
    return bouts

class SpatialGeometryStage5Tests(unittest.TestCase):
    def setUp(self):
        self.dist,self.receipt=verify_geometry(GEO_PATH)
    def test_true_source_figure2_labels_meters(self):
        self.assertEqual(len(self.receipt["ten_original_coordinate_labels"]),10)
        self.assertAlmostEqual(self.dist["1","4"],9.0,places=9)
        self.assertAlmostEqual(self.dist["1","6"],math.sqrt(8*8+13.5*13.5),places=9)
        self.assertAlmostEqual(self.dist["3","2"],16.0,places=9)
        self.assertAlmostEqual(self.dist["2","3"],self.dist["3","2"])
        self.assertEqual(self.dist["1","1"],0)
        self.assertGreaterEqual(self.receipt["adjacent_options_by_origin"]["1"],3)
    def test_source_geometry_sha_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/"fake.json"
            obj=GEO_PATH.read_text().replace(
                "7f275a219fe0128d30f70cf6d812ab41d4b64727a740102549e8362b83d4ff8b",
                "0"*64)
            dest.write_text(obj)
            with self.assertRaisesRegex(ValueError,"NO_GO_FIG2_SHA"):
                verify_geometry(dest)
    def test_spatial_kernel_normalized_including_unvisited_physical_flowers(self):
        p=static_probs(["1"]*20,PHYSICAL_FLOWERS)
        q=geo_probs(p,"1",PHYSICAL_FLOWERS,self.dist,0.1)
        self.assertAlmostEqual(sum(q.values()),1)
        self.assertGreater(q["10"],0)
        self.assertGreater(q["1"],q["7"])
        for x in q:self.assertGreater(q[x],0)
    def test_zero_lambda_exactly_recovers_static_flower_margins(self):
        p=static_probs(["1","4","4","6"],PHYSICAL_FLOWERS)
        q=geo_probs(p,"3",PHYSICAL_FLOWERS,self.dist,0.0)
        for k in PHYSICAL_FLOWERS:self.assertAlmostEqual(p[k],q[k])
    def test_geometry_history_prior_fully_normalized(self):
        p=static_probs(["1"]*10,PHYSICAL_FLOWERS)
        q=geo_probs(p,"1",PHYSICAL_FLOWERS,self.dist,0.05)
        h=geo_history_probs("1",{("1","2"):5},q,PHYSICAL_FLOWERS)
        self.assertAlmostEqual(sum(h.values()),1)
        self.assertGreater(h["10"],0)
        self.assertGreater(h["2"],q["2"])
    def test_switch_conditioning_renormalizes_without_self_cherrypick(self):
        p=static_probs(["1"]*10+["2"]*4,PHYSICAL_FLOWERS)
        got=conditional_switch_probability(p,"1","2")
        self.assertAlmostEqual(
            got,p["2"]/sum(p[k] for k in PHYSICAL_FLOWERS if k!="1"))
        with self.assertRaises(ValueError):
            conditional_switch_probability(p,"1","1")
    def test_lambda_selected_from_earlier_days_only(self):
        b=synthetic_bouts()
        _,train=split_bouts(b)
        lam,loss=choose_global_lambda(train,self.dist)
        self.assertIn(lam,LAMBDA_CANDIDATES)
        self.assertEqual(set(loss),set(str(x) for x in LAMBDA_CANDIDATES))
        mod=[dict(row) for row in b]
        for row in mod:
            if row["day"]==3:row["flowers"]=list(reversed(row["flowers"]))
        _,train2=split_bouts(mod)
        lam2,loss2=choose_global_lambda(train2,self.dist)
        self.assertEqual(lam,lam2)
        self.assertEqual(loss,loss2)
    def test_holdout_same_bouts_without_false_inter_bout_transitions(self):
        b=synthetic_bouts()
        r=analyze_geo(b,self.dist,self.receipt,expected_day5=None)
        self.assertEqual(r["status"],"FITTED_HELDOUT_SOURCE_GEOMETRY_DESCRIPTIVE")
        self.assertEqual(r["heldout_pairs"],6*10*11)
        self.assertEqual(r["heldout_self_repeat_pairs"],0)
        self.assertEqual(r["primary_qualifying_bee_tags"],6)
        self.assertGreater(r["switch_primary_geo_to_geo_history_gain"]["mean_bee_equal_gain_nats"],0)
        self.assertTrue(all(
            math.isfinite(v) for v in
            r["switch_transition_model_mean_bee_equal_nll"].values()))
    def test_self_repeats_are_reported_and_not_mixed_with_switch_conditioning(self):
        b=synthetic_bouts()
        for row in b:
            if row["day"]==3:
                row["flowers"][2]=row["flowers"][1]
        r=analyze_geo(b,self.dist,self.receipt,expected_day5=None)
        self.assertGreater(r["heldout_self_repeat_pairs"],0)
        self.assertEqual(r["heldout_pairs"],
                         r["heldout_self_repeat_pairs"]+r["heldout_between_flower_pairs"])
        self.assertTrue(all(
            p["heldout_distinct_flower_pairs"]>=5 for p in r["per_bee"]))
    def test_population_reconciliation_not_silently_relaxed(self):
        b=synthetic_bouts()
        r=analyze_geo(b,self.dist,self.receipt)
        self.assertEqual(r["status"],"NO_GO_SOURCE_STAGE4_POPULATION_DISAGREEMENT")

if __name__=="__main__":unittest.main()
