import unittest
from allocation import generate
from telemetry import mock_telemetry, validate_traces
from estimator import estimate

class EstimatorTests(unittest.TestCase):
    def source(self,nc=12,nb=2):
        a=generate(nc,nb,seed=20261111)
        t=mock_telemetry(a)
        gate,valid=validate_traces(a,t,{'calm':(.05,.15),'crosswind':(.95,1.05)})
        assert valid is not None
        return a,valid
    def test_mock_accurate_policy_recovers_half_query_saving(self):
        a,v=self.source(12,2)
        d=estimate(a,v)
        self.assertAlmostEqual(d['precommit_minus_contingent_leaf_requests'],.5,delta=.05)
        self.assertEqual(d['actual_correct_target_rate_by_arm']['contingent'],1)
        self.assertEqual(d['actual_correct_target_rate_by_arm']['precommit'],1)
        self.assertEqual(d['n_independent_colonies'],12)
        self.assertEqual(d['n_fake_trial_assignments'],12*2*64)
        self.assertTrue(d['NO_REAL_ANIMAL_OUTCOMES'])
    def test_failure_to_query_does_not_drop_trial(self):
        a,v=self.source(2,2)
        v[0]['final_target_choice']='no_choice'
        v[0]['verified_consumed_sucrose_mg']=0
        d=estimate(a,v)
        self.assertEqual(d['status'],'SYNTHETIC_PILOT_ONLY_LT_12_COLONIES')
        self.assertEqual(d['n_fake_trial_assignments'],len(a))
    def test_incomplete_trial_outcome_fail_closed(self):
        a,v=self.source(2,2)
        with self.assertRaisesRegex(ValueError,'ALL_ASSIGNED'):estimate(a,v[:-1])

if __name__=='__main__':unittest.main()
