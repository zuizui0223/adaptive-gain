"""Independent source geometry rule transport controls (no original outcome lookup)."""
from __future__ import annotations
import json
import math
from pathlib import Path
import unittest
from external_turn_transfer import (
    verify_source_plot_coordinates,turn_cosine,
    static_prior,geo_destination_probs,directed_destination_probs,
    source_bout_events,split_bouts,choose_array_lambdas,score_heldout,
    permutation_null_by_array,jitter_plot_uncertainty,
    analyze,FROZEN_EXTERNAL_KAPPA
)

def synthetic_source(bees=24):
    # Distinct original source 4-flower sequences; with two path motifs
    # per bee, so a physical origin F2 has multiple incoming directions.
    forward="0123412340"
    backward="0432143210"
    samples=[]
    for bee in range(bees):
        for array in ("1","2","3"):
            for bout in range(1,21):
                x=forward if ((bee+bout)%2) else backward
                samples.append({
                    "colony":("A" if bee<bees//2 else "B"),
                    "bee":f"bee{bee}",
                    "array":array,"bout":bout,
                    "flower_sequence":x,
                    "source_file_row":len(samples)+2,
                    "eligible_strict_complete_nest_borders":True
                })
    return samples

class ThreeArrayDirectionTransferTests(unittest.TestCase):
    def setUp(self):
        self.coords,self.receipt=verify_source_plot_coordinates()
    def test_original_figure_labels_and_units_preserved(self):
        self.assertEqual(set(self.coords),{"1","2","3"})
        self.assertEqual(set(self.coords["1"]),{"1","2","3","4"})
        self.assertEqual(self.coords["1"]["1"],(6.0,2.0))
        self.assertEqual(self.coords["2"]["4"],(3.0,3.0))
        self.assertEqual(self.coords["3"]["2"],(.5,1.5))
        self.assertEqual(self.receipt["plot_absolute_error_per_coordinate_m"],.10)
        self.assertTrue(self.receipt["not_actual_tracked_bee_heading"])
    def test_array_labels_are_specific_physical_layout(self):
        self.assertNotEqual(self.coords["1"]["1"],self.coords["2"]["1"])
        self.assertNotEqual(self.coords["2"]["1"],self.coords["3"]["1"])
        self.assertAlmostEqual(turn_cosine(self.coords["1"],"1","2","3"),
                               turn_cosine(self.coords["1"],"1","2","3"))
        with self.assertRaisesRegex(ValueError,"ZERO_INCOMING_OR_OUTGOING"):
            turn_cosine(self.coords["1"],"1","1","2")
    def test_frozen_external_kappa_and_all_alternative_destinations_positive(self):
        prior=static_prior(["1","1","2","4"])
        self.assertAlmostEqual(sum(prior.values()),1)
        g=geo_destination_probs(prior,self.coords["1"],"2",0.25)
        t=directed_destination_probs(g,self.coords["1"],"1","2")
        self.assertEqual(set(g),{"1","3","4"})
        self.assertEqual(set(t),{"1","3","4"})
        self.assertTrue(all(v>0 for v in t.values()))
        self.assertAlmostEqual(sum(t.values()),1)
        self.assertEqual(FROZEN_EXTERNAL_KAPPA,1.0)
        with self.assertRaisesRegex(ValueError,"REESTIMATED_EXTERNAL"):
            directed_destination_probs(g,self.coords["1"],"1","2",kappa=0.5)
    def test_source_bout_boundary_is_not_invented(self):
        src=synthetic_source(bees=24)
        groups,receipt=source_bout_events(src)
        self.assertEqual(receipt["original_bouts"],24*3*20)
        self.assertEqual(receipt["valid_bouts"],24*3*20)
        self.assertEqual(receipt.get("excluded_nest_boundary_bouts",0),0)
        pop,exclusions=split_bouts(groups,expected_original=False)
        self.assertEqual(len(pop),24*3)
        self.assertFalse(exclusions)
        self.assertTrue(all(x["n_train_source_bouts"]==15 for x in pop.values()))
        self.assertTrue(all(x["n_test_source_bouts"]==5 for x in pop.values()))
        self.assertTrue(all(x["train_source_max_bout"]==15 for x in pop.values()))
        self.assertTrue(all(x["test_source_min_bout"]==16 for x in pop.values()))
    def test_sample_decoupled_from_final_five_bout_destinations(self):
        rows=synthetic_source(bees=24)
        groups,_=source_bout_events(rows)
        pop,_=split_bouts(groups,expected_original=False)
        l1,a1=choose_array_lambdas(pop,self.coords)
        changed=[dict(x) for x in rows]
        for record in changed:
            if record["bout"]>15:
                record["flower_sequence"]="0123412340"
        alt,_=source_bout_events(changed)
        p2,_=split_bouts(alt,expected_original=False)
        l2,a2=choose_array_lambdas(p2,self.coords)
        self.assertEqual(l1,l2)
        self.assertEqual(a1,a2)
    def test_model_scores_source_triplets_and_conditional_null(self):
        rows=synthetic_source(bees=24)
        groups,s=source_bout_events(rows)
        pop,ex=split_bouts(groups,expected_original=False)
        lambdas,train=choose_array_lambdas(pop,self.coords)
        r,events=score_heldout(pop,self.coords,lambdas,require_source_support=True)
        self.assertEqual(set(r),{"1","2","3"})
        for array in r:
            self.assertEqual(r[array]["status"],"HELDOUT_TEST_SUPPORT_PASS")
            self.assertEqual(r[array]["qualifying_original_individuals"],24)
            self.assertEqual(r[array]["original_colonies"],2)
            self.assertGreater(r[array]["original_source_test_genuine_triplets"],100)
            self.assertTrue(math.isfinite(r[array]["bee_equal_external_direction_gain_nats"]))
            self.assertEqual(len(r[array]["source_bee_scores"]),24)
        null=permutation_null_by_array(events,pop,self.coords,lambdas,r,
                                        permutations=9,seed=20261029)
        self.assertEqual(set(null),{"1","2","3"})
        self.assertTrue(all(n["status"].startswith(("COMPUTED_","NO_GO_")) for n in null.values()))
        self.assertTrue(all(n["permutations"]==9 for n in null.values()))
    def test_manual_plot_jitter_runs_declared_number_without_cherry_picking(self):
        rows=synthetic_source(bees=24)
        groups,_=source_bout_events(rows)
        p,_=split_bouts(groups,expected_original=False)
        jitter=jitter_plot_uncertainty(p,self.coords,replicates=2,seed=7)
        self.assertEqual(set(jitter),{"1","2","3"})
        self.assertTrue(all(v["source_figure_perturbations"]==2 for v in jitter.values()))
        self.assertTrue(all(v["minimum_bee_equal_gain_nats_across_jitter"]<=
                            v["maximum_bee_equal_gain_nats_across_jitter"]
                            for v in jitter.values()))
    def test_source_anomalies_are_excluded_only_from_actual_triplet_grain(self):
        src=synthetic_source(bees=24)
        src[0]["eligible_strict_complete_nest_borders"]=False
        src[0]["flower_sequence"]="02341"
        groups,receipt=source_bout_events(src)
        self.assertEqual(receipt["original_bouts"],24*3*20)
        self.assertEqual(receipt["valid_bouts"],24*3*20-1)
        self.assertEqual(receipt["excluded_nest_boundary_bouts"],1)
        p,bad=split_bouts(groups,expected_original=False)
        self.assertEqual(p[("A","bee0","1")]["n_train_source_bouts"],14)

if __name__=="__main__":unittest.main()
