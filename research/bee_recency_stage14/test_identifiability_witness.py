import math,unittest
from identifiability_witness import passive_choice,order_by_wind,witness

class IdentifiabilityWitnessTests(unittest.TestCase):
    def test_equal_final_refresh_does_not_rule_out_passive_wind_primacy(self):
        r=witness()
        self.assertTrue(r['passive_fixed_forced_cues_only'])
        self.assertTrue(r['latest_external_reward_handling_refresh_identical'])
        self.assertAlmostEqual(r['calm_order_effect_high_reward_choice'],0.,places=12)
        self.assertGreater(r['crosswind_order_effect_high_reward_choice'],.45)
        self.assertGreater(r['order_by_wind_intake_contrast_mg_s'],.018)
        self.assertLess(r['order_by_wind_intake_contrast_mg_s'],.019)
    def test_identical_passive_weights_have_zero_order_effect(self):
        x=order_by_wind(first_calm=1,second_calm=1,first_wind=1,
                        second_wind=1,last_refresh=10.,high=.34,low=.30)
        self.assertAlmostEqual(x['delta_mg_s'],0.,places=12)
    def test_simultaneous_last_refresh_cancels_from_order_difference(self):
        for extra in (0.,.1,1.,100.):
            a=passive_choice(2.,1.,extra,True)
            b=passive_choice(2.,1.,extra,False)
            self.assertAlmostEqual(a+b,1.,places=12)
            self.assertAlmostEqual(a-b,math.tanh(.5),places=12)
if __name__=='__main__':unittest.main()