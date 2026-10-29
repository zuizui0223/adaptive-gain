"""Source-independent tests for frozen Stage9 cross-colony historical transfer.

Synthetic bee IDs, source action rows and original trip boundaries only.
Original empirical bytes are retrieved separately by GitHub Actions.
"""
from __future__ import annotations
import math
from pathlib import Path
import random
import sys
import unittest

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"bee_biomechanics_stage8"))
sys.path.insert(0,str(HERE.parent/"bee_biomechanics_stage8b"))

from test_heldout_experience_choice import fixture
from episode_audit import source_episode_audit
from heldout_experience_choice import true_visited_pairs,split_bee_source_trips
from cross_colony_transfer import (
    TREATMENTS,PREVIOUS,donor_effects,logit,invlogit,
    static_and_transferred_model,score_colony_transfer,analyze,
    _source_treatment
)

def source_fixture():
    raw=fixture(colonies=3,bees_per_colony=12,trips=10,
                episodes_per_trip=8)
    for row in raw:
        n=int(row["Bee"].rsplit("-",1)[-1])
        row["Treatment"]=TREATMENTS[n%3]
    episodes,quality=source_episode_audit(raw,source_expected=None)
    bybee,first,meta=true_visited_pairs(episodes,raw)
    bees,ex=split_bee_source_trips(bybee,first)
    return raw,episodes,quality,bees

class CrossColonyTransferTests(unittest.TestCase):
    def test_probability_expit_and_logit_are_valid_for_stable_rare_bees(self):
        for p in (0.00001,0.2,0.5,0.85,0.99999):
            self.assertAlmostEqual(invlogit(logit(p)),p,places=12)
    def test_original_trip_identity_and_all_three_synthetic_treatments(self):
        original,episodes,qa,bees=source_fixture()
        self.assertEqual(len(bees),36)
        self.assertEqual({b["colony"] for b in bees},{"1","2","3"})
        self.assertEqual(sum(len(b["test_pairs"]) for b in bees),756)
        self.assertEqual({ _source_treatment(x) for x in bees},set(TREATMENTS))
        self.assertTrue(all(len(b["train_pairs"])==49 for b in bees))
        self.assertTrue(all(len(b["test_pairs"])==21 for b in bees))
        self.assertTrue(all(
            {r["trip"] for r in b["train_pairs"]}.isdisjoint(
                {r["trip"] for r in b["test_pairs"]})
            for b in bees))
    def test_each_other_colony_donor_effect_and_source_support(self):
        original,episodes,qa,bees=source_fixture()
        for target in ("1","2","3"):
            delta,ledger=donor_effects(bees,target)
            self.assertEqual(ledger["status"],"PASS_DONOR_ONLY_TRAINING_SUPPORT")
            self.assertEqual(set(ledger["source_donor_colonies"]),{"1","2","3"}-{target})
            self.assertEqual(len(delta),6)
            self.assertTrue(all(math.isfinite(x) for x in delta.values()))
            for cell in ledger["source_cell_receipt"]:
                self.assertNotIn(target,cell["donor_source_colonies"])
                self.assertEqual(len(cell["donor_source_colonies"]),2)
                self.assertGreaterEqual(cell["donor_early_pairs_in_previous_orientation"],15)
    def test_source_target_bee_early_stationary_only_and_model_normalizes(self):
        original,episodes,qa,bees=source_fixture()
        donor,_=donor_effects(bees,"1")
        target=next(b for b in bees if b["colony"]=="1")
        model=static_and_transferred_model(target,donor)
        self.assertEqual(model["source_colony"],"1")
        self.assertEqual(model["source_early_pairs"],49)
        self.assertTrue(0<model["static"]<1)
        for v in PREVIOUS:
            self.assertTrue(0<model["cross_colony_transfer"][v]<1)
            self.assertAlmostEqual(
                model["cross_colony_transfer"][v],
                invlogit(logit(model["static"])+
                         model["donor_only_previous_orientation_delta"][v]))
    def test_donor_effect_does_not_look_at_target_colony_train_or_test(self):
        original,episodes,qa,bees=source_fixture()
        before,_=donor_effects(bees,"1")
        # This changes the entire target colony source *historical* and
        # future outcomes. The transferred delta must still be identical,
        # since it is derived only from the other two source colonies.
        tampered=[]
        for b in bees:
            if b["colony"]=="1":
                c=dict(b)
                c["train_pairs"]=[dict(x,next_horizontal=not x["next_horizontal"])
                                  for x in b["train_pairs"]]
                c["test_pairs"]=[dict(x,next_horizontal=not x["next_horizontal"])
                                 for x in b["test_pairs"]]
                tampered.append(c)
            else:
                tampered.append(b)
        after,_=donor_effects(tampered,"1")
        self.assertEqual(before,after)
    def test_donor_coverage_no_go_if_missing_one_treatment_colony(self):
        original,episodes,qa,bees=source_fixture()
        altered=[]
        for b in bees:
            if b["colony"]=="2" and _source_treatment(b)=="High Difference":
                # Change source treatment of an entire donor bee, train
                # and heldout, not just one row.
                x=dict(b)
                x["train_pairs"]=[
                    dict(v,source_treatment="Control") for v in b["train_pairs"]]
                x["test_pairs"]=[
                    dict(v,source_treatment="Control") for v in b["test_pairs"]]
                altered.append(x)
            else:altered.append(b)
        delta,receipt=donor_effects(altered,"1")
        self.assertIsNone(delta)
        self.assertEqual(receipt["status"],
                         "NO_GO_DONOR_TREATMENT_ORIENTATION_COVERAGE")
        self.assertTrue(any("High Difference" in x for x in receipt["reasons"]))
    def test_full_synthetic_three_colony_transfer_and_conditional_null(self):
        original,episodes,qa,bees=source_fixture()
        result=analyze(episodes,qa,original,
                       expected_original=False,permutations=19,seed=20261029)
        self.assertEqual(result["status"],
                         "COMPLETED_CROSSCOLONY_BEE_ORIENTATION_TRANSFER")
        score=result["source_actual_heldout_colony_transfer"]
        self.assertEqual(score["source_n_bees"],36)
        self.assertEqual(score["source_n_independent_colonies"],3)
        self.assertEqual(score["source_next_choice_events"],756)
        self.assertEqual(len(score["per_colony"]),3)
        self.assertAlmostEqual(
            score["M0_to_Mpersonal_colony_equal_gain"],
            result["original_36_bee_stage8_numerical_reconciliation"]
                  ["M0_to_Mpersonal_bee_gain"],places=12)
        null=result["original_segment_conditional_null"]
        self.assertIn(null["status"],(
            "COMPUTED_ORIGINAL_SOURCE_CROSSCOLONY_CONDITIONAL_LAG_NULL",
            "NO_GO_CONDITIONAL_EXCHANGEABILITY"))
        if null["status"].startswith("COMPUTED"):
            self.assertEqual(null["permutations_fixed_before_source_results"],19)
            self.assertEqual(len(null["source_per_colony_observed_minus_null"]),3)
            self.assertGreaterEqual(null["one_sided_positive_tail_conditional_p"],
                                    1/20)
    def test_treatments_are_fixed_per_bee_or_no_go(self):
        original,episodes,qa,bees=source_fixture()
        b=dict(bees[0])
        b["test_pairs"]=[
            *b["test_pairs"][:-1],
            dict(b["test_pairs"][-1],source_treatment="High Difference")]
        with self.assertRaisesRegex(ValueError,
                                    "NO_GO_EXPERIMENTAL_TREATMENT_CHANGED"):
            _source_treatment(b)

if __name__=="__main__":
    unittest.main()
