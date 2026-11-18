from dataclasses import replace
import unittest
from sequential_floral_cues import Context,binary_observation,solve

class PolicyTests(unittest.TestCase):
    def ctx(self):return Context(.45,.9,.68,.85,.025,.035,.07,.08,.96)
    def test_bayes_calibration(self):
        for p in (0,.2,.5,.8,1):
            for a in (.5,.6,.95,1):
                o=binary_observation(p,a)
                self.assertAlmostEqual(sum(w for w,z in o),1)
                self.assertAlmostEqual(sum(w*z for w,z in o),p)
    def test_free_advance_is_not_worse(self):
        for prior in (.01,.4,.75,.99):
            for odor in (.5,.7,.99):
                c=replace(self.ctx(),prior_reward=prior,accuracy_scent=odor)
                r=solve(c)
                self.assertGreaterEqual(r['optimal_expected_payoff']+1e-10,r['bypass_far_cues_value'])
                self.assertGreaterEqual(r['optimal_expected_payoff']+1e-10,0)
                self.assertGreaterEqual(r['optimal_expected_payoff']+1e-10,max(r['forced_first_expected_payoff'].values()))
    def test_zero_landing_success_means_no_approach(self):
        r=solve(replace(self.ctx(),landing_success=0.))
        self.assertEqual(r['optimal_first_action'],'abandon')
        self.assertEqual(r['optimal_expected_payoff'],0.)
    def test_uninformative_paid_far_signal_never_first(self):
        c=replace(self.ctx(),accuracy_scent=.5)
        self.assertNotEqual(solve(c)['optimal_first_action'],'inspect_far_scent')
    def test_validity_checks(self):
        with self.assertRaises(ValueError):replace(self.ctx(),accuracy_scent=.49)
        with self.assertRaises(ValueError):replace(self.ctx(),cost_visual=-1.)

if __name__=='__main__':unittest.main()
