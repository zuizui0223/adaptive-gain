import unittest
from estimator import estimate,synthetic_outcomes
from allocation import generate

class EstimatorTests(unittest.TestCase):
    def test_recency_equalized_DID_recovers_injected_mock(self):
        a=generate(12,4)
        o=synthetic_outcomes(a,effect_refreshed=.018,effect_sham=-.004,
                             colony_heterogeneity=.003,noise_sd=0.,seed=100)
        fit=estimate(a,o)
        self.assertEqual(fit['independent_colonies'],12)
        self.assertEqual(fit['assigned_trials'],12*4*64)
        self.assertEqual(fit['status'],'SYNTHETIC_QA_DESIGN_ESTIMATOR')
        self.assertAlmostEqual(fit['primary_refreshed_order_x_wind_delta'],.018,places=3)
        self.assertAlmostEqual(fit['secondary_sham_delta'],-.004,places=3)
        self.assertAlmostEqual(fit['secondary_refresh_difference'],.022,places=3)
        self.assertEqual(fit['primary_t_df'],11)
    def test_missing_sensor_is_not_a_measured_no_drink(self):
        a=generate(2,2);o=synthetic_outcomes(a,noise_sd=0.)
        o[0]['sensor_status']='hardware_failure'
        with self.assertRaisesRegex(ValueError,'SENSOR'):estimate(a,o)
    def test_verified_no_intake_stays_zero_in_full_ITT(self):
        a=generate(2,2);o=synthetic_outcomes(a,noise_sd=0.)
        o[0]['sensor_status']='verified_no_intake'
        o[0]['verified_consumed_sucrose_mg']=0.
        x=estimate(a,o)
        self.assertEqual(x['status'],'PILOT_ONLY_FEWER_THAN_12_COLONIES')
        self.assertTrue(x['includes_verified_zero_intake_trials'])
    def test_no_duplicate_or_unknown_trial(self):
        a=generate(2,2);o=synthetic_outcomes(a,noise_sd=0.)
        o[1]['trial_id']=o[0]['trial_id']
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):estimate(a,o)
if __name__=='__main__':unittest.main()