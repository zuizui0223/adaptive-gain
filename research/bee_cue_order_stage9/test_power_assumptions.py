import math
import unittest
from power_assumptions import (
    ALPHA,COLONY_SCENARIOS,sd_of_colony_contrast,
    noncentral_t_power,power_table
)

class IndependentColonyProspectivePowerTests(unittest.TestCase):
    def test_exact_colony_contrast_sd_under_balanced_cells(self):
        sd=sd_of_colony_contrast(.025,.03,.08,bees=12,cell_trials=16)
        expected=math.sqrt(.025**2+.03**2/12+4*.08**2/(12*16))
        self.assertAlmostEqual(sd,expected)
        self.assertGreater(sd,.025)
    def test_zero_effect_exact_type_one_under_colony_t(self):
        sd=sd_of_colony_contrast(.025,.03,.08)
        for n in (8,12,24):
            self.assertAlmostEqual(noncentral_t_power(n,0.,sd),ALPHA,delta=1e-10)
    def test_power_increases_with_colonies_for_fixed_effect_and_variance(self):
        sd=sd_of_colony_contrast(.025,.03,.08)
        powers=[noncentral_t_power(c,.02,sd) for c in COLONY_SCENARIOS]
        self.assertTrue(all(x<y for x,y in zip(powers,powers[1:])))
        self.assertTrue(all(ALPHA<=p<=1 for p in powers))
    def test_power_increases_with_effect_and_decreases_with_colony_variance(self):
        sd=sd_of_colony_contrast(.025,.03,.08)
        sd_big=sd_of_colony_contrast(.04,.03,.08)
        self.assertLess(noncentral_t_power(24,.01,sd),
                        noncentral_t_power(24,.02,sd))
        self.assertLess(noncentral_t_power(24,.02,sd_big),
                        noncentral_t_power(24,.02,sd))
    def test_no_false_real_data_claims_and_exact_scenario_grid(self):
        report=power_table()
        self.assertEqual(report["status"],"ASSUMED_MODEL_ONLY_NO_LIVE_BEE_DATA")
        self.assertTrue(report["sample_size_targets_not_actual_recruited_animals"])
        self.assertTrue(report["gaussian_balanced_heteroscedasticity_and_zero_intake_NOT_MODELED"])
        self.assertEqual(len(report["all_power_cases"]),2*3*6)
        self.assertEqual(len(report["minimum_within_tested_grid"]),2*3)
        self.assertEqual({r["n_independent_colonies"] for r in report["all_power_cases"]},
                         set(COLONY_SCENARIOS))
        self.assertTrue(all(r["total_randomized_trials"]==
                            r["n_independent_colonies"]*12*16*4
                            for r in report["all_power_cases"]))
    def test_no_go_invalid_trial_or_colony_dispersion(self):
        with self.assertRaises(ValueError):sd_of_colony_contrast(0,0,0)
        with self.assertRaises(ValueError):noncentral_t_power(2,.02,.025)
        with self.assertRaises(ValueError):noncentral_t_power(12,.02,0)

if __name__=="__main__":unittest.main()
