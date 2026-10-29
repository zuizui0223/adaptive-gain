import copy
import math
import unittest
from randomization import generate_allocation
from colony_contrast import (
    estimate_colony_order_wind_interaction,generate_synthetic_QA_outcomes
)

class ColonyIndependentCausalEstimatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.alloc=generate_allocation(n_colonies=12,bees_per_colony=4,seed=42)
        cls.mock=generate_synthetic_QA_outcomes(
            cls.alloc,delta=.03,seed=19,
            sigma_colony_delta=0.,sigma_bee_delta=0.,sigma_trial=.01)
    def test_one_colony_vs_many_sensor_trips_is_correct_inference_unit(self):
        result=estimate_colony_order_wind_interaction(self.alloc,self.mock)
        self.assertEqual(result["status"],"FITTED_COLONY_INDEPENDENT_ITTs")
        self.assertEqual(result["source_colonies"],12)
        self.assertEqual(result["bees"],48)
        self.assertEqual(result["randomized_trials_including_zero_drink"],3072)
        self.assertEqual(result["primary_t_df"],11)
        self.assertEqual(len(result["colony_level_effects"]),12)
        self.assertEqual(len(result["repeat_bee_level_effects"]),48)
    def test_synthetic_injected_interaction_recovers_at_colony_level(self):
        result=estimate_colony_order_wind_interaction(self.alloc,self.mock)
        self.assertAlmostEqual(result["colony_equal_primary_interaction_delta_mg_s"],
                               .03,delta=.004)
        self.assertTrue(0<=result["primary_two_sided_t_p"]<=1)
        self.assertLess(result["primary_student_t_95pct_CI_mg_s"][0],
                        result["colony_equal_primary_interaction_delta_mg_s"])
        self.assertGreater(result["primary_student_t_95pct_CI_mg_s"][1],
                           result["colony_equal_primary_interaction_delta_mg_s"])
    def test_verified_nonlanding_is_zero_NOT_missing_observation(self):
        source=[dict(x) for x in self.mock]
        source[0]={"trial_id":self.alloc[0]["trial_id"],
                   "sensor_status":"verified_no_intake",
                   "analysis_window_seconds":30,
                   "verified_consumed_sucrose_mg":0.0}
        result=estimate_colony_order_wind_interaction(self.alloc,source)
        self.assertEqual(result["randomized_trials_including_zero_drink"],len(source))
    def test_sensor_failure_cannot_be_recast_as_no_intake(self):
        source=[dict(x) for x in self.mock]
        source[0]["sensor_status"]="sensor_failed"
        with self.assertRaisesRegex(ValueError,"SENSOR_FAILURE"):
            estimate_colony_order_wind_interaction(self.alloc,source)
    def test_missing_randomized_trial_is_no_go_not_complete_case_analysis(self):
        with self.assertRaisesRegex(ValueError,"MISSING_OR_EXTRA"):
            estimate_colony_order_wind_interaction(self.alloc,self.mock[1:])
    def test_duplicate_original_trial_record_is_no_go(self):
        source=[dict(x) for x in self.mock]
        source[0]["trial_id"]=source[1]["trial_id"]
        with self.assertRaisesRegex(ValueError,"DUPLICATE_OR_UNKNOWN"):
            estimate_colony_order_wind_interaction(self.alloc,source)
    def test_negative_measured_sucrose_or_bad_clock_is_no_go(self):
        source=[dict(x) for x in self.mock]
        source[0]["verified_consumed_sucrose_mg"]=-1
        with self.assertRaisesRegex(ValueError,"NEGATIVE"):
            estimate_colony_order_wind_interaction(self.alloc,source)
        source=[dict(x) for x in self.mock]
        source[0]["analysis_window_seconds"]=29
        with self.assertRaisesRegex(ValueError,"NONSTANDARD"):
            estimate_colony_order_wind_interaction(self.alloc,source)
    def test_8_colonies_are_descriptive_pilot_not_population_effect(self):
        short=generate_allocation(8,4,seed=9)
        observations=generate_synthetic_QA_outcomes(short)
        result=estimate_colony_order_wind_interaction(short,observations)
        self.assertEqual(result["status"],"NO_GO_TOO_FEW_INDEPENDENT_COLONIES")
        self.assertTrue(result["no_general_p_value"])
        self.assertNotIn("primary_two_sided_t_p",result)
    def test_zero_between_colony_variability_is_not_falsely_certain(self):
        rows=generate_allocation(12,4,seed=9)
        vals=[{"trial_id":r["trial_id"],
               "analysis_window_seconds":30,
               "sensor_status":"measured",
               "verified_consumed_sucrose_mg":3}
              for r in rows]
        result=estimate_colony_order_wind_interaction(rows,vals)
        self.assertEqual(result["status"],
                         "NO_GO_NO_BETWEEN_COLONY_CONTRAST_VARIANCE")
    def test_zero_consumption_is_not_missing_and_fixed_30s_intention(self):
        rows=generate_allocation(12,4)
        vals=[{"trial_id":r["trial_id"],"analysis_window_seconds":30,
               "sensor_status":"verified_no_intake",
               "verified_consumed_sucrose_mg":0}
              for r in rows]
        result=estimate_colony_order_wind_interaction(rows,vals)
        self.assertEqual(result["status"],
                         "NO_GO_NO_BETWEEN_COLONY_CONTRAST_VARIANCE")

if __name__=="__main__":unittest.main()
