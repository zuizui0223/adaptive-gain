import unittest
from allocation import generate
from estimator import synthetic_outcomes
from source_contract import audit_future_source,synthetic_telemetry

def gate(a,rows):
    return audit_future_source(a,rows,{'calm':(.05,.15),'crosswind':(.95,1.05)},
                               {'informative':(19.5,20.5),'sham':(19.5,20.5)})

class SourceContractTests(unittest.TestCase):
    def test_all_eight_arms_have_measured_source_gates(self):
        a=generate(2,2);o=synthetic_outcomes(a,noise_sd=0.)
        raw=synthetic_telemetry(a,o)
        receipt,validated=gate(a,raw)
        self.assertEqual(receipt['status'],'SYNTHETIC_HARDWARE_QA_PASSED')
        self.assertEqual(len(validated),len(a))
        self.assertEqual(len(receipt['source_arms']),8)
    def test_predictive_graphic_at_release_invalidates_recency_control(self):
        a=generate(2,2);o=synthetic_outcomes(a,noise_sd=0.)
        raw=synthetic_telemetry(a,o)
        raw[0]['observed_predictive_graphics_at_release']=True
        with self.assertRaisesRegex(ValueError,'VISIBLE_AT_GATE'):gate(a,raw)
    def test_unequal_cue_duration_fails(self):
        a=generate(2,2);o=synthetic_outcomes(a,noise_sd=0.)
        raw=synthetic_telemetry(a,o)
        raw[0]['actual_first_off_s']=3.35
        with self.assertRaisesRegex(ValueError,'TIMING'):gate(a,raw)
    def test_real_zero_allowed_but_sensor_failure_is_not_zero(self):
        a=generate(2,2);o=synthetic_outcomes(a,noise_sd=0.)
        raw=synthetic_telemetry(a,o)
        raw[0]['sensor_status']='verified_no_intake'
        raw[0]['verified_consumed_sucrose_mg']=0.
        raw[0]['feeding_contact_verified']=False
        receipt,valid=gate(a,raw)
        self.assertEqual(valid[0]['verified_consumed_sucrose_mg'],0.)
        raw[0]['sensor_status']='sensor_failed'
        with self.assertRaisesRegex(ValueError,'SENSOR'):gate(a,raw)
    def test_fail_one_arm_even_if_pooled_compliance_high(self):
        a=generate(2,2);o=synthetic_outcomes(a,noise_sd=0.)
        raw=synthetic_telemetry(a,o)
        raw[0]['measured_wind_speed_m_s']=.3
        raw[0]['measured_wind_xyz_m_s']=[0.,.3,0.]
        receipt,validated=gate(a,raw)
        self.assertEqual(receipt['status'],'NO_GO_BELOW_EACH_ARM_98PCT_HARDWARE_ADHERENCE')
        self.assertIsNone(validated)
if __name__=='__main__':unittest.main()