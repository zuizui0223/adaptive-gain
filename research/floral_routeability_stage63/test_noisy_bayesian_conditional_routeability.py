"""Stage63 mock-only exact finite Bayes tests, no actual bumblebee parameters."""
from fractions import Fraction as F
import unittest

from noisy_bayesian_conditional_routeability import (
  CueContext,SCENARIOS,CUES,prob_one,posterior,
  exact_adaptive,exact_fixed,router_direct_target_information_zero,
  context_run,run_all)

class ConstructedFloralNoisyCueBayesDecisionTests(unittest.TestCase):
    def test_four_world_router_zero_direct_target_information(self):
        c=SCENARIOS["moderate_noisy_router"]
        self.assertTrue(router_direct_target_information_zero(c))
        for y in (0,1):
            weights,p=posterior(((0,y),),c)
            self.assertEqual(sum(weights[i] for i in (0,2)),F(1,2))
            self.assertEqual(sum(weights[i] for i in (1,3)),F(1,2))
            self.assertEqual(p,F(1,2))

    def test_ideal_router_exact_analytic_cost_and_conditional_cue(self):
        c=SCENARIOS["high_reliability_both_terminals_ideal_router"]
        a=exact_adaptive(c)
        f=exact_fixed(c)
        self.assertEqual(a["minimal_expected_loss_exact"],F(1,5))
        self.assertEqual(f["minimal_expected_loss_exact"],F(3,10))
        self.assertEqual(a["initial_optimal_actions"],(CUES[0],))
        self.assertEqual(a["optimal_continuation_after_router"]["0"]["optimal_next_actions"],[CUES[1]])
        self.assertEqual(a["optimal_continuation_after_router"]["1"]["optimal_next_actions"],[CUES[2]])
        self.assertIn(tuple(CUES),f["optimal_fixed_cue_subsets"])
        self.assertEqual(len(f["all_fixed_subsets"]),8)

    def test_uninformative_router_removes_advantage_without_stripping_other_sensors(self):
        x=context_run("synthetic",SCENARIOS["uninformative_router"])
        self.assertEqual(x["adaptive_loss_advantage_exact"],"0")
        self.assertEqual(x["optimal_adaptive_expected_loss_exact"],"3/8")
        self.assertEqual(x["optimal_fixed_expected_loss_exact"],"3/8")
        self.assertNotIn(CUES[0],x["adaptive_initial_action_candidates"])

    def test_noisy_olfaction_collapse_not_claimed_as_real_wind_effect(self):
        x=context_run("construct only",SCENARIOS["olfactory_terminal_noisy_not_wind_calibrated"])
        self.assertEqual(x["adaptive_loss_advantage_exact"],"0")
        self.assertEqual(x["optimal_fixed_expected_loss_exact"],"3/8")
        self.assertTrue(x["stochastic_context_not_actual_wind_or_Bombus_parameters"])
        self.assertTrue(x["fixed_policy_uses_best_joint_Bayes_decoder_not_a_strawman"])

    def test_6_scenarios_exact_source_free_loss_phase_table(self):
        result=run_all()
        table={q["scenario_assumed_not_measured"]:q for q in result["counterexample_scenarios"]}
        self.assertEqual(len(table),6)
        self.assertEqual({k:v["adaptive_loss_advantage_exact"] for k,v in table.items()},
          {"high_reliability_both_terminals_ideal_router":"1/10",
           "moderate_noisy_router":"1/10",
           "uninformative_router":"0",
           "olfactory_terminal_noisy_not_wind_calibrated":"0",
           "visual_terminal_noisy_not_wind_calibrated":"1/100",
           "both_terminals_noisy_not_wind_calibrated":"0"})
        self.assertTrue(result["requires_randomized_first_cue_and_receiver_observed_next_query"])
        self.assertTrue(result["not_a_novel_Bayesian_decision_theorem"])
        self.assertTrue(result["no_causal_wind_odor_vision_or_pollen_effect_estimated"])

    def test_no_duplicate_queries_wrong_binary_outcomes_invalid_error_and_float(self):
        c=SCENARIOS["moderate_noisy_router"]
        with self.assertRaisesRegex(ValueError,"ACQUIRED_TWICE"):
            posterior(((0,0),(0,1)),c)
        with self.assertRaisesRegex(ValueError,"NOT_BINARY"):
            posterior(((0,2),),c)
        with self.assertRaisesRegex(ValueError,"OUT_OF_RANGE"):
            bad=CueContext(F(3,4),F(1,20),F(1,20),F(1,20),F(1,10),F(1,10))
            exact_fixed(bad)
        with self.assertRaisesRegex(ValueError,"FLOAT"):
            bad=CueContext(0.10,F(1,20),F(1,20),F(1,20),F(1,10),F(1,10))
            exact_adaptive(bad)

    def test_bayes_information_bound_adaptive_no_worse_than_fixed_grid(self):
        for re in (F(0),F(1,10),F(1,4),F(1,2)):
            for ve in (F(0),F(1,5),F(1,2)):
                for oe in (F(0),F(1,5),F(1,2)):
                    c=CueContext(re,ve,oe,F(1,20),F(1,10),F(1,10))
                    a=exact_adaptive(c)
                    f=exact_fixed(c)
                    self.assertLessEqual(a["minimal_expected_loss_exact"],
                                         f["minimal_expected_loss_exact"])
                    self.assertEqual(router_direct_target_information_zero(c),True)
if __name__=="__main__":unittest.main()
