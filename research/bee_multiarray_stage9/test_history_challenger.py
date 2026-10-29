"""Strict synthetic controls: no invented original bee outcomes in unit tests."""
from __future__ import annotations
from collections import Counter
import math
import unittest

from bout_grain import FLOWERS
from external_turn_transfer import (
    verify_source_plot_coordinates, source_bout_events, split_bouts,
    choose_array_lambdas, score_heldout, geo_destination_probs,
)
from history_challenger import (
    BETA, history_destination_probs, analyze_history_challenge,
    _per_bee_components, _check_parent_source,
)
from test_external_turn_transfer import synthetic_source


class HistoryChallengerTests(unittest.TestCase):
    def setUp(self):
        self.coords, _ = verify_source_plot_coordinates()

    def test_frozen_five_pseudocounts_renormalize_on_actual_three(self):
        geo = {"1": .2, "3": .3, "4": .5}
        history = Counter({("2", "1"): 3, ("2", "3"): 1,
                           ("2", "4"): 0, ("1", "2"): 99})
        p = history_destination_probs(geo, history, "2")
        self.assertAlmostEqual(p["1"], (3+5*.2)/9)
        self.assertAlmostEqual(p["3"], (1+5*.3)/9)
        self.assertAlmostEqual(p["4"], (0+5*.5)/9)
        self.assertAlmostEqual(sum(p.values()), 1.0)
        self.assertTrue(all(v>0 for v in p.values()))
        self.assertEqual(BETA,5)
        with self.assertRaisesRegex(ValueError, "BETA_WAS_RETUNED"):
            history_destination_probs(geo, history, "2", beta=1.0)
        with self.assertRaisesRegex(ValueError, "WRONG_REAL"):
            history_destination_probs({"1": .5, "3": .5}, history, "2")

    def test_zero_earlier_switches_exactly_equals_spatial_prior(self):
        geo={"1":.2,"3":.3,"4":.5}
        self.assertEqual(history_destination_probs(geo,Counter(),"2"),geo)

    def get_synthetic_evaluation(self, permutations=7):
        groups, source_receipt=source_bout_events(synthetic_source(bees=24))
        pop, exclude=split_bouts(groups,expected_original=False)
        self.assertFalse(exclude)
        lambdas, _=choose_array_lambdas(pop,self.coords)
        parent, unused_events=score_heldout(pop,self.coords,lambdas,require_source_support=True)
        del unused_events
        fake_parent={"original_heldout_comparisons_by_array": parent}
        result=analyze_history_challenge(
            pop,self.coords,lambdas,fake_parent,
            expected_original=False,permutations=permutations)
        return result,pop,lambdas,fake_parent

    def test_same_holdout_sample_four_models_and_parent_scores(self):
        result,pop,lambdas,parent=self.get_synthetic_evaluation()
        self.assertEqual(result["status"],"STAGE9B_POST_HOC_HISTORY_CHALLENGE_EVALUATED")
        self.assertEqual(set(result["source_array_results"]),{"1","2","3"})
        for array, score in result["source_array_results"].items():
            self.assertEqual(score["qualifying_bees"],24)
            self.assertEqual(score["original_colonies"],2)
            self.assertTrue(score["parent_original_direction_reconciled_exactly"])
            self.assertEqual(set(score["bee_equal_model_nll"]),
                             {"Mgeo","Mturn","Mhistory","Mhistory_turn"})
            self.assertGreater(score["genuine_heldout_triplets"],100)
            self.assertTrue(math.isfinite(score["colony_equal_direction_over_history_gain_nats"]))
            null=result["source_conditioned_permutation_null"][array]
            self.assertEqual(null["status"],"COMPUTED_SOURCE_CONDITIONAL_HISTORY_CHALLENGE_NULL")
            self.assertEqual(null["permutations"],7)
            self.assertAlmostEqual(null["actual_colony_equal_direction_over_history_nats"],
                                   score["colony_equal_direction_over_history_gain_nats"])

    def test_parent_score_mutation_fails_closed(self):
        result,pop,lambdas,parent=self.get_synthetic_evaluation(permutations=3)
        parent["original_heldout_comparisons_by_array"]["1"]["bee_equal_Mgeo_nll"] += .001
        with self.assertRaisesRegex(ValueError,"PARENT_DIRECTION_SCORE_CHANGED"):
            analyze_history_challenge(pop,self.coords,lambdas,parent,
                                      expected_original=False,permutations=3)

    def test_only_source_early_bouts_train_history_and_lambda(self):
        original=synthetic_source(bees=24)
        groups,_=source_bout_events(original)
        pop,_=split_bouts(groups,expected_original=False)
        lambdas,_=choose_array_lambdas(pop,self.coords)
        changed=[dict(r) for r in original]
        for r in changed:
            if r["bout"]>15:
                r["flower_sequence"]="0123412340"
        changed_groups,_=source_bout_events(changed)
        changed_pop,_=split_bouts(changed_groups,expected_original=False)
        lambda2,_=choose_array_lambdas(changed_pop,self.coords)
        self.assertEqual(lambdas,lambda2)
        for key in pop:
            self.assertEqual(pop[key]["train_switch_pairs"], changed_pop[key]["train_switch_pairs"])
            self.assertEqual(pop[key]["train_visits"],changed_pop[key]["train_visits"])
            self.assertLessEqual(pop[key]["train_source_max_bout"],15)
            self.assertGreaterEqual(pop[key]["test_source_min_bout"],16)
        # Predictive outcomes may change, but earlier training histories cannot.
        scores,_=_per_bee_components(pop,self.coords,lambdas)
        scores2,_=_per_bee_components(changed_pop,self.coords,lambda2)
        self.assertNotEqual(
            [x["Mhistory_nll"] for x in scores["1"]],
            [x["Mhistory_nll"] for x in scores2["1"]])

    def test_not_implicitly_using_all_possible_nonflower_options(self):
        coords=self.coords["1"]
        geo=geo_destination_probs({"1":.25,"2":.25,"3":.25,"4":.25},
                                  coords,"1",.25)
        hist=history_destination_probs(geo,Counter(),"1")
        self.assertEqual(set(hist),set(FLOWERS)-{"1"})
        self.assertAlmostEqual(sum(hist.values()),1)


if __name__=="__main__":
    unittest.main()
